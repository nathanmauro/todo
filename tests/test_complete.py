"""Outbound completion leg: "done here -> done there".

Pins the new direction (local done -> Todoist close + Logseq DONE) and the
idempotency/echo guards that keep it from oscillating against the inbound
reconcile/mirror paths.
"""
from __future__ import annotations

import argparse
import io
import urllib.error
from unittest.mock import MagicMock

from todo_cli import commands, logseq, todoist
from todo_cli.models import LogseqSync, TodoEntry, TodoistSync
from todo_cli.storage import load_all, write_all


# --- Todoist: push_completions ----------------------------------------------


def _done_with_task(task_id="T1", **kw):
    e = TodoEntry(text="x", status="done", **kw)
    e.sync.todoist = TodoistSync(task_id=task_id, ts="x")
    return e


def test_push_closes_then_idempotent(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    ct = MagicMock()
    monkeypatch.setattr(todoist, "complete_task", ct)

    e = _done_with_task()
    assert todoist.push_completions([e]) == (1, 0)
    assert ct.call_count == 1
    assert e.sync.todoist.closed_ts is not None

    # closed_ts stamp makes a second pass a no-op
    assert todoist.push_completions([e]) == (0, 0)
    assert ct.call_count == 1


def test_push_skips_open_and_untracked(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    ct = MagicMock()
    monkeypatch.setattr(todoist, "complete_task", ct)

    open_row = TodoEntry(text="open")
    open_row.sync.todoist = TodoistSync(task_id="T1", ts="x")
    done_no_task = TodoEntry(text="done but never synced", status="done")

    assert todoist.push_completions([open_row, done_no_task]) == (0, 0)
    assert ct.call_count == 0  # never invents a remote task on completion


def test_push_404_counts_as_closed(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")

    def gone(tok, tid):
        raise urllib.error.HTTPError("u", 404, "nf", {}, io.BytesIO(b""))

    monkeypatch.setattr(todoist, "complete_task", gone)
    e = _done_with_task()
    assert todoist.push_completions([e]) == (1, 0)
    assert e.sync.todoist.closed_ts is not None


def test_push_network_error_leaves_unstamped_for_retry(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")

    def boom(tok, tid):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(todoist, "complete_task", boom)
    e = _done_with_task()
    assert todoist.push_completions([e]) == (0, 1)
    assert e.sync.todoist.closed_ts is None  # next sync retries


def test_push_no_token_is_noop(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: None)
    ct = MagicMock()
    monkeypatch.setattr(todoist, "complete_task", ct)
    e = _done_with_task()
    assert todoist.push_completions([e]) == (0, 0)
    assert ct.call_count == 0
    assert e.sync.todoist.closed_ts is None


# --- inbound flips stamp closed_ts (no echo back out) -----------------------


def test_reconcile_checked_stamps_closed_ts(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    monkeypatch.setattr(todoist, "fetch_task", lambda tok, tid: {"checked": True})
    e = TodoEntry(text="x")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x")
    todoist.reconcile([e])
    assert e.status == "done"
    assert e.sync.todoist.closed_ts is not None

    # the stamp means the outbound push won't try to re-close it
    ct = MagicMock()
    monkeypatch.setattr(todoist, "complete_task", ct)
    assert todoist.push_completions([e]) == (0, 0)
    assert ct.call_count == 0


def test_reconcile_404_stamps_closed_ts(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")

    def gone(tok, tid):
        raise urllib.error.HTTPError("u", 404, "nf", {}, io.BytesIO(b""))

    monkeypatch.setattr(todoist, "fetch_task", gone)
    e = TodoEntry(text="x")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x")
    todoist.reconcile([e])
    assert e.sync.todoist.closed_ts is not None


def test_mirror_sweep_stamps_closed_ts(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    monkeypatch.setattr(
        todoist,
        "mirror_policy",
        lambda: {"exclude_shared": True, "exclude_project_ids": [], "exclude_completed": True},
    )
    monkeypatch.setattr(
        todoist,
        "taxonomy_labels",
        lambda: {"source": [], "projects": [], "areas": []},
    )
    monkeypatch.setattr(todoist, "list_projects", lambda tok: [{"id": "P1", "is_shared": False}])
    monkeypatch.setattr(todoist, "list_active_tasks", lambda tok: [])  # T9 vanished

    e = TodoEntry(text="was mirrored", origin="todoist")
    e.sync.todoist = TodoistSync(task_id="T9", ts="x", project_id="P1")
    todoist.mirror([e])
    assert e.status == "done"
    assert e.sync.todoist.closed_ts is not None

    # the stamp means the outbound push never echoes the sweep back to Todoist
    ct = MagicMock()
    monkeypatch.setattr(todoist, "complete_task", ct)
    assert todoist.push_completions([e]) == (0, 0)
    assert ct.call_count == 0


def test_mirror_reopens_done_mirror_back_in_active_set(monkeypatch):
    # A done origin="todoist" row whose task reappears active (un-completed on
    # web, or a recurring occurrence that advanced) is reopened to follow Todoist.
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    monkeypatch.setattr(
        todoist,
        "mirror_policy",
        lambda: {"exclude_shared": True, "exclude_project_ids": [], "exclude_completed": True},
    )
    monkeypatch.setattr(
        todoist, "taxonomy_labels", lambda: {"source": [], "projects": [], "areas": []}
    )
    monkeypatch.setattr(todoist, "list_projects", lambda tok: [{"id": "P1", "is_shared": False}])
    monkeypatch.setattr(
        todoist,
        "list_active_tasks",
        lambda tok: [{"id": "T9", "content": "back", "project_id": "P1", "labels": []}],
    )

    e = TodoEntry(text="back", status="done", done_source="todoist", origin="todoist")
    e.sync.todoist = TodoistSync(task_id="T9", ts="x", project_id="P1", closed_ts="2026-01-01T00:00:00")
    todoist.mirror([e])
    assert e.status == "open"
    assert e.done_source is None
    assert e.done_ts is None
    assert e.sync.todoist.closed_ts is None  # eligible to be closed again later


def test_mirror_never_reopens_locally_done_row(monkeypatch):
    # A locally-completed row (origin != todoist) sharing a task_id must NOT be
    # reopened by a remote refresh — preserves the mirror's docstring promise.
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    monkeypatch.setattr(
        todoist,
        "mirror_policy",
        lambda: {"exclude_shared": True, "exclude_project_ids": [], "exclude_completed": True},
    )
    monkeypatch.setattr(
        todoist, "taxonomy_labels", lambda: {"source": [], "projects": [], "areas": []}
    )
    monkeypatch.setattr(todoist, "list_projects", lambda tok: [{"id": "P1", "is_shared": False}])
    monkeypatch.setattr(
        todoist,
        "list_active_tasks",
        lambda tok: [{"id": "T1", "content": "local", "project_id": "P1", "labels": []}],
    )

    e = TodoEntry(text="local", status="done", done_source="local", source="cli")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x", project_id="P1")
    todoist.mirror([e])
    assert e.status == "done"  # untouched


def test_sync_creates_and_closes_in_one_pass(monkeypatch):
    monkeypatch.setattr(todoist, "token", lambda: "tok")
    monkeypatch.setattr(todoist, "ensure_label", lambda *a, **k: None)
    monkeypatch.setattr(todoist, "create_task", MagicMock(return_value={"id": "999"}))
    ct = MagicMock()
    monkeypatch.setattr(todoist, "complete_task", ct)

    open_row = TodoEntry(text="push me", source="cli")
    done_row = _done_with_task(task_id="T1")
    assert todoist.sync([open_row, done_row]) == 0
    assert open_row.sync.todoist.task_id == "999"
    ct.assert_called_once_with("tok", "T1")
    assert done_row.sync.todoist.closed_ts is not None


# --- Logseq: complete -------------------------------------------------------


def _journal(tmp_path, body):
    j = tmp_path / "2026_05_29.md"
    j.write_text(body)
    return j


def _done_with_logseq(path, marker):
    e = TodoEntry(text="x", status="done")
    e.sync.logseq = LogseqSync(file=str(path), marker=marker, ts="x")
    return e


def test_logseq_complete_flips_todo(tmp_path):
    mk = "<!-- todo:abc -->"
    j = _journal(tmp_path, f"- TODO ship it {mk}\n- other line\n")
    e = _done_with_logseq(j, mk)
    assert logseq.complete([e]) == 1
    # exact: only the marked block flips, everything else byte-for-byte intact
    assert j.read_text() == f"- DONE ship it {mk}\n- other line\n"


def test_logseq_complete_flips_checkbox(tmp_path):
    mk = "<!-- todo:box -->"
    j = _journal(tmp_path, f"- [ ] do thing {mk}\n")
    e = _done_with_logseq(j, mk)
    assert logseq.complete([e]) == 1
    assert j.read_text() == f"- [x] do thing {mk}\n"


def test_logseq_complete_flips_doing(tmp_path):
    mk = "<!-- todo:doing -->"
    j = _journal(tmp_path, f"- DOING in progress {mk}\n")
    e = _done_with_logseq(j, mk)
    assert logseq.complete([e]) == 1
    assert j.read_text() == f"- DONE in progress {mk}\n"


def test_logseq_complete_preserves_no_trailing_newline(tmp_path):
    # last line, no trailing newline: flip must not append or eat a newline
    mk = "<!-- todo:last -->"
    j = _journal(tmp_path, f"- intro\n- TODO last task {mk}")
    e = _done_with_logseq(j, mk)
    assert logseq.complete([e]) == 1
    assert j.read_text() == f"- intro\n- DONE last task {mk}"


def test_logseq_complete_preserves_crlf(tmp_path):
    # a CRLF / mixed-ending journal must keep untouched lines verbatim
    mk = "<!-- todo:crlf -->"
    j = tmp_path / "2026_05_29.md"
    j.write_bytes(f"- TODO win {mk}\r\n- untouched note\r\n".encode())
    e = _done_with_logseq(j, mk)
    assert logseq.complete([e]) == 1
    assert j.read_bytes() == f"- DONE win {mk}\r\n- untouched note\r\n".encode()


def test_logseq_complete_anchors_to_trailing_marker(tmp_path):
    # a marker quoted in ANOTHER task's body must not flip that other task
    abc = "<!-- todo:abc -->"
    other = "<!-- todo:other -->"
    j = _journal(tmp_path, f"- TODO discuss the {abc} scheme {other}\n- TODO mine {abc}\n")
    e = _done_with_logseq(j, abc)
    assert logseq.complete([e]) == 1
    # only the line whose TRAILING marker is abc flips; the quoting line is left
    assert j.read_text() == (
        f"- TODO discuss the {abc} scheme {other}\n- DONE mine {abc}\n"
    )


def test_logseq_complete_counts_per_entry_on_duplicate_marker(tmp_path):
    # a copy-pasted block duplicates the marker; count is per-entry (1), not 2
    mk = "<!-- todo:dup -->"
    j = _journal(tmp_path, f"- TODO real {mk}\n- DOING copy {mk}\n")
    e = _done_with_logseq(j, mk)
    assert logseq.complete([e]) == 1
    assert j.read_text() == f"- DONE real {mk}\n- DONE copy {mk}\n"


def test_logseq_complete_idempotent(tmp_path):
    mk = "<!-- todo:done -->"
    j = _journal(tmp_path, f"- DONE already {mk}\n")
    e = _done_with_logseq(j, mk)
    assert logseq.complete([e]) == 0
    assert j.read_text() == f"- DONE already {mk}\n"


def test_logseq_complete_skips_unsynced(tmp_path):
    j = _journal(tmp_path, "- TODO orphan\n")
    e = TodoEntry(text="x", status="done")  # no sync.logseq
    assert logseq.complete([e]) == 0
    assert j.read_text() == "- TODO orphan\n"


# --- cmd_done end-to-end ----------------------------------------------------


def test_cmd_done_propagates_both_ways(tmp_path, monkeypatch):
    mk = "<!-- todo:e2e -->"
    j = _journal(tmp_path, f"- TODO finish feature {mk}\n")

    e = TodoEntry(text="finish feature")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x")
    e.sync.logseq = LogseqSync(file=str(j), marker=mk, ts="x")
    write_all([e])

    monkeypatch.setattr(todoist, "token", lambda: "tok")
    ct = MagicMock()
    monkeypatch.setattr(todoist, "complete_task", ct)

    rc = commands.cmd_done(argparse.Namespace(id_prefix=e.short_id))
    assert rc == 0
    ct.assert_called_once_with("tok", "T1")

    [back] = load_all()
    assert back.status == "done"
    assert back.done_source == "local"
    assert back.sync.todoist.closed_ts is not None
    assert f"- DONE finish feature {mk}" in j.read_text()


def test_cmd_done_offline_still_marks_local(tmp_path, monkeypatch):
    e = TodoEntry(text="no network")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x")
    write_all([e])

    monkeypatch.setattr(todoist, "token", lambda: "tok")

    def boom(tok, tid):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(todoist, "complete_task", boom)

    assert commands.cmd_done(argparse.Namespace(id_prefix=e.short_id)) == 0
    [back] = load_all()
    assert back.status == "done"  # local completion never blocked on the network
    assert back.sync.todoist.closed_ts is None  # next `todo sync` will retry


def test_cmd_done_survives_read_timeout(tmp_path, monkeypatch):
    # A stalled-but-connected Todoist raises socket.timeout (== TimeoutError,
    # NOT a URLError). cmd_done must not crash and must keep the local done.
    import socket

    e = TodoEntry(text="stalls")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x")
    write_all([e])

    monkeypatch.setattr(todoist, "token", lambda: "tok")

    def stall(tok, tid):
        raise socket.timeout("timed out")

    monkeypatch.setattr(todoist, "complete_task", stall)

    assert commands.cmd_done(argparse.Namespace(id_prefix=e.short_id)) == 0
    [back] = load_all()
    assert back.status == "done"
    assert back.sync.todoist.closed_ts is None  # retried by next sync


def test_converged_state_is_a_fixed_point(tmp_path, monkeypatch):
    # Fully converged (local done, Todoist closed via closed_ts, journal DONE):
    # a second pass over reconcile + push + logseq.complete is a total no-op.
    mk = "<!-- todo:fp -->"
    j = _journal(tmp_path, f"- DONE finish feature {mk}\n")
    before = j.read_text()

    e = TodoEntry(text="finish feature", status="done", done_source="local")
    e.sync.todoist = TodoistSync(task_id="T1", ts="x", closed_ts="2026-05-29T00:00:00")
    e.sync.logseq = LogseqSync(file=str(j), marker=mk, ts="x")

    monkeypatch.setattr(todoist, "token", lambda: "tok")
    ct = MagicMock()
    monkeypatch.setattr(todoist, "complete_task", ct)
    # reconcile only inspects open rows; a done row is never re-fetched/reopened
    monkeypatch.setattr(todoist, "fetch_task", MagicMock(side_effect=AssertionError("should not fetch")))

    assert todoist.reconcile([e]) == 0
    assert todoist.push_completions([e]) == (0, 0)
    assert logseq.complete([e]) == 0

    assert e.status == "done"
    assert e.sync.todoist.closed_ts == "2026-05-29T00:00:00"
    assert ct.call_count == 0
    assert j.read_text() == before  # journal byte-for-byte unchanged
