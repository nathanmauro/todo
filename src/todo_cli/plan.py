"""`todo plan` — graduate an idea into a project-homed plan (the plan gate).

The idea→plan→implement middle stage. "Planning" an idea stamps its note with a
`project:` (the Todoist label) and bumps it to `status: shaped` — in place, in
`05 Notes/ideas/`. No new store: a plan IS an idea that earned a home and a
shaped status. `todo backlog <project>` then surfaces it under Planned, and the
`project:` key makes the match exact (no more fuzzy substring hits).

Mutation is surgical: only the `status`/`project` frontmatter keys and the
`**Status:**` strip change; the id, tags, body, and everything else are
preserved byte-for-byte. `--dry-run` previews without writing.
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote_plus

from .config import OBSIDIAN_VAULT, taxonomy_labels
from .models import now_iso

SHAPED = "shaped"

# Frontmatter block: opening fence, body (non-greedy), closing fence. Anchored
# at the very start of the file so only the real frontmatter is touched.
_FM_RE = re.compile(r"^(---\n)(.*?)(\n---\n)", re.DOTALL)
# The one-line status strip, e.g. "**Status:** Cooking · **Heat:** Hot · …".
# Anchored to the START of a line (MULTILINE) so a mid-prose or in-code-fence
# mention of "**Status:**" is never matched; only the leading strip line is.
_STATUS_STRIP_RE = re.compile(r"(^[ \t]*\*\*Status:\*\*[ \t]*)([^\s·]+)", re.MULTILINE)


def ideas_dir():
    return OBSIDIAN_VAULT / "05 Notes" / "ideas"


def backlog_dir():
    return OBSIDIAN_VAULT / "06 Backlog"


def execution_plan_path(plan_id: str):
    return backlog_dir() / f"{plan_id}.md"


def execution_plan_index_path():
    return backlog_dir() / "_index.md"


def drive_lookup_url(query: str) -> str:
    return "https://drive.google.com/drive/search?q=" + quote_plus(query)


def _render_frontmatter(fields: dict[str, object]) -> str:
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, list):
            lines.append(f"{key}: [{', '.join(str(item) for item in value)}]")
        elif value is None:
            lines.append(f"{key}:")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def _split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip().splitlines()
    body = text[end + len("\n---") :].lstrip("\n")
    fields: dict[str, str] = {}
    for line in raw:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields, body


def _update_frontmatter(text: str, updates: dict[str, object]) -> str:
    fields, body = _split_frontmatter(text)
    ordered: dict[str, object] = {}
    for key in fields:
        ordered[key] = fields[key]
    for key, value in updates.items():
        ordered[key] = value
    return _render_frontmatter(ordered) + "\n\n" + body.lstrip("\n")


def _read_plan_text(plan_file: str | None, summary: str) -> str:
    if not plan_file:
        return summary.strip()
    if plan_file == "-":
        return sys.stdin.read().strip()
    return Path(plan_file).read_text(encoding="utf-8").strip()


def _ensure_execution_index_link(plan_id: str, priority: str, summary: str) -> None:
    path = execution_plan_index_path()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            _render_frontmatter(
                {
                    "id": "backlog-index",
                    "created": now_iso(),
                    "source": "todo",
                    "type": "backlog",
                    "status": "open",
                    "tags": ["system", "backlog"],
                }
            )
            + "\n\n# Backlog\n\n## Items\n\n",
            encoding="utf-8",
        )
    text = path.read_text(encoding="utf-8")
    needle = f"[[{plan_id}]]"
    if needle in text:
        return
    line = f"- [[{plan_id}]] - `{priority}` - {summary.strip() or plan_id}.\n"
    if "\n## Items\n" in text:
        text = text.rstrip() + "\n" + line
    else:
        text = text.rstrip() + "\n\n## Items\n\n" + line
    path.write_text(text, encoding="utf-8")


def _mark_execution_index_done(plan_id: str, executed_at: str) -> None:
    path = execution_plan_index_path()
    if not path.exists():
        return
    date = executed_at[:10]
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    for line in lines:
        if f"[[{plan_id}]]" in line:
            line = re.sub(r" \(executed \d{4}-\d{2}-\d{2}\)", "", line)
            line = f"{line} (executed {date})"
        out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def _atomic_write(path, text: str) -> None:
    """Write via a temp file + os.replace so an interrupt or a Drive-sync grab
    mid-write can never leave a truncated idea note. UTF-8 pinned (the store has
    em-dashes/arrows; the locale default must not decide the encoding)."""
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".plan-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def create_execution_plan(
    *,
    plan_id: str,
    title: str,
    summary: str,
    project: str,
    priority: str = "med",
    source: str = "codex",
    created: str | None = None,
    tags: list[str] | None = None,
    google_drive_url: str = "pending",
    drive_query: str | None = None,
    plan_file: str | None = None,
    force: bool = False,
) -> int:
    path = execution_plan_path(plan_id)
    if path.exists() and not force:
        print(f"plan already exists: {path}", file=sys.stderr)
        return 1

    path.parent.mkdir(parents=True, exist_ok=True)
    query = drive_query or title
    lookup_url = drive_lookup_url(query)
    plan_text = _read_plan_text(plan_file, summary)
    fields = {
        "id": plan_id,
        "created": created or now_iso(),
        "source": source,
        "type": "plan",
        "status": "shaped",
        "executed": False,
        "executed_at": None,
        "priority": priority,
        "project": project,
        "google_drive_url": google_drive_url,
        "drive_lookup_url": lookup_url,
        "drive_lookup_status": "lookup-url-created",
        "tags": tags or [],
    }
    body = f"""# {title}

