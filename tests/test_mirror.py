"""Inbound mirror (Todoist -> local): import, upsert, filter, echo-guard, sweep."""
from __future__ import annotations

import datetime as dt
from unittest.mock import MagicMock

from todo_cli import todoist
from todo_cli.models import TodoEntry, TodoistSync


def _patch(monkeypatch, projects, tasks, project_labels=("todo",)):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    monkeypatch.setattr(
        todoist,
        "mirror_policy",
        lambda: {
            "exclude_shared": True,
            "exclude_project_ids": [],
            "exclude_completed": True,
        },
    )
    monkeypatch.setattr(
        todoist,
        "taxonomy_labels",
        lambda: {
            "source": ["claude", "cli", "codex"],
            "projects": list(project_labels),
            "areas": [],
        },
    )
    monkeypatch.setattr(todoist, "list_projects", lambda tok: projects)
    monkeypatch.setattr(todoist, "list_active_tasks", lambda tok: tasks)


def test_mirror_creates_new(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}],
        tasks=[
            {
                "id": "T1",
                "content": "hello",
                "project_id": "P1",
                "labels": ["claude", "todo"],
                "due": {"date": "2026-06-01"},
            }
        ],
    )
    entries = []
    assert todoist.mirror(entries) == 0
    assert len(entries) == 1
    e = entries[0]
    assert e.origin == "todoist"
    assert e.source == "claude"
    assert e.project == "todo"
    assert e.due == "2026-06-01"
    assert e.sync.todoist.task_id == "T1"
    assert e.sync.todoist.project_id == "P1"


def test_mirror_unlabeled_source_defaults_to_todoist(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}],
        tasks=[{"id": "T1", "content": "phone capture", "project_id": "P1", "labels": []}],
    )
    entries = []
    todoist.mirror(entries)
    assert entries[0].source == "todoist"
    assert entries[0].project is None


def test_mirror_excludes_shared(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}, {"id": "S1", "is_shared": True}],
        tasks=[
            {"id": "T1", "content": "keep", "project_id": "P1", "labels": []},
            {"id": "T2", "content": "drop", "project_id": "S1", "labels": []},
        ],
    )
    entries = []
    todoist.mirror(entries)
    assert [e.sync.todoist.task_id for e in entries] == ["T1"]


def test_mirror_excludes_archived_project(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False, "is_archived": True}],
        tasks=[{"id": "T1", "content": "x", "project_id": "P1", "labels": []}],
    )
    entries = []
    todoist.mirror(entries)
    assert entries == []


def test_mirror_updates_existing_no_dup(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}],
        tasks=[{"id": "T1", "content": "new text", "project_id": "P1", "labels": []}],
    )
    e = TodoEntry(text="old text", source="cli", project="todo")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x")
    entries = [e]
    todoist.mirror(entries)
    assert len(entries) == 1
    assert entries[0].text == "new text"
    assert entries[0].source == "cli"  # local provenance preserved


def test_mirror_pulled_not_repushed(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}],
        tasks=[{"id": "T1", "content": "remote", "project_id": "P1", "labels": []}],
    )
    entries = []
    todoist.mirror(entries)

    ct = MagicMock(return_value={"id": "x"})
    monkeypatch.setattr(todoist, "create_task", ct)
    monkeypatch.setattr(todoist, "ensure_label", lambda *a, **k: None)
    assert todoist.sync(entries) == 0
    assert ct.call_count == 0  # echo guard: mirrored row never pushed back


def test_mirror_completion_sweep(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}],
        tasks=[],  # T9 vanished from the active set
    )
    e = TodoEntry(text="was mirrored", origin="todoist")
    e.sync.todoist = TodoistSync(task_id="T9", ts="x", project_id="P1")
    entries = [e]
    todoist.mirror(entries)
    assert entries[0].status == "done"
    assert entries[0].done_source == "todoist"


def test_mirror_sweep_ignores_out_of_scope(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}],
        tasks=[],
    )
    # a mirrored row whose project is no longer in scope can't be judged absent
    e = TodoEntry(text="other proj", origin="todoist")
    e.sync.todoist = TodoistSync(task_id="T9", ts="x", project_id="GONE")
    entries = [e]
    todoist.mirror(entries)
    assert entries[0].status == "open"


def test_mirror_idempotent(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}],
        tasks=[{"id": "T1", "content": "x", "project_id": "P1", "labels": []}],
    )
    entries = []
    todoist.mirror(entries)
    todoist.mirror(entries)
    assert len(entries) == 1


def test_mirror_dry_run_no_mutation(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}],
        tasks=[{"id": "T1", "content": "x", "project_id": "P1", "labels": []}],
    )
    entries = []
    assert todoist.mirror(entries, dry_run=True) == 0
    assert entries == []


def test_mirror_backfills_ts_from_added_at(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}],
        tasks=[
            {
                "id": "T1",
                "content": "typed in todoist last week",
                "project_id": "P1",
                "labels": [],
                "added_at": "2026-06-05T03:13:31.000000Z",
            }
        ],
    )
    entries = []
    todoist.mirror(entries)
    # ts carries the Todoist creation moment (rendered in local tz), not the
    # pull moment
    t = dt.datetime.fromisoformat(entries[0].ts)
    assert t.astimezone(dt.timezone.utc) == dt.datetime(
        2026, 6, 5, 3, 13, 31, tzinfo=dt.timezone.utc
    )


def test_mirror_missing_added_at_falls_back_to_now(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}],
        tasks=[{"id": "T1", "content": "x", "project_id": "P1", "labels": []}],
    )
    entries = []
    todoist.mirror(entries)
    assert entries[0].ts  # default now_iso, never empty


def test_mirror_update_rederives_labels_on_mirrored_rows(monkeypatch):
    _patch(
        monkeypatch,
        projects=[{"id": "P1", "is_shared": False}],
        tasks=[
            {
                "id": "T1",
                "content": "remote",
                "project_id": "P1",
                "labels": ["claude", "todo"],
            }
        ],
    )
    e = TodoEntry(text="remote", origin="todoist", source="todoist", project=None)
    e.sync.todoist = TodoistSync(task_id="T1", ts="x")
    entries = [e]
    todoist.mirror(entries)
    # labels added in Todoist web after import now propagate
    assert entries[0].source == "claude"
    assert entries[0].project == "todo"
