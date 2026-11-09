"""Actionable notifications: the action registry and the click executor."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
from todo_cli import actions, capture, obsidian
from todo_cli.models import TodoEntry
from todo_cli.storage import load_all, write_all


@pytest.fixture
def vault(tmp_path, monkeypatch):
    monkeypatch.setattr(obsidian, "OBSIDIAN_VAULT", tmp_path / "vault")
    return tmp_path / "vault"


@pytest.fixture
def registry(tmp_path, monkeypatch):
    monkeypatch.setattr(actions, "ACTIONS_DIR", tmp_path / "actions")
    return tmp_path / "actions"


def _execute(action_id: str, **kwargs) -> str:
    return actions.execute(actions.load(action_id), source="slack", **kwargs)


# --- registry ----------------------------------------------------------------


def test_register_writes_a_pending_record(registry):
    action_id = actions.register("add-task", "Buy milk", "Task")

    record = json.loads((registry / f"{action_id}.json").read_text())
    assert set(record) == {"id", "created", "verb", "payload", "label", "status"}
    assert (record["id"], record["verb"], record["payload"], record["label"]) == (
        action_id,
        "add-task",
        "Buy milk",
        "Task",
    )
    assert record["status"] == "pending"


def test_register_refuses_an_unknown_verb(registry):
    assert actions.register("shell", "rm -rf /", "Evil") is None
    assert not registry.exists()


def test_register_accepts_agent_verbs(registry):
    assert actions.valid_verb("agent-kill")
    assert actions.register("agent-kill", "rf-1", "Kill") is not None


def test_mark_records_the_outcome(registry):
    action_id = actions.register("ack", "n1", "Seen")

    actions.mark(action_id, "done", "✓")

    record = actions.load(action_id)
    assert (record["status"], record["result"]) == ("done", "✓")
    assert record["resolved"]


def test_load_rejects_ids_that_are_not_registry_ids(registry):
    registry.mkdir()
    (registry / "secret.json").write_text("{}")

    assert actions.load("secret") is None
    assert actions.load("../secret") is None
    assert actions.load("ffffffffffff") is None


def test_record_written_before_the_rename_still_loads_and_resolves(registry):
    # Verbatim shape of a record the retired transport wrote; the directory is
    # carried over as-is at cutover, so these must keep working.
    registry.mkdir()
    legacy = {
        "id": "0a1b2c3d4e5f",
        "created": "2026-09-30T08:15:02-04:00",
        "verb": "ack",
        "payload": "career-pulse:2026-09-30",
        "label": "Seen",
        "status": "pending",
    }
    (registry / "0a1b2c3d4e5f.json").write_text(json.dumps(legacy, indent=2))

    assert actions.load("0a1b2c3d4e5f") == legacy
    assert _execute("0a1b2c3d4e5f") == "✓"

    actions.mark("0a1b2c3d4e5f", "done", "✓")
    resolved = actions.load("0a1b2c3d4e5f")
    assert resolved["status"] == "done"
    assert {key: resolved[key] for key in legacy if key != "status"} == {
        key: legacy[key] for key in legacy if key != "status"
    }


def _configured_actions_dir(env: dict[str, str]) -> Path:
    """ACTIONS_DIR as a fresh interpreter resolves it (config is import-time)."""
    src = Path(actions.__file__).resolve().parents[1]
    out = subprocess.run(
        [sys.executable, "-c", "from todo_cli import config; print(config.ACTIONS_DIR)"],
        env={"PYTHONPATH": str(src), "HOME": env["TODO_DIR"], **env},
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(out.stdout.strip())


def test_registry_directory_defaults_to_actions_with_env_override(tmp_path):
    base = {"TODO_DIR": str(tmp_path)}
    assert _configured_actions_dir(base) == tmp_path / "actions"

    override = {**base, "TODO_ACTIONS": str(tmp_path / "elsewhere")}
    assert _configured_actions_dir(override) == tmp_path / "elsewhere"

    # The retired override must not be able to redirect the registry.
    retired = {**base, "TODO_TELEGRAM_ACTIONS": str(tmp_path / "old")}
    assert _configured_actions_dir(retired) == tmp_path / "actions"


# --- executor ----------------------------------------------------------------


def test_add_task_pushes_with_the_transport_source(registry, monkeypatch):
    monkeypatch.setenv("TODO_TASK_BACKEND", "todoist")  # legacy Todoist lane under test
    pushed = []
    monkeypatch.setattr(
        capture, "push_task", lambda text, source: pushed.append((text, source)) or True
    )
    action_id = actions.register("add-task", "Buy milk", "Task")

    assert _execute(action_id) == "task → Todoist ✓"
    assert pushed == [("Buy milk", "slack")]


def test_add_task_reports_a_failed_push(registry, monkeypatch):
    monkeypatch.setattr(capture, "push_task", lambda text, source: False)

    assert _execute(actions.register("add-task", "Buy milk", "Task")) == (
        "Linear push failed (see log)"
    )
    assert _execute(actions.register("add-task", "  ", "Task")) == "empty task payload"


def test_unknown_stored_verb_is_reported_not_run(registry):
    assert actions.execute({"verb": "shell", "payload": "x"}, source="slack") == (
        "unknown verb: shell"
    )


def test_idea_hot_flips_heat_strip(registry, vault):
    ideas = vault / "05 Notes" / "ideas"
    ideas.mkdir(parents=True)
    idea = ideas / "idea-subconscious-renderer.md"
    idea.write_text(
        "# X\n\n**Status:** Raw · **Heat:** — · **Domain:** Tooling\n", encoding="utf-8"
    )
    action_id = actions.register("idea-hot", "subconscious-renderer", "Hot")

    assert _execute(action_id) == "idea → Hot 🔥"
    assert "**Heat:** Hot" in idea.read_text(encoding="utf-8")
    assert _execute(action_id) == "already hot 🔥"


def test_idea_hot_rejects_traversal_slug(vault):
    assert actions._idea_hot("../../etc/passwd") == "bad idea slug"


def test_todoist_complete_closes_the_row_once(registry, monkeypatch):
    monkeypatch.setenv("TODO_TASK_BACKEND", "todoist")  # legacy Todoist lane under test
    entry = TodoEntry(text="Buy milk", source="claude")
    write_all([entry])
    pushed = []
    monkeypatch.setattr(
        actions.todoist,
        "push_completions",
        lambda entries, tok=None: pushed.extend(e.id for e in entries) or (1, 0),
    )
    action_id = actions.register("todoist-complete", entry.id, "✓ 1")

    assert _execute(action_id) == "done ✓ Buy milk"
    assert pushed == [entry.id]
    stored = load_all()[0]
    assert stored.status == "done" and stored.done_source == "slack"

    # A second run finds the row already done: no second push.
    assert _execute(action_id) == "already done ✓"
    assert pushed == [entry.id]


def test_complete_todo_pending_when_push_fails(monkeypatch):
    entry = TodoEntry(text="Call school", source="claude")
    write_all([entry])
    monkeypatch.setattr(actions.todoist, "push_completions", lambda entries, tok=None: (0, 1))

    toast = actions._complete_todo(entry.id, "slack")

    # local done survives a failed remote leg; next sync retries
    assert load_all()[0].status == "done"
    assert toast == "done ✓ Call school (Todoist pending)"


def test_complete_todo_rejects_bad_or_missing_id():
    assert actions._complete_todo("../../etc", "slack") == "bad todo id"
    assert actions._complete_todo("deadbeef0000", "slack") == "todo not found"


def test_completion_keeps_an_existing_done_source(monkeypatch):
    # A row someone else already attributed must not be re-attributed.
    entry = TodoEntry(text="Old row", source="telegram")
    entry.done_source = "telegram"
    write_all([entry])
    monkeypatch.setattr(actions.todoist, "push_completions", lambda entries, tok=None: (1, 0))

    actions._complete_todo(entry.id, "slack")

    assert load_all()[0].done_source == "telegram"


# --- agent verbs -------------------------------------------------------------


def test_agent_verb_is_refused_without_a_user_lock(registry, monkeypatch):
    monkeypatch.setenv("TODO_AGENT_BRIDGE_CMD", "/bin/bridge")
    monkeypatch.setattr(
        actions.subprocess, "run", lambda *a, **k: pytest.fail("bridge must not run in open mode")
    )
    action_id = actions.register("agent-kill", "rf-1", "Kill")

    assert _execute(action_id) == "agent actions require a configured chat allow-list"
    assert _execute(action_id, agent_allowed=False) == (
        "agent actions require a configured chat allow-list"
    )


def test_agent_verb_needs_a_configured_bridge(registry, monkeypatch):
    monkeypatch.delenv("TODO_AGENT_BRIDGE_CMD", raising=False)
    action_id = actions.register("agent-kill", "rf-1", "Kill")

    assert _execute(action_id, agent_allowed=True) == (
        "agent bridge not configured (set TODO_AGENT_BRIDGE_CMD)"
    )


def test_agent_verb_invokes_the_bridge_with_the_frozen_contract(registry, monkeypatch):
    calls = []

    class Result:
        stdout = "killed rf-1\n"
        stderr = ""

    def fake_run(args, **kwargs):
        calls.append((args, kwargs))
        return Result()

    monkeypatch.setenv("TODO_AGENT_BRIDGE_CMD", "/bin/bridge")
    monkeypatch.setattr(actions.subprocess, "run", fake_run)
    action_id = actions.register("agent-kill", "rf-1", "Kill")

    assert _execute(action_id, chat_id="CAGENTS", agent_allowed=True) == "killed rf-1"
    assert _execute(action_id, agent_allowed=True) == "killed rf-1"

    with_chat, without_chat = calls
    assert with_chat[0] == [
        "/bin/bridge",
        "--action",
        "agent-kill",
        "--payload",
        "rf-1",
        "--chat-id",
        "CAGENTS",
    ]
    assert with_chat[1] == {"capture_output": True, "text": True, "timeout": 30}
    assert without_chat[0] == ["/bin/bridge", "--action", "agent-kill", "--payload", "rf-1"]
