# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`todo` is a local-first capture CLI (`todo_cli`). A single JSONL file at `~/.todo/todos.jsonl` is the local store; **Todoist is the canonical task layer** and the **Obsidian vault** (`~/Notes/obsidian`) is the canonical note/idea store. Task completion is **bidirectional and convergent**: finish a task anywhere — here, Todoist web/mobile, or (when enabled) Logseq — and the state converges everywhere without oscillating.

Three "surfaces" plus a mobile front door:
- **Local JSONL** (`storage.py` + `models.py`) — the in-process source image; every command does `load_all → mutate → write_all`.
- **Todoist** (`todoist.py`) — canonical tasks; outbound push (create + complete) and inbound mirror/reconcile.
- **Obsidian** (`obsidian.py`) — one Markdown file per note/idea capture; the canonical memory store.
- **Logseq** (`logseq.py`) — **frozen read-only archive since 2026-06-01**. Its journal-sync writers still exist but are **no-ops unless `TODO_LOGSEQ_SYNC=1`**.
- **Telegram** (`telegram.py`) — the live mobile front door: a long-poll daemon files each message into Obsidian (and pushes tasks to Todoist).

## Commands

```sh
uv tool install --editable .        # editable install; the `todo` shim lands in ~/.local/bin
```
Edits to `src/todo_cli/` apply immediately via the editable shim — no reinstall.

```sh
.venv/bin/python -m pytest          # run the whole suite (70 tests, ~0.1s). -q for quiet.
.venv/bin/python -m pytest tests/test_complete.py::test_cmd_done_propagates_both_ways   # single test
.venv/bin/python -m pytest tests/test_mirror.py                                          # single file
.venv/bin/python -m pytest -k closed_ts                                                  # by substring
```
`pyproject.toml` sets `pythonpath=["src"]` and `testpaths=["tests"]`, so plain `pytest` discovers and imports `todo_cli` with **no install step**. The venv is Python 3.11 at `.venv/bin/python`. There is **no linter/formatter configured** (no ruff/flake8/black config) — don't invent a lint command.

Parametrized cases use the bracketed id and must be quoted: `.venv/bin/python -m pytest 'tests/test_telegram_obsidian.py::test_classify_contract[+t buy milk-task-buy milk]'`.

## Architecture

### Module layout & dependency direction

`config.py` and `models.py` are leaves. Everything imports from them; they import nothing internal.

```
cli.py            argparse → binds each subcommand to a cmd_* via set_defaults(func=...); main() just calls args.func(args). No if/elif table — add a verb = add a subparser + a cmd_*.
  └ commands.py   the orchestration brain: one cmd_* per verb. The ONLY caller of the sync modules. Pattern: load_all → orchestrate inbound/outbound → write_all.
       ├ storage.py    JSONL load/write/append/find_by_prefix over ~/.todo/todos.jsonl (+ append-only todo.log).
       ├ todoist.py     Todoist API v1 leg (HTTP via stdlib urllib).
       ├ logseq.py      Logseq journal leg (pure filesystem; gated off).
       ├ obsidian.py    Obsidian capture writer (pure filesystem).
       ├ telegram.py    Telegram capture daemon (HTTP + ffmpeg/whisper subprocess).
       └ formatting.py  display helpers for `todo ls` ONLY (audit/doctor print inline).
  config.py  / models.py   (leaves: env/paths/constants ; pydantic schema)
```
The sync modules **mutate the shared `entries: list[TodoEntry]` in place and do NOT persist** — `commands.py` owns every `write_all`.

### The data model (`models.py`)

`TodoEntry` is the JSONL row. Every model is `ConfigDict(extra="allow")` so unknown/future fields survive a read-modify-write round-trip (older/newer CLI versions share one file safely). Only `text` is required.

