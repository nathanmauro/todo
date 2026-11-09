"""Action registry for actionable notifications, and the executor for a click.

A notification button cannot carry its action on the wire, so it carries only a
short hex id. The real action (a closed verb plus payload) is one JSON file
under ACTIONS_DIR, written when the notification is sent (`register`). When the
click comes back, the transport loads it, runs it exactly once (`execute`) and
records the outcome (`mark`).

The files are a contract other tools read (Job Scout's career learning scans
them for acks and snoozes), so the record shape is append-only: id, created,
verb, payload, label, status, then result and resolved once handled.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import subprocess
from pathlib import Path

from . import capture, gtasks, linear, obsidian, todoist
from .config import ACTIONS_DIR
from .config import task_backend as config_task_backend
from .models import now_iso
from .storage import file_lock, find_by_prefix, load_all, log, write_all

ACTION_VERBS = {
    "ack",
    "add-task",
    "idea-hot",
    "todoist-complete",
    "gtasks-complete",
    "linear-complete",
}
_ACTION_ID_RE = re.compile(r"^[0-9a-f]{12}$")


def valid_verb(verb: str) -> bool:
    """A verb from the closed set, or an `agent-*` verb the bridge interprets."""
    return verb in ACTION_VERBS or verb.startswith("agent-")


# --- registry ----------------------------------------------------------------


def _action_path(action_id: str) -> Path | None:
    if not _ACTION_ID_RE.fullmatch(action_id):
        return None
    return ACTIONS_DIR / f"{action_id}.json"


def register(verb: str, payload: str, label: str) -> str | None:
    """Store one pending action; return its id, or None if it was refused."""
    if not valid_verb(verb):
        log(f"action: unknown verb '{verb}' (allowed: {sorted(ACTION_VERBS)} + agent-*)")
        return None

    action_id = secrets.token_hex(6)
    record = {
        "id": action_id,
        "created": now_iso(),
        "verb": verb,
        "payload": payload,
        "label": label,
        "status": "pending",
    }
    try:
        ACTIONS_DIR.mkdir(parents=True, exist_ok=True)
        (ACTIONS_DIR / f"{action_id}.json").write_text(json.dumps(record, indent=2))
    except OSError as exc:
        log(f"action: could not register: {exc}")
        return None
    return action_id


def load(action_id: str) -> dict | None:
    path = _action_path(action_id)
    if path is None or not path.is_file():
        return None
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def mark(action_id: str, status: str, result: str = "") -> None:
    path = _action_path(action_id)
    action = load(action_id)
    if path is None or action is None:
        return
    action["status"] = status
    action["result"] = result
    action["resolved"] = now_iso()
    try:
        path.write_text(json.dumps(action, indent=2))
    except OSError as exc:
        log(f"action: could not mark {action_id} {status}: {exc}")


# --- verbs -------------------------------------------------------------------


def _idea_hot(slug: str) -> str:
    """Flip an Ideas-store file's Heat strip to Hot. Returns a toast string."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,80}", slug):
        return "bad idea slug"
    path = obsidian.OBSIDIAN_VAULT / "05 Notes" / "ideas" / f"idea-{slug}.md"
    if not path.is_file():
        return f"idea not found: {slug}"
    try:
        text = path.read_text(encoding="utf-8")
        if "**Heat:** Hot" in text:
            return "already hot 🔥"
        new = text.replace("**Heat:** —", "**Heat:** Hot", 1)
        if new == text:
            return "no Heat field to flip"
        path.write_text(new, encoding="utf-8")
    except OSError as exc:
        return f"idea edit failed: {exc}"
    return "idea → Hot 🔥"


def _complete_todo(id_prefix: str, source: str) -> str:
    """Mark a local todo done and propagate the close to Todoist. Toast string.

    Mirrors `todo done`: the local "done" is persisted before the network leg so
    a stalled Todoist can never cost the completion; push_completions is
    best-effort and the next `todo sync`/`refresh` flushes whatever didn't land.
    The frozen Logseq leg is deliberately skipped.
    """
    if not re.fullmatch(r"[0-9a-f]{6,32}", id_prefix):
        return "bad todo id"
    try:
        with file_lock():
            entries = load_all()
            target = find_by_prefix(entries, id_prefix)
            if not target:
                return "todo not found"
            if target.status == "done":
                return "already done ✓"
            target.status = "done"
            target.done_ts = now_iso()
            target.done_source = target.done_source or source
            write_all(entries)
            closed, _ = todoist.push_completions([target])
            write_all(entries)
    except Exception as exc:  # noqa: BLE001 — a click must always toast, not crash the listener
        log(f"action todoist-complete: {exc}")
        return "complete failed (see log)"
    label = target.text if len(target.text) <= 40 else target.text[:39] + "…"
    suffix = "" if closed else " (Todoist pending)"
    return f"done ✓ {label}{suffix}"


