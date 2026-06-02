"""Subcommand handlers — one per CLI verb."""
from __future__ import annotations

import argparse
import contextlib
import io
import os
import subprocess
import sys

from . import logseq, obsidian, telegram, todoist
from .config import (
    LOGSEQ_GRAPH,
    LOGSEQ_SYNC_ENABLED,
    TELEGRAM_ENABLED,
    TODOIST_PROJECT_ID,
    TODO_DIR,
    TODOS_FILE,
    mirror_policy,
)
from .formatting import human_ago, sync_badges
from .models import TodoEntry, now_iso
from .storage import (
    append,
    ensure_store,
    find_by_prefix,
    load_all,
    log,
    write_all,
)


def _run_quiet(func, *args, quiet: bool = False, **kwargs):
    if not quiet:
        return func(*args, **kwargs)
    with contextlib.redirect_stdout(io.StringIO()):
        return func(*args, **kwargs)


def _sync_outbound(entries: list[TodoEntry], *, quiet: bool = False) -> int:
    """Push eligible local-origin task state to Logseq and Todoist."""
    rc = 0
    rc |= _run_quiet(logseq.sync, entries, quiet=quiet)
    rc |= _run_quiet(todoist.sync, entries, quiet=quiet)
    return rc


def _refresh_task_state(
    entries: list[TodoEntry], *, dry_run: bool = False, quiet: bool = False
) -> int:
    """Converge Todoist, local JSONL, and curated Logseq task blocks."""
    if dry_run:
        scratch = [e.model_copy(deep=True) for e in entries]
        rc = 0
        rc |= todoist.mirror(scratch, dry_run=True)
        rc |= logseq.reconcile(scratch)
        rc |= todoist.reconcile(scratch)
        print(
            "refresh dry-run: would sync "
            f"{len(logseq.sync_candidates(scratch))} task(s) to Logseq, "
            f"create {len(todoist.create_candidates(scratch))} Todoist task(s), "
            f"close {len(todoist.completion_candidates(scratch))} Todoist task(s)"
        )
        return rc

    rc = 0
    rc |= _run_quiet(todoist.mirror, entries, quiet=quiet)
    rc |= _run_quiet(logseq.reconcile, entries, quiet=quiet)
    rc |= _run_quiet(todoist.reconcile, entries, quiet=quiet)
    write_all(entries)
    rc |= _sync_outbound(entries, quiet=quiet)
    write_all(entries)
    return rc


def _audit_counts(entries: list[TodoEntry]) -> dict[str, int]:
    open_rows = [e for e in entries if e.status == "open"]
    done_rows = [e for e in entries if e.status == "done"]
    local_open = [e for e in open_rows if e.origin != "todoist"]
    mirrored_open = [e for e in open_rows if e.origin == "todoist"]
    return {
        "total": len(entries),
        "open": len(open_rows),
        "done": len(done_rows),
        "origin_todoist": len([e for e in entries if e.origin == "todoist"]),
        "open_local_missing_todoist": len(
            [e for e in local_open if e.sync.todoist is None]
        ),
        "open_local_missing_logseq": len(
            [e for e in local_open if e.sync.logseq is None]
        ),
        "open_mirrored_missing_logseq_expected": len(
            [e for e in mirrored_open if e.sync.logseq is None]
        ),
    }


def cmd_add(args: argparse.Namespace) -> int:
    text = " ".join(args.text).strip()
    if not text:
        sys.exit("empty todo")
    entry = TodoEntry(
        text=text, source=args.source, due=args.due, project=args.project
    )
    append(entry)
    if not getattr(args, "no_sync", False):
        try:
            entries = load_all()
            _sync_outbound(entries)
            write_all(entries)
        except Exception as exc:  # noqa: BLE001 - capture already persisted
            log(f"add sync best-effort failed id={entry.id}: {exc}")
    print(f"+ {entry.short_id}  {entry.text}")
    return 0


