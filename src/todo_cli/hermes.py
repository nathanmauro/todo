"""Slack #hermes line: forward Nathan's messages to the local Hermes desk agent (2026-11-22).

The Cockpit bot stays the only Socket Mode listener (Slack hands each event to just one connection
per app), so Hermes never touches Slack. Messages in the `hermes` route's channel skip capture
filing, go to the Hermes API server on 127.0.0.1, and the reply posts back in the same thread.
Each Slack thread is one Hermes session (`X-Hermes-Session-Id`).

Trust: only the allowlisted Slack user is forwarded, and the line refuses to run in open mode.
Hermes cannot write. Its desk MCP tools (cockpit agents/hermes/desk_mcp.py) only *stage* one
`herd send` / `todo add` per thread under pending/<session>.json; this module shows Nathan the exact
action and runs it itself when his next message in that thread is a bare "yes". Anything else
cancels it. The turn file tells the MCP server which thread is in flight; calls are serialized so
it is always the current one.
"""

from __future__ import annotations

import html
import json
import os
import re
import threading
import subprocess
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

from .config import SLACK_ALLOWED_USERS, TODO_DIR
from .storage import log

HERMES_URL = os.environ.get("TODO_HERMES_URL", "http://127.0.0.1:8642")
HERMES_KEY_FILE = Path(
    os.environ.get("TODO_HERMES_KEY_FILE", Path.home() / ".config/cockpit/hermes-desk.key")
)
HERMES_DIR = Path(os.environ.get("HERMES_LINE_DIR", TODO_DIR / "hermes"))
TURN_FILE = HERMES_DIR / "turn.json"
PENDING_DIR = HERMES_DIR / "pending"
PENDING_TTL = 10 * 60
CONFIRM_WORDS = {"yes", "y", "yes.", "send", "send it", "do it"}
HERMES_TIMEOUT = int(os.environ.get("TODO_HERMES_TIMEOUT", "300"))
HERMES_ROUTE = "hermes"

TAB_ID = re.compile(r"^t[0-9a-z]{2,6}$")
PROJECT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _.-]{0,59}$")
TOOL_PATH = ":".join(
    [str(Path.home() / ".local/bin"), "/opt/homebrew/bin", "/usr/local/bin", "/usr/bin", "/bin"]
)

DOWN_TEXT = "Hermes is down. (The desk gateway on this Mac isn't answering; captures still work.)"

_call_lock = threading.Lock()


def hermes_channel(routes: dict) -> str | None:
    channel = (routes.get("routes") or {}).get(HERMES_ROUTE)
    return str(channel) if channel else None


def is_hermes_message(event: dict, routes: dict) -> bool:
    channel = hermes_channel(routes)
    return bool(channel) and event.get("channel") == channel


def accepts(event: dict) -> bool:
    """Only Nathan's own plain messages. Open mode (no allowlist) forwards nothing."""
    if event.get("bot_id") or event.get("app_id"):
        return False
    if event.get("subtype") not in (None, "thread_broadcast"):
        return False
    if not SLACK_ALLOWED_USERS:
        return False
    return str(event.get("user") or "") in SLACK_ALLOWED_USERS


def session_id(event: dict) -> str:
    thread = event.get("thread_ts") or event.get("ts") or "0"
    return f"slack-{event.get('channel')}-{thread}"


def slack_to_text(text: str) -> str:
    """Undo Slack's entity escaping and link wrapping so Hermes sees what Nathan typed."""
    text = re.sub(r"<(https?://[^|>]+)\|([^>]+)>", r"\2 (\1)", text)
    text = re.sub(r"<(https?://[^>]+)>", r"\1", text)
    return html.unescape(text).strip()


def to_slack(text: str) -> str:
    """Markdown bold to Slack bold, headings to bold lines, links unmasked so URLs show."""
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r"\1 (\2)", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"*\1*", text)
    text = re.sub(r"^#{1,6}\s+(.+)$", r"*\1*", text, flags=re.M)
    return text.strip()


def _write_turn(sid: str) -> None:
    HERMES_DIR.mkdir(parents=True, exist_ok=True)
    tmp = TURN_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps({"ts": time.time(), "session": sid}))
    tmp.replace(TURN_FILE)


def _end_turn() -> None:
    TURN_FILE.unlink(missing_ok=True)


# --- staged writes ---------------------------------------------------------------------------


def _pending_path(sid: str) -> Path:
    return PENDING_DIR / f"{sid}.json"


def take_pending(sid: str) -> dict | None:
    """Pop this thread's staged action; expired or unreadable records are dropped."""
    path = _pending_path(sid)
    try:
        record = json.loads(path.read_text())
    except (OSError, ValueError):
        path.unlink(missing_ok=True)
        return None
    path.unlink(missing_ok=True)
    if time.time() - float(record.get("ts", 0)) > PENDING_TTL:
        return None
    return record


def _plain_line(text: str, limit: int) -> bool:
    if not text or len(text) > limit or not text[0].isalnum():
        return False
    return not any(
        ch == "`" or unicodedata.category(ch) in ("Cc", "Cf", "Zl", "Zp") for ch in text
    )


