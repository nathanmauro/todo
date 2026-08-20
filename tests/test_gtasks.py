"""Google Tasks backend invariants (2026-08-20 migration).

Pins: sync eligibility (never re-push a row either backend already has, never
push mirrored rows), the fail-closed telegram lane (local row lands before the
network push and survives its failure), backend switching, and the
gtasks-complete button verb.
"""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from todo_cli import gtasks, telegram
from todo_cli.models import GtasksSync, TodoEntry, TodoistSync
from todo_cli.storage import load_all, write_all


@pytest.fixture
def gtasks_backend(monkeypatch):
    monkeypatch.setenv("TODO_TASK_BACKEND", "gtasks")


def _mock_create(monkeypatch, **kwargs):
    ct = MagicMock(return_value={"id": "G1", "_list_id": "L1", "selfLink": "s"}, **kwargs)
    monkeypatch.setattr(gtasks, "create_task", ct)
    return ct


# --- gtasks.sync eligibility -------------------------------------------------

def test_sync_pushes_then_idempotent(monkeypatch):
    ct = _mock_create(monkeypatch)
    entries = [TodoEntry(text="push me", source="cli", due="2026-08-21")]
    assert gtasks.sync(entries, quiet=True) == 0
    assert ct.call_count == 1
    assert ct.call_args.kwargs["due"] == "2026-08-21"
    assert entries[0].sync.gtasks.task_id == "G1"
    assert entries[0].sync.gtasks.list_id == "L1"
    # second run: the stamp makes it a no-op
    assert gtasks.sync(entries, quiet=True) == 0
    assert ct.call_count == 1


def test_sync_skips_todoist_stamped_and_mirrored(monkeypatch):
    ct = _mock_create(monkeypatch)
    stamped = TodoEntry(text="already in todoist")
    stamped.sync.todoist = TodoistSync(task_id="T1", ts="x")
    mirrored = TodoEntry(text="mirrored", origin="todoist")
    done = TodoEntry(text="done", status="done")
    assert gtasks.sync([stamped, mirrored, done], quiet=True) == 0
    assert ct.call_count == 0


def test_sync_partial_failure_keeps_going(monkeypatch):
    calls = {"n": 0}

    def flaky(text, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise gtasks.GtasksError("boom")
        return {"id": "G2", "_list_id": "L1"}

    monkeypatch.setattr(gtasks, "create_task", flaky)
    entries = [TodoEntry(text="fails"), TodoEntry(text="succeeds")]
    assert gtasks.sync(entries, quiet=True) == 1
    assert entries[0].sync.gtasks is None
    assert entries[1].sync.gtasks.task_id == "G2"


def test_rfc3339_due_mapping():
    assert gtasks._rfc3339("2026-08-21") == "2026-08-21T00:00:00.000Z"
    assert gtasks._rfc3339("2026-08-21T09:00:00") == "2026-08-21T00:00:00.000Z"
    assert gtasks._rfc3339(None) is None
    assert gtasks._rfc3339("tomorrow") is None


# --- telegram +t lane --------------------------------------------------------

def test_push_task_gtasks_success_stamps(monkeypatch, gtasks_backend):
    _mock_create(monkeypatch)
    assert telegram._push_task("buy milk", source="telegram") is True
    [row] = load_all()
    assert row.text == "buy milk"
    assert row.source == "telegram"
    assert row.sync.gtasks.task_id == "G1"
    assert row.sync.todoist is None


def test_push_task_gtasks_fail_closed(monkeypatch, gtasks_backend):
    """The row must land locally BEFORE the push, and survive its failure."""
    monkeypatch.setattr(
        gtasks, "create_task",
        MagicMock(side_effect=gtasks.GtasksError("offline")),
    )
    assert telegram._push_task("do not lose me", source="telegram") is False
    [row] = load_all()
    assert row.text == "do not lose me"
    assert row.sync.gtasks is None          # unstamped -> `todo sync` retries it
    # ...and the retry actually picks it up:
    ct = _mock_create(monkeypatch)
    entries = load_all()
    assert gtasks.sync(entries, quiet=True) == 0
    assert ct.call_count == 1
    assert entries[0].sync.gtasks.task_id == "G1"


def test_push_task_default_backend_still_todoist(monkeypatch):
    """Without the env flip, +t keeps using the Todoist lane."""
    monkeypatch.delenv("TODO_TASK_BACKEND", raising=False)
    gt = _mock_create(monkeypatch)
    from todo_cli import todoist
    monkeypatch.setattr(todoist, "token", lambda: None)  # short-circuits lane
    assert telegram._push_task("still todoist") is False
    assert gt.call_count == 0


def test_backend_name(monkeypatch, gtasks_backend):
    assert telegram._task_backend_name() == "Google Tasks"
    monkeypatch.setenv("TODO_TASK_BACKEND", "todoist")
    assert telegram._task_backend_name() == "Todoist"


# --- gtasks-complete button verb --------------------------------------------

def test_gtasks_complete_flips_local_row(monkeypatch):
    done = MagicMock()
    monkeypatch.setattr(gtasks, "complete_task", done)
    row = TodoEntry(text="tap me")
    row.sync.gtasks = GtasksSync(task_id="G9", list_id="L1", ts="x")
    write_all([row])
    assert telegram._gtasks_complete("L1:G9") == "done ✓"
    done.assert_called_once_with("L1", "G9")
    [back] = load_all()
    assert back.status == "done"
    assert back.sync.gtasks.closed_ts


def test_gtasks_complete_bad_payload(monkeypatch):
    done = MagicMock()
    monkeypatch.setattr(gtasks, "complete_task", done)
    assert telegram._gtasks_complete("nocolon") == "bad gtasks payload"
    assert done.call_count == 0


def test_gtasks_complete_api_failure(monkeypatch):
    monkeypatch.setattr(
        gtasks, "complete_task",
        MagicMock(side_effect=gtasks.GtasksError("nope")),
    )
    assert "failed" in telegram._gtasks_complete("L1:G9")


def test_action_verb_registered():
    assert "gtasks-complete" in telegram.ACTION_VERBS
