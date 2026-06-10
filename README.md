# todo

Local-first capture CLI. Tasks live in `~/.todo/todos.jsonl` and push to **Todoist**; notes/captures land in the **Obsidian vault** (the canonical store) as one Markdown file each. Task completion is bidirectional — finish a task anywhere and it converges everywhere: `done` here closes it there; `pull`/`reconcile` bring remote completions back here.

> **Logseq is a frozen archive** (2026-06-01). The Logseq task-sync writers are kept but gated **off** behind `TODO_LOGSEQ_SYNC=1`; by default the CLI never writes to the Logseq graph. The mobile front door is the Telegram bot → Obsidian (`todo telegram-poll --loop`).

## Install

```sh
uv tool install --editable .
```

Edits to `src/todo_cli/cli.py` apply immediately via the `todo` shim in `~/.local/bin/`.

## Commands

```
todo add "text" [--due YYYY-MM-DD] [--source ...] [--project ...] [--no-sync]
todo ls   [--all|--open|--done]
todo done <id-prefix>          # closes it in Todoist (+ flips its Logseq line to DONE only if TODO_LOGSEQ_SYNC=1)
todo rm   <id-prefix>
todo edit
todo note "text"               # capture a note into the Obsidian vault (captures/YYYY-MM-DD/)
todo plan <idea> --project <project>
todo plan create --id <slug> --title "title" --project <project> --summary "one-line" [--plan-file plan.md]
todo plan execute <slug> --summary "what shipped"
todo plan status <slug>
todo backlog [project] [--offline] [--json] [--history]
todo sync       [--target all|logseq|todoist]
todo refresh    [--dry-run]
todo audit
todo reconcile  [--target all|logseq|todoist]
todo pull       [--dry-run]
todo telegram-poll [--loop]     # poll the capture bot; file each message into the vault
todo telegram-send "text"       # message the last chat that messaged the bot
todo doctor
```

## Config

Env overrides:

- `TODO_DIR` — store dir (default `~/.todo`)
- `TODO_OBSIDIAN_VAULT` — Obsidian vault root for captures (default `~/Notes/obsidian`)
- `TODO_LOGSEQ_SYNC` — set to `1` to re-enable the (frozen) Logseq task-sync writers; off by default
- `TODO_LOGSEQ_GRAPH` — Logseq graph root (default `~/Notes/logseq`); only used when `TODO_LOGSEQ_SYNC=1`
- `TODO_TODOIST_PROJECT_ID` — Todoist project to create tasks in (default: Inbox, resolved from `~/Developer/proj/cockpit/todoist-structure.json`)
- `TODOIST_TOKEN` — overrides Keychain lookup
- `TODO_TELEGRAM_STATE` / `TODO_TELEGRAM_CHAT` — Telegram offset cursor + last-chat file (default under `~/.todo/`)

Todoist token in Keychain:

```sh
security add-generic-password -a todoist -s todo-cli -w '<token>'
```

Get your token from https://app.todoist.com/app/settings/integrations/developer.

## Spotlight capture

Build an Apple Shortcut named `Todo`:

1. Action **Ask for Input** (text)
2. Action **Run Shell Script** (zsh, pass input as arguments): `todo add "$1"`
3. Optional: keyboard shortcut, e.g. `⌃⌥⌘T`

Use: `⌘Space` → `todo` → `↵` → type text → `↵`.

## Completion sync ("done here → done there")

`status` is the single source of truth for done-ness, and completion converges across all three surfaces:

- **Inbound** (remote → local): `reconcile` and `pull` flip a local row to `done` when its Todoist task is completed/deleted or its Logseq block is marked done.
- **Outbound** (local → remote): `done` immediately closes the Todoist task (`POST /tasks/{id}/close`) and rewrites the Logseq block to `- DONE`, best-effort. If a remote is unreachable (offline, no token) the local completion still succeeds; the next `todo sync` flushes whatever didn't land.

A `sync.todoist.closed_ts` stamp gates the outbound push so a completion is pushed exactly once and rows flipped done *by* a remote (via `reconcile`/`pull`) are never echoed back out. The two directions converge to the same state and never oscillate.

## Obsidian capture

`todo note "..."` (and every Telegram capture) writes one Markdown file under `<vault>/captures/YYYY-MM-DD/<HHMMSS>-<source>-<id8>.md` with frontmatter (`id, created, source, type, status, tags`). Telegram file/media payloads are saved best-effort under `<vault>/Attachments/telegram/YYYY-MM-DD/`; if a download fails, the capture still records the metadata and error. One file per capture keeps a Google-Drive-synced vault conflict-free. The Obsidian vault is the canonical note/idea store.

## Plan / Backlog

`todo backlog <project>` is the single project work view. It reads Obsidian plus
Todoist and groups work as In flight, Planned, and Backlog / Ideas. The command
is read-only; `--json` emits stable groups for agent hooks, and `--history`
shows executed plan records that are hidden by default.

