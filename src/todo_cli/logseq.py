"""Logseq journal sync + reconcile (FROZEN archive; gated OFF by default).

Logseq (~/Notes/logseq) became a read-only archive on 2026-06-01 — the Obsidian
vault is now the canonical store. Every writer/reader here is gated behind
`config.LOGSEQ_SYNC_ENABLED` (env `TODO_LOGSEQ_SYNC=1`) and is a NO-OP unless it
is explicitly turned on, so `todo add/done/sync/refresh` no longer touch the
frozen graph. The code is kept (not deleted) so a one-off backfill can re-enable
it by flipping the flag.
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

from .config import LOGSEQ_GRAPH, LOGSEQ_SYNC_ENABLED
from .models import LogseqSync, TodoEntry, now_iso
from .storage import log


_DONE_RE = re.compile(r"^\s*-\s+(DONE|CANCELED|CANCELLED)\b", re.IGNORECASE)
_ARCHIVED_RE = re.compile(r"^\s*-\s+\[x\]", re.IGNORECASE)
# Open task-marker forms we rewrite to DONE on outbound completion.
_OPEN_KW_RE = re.compile(r"^(\s*-\s+)(TODO|DOING|NOW|LATER|WAITING)\b", re.IGNORECASE)
_OPEN_BOX_RE = re.compile(r"^(\s*-\s+)\[ \]")


def journal_path(when: dt.date | None = None) -> Path:
    when = when or dt.date.today()
    return LOGSEQ_GRAPH / "journals" / when.strftime("%Y_%m_%d.md")


def line_for(entry: TodoEntry) -> str:
    return f"- TODO {entry.text}"


def marker(entry: TodoEntry) -> str:
    """Stable marker we can grep for to confirm presence (idempotency)."""
    return f"<!-- todo:{entry.id} -->"


def append_lines(lines: list[str], when: dt.date | None = None) -> Path:
    """Append already-formatted journal blocks to a day's journal.

    Each item in `lines` is a full block including its leading `- `. Adds a
    leading newline if the file does not already end in one. Returns the path.
    Shared by `notion-sync` and `note`; callers handle idempotency themselves.
    """
    journal = journal_path(when)
    journal.parent.mkdir(parents=True, exist_ok=True)
    existing = journal.read_text() if journal.exists() else ""
    if not lines:
        return journal
    sep = "" if not existing or existing.endswith("\n") else "\n"
    with journal.open("a") as f:
        f.write(sep + "\n".join(lines) + "\n")
    return journal


def pages_dir() -> Path:
    return LOGSEQ_GRAPH / "pages"


def file_for_page(name: str) -> str:
    """Logseq page name -> filename (triple-underscore namespaces). 'prj/X' -> 'prj___X.md'."""
    return name.replace("/", "___") + ".md"


def page_index() -> dict[str, str]:
    """Map existing Logseq page names -> filename, as PARA-filing destinations.

    Excludes auto-generated agent-log pages (claude*/…) — captures must never be
    filed into a session/memory log. Journals are excluded by living elsewhere.
    """
    out: dict[str, str] = {}
    d = pages_dir()
    if not d.exists():
        return out
    for p in sorted(d.glob("*.md")):
        fn = p.name
        if fn.startswith("claude"):  # claude___, claude-memory___, claude-research___
            continue
        name = fn[:-3].replace("___", "/")  # strip .md, restore namespace
        out[name] = fn
    return out


def append_to_page(filename: str, block: str, marker: str | None = None,
                    create_props: str | None = None) -> Path | None:
    """Append one outliner `block` to pages/<filename> (create if missing).

    `marker` (the trailing `<!-- nx:… -->`) gives an in-file idempotency guard:
    if it is already present the append is skipped. `create_props` is a page
    properties header (no leading dash) written only when the file is new.
    Returns the path, or None if skipped as a duplicate.
    """
    page = pages_dir() / filename
    page.parent.mkdir(parents=True, exist_ok=True)
    existing = page.read_text() if page.exists() else ""
    if marker and marker in existing:
        return None
    head = ""
    if not existing and create_props:
        head = create_props.rstrip("\n") + "\n"
    sep = "" if not existing or existing.endswith("\n") else "\n"
    with page.open("a") as f:
        f.write(head + sep + block + "\n")
    log(f"logseq filed to page={filename}")
    return page


def note(text: str, src_id: str) -> int:
    """Append a free-form `- <text>` note to today's journal (local-only).

    `src_id` is the entry/capture id used to build a grep-able idempotency
    marker so re-runs never duplicate the block. No-op while Logseq sync is
    frozen (`TODO_LOGSEQ_SYNC` unset); `cmd_note` now writes an Obsidian capture.
    """
    if not LOGSEQ_SYNC_ENABLED:
        return 0
    text = text.strip()
    if not text:
        return 0
    mk = f"<!-- note:{src_id} -->"
    journal = journal_path()
    existing = journal.read_text() if journal.exists() else ""
    if mk in existing:
        return 0
    append_lines([f"- {text} {mk}"])
    log(f"logseq note appended id={src_id} file={journal}")
    return 1


def append_journal_dedup(block: str, marker: str) -> bool:
    """Append a pre-formatted block to today's journal unless `marker` is present.

    Returns True if appended, False if the marker already existed (idempotent).
    No-op (returns False) while Logseq sync is frozen (`TODO_LOGSEQ_SYNC` unset).
    """
    if not LOGSEQ_SYNC_ENABLED:
        return False
    journal = journal_path()
    existing = journal.read_text() if journal.exists() else ""
    if marker and marker in existing:
        return False
    append_lines([block])
    return True


def sync_candidates(entries: list[TodoEntry]) -> list[TodoEntry]:
    """Open local-origin rows eligible for Logseq task blocks.

    Todoist-origin rows are a read-only backlog mirror. They stay out of the
    journal unless a future command deliberately promotes one into local work.
    """
    return [
        e
        for e in entries
        if e.status == "open" and e.sync.logseq is None and e.origin != "todoist"
    ]


def sync(entries: list[TodoEntry]) -> int:
    if not LOGSEQ_SYNC_ENABLED:
        return 0
    journal = journal_path()
    journal.parent.mkdir(parents=True, exist_ok=True)
    existing = journal.read_text() if journal.exists() else ""
    pending = sync_candidates(entries)
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
    # Outbound completion flush: flip any already-synced row that's now done.
    completed = complete(entries)
    print(f"logseq: appended {appended}, completed {completed} → {journal}")
    log(f"logseq sync appended={appended} completed={completed} file={journal}")
    return 0


def complete(entries: list[TodoEntry]) -> int:
    """Flip journal lines to DONE for rows completed locally (outbound leg).

    The Logseq half of "done here -> done there": for each `status == "done"`
    row that carries a Logseq marker, find the block(s) whose *trailing* marker
    is that row's marker and rewrite the leading `- TODO`/`- DOING`/... (or
    `- [ ]`) to `- DONE` (or `- [x]`). Idempotent — a block already DONE/`[x]`,
    or no longer a task line, is left untouched. Counts one flip per entry
    (matching `reconcile`'s per-entry view), not per line. Reads/writes with
    `newline=""` so untouched CRLF/mixed line endings survive verbatim.
    Returns the number of entries flipped. Silent: callers own the summary.
    No-op (returns 0) while Logseq sync is frozen (`TODO_LOGSEQ_SYNC` unset).
    """
    if not LOGSEQ_SYNC_ENABLED:
        return 0
    flipped = 0
    by_file: dict[str, list[TodoEntry]] = {}
    for e in entries:
        if e.status != "done" or e.sync.logseq is None:
            continue
        by_file.setdefault(e.sync.logseq.file, []).append(e)
    for path, batch in by_file.items():
        p = Path(path)
        if not p.exists():
            continue
        with p.open("r", newline="") as f:  # newline="" disables \r\n translation
            lines = f.read().splitlines(keepends=True)
        changed = False
        for e in batch:
            mk = e.sync.logseq.marker if e.sync.logseq else None
            if not mk:
                continue
            hit = False
            for i, ln in enumerate(lines):
                # Anchor to the line's OWN trailing marker so a marker quoted in
                # another task's body never flips the wrong block.
                if not ln.rstrip("\r\n").endswith(mk):
                    continue
                if _DONE_RE.match(ln) or _ARCHIVED_RE.match(ln):
                    continue  # already done — idempotent
                new = _OPEN_KW_RE.sub(r"\1DONE", ln, count=1)
                if new == ln:
                    new = _OPEN_BOX_RE.sub(r"\1[x]", ln, count=1)
                if new != ln:
                    lines[i] = new
                    changed = True
                    hit = True
            if hit:
                flipped += 1
        if changed:
            with p.open("w", newline="") as f:  # write verbatim, no translation
                f.write("".join(lines))
    if flipped:
        log(f"logseq complete flipped={flipped}")
    return flipped


def reconcile(entries: list[TodoEntry]) -> int:
    """Scan synced journal lines; if marker line begins with DONE, mark local done.

    Also detects Logseq's checkbox `- [x]` form. No-op (returns 0) while Logseq
    sync is frozen (`TODO_LOGSEQ_SYNC` unset).
    """
    if not LOGSEQ_SYNC_ENABLED:
        return 0
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
                # Deliberately do NOT stamp sync.todoist.closed_ts here: a task
                # completed in Logseq *should* propagate out to Todoist on the
                # next push (done here -> done there). If Todoist already had it
                # done, the close returns 404 and is treated as already-closed.
                flipped += 1
    print(
        f"logseq reconcile: checked {checked}, flipped {flipped}, missing {missing}"
    )
    log(
        f"logseq reconcile checked={checked} flipped={flipped} missing={missing}"
    )
    return 0
