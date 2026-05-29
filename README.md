# todo

Local-first todo capture CLI. Store in `~/.todo/todos.jsonl`. Push to Logseq journal + Todoist. Completion is bidirectional — finish a task anywhere and it converges everywhere: `done` here closes it there; `pull`/`reconcile` bring remote completions back here.

## Install

```sh
uv tool install --editable .
```

Edits to `src/todo_cli/cli.py` apply immediately via the `todo` shim in `~/.local/bin/`.

## Commands

```
todo add "text" [--due YYYY-MM-DD] [--source ...] [--project ...]
todo ls   [--all|--open|--done]
todo done <id-prefix>          # closes it in Todoist + flips its Logseq line to DONE
todo rm   <id-prefix>
todo edit
todo sync       [--target all|logseq|todoist]
todo reconcile  [--target all|logseq|todoist]
todo pull       [--dry-run]
todo doctor
```

## Config

Env overrides:

- `TODO_DIR` — store dir (default `~/.todo`)
- `TODO_LOGSEQ_GRAPH` — Logseq graph root (default `~/Notes`)
- `TODO_TODOIST_PROJECT_ID` — Todoist project to create tasks in (default: Inbox, resolved from `~/Documents/cockpit/todoist-structure.json`)
- `TODOIST_TOKEN` — overrides Keychain lookup

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

## Logseq

Appends `- TODO <text> <!-- todo:<id> --></text>` block to today's journal `<graph>/journals/YYYY_MM_DD.md`. `reconcile` flips local to done when the block starts with `- DONE` / `- CANCELED` / `- [x]`; conversely, completing a task locally rewrites its `- TODO` / `- DOING` / `- [ ]` block to `- DONE` / `- [x]` (idempotent, matched by marker).

## Todoist

Creates a task via Todoist API v1. Tasks land in the default capture project (Inbox, resolved from `~/Documents/cockpit/todoist-structure.json`, overridable with `TODO_TODOIST_PROJECT_ID`). `--source` and `--project` are attached as **labels** — not sections — and a missing project label is auto-created on first use. `reconcile` flips local to done when the remote task is completed or deleted (404); completing a task locally closes it remotely (a 404 counts as already-closed). `todo sync` both creates new open tasks and flushes pending completions.

## Mirror (`todo pull`)

`pull` makes Todoist the source of truth and the local store a read-only mirror. It lists in-scope Todoist tasks and upserts them into `todos.jsonl` keyed on `sync.todoist.task_id`: tasks created here (CLI/agents) update in place, and tasks created elsewhere (phone, web, MCP) are imported as `origin: "todoist"` rows. Imported rows are never pushed back (echo-loop guard), and a mirrored task that disappears from Todoist's active set is flipped to done.

Scope is read from the `mirror` block of `~/Documents/cockpit/todoist-structure.json` (default: every personal project, drop shared/workspace projects like Team Inbox, active tasks only). `--dry-run` reports what would change without writing.

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
  "sync": {
    "logseq": null | {"file": "...", "marker": "...", "ts": "..."},
    "todoist": null | {"task_id": "...", "url": "...", "ts": "...", "project_id": "...", "closed_ts": null | "ISO-8601"}
  }
}
```

`origin: "todoist"` marks a row mirrored in by `pull`; such rows are never pushed back to Todoist.