`todo plan <idea> --project <project>` graduates an idea note in
`05 Notes/ideas/` by stamping `project:` and `status: shaped`. `todo plan
create` writes standalone execution plans into `06 Backlog/` with `type: plan`
and `status: shaped`; `todo plan execute` marks them `done` with execution
metadata. Cockpit's `scripts/cockpit-plan` delegates here.

## Logseq (frozen archive)

Logseq became a read-only archive on 2026-06-01. The task-sync writers still exist — appending `- TODO <text> <!-- todo:<id> -->` to today's journal and flipping it to `- DONE`/`- [x]` on completion — but they are **no-ops unless `TODO_LOGSEQ_SYNC=1`**. Re-enable only for a one-off backfill; the CLI does not touch the graph in normal operation.

## Todoist

Creates a task via Todoist API v1. Tasks land in the default capture project (Inbox, resolved from `~/Developer/proj/cockpit/todoist-structure.json`, overridable with `TODO_TODOIST_PROJECT_ID`). `--source` and `--project` are attached as **labels** — not sections — and a missing project label is auto-created on first use. `reconcile` flips local to done when the remote task is completed or deleted (404); completing a task locally closes it remotely (a 404 counts as already-closed). `todo sync` both creates new open tasks and flushes pending completions.

## Mirror (`todo pull`)

`pull` makes Todoist the source of truth and the local store a read-only mirror. It lists in-scope Todoist tasks and upserts them into `todos.jsonl` keyed on `sync.todoist.task_id`: tasks created here (CLI/agents) update in place, and tasks created elsewhere (phone, web, MCP) are imported as `origin: "todoist"` rows. Imported rows are never pushed back (echo-loop guard), and a mirrored task that disappears from Todoist's active set is flipped to done.

Imported rows carry Todoist's real creation time (`added_at`) as `ts`, so `ls`
age and ordering reflect when the task was typed, not when the pull ran. On
every pull, mirrored rows also re-derive `project`/`source` from their Todoist
labels, so label edits made on web/phone propagate. In `ls`, Todoist-owned rows
show a `[mirror]` badge (vs `[todoist]` for locally-created rows pushed out)
and due dates render as `[due …]`.

Scope is read from the `mirror` block of `~/Developer/proj/cockpit/todoist-structure.json` (default: every personal project, drop shared/workspace projects like Team Inbox, active tasks only). `--dry-run` reports what would change without writing.

## Refresh / Audit

`refresh` is the convergence command: it pulls the Todoist mirror,
reconciles remote completion status, writes inbound state, then pushes eligible
local-origin task completions out to Todoist (and, only when `TODO_LOGSEQ_SYNC=1`,
to the Logseq journal). Mirrored Todoist backlog rows are deliberately skipped by
Logseq sync so the journal only gets curated local/agent task references. The
per-task reconcile fetch is narrowed during a refresh to the rows the mirror's
absence sweep could not judge: local-origin rows plus any mirrored row whose
project left mirror scope (everything sweep-covered is skipped).

The launchd agent `com.nathan.todo-refresh` (`launchd/com.nathan.todo-refresh.plist`)
runs `todo refresh` every 10 minutes (plus once at login), so tasks typed into
Todoist anywhere appear locally without manual pulls. Install:

```sh
cp launchd/com.nathan.todo-refresh.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.nathan.todo-refresh.plist
```

Unattended safety: every load→write critical section takes an `flock` on
`~/.todo/todos.lock` (so the interval refresh and the Telegram daemon can't
clobber each other; on a 120s timeout the verb fails loudly rather than ever
writing unlocked), and `load_all` quarantines unparseable JSONL lines to
`~/.todo/todos.rejects.jsonl` instead of silently dropping them.

`audit` summarizes the local store counts and the expected gap between the
Todoist backlog mirror and curated Logseq task refs.

## Storage

`~/.todo/todos.jsonl` — one JSON object per line, append-only logical model (file rewritten on edits). Per-entry shape:

```json
{
  "id": "<13-digit ts><8 hex>",
  "ts": "ISO-8601",
  "text": "...",
  "status": "open|done",
  "source": "cli|claude|codex|todoist|...",
  "project": "bin|todo|...",
  "origin": null | "todoist",
  "mirrored_at": null | "ISO-8601",
  "notion_inbox_id": null,   // dormant: only present on legacy rows from the retired Notion drain (2026-06-01)
  "sync": {
    "logseq": null | {"file": "...", "marker": "...", "ts": "..."},
    "todoist": null | {"task_id": "...", "url": "...", "ts": "...", "project_id": "...", "closed_ts": null | "ISO-8601"}
  }
}
```

`origin: "todoist"` marks a row mirrored in by `pull`; such rows are never pushed back to Todoist.
