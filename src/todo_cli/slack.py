"""Slack transport: the replacement for the Telegram front door (2026-11-03).

Two directions, one Socket Mode app:

- Outbound: `send()` posts to a channel picked by *route* (capture, agents,
  digest, career, alerts, ...) through `chat.postMessage`. Buttons reuse the
  transport-neutral action registry (`telegram._new_action`), so a Slack tap
  writes the same ~/.todo/telegram-actions/<id>.json record that Job Scout's
  career_learning already reads for acks and snoozes.
- Inbound: `listen_forever()` holds a Socket Mode websocket (outbound only; no
  public endpoint, works behind NAT like the Telegram long poll). Messages in
  the capture channel or the bot DM become one Obsidian capture each; `+t` also
  pushes to Linear. Files are saved under Attachments/slack/, voice clips are
  transcribed locally. Button clicks execute the registered action exactly once.
  Slash commands (/claude, /sessions, /kill) hand off to the agent bridge.

Only the wire is Slack-specific. Classification, the Obsidian writer, the Linear
push, and the action executor are the same functions the Telegram lane uses; the
Telegram retirement slice moves them out of telegram.py.

Tokens: login keychain service 'todo-cli', accounts 'slack-bot' (xoxb-) and
'slack-app' (xapp-), or SLACK_BOT_TOKEN / SLACK_APP_TOKEN. Channel ids live in
~/.todo/slack-routes.json (never in code).
"""

from __future__ import annotations

import datetime as dt
import json
import mimetypes
import os
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

from . import obsidian
from . import telegram as core
from . import transcribe as _transcribe_mod
from .config import (
    KEYCHAIN_SERVICE,
    SLACK_ALLOWED_USERS,
    SLACK_API,
    SLACK_APP_KEYCHAIN_ACCOUNT,
    SLACK_BOT_KEYCHAIN_ACCOUNT,
    SLACK_ROUTES,
    SLACK_STATE,
)
from .models import now_iso
from .storage import log

# Routes every producer may name. A route missing from slack-routes.json falls
# back to "default" (see resolve_channel).
KNOWN_ROUTES = ("default", "capture", "agents", "digest", "career", "alerts")

# Slack caps: section text 3000 chars, 50 blocks, 25 elements per actions block,
# button label 75 chars. Plain `text` may run to 40k but truncates in clients.
_SECTION_LIMIT = 3000
_MAX_SECTIONS = 45
_MAX_BUTTONS = 25
_BUTTON_LABEL_LIMIT = 75
_SEEN_EVENT_LIMIT = 500
_ACTION_ID_PREFIX = "todo_action"
# Slack slash command -> agent-bridge grammar. Prefixed so they cannot collide
# with another app's /claude in the workspace.
SLASH_TO_BRIDGE = {"/cc": "/claude", "/cc-sessions": "/sessions", "/cc-kill": "/kill"}


# --- credentials -------------------------------------------------------------


