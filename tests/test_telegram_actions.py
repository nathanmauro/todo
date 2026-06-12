"""Actionable notifications: inline buttons, the action registry, and callbacks."""
from __future__ import annotations

import json

import pytest

from todo_cli import obsidian, telegram


@pytest.fixture
def vault(tmp_path, monkeypatch):
    monkeypatch.setattr(obsidian, "OBSIDIAN_VAULT", tmp_path / "vault")
    return tmp_path / "vault"


@pytest.fixture
def actions_env(vault, tmp_path, monkeypatch):
    monkeypatch.setattr(telegram, "TELEGRAM_STATE", tmp_path / "telegram-state.json")
    monkeypatch.setattr(telegram, "TELEGRAM_CHAT", tmp_path / "telegram-chat.json")
    monkeypatch.setattr(telegram, "TELEGRAM_ACTIONS", tmp_path / "telegram-actions")
    monkeypatch.setattr(telegram, "TELEGRAM_ALLOWED_CHATS", ["123"])
    monkeypatch.setattr(telegram, "token", lambda: "TESTTOK")
    (tmp_path / "telegram-chat.json").write_text(json.dumps({"chat_id": 123}))
    return tmp_path


class ApiRecorder:
    """Fake telegram._api: records every call, serves a scripted getUpdates."""

    def __init__(self, updates=None):
        self.updates = updates or []
        self.calls = []

    def __call__(self, tok, method, params, timeout=35.0):
        self.calls.append((method, params))
        if method == "getUpdates":
            return {"ok": True, "result": self.updates}
        return {"ok": True, "result": {}}

    def of(self, method):
        return [p for m, p in self.calls if m == method]


def callback_update(data, update_id=50, chat_id=123):
    return {
        "update_id": update_id,
        "callback_query": {
            "id": "cbq-1",
            "from": {"id": chat_id},
            "data": data,
            "message": {
                "message_id": 99,
                "chat": {"id": chat_id, "type": "private"},
            },
        },
    }


def test_send_with_buttons_registers_actions(actions_env, monkeypatch):
    api = ApiRecorder()
    monkeypatch.setattr(telegram, "_api", api)

    assert telegram.send("pick one", buttons=[("Do it", "ack", ""), ("Task", "add-task", "Buy milk")])

    sent = api.of("sendMessage")
    assert len(sent) == 1
    keyboard = json.loads(sent[0]["reply_markup"])["inline_keyboard"][0]
    assert [b["text"] for b in keyboard] == ["Do it", "Task"]
    for button in keyboard:
        action = telegram._load_action(button["callback_data"])
        assert action is not None and action["status"] == "pending"


def test_send_rejects_unknown_verb_button(actions_env, monkeypatch):
    api = ApiRecorder()
    monkeypatch.setattr(telegram, "_api", api)

    assert telegram.send("hi", buttons=[("Evil", "shell", "rm -rf /")])

    sent = api.of("sendMessage")
    assert len(sent) == 1
    assert "reply_markup" not in sent[0]  # bad verb dropped; message still goes out


def test_callback_executes_add_task_once(actions_env, monkeypatch):
    pushed = []
    monkeypatch.setattr(telegram, "_push_task", lambda text, source="telegram": pushed.append(text) or True)
    action_id = telegram._new_action("add-task", "Buy milk", "Task")
    api = ApiRecorder(updates=[callback_update(action_id)])
    monkeypatch.setattr(telegram, "_api", api)

    telegram.poll_once()

    assert pushed == ["Buy milk"]
    assert telegram._load_action(action_id)["status"] == "done"
    answers = api.of("answerCallbackQuery")
    assert answers and answers[0]["text"] == "task → Todoist ✓"
    collapsed = api.of("editMessageReplyMarkup")
    assert collapsed and json.loads(collapsed[0]["reply_markup"]) == {"inline_keyboard": []}
    # offset cursor advanced past the callback update
    assert json.loads((actions_env / "telegram-state.json").read_text())["offset"] == 50

    # second tap on the same button: no re-execution
    api2 = ApiRecorder(updates=[callback_update(action_id, update_id=51)])
    monkeypatch.setattr(telegram, "_api", api2)
    telegram.poll_once()
    assert pushed == ["Buy milk"]
    assert api2.of("answerCallbackQuery")[0]["text"] == "already done ✓"


