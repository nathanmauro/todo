# todo agent guide

This file guides Claude Code and Codex in this repository; CLAUDE.md is a symlink to it.

## What this is

`todo` is a local-first capture CLI (`todo_cli`). A single JSONL file at `~/.todo/todos.jsonl` is the local store; **Linear is the canonical task layer since 2026-09-17** (`linear.py`; Todoist and Google Tasks are frozen read-only sources and their legs below are legacy, selectable only by `TODO_TASK_BACKEND=todoist|gtasks`) and the **Obsidian vault** (`~/Notes/obsidian`) is the canonical note/idea store. Task completion is **bidirectional and convergent**: finish a task anywhere — here, Todoist web/mobile, or (when enabled) Logseq — and the state converges everywhere without oscillating.

Three "surfaces" plus a mobile front door:

- **Local JSONL** (`storage.py` + `models.py`) — the in-process source image; every command does `load_all → mutate → write_all`.
- **Linear** (`linear.py`) — canonical tasks: outbound create (idempotent: deterministic `uuid5(row id)` issue id + `capture-id:` footer, lookup-then-create, adopt on race) and complete; fail-closed without the keychain key; no inbound mirror (the local file is a delivery queue + frozen Todoist snapshot). Project aliases in `linear_projects.json`; unknown explicit projects raise `RoutingError` and stay queued.
- **Todoist** (`todoist.py`) — legacy (retired 2026-09-17): outbound push and inbound mirror/reconcile, only under `TODO_TASK_BACKEND=todoist`.
- **Obsidian** (`obsidian.py`) — one Markdown file per note/idea capture; the canonical memory store.
- **Logseq** (`logseq.py`) — **frozen read-only archive since 2026-06-01**. Its journal-sync writers still exist but are **no-ops unless `TODO_LOGSEQ_SYNC=1`**.
- **Slack** (`slack.py`) — the live mobile front door and the notification wire: a Socket Mode listener files every human message the bot can see into Obsidian (and pushes `+t` tasks to Linear, holding the store lock across the push), and `todo notify` posts to a routed channel. Notification buttons run through the action registry (`actions.py`): `linear-complete` closes issues; `todoist-complete`/`gtasks-complete` are refused under the Linear backend. Telegram was the previous front door; it is retired and no code path speaks to it.

## Commands

```sh
uv tool install --editable .        # editable install; the `todo` shim lands in ~/.local/bin
```

Edits to `src/todo_cli/` apply immediately via the editable shim — no reinstall.

```sh
.venv/bin/python -m pytest          # run the whole suite (~240 tests, ~0.6s). -q for quiet.
.venv/bin/python -m pytest tests/test_complete.py::test_cmd_done_propagates_both_ways   # single test
.venv/bin/python -m pytest tests/test_mirror.py                                          # single file
.venv/bin/python -m pytest -k closed_ts                                                  # by substring
```

`pyproject.toml` sets `pythonpath=["src"]` and `testpaths=["tests"]`, so plain `pytest` discovers and imports `todo_cli` with **no install step**. The venv is Python 3.11 at `.venv/bin/python`. There is **no linter/formatter configured** (no ruff/flake8/black config) — don't invent a lint command.

Parametrized cases use the bracketed id and must be quoted: `.venv/bin/python -m pytest 'tests/test_capture_core.py::test_classify_contract[+t buy milk-task-buy milk]'`.

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
       ├ slack.py       Slack wire only: Socket Mode listener, chat.postMessage sender, doctor.
       ├ capture.py     transport-neutral capture core: classify(), push_task(), agent_prefixes().
       ├ actions.py     action registry (register/load/mark) + execute() for notification buttons.
       ├ transcribe.py  voice transcription (ffmpeg + Parakeet subprocess; whisper.cpp fallback).
       └ formatting.py  display helpers for `todo ls` ONLY (audit/doctor print inline).
  config.py  / models.py   (leaves: env/paths/constants ; pydantic schema)
