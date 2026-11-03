# Slack capture and notifications (replaces Telegram)

Slack is the messaging transport; Linear stays the task system, Obsidian the note
store, Black Box the agent record. `src/todo_cli/slack.py` owns the wire; the
classifier, Obsidian writer, Linear push, and action executor are shared with the
Telegram lane until it is retired.

## Pieces

- `todo slack-listen` — Socket Mode daemon (`launchd/com.nathan.slack-capture.plist`).
  Outbound websocket only, so no public endpoint. Messages in the `capture` channel
  or the bot DM become one capture under `captures/YYYY-MM-DD/<HHMMSS>-slack-<id>.md`;
  `+t` / `+i` prefixes work as on Telegram. Files land in `Attachments/slack/`;
  voice clips are transcribed locally (Parakeet, whisper.cpp fallback). The bot
  replies in thread `filed ✓ <kind>` with an Obsidian link.
- Buttons — `todo notify --button Label=verb[:payload]` registers the same action
  records under `~/.todo/telegram-actions/` that Job Scout reads; a click executes
  once and collapses the buttons. `agent-*` verbs need `SLACK_ALLOWED_USER_ID`.
- Slash commands — `/cc`, `/cc-sessions`, `/cc-kill` (mapped to the bridge's `/claude`, `/sessions`, `/kill`) go to `TODO_AGENT_BRIDGE_CMD`
  (Cockpit's `cockpit-remote-fire`) with the channel id as `--chat-id`.
- `todo notify [--route R] [--button …] [--thread TS] text` — the transport-neutral
  sender. `TODO_NOTIFY_TRANSPORT=telegram|slack|both` picks the wire (default
  `telegram` until cutover). `todo telegram-send` is now an alias for
  `notify --route default`, so flipping the variable moves every unmigrated
  producer. `todo notify --check --route R` prints `ready` or problem codes.
- `todo slack-doctor` — read-only: tokens present, routes, user lock, `auth.test`,
  last recorded send/listen error.

## Routes

`~/.todo/slack-routes.json` (local, never committed):

```json
{
  "default": "C…alerts",
  "routes": { "capture": "C…", "agents": "C…", "digest": "C…", "career": "C…", "alerts": "C…" }
}
```

An unmapped route falls back to `default` and logs it.

## Setup

1. Create the app from `docs/slack-app-manifest.yaml`, install it, store both tokens
   (commands in the manifest header).
2. Create the channels, invite the bot, write `slack-routes.json`.
3. Put your member id in the plist's `SLACK_ALLOWED_USER_ID`, copy it to
   `~/Library/LaunchAgents/`, `launchctl bootstrap gui/$(id -u) <plist>`.
4. `todo slack-doctor`, then `todo notify --route alerts "hello"`.

## Failure behavior

Send failures log to `~/.todo/todo.log`, stamp `slack-state.json` for the doctor,
and exit 1 so producers keep their own queue/retry. One 429 retry honors
`Retry-After`. Redelivered events are deduped by `event_id`; captures never drop
on a failed download (the note records the error).
