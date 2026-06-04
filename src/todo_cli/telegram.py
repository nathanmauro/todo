"""Telegram -> Obsidian capture lane (the live mobile front door, 2026-06-01).

A @BotFather bot is polled with getUpdates (long-poll offset cursor, no public
endpoint, works behind NAT). Each inbound message becomes ONE Markdown file in
the Obsidian vault under captures/YYYY-MM-DD/ (see obsidian.py) — the Obsidian
vault is the canonical store; there is no Notion/Logseq writer in this path.
"+t"/"+task" captures also push a single task to Todoist. Voice notes are
downloaded (OGG/Opus, <=20 MB) and transcribed locally with whisper.cpp when
configured. The bot replies "filed ✓" to close the loop, and persists the
sender chat_id so it can proactively message back (`todo telegram-send`). The
last update_id is the exactly-once offset cursor.

Token: login keychain (account 'telegram', service 'todo-cli') or
TELEGRAM_BOT_TOKEN. Only ONE process may poll a token at once (Telegram returns
409 otherwise) — fine here, the single launchd daemon owns it.
"""
from __future__ import annotations

import datetime as dt
import json
import mimetypes
import os
import re
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from . import obsidian, todoist
from .config import (
    KEYCHAIN_SERVICE,
    TELEGRAM_ALLOWED_CHATS,
    TELEGRAM_API,
    TELEGRAM_CHAT,
    TELEGRAM_KEYCHAIN_ACCOUNT,
    TELEGRAM_STATE,
    WHISPER_BIN,
    WHISPER_MODEL,
)
from .models import TodoEntry, TodoistSync, now_iso
from .storage import load_all, log, write_all


