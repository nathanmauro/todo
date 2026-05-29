# Telegram quick-capture → Notion Capture Inbox → Logseq

A @BotFather bot is a second capture **producer** (alongside the Android HTTP
Shortcut). You message the bot — text or a held-to-record voice note — and the
existing 15-min `logseq-notion-sync` job turns each message into a Capture Inbox
row, then PARA-classifies and files it into the Logseq graph. The bot is **not**
a second writer to `~/Notes`; it only creates Notion rows.

Why Telegram (vs WhatsApp/Discord): `getUpdates` long-polling is a plain
outbound HTTPS call, so the Mac needs **no public endpoint, no tunnel, no second
daemon** — the poll folds into the job that already runs. Official Bot API, zero
ban risk. (WhatsApp's API is webhook-only + needs a business number; Discord
needs a persistent gateway daemon.)

## One-time setup

1. **Create the bot.** In Telegram, message **@BotFather** → `/newbot` → pick a
   name and a username. Copy the token it gives you (`123456:ABC-…`).
2. **Store the token** in the login keychain (same service the CLI uses):
   ```bash
   security add-generic-password -a telegram -s todo-cli -w '<BOT_TOKEN>'
   ```
   (Or export `TELEGRAM_BOT_TOKEN` for a one-off.)
3. **Open the chat once.** Find your bot in Telegram and press **Start** (or send
   "hi"). A bot can only message a chat the user has opened — this permanently
   satisfies that, enabling the "filed ✓" confirmations. Pin the chat to the top
   of your list so it's a dedicated capture surface.
4. **Voice (optional).** Transcription uses whisper.cpp locally:
   ```bash
   brew install whisper-cpp
   mkdir -p ~/.cache/whisper && curl -SL -o ~/.cache/whisper/ggml-base.en.bin \
     https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin
   ```
   The CLI auto-detects that model path. Override with `TODO_WHISPER_MODEL`, or
   set it to `""` to disable voice (text still works). `ffmpeg` is required
   (decodes the OGG/Opus voice note to 16 kHz WAV).

## How it runs

`todo notion-sync` (the launchd job, every 15 min) now:

1. **Telegram lane** — `getUpdates` from the stored offset; for each message,
   text is taken as-is, a voice note is downloaded (≤20 MB) and transcribed; one
   `create_row` into the Capture Inbox; replies "filed ✓"; advances the offset
   cursor (`~/.notion-sync/telegram-state.json`) — exactly-once.
2. **Drain** — pulls unsynced Capture Inbox rows (from Telegram *and* the Android
   shortcut), classifies notes, files them, marks `Synced=true`.

Nothing new is scheduled — it's all the one existing job. Test offline with
`todo notion-sync --dry-run` (shows placement; the Telegram poll is skipped in
dry-run so it never creates rows).

## Toggles (env)

- `TODO_TELEGRAM=0` — disable the Telegram lane entirely.
- `TODO_WHISPER_MODEL` — ggml model path (`""` disables voice).
- `TELEGRAM_BOT_TOKEN` — token override (else keychain `telegram`/`todo-cli`).
