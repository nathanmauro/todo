"""Hardening for unattended interval refresh: lock, quarantine, narrowed
reconcile, and ls coherence for mirrored rows."""
from __future__ import annotations

import argparse
import fcntl
from unittest.mock import MagicMock

import pytest

from todo_cli import commands, storage, todoist
from todo_cli.formatting import sync_badges
from todo_cli.models import TodoEntry, TodoistSync
from todo_cli.storage import file_lock, load_all, write_all


# --- quarantine ---------------------------------------------------------------


def test_load_all_quarantines_bad_lines(tmp_path, store, capsys):
    good = TodoEntry(text="good")
    store.write_text(good.model_dump_json() + "\n" + "{not json\n")

    entries = load_all()

    assert [e.text for e in entries] == ["good"]
    rejects = tmp_path / "todos.rejects.jsonl"
    assert rejects.read_text() == "{not json\n"
    assert "1 unparseable line(s)" in capsys.readouterr().err


def test_quarantine_dedupes_across_reads(tmp_path, store):
    store.write_text("{torn line\n")
    load_all()
    load_all()  # read-only verbs re-parse the same bad line; must not duplicate
    rejects = tmp_path / "todos.rejects.jsonl"
    assert rejects.read_text() == "{torn line\n"


def test_quarantine_survives_rewrite(tmp_path, store):
    good = TodoEntry(text="keep me")
    store.write_text(good.model_dump_json() + "\n" + '{"half": "a row' + "\n")
    entries = load_all()
    write_all(entries)  # the rewrite that used to silently erase the bad line
    assert '{"half": "a row' in (tmp_path / "todos.rejects.jsonl").read_text()
    assert "keep me" in store.read_text()
    assert "half" not in store.read_text()


# --- file lock ----------------------------------------------------------------


