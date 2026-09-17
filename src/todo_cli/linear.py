"""Linear outbound backend — the 2026-09-17 Todoist / Google Tasks -> Linear migration.

Captures become Linear issues in team ``TODO_LINEAR_TEAM`` (default ``NAT``), project
``TODO_LINEAR_PROJECT`` (default ``Personal``) unless a project/alias is given, carrying
the ``capture`` label so the old Todoist "Inbox pile" survives as a label filter.
Transport is the Linear GraphQL API with a personal API key from the login keychain
(``security add-generic-password -a linear -s todo-cli -w '<key>'``) or
``TODO_LINEAR_API_KEY``.

Contract:
- FAIL-CLOSED: no key, unknown team/project/state, or any API error -> nothing is
  created, the local ``todos.jsonl`` row stays queued, ``todo sync``/``todo refresh``
  retries. Nothing here ever falls back to Todoist or Google Tasks.
- IDEMPOTENT: every issue body carries ``capture-id: <row id>``; before creating, the
  row's capture-id is looked up in Linear, so a lost response never yields a second
  issue on retry — the existing issue is adopted (stamped) instead.
- LOSSLESS: titles are capped at Linear's 255 chars but the full capture text and the
  original due value (including any time component, which Linear cannot store) are
  preserved in the description.
"""
from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request
import uuid
from pathlib import Path

from .config import (
    KEYCHAIN_SERVICE,
    LINEAR_API,
    LINEAR_CAPTURE_LABEL,
    LINEAR_DEFAULT_PROJECT,
    LINEAR_KEYCHAIN_ACCOUNT,
    LINEAR_TEAM_KEY,
)
from .models import LinearSync, TodoEntry, now_iso
from .storage import log

TITLE_MAX = 255
# Deterministic client-side issue id: uuid5(namespace, capture-id). IssueCreateInput.id is
# a supported client-supplied UUID, so a retry after a lost response (or two overlapping
# pushes of the same row) cannot mint a second issue — the second create is rejected by
# Linear and the existing issue is adopted by id.
CAPTURE_NAMESPACE = uuid.UUID("1f3c0b2a-6e8d-4a51-9c7b-2d4e6f8a0b1c")
# Todoist-style priorities -> Linear (0 none, 1 urgent, 2 high, 3 medium, 4 low)
PRIORITY_MAP = {"p1": 1, "p2": 2, "p3": 3, "p4": 0}
# cockpit-task-sync / cockpit-capture destinations -> workflow state type + extra label
DEST_MAP = {
    "inbox": ("unstarted", None),
    "intake": ("unstarted", None),
    "current": ("started", None),
    "work": ("started", None),
    "doing": ("started", None),
    "idea": ("backlog", "idea"),
    "ideas": ("backlog", "idea"),
    "dreamer": ("backlog", "idea"),
}
KEY_HINT = (
    "no Linear API key: create one at linear.app → Settings → Security & access → "
    "Personal API keys, then `security add-generic-password -a linear -s todo-cli -w '<key>'`"
)
ALIASES_PATH = Path(os.environ.get("TODO_LINEAR_PROJECT_ALIASES", Path(__file__).with_name("linear_projects.json")))


class LinearError(Exception):
    pass


class RoutingError(LinearError):
    """The capture names a project Linear does not have; keep it queued, never misfile."""


