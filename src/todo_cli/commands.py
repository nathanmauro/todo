"""Subcommand handlers — one per CLI verb."""
from __future__ import annotations

import argparse
import contextlib
import io
import os
import subprocess
import sys

from . import classify, ledger, logseq, notion, telegram, todoist
from .config import (
    CLASSIFY_ENABLED,
    INBOX_CAPTURE_PAGE,
    LOGSEQ_GRAPH,
    TELEGRAM_ENABLED,
    TODOIST_PROJECT_ID,
    TODO_DIR,
    TODOS_FILE,
    mirror_policy,
)
from .formatting import human_ago, sync_badges
from .models import TodoEntry, new_id, now_iso
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
        "notion_inbox_linked": len(
            [e for e in entries if e.notion_inbox_id is not None]
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
    print(f"  notion_inbox_linked: {counts['notion_inbox_linked']}")
    return 0


def cmd_note(args: argparse.Namespace) -> int:
    """Append a free-form note to today's Logseq journal (local-only)."""
    text = " ".join(args.text).strip()
    if not text:
        sys.exit("empty note")
    src_id = new_id()[-8:]
    if logseq.note(text, src_id):
        print(f"note → today's journal  ({src_id})  {text}")
    else:
        print("note: nothing appended (empty or already present)")
    return 0


_INBOX_PROPS = (
    "para:: resource\n"
    "area:: [[area/agent-logs]]\n"
    "summary:: low-confidence mobile captures awaiting manual triage"
)


def _file_capture(row, pages: dict[str, str], dry_run: bool) -> str:
    """Decide + write one note/idea capture; return a one-line description.

    Idea rows keep the existing `#idea` journal flow. Plain notes are routed by
    the PARA classifier: a confident match goes to that topic page, a borderline
    match is quarantined to the inbox-capture page, everything else lands in the
    journal. Every block carries the `nx` marker and is recorded in the ledger so
    re-runs never double-file even if the classifier later picks a different page.
    """
    mk = notion.nx_marker(row.page_id)

    if row.idea:
        block = f"- #idea {row.text} {mk}"
        if not dry_run:
            logseq.append_journal_dedup(block, mk)
            ledger.record(row.page_id, "journal", source=row.source)
        return "journal (#idea)"

    if CLASSIFY_ENABLED and pages:
        dec = classify.classify(row.text, pages)
    else:
        dec = classify.Decision("journal", via="disabled")

    links = " ".join(f"[[{name}]]" for name in dec.links)
    block = f"- {row.text}{(' ' + links) if links else ''} {mk}"

    if dec.action == "page" and dec.target_file:
        if not dry_run:
            logseq.append_to_page(dec.target_file, block, marker=mk)
            ledger.record(row.page_id, dec.target_file,
                          confidence=dec.confidence, source=row.source)
        return f"page [[{dec.page_name}]] (conf {dec.confidence:.2f} via {dec.via})"

    if dec.action == "inbox":
        fn = logseq.file_for_page(INBOX_CAPTURE_PAGE)
        if not dry_run:
            logseq.append_to_page(fn, block, marker=mk, create_props=_INBOX_PROPS)
            ledger.record(row.page_id, fn,
                          confidence=dec.confidence, source=row.source)
        return f"inbox-capture (conf {dec.confidence:.2f}, needs triage)"

    if not dry_run:
        logseq.append_journal_dedup(block, mk)
        ledger.record(row.page_id, "journal",
                      confidence=dec.confidence, source=row.source)
    return f"journal (conf {dec.confidence:.2f} via {dec.via})"


def cmd_notion_sync(args: argparse.Namespace) -> int:
    """Pull mobile captures (Notion Capture Inbox + Telegram) into the Logseq graph.

    Telegram messages are first turned into Capture Inbox rows (producer lane), so
    the single drain below handles everything. Plain notes are PARA-classified and
    filed to the best topic page (or quarantined / journaled); idea rows keep the
    `#idea` journal flow; task-flagged rows become TodoEntry rows that reach
    Todoist + the journal via the existing sync path. Each processed row is flipped
    to Synced=true. `--dry-run` reports placement without writing or marking.
    """
    tok = notion.token()
    if not tok:
        print(
            "notion: no token — set NOTION_TOKEN or add keychain account "
            f"'{notion.NOTION_KEYCHAIN_ACCOUNT}' under service "
            f"'{notion.KEYCHAIN_SERVICE}'"
        )
        return 1

    # Telegram lane: turn new messages into Capture Inbox rows first, so the
    # single drain below files them too. Best-effort — never blocks the drain.
    tg = 0
    if TELEGRAM_ENABLED and not args.dry_run:
        try:
            tg = telegram.pull_into_inbox(tok)
        except Exception as exc:  # noqa: BLE001 — lane must not break the drain
            log(f"telegram lane error: {exc}")

    rows = notion.query_unsynced(tok)
    if rows is None:
        print(
            f"notion: could not reach Capture Inbox (db {notion.NOTION_INBOX_DB}) "
            "— is the 'local-todo' integration connected to it? "
            "See ~/Developer/proj/todo/docs/android-capture.md"
        )
        return 1
    if not rows:
        print("notion: nothing to pull")
        rc = 0
        if not args.dry_run:
            notion.write_state(0, 0, 0)
            if not args.pull_only:
                rc = _refresh_task_state(load_all(), quiet=True)
        return rc

    entries = load_all()
    seen_inbox = {getattr(e, "notion_inbox_id", None) for e in entries}
    pages = logseq.page_index() if CLASSIFY_ENABLED else {}

    to_mark: list[str] = []
    notes_filed = 0
    tasks_created = 0

    for row in rows:
        if ledger.has(row.page_id):
            # Already filed on a prior run; just (re)ensure it gets marked.
            to_mark.append(row.page_id)
            continue
        if row.task:
            # Route through the todo store -> Todoist + journal TODO line.
            if row.page_id not in seen_inbox:
                if not args.dry_run:
                    entries.append(
                        TodoEntry(
                            text=row.text,
                            source=row.source or "mobile",
                            notion_inbox_id=row.page_id,
                        )
                    )
                tasks_created += 1
                if args.dry_run:
                    print(f"  task  {row.text!r} -> Todoist + journal")
            to_mark.append(row.page_id)
            continue
        desc = _file_capture(row, pages, args.dry_run)
        notes_filed += 1
        if args.dry_run:
            print(f"  note  {row.text!r} -> {desc}")
        to_mark.append(row.page_id)

    if args.dry_run:
        print(
            f"notion: DRY RUN — {notes_filed} note(s), {tasks_created} task(s) "
            f"across {len(rows)} row(s); nothing written or marked"
        )
        return 0

    if tasks_created:
        write_all(entries)

    marked = sum(1 for pid in to_mark if notion.mark_synced(tok, pid))
    notion.write_state(notes_filed, tasks_created, len(rows))
    refresh_rc = 0
    if args.pull_only:
        # Preserve the explicit pull-only contract: task rows get journal refs,
        # but no Todoist creates/closes are pushed by this command.
        entries = load_all()
        _run_quiet(logseq.sync, entries, quiet=True)
        write_all(entries)
    else:
        refresh_rc = _refresh_task_state(load_all(), quiet=True)
    print(
        f"notion: pulled {notes_filed} note(s), {tasks_created} task(s)"
        f"{f' (+{tg} via Telegram)' if tg else ''}; "
        f"marked {marked}/{len(to_mark)} synced"
    )
    return refresh_rc


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
    ls_dir = LOGSEQ_GRAPH / "journals"
    print(f"logseq journals: {ls_dir}  {'OK' if ls_dir.exists() else 'MISSING'}")
    if not ls_dir.exists():
        ok = False
    tok = todoist.token()
    print(f"todoist token: {'OK (keychain or env)' if tok else 'MISSING'}")
    if not tok:
        ok = False
    print(f"todoist project: {TODOIST_PROJECT_ID}")
    ntok = notion.token()
    print(f"notion token: {'OK (keychain or env)' if ntok else 'MISSING'}")
    print(f"notion inbox db: {notion.NOTION_INBOX_DB}")
    pol = mirror_policy()
    print(
        f"mirror policy: exclude_shared={pol['exclude_shared']} "
        f"exclude_ids={pol['exclude_project_ids'] or '[]'}"
    )
    return 0 if ok else 1
