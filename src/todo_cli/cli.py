"""todo — local-first capture CLI with Obsidian + Todoist sync.

Storage: ~/.todo/todos.jsonl (append-only JSON Lines). Notes/captures land in the
Obsidian vault (the canonical store); tasks push to Todoist. Logseq is a frozen
archive — its task-sync writers are gated off behind TODO_LOGSEQ_SYNC.
"""
from __future__ import annotations

import argparse
import sys

from .storage import LockTimeout

from .commands import (
    cmd_add,
    cmd_audit,
    cmd_backlog,
    cmd_doctor,
    cmd_done,
    cmd_edit,
    cmd_ls,
    cmd_note,
    cmd_plan,
    cmd_pull,
    cmd_refresh,
    cmd_reconcile,
    cmd_rm,
    cmd_sync,
    cmd_telegram_poll,
    cmd_telegram_send,
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo", description="local todo capture")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="add a todo")
    a.add_argument("text", nargs="+")
    a.add_argument("--due", help="ISO date YYYY-MM-DD")
    a.add_argument("--source", default="cli")
    a.add_argument("--project", help="project tag (e.g. bin, todo, mcp-memory-agent)")
    a.add_argument(
        "--no-sync",
        action="store_true",
        help="only write the local JSONL row; defer Todoist sync",
    )
    a.set_defaults(func=cmd_add)

    ls = sub.add_parser("ls", help="list todos")
    ls.add_argument("--all", dest="filter", action="store_const", const="all")
    ls.add_argument("--done", dest="filter", action="store_const", const="done")
    ls.add_argument("--open", dest="filter", action="store_const", const="open")
    ls.set_defaults(filter="open", func=cmd_ls)

    bk = sub.add_parser(
        "backlog",
        help="show this project's backlog / planned / in-flight (cwd-derived)",
    )
    bk.add_argument(
        "name",
        nargs="?",
        help="project label (default: current directory name)",
    )
    bk.add_argument(
        "--if-project",
        action="store_true",
        help="silent no-op unless cwd is a known project label "
        "(near-free guard for a global SessionStart hook; implies --offline)",
    )
    bk.add_argument(
        "--offline",
        action="store_true",
        help="use the local Todoist mirror only — no network call",
    )
    bk.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="emit stable JSON groups for agents and hooks",
    )
    bk.add_argument(
        "--history",
        action="store_true",
        help="include executed/done plan history in terminal output",
    )
    bk.set_defaults(func=cmd_backlog)

    pl = sub.add_parser(
        "plan",
        help="shape an idea or create/execute/status an execution plan",
        description="Shape an idea or manage execution-plan records.",
        epilog=(
            "Examples:\n"
            "  todo plan idea-slug --project cockpit\n"
            "  todo plan create --id plan-slug --title \"Plan\" --project cockpit --summary \"one-line\"\n"
            "  todo plan execute plan-slug --summary \"what shipped\"\n"
            "  todo plan status plan-slug"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    pl.add_argument("plan_args", nargs=argparse.REMAINDER, metavar="{<idea>|create|execute|status}")
    pl.set_defaults(func=cmd_plan)

    d = sub.add_parser("done", help="mark a todo done")
    d.add_argument("id_prefix")
    d.set_defaults(func=cmd_done)

    r = sub.add_parser("rm", help="delete a todo")
    r.add_argument("id_prefix")
    r.set_defaults(func=cmd_rm)

    e = sub.add_parser("edit", help="open todos.jsonl in $EDITOR")
    e.set_defaults(func=cmd_edit)

    s = sub.add_parser(
        "sync",
        help="push pending tasks to Todoist (logseq target is frozen unless TODO_LOGSEQ_SYNC=1)",
    )
    s.add_argument(
        "--target", choices=["all", "logseq", "todoist"], default="all"
    )
    s.set_defaults(func=cmd_sync)

    pull = sub.add_parser(
        "pull",
        help="mirror Todoist tasks into the local store (Todoist is source of truth)",
    )
    pull.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would change without writing",
    )
    pull.set_defaults(func=cmd_pull)

    refresh = sub.add_parser(
        "refresh",
        help="converge Todoist and the local store (Logseq sync frozen by default)",
    )
    refresh.add_argument(
        "--dry-run",
        action="store_true",
        help="show planned convergence without writing",
    )
    refresh.set_defaults(func=cmd_refresh)

    rc = sub.add_parser(
        "reconcile",
        help="pull status from remotes (mark local done if remote done)",
    )
    rc.add_argument(
        "--target", choices=["all", "logseq", "todoist"], default="all"
    )
    rc.set_defaults(func=cmd_reconcile)

    nt = sub.add_parser(
        "note", help="capture a free-form note into the Obsidian vault"
    )
    nt.add_argument("text", nargs="+")
    nt.set_defaults(func=cmd_note)

    tg = sub.add_parser(
        "telegram-poll",
        help="poll the Telegram capture bot; file messages into the Obsidian vault",
    )
    tg.add_argument(
        "--loop",
        action="store_true",
        help="run the long-poll daemon (launchd KeepAlive); default is one pass",
    )
    tg.set_defaults(func=cmd_telegram_poll)

    ts = sub.add_parser(
        "telegram-send",
        help="send a message to the last chat that messaged the capture bot",
    )
    ts.add_argument("text", nargs="+")
    ts.add_argument(
        "--button",
        action="append",
        default=[],
        metavar="LABEL=VERB[:PAYLOAD]",
        help=(
            "inline action button (repeatable); "
            "verbs: ack, add-task, idea-hot, todoist-complete"
        ),
    )
    ts.set_defaults(func=cmd_telegram_send)

    audit = sub.add_parser("audit", help="summarize local sync state")
    audit.set_defaults(func=cmd_audit)

    doc = sub.add_parser("doctor", help="check setup")
    doc.set_defaults(func=cmd_doctor)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except LockTimeout as exc:
        print(f"todo: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
