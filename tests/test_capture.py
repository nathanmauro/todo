"""Capture-lane invariants after the 2026-06-01 cutover.

The old Notion-drain + PARA-classifier-into-Logseq chain is retired (Notion is
read-only, Logseq is a frozen archive). What remains pinned here: the Telegram
message-text extractor, and the guarantee that every Logseq writer is a NO-OP
while sync is frozen (TODO_LOGSEQ_SYNC unset) so `todo add/done/sync` never touch
the frozen graph.
"""
from __future__ import annotations

import todo_cli.logseq as logseq
from todo_cli import telegram
from todo_cli.models import LogseqSync, TodoEntry


# --- telegram parser ---------------------------------------------------------

def test_telegram_message_text():
    assert telegram.message_text({"text": "  hi  "}, "tok") == "hi"
    assert telegram.message_text({"caption": "cap"}, "tok") == "cap"
    assert telegram.message_text({}, "tok") is None


# --- Logseq writers are frozen by default ------------------------------------

def test_logseq_sync_is_noop_when_frozen(tmp_path, monkeypatch):
    """With sync frozen (the default), no journal file is written or touched."""
    graph = tmp_path / "graph"
    (graph / "journals").mkdir(parents=True)
    monkeypatch.setattr(logseq, "LOGSEQ_GRAPH", graph)
    monkeypatch.setattr(logseq, "LOGSEQ_SYNC_ENABLED", False)

    entry = TodoEntry(text="should not be written", source="cli")
    assert logseq.sync([entry]) == 0
    # nothing appended, and the row is NOT stamped with a logseq marker
    assert not logseq.journal_path().exists()
    assert entry.sync.logseq is None


def test_logseq_note_is_noop_when_frozen(tmp_path, monkeypatch):
    graph = tmp_path / "graph"
    (graph / "journals").mkdir(parents=True)
    monkeypatch.setattr(logseq, "LOGSEQ_GRAPH", graph)
    monkeypatch.setattr(logseq, "LOGSEQ_SYNC_ENABLED", False)

    assert logseq.note("a thought", "abc12345") == 0
    assert not logseq.journal_path().exists()


def test_logseq_complete_is_noop_when_frozen(tmp_path, monkeypatch):
    monkeypatch.setattr(logseq, "LOGSEQ_SYNC_ENABLED", False)
    done = TodoEntry(text="done", status="done", source="cli")
    done.sync.logseq = LogseqSync(file="j.md", marker="m", ts="x")
    assert logseq.complete([done]) == 0


def test_logseq_sync_writes_when_enabled(tmp_path, monkeypatch):
    """Flipping TODO_LOGSEQ_SYNC on restores the writer (one-off backfill path)."""
    graph = tmp_path / "graph"
    (graph / "journals").mkdir(parents=True)
    monkeypatch.setattr(logseq, "LOGSEQ_GRAPH", graph)
    monkeypatch.setattr(logseq, "LOGSEQ_SYNC_ENABLED", True)

    entry = TodoEntry(text="now it writes", source="cli")
    assert logseq.sync([entry]) == 0
    assert "now it writes" in logseq.journal_path().read_text()
    assert entry.sync.logseq is not None
