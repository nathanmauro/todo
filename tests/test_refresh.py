"""Refresh/audit convergence behavior."""
from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from todo_cli import commands, logseq, todoist
from todo_cli.models import LogseqSync, TodoEntry, TodoistSync
from todo_cli.storage import load_all, write_all


def test_logseq_sync_skips_todoist_origin_rows(tmp_path, monkeypatch):
    graph = tmp_path / "graph"
    (graph / "journals").mkdir(parents=True)
    monkeypatch.setattr(logseq, "LOGSEQ_GRAPH", graph)
    # Logseq sync is frozen by default; this test pins the *enabled* behavior
    # (the mirror-origin exclusion that a one-off backfill must still honor).
    monkeypatch.setattr(logseq, "LOGSEQ_SYNC_ENABLED", True)

    local = TodoEntry(text="local task", source="cli")
    mirrored = TodoEntry(text="remote backlog", source="todoist", origin="todoist")

    assert logseq.sync([local, mirrored]) == 0

    body = logseq.journal_path().read_text()
    assert "local task" in body
    assert "remote backlog" not in body
    assert local.sync.logseq is not None
    assert mirrored.sync.logseq is None


def test_add_persists_even_when_best_effort_sync_fails(monkeypatch):
    calls = []

    def fail_sync(entries):
        calls.append(len(entries))
        raise RuntimeError("offline")

    monkeypatch.setattr(commands, "_sync_outbound", fail_sync)

    rc = commands.cmd_add(
        argparse.Namespace(
            text=["capture", "this"],
            source="cli",
            due=None,
            project="todo",
            no_sync=False,
        )
    )

    assert rc == 0
    [entry] = load_all()
    assert entry.text == "capture this"
    assert entry.project == "todo"
    assert calls == [1]


def test_add_no_sync_defers_outbound(monkeypatch):
    def unexpected(entries):
        raise AssertionError("sync should not run")

    monkeypatch.setattr(commands, "_sync_outbound", unexpected)

    assert commands.cmd_add(
        argparse.Namespace(
            text=["defer", "me"],
            source="cli",
            due=None,
            project=None,
            no_sync=True,
        )
    ) == 0
    [entry] = load_all()
    assert entry.text == "defer me"
    assert entry.sync.todoist is None
    assert entry.sync.logseq is None


def test_refresh_order_and_write_boundaries(monkeypatch):
    write_all([TodoEntry(text="x")])
    calls = []

    monkeypatch.setattr(
        todoist,
        "mirror",
        lambda entries, dry_run=False, covered=None: calls.append("mirror") or 0,
    )
    monkeypatch.setattr(
        logseq, "reconcile", lambda entries: calls.append("logseq.reconcile") or 0
    )
    monkeypatch.setattr(
        todoist,
        "reconcile",
        lambda entries, skip_project_ids=None: calls.append(
            "todoist.reconcile(covered)"
            if skip_project_ids is not None
            else "todoist.reconcile(full)"
        )
        or 0,
    )
    monkeypatch.setattr(
        logseq, "sync", lambda entries: calls.append("logseq.sync") or 0
    )
    monkeypatch.setattr(
        todoist, "sync", lambda entries: calls.append("todoist.sync") or 0
    )
    monkeypatch.setattr(commands, "write_all", lambda entries: calls.append("write"))

    assert commands.cmd_refresh(argparse.Namespace(dry_run=False)) == 0
    assert calls == [
        "mirror",
        "logseq.reconcile",
        # refresh hands mirror's covered-project set to reconcile so sweep-
        # covered mirrored rows skip the per-task fetch.
        "todoist.reconcile(covered)",
        "write",
        "logseq.sync",
        "todoist.sync",
        "write",
    ]


def test_audit_counts(capsys):
    local_missing = TodoEntry(text="local missing", source="cli")
    mirrored = TodoEntry(text="remote", origin="todoist", source="todoist")
    mirrored.sync.todoist = TodoistSync(task_id="T1", ts="x")
    done = TodoEntry(text="done", status="done", source="cli")
    # A legacy row that still carries the dormant notion_inbox_id field must
    # still parse and be counted normally (no special-cased audit line anymore).
    linked = TodoEntry(text="legacy mobile task", source="mobile", notion_inbox_id="N1")
    linked.sync.logseq = LogseqSync(file="j.md", marker="m", ts="x")

    write_all([local_missing, mirrored, done, linked])

    assert commands.cmd_audit(argparse.Namespace()) == 0
    out = capsys.readouterr().out
    assert "total: 4" in out
    assert "open: 3" in out
    assert "done: 1" in out
    assert "origin_todoist: 1" in out
    assert "open_local_missing_todoist: 2" in out
    assert "open_local_missing_logseq: 1" in out
    assert "open_mirrored_missing_logseq_expected: 1" in out
    assert "notion_inbox_linked" not in out


def test_session_hook_uses_refresh():
    hook = Path(
        "/Users/nathan/Developer/proj/cockpit/scripts/cockpit-todoist-session-hook"
    )
    if not hook.exists():
        pytest.skip("cockpit hook is outside this checkout")
    body = hook.read_text()
    assert '"$TODO_BIN" refresh' in body
    assert '"$TODO_BIN" pull' not in body