```

The sync modules **mutate the shared `entries: list[TodoEntry]` in place and do NOT persist** — `commands.py` owns every `write_all`.

### The data model (`models.py`)

`TodoEntry` is the JSONL row. Every model is `ConfigDict(extra="allow")` so unknown/future fields survive a read-modify-write round-trip (older/newer CLI versions share one file safely). Only `text` is required.

Completion is recorded by three parallel signals — `status` (`Literal["open","done"]`), `done_ts`, `done_source` — plus a nested gate. Key fields that the whole sync logic reasons over:

- **`sync.todoist.closed_ts`** — _the no-echo gate_ (see below).
- **`origin`** — `"todoist"` marks a row mirrored IN by `pull` (read-only; never pushed back out). None/other = locally originated.
- **`done_source`** — who completed it (`local`/`todoist`/`logseq`/agent label). Distinguishes who-finished-what for the gate.
- **`short_id`** = `id[-8:]` — the random hex tail (NOT the timestamp prefix), used for display and prefix lookup. `id` itself is `{ms-epoch:013d}{token_hex(4)}` — lexically sortable by creation time.
- `notion_inbox_id` and `sync.logseq` are **dormant legacy** (retired Notion drain / frozen Logseq) — kept only so old rows still parse. Don't build on them.

### Convergence model — the invariants that must not break

These are the load-bearing rules; the test suite pins them exactly.

1. **No-echo gate = `sync.todoist.closed_ts`.** A completion is pushed to Todoist _exactly once_. `push_completions`/`todoist.sync` only close a row where `status=="done"` AND it has a `task_id` AND `closed_ts` is unset. Any inbound path that flips a row done (`todoist.reconcile`, `mirror` sweep, a 404 on close) **stamps `closed_ts` at flip time**, so rows completed _by_ a remote are never echoed back out. This is what makes the two directions converge without oscillating. `test_converged_state_is_a_fixed_point` even sets `fetch_task` to raise to prove a converged row is never re-fetched.

2. **Persist-before-network.** `cmd_done` calls `write_all()` to stamp `status=done` **before** any remote call, then `write_all()` again to record `closed_ts`. A down/stalled/offline remote can never cost the local "done" — completion errors swallow `OSError` (URLError/timeout/reset all subclass it), leave `closed_ts` unset for retry, and never re-raise (an escaping exception would abort the caller's `write_all`).

3. **Inbound-before-outbound ordering.** `_refresh_task_state` (backing `todo refresh`) runs `todoist.mirror(covered=…) → logseq.reconcile → todoist.reconcile(skip_project_ids=covered) → write_all → _sync_outbound → write_all` — two `write_all` boundaries bracketing the outbound push, so remote completions land before anything is pushed. `tests/test_refresh.py` asserts this exact sequence; don't reorder it. `covered` is the set of project ids mirror's absence sweep actually judged: reconcile skips the per-task fetch ONLY for mirrored rows in those projects. Mirrored rows whose project left mirror scope (archived/shared/excluded — the sweep guard skips them) and all local-origin rows still get fetched, and a failed mirror leaves `covered` empty (full scan). Don't widen this skip back to "all `origin=='todoist'` rows" — that silently orphans out-of-scope mirrored completions forever (`test_reconcile_flips_out_of_scope_mirrored_completion` pins it).

4. **Origin gate.** `create_candidates` and `logseq.sync_candidates` exclude `origin=="todoist"` rows — the mirrored Todoist backlog is read-only and is never re-pushed or materialized into the journal. This is redundant defense on top of the `task_id`/`closed_ts` checks.

5. **Asymmetric reopen.** `mirror` reopens a _done_ row only if `origin=="todoist"` and it reappears in Todoist's active set (handles web un-complete and recurring-task due-advance); it **never** reopens a `done_source=="local"` row. Don't collapse these.

6. **Logseq's deliberate asymmetry.** `logseq.reconcile` flips a row done from the journal but **does not** stamp `closed_ts` — so a Logseq completion still propagates _out_ to Todoist on the next push (a 404 there counts as already-closed). Contrast `todoist.reconcile`/`mirror`, which DO stamp it.

### Config is import-time; the structure file is canonical

`config.py` resolves `TODOIST_PROJECT_ID`, `LOGSEQ_SYNC_ENABLED`, `SLACK_ENABLED`, `ACTIONS_DIR`, `WHISPER_MODEL`, etc. **once at import**. Changing an env var after import has no effect. The default capture project and the `pull` mirror scope come from the cockpit structure file:

- **`~/Developer/proj/cockpit/todoist-structure.json`** (override: `TODOIST_STRUCTURE`) is the single source of truth for Todoist IDs and mirror scope. `_structure()` swallows all errors and returns `{}`, degrading to defaults (`TODOIST_INBOX_FALLBACK="6CrgHvjH3RPXmHCg"`, `exclude_shared=True`). **Do not hard-code Todoist IDs anywhere in this repo** — read them through config.

Because config constants are imported _by value_ into their consumers, **tests patch the consumer module, not config** (e.g. `monkeypatch.setattr(logseq, "LOGSEQ_SYNC_ENABLED", ...)`, `monkeypatch.setattr(todoist, "fetch_task", ...)`), and `conftest.py` patches `storage.TODOS_FILE` (not `config.TODOS_FILE`). Keep this pattern.

Inverted boolean conventions to watch: `TODO_LOGSEQ_SYNC` is **opt-in** (`== "1"`, default off); `TODO_SLACK` is **opt-out** (`!= "0"`, default on).

### Slack lane (`slack.py`) and the transport-neutral core (`capture.py`, `actions.py`)

`todo slack-listen` is the launchd `KeepAlive` daemon (`com.nathan.slack-capture`): one outbound Socket Mode websocket, no public endpoint. Each envelope is **acked first** (Slack redelivers after 3s) and then handled; redelivered events are deduped by `event_id` in `~/.todo/slack-state.json`. Every human message the bot can see becomes one capture (bot posts and edits never do, so the bot's own "filed" reply cannot loop). A single-user lock comes from `SLACK_ALLOWED_USER_ID` (empty = open mode: captures still file, agent commands and `agent-*` buttons are refused). Voice clips are transcribed locally via `transcribe.py`. Slash commands `/cc`, `/cc-sessions`, `/cc-kill` map onto the bridge grammar (`/claude`, `/sessions`, `/kill`) and call `TODO_AGENT_BRIDGE_CMD` with `--chat-id <channel> --text <command>`; that command line is a frozen contract with Cockpit's `cockpit-remote-fire`.

`slack.py` owns only the wire. What a second transport would reuse lives beside it:

- **`capture.classify()`** is a **deliberately swappable seam** (prefix parser: `+t`/`+task`→task, `+i`/`+idea`→idea, else note; bare prefix falls back to note) whose contract is pinned by `tests/test_capture_core.py`.
- **`capture.push_task(text, source)`** creates one task in the active backend, local row first. `source` has no default on purpose: the caller names its transport, and that name lands on the row.
- **`actions`** is the registry behind notification buttons. A button carries only a 12-hex id; the action (closed verb set + payload) is one JSON file in `~/.todo/actions/` (`TODO_ACTIONS`), written by `register()` at send time and run exactly once by `execute()` on click. Job Scout reads these files, so the record shape is a contract: add keys, never rename them. `execute(..., agent_allowed=...)` defaults to refusing `agent-*` verbs; the transport passes its own user lock.

`todo notify [--route R] [--button Label=verb[:payload]] [--thread TS] [--check] text` is the only send verb, and producers in other repos shell out to it: its flags, stdout (`slack: sent to route …`, `ready`, the `slack-…` problem codes) and exit codes are an external interface.

**Historical values stay readable.** Captures and todo rows written by the retired Telegram lane carry `source: telegram` / `done_source: telegram` and filenames like `<HHMMSS>-telegram-<id8>.md`. They are opaque strings to every reader here; never rewrite or special-case them.

### Capture file format (`obsidian.py`)

One file per capture: `<vault>/captures/YYYY-MM-DD/<HHMMSS>-<source>-<id8>.md`, six-field YAML frontmatter in fixed order `id, created, source, type, status, tags`. Note the YAML key is **`type`** though the Python param is `kind`; `status` is always written `open` (a downstream janitor flips it). Conflict-free on a Drive-synced vault comes purely from one-file-per-capture + random `id8` — there is no shared inbox file and no locking. (Logseq journals, when enabled, use a _different_ convention: `journals/YYYY_MM_DD.md` with underscores and `<!-- todo:{id} -->` markers.)

## Sharp edges

- **`find_by_prefix` matches loosely**: full `id` OR `short_id` prefix OR _any substring of the full id_ (a short numeric needle can collide across same-era timestamp prefixes). On >1 match it calls `sys.exit()` directly from the storage layer — callers can't catch it.
- **`load_all` quarantines** any line that fails JSON/pydantic parse into `~/.todo/todos.rejects.jsonl` (deduped, warning on stderr) — the next `write_all` still rewrites the file _without_ it, but the raw line survives for manual recovery. A crash mid-`append` can leave such a partial line.
- **`append()` vs `write_all()` serialize differently**: `write_all` uses `exclude_none=True` (compact), `append` does not (emits nulls). Round-tripping a freshly-appended row changes its on-disk JSON. Only `write_all` is atomic (tmp-file + `os.replace`).
- **Cross-process locking is `storage.file_lock()`** — an flock on `~/.todo/todos.lock` (a sidecar, because `write_all` replaces the data file). Every mutating verb in `commands.py` and `capture.push_task` wraps its load→write critical section in it; `cmd_refresh` holds it across the whole network window, which is what makes the interval agent and the Slack listener safe together. On timeout (120s) it **raises `LockTimeout`** — never proceeds unlocked, because an unlocked rewrite could silently destroy a concurrent local-origin append that would never re-converge from Todoist. `cli.main` turns it into a friendly nonzero exit; `capture.push_task`'s broad except logs it (under the Linear backend the local row is already queued for `todo sync`; on the legacy Todoist lane the task is already in Todoist + the vault, so the next mirror re-imports it, and `push_task` adopts an already-mirrored row instead of duplicating). Read-only verbs (`ls`, `audit`, dry-runs) don't take it.
- **`cmd_rm` is local-only** — it deletes the JSONL row but does NOT close/delete the Todoist task (orphans it). Only `cmd_done` propagates.

## External dependencies (outside this repo)

- **macOS login keychain**, service `todo-cli`: account `linear` (Linear API key), account `todoist` (legacy Todoist token), and accounts `slack-bot` (xoxb-) and `slack-app` (xapp-). All env-overridable (`TODO_LINEAR_API_KEY`, `TODOIST_TOKEN`, `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`).
- **`~/Developer/proj/cockpit/todoist-structure.json`** — canonical Todoist IDs + mirror scope (see above).
- **Obsidian vault** `~/Notes/obsidian` (captures); **Logseq graph** `~/Notes/logseq` (frozen).
- **`ffmpeg` + `parakeet-mlx`** (preferred) / **`whisper.cpp`** (fallback) for voice transcription, see `transcribe.py`; **launchd** agent `com.nathan.slack-capture` (`launchd/com.nathan.slack-capture.plist`) for the Slack listener.
- **launchd** agent `com.nathan.todo-refresh` (`launchd/com.nathan.todo-refresh.plist` in this repo, installed to `~/Library/LaunchAgents/`) runs `todo refresh` every 10 min + at login — the standing Todoist⇄local convergence loop. Mirrored rows import with Todoist's `added_at` as `ts`, re-derive `project`/`source` from labels on every pull, and render in `ls` with a `[mirror]` badge and `[due …]`.
- `docs/slack-capture.md` documents the live mobile lane and `todo notify`; channel ids live in `~/.todo/slack-routes.json`, never in code. `docs/android-capture.md` is **superseded historical reference** (the old Notion→Logseq flow, retired 2026-06-01) — don't act on it.