def cmd_ls(args: argparse.Namespace) -> int:
    entries = load_all()
    if args.filter == "open":
        entries = [e for e in entries if e.status == "open"]
    elif args.filter == "done":
        entries = [e for e in entries if e.status == "done"]
    if not entries:
        print("(no todos)")
        return 0
    entries.sort(key=lambda e: e.ts)
    proj_w = max((len(e.project or "-") for e in entries), default=1)
    proj_w = min(max(proj_w, 4), 16)
    src_w = max((len(e.source or "-") for e in entries), default=1)
    src_w = min(max(src_w, 4), 12)
    for e in entries:
        mark = "x" if e.status == "done" else " "
        badges = sync_badges(e)
        ago = human_ago(e.ts)
        proj = (e.project or "-")[:proj_w]
        src = (e.source or "-")[:src_w]
        line = (
            f"{e.short_id}  [{mark}]  {ago:>10}  "
            f"{proj:<{proj_w}}  {src:<{src_w}}  {e.text}"
        )
        if badges:
            line += f"  {badges}"
        print(line)
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    entries = load_all()
    target = find_by_prefix(entries, args.id_prefix)
    if not target:
        sys.exit(f"no todo matches '{args.id_prefix}'")
    target.status = "done"
    target.done_ts = now_iso()
    target.done_source = target.done_source or "local"
    # Persist the local completion before touching the network: a remote that
    # is down or stalls must never cost us the local "done".
    write_all(entries)
    # Done here -> done there: propagate to Todoist + Logseq right away.
    # Best-effort (push_completions swallows network errors); whatever doesn't
    # land is flushed by the next `todo sync`. Re-persist to capture closed_ts.
    closed, _ = todoist.push_completions([target])
    ls_flipped = logseq.complete([target])
    write_all(entries)
    where = [w for w, hit in (("todoist", closed), ("logseq", ls_flipped)) if hit]
    suffix = f"  → {', '.join(where)}" if where else ""
    print(f"done {target.short_id}  {target.text}{suffix}")
    return 0


def cmd_rm(args: argparse.Namespace) -> int:
    entries = load_all()
    target = find_by_prefix(entries, args.id_prefix)
    if not target:
        sys.exit(f"no todo matches '{args.id_prefix}'")
    entries = [e for e in entries if e.id != target.id]
    write_all(entries)
    print(f"rm {target.short_id}  {target.text}")
    return 0


def cmd_edit(args: argparse.Namespace) -> int:
    ensure_store()
    editor = os.environ.get("EDITOR", "vi")
    subprocess.call([editor, str(TODOS_FILE)])
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    entries = load_all()
    rc = 0
    if args.target in ("all", "logseq"):
        rc |= logseq.sync(entries)
    if args.target in ("all", "todoist"):
        rc |= todoist.sync(entries)
    write_all(entries)
    return rc


def cmd_pull(args: argparse.Namespace) -> int:
    entries = load_all()
    rc = todoist.mirror(entries, dry_run=args.dry_run)
    if not args.dry_run:
        write_all(entries)
    return rc


def cmd_refresh(args: argparse.Namespace) -> int:
    entries = load_all()
    return _refresh_task_state(entries, dry_run=args.dry_run)


def cmd_reconcile(args: argparse.Namespace) -> int:
    entries = load_all()
    rc = 0
    if args.target in ("all", "logseq"):
        rc |= logseq.reconcile(entries)
    if args.target in ("all", "todoist"):
        rc |= todoist.reconcile(entries)
    write_all(entries)
    return rc


def cmd_audit(args: argparse.Namespace) -> int:
    counts = _audit_counts(load_all())
    print("todo audit:")
    print(f"  total: {counts['total']}")
    print(f"  open: {counts['open']}")
    print(f"  done: {counts['done']}")
    print(f"  origin_todoist: {counts['origin_todoist']}")
    print(
        "  open_local_missing_todoist: "
        f"{counts['open_local_missing_todoist']}"
    )
    print(
        "  open_local_missing_logseq: "
        f"{counts['open_local_missing_logseq']}"
    )
    print(
        "  open_mirrored_missing_logseq_expected: "
        f"{counts['open_mirrored_missing_logseq_expected']}"
    )
    return 0


