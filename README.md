# todo

Local-first todo capture CLI. Store in `~/.todo/todos.jsonl`. Push to Logseq journal + Todoist. Pull status back with `reconcile`.

## Install

```sh
uv tool install --editable .
```

Edits to `src/todo_cli/cli.py` apply immediately via the `todo` shim in `~/.local/bin/`.

## Commands

```
todo add "text" [--due YYYY-MM-DD] [--source ...] [--project ...]
todo ls   [--all|--open|--done]
todo done <id-prefix>
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

## Logseq

Appends `- TODO <text> <!-- todo:<id> --></text>` block to today's journal `<graph>/journals/YYYY_MM_DD.md`. `reconcile` flips local to done when block starts with `- DONE` / `- CANCELED` / `- [x]`.

## Todoist

Creates a task via Todoist API v1. Tasks land in the default capture project (Inbox, resolved from `~/Documents/cockpit/todoist-structure.json`, overridable with `TODO_TODOIST_PROJECT_ID`). `--source` and `--project` are attached as **labels** — not sections — and a missing project label is auto-created on first use. `reconcile` flips local to done when the remote task is completed or deleted (404).

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
    "todoist": null | {"task_id": "...", "url": "...", "ts": "...", "project_id": "..."}
  }
}
```

`origin: "todoist"` marks a row mirrored in by `pull`; such rows are never pushed back to Todoist.