def token() -> str | None:
    env = os.environ.get("TELEGRAM_BOT_TOKEN")
    if env:
        return env
    try:
        r = subprocess.run(
            ["security", "find-generic-password",
             "-a", TELEGRAM_KEYCHAIN_ACCOUNT, "-s", KEYCHAIN_SERVICE, "-w"],
            capture_output=True, text=True, check=False,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except FileNotFoundError:
        pass
    return None


def _state() -> dict:
    try:
        return json.loads(TELEGRAM_STATE.read_text())
    except Exception:
        return {}


def _save_offset(update_id: int) -> None:
    TELEGRAM_STATE.parent.mkdir(parents=True, exist_ok=True)
    TELEGRAM_STATE.write_text(json.dumps({"offset": update_id}, indent=2))


def _api(tok: str, method: str, params: dict, timeout: float = 35.0) -> dict | None:
    url = f"{TELEGRAM_API}/bot{tok}/{method}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, ValueError) as exc:
        log(f"telegram {method} error: {exc}")
        return None


def _download(tok: str, file_id: str) -> Path | None:
    info = _api(tok, "getFile", {"file_id": file_id})
    if not info or not info.get("ok"):
        return None
    file_path = info["result"].get("file_path")
    if not file_path:
        return None
    url = f"{TELEGRAM_API}/file/bot{tok}/{file_path}"
    suffix = Path(file_path).suffix or ".oga"
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            data = resp.read()
        fd, tmp = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        return Path(tmp)
    except (urllib.error.URLError, OSError) as exc:
        log(f"telegram download error: {exc}")
        return None


_SAFE_FILENAME = re.compile(r"[^A-Za-z0-9._-]+")
_MESSAGE_META_KEYS = {
    "message_id",
    "message_thread_id",
    "from",
    "sender_chat",
    "sender_boost_count",
    "sender_business_bot",
    "date",
    "business_connection_id",
    "chat",
    "forward_origin",
    "is_topic_message",
    "is_automatic_forward",
    "reply_to_message",
    "external_reply",
    "quote",
    "reply_to_story",
    "via_bot",
    "edit_date",
    "has_protected_content",
    "media_group_id",
    "author_signature",
    "text",
    "entities",
    "link_preview_options",
    "effect_id",
    "caption",
    "caption_entities",
    "show_caption_above_media",
    "has_media_spoiler",
    "reply_markup",
}


def _message_datetime(msg: dict) -> dt.datetime:
    raw = msg.get("date")
    if isinstance(raw, int | float):
        try:
            return dt.datetime.fromtimestamp(raw, tz=dt.timezone.utc).astimezone()
        except (OSError, OverflowError, ValueError):
            pass
    return dt.datetime.now().astimezone()


def _safe_filename(name: str) -> str:
    safe = _SAFE_FILENAME.sub("-", Path(name).name).strip(".-")
    return safe or "telegram-file"


def _unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for i in range(2, 1000):
        candidate = path.with_name(f"{path.stem}-{i}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise OSError(f"could not allocate unique attachment path for {path}")


def _vault_relative(path: Path) -> str:
    try:
        return str(path.relative_to(obsidian.OBSIDIAN_VAULT))
    except ValueError:
        return str(path)


def _content_types(msg: dict) -> list[str]:
    found: list[str] = []
    if msg.get("text"):
        found.append("text")
    if msg.get("caption"):
        found.append("caption")
    for key, value in msg.items():
        if key in _MESSAGE_META_KEYS:
            continue
        if value in (None, "", [], {}):
            continue
        found.append(key)
    return found or ["message"]


def _message_content(msg: dict) -> dict[str, Any]:
    return {
        key: value
        for key, value in msg.items()
        if key not in _MESSAGE_META_KEYS and value not in (None, "", [], {})
    }


def _iter_file_refs(value: Any, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        file_id = value.get("file_id")
        if isinstance(file_id, str) and file_id:
            ref = {
                "file_id": file_id,
                "file_unique_id": value.get("file_unique_id"),
                "file_name": value.get("file_name"),
                "mime_type": value.get("mime_type"),
                "file_size": value.get("file_size"),
                "telegram_field": path[0] if path else "message",
                "telegram_path": ".".join(path),
            }
            yield ref
        for key, nested in value.items():
            yield from _iter_file_refs(nested, (*path, str(key)))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            yield from _iter_file_refs(item, (*path, str(i)))


def _file_refs(msg: dict) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for ref in _iter_file_refs(_message_content(msg)):
        identity = str(ref.get("file_unique_id") or ref["file_id"])
        if identity in seen:
            continue
        seen.add(identity)
        refs.append(ref)
    return refs


def _attachment_filename(
    ref: dict[str, Any], info: dict[str, Any], index: int
) -> str:
    source_name = str(
        ref.get("file_name") or info.get("file_path") or ref["telegram_field"]
    )
    safe_name = _safe_filename(source_name)
    suffix = Path(safe_name).suffix or Path(str(info.get("file_path", ""))).suffix
    if not suffix and ref.get("mime_type"):
        suffix = mimetypes.guess_extension(str(ref["mime_type"])) or ""
    if Path(safe_name).suffix:
        return safe_name
    identity = str(ref.get("file_unique_id") or ref["file_id"])[:10]
    stem = f"{Path(safe_name).stem}-{index:02d}-{identity}".strip("-")
    return _safe_filename(stem + suffix)


def _download_attachment(
    tok: str, ref: dict[str, Any], folder: Path, index: int
) -> dict[str, Any]:
    record = {
        "telegram_field": ref["telegram_field"],
        "telegram_path": ref["telegram_path"],
        "file_id": ref["file_id"],
        "file_unique_id": ref.get("file_unique_id"),
        "file_name": ref.get("file_name"),
        "mime_type": ref.get("mime_type"),
        "file_size": ref.get("file_size"),
        "downloaded": False,
    }
    info = _api(tok, "getFile", {"file_id": ref["file_id"]})
    if not info or not info.get("ok"):
        record["error"] = "getFile failed"
        return record
    result = info.get("result") or {}
    file_path = result.get("file_path")
    if not file_path:
        record["error"] = "getFile returned no file_path"
        return record

    folder.mkdir(parents=True, exist_ok=True)
    filename = _attachment_filename(ref, result, index)
    destination = _unique_path(folder / filename)
    url = f"{TELEGRAM_API}/file/bot{tok}/{file_path}"
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            data = resp.read()
        destination.write_bytes(data)
    except (urllib.error.URLError, OSError) as exc:
        log(f"telegram attachment download error: {exc}")
        record["error"] = str(exc)
        return record

    record.update({
        "downloaded": True,
        "path": _vault_relative(destination),
        "bytes": len(data),
    })
    return record


def _transcribe(audio: Path) -> str | None:
    """OGG/Opus -> 16k mono WAV (ffmpeg) -> text (whisper.cpp). None if unset."""
    if not WHISPER_MODEL:
        return None
    wav = audio.with_suffix(".wav")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(audio), "-ar", "16000", "-ac", "1",
             "-f", "wav", str(wav)],
            capture_output=True, check=True,
        )
        r = subprocess.run(
            [WHISPER_BIN, "-m", WHISPER_MODEL, "-f", str(wav), "-nt", "-np"],
            capture_output=True, text=True, check=True,
        )
        return " ".join(r.stdout.split()).strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        log(f"transcribe error: {exc}")
        return None
    finally:
        wav.unlink(missing_ok=True)


def message_text(msg: dict, tok: str) -> str | None:
    """Extract capture text from a message: text/caption, or transcribed voice."""
    if msg.get("text"):
        return msg["text"].strip()
    voice = msg.get("voice") or msg.get("audio")
    if voice and voice.get("file_id"):
        audio = _download(tok, voice["file_id"])
        if audio:
            try:
                tx = _transcribe(audio)
            finally:
                audio.unlink(missing_ok=True)
            if tx:
                return tx
            return "[voice note received — set TODO_WHISPER_MODEL to transcribe]"
    if msg.get("caption"):
        return msg["caption"].strip()
    return None


def _chat_state() -> dict:
    try:
        return json.loads(TELEGRAM_CHAT.read_text())
    except Exception:
        return {}


def _save_chat_id(chat_id) -> None:
    """Persist the most recent sender chat_id so the bot can message back.

    Best-effort: a write failure must never break the capture path. The last
    writer wins — captures come from one chat in practice, and `telegram-send`
    only needs *a* reachable chat.
    """
    if chat_id is None:
        return
    try:
        TELEGRAM_CHAT.parent.mkdir(parents=True, exist_ok=True)
        TELEGRAM_CHAT.write_text(json.dumps({"chat_id": chat_id}, indent=2))
    except OSError as exc:
        log(f"telegram: could not persist chat_id: {exc}")


def last_chat_id() -> int | str | None:
    """The most recently seen sender chat_id, or None if none has been stored."""
    return _chat_state().get("chat_id")


def send(text: str) -> bool:
    """Send `text` to the last-persisted chat via the bot. Returns success.

    Delivery enabler: turns the capture bot into a two-way channel so other
    tooling (or Nathan, via `todo telegram-send`) can push a notification to the
    phone. No-op (returns False) when there is no token or no known chat.
    """
    tok = token()
    if not tok:
        log("telegram send: no token")
        return False
    chat_id = last_chat_id()
    if chat_id is None:
        log("telegram send: no chat_id yet (message the bot once first)")
        return False
    resp = _api(tok, "sendMessage", {"chat_id": chat_id, "text": text})
    return bool(resp and resp.get("ok"))


# --- Obsidian-canonical capture lane (live path, 2026-06-01) ----------------
# A message becomes one Markdown file in the vault; tasks also push to Todoist.

_PREFIXES = {"+t": "task", "+task": "task", "+i": "idea", "+idea": "idea"}


def classify(text: str) -> tuple[str, str]:
    """Map a raw message to (kind, body). DEFAULT classifier = prefix parser.

    "+t "/"+task " -> task, "+i "/"+idea " -> idea, anything else -> note. The
    prefix token (and the space after it) is stripped from the body; a bare
    "+t" with no body falls back to a plain note so an empty task is never made.

    This is the SWAPPABLE SEAM: a future LLM / Black Box classifier (see the
    vault's 06 Backlog/llm-classifier-for-telegram-captures) can replace this
    body wholesale, and tests/test_telegram_obsidian.py pins the contract it
    must keep.
    """
    stripped = text.strip()
    head, _, rest = stripped.partition(" ")
    kind = _PREFIXES.get(head.lower())
    if kind and rest.strip():
        return kind, rest.strip()
    return "note", stripped


def _push_task(text: str, source: str = "telegram") -> bool:
    """Create ONE Todoist task for a captured task, without touching Logseq.

    Pushes only this task (not a full `todo sync`, which would flush unrelated
    pending rows), records it in the local store with the Todoist id stamped so
    it is never re-pushed, and ensures the source label exists first. Swallows
    every error — the vault file is the canonical record regardless.
    """
    try:
        tok = todoist.token()
        if not tok:
            log("telegram task: no todoist token; saved to vault only")
            return False
        todoist.ensure_label(tok, source)
        task = todoist.create_task(
            tok, text, project_id=todoist.TODOIST_PROJECT_ID, labels=[source]
        )
        tid = str(task.get("id", ""))
        entries = load_all()
        entry = TodoEntry(text=text, source=source)
        entry.sync.todoist = TodoistSync(
            task_id=tid,
            url=f"https://app.todoist.com/app/task/{tid}",
            ts=now_iso(),
        )
        entries.append(entry)
        write_all(entries)
        return True
    except Exception as exc:  # noqa: BLE001 — a capture must survive a bad push
        log(f"telegram task -> todoist failed: {exc}")
        return False


def _route(text: str, source: str = "telegram") -> tuple[str, Path]:
    """Classify, write the capture file, and (for tasks) push to Todoist."""
    kind, body = classify(text)
    path = obsidian.write_capture(body, kind=kind, source=source)
    if kind == "task":
        _push_task(body, source=source)
    return kind, path


def _default_message_body(content_types: list[str]) -> str:
    label = ", ".join(content_types)
    return f"Telegram {label} received"


def _extra_body(
    msg: dict, content_types: list[str], attachments: list[dict[str, Any]]
) -> str:
    sections: list[str] = []
    if attachments:
        lines = ["## Attachments"]
        for item in attachments:
            name = (
                item.get("file_name")
                or Path(str(item.get("path", ""))).name
                or item["telegram_field"]
            )
            parts = [str(name)]
            if item.get("mime_type"):
                parts.append(str(item["mime_type"]))
            if item.get("file_size"):
                parts.append(f"{item['file_size']} bytes")
            if item.get("downloaded") and item.get("path"):
                parts.append(f"saved `{item['path']}`")
            elif item.get("error"):
                parts.append(f"not downloaded: {item['error']}")
            lines.append("- " + " | ".join(parts))
        sections.append("\n".join(lines))

    metadata = {
        "content_types": content_types,
        "message": _message_content(msg),
        "attachments": attachments,
    }
    sections.append(
        "## Telegram Metadata\n"
        "```json\n"
        f"{json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True)}\n"
        "```"
    )
    return "\n\n".join(sections)


def _route_message(
    msg: dict, tok: str, source: str = "telegram"
) -> tuple[str, Path]:
    """Route any authorized Telegram message into the vault without dropping it."""
    text = message_text(msg, tok)
    content_types = _content_types(msg)
    stamp = _message_datetime(msg)
    attachment_folder = (
        obsidian.attachments_root() / "telegram" / stamp.strftime("%Y-%m-%d")
    )
    attachments = [
        _download_attachment(tok, ref, attachment_folder, i)
        for i, ref in enumerate(_file_refs(msg), start=1)
    ]

    if text and not attachments and set(content_types) <= {"text", "caption"}:
        return _route(text, source=source)

    kind, body = classify(text) if text else (
        "note", _default_message_body(content_types)
    )
    path = obsidian.write_capture(
        body,
        kind=kind,
        source=source,
        created=stamp.isoformat(timespec="seconds"),
        metadata={
            "telegram_message_id": msg.get("message_id"),
            "telegram_chat_id": (msg.get("chat") or {}).get("id"),
            "telegram_content_types": content_types,
            "telegram_attachment_count": len(attachments),
            "telegram_downloaded_attachment_count": sum(
                1 for item in attachments if item.get("downloaded")
            ),
        },
        extra_body=_extra_body(msg, content_types, attachments),
    )
    if kind == "task":
        _push_task(body, source=source)
    return kind, path


def _reply(tok: str, chat_id, kind: str, locked: bool) -> None:
    msg = f"filed ✓ {kind}" + (" → Todoist" if kind == "task" else "")
    if not locked:
        msg += (
            f"\nchat_id {chat_id} — set TELEGRAM_ALLOWED_CHAT_ID to this "
            "to lock the bot to you"
        )
    _api(tok, "sendMessage", {"chat_id": chat_id, "text": msg})


def poll_once(long_poll: bool = False) -> int:
    """One getUpdates pass: route each authorized message into the vault.

    Advances the exactly-once offset cursor past every handled update (even
    dropped/unauthorized ones, so they aren't reprocessed). Returns the number
    of messages filed. `long_poll=True` waits up to 25s server-side (daemon
    loop); False returns immediately (one-shot / cron / chat_id bootstrap).
    """
    tok = token()
    if not tok:
        return 0
    offset = int(_state().get("offset", 0))
    params = {
        "timeout": 25 if long_poll else 0,
        "allowed_updates": json.dumps(["message"]),
    }
    if offset:
        params["offset"] = offset + 1
    resp = _api(tok, "getUpdates", params)
    if not resp or not resp.get("ok"):
        return 0
    locked = bool(TELEGRAM_ALLOWED_CHATS)
    filed = 0
    for upd in resp.get("result", []):
        last_id = upd["update_id"]
        msg = upd.get("message") or {}
        chat_id = (msg.get("chat") or {}).get("id")
        try:
            if locked and str(chat_id) not in TELEGRAM_ALLOWED_CHATS:
                log(f"telegram: dropped msg from unauthorized chat {chat_id}")
                continue
            # Remember who we're talking to so the bot can message back later
            # (`todo telegram-send`). Done for every authorized message, even one
            # with no capturable text (e.g. a "/start"), so the channel opens on
            # first contact.
            _save_chat_id(chat_id)
            kind, _ = _route_message(msg, tok)
            filed += 1
            if chat_id is not None:
                _reply(tok, chat_id, kind, locked)
        finally:
            _save_offset(last_id)  # advance past every handled update
    if filed:
        log(f"telegram filed {filed} capture(s) into the vault")
    return filed


def poll_loop() -> int:
    """Long-poll forever (launchd KeepAlive daemon).

    Idles cheaply until a token exists, so storing the BotFather token later
    activates the bot with no reload. Never raises out: transport errors are
    logged and retried with capped backoff.
    """
    import time

    backoff = 5
    while True:
        try:
            if not token():
                time.sleep(60)
                continue
            poll_once(long_poll=True)
            backoff = 5
        except Exception as exc:  # noqa: BLE001 — the daemon must not die
            log(f"telegram poll loop error: {exc}")
            time.sleep(backoff)
            backoff = min(backoff * 2, 120)
