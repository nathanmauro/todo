"""Transport-neutral capture core: classify a message and push a task.

A transport (today only slack.py) turns its wire format into plain text and
calls in here. Nothing in this module knows which wire the text arrived on; the
caller names itself through `source`, which is stamped on the rows it creates.

The Obsidian file itself is written by obsidian.py. A "+t" capture additionally
becomes one task in the active backend (Linear by default), with the local
todos.jsonl row landing first so a failed push is retried by `todo sync`.
"""

from __future__ import annotations

import os

from . import gtasks, linear, todoist
from .config import task_backend as config_task_backend
from .models import TodoEntry, TodoistSync, now_iso
from .storage import file_lock, load_all, log, write_all

_PREFIXES = {"+t": "task", "+task": "task", "+i": "idea", "+idea": "idea"}

_AGENT_PREFIX_DEFAULTS = frozenset({"/claude", "/sessions", "/kill"})
# NOTE: /codex is intentionally absent — cockpit-remote-fire has no /codex handler;
# adding it here without a matching dispatch case would silently drop messages.


def agent_prefixes() -> frozenset[str]:
    """Agent-command prefix set (from TODO_AGENT_PREFIXES env, comma-separated)."""
    raw = os.environ.get("TODO_AGENT_PREFIXES", "")
    if raw:
        return frozenset(p.strip() for p in raw.split(",") if p.strip())
    return _AGENT_PREFIX_DEFAULTS


def classify(text: str) -> tuple[str, str]:
    """Map a raw message to (kind, body). DEFAULT classifier = prefix parser.

    "+t "/"+task " -> task, "+i "/"+idea " -> idea, anything else -> note. The
    prefix token (and the space after it) is stripped from the body; a bare
    "+t" with no body falls back to a plain note so an empty task is never made.

    This is the SWAPPABLE SEAM: a future LLM / Black Box classifier (see the
    vault's 06 Backlog/llm-classifier-for-telegram-captures) can replace this
    body wholesale, and tests/test_capture_core.py pins the contract it must
    keep.
    """
    stripped = text.strip()
    head, _, rest = stripped.partition(" ")
    kind = _PREFIXES.get(head.lower())
    if kind and rest.strip():
        return kind, rest.strip()
    return "note", stripped


def task_backend_name() -> str:
    """Display name for the active task backend ("Linear"/"Google Tasks"/"Todoist")."""
    backend = config_task_backend()
    if backend == "linear":
        return "Linear"
    return "Google Tasks" if backend == "gtasks" else "Todoist"


def _push_task_linear(text: str, source: str) -> bool:
    """Linear lane of push_task — FAIL-CLOSED, local row first.

    The todos.jsonl row is appended BEFORE the network push, so a missing API key,
    an offline machine, or any API error leaves a queued row that the next
    `todo sync` / `todo refresh` (linear.sync) picks up. Never falls back to
    Todoist or Google Tasks.
    """
    with file_lock():
        entries = load_all()
        entry = TodoEntry(text=text, source=source)
        entries.append(entry)
        write_all(entries)
    if not linear.available():
        log(f"capture task -> linear queued (no API key): {linear.KEY_HINT}")
        return False
    try:
        # Hold the store lock across the network leg so this push and a concurrent
        # `todo refresh` (which also pushes under the lock) never race the same row;
        # the deterministic issue id makes any remaining overlap adopt, not duplicate.
        with file_lock():
            entries = load_all()
            for e in entries:
                if e.id == entry.id:
                    if e.sync.linear is None:
                        linear.push_entry(e)
                    break
            write_all(entries)
        return True
    except Exception as exc:  # noqa: BLE001 — a capture must survive a bad push
        log(f"capture task -> linear failed: {exc}; row queued for `todo sync`")
        return False


def _push_task_gtasks(text: str, source: str) -> bool:
    """Google Tasks lane of push_task — FAIL-CLOSED.

    The local todos.jsonl row is appended BEFORE the network push, so a failed
    or offline push leaves a queued row that the next `todo sync` (gtasks.sync)
    picks up. Contrast with the Todoist lane, which historically only recorded
    successfully pushed rows.
    """
    with file_lock():
        entries = load_all()
        entry = TodoEntry(text=text, source=source)
        entries.append(entry)
        write_all(entries)
    try:
        task = gtasks.create_task(text, notes=f"source: {source}")
        with file_lock():
            entries = load_all()
            for e in entries:
                if e.id == entry.id:
                    gtasks.stamp(e, task)
            write_all(entries)
        return True
    except Exception as exc:  # noqa: BLE001 — a capture must survive a bad push
        log(f"capture task -> gtasks failed: {exc}; row queued for `todo sync`")
        return False


def _push_task_todoist(text: str, source: str) -> bool:
    """Legacy Todoist lane of push_task: push first, record the row on success."""
    try:
        tok = todoist.token()
        if not tok:
            log("capture task: no todoist token; saved to vault only")
            return False
        todoist.ensure_label(tok, source)
        task = todoist.create_task(
            tok, text, project_id=todoist.TODOIST_PROJECT_ID, labels=[source]
        )
        tid = str(task.get("id", ""))
        # Lock the read-modify-rewrite so an in-flight `todo refresh` (which
        # holds the lock across its network window) can't clobber this row.
        with file_lock():
            entries = load_all()
            if any(e.sync.todoist and e.sync.todoist.task_id == tid for e in entries):
                # A refresh that held the lock while we waited already
                # mirrored the task we just created — that row is the record;
                # appending another would duplicate it forever.
                return True
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
        log(f"capture task -> todoist failed: {exc}")
        return False


def push_task(text: str, source: str) -> bool:
    """Create ONE task in the active backend, without touching Logseq.

    Pushes only this task (not a full `todo sync`, which would flush unrelated
    pending rows), records it in the local store with the backend id stamped so
    it is never re-pushed, and (Todoist) ensures the source label exists first.
    Swallows every error — the vault file is the canonical record regardless.

    `source` names the calling transport ("slack") and lands on the local row.
    """
    backend = config_task_backend()
    if backend == "linear":
        return _push_task_linear(text, source)
    if backend == "gtasks":
        return _push_task_gtasks(text, source)
    if backend == "todoist":
        return _push_task_todoist(text, source)
    # Unknown value: keep the vault note, queue nothing anywhere, never guess Todoist.
    log(f"capture task: unknown TODO_TASK_BACKEND={backend!r}; saved to vault only")
    return False