def validate(record: dict) -> str | None:
    """Re-check a staged action here; the MCP server's checks are not trusted alone."""
    kind = record.get("kind")
    text = str(record.get("text", ""))
    if kind == "herd_send":
        if not TAB_ID.match(str(record.get("tab", ""))) or not _plain_line(text, 400):
            return "invalid herd send"
        return None
    if kind == "todo_add":
        project = str(record.get("project", ""))
        if not _plain_line(text, 200) or (project and not PROJECT.match(project)):
            return "invalid todo"
        return None
    return f"unknown action {kind!r}"


def _tab_title(tab: str) -> str:
    listing = _tool(["herd", "ls"])
    for line in listing.splitlines():
        if line.startswith(tab + " "):
            return line[len(tab) :].strip()
    return "(tab not found in herd ls)"


def confirm_card(record: dict) -> str:
    if record["kind"] == "herd_send":
        head = f"Hermes proposes sending to {record['tab']}: {_tab_title(record['tab'])}"
    else:
        project = record.get("project") or "inbox"
        head = f"Hermes proposes a todo ({project})"
    return f"{head}\n```{record['text']}```\nReply yes in this thread to run it. Anything else cancels."


def _tool(argv: list[str]) -> str:
    env = dict(os.environ, PATH=TOOL_PATH, NO_COLOR="1")
    try:
        done = subprocess.run(
            argv, capture_output=True, text=True, timeout=90, env=env, stdin=subprocess.DEVNULL
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"{argv[0]} failed: {exc}"
    out = (done.stdout or "").strip()
    if done.returncode:
        out = f"{out}\n{(done.stderr or '').strip()}\n(exit {done.returncode})".strip()
    return out[:1500] or "(no output)"


def execute(record: dict) -> str:
    problem = validate(record)
    if problem:
        return f"Not run: {problem}."
    if record["kind"] == "herd_send":
        result = _tool(["herd", "send", record["tab"], record["text"]])
        return f"Sent to {record['tab']}.\n```{result}```"

    argv = ["todo", "add", "--source", "hermes-slack"]
    if record.get("project"):
        argv += ["--project", record["project"]]
    result = _tool([*argv, record["text"]])
    return f"Todo added.\n```{result}```"


def ask(text: str, sid: str) -> str:
    """One Hermes turn. Raises ConnectionError when the gateway is unreachable."""
    try:
        key = HERMES_KEY_FILE.read_text().strip()
    except OSError as exc:
        raise ConnectionError(f"no Hermes key at {HERMES_KEY_FILE}") from exc

    body = json.dumps(
        {"model": "hermes-desk", "messages": [{"role": "user", "content": text}]}
    ).encode()
    request = urllib.request.Request(
        f"{HERMES_URL}/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "X-Hermes-Session-Id": sid,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=HERMES_TIMEOUT) as response:
            data = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Hermes HTTP {exc.code}") from exc
    except (urllib.error.URLError, ConnectionError, OSError) as exc:
        raise ConnectionError(str(exc)) from exc

    return str(data["choices"][0]["message"]["content"] or "").strip()


def handle(event: dict, post) -> str:
    """Forward one accepted message and post the reply. `post(text, channel, thread_ts)`."""
    channel = event.get("channel")
    thread = event.get("thread_ts") or event.get("ts")
    text = slack_to_text(str(event.get("text") or ""))
    if not text:
        return "empty"

    sid = session_id(event)
    with _call_lock:
        staged = take_pending(sid)
        if staged and text.lower().strip(" !") in CONFIRM_WORDS:
            post(execute(staged), channel, thread)
            log(f"hermes: confirmed {staged.get('kind')} session={sid}")
            return "confirmed"
        if staged:
            post("Cancelled the pending action.", channel, thread)

        _write_turn(sid)
        try:
            reply = ask(text, sid)
            outcome = "ok"
        except ConnectionError as exc:
            log(f"hermes: down ({exc})")
            reply = DOWN_TEXT
            outcome = "down"
        except Exception as exc:  # noqa: BLE001 - any failure must still answer Nathan
            log(f"hermes: failed ({exc})")
            reply = f"Hermes hit an error: {exc}"
            outcome = "error"
        finally:
            _end_turn()

        post(to_slack(reply) or "(Hermes returned nothing)", channel, thread)
        proposal = _peek_pending(sid)
        if proposal:
            post(confirm_card(proposal), channel, thread)

    log(f"hermes: {outcome} session={sid}")
    return outcome


def _peek_pending(sid: str) -> dict | None:
    record = take_pending(sid)
    if not record:
        return None
    if validate(record):
        log(f"hermes: dropped invalid staged action session={sid}")
        return None
    # Put it back: the card is shown now, the yes arrives as the next message.
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    _pending_path(sid).write_text(json.dumps(record))
    return record


def handle_async(event: dict, post) -> threading.Thread:
    """Hermes turns take seconds to minutes; never block the Socket Mode loop on one."""
    worker = threading.Thread(target=handle, args=(event, post), name="hermes", daemon=True)
    worker.start()
    return worker
