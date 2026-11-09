"""Transport-neutral capture core: the classifier seam contract + file format.

These tests PIN the routing contract a future LLM / Black Box classifier must
keep (see the vault's 06 Backlog/llm-classifier-for-telegram-captures): "+t" /
"+task" -> task, "+i" / "+idea" -> idea, anything else -> note, prefix stripped,
empty-after-prefix falls back to note. They also pin the on-disk capture format
and the vault path helpers every transport shares.
"""

from __future__ import annotations

import urllib.parse

import pytest
from todo_cli import capture, obsidian
from todo_cli.models import TodoEntry
from todo_cli.storage import load_all, write_all

# --- classifier seam (the contract) -----------------------------------------


@pytest.mark.parametrize(
    "text, kind, body",
    [
        ("+t buy milk", "task", "buy milk"),
        ("+task call dentist", "task", "call dentist"),
        ("+i what if agents dreamed", "idea", "what if agents dreamed"),
        ("+idea pluggable router", "idea", "pluggable router"),
        ("just a plain thought", "note", "just a plain thought"),
        ("+T UPPER prefix", "task", "UPPER prefix"),
        ("  +i   trims  ", "idea", "trims"),
        ("+t", "note", "+t"),  # no body -> note fallback
        ("+thinking out loud", "note", "+thinking out loud"),  # not a real prefix
    ],
)
def test_classify_contract(text, kind, body):
    assert capture.classify(text) == (kind, body)


def test_agent_prefixes_default_and_env_override(monkeypatch):
    monkeypatch.delenv("TODO_AGENT_PREFIXES", raising=False)
    assert capture.agent_prefixes() == {"/claude", "/sessions", "/kill"}

    monkeypatch.setenv("TODO_AGENT_PREFIXES", "/claude, /codex,")
    assert capture.agent_prefixes() == {"/claude", "/codex"}


# --- on-disk capture format --------------------------------------------------


@pytest.fixture
def vault(tmp_path, monkeypatch):
    monkeypatch.setattr(obsidian, "OBSIDIAN_VAULT", tmp_path)
    return tmp_path


def test_write_capture_note(vault):
    p = obsidian.write_capture("a thought", kind="note", source="slack")
    assert p.exists()
    assert p.parent.parent.name == "captures"
    text = p.read_text()
    assert text.startswith("---\n")
    for line in ("type: note\n", "source: slack\n", "status: open\n"):
        assert line in text
    assert text.rstrip().endswith("a thought")


def test_write_capture_task_is_checkbox(vault):
    p = obsidian.write_capture("ship it", kind="task", source="slack")
    body = p.read_text()
    assert "type: task\n" in body
    assert "- [ ] ship it" in body


def test_write_capture_filename_pattern(vault):
    p = obsidian.write_capture("x", kind="idea", source="slack")
    # <HHMMSS>-<source>-<id8>.md
    parts = p.stem.split("-")
    assert parts[0].isdigit() and len(parts[0]) == 6
    assert parts[1] == "slack"
    assert len(parts[-1]) == 8


def test_write_capture_default_source_is_cli(vault):
    p = obsidian.write_capture("no transport named")
    assert "source: cli\n" in p.read_text()
    assert "-cli-" in p.name


# --- vault path helpers ------------------------------------------------------


def test_deep_link_format(vault):
    path = vault / "captures" / "2026-06-12" / "143022-slack-ab12cd34.md"
    link = obsidian.deep_link(path)
    assert link.startswith("obsidian://open?vault=")
    # vault name is the directory name (monkeypatched to tmp_path)
    assert f"vault={urllib.parse.quote(vault.name)}" in link
    assert "file=captures/2026-06-12/143022-slack-ab12cd34.md" in link
    # no double-encoding: path separator must stay as /
    assert "%2F" not in link


def test_deep_link_still_opens_a_capture_filed_by_the_retired_transport(vault):
    # Old captures keep their on-disk name; links to them must keep resolving.
    path = vault / "captures" / "2026-06-12" / "143022-telegram-ab12cd34.md"
    assert "file=captures/2026-06-12/143022-telegram-ab12cd34.md" in obsidian.deep_link(path)


def test_vault_relative_and_unique_path(vault, tmp_path_factory):
    inside = vault / "Attachments" / "slack" / "clip.m4a"
    assert obsidian.vault_relative(inside) == "Attachments/slack/clip.m4a"

    outside = tmp_path_factory.mktemp("elsewhere") / "clip.m4a"
    assert obsidian.vault_relative(outside) == str(outside)

    inside.parent.mkdir(parents=True)
    assert obsidian.unique_path(inside) == inside
    inside.write_bytes(b"1")
    assert obsidian.unique_path(inside).name == "clip-2.m4a"


# --- task push ---------------------------------------------------------------


def test_push_task_stamps_the_callers_source(monkeypatch):
    monkeypatch.setattr(capture.linear, "push_entry", lambda entry: None)

    assert capture.push_task("buy milk", "slack") is True

    [row] = load_all()
    assert (row.text, row.source) == ("buy milk", "slack")


def test_rows_from_the_retired_transport_still_load_and_round_trip():
    old = TodoEntry(text="filed last spring", source="telegram")
    old.status = "done"
    old.done_source = "telegram"
    write_all([old])

    [row] = load_all()
    assert (row.source, row.done_source) == ("telegram", "telegram")

    write_all([row])
    assert load_all()[0].model_dump() == row.model_dump()
