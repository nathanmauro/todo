"""Telegram -> Obsidian capture lane: the classifier seam contract + file format.

These tests PIN the routing contract a future LLM / Black Box classifier must
keep (see the vault's 06 Backlog/llm-classifier-for-telegram-captures): "+t" /
"+task" -> task, "+i" / "+idea" -> idea, anything else -> note, prefix stripped,
empty-after-prefix falls back to note. They also pin the on-disk capture format.
"""
from __future__ import annotations

import pytest

from todo_cli import obsidian, telegram


# --- classifier seam (the contract) -----------------------------------------

@pytest.mark.parametrize("text, kind, body", [
    ("+t buy milk", "task", "buy milk"),
    ("+task call dentist", "task", "call dentist"),
    ("+i what if agents dreamed", "idea", "what if agents dreamed"),
    ("+idea pluggable router", "idea", "pluggable router"),
    ("just a plain thought", "note", "just a plain thought"),
    ("+T UPPER prefix", "task", "UPPER prefix"),
    ("  +i   trims  ", "idea", "trims"),
    ("+t", "note", "+t"),                       # no body -> note fallback
    ("+thinking out loud", "note", "+thinking out loud"),  # not a real prefix
])
def test_classify_contract(text, kind, body):
    assert telegram.classify(text) == (kind, body)


# --- on-disk capture format --------------------------------------------------

@pytest.fixture
def vault(tmp_path, monkeypatch):
    monkeypatch.setattr(obsidian, "OBSIDIAN_VAULT", tmp_path)
    return tmp_path


def test_write_capture_note(vault):
    p = obsidian.write_capture("a thought", kind="note", source="telegram")
    assert p.exists()
    assert p.parent.parent.name == "captures"
    text = p.read_text()
    assert text.startswith("---\n")
    for line in ("type: note\n", "source: telegram\n", "status: open\n"):
        assert line in text
    assert text.rstrip().endswith("a thought")


def test_write_capture_task_is_checkbox(vault):
    p = obsidian.write_capture("ship it", kind="task", source="telegram")
    body = p.read_text()
    assert "type: task\n" in body
    assert "- [ ] ship it" in body


def test_write_capture_filename_pattern(vault):
    p = obsidian.write_capture("x", kind="idea", source="telegram")
    # <HHMMSS>-<source>-<id8>.md
    parts = p.stem.split("-")
    assert parts[0].isdigit() and len(parts[0]) == 6
    assert parts[1] == "telegram"
    assert len(parts[-1]) == 8


def test_route_writes_file_and_pushes_task(vault, monkeypatch):
    # stub the Todoist push so the test never touches the network
    pushed: list[str] = []
    monkeypatch.setattr(
        telegram, "_push_task", lambda text, source="telegram": pushed.append(text)
    )
    kind, path = telegram._route("+t do the thing")
    assert kind == "task"
    assert path.exists()
    assert "- [ ] do the thing" in path.read_text()
    assert pushed == ["do the thing"]


def test_route_note_does_not_push(vault, monkeypatch):
    monkeypatch.setattr(
        telegram, "_push_task",
        lambda *a, **k: pytest.fail("notes must not push to Todoist"),
    )
    kind, path = telegram._route("plain note")
    assert kind == "note"
    assert path.exists()
