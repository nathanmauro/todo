"""PARA auto-filing + Telegram producer invariants.

Pins the capture-filing behavior added on top of the Notion drain: page index
excludes agent logs, page/journal writes are idempotent, the ledger prevents
double-filing across classifier non-determinism, `_file_capture` routes by the
classifier's decision, and the Telegram text parser extracts captures.
"""
from __future__ import annotations

import pytest

from todo_cli import classify, commands, ledger, logseq, telegram
from todo_cli.classify import Decision
from todo_cli.notion import InboxRow


@pytest.fixture
def graph(tmp_path, monkeypatch):
    """Isolated Logseq graph + ledger, never the real ~/Notes / ~/.notion-sync."""
    (tmp_path / "pages").mkdir()
    (tmp_path / "journals").mkdir()
    monkeypatch.setattr(logseq, "LOGSEQ_GRAPH", tmp_path)
    monkeypatch.setattr(ledger, "FILED_LEDGER", tmp_path / "filed.json")
    return tmp_path


def _row(text, page_id="p1", idea=False, task=False):
    return InboxRow(page_id=page_id, text=text, idea=idea, task=task, source="telegram")


# --- page index --------------------------------------------------------------

def test_page_index_excludes_agent_logs(graph):
    (graph / "pages" / "Event Pipeline.md").write_text("- x\n")
    (graph / "pages" / "prj___MenuTasks.md").write_text("- x\n")
    (graph / "pages" / "claude___Notes___foo.md").write_text("- x\n")
    (graph / "pages" / "claude-memory___todo___bar.md").write_text("- x\n")
    idx = logseq.page_index()
    assert idx == {
        "Event Pipeline": "Event Pipeline.md",
        "prj/MenuTasks": "prj___MenuTasks.md",
    }


# --- idempotent writes -------------------------------------------------------

def test_append_to_page_creates_props_then_dedups(graph):
    mk = "<!-- nx:abc -->"
    p = logseq.append_to_page("res___t.md", f"- hello {mk}", marker=mk,
                              create_props="para:: resource")
    assert p is not None
    body = (graph / "pages" / "res___t.md").read_text()
    assert body.startswith("para:: resource\n")
    assert body.count(mk) == 1
    # second call with the same marker is a no-op
    assert logseq.append_to_page("res___t.md", f"- hello {mk}", marker=mk) is None
    assert (graph / "pages" / "res___t.md").read_text().count(mk) == 1


def test_append_journal_dedup(graph):
    mk = "<!-- nx:j1 -->"
    assert logseq.append_journal_dedup(f"- thought {mk}", mk) is True
    assert logseq.append_journal_dedup(f"- thought {mk}", mk) is False
    assert logseq.journal_path().read_text().count(mk) == 1


# --- ledger ------------------------------------------------------------------

def test_ledger_record_and_has(graph):
    assert ledger.has("p1") is False
    ledger.record("p1", "Event Pipeline.md", confidence=0.9, source="telegram")
    assert ledger.has("p1") is True
    assert ledger.target_for("p1") == "Event Pipeline.md"


# --- _file_capture routing (classifier mocked for determinism) ---------------

def test_file_capture_routes_to_page(graph, monkeypatch):
    (graph / "pages" / "Event Pipeline.md").write_text("- existing\n")
    monkeypatch.setattr(classify, "classify", lambda t, p: Decision(
        "page", target_file="Event Pipeline.md", page_name="Event Pipeline",
        links=["Foo"], confidence=0.92))
    desc = commands._file_capture(_row("batch the writes"), {"Event Pipeline": "Event Pipeline.md"}, dry_run=False)
    assert "Event Pipeline" in desc
    body = (graph / "pages" / "Event Pipeline.md").read_text()
    assert "batch the writes" in body and "[[Foo]]" in body and "<!-- nx:p1 -->" in body
    assert ledger.target_for("p1") == "Event Pipeline.md"


def test_file_capture_journal_default(graph, monkeypatch):
    monkeypatch.setattr(classify, "classify", lambda t, p: Decision("journal", confidence=1.0))
    desc = commands._file_capture(_row("buy milk"), {"X": "X.md"}, dry_run=False)
    assert desc.startswith("journal")
    assert "buy milk" in logseq.journal_path().read_text()
    assert ledger.has("p1")


def test_file_capture_idea_skips_classifier(graph, monkeypatch):
    def boom(*a, **k):
        raise AssertionError("classifier must not run for idea rows")
    monkeypatch.setattr(classify, "classify", boom)
    desc = commands._file_capture(_row("a moonshot", idea=True), {}, dry_run=False)
    assert desc == "journal (#idea)"
    assert "#idea a moonshot" in logseq.journal_path().read_text()


def test_file_capture_inbox_quarantine(graph, monkeypatch):
    monkeypatch.setattr(classify, "classify", lambda t, p: Decision("inbox", confidence=0.5))
    desc = commands._file_capture(_row("ambiguous note"), {"X": "X.md"}, dry_run=False)
    assert "inbox-capture" in desc
    inbox = graph / "pages" / "inbox-capture.md"
    assert inbox.exists()
    assert "para:: resource" in inbox.read_text()
    assert "ambiguous note" in inbox.read_text()


def test_file_capture_dry_run_writes_nothing(graph, monkeypatch):
    monkeypatch.setattr(classify, "classify", lambda t, p: Decision(
        "page", target_file="Event Pipeline.md", page_name="Event Pipeline", confidence=0.99))
    commands._file_capture(_row("x"), {"Event Pipeline": "Event Pipeline.md"}, dry_run=True)
    assert not (graph / "pages" / "Event Pipeline.md").exists()
    assert ledger.has("p1") is False


# --- telegram parser ---------------------------------------------------------

def test_telegram_message_text():
    assert telegram.message_text({"text": "  hi  "}, "tok") == "hi"
    assert telegram.message_text({"caption": "cap"}, "tok") == "cap"
    assert telegram.message_text({}, "tok") is None