def token() -> str | None:
    env = os.environ.get("TODO_LINEAR_API_KEY")
    if env:
        return env
    try:
        r = subprocess.run(
            ["security", "find-generic-password", "-a", LINEAR_KEYCHAIN_ACCOUNT,
             "-s", KEYCHAIN_SERVICE, "-w"],
            capture_output=True, text=True, check=False,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except FileNotFoundError:
        pass
    return None


def available() -> bool:
    return token() is not None


def _graphql(query: str, variables: dict | None = None) -> dict:
    """POST one GraphQL document; return `data`. LinearError on any failure."""
    tok = token()
    if not tok:
        raise LinearError(KEY_HINT)
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        LINEAR_API, data=body,
        # Personal API keys are sent bare (no "Bearer"); OAuth tokens would use Bearer.
        headers={"Content-Type": "application/json", "Authorization": tok},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:300] if exc.fp else ""
        raise LinearError(f"Linear HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        raise LinearError(f"Linear unreachable: {exc}") from exc
    if not isinstance(payload, dict):
        raise LinearError("Linear returned a non-object response")
    if payload.get("errors"):
        raise LinearError("Linear GraphQL error: " + "; ".join(
            str(e.get("message", e)) for e in payload["errors"]))
    return payload.get("data") or {}


# --- id resolution (cached per process) --------------------------------------
_cache: dict[str, object] = {}


def reset_cache() -> None:
    _cache.clear()


def team_id() -> str:
    if "team" not in _cache:
        data = _graphql(
            "query($key:String!){ teams(filter:{key:{eq:$key}}){ nodes{ id key name } } }",
            {"key": LINEAR_TEAM_KEY},
        )
        nodes = ((data.get("teams") or {}).get("nodes")) or []
        if not nodes:
            raise LinearError(f"Linear team {LINEAR_TEAM_KEY!r} not found")
        _cache["team"] = nodes[0]["id"]
    return str(_cache["team"])


def _states() -> list[dict]:
    if "states" not in _cache:
        data = _graphql(
            "query($id:String!){ team(id:$id){ states{ nodes{ id name type } } } }",
            {"id": team_id()},
        )
        _cache["states"] = (((data.get("team") or {}).get("states") or {}).get("nodes")) or []
    return list(_cache["states"])  # type: ignore[arg-type]


def state_id(state_type: str) -> str:
    for s in _states():
        if s.get("type") == state_type:
            return s["id"]
    raise LinearError(f"Linear team has no workflow state of type {state_type!r}")


def _projects() -> list[dict]:
    if "projects" not in _cache:
        data = _graphql(
            "query($id:String!){ team(id:$id){ projects(first:100){ nodes{ id name } } } }",
            {"id": team_id()},
        )
        _cache["projects"] = (((data.get("team") or {}).get("projects") or {}).get("nodes")) or []
    return list(_cache["projects"])  # type: ignore[arg-type]


def _aliases() -> dict[str, str]:
    if "aliases" not in _cache:
        try:
            raw = json.loads(ALIASES_PATH.read_text())
        except (OSError, ValueError):
            raw = {}
        _cache["aliases"] = {str(k).lower(): str(v) for k, v in raw.items() if not str(k).startswith("_")}
    return dict(_cache["aliases"])  # type: ignore[arg-type]


def resolve_project(name: str | None) -> tuple[str, str]:
    """Map a capture's project tag (repo slug, area, or Linear name) to (id, Linear name).

    Resolution: exact Linear project name (case-insensitive) -> alias table
    (linear_projects.json) -> RoutingError. `None` means the default project, and a
    missing default is an error too: nothing is ever filed without a project.
    """
    want = (name or LINEAR_DEFAULT_PROJECT).strip()
    by_name = {str(p.get("name", "")).lower(): p for p in _projects()}
    hit = by_name.get(want.lower())
    if hit is None:
        alias = _aliases().get(want.lower())
        if alias:
            hit = by_name.get(alias.lower())
    if hit is None:
        raise RoutingError(
            f"Linear project {want!r} not found (no exact name or alias in {ALIASES_PATH.name}); "
            "capture kept queued — add the project/alias or re-run with an existing project"
        )
    return hit["id"], str(hit["name"])


def label_ids(names: list[str]) -> list[str]:
    if "labels" not in _cache:
        data = _graphql("query{ issueLabels(first:250){ nodes{ id name } } }")
        _cache["labels"] = ((data.get("issueLabels") or {}).get("nodes")) or []
    by_name = {str(l.get("name", "")).lower(): l["id"] for l in _cache["labels"]}  # type: ignore[union-attr]
    return [by_name[n.lower()] for n in names if n and n.lower() in by_name]


def _due_date(due: str | None) -> str | None:
    if not due:
        return None
    date = due[:10]
    if len(date) == 10 and date[4] == "-" and date[7] == "-":
        return date
    return None


def issue_uuid(capture_id: str) -> str:
    return str(uuid.uuid5(CAPTURE_NAMESPACE, capture_id))


def _issue_by_id(issue_id: str) -> dict | None:
    """{id, identifier, url} for an existing issue id, None when Linear has no such entity."""
    try:
        data = _graphql("query($id:String!){ issue(id:$id){ id identifier url } }", {"id": issue_id})
    except LinearError as exc:
        if "not found" in str(exc).lower() or "entity" in str(exc).lower():
            return None
        raise
    node = data.get("issue")
    return dict(node) if node else None


def find_existing(capture_id: str) -> dict | None:
    """The issue this capture already became, if any: by deterministic id, then by capture-id text."""
    hit = _issue_by_id(issue_uuid(capture_id))
    if hit:
        return hit
    return find_by_capture_id(capture_id)


def find_by_capture_id(capture_id: str) -> dict | None:
    """Return {id, identifier, url} of an issue already carrying this capture-id, if any."""
    data = _graphql(
        "query($needle:String!){ issues(first:5, filter:{description:{contains:$needle}}){ nodes{ id identifier url } } }",
        {"needle": f"capture-id: {capture_id}"},
    )
    nodes = ((data.get("issues") or {}).get("nodes")) or []
    return dict(nodes[0]) if nodes else None


def build_issue_input(
    text: str,
    *,
    capture_id: str,
    notes: str | None = None,
    due: str | None = None,
    source: str = "cli",
    project: str | None = None,
    priority: str | None = None,
    dest: str | None = None,
) -> tuple[dict, str]:
    """Assemble the IssueCreateInput for a capture; returns (input, resolved project name)."""
    state_type, extra_label = DEST_MAP.get((dest or "inbox").lower(), ("unstarted", None))
    labels = [LINEAR_CAPTURE_LABEL] + ([extra_label] if extra_label else [])
    pid, pname = resolve_project(project)
    text = text.strip()
    title = text if len(text) <= TITLE_MAX else text[: TITLE_MAX - 1].rstrip() + "…"
    body: list[str] = []
    if len(text) > TITLE_MAX or "\n" in text:
        body.append("Full original capture:\n\n" + "\n".join(f"> {ln}" for ln in text.splitlines()))
    if notes:
        body.append(notes.strip())
    due_date = _due_date(due)
    if due and due != due_date:
        body.append(
            f"**Due (source):** `{due}` — Linear due dates are date-only; the time component "
            "is not carried and no Linear reminder was set."
        )
    elif due and not due_date:
        body.append(f"**Due (source, unparsed):** `{due}` — not an ISO date; no Linear due date set.")
    body.append(f"---\n_Captured via todo ({source}) at {now_iso()} · capture-id: {capture_id}_")
    inp: dict = {
        "id": issue_uuid(capture_id),
        "teamId": team_id(),
        "title": title,
        "description": "\n\n".join(body),
        "projectId": pid,
        "stateId": state_id(state_type),
        "labelIds": label_ids(labels),
        "priority": PRIORITY_MAP.get((priority or "p4").lower(), 0),
    }
    if due_date:
        inp["dueDate"] = due_date
    return inp, pname


def create_issue(text: str, *, capture_id: str, **kwargs) -> dict:
    """Idempotently create one issue; returns {id, identifier, url, _project, _adopted}.

    Order: lookup (deterministic id, then capture-id text) -> create with the
    deterministic id -> on a create error, re-check by id and adopt if Linear already
    holds it (the overlapping-writer / lost-response case).
    """
    existing = find_existing(capture_id)
    if existing:
        existing["_project"] = None
        existing["_adopted"] = True
        return existing
    inp, pname = build_issue_input(text, capture_id=capture_id, **kwargs)
    try:
        data = _graphql(
            "mutation($input:IssueCreateInput!){ issueCreate(input:$input){ success issue{ id identifier url } } }",
            {"input": inp},
        )
    except LinearError:
        raced = _issue_by_id(inp["id"])
        if raced:
            raced["_project"] = pname
            raced["_adopted"] = True
            return raced
        raise
    res = (data.get("issueCreate") or {})
    if not res.get("success") or not res.get("issue"):
        raise LinearError(f"issueCreate failed: {json.dumps(res)[:200]}")
    issue = dict(res["issue"])
    issue["_project"] = pname
    issue["_adopted"] = False
    return issue


def complete_issue(issue_ref: str) -> None:
    """Move an issue (uuid or identifier like NAT-12) to the team's completed state."""
    data = _graphql(
        "mutation($id:String!,$input:IssueUpdateInput!){ issueUpdate(id:$id,input:$input){ success } }",
        {"id": issue_ref, "input": {"stateId": state_id("completed")}},
    )
    if not (data.get("issueUpdate") or {}).get("success"):
        raise LinearError(f"issueUpdate(complete) failed for {issue_ref}")


def stamp(entry: TodoEntry, issue: dict) -> None:
    """Record the created/adopted issue on the row so it is never re-pushed."""
    entry.sync.linear = LinearSync(
        issue_id=str(issue.get("id", "")),
        identifier=str(issue.get("identifier", "")),
        url=issue.get("url"),
        ts=now_iso(),
    )


def push_entry(entry: TodoEntry) -> dict:
    """Create (or adopt) the Linear issue for one local row and stamp it."""
    issue = create_issue(
        entry.text, capture_id=entry.id, notes=entry.notes, due=entry.due, source=entry.source,
        project=entry.project, priority=entry.priority, dest=entry.dest,
    )
    stamp(entry, issue)
    return issue


def create_candidates(entries: list[TodoEntry]) -> list[TodoEntry]:
    """Open local-origin rows that reached NO backend yet.

    Rows already stamped `sync.todoist` / `sync.gtasks` are excluded: the historical
    corpus moved to Linear once, via cockpit-linear-migrate, never per-row here.
    """
    return [
        e for e in entries
        if e.status == "open"
        and e.sync.linear is None
        and e.sync.todoist is None
        and e.sync.gtasks is None
        and e.origin != "todoist"
    ]


def completion_candidates(entries: list[TodoEntry]) -> list[TodoEntry]:
    """Done rows whose Linear issue has not been closed yet."""
    return [
        e for e in entries
        if e.status == "done" and e.sync.linear is not None and e.sync.linear.closed_ts is None
    ]


def push_completions(entries: list[TodoEntry]) -> tuple[int, int]:
    """Close the Linear issue for each candidate; returns (closed, failed). Best-effort."""
    closed = failed = 0
    for e in completion_candidates(entries):
        try:
            complete_issue(e.sync.linear.issue_id)  # type: ignore[union-attr]
            e.sync.linear.closed_ts = now_iso()  # type: ignore[union-attr]
            closed += 1
        except LinearError as exc:
            failed += 1
            log(f"linear complete failed for {e.short_id}: {exc}")
    return closed, failed


def sync(entries: list[TodoEntry], *, quiet: bool = False) -> int:
    """Push eligible creates and pending completions (best-effort, per-row failures skipped)."""
    todo = create_candidates(entries)
    pending_close = completion_candidates(entries)
    if not todo and not pending_close:
        if not quiet:
            print("linear: nothing to push")
        return 0
    if not available():
        log(f"linear: {len(todo)} row(s) queued locally — {KEY_HINT}")
        if not quiet:
            print(f"linear: {len(todo)} queued locally, 0 pushed — {KEY_HINT}")
        return 1
    pushed = adopted = failed = 0
    for e in todo:
        try:
            issue = push_entry(e)
            if issue.get("_adopted"):
                adopted += 1
            else:
                pushed += 1
        except RoutingError as exc:
            failed += 1
            log(f"linear routing error for {e.short_id} (project={e.project!r}): {exc}")
        except LinearError as exc:
            failed += 1
            log(f"linear push failed for {e.short_id}: {exc}")
    closed, cfailed = push_completions(entries)
    failed += cfailed
    if not quiet:
        print(f"linear: pushed {pushed}, adopted {adopted}, closed {closed}, failed {failed}")
    return 0 if failed == 0 else 1
