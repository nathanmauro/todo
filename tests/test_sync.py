"""Push (sync) + completion read-back (reconcile) invariants.

These pin the existing one-way behavior so the inbound mirror can't silently
break it: sync pushes each open row exactly once and never touches a mirrored
row; reconcile only flips status and never creates rows.
"""
from __future__ import annotations

import io
import urllib.error
from unittest.mock import MagicMock

from todo_cli import todoist
from todo_cli.models import TodoEntry, TodoistSync
from todo_cli.storage import load_all, write_all


def test_roundtrip_preserves_sync_and_origin(store):
    e = TodoEntry(text="hi", origin="todoist", mirrored_at="2026-01-01T00:00:00")
    e.sync.todoist = TodoistSync(task_id="T1", url="u", ts="x", project_id="P1")
    write_all([e])
    [back] = load_all()
    assert back.origin == "todoist"
    assert back.mirrored_at == "2026-01-01T00:00:00"
    assert back.sync.todoist.task_id == "T1"
    assert back.sync.todoist.project_id == "P1"


def test_sync_pushes_then_idempotent(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    monkeypatch.setattr(todoist, "ensure_label", lambda *a, **k: None)
    ct = MagicMock(return_value={"id": "999"})
    monkeypatch.setattr(todoist, "create_task", ct)

    entries = [TodoEntry(text="push me", project="todo", source="cli")]
    assert todoist.sync(entries) == 0
    assert ct.call_count == 1
    assert entries[0].sync.todoist.task_id == "999"

    # second run: the task_id stamp makes it a no-op
    assert todoist.sync(entries) == 0
    assert ct.call_count == 1


def test_sync_skips_todoist_origin(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    monkeypatch.setattr(todoist, "ensure_label", lambda *a, **k: None)
    ct = MagicMock(return_value={"id": "1"})
    monkeypatch.setattr(todoist, "create_task", ct)

    # an imported row even without a task_id must never be pushed
    e = TodoEntry(text="mirrored", origin="todoist")
    assert todoist.sync([e]) == 0
    assert ct.call_count == 0


def test_reconcile_flips_done_on_checked(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    monkeypatch.setattr(todoist, "fetch_task", lambda tok, tid: {"checked": True})
    e = TodoEntry(text="x")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x")
    todoist.reconcile([e])
    assert e.status == "done"
    assert e.done_source == "todoist"


def test_reconcile_flips_done_on_404(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")

    def boom(tok, tid):
        raise urllib.error.HTTPError("u", 404, "nf", {}, io.BytesIO(b""))

    monkeypatch.setattr(todoist, "fetch_task", boom)
    e = TodoEntry(text="x")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x")
    todoist.reconcile([e])
    assert e.status == "done"
    assert e.done_source == "todoist"


def test_reconcile_never_creates(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    monkeypatch.setattr(todoist, "fetch_task", lambda tok, tid: {"checked": False})
    e = TodoEntry(text="still open")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x")
    entries = [e]
    todoist.reconcile(entries)
    assert len(entries) == 1
    assert entries[0].status == "open"
