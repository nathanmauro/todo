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


# --- media-safe Telegram capture --------------------------------------------

class _FakeResponse:
    def __init__(self, data: bytes):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self) -> bytes:
        return self.data


@pytest.fixture
def telegram_poll_env(vault, tmp_path, monkeypatch):
    monkeypatch.setattr(telegram, "TELEGRAM_STATE", tmp_path / "telegram-state.json")
    monkeypatch.setattr(telegram, "TELEGRAM_CHAT", tmp_path / "telegram-chat.json")
    monkeypatch.setattr(telegram, "TELEGRAM_ALLOWED_CHATS", ["123"])
    monkeypatch.setattr(telegram, "token", lambda: "TESTTOK")
    monkeypatch.setattr(telegram, "_push_task", lambda *a, **k: None)
    return tmp_path


def test_poll_once_files_document_without_caption(
    telegram_poll_env, vault, monkeypatch
):
    def fake_api(tok, method, params, timeout=35.0):
        if method == "getUpdates":
            return {
                "ok": True,
                "result": [{
                    "update_id": 10,
                    "message": {
                        "message_id": 77,
                        "date": 1780500000,
                        "chat": {"id": 123, "type": "private"},
                        "document": {
                            "file_id": "doc-file",
                            "file_unique_id": "doc-unique",
                            "file_name": "report.pdf",
                            "mime_type": "application/pdf",
                            "file_size": 7,
                        },
                    },
                }],
            }
        if method == "getFile":
            assert params["file_id"] == "doc-file"
            return {
                "ok": True,
                "result": {
                    "file_id": "doc-file",
                    "file_unique_id": "doc-unique",
                    "file_path": "documents/report.pdf",
                    "file_size": 7,
                },
            }
        if method == "sendMessage":
            return {"ok": True, "result": {"message_id": 78}}
        raise AssertionError(method)

    monkeypatch.setattr(telegram, "_api", fake_api)
    monkeypatch.setattr(
        telegram.urllib.request,
        "urlopen",
        lambda url, timeout=60: _FakeResponse(b"PDFDATA"),
    )

    assert telegram.poll_once() == 1
    captures = list((obsidian.captures_root()).glob("*/*.md"))
    assert len(captures) == 1
    body = captures[0].read_text()
    assert "Telegram document received" in body
    assert "report.pdf" in body
    assert "application/pdf" in body

    attachments = list((vault / "Attachments" / "telegram").glob("*/*"))
    assert len(attachments) == 1
    assert attachments[0].name.endswith(".pdf")
    assert attachments[0].read_bytes() == b"PDFDATA"


def test_poll_once_records_structured_message_without_media(
    telegram_poll_env, monkeypatch
):
    def fake_api(tok, method, params, timeout=35.0):
        if method == "getUpdates":
            return {
                "ok": True,
                "result": [{
                    "update_id": 11,
                    "message": {
                        "message_id": 79,
                        "date": 1780500010,
                        "chat": {"id": 123, "type": "private"},
                        "location": {"latitude": 40.44, "longitude": -79.99},
                    },
                }],
            }
        if method == "sendMessage":
            return {"ok": True, "result": {"message_id": 80}}
        raise AssertionError(method)

    monkeypatch.setattr(telegram, "_api", fake_api)

    assert telegram.poll_once() == 1
    captures = list((obsidian.captures_root()).glob("*/*.md"))
    assert len(captures) == 1
    body = captures[0].read_text()
    assert "Telegram location received" in body
    assert '"latitude": 40.44' in body
    assert '"longitude": -79.99' in body


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
