"""Slack transport: routing, outbound blocks, inbound captures, buttons, slash commands."""

from __future__ import annotations

import argparse
import json

import pytest
from todo_cli import actions, capture, commands, obsidian, slack

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
    monkeypatch.setattr(actions, "ACTIONS_DIR", tmp_path / "actions")
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
        capture,
        "push_task",
        lambda text, source: pushed.append((text, source)) or True,
    )
    fake.pushed = pushed
    fake.tmp_path = tmp_path
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


def _click(env, verb, payload, user="UNATHAN"):
    """Send one button and return the block_actions payload for clicking it."""
    slack.send("digest", buttons=[("Go", verb, payload)])
    posted = env.of("chat.postMessage")[-1]
    return {
        "type": "block_actions",
        "user": {"id": user},
        "channel": {"id": "CDEFAULT"},
        "message": {"ts": "1.1", "text": "digest", "blocks": posted["blocks"]},
        "actions": [dict(posted["blocks"][-1]["elements"][0])],
    }


def test_add_task_button_pushes_a_slack_sourced_task_once(env):
    payload = _click(env, "add-task", "Buy milk")

    assert slack.handle_block_actions(payload) == ["task → Linear ✓"]
    assert slack.handle_block_actions(payload) == ["already done ✓"]
    assert env.pushed == [("Buy milk", "slack")]


def test_button_click_from_unauthorized_user_is_dropped(env):
    payload = _click(env, "add-task", "Buy milk", user="USTRANGER")
    action_id = payload["actions"][0]["value"]

    assert slack.handle_block_actions(payload) == []
    assert env.pushed == []
    assert actions.load(action_id)["status"] == "pending"
    assert env.of("chat.update") == []


def test_button_click_on_unknown_action_answers_gracefully(env):
    payload = _click(env, "ack", "n1")
    payload["actions"][0]["value"] = "ffffffffffff"

    assert slack.handle_block_actions(payload) == ["unknown or expired action"]


def test_agent_button_is_gated_by_the_slack_user_lock(env, monkeypatch):
    fired = []

    def fake_run(args, **kwargs):
        fired.append(args)
        return argparse.Namespace(stdout="killed rf-1\n", stderr="")

    monkeypatch.setenv("TODO_AGENT_BRIDGE_CMD", "/bin/bridge")
    monkeypatch.setattr(actions.subprocess, "run", fake_run)

    assert slack.handle_block_actions(_click(env, "agent-kill", "rf-1")) == ["killed rf-1"]
    # The frozen bridge contract for a button: --action, --payload, --chat-id.
    assert fired == [
        ["/bin/bridge", "--action", "agent-kill", "--payload", "rf-1", "--chat-id", "CDEFAULT"]
    ]

    # Open mode: the listener has no allow-list, so agent verbs are refused.
    monkeypatch.setattr(slack, "SLACK_ALLOWED_USERS", [])
    toasts = slack.handle_block_actions(_click(env, "agent-kill", "rf-2"))
    assert toasts == ["agent actions require a configured chat allow-list"]
    assert len(fired) == 1


def test_queued_task_reply_says_so_once(env, tmp_path, monkeypatch):
    monkeypatch.setattr(capture, "push_task", lambda text, source: False)
    event = {
        "type": "message",
        "channel": "CCAPTURE",
        "user": "UNATHAN",
        "text": "+t buy milk",
        "ts": "1700000000.3",
    }

    assert slack.handle_message_event(event, ROUTES) == "task"

    reply = env.of("chat.postMessage")[0]["text"]
    assert "saved locally, Linear push queued (see todo.log)" in reply
    assert "obsidian://open?vault=vault&amp;file=captures/" in reply
    assert slack._PUSH_QUEUED == set()


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


def test_notify_posts_to_the_route_channel(env, capsys):
    assert commands.cmd_notify(_notify_args(route="agents")) == 0
    assert env.of("chat.postMessage")[0]["channel"] == "CAGENTS"
    assert capsys.readouterr().out == "slack: sent to route agents ts 1.1\n"


def test_notify_exits_nonzero_when_slack_rejects(env, monkeypatch, capsys):
    monkeypatch.setattr(slack, "bot_token", lambda: None)
    assert commands.cmd_notify(_notify_args()) == 1
    assert "slack: not sent to route career" in capsys.readouterr().out


def test_notify_ignores_the_retired_transport_switch(env, monkeypatch):
    # launchd plists may still export it; Slack is the only wire now.
    monkeypatch.setenv("TODO_NOTIFY_TRANSPORT", "telegram")
    assert commands.cmd_notify(_notify_args()) == 0
    assert env.of("chat.postMessage")[0]["channel"] == "CDEFAULT"


def test_notify_check_reports_problem_codes(env, monkeypatch, capsys):
    assert commands.cmd_notify(_notify_args(route="agents", check=True)) == 0
    assert capsys.readouterr().out == "ready\n"

    assert commands.cmd_notify(_notify_args(route="default", check=True)) == 0
    assert capsys.readouterr().out == "ready\n"

    # A send would land in the default room, but a producer asking about its own route
    # must hear that the route has no channel (career sat in #alerts unnoticed this way).
    assert commands.cmd_notify(_notify_args(check=True)) == 1
    assert capsys.readouterr().out == "slack-route-unmapped\n"

    (env.tmp_path / "slack-routes.json").write_text("{}")
    assert commands.cmd_notify(_notify_args(check=True)) == 1
    assert capsys.readouterr().out == "slack-route-unmapped\n"

    monkeypatch.setattr(slack, "bot_token", lambda: None)
    assert commands.cmd_notify(_notify_args(check=True)) == 1
    assert capsys.readouterr().out == "slack-token-missing\n"


def test_notify_cli_surface_is_unchanged():
    from todo_cli.cli import build_parser

    args = build_parser().parse_args(
        ["notify", "--route", "digest", "--button", "Seen=ack:n1", "--thread", "1.2", "hi", "there"]
    )
    assert (args.route, args.button, args.thread, args.check) == (
        "digest",
        ["Seen=ack:n1"],
        "1.2",
        False,
    )
    assert args.text == ["hi", "there"]
    assert build_parser().parse_args(["notify", "--check"]).check is True


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("<@U0CERJYFEF6> hope you are there now", "hope you are there now"),
        ("<@U0CERJYFEF6>: +t call mom", "+t call mom"),
        ("ping <@U0D50R52P> later", "ping <@U0D50R52P> later"),
        ("plain thought", "plain thought"),
    ],
)
def test_strip_leading_mentions(raw, expected):
    assert slack._strip_leading_mentions(raw) == expected


def test_doctor_flags_bot_token_in_app_slot():
    name, ok, detail = slack._token_check("app token (xapp)", "xoxb-123", "xapp-", "slack-app")
    assert not ok
    assert "wrong type" in detail
    assert "123" not in detail


def test_user_lock_reads_listener_plist(tmp_path, monkeypatch):
    import plistlib

    plist = tmp_path / "listener.plist"
    plist.write_bytes(plistlib.dumps({"EnvironmentVariables": {"SLACK_ALLOWED_USER_ID": "U1"}}))
    monkeypatch.setattr(slack, "SLACK_ALLOWED_USERS", [])
    monkeypatch.setattr(slack, "LISTENER_PLIST", plist)
    assert slack._user_lock_check()[1] is True

    monkeypatch.setattr(slack, "LISTENER_PLIST", tmp_path / "missing.plist")
    assert slack._user_lock_check()[1] is False