## Plan status

- Executed: no
- Google Drive direct URL: {google_drive_url}
- Google Drive lookup: {lookup_url}

## Plan

{plan_text}

## Execution log

- Pending execution.
"""
    _atomic_write(path, _render_frontmatter(fields) + "\n\n" + body)
    _ensure_execution_index_link(plan_id, priority, summary)
    print(path)
    return 0


def execute_plan(
    plan_id: str,
    *,
    summary: str,
    executed_at: str | None = None,
    google_drive_url: str | None = None,
) -> int:
    path = execution_plan_path(plan_id)
    if not path.exists():
        print(f"missing plan: {path}", file=sys.stderr)
        return 1

    timestamp = executed_at or now_iso()
    text = path.read_text(encoding="utf-8")
    updates: dict[str, object] = {
        "status": "done",
        "executed": True,
        "executed_at": timestamp,
    }
    if google_drive_url:
        updates["google_drive_url"] = google_drive_url
        updates["drive_lookup_status"] = "resolved"
    text = _update_frontmatter(text, updates)
    text = text.replace("- Executed: no\n", "- Executed: yes\n", 1)
    if google_drive_url:
        text = re.sub(
            r"- Google Drive direct URL: .*\n",
            f"- Google Drive direct URL: {google_drive_url}\n",
            text,
            count=1,
        )
    marker = "\n## Execution log\n"
    entry = f"\n### {timestamp}\n\n- Executed: yes\n- Summary: {summary}\n"
    if f"### {timestamp}" not in text:
        if marker in text:
            text = text.replace("- Pending execution.\n", "", 1)
            text = text.rstrip() + entry
        else:
            text = text.rstrip() + "\n\n## Execution log\n" + entry.lstrip()
    _atomic_write(path, text.rstrip() + "\n")
    _mark_execution_index_done(plan_id, timestamp)
    print(path)
    return 0


def execution_plan_status(plan_id: str) -> int:
    path = execution_plan_path(plan_id)
    if not path.exists():
        print(f"missing plan: {path}", file=sys.stderr)
        return 1
    fields, _ = _split_frontmatter(path.read_text(encoding="utf-8"))
    print(f"path: {path}")
    print(f"status: {fields.get('status', '')}")
    print(f"executed: {fields.get('executed', '')}")
    print(f"executed_at: {fields.get('executed_at', '')}")
    print(f"drive_lookup_url: {fields.get('drive_lookup_url', '')}")
    print(f"google_drive_url: {fields.get('google_drive_url', '')}")
    return 0


def _title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _find_idea(query: str):
    """Resolve a query to a single idea file. Returns (path|None, candidates)."""
    d = ideas_dir()
    if not d.is_dir():
        return None, []
    q = query.strip().lower()
    files = [p for p in sorted(d.glob("*.md")) if not p.name.startswith("_")]
    # 1. exact stem, or stem with the conventional `idea-` prefix
    for p in files:
        if p.stem.lower() in (q, f"idea-{q}"):
            return p, [p]
    # 2. substring of the slug or the H1 title
    matches = []
    for p in files:
        try:
            title = _title(p.read_text(errors="replace"), p.stem).lower()
        except OSError:
            continue
        if q in p.stem.lower() or q in title:
            matches.append(p)
    return (matches[0], matches) if len(matches) == 1 else (None, matches)


def _set_fm_key(fm_body: str, key: str, value: str) -> str:
    """Replace `key:`'s value in the frontmatter body, or append the key."""
    pat = re.compile(rf"^{re.escape(key)}\s*:")
    out, found = [], False
    for line in fm_body.split("\n"):
        if pat.match(line):
            out.append(f"{key}: {value}")
            found = True
        else:
            out.append(line)
    if not found:
        out.append(f"{key}: {value}")
    return "\n".join(out)


def shape(query: str, project: str, *, dry_run: bool = False) -> int:
    project = (project or "").strip()
    if not project:
        print("todo plan: --project is required (a plan must have a home)")
        return 2

    path, candidates = _find_idea(query)
    if path is None:
        if candidates:
            print(f"todo plan: '{query}' is ambiguous — matches:")
            for c in candidates:
                print(f"  - {c.stem}")
        else:
            print(f"todo plan: no idea matches '{query}' in {ideas_dir()}")
        return 1

    text = path.read_text(encoding="utf-8")
    m = _FM_RE.match(text)
    if not m:
        print(f"todo plan: {path.name} has no frontmatter block to stamp")
        return 1

    new_fm = m.group(1) + _set_fm_key(_set_fm_key(m.group(2), "status", SHAPED), "project", project) + m.group(3)
    body = text[m.end():]
    # count=1: only the leading status strip, never a later occurrence.
    new_body, strip_hits = _STATUS_STRIP_RE.subn(r"\g<1>Shaped", body, count=1)
    new_text = new_fm + new_body

    title = _title(text, path.stem)
    known = set(taxonomy_labels().get("projects", []))
    unknown = f"   (note: '{project}' isn't a known project label yet)" if known and project not in known else ""

    if dry_run:
        print(f"todo plan (dry-run): would shape '{title}'{unknown}")
        print(f"  → frontmatter: status: shaped · project: {project}")
        print(f"  → status strip: {'updated to Shaped' if strip_hits else '(none found — frontmatter only)'}")
        print(f"  → {path}")
        return 0

    if new_text == text:
        print(f"already planned: '{title}' (project: {project}, status: shaped)")
        return 0

    _atomic_write(path, new_text)
    print(f"planned: '{title}'  → project: {project} · status: shaped{unknown}")
    print(f"  {path}")
    print(f"  see it: todo backlog {project}")
    return 0
