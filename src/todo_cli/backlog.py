"""`todo backlog` — per-project pull across Obsidian + Todoist.

Surfaces, for one project, three groups in a single screen:

  - In flight : Todoist `Current Work` tasks labeled <project>
  - Planned   : Todoist Idea Cooker (Shaped/Board-ready) labeled <project>
                + Obsidian items with `status: shaped`
  - Backlog   : Obsidian `06 Backlog/` + `05 Notes/ideas/` items for <project>
                + Todoist Idea Cooker (Dreamer/Cooking) + Inbox labeled <project>

Read-only — it queries, never writes. Project identity IS the Todoist label
(canonical in todoist-structure.json). Obsidian association is exact when a
`project:` frontmatter key is present, else best-effort (tags / wikilink /
narrative line / filename) until that key is backfilled.

The cwd basename is the default project, so `todo backlog` run inside
~/Developer/proj/<name> just works. `--if-project` makes the whole thing a
silent no-op unless the cwd is a known project label (one JSON read, no
network) — safe to wire into a single global SessionStart hook.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass

from . import todoist
from .config import (
    OBSIDIAN_VAULT,
    idea_cooker_sections,
    project_role_ids,
    taxonomy_labels,
)
from .storage import load_all

PLANNED_STATUSES = {"shaped", "board-ready", "board_ready"}


@dataclass
class Item:
    title: str
    where: str           # store/lane, e.g. "ideas", "backlog", "current-work"
    status: str = ""     # raw status / heat / section, lowercased
    priority: str = ""   # high|med|low or ""
    ref: str = ""        # path or url
    match: str = ""      # how it matched: project:|tag|wikilink|prose|filename|label

    def to_json(self) -> dict[str, str]:
        return {
            "title": self.title,
            "where": self.where,
            "status": self.status,
            "priority": self.priority,
            "ref": self.ref,
            "match": self.match,
        }


# --- Obsidian side -----------------------------------------------------------

_FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_HEAT_RE = re.compile(r"\*\*Heat:\*\*\s*([A-Za-z—_-]+)")
_STATUS_STRIP_RE = re.compile(r"\*\*Status:\*\*\s*([A-Za-z—_-]+)")


def _parse_frontmatter(text: str) -> dict[str, str]:
    m = _FM_RE.match(text)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip()
    return fm


def _tags(fm: dict[str, str]) -> list[str]:
    raw = fm.get("tags", "").strip().strip("[]")
    return [t.strip() for t in raw.split(",") if t.strip()]


def _title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def _strip_field(text: str, regex: re.Pattern) -> str:
    m = regex.search(text)
    return m.group(1).strip() if m else ""


def _match_project(name: str, slug: str, fm: dict[str, str], body: str) -> str | None:
    """How (if at all) this note belongs to `name`, in priority order.

    A `project:` frontmatter key is AUTHORITATIVE: a note that declares its home
    matches only that project and never falls through to the fuzzy signals — so
    once an idea is `todo plan`'d, it stops matching unrelated projects.
    """
    nl = name.lower()
    declared = fm.get("project", "").strip().lower()
    if declared:
        return "project:" if declared == nl else None
    if nl in [t.lower() for t in _tags(fm)]:          # frontmatter tag
        return "tag"
    low = body.lower()
    if re.search(r"\[\[[^\]]*" + re.escape(nl) + r"[^\]]*\]\]", low):  # wikilink
        return "wikilink"
    for line in low.splitlines():                      # narrative "Projects:" line
        if "project" in line and nl in line:
            return "prose"
    if slug.lower() == nl or slug.lower().startswith(nl + "-"):       # filename
        return "filename"
    return None


def _scan_dir(dir_path, name: str, lane: str) -> list[Item]:
    items: list[Item] = []
    if not dir_path.is_dir():
        return items
    for p in sorted(dir_path.glob("*.md")):
        if p.name.startswith("_"):          # _index.md and friends
            continue
        try:
            text = p.read_text()
        except OSError:
            continue
        fm = _parse_frontmatter(text)
        match = _match_project(name, p.stem, fm, text)
        if not match:
            continue
        status = (fm.get("status", "") or _strip_field(text, _STATUS_STRIP_RE)).lower()
        if fm.get("executed", "").strip().lower() == "true":
            status = "done"
        heat = _strip_field(text, _HEAT_RE).lower()
        items.append(
            Item(
                title=_title(text, p.stem),
                where=lane,
                status=status or heat,
                priority=fm.get("priority", ""),
                ref=str(p),
                match=match,
            )
        )
    return items


def _obsidian_groups(name: str) -> tuple[list[Item], list[Item], list[Item]]:
    """Return (planned, backlog, done) from the vault's ideas + backlog folders."""
    notes = _scan_dir(OBSIDIAN_VAULT / "05 Notes" / "ideas", name, "ideas")
    notes += _scan_dir(OBSIDIAN_VAULT / "06 Backlog", name, "backlog")
    planned, backlog, done = [], [], []
    for it in notes:
        if it.status == "done":
            done.append(it)
        elif it.status in PLANNED_STATUSES:
            planned.append(it)
        else:
            backlog.append(it)
    return planned, backlog, done


def _obsidian_items(name: str) -> tuple[list[Item], list[Item]]:
    """Return (planned, backlog) from the vault's ideas + backlog folders."""
    planned, backlog, _done = _obsidian_groups(name)
    return planned, backlog


# --- Todoist side ------------------------------------------------------------


def _task_url(task: dict) -> str:
    tid = str(task.get("id", ""))
    return f"https://app.todoist.com/app/task/{tid}" if tid else ""