Completion is recorded by three parallel signals — `status` (`Literal["open","done"]`), `done_ts`, `done_source` — plus a nested gate. Key fields that the whole sync logic reasons over:
- **`sync.todoist.closed_ts`** — *the no-echo gate* (see below).
- **`origin`** — `"todoist"` marks a row mirrored IN by `pull` (read-only; never pushed back out). None/other = locally originated.
- **`done_source`** — who completed it (`local`/`todoist`/`logseq`/agent label). Distinguishes who-finished-what for the gate.
- **`short_id`** = `id[-8:]` — the random hex tail (NOT the timestamp prefix), used for display and prefix lookup. `id` itself is `{ms-epoch:013d}{token_hex(4)}` — lexically sortable by creation time.
- `notion_inbox_id` and `sync.logseq` are **dormant legacy** (retired Notion drain / frozen Logseq) — kept only so old rows still parse. Don't build on them.

### Convergence model — the invariants that must not break

These are the load-bearing rules; the test suite pins them exactly.

1. **No-echo gate = `sync.todoist.closed_ts`.** A completion is pushed to Todoist *exactly once*. `push_completions`/`todoist.sync` only close a row where `status=="done"` AND it has a `task_id` AND `closed_ts` is unset. Any inbound path that flips a row done (`todoist.reconcile`, `mirror` sweep, a 404 on close) **stamps `closed_ts` at flip time**, so rows completed *by* a remote are never echoed back out. This is what makes the two directions converge without oscillating. `test_converged_state_is_a_fixed_point` even sets `fetch_task` to raise to prove a converged row is never re-fetched.

