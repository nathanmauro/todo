"""todo — local-first capture CLI with Logseq + Notion sync.

Storage: ~/.todo/todos.jsonl (append-only JSON Lines).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import secrets
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

HOME = Path.home()
TODO_DIR = Path(os.environ.get("TODO_DIR", HOME / ".todo"))
TODOS_FILE = TODO_DIR / "todos.jsonl"
LOG_FILE = TODO_DIR / "todo.log"

LOGSEQ_GRAPH = Path(
    os.environ.get("TODO_LOGSEQ_GRAPH", HOME / "Notes")
)
NOTION_DB_ID = os.environ.get(
    "TODO_NOTION_DB_ID", "353b9be9-bd58-8049-b5c5-e577f0a49756"
)
NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
KEYCHAIN_ACCOUNT = "notion"
KEYCHAIN_SERVICE = "todo-cli"


# ---------- storage ----------


def ensure_store() -> None:
    TODO_DIR.mkdir(parents=True, exist_ok=True)
    TODOS_FILE.touch(exist_ok=True)


def new_id() -> str:
    # ULID-ish: timestamp + random, sortable, short enough for prefix matching.
    ts = int(dt.datetime.now().timestamp() * 1000)
    return f"{ts:013d}{secrets.token_hex(4)}"


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def load_all() -> list[dict]:
    ensure_store()
    out = []
    with TODOS_FILE.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def write_all(entries: list[dict]) -> None:
    ensure_store()
    tmp = TODOS_FILE.with_suffix(".jsonl.tmp")
    with tmp.open("w") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    tmp.replace(TODOS_FILE)


def append(entry: dict) -> None:
    ensure_store()
    with TODOS_FILE.open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def short_id(entry_id: str) -> str:
    """Display id: trailing 8 random hex chars (more unique than ts prefix)."""
    return entry_id[-8:]


def find_by_prefix(entries: list[dict], needle: str) -> dict | None:
    """Match against full id, short_id, or any substring of full id."""
    matches = [
        e
        for e in entries
        if e["id"] == needle
        or short_id(e["id"]).startswith(needle)
        or needle in e["id"]
    ]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        sys.exit(f"ambiguous '{needle}' ({len(matches)} matches)")
    return None


def log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a") as f:
        f.write(f"{now_iso()} {msg}\n")


# ---------- formatting ----------


def human_ago(iso: str) -> str:
    try:
        t = dt.datetime.fromisoformat(iso)
    except ValueError:
        return iso
    delta = dt.datetime.now().astimezone() - t
    secs = int(delta.total_seconds())
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    days = secs // 86400
    if days < 30:
        return f"{days}d ago"
    return t.strftime("%Y-%m-%d")


def sync_badges(entry: dict) -> str:
    s = entry.get("sync") or {}
    parts = []
    if s.get("logseq"):
        parts.append("logseq")
    if s.get("notion"):
        parts.append("notion")
    return " ".join(f"[{p}]" for p in parts)


# ---------- commands ----------


def cmd_add(args: argparse.Namespace) -> int:
    text = " ".join(args.text).strip()
    if not text:
        sys.exit("empty todo")
    entry = {
        "id": new_id(),
        "ts": now_iso(),
        "text": text,
        "status": "open",
        "source": args.source,
        "sync": {"logseq": None, "notion": None},
    }
    if args.due:
        entry["due"] = args.due
    append(entry)
    print(f"+ {short_id(entry['id'])}  {text}")
    return 0


def cmd_ls(args: argparse.Namespace) -> int:
    entries = load_all()
    if args.filter == "open":
        entries = [e for e in entries if e.get("status") == "open"]
    elif args.filter == "done":
        entries = [e for e in entries if e.get("status") == "done"]
    if not entries:
        print("(no todos)")
        return 0
    entries.sort(key=lambda e: e["ts"])
    for e in entries:
        mark = "x" if e.get("status") == "done" else " "
        badges = sync_badges(e)
        prefix = short_id(e["id"])
        ago = human_ago(e["ts"])
        text = e["text"]
        line = f"{prefix}  [{mark}]  {ago:>10}  {text}"
        if badges:
            line += f"  {badges}"
        print(line)
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    entries = load_all()
    target = find_by_prefix(entries, args.id_prefix)
    if not target:
        sys.exit(f"no todo matches '{args.id_prefix}'")
    target["status"] = "done"
    target["done_ts"] = now_iso()
    write_all(entries)
    print(f"done {short_id(target['id'])}  {target['text']}")
    return 0


def cmd_rm(args: argparse.Namespace) -> int:
    entries = load_all()
    target = find_by_prefix(entries, args.id_prefix)
    if not target:
        sys.exit(f"no todo matches '{args.id_prefix}'")
    entries = [e for e in entries if e["id"] != target["id"]]
    write_all(entries)
    print(f"rm {short_id(target['id'])}  {target['text']}")
    return 0


def cmd_edit(args: argparse.Namespace) -> int:
    ensure_store()
    editor = os.environ.get("EDITOR", "vi")
    subprocess.call([editor, str(TODOS_FILE)])
    return 0


# ---------- Logseq sync ----------


def logseq_journal_path(when: dt.date | None = None) -> Path:
    when = when or dt.date.today()
    return LOGSEQ_GRAPH / "journals" / when.strftime("%Y_%m_%d.md")


def logseq_line_for(entry: dict) -> str:
    return f"- TODO {entry['text']}"


def logseq_marker(entry: dict) -> str:
    """Stable marker we can grep for to confirm presence (idempotency)."""
    return f"<!-- todo:{entry['id']} -->"


def sync_logseq(entries: list[dict]) -> int:
    journal = logseq_journal_path()
    journal.parent.mkdir(parents=True, exist_ok=True)
    existing = journal.read_text() if journal.exists() else ""
    pending = [
        e
        for e in entries
        if e.get("status") == "open" and not (e.get("sync") or {}).get("logseq")
    ]
    if not pending:
        print("logseq: nothing to sync")
        return 0
    appended = 0
    new_blocks: list[str] = []
    for e in pending:
        marker = logseq_marker(e)
        if marker in existing:
            e.setdefault("sync", {})["logseq"] = {
                "file": str(journal),
                "marker": marker,
                "ts": now_iso(),
            }
            continue
        new_blocks.append(f"{logseq_line_for(e)} {marker}")
        e.setdefault("sync", {})["logseq"] = {
            "file": str(journal),
            "marker": marker,
            "ts": now_iso(),
        }
        appended += 1
    if new_blocks:
        sep = "" if not existing or existing.endswith("\n") else "\n"
        with journal.open("a") as f:
            f.write(sep + "\n".join(new_blocks) + "\n")
    print(f"logseq: appended {appended} → {journal}")
    log(f"logseq sync appended={appended} file={journal}")
    return 0


# ---------- Notion sync ----------


def notion_token() -> str | None:
    env = os.environ.get("NOTION_TOKEN")
    if env:
        return env
    try:
        r = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-a",
                KEYCHAIN_ACCOUNT,
                "-s",
                KEYCHAIN_SERVICE,
                "-w",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except FileNotFoundError:
        pass
    return None


def notion_fetch_page(token: str, page_id: str) -> dict:
    req = urllib.request.Request(
        f"{NOTION_API}/pages/{page_id}",
        method="GET",
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def notion_create_page(token: str, text: str) -> dict:
    body = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "Task name": {"title": [{"text": {"content": text}}]},
            "Status": {"status": {"name": "Not started"}},
        },
    }
    req = urllib.request.Request(
        f"{NOTION_API}/pages",
        data=json.dumps(body).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def sync_notion(entries: list[dict]) -> int:
    token = notion_token()
    if not token:
        print(
            "notion: no token. store one: security add-generic-password "
            f"-a {KEYCHAIN_ACCOUNT} -s {KEYCHAIN_SERVICE} -w <token>"
        )
        return 1
    pending = [
        e
        for e in entries
        if e.get("status") == "open" and not (e.get("sync") or {}).get("notion")
    ]
    if not pending:
        print("notion: nothing to sync")
        return 0
    created = 0
    failed = 0
    for e in pending:
        try:
            page = notion_create_page(token, e["text"])
        except urllib.error.HTTPError as exc:
            body = exc.read().decode(errors="replace")
            print(f"notion: {e['id'][:8]} FAIL {exc.code} {body[:200]}")
            log(f"notion fail id={e['id']} code={exc.code} body={body[:500]}")
            failed += 1
            continue
        except urllib.error.URLError as exc:
            print(f"notion: {e['id'][:8]} network error: {exc}")
            failed += 1
            continue
        e.setdefault("sync", {})["notion"] = {
            "page_id": page.get("id"),
            "url": page.get("url"),
            "ts": now_iso(),
        }
        created += 1
    print(f"notion: created {created}, failed {failed}")
    log(f"notion sync created={created} failed={failed}")
    return 0 if failed == 0 else 1


# ---------- reconcile (remote → local) ----------


_DONE_RE = re.compile(r"^\s*-\s+(DONE|CANCELED|CANCELLED)\b", re.IGNORECASE)
_ARCHIVED_RE = re.compile(r"^\s*-\s+\[x\]", re.IGNORECASE)


def reconcile_logseq(entries: list[dict]) -> int:
    """Scan synced journal lines; if marker line begins with DONE, mark local done.

    Also detects Logseq's checkbox `- [x]` form just in case.
    """
    checked = 0
    flipped = 0
    missing = 0
    # Group entries by file to read each journal once.
    by_file: dict[str, list[dict]] = {}
    for e in entries:
        sl = (e.get("sync") or {}).get("logseq")
        if not sl or e.get("status") != "open":
            continue
        by_file.setdefault(sl["file"], []).append(e)
    for path, batch in by_file.items():
        p = Path(path)
        if not p.exists():
            print(f"logseq: file gone {path}")
            missing += len(batch)
            continue
        text = p.read_text()
        for e in batch:
            marker = (e["sync"]["logseq"] or {}).get("marker", "")
            checked += 1
            line = next(
                (ln for ln in text.splitlines() if marker in ln), None
            )
            if line is None:
                missing += 1
                continue
            if _DONE_RE.match(line) or _ARCHIVED_RE.match(line):
                e["status"] = "done"
                e["done_ts"] = now_iso()
                e["done_source"] = "logseq"
                flipped += 1
    print(
        f"logseq reconcile: checked {checked}, flipped {flipped}, missing {missing}"
    )
    log(
        f"logseq reconcile checked={checked} flipped={flipped} missing={missing}"
    )
    return 0


def reconcile_notion(entries: list[dict]) -> int:
    token = notion_token()
    if not token:
        print("notion: no token; skipping reconcile")
        return 1
    checked = 0
    flipped = 0
    archived = 0
    failed = 0
    for e in entries:
        sn = (e.get("sync") or {}).get("notion")
        if not sn or e.get("status") != "open":
            continue
        page_id = sn.get("page_id")
        if not page_id:
            continue
        checked += 1
        try:
            page = notion_fetch_page(token, page_id)
        except urllib.error.HTTPError as exc:
            print(f"notion: {short_id(e['id'])} FAIL {exc.code}")
            failed += 1
            continue
        except urllib.error.URLError as exc:
            print(f"notion: {short_id(e['id'])} network error {exc}")
            failed += 1
            continue
        if page.get("archived") or page.get("in_trash"):
            archived += 1
            continue
        status = (
            page.get("properties", {})
            .get("Status", {})
            .get("status")
            or {}
        )
        name = (status.get("name") or "").lower()
        if name == "done":
            e["status"] = "done"
            e["done_ts"] = now_iso()
            e["done_source"] = "notion"
            flipped += 1
    print(
        f"notion reconcile: checked {checked}, flipped {flipped}, "
        f"archived {archived}, failed {failed}"
    )
    log(
        f"notion reconcile checked={checked} flipped={flipped} "
        f"archived={archived} failed={failed}"
    )
    return 0 if failed == 0 else 1


def cmd_reconcile(args: argparse.Namespace) -> int:
    entries = load_all()
    rc = 0
    if args.target in ("all", "logseq"):
        rc |= reconcile_logseq(entries)
    if args.target in ("all", "notion"):
        rc |= reconcile_notion(entries)
    write_all(entries)
    return rc


# ---------- sync orchestration ----------


def cmd_sync(args: argparse.Namespace) -> int:
    entries = load_all()
    targets = []
    if args.target in ("all", "logseq"):
        targets.append("logseq")
    if args.target in ("all", "notion"):
        targets.append("notion")
    rc = 0
    if "logseq" in targets:
        rc |= sync_logseq(entries)
    if "notion" in targets:
        rc |= sync_notion(entries)
    write_all(entries)
    return rc


# ---------- doctor ----------


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
    token = notion_token()
    print(f"notion token: {'OK (keychain or env)' if token else 'MISSING'}")
    if not token:
        ok = False
    print(f"notion db id: {NOTION_DB_ID}")
    return 0 if ok else 1


# ---------- argparse ----------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo", description="local todo capture")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="add a todo")
    a.add_argument("text", nargs="+")
    a.add_argument("--due", help="ISO date YYYY-MM-DD")
    a.add_argument("--source", default="cli")
    a.set_defaults(func=cmd_add)

    ls = sub.add_parser("ls", help="list todos")
    ls.add_argument(
        "--all", dest="filter", action="store_const", const="all"
    )
    ls.add_argument(
        "--done", dest="filter", action="store_const", const="done"
    )
    ls.add_argument(
        "--open", dest="filter", action="store_const", const="open"
    )
    ls.set_defaults(filter="open", func=cmd_ls)

    d = sub.add_parser("done", help="mark a todo done")
    d.add_argument("id_prefix")
    d.set_defaults(func=cmd_done)

    r = sub.add_parser("rm", help="delete a todo")
    r.add_argument("id_prefix")
    r.set_defaults(func=cmd_rm)

    e = sub.add_parser("edit", help="open todos.jsonl in $EDITOR")
    e.set_defaults(func=cmd_edit)

    s = sub.add_parser("sync", help="push to Logseq and/or Notion")
    s.add_argument(
        "--target",
        choices=["all", "logseq", "notion"],
        default="all",
    )
    s.set_defaults(func=cmd_sync)

    rc = sub.add_parser(
        "reconcile",
        help="pull status from remotes (mark local done if remote done)",
    )
    rc.add_argument(
        "--target",
        choices=["all", "logseq", "notion"],
        default="all",
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