def _classify_live(tasks: list[dict], name: str, roles: dict, sections: dict):
    cw, ic, inbox = roles.get("current_work"), roles.get("idea_cooker"), roles.get("inbox")
    res, arch = roles.get("resource"), roles.get("archive")
    shaped = {sections.get("shaped"), sections.get("board_ready")} - {None}
    inflight, planned, ideas = [], [], []
    for t in tasks:
        labels = [str(x) for x in (t.get("labels") or [])]
        if name not in labels:
            continue
        pid, sid = t.get("project_id"), t.get("section_id")
        it = Item(title=t.get("content", ""), where="todoist", ref=_task_url(t), match="label")
        if pid in (res, arch):
            continue
        if pid == ic and sid in shaped:
            it.where, dest = "idea-cooker/shaped", planned
        elif pid == ic:
            it.where, dest = "idea-cooker", ideas
        elif pid == inbox:
            it.where, dest = "inbox", ideas
        else:                                   # Current Work or any other active project
            it.where, dest = ("current-work" if pid == cw else "todoist"), inflight
        dest.append(it)
    return inflight, planned, ideas


def _classify_mirror(name: str, roles: dict):
    """Offline path: classify the local Todoist mirror (~/.todo/todos.jsonl).

    Coarser than the live path — the mirror records a task's project but not its
    Idea Cooker section, so Idea Cooker items land in `planned` undifferentiated.
    """
    cw, ic, inbox = roles.get("current_work"), roles.get("idea_cooker"), roles.get("inbox")
    inflight, planned, ideas = [], [], []
    for e in load_all():
        if e.status != "open" or (e.project or "") != name:
            continue
        st = e.sync.todoist if e.sync else None
        pid = st.project_id if st else None
        url = st.url if st else ""
        it = Item(title=e.text, where="mirror", ref=url or "", match="label")
        if pid == ic:
            it.where, dest = "idea-cooker", planned
        elif pid == inbox:
            it.where, dest = "inbox", ideas
        else:                                   # Current Work or any other project
            it.where, dest = ("current-work" if pid == cw else "mirror"), inflight
        dest.append(it)
    return inflight, planned, ideas


def _todoist_items(name: str, offline: bool):
    """Return (inflight, planned, ideas, note)."""
    roles = project_role_ids()
    sections = idea_cooker_sections()
    if not offline:
        tok = todoist.token()
        if tok:
            try:
                tasks = todoist.list_active_tasks(tok)
            except Exception:  # noqa: BLE001 — any network/parse failure → mirror
                tasks = None
            if tasks is not None:
                inflight, planned, ideas = _classify_live(tasks, name, roles, sections)
                return inflight, planned, ideas, ""
            note = "todoist: live query failed — showing local mirror"
        else:
            note = "todoist: no token — showing local mirror (run `todo pull` to refresh)"
    else:
        note = ""
    inflight, planned, ideas = _classify_mirror(name, roles)
    return inflight, planned, ideas, note


# --- render ------------------------------------------------------------------


def _section(label: str, items: list[Item], *, skip_empty: bool) -> None:
    if not items and skip_empty:
        return
    print(f"\n{label}  ({len(items)})")
    if not items:
        print("  —")
        return
    for it in items:
        meta = " · ".join(x for x in (it.where, it.status, it.priority) if x)
        tail = f"  ⟨{it.match}⟩" if it.match and it.match != "label" else ""
        suffix = f"   ({meta})" if meta else ""
        print(f"  • {it.title}{suffix}{tail}")


def _render_json(
    name: str,
    inflight: list[Item],
    planned: list[Item],
    backlog: list[Item],
    done: list[Item],
    note: str,
) -> None:
    data = {
        "project": name,
        "in_flight": [it.to_json() for it in inflight],
        "planned": [it.to_json() for it in planned],
        "backlog": [it.to_json() for it in backlog],
        "done": [it.to_json() for it in done],
        "note": note,
    }
    print(json.dumps(data, sort_keys=True))


def run(
    name: str,
    *,
    if_project: bool = False,
    offline: bool = False,
    json_output: bool = False,
    history: bool = False,
) -> int:
    name = (name or "").strip()
    known = set(taxonomy_labels().get("projects", []))

    if if_project:
        # Near-free guard for a global SessionStart hook: silent unless the cwd
        # is a recognized project. Stay offline so session start never blocks.
        if name not in known:
            return 0
        offline = True

    planned_obs, backlog_obs, done_obs = _obsidian_groups(name)
    inflight, planned_tos, ideas_tos, note = _todoist_items(name, offline)

    planned = planned_tos + planned_obs
    backlog = backlog_obs + ideas_tos
    done = done_obs

    if if_project and not (inflight or planned or backlog or (history and done)):
        return 0  # known project but nothing to show → quiet, normal start

    if json_output:
        _render_json(name, inflight, planned, backlog, done, note)
        return 0

    header = (
        f"┃ {name}  —  Backlog: {len(backlog)} · "
        f"Planned: {len(planned)} · In flight: {len(inflight)}"
    )
    if history:
        header += f" · Done: {len(done)}"
    if not if_project and known and name not in known:
        header += "   (not a known project label — best-effort match)"
    print(header)

    _section("In flight", inflight, skip_empty=if_project)
    _section("Planned", planned, skip_empty=if_project)
    _section("Backlog / Ideas", backlog, skip_empty=if_project)
    if history:
        _section("Done / History", done, skip_empty=if_project)

    if note and not if_project:
        print(f"\n  {note}")
    return 0