2. **Persist-before-network.** `cmd_done` calls `write_all()` to stamp `status=done` **before** any remote call, then `write_all()` again to record `closed_ts`. A down/stalled/offline remote can never cost the local "done" — completion errors swallow `OSError` (URLError/timeout/reset all subclass it), leave `closed_ts` unset for retry, and never re-raise (an escaping exception would abort the caller's `write_all`).

3. **Inbound-before-outbound ordering.** `_refresh_task_state` (backing `todo refresh`) runs `todoist.mirror → logseq.reconcile → todoist.reconcile → write_all → _sync_outbound → write_all` — two `write_all` boundaries bracketing the outbound push, so remote completions land before anything is pushed. `tests/test_refresh.py` asserts this exact sequence; don't reorder it.

4. **Origin gate.** `create_candidates` and `logseq.sync_candidates` exclude `origin=="todoist"` rows — the mirrored Todoist backlog is read-only and is never re-pushed or materialized into the journal. This is redundant defense on top of the `task_id`/`closed_ts` checks.

5. **Asymmetric reopen.** `mirror` reopens a *done* row only if `origin=="todoist"` and it reappears in Todoist's active set (handles web un-complete and recurring-task due-advance); it **never** reopens a `done_source=="local"` row. Don't collapse these.

6. **Logseq's deliberate asymmetry.** `logseq.reconcile` flips a row done from the journal but **does not** stamp `closed_ts` — so a Logseq completion still propagates *out* to Todoist on the next push (a 404 there counts as already-closed). Contrast `todoist.reconcile`/`mirror`, which DO stamp it.

### Config is import-time; the structure file is canonical

`config.py` resolves `TODOIST_PROJECT_ID`, `LOGSEQ_SYNC_ENABLED`, `TELEGRAM_ENABLED`, `WHISPER_MODEL`, etc. **once at import**. Changing an env var after import has no effect. The default capture project and the `pull` mirror scope come from the cockpit structure file:

- **`~/Developer/proj/cockpit/todoist-structure.json`** (override: `TODOIST_STRUCTURE`) is the single source of truth for Todoist IDs and mirror scope. `_structure()` swallows all errors and returns `{}`, degrading to defaults (`TODOIST_INBOX_FALLBACK="6CrgHvjH3RPXmHCg"`, `exclude_shared=True`). **Do not hard-code Todoist IDs anywhere in this repo** — read them through config.

Because config constants are imported *by value* into their consumers, **tests patch the consumer module, not config** (e.g. `monkeypatch.setattr(logseq, "LOGSEQ_SYNC_ENABLED", ...)`, `monkeypatch.setattr(todoist, "fetch_task", ...)`), and `conftest.py` patches `storage.TODOS_FILE` (not `config.TODOS_FILE`). Keep this pattern.

Inverted boolean conventions to watch: `TODO_LOGSEQ_SYNC` is **opt-in** (`== "1"`, default off); `TODO_TELEGRAM` is **opt-out** (`!= "0"`, default on).

### Telegram capture daemon (`telegram.py`)

`todo telegram-poll --loop` is the launchd `KeepAlive` daemon (`com.nathan.telegram-capture`). `getUpdates` long-poll with an **exactly-once `update_id` offset cursor** (`~/.todo/telegram-state.json`) advanced in a `finally` for *every* handled update (including dropped/unauthorized ones — no retry, no dead-letter). `classify()` is a **deliberately swappable seam** (prefix parser: `+t`/`+task`→task, `+i`/`+idea`→idea, else note; bare prefix falls back to note) whose contract is pinned by `tests/test_telegram_obsidian.py`. A single-user lock comes from `TELEGRAM_ALLOWED_CHAT_ID` (empty = open bot, and the reply tells you your `chat_id`). Voice notes are downloaded and transcribed locally via `ffmpeg` + `whisper.cpp`; unset `TODO_WHISPER_MODEL` → a placeholder body, text still captured. Only one poller may own a token (HTTP 409 otherwise).

### Capture file format (`obsidian.py`)

One file per capture: `<vault>/captures/YYYY-MM-DD/<HHMMSS>-<source>-<id8>.md`, six-field YAML frontmatter in fixed order `id, created, source, type, status, tags`. Note the YAML key is **`type`** though the Python param is `kind`; `status` is always written `open` (a downstream janitor flips it). Conflict-free on a Drive-synced vault comes purely from one-file-per-capture + random `id8` — there is no shared inbox file and no locking. (Logseq journals, when enabled, use a *different* convention: `journals/YYYY_MM_DD.md` with underscores and `<!-- todo:{id} -->` markers.)

## Sharp edges

- **`find_by_prefix` matches loosely**: full `id` OR `short_id` prefix OR *any substring of the full id* (a short numeric needle can collide across same-era timestamp prefixes). On >1 match it calls `sys.exit()` directly from the storage layer — callers can't catch it.
- **`load_all` silently drops** any line that fails JSON/pydantic parse; the next `write_all` then rewrites the file *without* it (permanent loss, no warning). A crash mid-`append` can leave such a partial line.
- **`append()` vs `write_all()` serialize differently**: `write_all` uses `exclude_none=True` (compact), `append` does not (emits nulls). Round-tripping a freshly-appended row changes its on-disk JSON. Only `write_all` is atomic (tmp-file + `os.replace`); there is no file locking anywhere (last writer wins).
- **`cmd_rm` is local-only** — it deletes the JSONL row but does NOT close/delete the Todoist task (orphans it). Only `cmd_done` propagates.
- **`test_session_hook_uses_refresh`** reaches outside the repo to `~/Developer/proj/cockpit/scripts/cockpit-todoist-session-hook` and `pytest.skip()`s if absent — so a standalone clone skips it rather than failing.

## External dependencies (outside this repo)

- **macOS login keychain**, service `todo-cli`: account `todoist` (Todoist token) and account `telegram` (bot token). Both env-overridable (`TODOIST_TOKEN`, `TELEGRAM_BOT_TOKEN`).
- **`~/Developer/proj/cockpit/todoist-structure.json`** — canonical Todoist IDs + mirror scope (see above).
- **Obsidian vault** `~/Notes/obsidian` (captures); **Logseq graph** `~/Notes/logseq` (frozen).
- **`ffmpeg` + `whisper.cpp`** for voice transcription; **launchd** agent `com.nathan.telegram-capture` for the daemon.
- `docs/telegram-capture.md` documents the live mobile lane. `docs/android-capture.md` is **superseded historical reference** (the old Notion→Logseq flow, retired 2026-06-01) — don't act on it.
