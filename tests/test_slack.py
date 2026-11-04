"""Slack transport: routing, outbound blocks, inbound captures, buttons, slash commands."""

from __future__ import annotations

import argparse
import json

import pytest
from todo_cli import commands, config, obsidian, slack, telegram

ROUTES = {"default": "CDEFAULT", "routes": {"capture": "CCAPTURE", "agents": "CAGENTS"}}


class FakeSlack:
    """Stands in for slack._http: scripted Web API answers plus file bytes."""

    def __init__(self):
        self.calls = []
        self.files = {}
        self.rate_limit_next = False

    def __call__(self, request, timeout):
        url = request.full_url
        if url in self.files:
            body, ctype = self.files[url]
            self.calls.append(("download", url, request.headers))
            return 200, {"Content-Type": ctype}, body
        method = url.rsplit("/", 1)[-1]
        raw = request.data.decode() if request.data else ""
        params = json.loads(raw) if raw.startswith("{") else raw
        self.calls.append((method, params, request.headers))
        if self.rate_limit_next:
            self.rate_limit_next = False
            return 429, {"Retry-After": "1"}, b'{"ok": false, "error": "ratelimited"}'
        if method == "chat.postMessage":
            return (
                200,
                {},
                json.dumps({"ok": True, "channel": params["channel"], "ts": "1.1"}).encode(),
            )
        return 200, {}, b'{"ok": true}'

    def of(self, method):
        return [params for m, params, _ in self.calls if m == method]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setattr(obsidian, "OBSIDIAN_VAULT", tmp_path / "vault")
    monkeypatch.setattr(telegram, "TELEGRAM_ACTIONS", tmp_path / "actions")
    monkeypatch.setattr(slack, "SLACK_ROUTES", tmp_path / "slack-routes.json")
    monkeypatch.setattr(slack, "SLACK_STATE", tmp_path / "slack-state.json")
    monkeypatch.setattr(slack, "SLACK_ALLOWED_USERS", ["UNATHAN"])
    monkeypatch.setattr(slack, "bot_token", lambda: "xoxb-test")
    monkeypatch.setattr(slack.time, "sleep", lambda s: None)
    (tmp_path / "slack-routes.json").write_text(json.dumps(ROUTES))
    fake = FakeSlack()
    monkeypatch.setattr(slack, "_http", fake)
    pushed = []
    monkeypatch.setattr(
        telegram,
        "_push_task",
        lambda text, source="telegram": pushed.append((text, source)) or True,
    )
    fake.pushed = pushed
    return fake


def test_route_resolution_falls_back_to_default():
    assert slack.resolve_channel("agents", ROUTES) == "CAGENTS"
    assert slack.resolve_channel("career", ROUTES) == "CDEFAULT"
    assert slack.resolve_channel("career", {}) is None


def test_send_with_buttons_registers_shared_actions(env, tmp_path):
    result = slack.send(
        "pick <one> & go", route="agents", buttons=[("Seen", "ack", "n1"), ("Bad", "shell", "x")]
    )

    assert result == {"channel": "CAGENTS", "ts": "1.1"}
    params = env.of("chat.postMessage")[0]
    assert params["text"] == "pick &lt;one&gt; &amp; go"
    buttons = params["blocks"][-1]["elements"]
    assert len(buttons) == 1  # the unknown verb is refused by the registry
    action = json.loads((tmp_path / "actions" / f"{buttons[0]['value']}.json").read_text())
    assert (action["verb"], action["payload"], action["status"]) == ("ack", "n1", "pending")


def test_send_retries_once_on_rate_limit(env):
    env.rate_limit_next = True
    assert slack.send("hello") is not None
    assert len(env.of("chat.postMessage")) == 2


def test_send_without_token_or_route_returns_none(env, monkeypatch, tmp_path):
    (tmp_path / "slack-routes.json").write_text("{}")
    assert slack.send("x") is None
    monkeypatch.setattr(slack, "bot_token", lambda: None)
    assert slack.send("x") is None
    assert env.of("chat.postMessage") == []


def test_long_text_is_chunked_into_sections():
    blocks = slack.build_blocks("a" * 7000, None)
    assert [len(b["text"]["text"]) for b in blocks] == [3000, 3000, 1000]


