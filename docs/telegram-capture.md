# Telegram quick-capture → Obsidian vault

A @BotFather bot is the **mobile front door** for capture (2026-06-01 cutover).
You message the bot — text or a held-to-record voice note — and the
`com.nathan.telegram-capture` launchd daemon (`todo telegram-poll --loop`) files
each message as **one Markdown file in the Obsidian vault** under
`captures/YYYY-MM-DD/<HHMMSS>-telegram-<id8>.md`. The Obsidian vault is the
canonical store; there is no Notion or Logseq writer in this path anymore (Notion
is read-only reference, Logseq is a frozen archive).

Prefixes route the capture:

- `+t ` / `+task ` → **task** (written as a `- [ ]` checkbox **and** pushed to Todoist)
- `+i ` / `+idea ` → **idea**
- anything else → **note**

The prefix (and the space after it) is stripped from the body; a bare `+t` with
no body falls back to a plain note so an empty task is never created. The bot
replies `filed ✓ <kind>` to close the loop, and (until you lock it) tells you
your `chat_id`.

Why Telegram (vs WhatsApp/Discord): `getUpdates` long-polling is a plain
outbound HTTPS call, so the Mac needs **no public endpoint, no tunnel** — works
behind NAT. Official Bot API, zero ban risk.

## One-time setup

1. **Create the bot.** In Telegram, message **@BotFather** → `/newbot` → pick a
   name and a username. Copy the token it gives you (`123456:ABC-…`).
2. **Store the token** in the login keychain (same service the CLI uses):
   ```bash
   security add-generic-password -a telegram -s todo-cli -w '<BOT_TOKEN>'
   ```
   The daemon idles until the token exists, then activates within ~60s with no
   reload. (Or export `TELEGRAM_BOT_TOKEN` for a one-off.)
3. **Open the chat once.** Find your bot in Telegram and press **Start** (or send
   "hi"). A bot can only message a chat the user has opened — this enables the
   "filed ✓" confirmations and records your `chat_id` (so `todo telegram-send`
   can message you back). Pin the chat to the top of your list.
4. **Lock the bot to you (recommended).** Read the `chat_id` from the bot's first
   reply, set `TELEGRAM_ALLOWED_CHAT_ID=<id>` in
   `~/Library/LaunchAgents/com.nathan.telegram-capture.plist`, then
   `launchctl kickstart -k gui/$(id -u)/com.nathan.telegram-capture`. A non-empty
   allow-list silently drops messages from any other chat.
5. **Voice (optional).** Transcription uses whisper.cpp locally:
   ```bash
   brew install whisper-cpp
   mkdir -p ~/.cache/whisper && curl -SL -o ~/.cache/whisper/ggml-base.en.bin \
     https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
   ```
   The CLI auto-detects that model path. Override with `TODO_WHISPER_MODEL`, or
   set it to `""` to disable voice (text still works). `ffmpeg` is required.

## How it runs

`todo telegram-poll --loop` is the daemon (launchd `KeepAlive`):

1. `getUpdates` long-poll from the stored offset cursor
   (`~/.todo/telegram-state.json`) — exactly-once.
2. For each authorized message: extract text (voice notes are downloaded ≤20 MB
   and transcribed), classify by prefix, write one capture file; tasks also push
   a single Todoist task. Persist the sender `chat_id`, reply `filed ✓`, and
   advance the offset cursor past the handled update.

Test one pass without the loop: `todo telegram-poll` (also the easiest way to
grab your `chat_id` from the reply). Send a message back to yourself with
`todo telegram-send "…"`.

## The classifier seam

Routing is the deterministic prefix parser in `telegram.classify()` today. It is
a **swappable seam**: a future LLM / Black-Box auto-classifier can replace that
function body wholesale, and `tests/test_telegram_obsidian.py` pins the contract
it must keep. (See the vault's `06 Backlog/llm-classifier-for-telegram-captures`.)

## Toggles (env)

- `TODO_TELEGRAM=0` — disable the Telegram lane entirely.
- `TODO_OBSIDIAN_VAULT` — vault root for captures (default `~/Notes/obsidian`).
- `TODO_WHISPER_MODEL` — ggml model path (`""` disables voice).
- `TELEGRAM_BOT_TOKEN` — token override (else keychain `telegram`/`todo-cli`).
- `TELEGRAM_ALLOWED_CHAT_ID` — comma-separated chat-id allow-list (single-user lock).
