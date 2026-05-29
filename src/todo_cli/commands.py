"""Subcommand handlers — one per CLI verb."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

from . import logseq, todoist
from .config import (
    LOGSEQ_GRAPH,
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
    write_all,
)


def cmd_add(args: argparse.Namespace) -> int:
    text = " ".join(args.text).strip()
    if not text:
        sys.exit("empty todo")
    entry = TodoEntry(
        text=text, source=args.source, due=args.due, project=args.project
    )
    append(entry)
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
    write_all(entries)
    print(f"done {target.short_id}  {target.text}")
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


def cmd_reconcile(args: argparse.Namespace) -> int:
    entries = load_all()
    rc = 0
    if args.target in ("all", "logseq"):
        rc |= logseq.reconcile(entries)
    if args.target in ("all", "todoist"):
        rc |= todoist.reconcile(entries)
    write_all(entries)
    return rc


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
    pol = mirror_policy()
    print(
        f"mirror policy: exclude_shared={pol['exclude_shared']} "
        f"exclude_ids={pol['exclude_project_ids'] or '[]'}"
    )
    return 0 if ok else 1