@pytest.mark.parametrize(
    "event,expected",
    [
        ({"type": "message", "channel": "CCAPTURE", "user": "U"}, True),
        ({"type": "message", "channel_type": "im", "channel": "D1", "user": "U"}, True),
        ({"type": "message", "channel": "CCAPTURE", "subtype": "file_share"}, True),
        ({"type": "message", "channel": "CCAPTURE", "bot_id": "B1"}, False),
        ({"type": "message", "channel": "CCAPTURE", "subtype": "message_changed"}, False),
        ({"type": "message", "channel": "COTHER", "user": "U"}, True),
    ],
)
def test_is_capture_message(event, expected):
    assert slack.is_capture_message(event, ROUTES) is expected


def test_task_message_files_capture_pushes_linear_and_replies_in_thread(env, tmp_path):
    event = {
        "type": "message",
        "channel": "CCAPTURE",
        "user": "UNATHAN",
        "text": "+t buy milk",
        "ts": "1700000000.1",
    }

    assert slack.handle_message_event(event, ROUTES) == "task"

    capture = next((tmp_path / "vault" / "captures").rglob("*-slack-*.md"))
    text = capture.read_text()
    assert "- [ ] buy milk" in text and "source: slack" in text
    assert env.pushed == [("buy milk", "slack")]
    reply = env.of("chat.postMessage")[0]
    assert reply["thread_ts"] == "1700000000.1" and reply["text"].startswith("filed ✓ task")


def test_voice_clip_is_saved_and_transcribed(env, tmp_path, monkeypatch):
    url = "https://files.slack.com/clip.m4a"
    env.files[url] = (b"AUDIO", "audio/mp4")
    monkeypatch.setattr(slack._transcribe_mod, "transcribe", lambda path: "+i solar boats")
    event = {
        "type": "message",
        "subtype": "file_share",
        "channel_type": "im",
        "channel": "D1",
        "user": "UNATHAN",
        "text": "",
        "ts": "1700000000.2",
        "files": [
            {
                "id": "F1",
                "name": "clip.m4a",
                "mimetype": "audio/mp4",
                "subtype": "slack_audio",
                "mode": "hosted",
                "url_private_download": url,
            }
        ],
    }

    assert slack.handle_message_event(event, ROUTES) == "idea"

    saved = next((tmp_path / "vault").rglob("Attachments/slack/*/clip.m4a"))
    assert saved.read_bytes() == b"AUDIO"
    download = next(c for c in env.calls if c[0] == "download")
    assert download[2]["Authorization"] == "Bearer xoxb-test"
    capture = next((tmp_path / "vault" / "captures").rglob("*-slack-*.md")).read_text()
    assert "solar boats" in capture and "saved `" in capture


def test_html_download_is_recorded_not_saved(env, tmp_path):
    url = "https://files.slack.com/doc.pdf"
    env.files[url] = (b"<html>login</html>", "text/html")
    record = slack._download_file(
        "xoxb-test", {"id": "F2", "name": "doc.pdf", "url_private": url}, tmp_path / "att"
    )
    assert record["downloaded"] is False and "HTTP 200, text/html" in record["error"]


def test_unauthorized_user_is_dropped(env, tmp_path):
    event = {
        "type": "message",
        "channel": "CCAPTURE",
        "user": "USTRANGER",
        "text": "hi",
        "ts": "1.0",
    }
    assert slack.handle_message_event(event, ROUTES) is None
    assert not (tmp_path / "vault").exists()


def test_button_click_executes_once_and_collapses(env):
    slack.send("digest", buttons=[("Seen", "ack", "n1")])
    posted = env.of("chat.postMessage")[0]
    payload = {
        "type": "block_actions",
        "user": {"id": "UNATHAN"},
        "channel": {"id": "CDEFAULT"},
        "message": {"ts": "1.1", "text": "digest", "blocks": posted["blocks"]},
        "actions": [dict(posted["blocks"][-1]["elements"][0])],
    }

    assert slack.handle_block_actions(payload) == ["✓"]
    assert slack.handle_block_actions(payload) == ["already done ✓"]
    update = env.of("chat.update")[0]
    assert all(b["type"] != "actions" for b in update["blocks"])


def test_agent_button_uses_slack_lock_not_telegram(env, monkeypatch):
    monkeypatch.setattr(telegram, "TELEGRAM_ALLOWED_CHATS", [])
    monkeypatch.delenv("TODO_AGENT_BRIDGE_CMD", raising=False)
    action_id = telegram._new_action("agent-kill", "rf-1", "Kill")
    toast = telegram._execute_action(telegram._load_action(action_id), agent_allowed=True)
    assert toast == "agent bridge not configured (set TODO_AGENT_BRIDGE_CMD)"