def test_callback_unknown_action_answers_gracefully(actions_env, monkeypatch):
    api = ApiRecorder(updates=[callback_update("ffffffffffff")])
    monkeypatch.setattr(telegram, "_api", api)

    telegram.poll_once()

    assert api.of("answerCallbackQuery")[0]["text"] == "unknown or expired action"
    assert not api.of("editMessageReplyMarkup")


def test_callback_unauthorized_chat_is_dropped(actions_env, monkeypatch):
    executed = []
    monkeypatch.setattr(telegram, "_push_task", lambda *a, **k: executed.append(a) or True)
    action_id = telegram._new_action("add-task", "Buy milk", "Task")
    api = ApiRecorder(updates=[callback_update(action_id, chat_id=999)])
    monkeypatch.setattr(telegram, "_api", api)

    telegram.poll_once()

    assert not executed
    assert telegram._load_action(action_id)["status"] == "pending"
    # spinner still killed, but with no toast text
    assert api.of("answerCallbackQuery") == [{"callback_query_id": "cbq-1"}]


def test_idea_hot_flips_heat_strip(actions_env, vault, monkeypatch):
    ideas = vault / "05 Notes" / "ideas"
    ideas.mkdir(parents=True)
    idea = ideas / "idea-subconscious-renderer.md"
    idea.write_text("# X\n\n**Status:** Raw · **Heat:** — · **Domain:** Tooling\n", encoding="utf-8")
    action_id = telegram._new_action("idea-hot", "subconscious-renderer", "Hot")
    api = ApiRecorder(updates=[callback_update(action_id)])
    monkeypatch.setattr(telegram, "_api", api)

    telegram.poll_once()

    assert "**Heat:** Hot" in idea.read_text(encoding="utf-8")
    assert api.of("answerCallbackQuery")[0]["text"] == "idea → Hot 🔥"


def test_idea_hot_rejects_traversal_slug(actions_env):
    assert telegram._idea_hot("../../etc/passwd") == "bad idea slug"


def test_send_chunks_buttons_into_rows_of_three(actions_env, monkeypatch):
    api = ApiRecorder()
    monkeypatch.setattr(telegram, "_api", api)

    buttons = [(f"B{i}", "ack", "") for i in range(5)]
    assert telegram.send("digest", buttons=buttons)

    keyboard = json.loads(api.of("sendMessage")[0]["reply_markup"])["inline_keyboard"]
    assert [[b["text"] for b in row] for row in keyboard] == [["B0", "B1", "B2"], ["B3", "B4"]]


def test_callback_completes_todo_once(actions_env, monkeypatch):
    from todo_cli.models import TodoEntry
    from todo_cli.storage import load_all, write_all

    entry = TodoEntry(text="Buy milk", source="claude")
    write_all([entry])
    pushed = []
    monkeypatch.setattr(
        telegram.todoist,
        "push_completions",
        lambda entries, tok=None: pushed.extend(e.id for e in entries) or (1, 0),
    )
    action_id = telegram._new_action("todoist-complete", entry.id, "✓ 1")
    api = ApiRecorder(updates=[callback_update(action_id)])
    monkeypatch.setattr(telegram, "_api", api)

    telegram.poll_once()

    assert pushed == [entry.id]
    stored = load_all()[0]
    assert stored.status == "done" and stored.done_source == "telegram"
    assert api.of("answerCallbackQuery")[0]["text"] == "done ✓ Buy milk"

    # second tap: the row is already done — no second push
    api2 = ApiRecorder(updates=[callback_update(action_id, update_id=51)])
    monkeypatch.setattr(telegram, "_api", api2)
    telegram.poll_once()
    assert pushed == [entry.id]
    assert api2.of("answerCallbackQuery")[0]["text"] == "already done ✓"


def test_complete_todo_pending_when_push_fails(actions_env, monkeypatch):
    from todo_cli.models import TodoEntry
    from todo_cli.storage import load_all, write_all

    entry = TodoEntry(text="Call school", source="claude")
    write_all([entry])
    monkeypatch.setattr(
        telegram.todoist, "push_completions", lambda entries, tok=None: (0, 1)
    )

    toast = telegram._complete_todo(entry.id)

    # local done survives a failed remote leg; next sync retries
    assert load_all()[0].status == "done"
    assert toast == "done ✓ Call school (Todoist pending)"


def test_complete_todo_rejects_bad_or_missing_id(actions_env):
    assert telegram._complete_todo("../../etc") == "bad todo id"
    assert telegram._complete_todo("deadbeef0000") == "todo not found"