def cmd_note(args: argparse.Namespace) -> int:
    """Capture a free-form note into the Obsidian vault (canonical store).

    Writes one Markdown file under <vault>/captures/YYYY-MM-DD/ — the same lane
    the Telegram bot uses — instead of the (now frozen) Logseq journal.
    """
    text = " ".join(args.text).strip()
    if not text:
        sys.exit("empty note")
    path = obsidian.write_capture(text, kind="note", source="cli")
    print(f"note → {path}")
    return 0


def cmd_telegram_send(args: argparse.Namespace) -> int:
    """Send a message to the last chat that messaged the capture bot.

    Lets the bot push a notification back to Nathan's phone (delivery enabler).
    Requires that a message has been received at least once (so a chat_id is on
    file) and that the BotFather token is stored.
    """
    text = " ".join(args.text).strip()
    if not text:
        sys.exit("empty message")
    if telegram.send(text):
        print(f"telegram: sent to chat {telegram.last_chat_id()}")
        return 0
    print(
        "telegram: not sent — need a stored token AND a known chat_id "
        "(message the bot once so it records your chat)"
    )
    return 1


def cmd_telegram_poll(args: argparse.Namespace) -> int:
    """Poll the Telegram capture bot and file messages into the Obsidian vault.

    `--loop` runs the long-poll daemon (launchd KeepAlive); the default single
    pass is handy for testing and for grabbing your chat_id from the bot's reply.
    """
    if not TELEGRAM_ENABLED:
        print("telegram: disabled (TODO_TELEGRAM=0)")
        return 0
    if args.loop:
        # poll_loop idles until a token appears, so the daemon can be loaded
        # before the BotFather token is stored (it activates with no reload).
        return telegram.poll_loop()
    if not telegram.token():
        print(
            "telegram: no token — store one:\n"
            "  security add-generic-password -a telegram -s todo-cli -w "
            "'<BOTFATHER_TOKEN>'"
        )
        return 1
    n = telegram.poll_once()
    print(f"telegram: filed {n} capture(s) into the vault")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    ok = True
    print(f"store dir: {TODO_DIR}  {'OK' if TODO_DIR.exists() else 'MISSING'}")
    print(
        f"todos file: {TODOS_FILE}  "
        f"{'OK' if TODOS_FILE.exists() else 'MISSING'}"
    )
    vault = obsidian.captures_root()
    print(
        f"obsidian captures: {vault}  "
        f"{'OK' if vault.parent.exists() else 'MISSING (vault root absent)'}"
    )
    if not vault.parent.exists():
        ok = False
    # Logseq is a frozen archive (2026-06-01) — writes are gated off by default.
    print(
        f"logseq sync: {'ENABLED (TODO_LOGSEQ_SYNC=1)' if LOGSEQ_SYNC_ENABLED else 'FROZEN (off; archive)'}"
        f"  graph={LOGSEQ_GRAPH}"
    )
    tok = todoist.token()
    print(f"todoist token: {'OK (keychain or env)' if tok else 'MISSING'}")
    if not tok:
        ok = False
    print(f"todoist project: {TODOIST_PROJECT_ID}")
    ttok = telegram.token()
    print(f"telegram token: {'OK (keychain or env)' if ttok else 'MISSING (bot idle)'}")
    print(
        f"telegram chat: {telegram.last_chat_id() or 'none yet (message the bot once)'}"
    )
    pol = mirror_policy()
    print(
        f"mirror policy: exclude_shared={pol['exclude_shared']} "
        f"exclude_ids={pol['exclude_project_ids'] or '[]'}"
    )
    return 0 if ok else 1
