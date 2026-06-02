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


# --- chat_id persistence + send-to-last-chat (delivery enabler) --------------

@pytest.fixture
def chat_file(tmp_path, monkeypatch):
    """Isolate the persisted chat_id file so the test never touches ~/.todo."""
    p = tmp_path / "telegram-chat.json"
    monkeypatch.setattr(telegram, "TELEGRAM_CHAT", p)
    return p


def test_chat_id_persists_and_reads_back(chat_file):
    assert telegram.last_chat_id() is None
    telegram._save_chat_id(424242)
    assert chat_file.exists()
    assert telegram.last_chat_id() == 424242
    # last writer wins
    telegram._save_chat_id(999)
    assert telegram.last_chat_id() == 999


def test_save_chat_id_ignores_none(chat_file):
    telegram._save_chat_id(None)
    assert not chat_file.exists()
    assert telegram.last_chat_id() is None


def test_send_uses_last_chat(chat_file, monkeypatch):
    sent = {}

    def fake_api(tok, method, params, timeout=35.0):
        sent["tok"] = tok
        sent["method"] = method
        sent["params"] = params
        return {"ok": True, "result": {"message_id": 1}}

    monkeypatch.setattr(telegram, "token", lambda: "TESTTOK")
    monkeypatch.setattr(telegram, "_api", fake_api)
    telegram._save_chat_id(555)

    assert telegram.send("ping from the bot") is True
    assert sent["method"] == "sendMessage"
    assert sent["params"]["chat_id"] == 555
    assert sent["params"]["text"] == "ping from the bot"


def test_send_no_chat_is_noop(chat_file, monkeypatch):
    monkeypatch.setattr(telegram, "token", lambda: "TESTTOK")
    monkeypatch.setattr(
        telegram, "_api",
        lambda *a, **k: pytest.fail("must not call the API with no chat_id"),
    )
    assert telegram.send("nobody to send to") is False


def test_send_no_token_is_noop(chat_file, monkeypatch):
    telegram._save_chat_id(7)
    monkeypatch.setattr(telegram, "token", lambda: None)
    monkeypatch.setattr(
        telegram, "_api",
        lambda *a, **k: pytest.fail("must not call the API with no token"),
    )
    assert telegram.send("no token") is False