def test_file_lock_is_exclusive(tmp_path):
    with file_lock():
        outside = (tmp_path / "todos.lock").open("w")
        try:
            try:
                fcntl.flock(outside, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                contended = True
            else:
                contended = False
            assert contended
        finally:
            outside.close()
    # released on exit: an outside flock now succeeds
    outside = (tmp_path / "todos.lock").open("w")
    try:
        fcntl.flock(outside, fcntl.LOCK_EX | fcntl.LOCK_NB)
    finally:
        outside.close()


def test_file_lock_timeout_raises(tmp_path):
    holder = (tmp_path / "todos.lock").open("w")
    fcntl.flock(holder, fcntl.LOCK_EX)
    try:
        with pytest.raises(storage.LockTimeout):
            with file_lock(timeout=0.05):
                raise AssertionError("must not enter the critical section")
        # loud failure beats an unlocked write that could silently destroy a
        # concurrent local-origin append
        assert "file_lock: timeout" in (tmp_path / "todo.log").read_text()
    finally:
        holder.close()


# --- narrowed reconcile -------------------------------------------------------


def test_reconcile_skips_only_sweep_covered_mirrored_rows(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    covered_row = TodoEntry(text="in scope", origin="todoist")
    covered_row.sync.todoist = TodoistSync(task_id="T1", ts="x", project_id="P1")
    out_of_scope = TodoEntry(text="project archived", origin="todoist")
    out_of_scope.sync.todoist = TodoistSync(task_id="T2", ts="x", project_id="GONE")
    local = TodoEntry(text="local", source="cli")
    local.sync.todoist = TodoistSync(task_id="T3", ts="x")

    fetched: list[str] = []
    monkeypatch.setattr(
        todoist,
        "fetch_task",
        lambda tok, tid: fetched.append(tid) or {"checked": False},
    )

    rc = todoist.reconcile(
        [covered_row, out_of_scope, local], skip_project_ids={"P1"}
    )
    assert rc == 0
    # T1 was judged by mirror's sweep; T2's project left mirror scope, so the
    # per-task fetch is its ONLY completion path; T3 is local-origin.
    assert fetched == ["T2", "T3"]


def test_reconcile_flips_out_of_scope_mirrored_completion(monkeypatch):
    """Regression: archive a Todoist project after import — completing the
    task must still converge through the refresh path (mirror sweep can't
    judge it; reconcile must)."""
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    e = TodoEntry(text="done remotely", origin="todoist")
    e.sync.todoist = TodoistSync(task_id="T9", ts="x", project_id="GONE")
    monkeypatch.setattr(todoist, "fetch_task", lambda tok, tid: {"checked": True})

    todoist.reconcile([e], skip_project_ids={"P1"})

    assert e.status == "done"
    assert e.done_source == "todoist"
    assert e.sync.todoist.closed_ts  # no-echo gate stamped


def test_reconcile_empty_covered_set_means_full_scan(monkeypatch):
    """A failed mirror passes an empty set — reconcile must degrade to the
    full scan, not skip everything."""
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    mirrored = TodoEntry(text="remote", origin="todoist")
    mirrored.sync.todoist = TodoistSync(task_id="T1", ts="x", project_id="P1")
    fetch = MagicMock(return_value={"checked": False})
    monkeypatch.setattr(todoist, "fetch_task", fetch)
    todoist.reconcile([mirrored], skip_project_ids=set())
    assert fetch.call_count == 1


def test_reconcile_default_still_fetches_everything(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    mirrored = TodoEntry(text="remote", origin="todoist")
    mirrored.sync.todoist = TodoistSync(task_id="T1", ts="x", project_id="P1")
    fetch = MagicMock(return_value={"checked": False})
    monkeypatch.setattr(todoist, "fetch_task", fetch)
    todoist.reconcile([mirrored])
    assert fetch.call_count == 1  # standalone `todo reconcile` keeps full scan


# --- ls coherence -------------------------------------------------------------


def test_badges_distinguish_mirror_from_pushed():
    mirrored = TodoEntry(text="m", origin="todoist")
    mirrored.sync.todoist = TodoistSync(task_id="T1", ts="x")
    pushed = TodoEntry(text="p", source="cli")
    pushed.sync.todoist = TodoistSync(task_id="T2", ts="x")
    assert sync_badges(mirrored) == "[mirror]"
    assert sync_badges(pushed) == "[todoist]"


def test_ls_shows_due_date(capsys):
    e = TodoEntry(text="dated", due="2026-06-12")
    write_all([e])
    assert commands.cmd_ls(argparse.Namespace(filter="open")) == 0
    assert "[due 2026-06-12]" in capsys.readouterr().out


# --- telegram push uses the lock ----------------------------------------------


def test_telegram_push_task_holds_lock(monkeypatch):
    from todo_cli import telegram

    monkeypatch.setattr(telegram.todoist, "token", lambda: "tok")
    monkeypatch.setattr(telegram.todoist, "ensure_label", lambda *a, **k: None)
    monkeypatch.setattr(
        telegram.todoist, "create_task", lambda *a, **k: {"id": "T77"}
    )
    locked: list[bool] = []
    real_lock = storage.file_lock

    def spying_lock(*a, **k):
        locked.append(True)
        return real_lock(*a, **k)

    monkeypatch.setattr(telegram, "file_lock", spying_lock)

    assert telegram._push_task("buy milk") is True
    assert locked == [True]
    [entry] = load_all()
    assert entry.text == "buy milk"
    assert entry.sync.todoist.task_id == "T77"


def test_telegram_push_task_adopts_already_mirrored_row(monkeypatch):
    """If a refresh mirrored the just-created task while _push_task waited on
    the lock, the mirrored row is the record — no duplicate append."""
    from todo_cli import telegram

    monkeypatch.setattr(telegram.todoist, "token", lambda: "tok")
    monkeypatch.setattr(telegram.todoist, "ensure_label", lambda *a, **k: None)
    monkeypatch.setattr(
        telegram.todoist, "create_task", lambda *a, **k: {"id": "T77"}
    )
    mirrored = TodoEntry(text="buy milk", origin="todoist", source="telegram")
    mirrored.sync.todoist = TodoistSync(task_id="T77", ts="x")
    write_all([mirrored])

    assert telegram._push_task("buy milk") is True
    entries = load_all()
    assert len(entries) == 1  # adopted, not duplicated
    assert entries[0].origin == "todoist"


def test_mirror_fills_covered_with_included_projects(monkeypatch):
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
        lambda: {"source": ["cli"], "projects": ["todo"], "areas": []},
    )
    monkeypatch.setattr(
        todoist,
        "list_projects",
        lambda tok: [
            {"id": "P1", "is_shared": False},
            {"id": "S1", "is_shared": True},
        ],
    )
    monkeypatch.setattr(todoist, "list_active_tasks", lambda tok: [])
    covered: set[str] = set()
    assert todoist.mirror([], covered=covered) == 0
    assert covered == {"P1"}  # shared S1 excluded — sweep never judged it


def test_mirror_failed_listing_leaves_covered_empty(monkeypatch):
    import urllib.error

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
        lambda: {"source": [], "projects": [], "areas": []},
    )

    def boom(tok):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(todoist, "list_projects", boom)
    covered: set[str] = set()
    assert todoist.mirror([], covered=covered) == 1
    assert covered == set()  # reconcile degrades to the full scan


def test_mirror_update_skips_rederive_when_taxonomy_degraded(monkeypatch):
    """todoist-structure.json unreadable -> empty taxonomy. The update path
    must keep prior project/source instead of wiping them to ("todoist", None)."""
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
        lambda: {"source": [], "projects": [], "areas": []},
    )
    monkeypatch.setattr(
        todoist, "list_projects", lambda tok: [{"id": "P1", "is_shared": False}]
    )
    monkeypatch.setattr(
        todoist,
        "list_active_tasks",
        lambda tok: [
            {
                "id": "T1",
                "content": "remote",
                "project_id": "P1",
                "labels": ["claude", "todo"],
            }
        ],
    )
    e = TodoEntry(text="remote", origin="todoist", source="claude", project="todo")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x")
    todoist.mirror([e])
    assert e.source == "claude"
    assert e.project == "todo"
