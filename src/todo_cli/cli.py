"""todo — local-first capture CLI with Logseq + Todoist sync.

Storage: ~/.todo/todos.jsonl (append-only JSON Lines).
"""
from __future__ import annotations

import argparse

from .commands import (
    cmd_add,
    cmd_doctor,
    cmd_done,
    cmd_edit,
    cmd_ls,
    cmd_reconcile,
    cmd_rm,
    cmd_sync,
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo", description="local todo capture")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="add a todo")
    a.add_argument("text", nargs="+")
    a.add_argument("--due", help="ISO date YYYY-MM-DD")
    a.add_argument("--source", default="cli")
    a.add_argument("--project", help="project tag (e.g. bin, todo, mcp-memory-agent)")
    a.set_defaults(func=cmd_add)

    ls = sub.add_parser("ls", help="list todos")
    ls.add_argument("--all", dest="filter", action="store_const", const="all")
    ls.add_argument("--done", dest="filter", action="store_const", const="done")
    ls.add_argument("--open", dest="filter", action="store_const", const="open")
    ls.set_defaults(filter="open", func=cmd_ls)

    d = sub.add_parser("done", help="mark a todo done")
    d.add_argument("id_prefix")
    d.set_defaults(func=cmd_done)

    r = sub.add_parser("rm", help="delete a todo")
    r.add_argument("id_prefix")
    r.set_defaults(func=cmd_rm)

    e = sub.add_parser("edit", help="open todos.jsonl in $EDITOR")
    e.set_defaults(func=cmd_edit)

    s = sub.add_parser("sync", help="push to Logseq and/or Todoist")
    s.add_argument(
        "--target", choices=["all", "logseq", "todoist"], default="all"
    )
    s.set_defaults(func=cmd_sync)

    rc = sub.add_parser(
        "reconcile",
        help="pull status from remotes (mark local done if remote done)",
    )
    rc.add_argument(
        "--target", choices=["all", "logseq", "todoist"], default="all"
    )
    rc.set_defaults(func=cmd_reconcile)

    doc = sub.add_parser("doctor", help="check setup")
    doc.set_defaults(func=cmd_doctor)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