def _keychain(account: str) -> str | None:
    try:
        out = subprocess.run(
            ["security", "find-generic-password", "-a", account, "-s", KEYCHAIN_SERVICE, "-w"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    secret = out.stdout.strip()
    return secret if out.returncode == 0 and secret else None


def bot_token() -> str | None:
    return os.environ.get("SLACK_BOT_TOKEN") or _keychain(SLACK_BOT_KEYCHAIN_ACCOUNT)


def app_token() -> str | None:
    return os.environ.get("SLACK_APP_TOKEN") or _keychain(SLACK_APP_KEYCHAIN_ACCOUNT)


# --- HTTP seam ---------------------------------------------------------------
# Tests replace `_http`; nothing else in this module touches urllib directly.


class SlackError(RuntimeError):
    pass


def _http(request: urllib.request.Request, timeout: float) -> tuple[int, dict[str, str], bytes]:
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            return resp.status, dict(resp.headers.items()), resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers.items()), exc.read()


def api(
    method: str,
    token: str,
    params: dict[str, Any] | None = None,
    *,
    form: bool = False,
    timeout: float = 30.0,
) -> dict:
    """Call one Web API method. Raises SlackError on transport or `ok: false`.

    Write methods take a JSON body; read methods (`form=True`) take form fields,
    which is what Slack accepts for them. One 429 retry honors Retry-After.
    """
    url = f"{SLACK_API}/{method}"
    headers = {"Authorization": f"Bearer {token}"}
    if form:
        body = urllib.parse.urlencode(params or {}).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    else:
        body = json.dumps(params or {}).encode()
        headers["Content-Type"] = "application/json; charset=utf-8"

    for attempt in range(2):
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            status, resp_headers, raw = _http(request, timeout)
        except (urllib.error.URLError, OSError, TimeoutError) as exc:
            raise SlackError(f"{method}: transport error: {exc}") from exc

        if status == 429 and attempt == 0:
            retry_after = _retry_after_seconds(resp_headers)
            log(f"slack {method}: rate limited, retrying in {retry_after}s")
            time.sleep(retry_after)
            continue
        break

    try:
        data = json.loads(raw.decode() or "{}")
    except ValueError as exc:
        raise SlackError(f"{method}: HTTP {status}, non-JSON body") from exc
    if not data.get("ok"):
        raise SlackError(f"{method}: {data.get('error') or f'HTTP {status}'}")
    return data


def _retry_after_seconds(headers: dict[str, str]) -> int:
    raw = next((v for k, v in headers.items() if k.lower() == "retry-after"), "1")
    try:
        return max(1, min(int(raw), 30))
    except ValueError:
        return 1


# --- routes ------------------------------------------------------------------


def load_routes() -> dict:
    try:
        data = json.loads(SLACK_ROUTES.read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def resolve_channel(route: str, routes: dict | None = None) -> str | None:
    """Map a producer's route name to a channel id.

    Unknown or unmapped routes deliver to the default channel rather than
    vanishing; a notification in the wrong room is visible, a dropped one is not.
    """
    routes = load_routes() if routes is None else routes
    table = routes.get("routes") or {}
    channel = table.get(route)
    if channel:
        return str(channel)
    default = routes.get("default") or table.get("default")
    if default and route != "default":
        log(f"slack: route {route!r} unmapped, using default channel")
    return str(default) if default else None


# --- outbound ----------------------------------------------------------------


def escape(text: str) -> str:
    """Escape the three characters Slack's mrkdwn reserves."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _chunks(text: str, limit: int) -> list[str]:
    """Split on line boundaries where possible, hard-cut a single long line."""
    chunks: list[str] = []
    current = ""
    for line in text.splitlines(keepends=True):
        while len(line) > limit:
            if current:
                chunks.append(current)
                current = ""
            chunks.append(line[:limit])
            line = line[limit:]
        if len(current) + len(line) > limit:
            chunks.append(current)
            current = ""
        current += line
    if current:
        chunks.append(current)
    return chunks or [""]


def build_blocks(text: str, buttons: list[tuple[str, str]] | None) -> list[dict]:
    """Section blocks for `text`, then one actions block of (label, action_id)."""
    sections = _chunks(escape(text), _SECTION_LIMIT)[:_MAX_SECTIONS]
    blocks: list[dict] = [
        {"type": "section", "text": {"type": "mrkdwn", "text": chunk or " "}} for chunk in sections
    ]
    if buttons:
        elements = [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": label[:_BUTTON_LABEL_LIMIT], "emoji": True},
                "action_id": f"{_ACTION_ID_PREFIX}_{index}",
                "value": action_id,
            }
            for index, (label, action_id) in enumerate(buttons[:_MAX_BUTTONS])
        ]
        blocks.append({"type": "actions", "block_id": "todo_actions", "elements": elements})
    return blocks


def send(
    text: str,
    route: str = "default",
    buttons: list[tuple[str, str, str]] | None = None,
    *,
    thread_ts: str | None = None,
    channel: str | None = None,
) -> dict | None:
    """Post `text` to the route's channel. Returns {"channel", "ts"} or None.

    `buttons` are (label, verb, payload) like telegram.send: each is registered
    in the shared action registry and rendered as a Block Kit button whose
    value is the action id. Failure is logged and returned as None so callers
    keep their own retry/queue semantics.
    """
    token = bot_token()
    if not token:
        log("slack send: no bot token (keychain todo-cli/slack-bot)")
        return None
    target = channel or resolve_channel(route)
    if not target:
        log(f"slack send: no channel for route {route!r} (configure {SLACK_ROUTES})")
        return None

    registered: list[tuple[str, str]] = []
    for label, verb, payload in buttons or []:
        action_id = core._new_action(verb, payload, label)
        if action_id:
            registered.append((label, action_id))

    params: dict[str, Any] = {
        "channel": target,
        "text": escape(text)[:3900],
        "unfurl_links": False,
        "unfurl_media": False,
    }
    if registered or len(text) > _SECTION_LIMIT:
        params["blocks"] = build_blocks(text, registered)
    if thread_ts:
        params["thread_ts"] = thread_ts

    try:
        data = api("chat.postMessage", token, params)
    except SlackError as exc:
        log(f"slack send ({route}): {exc}")
        _record_error("send", str(exc))
        return None
    _clear_error("send")
    return {"channel": data.get("channel", target), "ts": data.get("ts")}


# --- state -------------------------------------------------------------------


def _state() -> dict:
    try:
        data = json.loads(SLACK_STATE.read_text())
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _save_state(state: dict) -> None:
    try:
        SLACK_STATE.parent.mkdir(parents=True, exist_ok=True)
        SLACK_STATE.write_text(json.dumps(state, indent=2))
    except OSError as exc:
        log(f"slack: could not persist state: {exc}")


def _record_error(kind: str, detail: str) -> None:
    """Stamp the last failure so `todo slack-doctor` can surface it."""
    state = _state()
    state.setdefault("errors", {})[kind] = {"at": now_iso(), "detail": detail[:300]}
    _save_state(state)


def _clear_error(kind: str) -> None:
    state = _state()
    if kind in (state.get("errors") or {}):
        del state["errors"][kind]
        _save_state(state)


def _first_sighting(event_id: str | None) -> bool:
    """True the first time an event id is seen; Socket Mode can redeliver."""
    if not event_id:
        return True
    state = _state()
    seen = state.get("seen_events") or []
    if event_id in seen:
        return False
    seen.append(event_id)
    state["seen_events"] = seen[-_SEEN_EVENT_LIMIT:]
    _save_state(state)
    return True


# --- inbound: authorization and classification -------------------------------


def _locked() -> bool:
    return bool(SLACK_ALLOWED_USERS)


def _authorized(user_id: str | None) -> bool:
    return not _locked() or (user_id is not None and str(user_id) in SLACK_ALLOWED_USERS)


def is_capture_message(event: dict, routes: dict) -> bool:
    """Decide whether one Slack `message` event becomes an Obsidian capture.

    Top-level human messages (and file shares) in the capture channel or the bot
    DM are captures. Bot posts and edits/deletes never are, so the bot's own
    "filed" replies cannot loop. Thread replies count too: replying under a
    notification is the most natural place to jot a follow-up, and dropping it
    would lose the thought.
    """
    if event.get("type") != "message":
        return False
    if event.get("bot_id") or event.get("subtype") not in (None, "file_share", "thread_broadcast"):
        return False
    capture_channel = (routes.get("routes") or {}).get("capture")
    return event.get("channel_type") == "im" or (
        capture_channel is not None and event.get("channel") == capture_channel
    )


# --- inbound: files and voice ------------------------------------------------

_SAFE_FILENAME = re.compile(r"[^A-Za-z0-9._-]+")
_AUDIO_SUBTYPES = {"slack_audio"}


def _safe_filename(name: str, fallback: str) -> str:
    safe = _SAFE_FILENAME.sub("-", Path(name).name).strip(".-")
    return safe or fallback


def _is_audio(file: dict) -> bool:
    mimetype = str(file.get("mimetype") or "")
    return file.get("subtype") in _AUDIO_SUBTYPES or mimetype.startswith("audio/")


def _download_file(token: str, file: dict, folder: Path) -> dict[str, Any]:
    record: dict[str, Any] = {
        "slack_file_id": file.get("id"),
        "file_name": file.get("name"),
        "mime_type": file.get("mimetype"),
        "file_size": file.get("size"),
        "slack_subtype": file.get("subtype"),
        "downloaded": False,
    }
    url = file.get("url_private_download") or file.get("url_private")
    if file.get("mode") in {"tombstone", "external"} or not url:
        record["error"] = f"no downloadable bytes (mode={file.get('mode')})"
        return record

    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        status, headers, data = _http(request, 120)
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        record["error"] = f"download failed: {exc}"
        return record
    content_type = next((v for k, v in headers.items() if k.lower() == "content-type"), "")
    if status != 200 or content_type.startswith("text/html"):
        # Slack answers a missing files:read scope with an HTML login page.
        record["error"] = f"download refused (HTTP {status}, {content_type or 'no type'})"
        return record

    suffix = Path(str(file.get("name") or "")).suffix
    if not suffix and file.get("mimetype"):
        suffix = mimetypes.guess_extension(str(file["mimetype"])) or ""
    name = _safe_filename(str(file.get("name") or ""), f"slack-{file.get('id', 'file')}{suffix}")
    folder.mkdir(parents=True, exist_ok=True)
    destination = core._unique_path(folder / name)
    try:
        destination.write_bytes(data)
    except OSError as exc:
        record["error"] = f"write failed: {exc}"
        return record
    record.update(
        {"downloaded": True, "path": core._vault_relative(destination), "bytes": len(data)}
    )
    record["_abs_path"] = str(destination)
    return record


def _transcribe_first_audio(records: list[dict], files: list[dict]) -> str | None:
    for record, file in zip(records, files):
        if record.get("downloaded") and _is_audio(file):
            transcript = _transcribe_mod.transcribe(Path(record["_abs_path"]))
            if transcript:
                return transcript.strip()
            return "[voice clip received — no transcription engine produced text]"
    return None


def _attachments_body(records: list[dict]) -> str:
    lines = ["## Attachments"]
    for item in records:
        parts = [str(item.get("file_name") or item.get("slack_file_id") or "file")]
        if item.get("mime_type"):
            parts.append(str(item["mime_type"]))
        if item.get("file_size"):
            parts.append(f"{item['file_size']} bytes")
        if item.get("downloaded") and item.get("path"):
            parts.append(f"saved `{item['path']}`")
        elif item.get("error"):
            parts.append(f"not downloaded: {item['error']}")
        lines.append("- " + " | ".join(parts))
    return "\n".join(lines)


def _event_datetime(event: dict) -> dt.datetime:
    try:
        return dt.datetime.fromtimestamp(float(event.get("ts")), tz=dt.timezone.utc).astimezone()
    except (TypeError, ValueError, OSError, OverflowError):
        return dt.datetime.now().astimezone()


# --- inbound: capture --------------------------------------------------------


def file_message(event: dict, token: str) -> tuple[str, Path]:
    """Write one capture for a Slack message event; push `+t` tasks to Linear."""
    text = str(event.get("text") or "").strip()
    files = [f for f in event.get("files") or [] if isinstance(f, dict)]
    stamp = _event_datetime(event)
    folder = obsidian.attachments_root() / "slack" / stamp.strftime("%Y-%m-%d")
    records = [_download_file(token, f, folder) for f in files]

    if not text:
        text = _transcribe_first_audio(records, files) or ""
    if text:
        kind, body = core.classify(text)
    else:
        kind, body = "note", f"Slack file share received ({len(files)} file(s))"

    metadata = {
        "slack_channel": event.get("channel"),
        "slack_ts": event.get("ts"),
        "slack_thread_ts": event.get("thread_ts"),
        "slack_user": event.get("user"),
        "slack_attachment_count": len(records),
        "slack_downloaded_attachment_count": sum(1 for r in records if r.get("downloaded")),
    }
    for record in records:
        record.pop("_abs_path", None)
    path = obsidian.write_capture(
        body,
        kind=kind,
        source="slack",
        created=stamp.isoformat(timespec="seconds"),
        metadata={k: v for k, v in metadata.items() if v is not None},
        extra_body=_attachments_body(records) if records else None,
    )
    if kind == "task" and not core._push_task(body, source="slack"):
        core._LAST_PUSH_QUEUED.add(str(path))
    return kind, path


def _reply_text(kind: str, path: Path, user_id: str | None) -> str:
    message = f"filed ✓ {kind}"
    if kind == "task":
        if str(path) in core._LAST_PUSH_QUEUED:
            core._LAST_PUSH_QUEUED.discard(str(path))
            message += f" → saved locally, {core._task_backend_name()} push queued (see todo.log)"
        else:
            message += f" → {core._task_backend_name()}"
    message += f"\n{core._obsidian_deep_link(path)}"
    if not _locked():
        message += f"\nuser {user_id} — set SLACK_ALLOWED_USER_ID to this to lock the bot to you"
    return message


def handle_message_event(event: dict, routes: dict) -> str | None:
    """Route one message event. Returns the capture kind, or None if ignored."""
    if not is_capture_message(event, routes):
        log(
            "slack: ignored message"
            f" channel={event.get('channel')} channel_type={event.get('channel_type')}"
            f" subtype={event.get('subtype')} bot={bool(event.get('bot_id'))}"
        )
        return None
    user_id = event.get("user")
    if not _authorized(user_id):
        log(f"slack: dropped message from unauthorized user {user_id}")
        return None
    token = bot_token()
    if not token:
        log("slack: message arrived but no bot token to fetch files or reply")
        return None

    kind, path = file_message(event, token)
    thread = event.get("thread_ts") or event.get("ts")
    send(_reply_text(kind, path, user_id), channel=event.get("channel"), thread_ts=thread)
    return kind


# --- inbound: button clicks --------------------------------------------------


def handle_block_actions(payload: dict) -> list[str]:
    """Execute each clicked registry action once; collapse the buttons."""
    user_id = (payload.get("user") or {}).get("id")
    channel = (payload.get("channel") or {}).get("id")
    message = payload.get("message") or {}
    toasts: list[str] = []

    if not _authorized(user_id):
        log(f"slack: dropped button click from unauthorized user {user_id}")
        return toasts

    last_label = ""
    for clicked in payload.get("actions") or []:
        if not str(clicked.get("action_id", "")).startswith(_ACTION_ID_PREFIX):
            continue
        last_label = str((clicked.get("text") or {}).get("text") or "")
        action = core._load_action(str(clicked.get("value") or ""))
        if action is None:
            toast = "unknown or expired action"
        elif action.get("status") == "done":
            toast = "already done ✓"
        else:
            toast = core._execute_action(action, chat_id=channel, agent_allowed=_locked())
            core._mark_action(action["id"], "done", toast)
            log(f"slack action {action['id']} ({action.get('verb')}): {toast}")
        toasts.append(toast)

    if toasts and channel and message.get("ts"):
        _collapse_buttons(
            channel, message, f"{last_label} → {toasts[-1]}"
        )
    return toasts


def _collapse_buttons(channel: str, message: dict, note: str) -> None:
    token = bot_token()
    if not token:
        return
    blocks = [b for b in message.get("blocks") or [] if b.get("type") != "actions"]
    blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": escape(note)}]})
    try:
        api(
            "chat.update",
            token,
            {
                "channel": channel,
                "ts": message["ts"],
                "text": message.get("text", ""),
                "blocks": blocks,
            },
        )
    except SlackError as exc:
        log(f"slack: could not collapse buttons: {exc}")


# --- inbound: slash commands -> agent bridge ---------------------------------


def handle_slash_command(payload: dict) -> str:
    """Hand /claude, /sessions, /kill to the agent bridge. Returns ack text."""
    command = str(payload.get("command") or "")
    user_id = payload.get("user_id")
    if not _locked():
        return "agent commands require SLACK_ALLOWED_USER_ID (open mode)"
    if not _authorized(user_id):
        log(f"slack: refused {command} from unauthorized user {user_id}")
        return "not authorized"
    bridge_command = SLASH_TO_BRIDGE.get(command, command)
    if bridge_command not in core._agent_prefixes():
        return f"unknown command {command}"
    bridge = os.environ.get("TODO_AGENT_BRIDGE_CMD", "")
    if not bridge:
        return "agent bridge not configured (set TODO_AGENT_BRIDGE_CMD)"

    text = f"{bridge_command} {payload.get('text') or ''}".strip()
    args = [bridge, "--chat-id", str(payload.get("channel_id") or ""), "--text", text]
    try:
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError as exc:
        log(f"slack: agent bridge error: {exc}")
        return f"agent bridge failed: {exc}"
    return f"on it: {text}"


# --- Socket Mode loop --------------------------------------------------------


def handle_envelope(envelope: dict, ack: Callable[[dict], None], routes: dict) -> None:
    """Ack first (Slack redelivers after 3s), then do the slow work."""
    kind = envelope.get("type")
    envelope_id = envelope.get("envelope_id")
    payload = envelope.get("payload") or {}

    if kind == "slash_commands":
        ack({"envelope_id": envelope_id, "payload": {"text": handle_slash_command(payload)}})
        return
    if envelope_id:
        ack({"envelope_id": envelope_id})

    if kind == "events_api":
        if not _first_sighting(payload.get("event_id")):
            return
        event = payload.get("event") or {}
        if event.get("type") == "message":
            handle_message_event(event, routes)
    elif kind == "interactive" and payload.get("type") == "block_actions":
        handle_block_actions(payload)


def _open_socket_url(token: str) -> str:
    return str(api("apps.connections.open", token)["url"])


def run_socket_once(socket_factory: Callable[[str], Any] | None = None) -> str:
    """One websocket session; returns why it ended so the loop can log it."""
    token = app_token()
    if not token or not bot_token():
        return "no-token"
    if socket_factory is None:
        import websocket  # websocket-client; imported lazily so `notify` never needs it

        socket_factory = lambda url: websocket.create_connection(url, timeout=90)  # noqa: E731

    ws = socket_factory(_open_socket_url(token))
    routes = load_routes()
    try:
        while True:
            raw = ws.recv()
            if not raw:
                return "closed"
            envelope = json.loads(raw)
            if envelope.get("type") == "disconnect":
                return f"disconnect:{envelope.get('reason')}"
            if envelope.get("type") == "hello":
                routes = load_routes()
                continue
            try:
                handle_envelope(envelope, lambda body: ws.send(json.dumps(body)), routes)
            except Exception as exc:  # noqa: BLE001 — one bad event must not drop the socket
                log(f"slack: envelope {envelope.get('type')} failed: {exc}")
                _record_error("envelope", str(exc))
    finally:
        try:
            ws.close()
        except Exception:  # noqa: BLE001
            pass


def listen_forever() -> int:
    """Socket Mode daemon (launchd KeepAlive). Idles until both tokens exist."""
    backoff = 5
    while True:
        try:
            reason = run_socket_once()
            if reason == "no-token":
                time.sleep(60)
                continue
            log(f"slack: socket ended ({reason}); reconnecting")
            backoff = 5
        except Exception as exc:  # noqa: BLE001 — the daemon must not die
            log(f"slack listen error: {exc}")
            _record_error("listen", str(exc))
            time.sleep(backoff)
            backoff = min(backoff * 2, 120)


# --- doctor ------------------------------------------------------------------


def doctor() -> list[tuple[str, bool, str]]:
    """Read-only checks: (name, ok, detail). Never prints a secret."""
    checks: list[tuple[str, bool, str]] = []
    bot = bot_token()
    app = app_token()
    checks.append(
        (
            "bot token (xoxb)",
            bool(bot),
            "present" if bot else "missing: keychain todo-cli/slack-bot",
        )
    )
    checks.append(
        (
            "app token (xapp)",
            bool(app),
            "present" if app else "missing: keychain todo-cli/slack-app",
        )
    )

    routes = load_routes()
    mapped = sorted((routes.get("routes") or {}).keys())
    checks.append(
        (
            "routes file",
            bool(routes.get("default")),
            f"{SLACK_ROUTES} default={'set' if routes.get('default') else 'MISSING'} routes={mapped}",
        )
    )
    checks.append(
        ("user lock", _locked(), "locked" if _locked() else "open mode: set SLACK_ALLOWED_USER_ID")
    )

    if bot:
        try:
            who = api("auth.test", bot, form=True)
            checks.append(("auth.test", True, f"team={who.get('team')} bot={who.get('user')}"))
        except SlackError as exc:
            checks.append(("auth.test", False, str(exc)))

    for kind, info in sorted((_state().get("errors") or {}).items()):
        checks.append((f"last {kind} error", False, f"{info.get('at')} {info.get('detail')}"))
    return checks