def test_slash_command_requires_lock_and_fires_bridge(env, monkeypatch):
    fired = []
    monkeypatch.setenv("TODO_AGENT_BRIDGE_CMD", "/bin/bridge")
    monkeypatch.setattr(slack.subprocess, "Popen", lambda args, **kw: fired.append(args))
    payload = {
        "command": "/cc",
        "text": "@cockpit fix it",
        "user_id": "UNATHAN",
        "channel_id": "CAGENTS",
    }

    assert slack.handle_slash_command(payload) == "on it: /claude @cockpit fix it"
    assert fired == [["/bin/bridge", "--chat-id", "CAGENTS", "--text", "/claude @cockpit fix it"]]

    monkeypatch.setattr(slack, "SLACK_ALLOWED_USERS", [])
    assert "open mode" in slack.handle_slash_command(payload)


def test_redelivered_event_is_filed_once(env, tmp_path):
    envelope = {
        "type": "events_api",
        "envelope_id": "E1",
        "payload": {
            "event_id": "Ev1",
            "event": {
                "type": "message",
                "channel": "CCAPTURE",
                "user": "UNATHAN",
                "text": "note",
                "ts": "2.0",
            },
        },
    }
    acks = []
    slack.handle_envelope(envelope, acks.append, ROUTES)
    slack.handle_envelope(envelope, acks.append, ROUTES)

    assert acks == [{"envelope_id": "E1"}, {"envelope_id": "E1"}]
    assert len(list((tmp_path / "vault" / "captures").rglob("*-slack-*.md"))) == 1


def test_socket_loop_acks_and_stops_on_disconnect(env, monkeypatch):
    monkeypatch.setattr(slack, "app_token", lambda: "xapp-test")
    monkeypatch.setattr(slack, "_open_socket_url", lambda token: "wss://fake")
    frames = [
        json.dumps({"type": "hello"}),
        json.dumps(
            {
                "type": "events_api",
                "envelope_id": "E9",
                "payload": {"event_id": "Ev9", "event": {"type": "reaction_added"}},
            }
        ),
        json.dumps({"type": "disconnect", "reason": "refresh_requested"}),
    ]

    class Socket:
        sent = []

        def recv(self):
            return frames.pop(0)

        def send(self, body):
            self.sent.append(json.loads(body))

        def close(self):
            pass

    sock = Socket()
    assert slack.run_socket_once(lambda url: sock) == "disconnect:refresh_requested"
    assert sock.sent == [{"envelope_id": "E9"}]


def _notify_args(**kw):
    base = {"text": ["hello"], "route": "career", "button": [], "thread": None, "check": False}
    base.update(kw)
    return argparse.Namespace(**base)


def test_notify_both_succeeds_when_one_transport_delivers(env, monkeypatch):
    monkeypatch.setattr(config, "NOTIFY_TRANSPORT", "both")
    monkeypatch.setattr(telegram, "send", lambda text, buttons=None: False)
    assert commands.cmd_notify(_notify_args()) == 0
    assert env.of("chat.postMessage")[0]["channel"] == "CDEFAULT"


def test_legacy_telegram_send_follows_transport(env, monkeypatch):
    monkeypatch.setattr(config, "NOTIFY_TRANSPORT", "slack")
    assert commands.cmd_telegram_send(argparse.Namespace(text=["hi"], button=[])) == 0
    assert env.of("chat.postMessage")[0]["channel"] == "CDEFAULT"


def test_notify_check_reports_problem_codes(env, monkeypatch, capsys):
    monkeypatch.setattr(config, "NOTIFY_TRANSPORT", "slack")
    assert commands.cmd_notify(_notify_args(check=True)) == 0
    monkeypatch.setattr(slack, "bot_token", lambda: None)
    assert commands.cmd_notify(_notify_args(check=True)) == 1
    assert "slack-token-missing" in capsys.readouterr().out


def test_notify_transport_reads_file_and_env_wins(tmp_path, monkeypatch):
    switch = tmp_path / "notify-transport"
    monkeypatch.setattr(config, "NOTIFY_TRANSPORT_FILE", switch)
    monkeypatch.delenv("TODO_NOTIFY_TRANSPORT", raising=False)
    assert config._notify_transport() == "telegram"

    switch.write_text("Slack\n")
    assert config._notify_transport() == "slack"

    monkeypatch.setenv("TODO_NOTIFY_TRANSPORT", "both")
    assert config._notify_transport() == "both"
