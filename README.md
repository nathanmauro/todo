# todo

Local-first todo capture CLI. Store in `~/.todo/todos.jsonl`. Push to Logseq journal + Notion DB. Pull status back with `reconcile`.

## Install

```sh
uv tool install --editable .
```

Edits to `src/todo_cli/cli.py` apply immediately via the `todo` shim in `~/.local/bin/`.

## Commands

```
todo add "text" [--due YYYY-MM-DD] [--source ...]
todo ls   [--all|--open|--done]
todo done <id-prefix>
todo rm   <id-prefix>
todo edit
todo sync       [--target all|logseq|notion]
todo reconcile  [--target all|logseq|notion]
todo doctor
```

## Config

Env overrides:

- `TODO_DIR` — store dir (default `~/.todo`)
- `TODO_LOGSEQ_GRAPH` — Logseq graph root (default `~/Notes`)
- `TODO_NOTION_DB_ID` — Notion "Todo List" database id
- `NOTION_TOKEN` — overrides Keychain lookup

Notion token in Keychain:

```sh
security add-generic-password -a notion -s todo-cli -w '<token>'
```

## Spotlight capture

Build an Apple Shortcut named `Todo`:

1. Action **Ask for Input** (text)
2. Action **Run Shell Script** (zsh, pass input as arguments): `todo add "$1"`
3. Optional: keyboard shortcut, e.g. `⌃⌥⌘T`

Use: `⌘Space` → `todo` → `↵` → type text → `↵`.

## Logseq

Appends `- TODO <text> <!-- todo:<id> --></text>` block to today's journal `<graph>/journals/YYYY_MM_DD.md`. `reconcile` flips local to done when block starts with `- DONE` / `- CANCELED` / `- [x]`.

## Notion

Creates a row in the configured DB with `Task name` (title) + `Status` = `Not started`. `reconcile` flips local to done when remote `Status` is `Done`. Skips archived/trashed pages.

## Storage

`~/.todo/todos.jsonl` — one JSON object per line, append-only logical model (file rewritten on edits). Per-entry shape:

```json
{
  "id": "<13-digit ts><8 hex>",
  "ts": "ISO-8601",
  "text": "...",
  "status": "open|done",
  "source": "cli|spotlight|...",
  "sync": {
    "logseq": null | {"file": "...", "marker": "...", "ts": "..."},
    "notion": null | {"page_id": "...", "url": "...", "ts": "..."}
  }
}
```