def _gtasks_complete(payload: str, source: str) -> str:
    """Complete a Google Tasks task from a button.

    Payload is "<list_id>:<task_id>" (from e.g. cockpit-gtasks-digest
    --buttons). Also flips any local row stamped with that task id.
    """
    lid, sep, task_id = payload.partition(":")
    if not sep or not lid or not task_id:
        return "bad gtasks payload"
    try:
        gtasks.complete_task(lid, task_id)
    except Exception as exc:  # noqa: BLE001 — a click must always toast, not crash the listener
        log(f"action gtasks-complete: {exc}")
        return "complete failed (see log)"
    try:
        with file_lock():
            entries = load_all()
            for e in entries:
                if e.sync.gtasks and e.sync.gtasks.task_id == task_id:
                    if e.status != "done":
                        e.status = "done"
                        e.done_ts = now_iso()
                        e.done_source = e.done_source or source
                    e.sync.gtasks.closed_ts = now_iso()
            write_all(entries)
    except Exception as exc:  # noqa: BLE001 — Google side is done; local flip is best-effort
        log(f"action gtasks-complete local flip: {exc}")
    return "done ✓"


def _linear_complete(payload: str, source: str) -> str:
    """Close a Linear issue from a digest button and flip the local row if stamped.

    Payload is the Linear issue id (uuid) or identifier (e.g. NAT-123) as emitted
    by cockpit-morning-digest. Linear side first; local flip is best-effort.
    """
    issue_ref = payload.strip()
    if not re.fullmatch(r"[A-Za-z0-9-]{3,64}", issue_ref):
        return "bad linear payload"
    try:
        linear.complete_issue(issue_ref)
    except Exception as exc:  # noqa: BLE001 — a click must always toast
        log(f"action linear-complete: {exc}")
        return "linear complete failed (see log)"
    try:
        with file_lock():
            entries = load_all()
            for e in entries:
                ls = e.sync.linear
                if ls and issue_ref in (ls.issue_id, ls.identifier):
                    if e.status != "done":
                        e.status = "done"
                        e.done_ts = now_iso()
                        e.done_source = e.done_source or source
                    ls.closed_ts = now_iso()
            write_all(entries)
    except Exception as exc:  # noqa: BLE001 — Linear side is done; local flip is best-effort
        log(f"action linear-complete local flip: {exc}")
    return "done ✓"


def _agent_action(verb: str, payload: str, chat_id, agent_allowed: bool) -> str:
    """Hand an `agent-*` verb to the agent bridge (TODO_AGENT_BRIDGE_CMD)."""
    # Defense-in-depth: an open-mode transport must never fire agents for
    # arbitrary senders, so the caller has to vouch for a user allow-list.
    if not agent_allowed:
        log("agent-action blocked — the transport has no user allow-list (open mode)")
        return "agent actions require a configured chat allow-list"
    bridge = os.environ.get("TODO_AGENT_BRIDGE_CMD", "")
    if not bridge:
        return "agent bridge not configured (set TODO_AGENT_BRIDGE_CMD)"

    args = [bridge, "--action", verb, "--payload", payload]
    if chat_id is not None:
        args += ["--chat-id", str(chat_id)]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=30)
        return r.stdout.strip() or r.stderr.strip() or "done"
    except Exception as exc:  # noqa: BLE001 — a click must always toast, not crash
        log(f"agent-action {verb}: {exc}")
        return f"agent-action failed: {exc}"


# --- executor ----------------------------------------------------------------


def execute(action: dict, *, source: str, chat_id=None, agent_allowed: bool = False) -> str:
    """Run one registered action. Returns the toast shown to the user.

    `source` names the calling transport ("slack"); it is stamped on any task
    the action creates and on any row it completes. `chat_id` is where the
    click happened, passed through to the agent bridge. `agent_allowed` is the
    transport's own user lock: agent verbs are refused unless it is set.
    """
    verb = action.get("verb", "")
    payload = str(action.get("payload") or "")
    if verb == "ack":
        return "✓"
    if verb == "add-task":
        if not payload.strip():
            return "empty task payload"
        if capture.push_task(payload, source):
            return f"task → {capture.task_backend_name()} ✓"
        return f"{capture.task_backend_name()} push failed (see log)"
    if verb == "idea-hot":
        return _idea_hot(payload)

    backend = config_task_backend()
    if verb == "todoist-complete":
        if backend != "todoist":
            log(f"action: todoist-complete refused under backend={backend}")
            return (
                "Todoist lane retired — this task now lives in Linear; use the Linear button or app"
            )
        return _complete_todo(payload, source)
    if verb == "gtasks-complete":
        if backend != "gtasks":
            log(f"action: gtasks-complete refused under backend={backend}")
            return "Google Tasks lane retired — this task now lives in Linear; use the Linear button or app"
        return _gtasks_complete(payload, source)
    if verb == "linear-complete":
        return _linear_complete(payload, source)

    if verb.startswith("agent-"):
        return _agent_action(verb, payload, chat_id, agent_allowed)
    return f"unknown verb: {verb}"
