"""Logseq journal sync + reconcile."""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

from .config import LOGSEQ_GRAPH
from .models import LogseqSync, TodoEntry, now_iso
from .storage import log


_DONE_RE = re.compile(r"^\s*-\s+(DONE|CANCELED|CANCELLED)\b", re.IGNORECASE)
_ARCHIVED_RE = re.compile(r"^\s*-\s+\[x\]", re.IGNORECASE)


def journal_path(when: dt.date | None = None) -> Path:
    when = when or dt.date.today()
    return LOGSEQ_GRAPH / "journals" / when.strftime("%Y_%m_%d.md")


def line_for(entry: TodoEntry) -> str:
    return f"- TODO {entry.text}"


def marker(entry: TodoEntry) -> str:
    """Stable marker we can grep for to confirm presence (idempotency)."""
    return f"<!-- todo:{entry.id} -->"


def sync(entries: list[TodoEntry]) -> int:
    journal = journal_path()
    journal.parent.mkdir(parents=True, exist_ok=True)
    existing = journal.read_text() if journal.exists() else ""
    pending = [e for e in entries if e.status == "open" and e.sync.logseq is None]
    if not pending:
        print("logseq: nothing to sync")
        return 0
    appended = 0
    new_blocks: list[str] = []
    for e in pending:
        m = marker(e)
        ls = LogseqSync(file=str(journal), marker=m, ts=now_iso())
        if m in existing:
            e.sync.logseq = ls
            continue
        new_blocks.append(f"{line_for(e)} {m}")
        e.sync.logseq = ls
        appended += 1
    if new_blocks:
        sep = "" if not existing or existing.endswith("\n") else "\n"
        with journal.open("a") as f:
            f.write(sep + "\n".join(new_blocks) + "\n")
    print(f"logseq: appended {appended} → {journal}")
    log(f"logseq sync appended={appended} file={journal}")
    return 0


def reconcile(entries: list[TodoEntry]) -> int:
    """Scan synced journal lines; if marker line begins with DONE, mark local done.

    Also detects Logseq's checkbox `- [x]` form.
    """
    checked = 0
    flipped = 0
    missing = 0
    by_file: dict[str, list[TodoEntry]] = {}
    for e in entries:
        if e.sync.logseq is None or e.status != "open":
            continue
        by_file.setdefault(e.sync.logseq.file, []).append(e)
    for path, batch in by_file.items():
        p = Path(path)
        if not p.exists():
            print(f"logseq: file gone {path}")
            missing += len(batch)
            continue
        text = p.read_text()
        for e in batch:
            assert e.sync.logseq is not None
            mk = e.sync.logseq.marker
            checked += 1
            line = next((ln for ln in text.splitlines() if mk in ln), None)
            if line is None:
                missing += 1
                continue
            if _DONE_RE.match(line) or _ARCHIVED_RE.match(line):
                e.status = "done"
                e.done_ts = now_iso()
                e.done_source = "logseq"
                flipped += 1
    print(
        f"logseq reconcile: checked {checked}, flipped {flipped}, missing {missing}"
    )
    log(
        f"logseq reconcile checked={checked} flipped={flipped} missing={missing}"
    )
    return 0
