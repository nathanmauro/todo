"""Telegram capture lane — a producer into the Notion Capture Inbox.

A @BotFather bot is polled with getUpdates (long-poll offset cursor, no public
endpoint, works behind NAT). Each inbound message becomes one Capture Inbox row
so the existing 15-min drain files it into Logseq — Telegram is NOT a second
writer to the graph. Voice notes are downloaded (OGG/Opus, <=20 MB) and
transcribed locally with whisper.cpp when configured. The bot replies
"filed ✓" to close the loop. The last update_id is the exactly-once cursor.

Token: login keychain (account 'telegram', service 'todo-cli') or
TELEGRAM_BOT_TOKEN. Only ONE process may poll a token at once (Telegram returns
409 otherwise) — fine here, the single launchd job owns it.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from . import notion
from .config import (
    KEYCHAIN_SERVICE,
    TELEGRAM_API,
    TELEGRAM_KEYCHAIN_ACCOUNT,
    TELEGRAM_STATE,
    WHISPER_BIN,
    WHISPER_MODEL,
)
from .storage import log


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


def pull_into_inbox(notion_tok: str) -> int:
    """Poll new Telegram messages and create a Capture Inbox row for each.

    Best-effort: returns the number of rows created; logs and returns 0 on any
    transport error so it never blocks the Notion drain. Advances the offset
    cursor only past messages it has handled.
    """
    tok = token()
    if not tok:
        return 0
    offset = int(_state().get("offset", 0))
    params = {"timeout": 0, "allowed_updates": json.dumps(["message"])}
    if offset:
        params["offset"] = offset + 1
    resp = _api(tok, "getUpdates", params)
    if not resp or not resp.get("ok"):
        return 0
    created = 0
    last_id = offset
    for upd in resp.get("result", []):
        last_id = upd["update_id"]
        msg = upd.get("message") or {}
        chat_id = (msg.get("chat") or {}).get("id")
        text = message_text(msg, tok)
        if text:
            pid = notion.create_row(notion_tok, text, source="telegram")
            if pid:
                created += 1
                if chat_id is not None:
                    _api(tok, "sendMessage",
                         {"chat_id": chat_id, "text": "filed ✓"})
        _save_offset(last_id)  # advance past every handled update
    if created:
        log(f"telegram pulled {created} capture(s) into Notion inbox")
    return created
