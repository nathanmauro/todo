"""Google Tasks outbound sync — the 2026-08-20 migration backend.

Captures push to the primary Google Tasks list ("Tasks"). Transport is the
authed `gws` CLI rather than raw REST so token/scope management lives in one
place (`gws auth login`). Selected via TODO_TASK_BACKEND=gtasks (config.py);
Todoist stays the default until cutover.

Outbound-only by design (phase 1): create + complete. The inbound mirror
stays Todoist-shaped or dark — see the cockpit spec
docs/superpowers/specs/2026-08-20-gtasks-migration-design.md.
"""
from __future__ import annotations

import json
import shutil
import subprocess

from .config import GTASKS_PRIMARY_LIST, GWS_BIN
from .models import GtasksSync, TodoEntry, now_iso
from .storage import log

GTASKS_URL = "https://tasks.google.com/"


class GtasksError(Exception):
    pass


def available() -> bool:
    return shutil.which(GWS_BIN) is not None


def _run(args: list[str]) -> dict:
    """Run one gws command, return parsed JSON; GtasksError on any failure."""
    cmd = [GWS_BIN, *args]
    try:
        result = subprocess.run(
            cmd, text=True, capture_output=True, check=False, timeout=15
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GtasksError(f"{GWS_BIN} unavailable: {exc}") from exc
    if result.returncode != 0:
        detail = " ".join((result.stderr or result.stdout).split())
        raise GtasksError(f"`{' '.join(cmd)}` failed (exit {result.returncode}): {detail}")
    try:
        return json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError as exc:
        raise GtasksError(f"gws returned non-JSON: {result.stdout[:200]}") from exc


_list_id_cache: str | None = None


def list_id(refresh: bool = False) -> str:
    """Resolve the primary list id by title (cached for the process lifetime)."""
    global _list_id_cache
    if _list_id_cache and not refresh:
        return _list_id_cache
    resp = _run(["tasks", "tasklists", "list", "--params", '{"maxResults": 100}'])
    for lst in resp.get("items", []):
        if lst.get("title") == GTASKS_PRIMARY_LIST:
            _list_id_cache = lst["id"]
            return _list_id_cache
    raise GtasksError(
        f"Google Tasks list {GTASKS_PRIMARY_LIST!r} not found — "
        "run cockpit-gtasks-migrate first or set TODO_GTASKS_LIST"
    )


def _rfc3339(due: str | None) -> str | None:
    if not due:
        return None
    date = due[:10]
    if len(date) == 10 and date[4] == "-" and date[7] == "-":
        return f"{date}T00:00:00.000Z"
    return None


def create_task(text: str, *, notes: str | None = None, due: str | None = None) -> dict:
    """Insert one task at the top of the primary list; returns the API task."""
    resource: dict = {"title": text}
    if notes:
        resource["notes"] = notes
    rfc = _rfc3339(due)
    if rfc:
        resource["due"] = rfc
    lid = list_id()
    task = _run([
        "tasks", "tasks", "insert",
        "--params", json.dumps({"tasklist": lid}),
        "--json", json.dumps(resource),
    ])
    task["_list_id"] = lid
    return task


def complete_task(lid: str, task_id: str) -> None:
    _run([
        "tasks", "tasks", "patch",
        "--params", json.dumps({"tasklist": lid, "task": task_id}),
        "--json", '{"status": "completed"}',
    ])


def stamp(entry: TodoEntry, task: dict) -> None:
    """Record a pushed task on the row so it is never re-pushed."""
    entry.sync.gtasks = GtasksSync(
        task_id=str(task.get("id", "")),
        list_id=str(task.get("_list_id", "")),
        url=task.get("selfLink") or GTASKS_URL,
        ts=now_iso(),
    )


def create_candidates(entries: list[TodoEntry]) -> list[TodoEntry]:
    """Open local-origin rows that have reached NEITHER backend.

    Rows already stamped `sync.todoist` are excluded on purpose: the historical
    Todoist corpus moves over once, via cockpit-gtasks-migrate, not per-row here.
    """
    return [
        e for e in entries
        if e.status == "open"
        and e.sync.gtasks is None
        and e.sync.todoist is None
        and e.origin != "todoist"
    ]


def sync(entries: list[TodoEntry], *, quiet: bool = False) -> int:
    """Push every eligible row (best-effort, per-row failures skipped)."""
    todo = create_candidates(entries)
    if not todo:
        if not quiet:
            print("gtasks: nothing to push")
        return 0
    pushed = failed = 0
    for e in todo:
        try:
            task = create_task(e.text, notes=f"source: {e.source}", due=e.due)
            stamp(e, task)
            pushed += 1
        except GtasksError as exc:
            failed += 1
            log(f"gtasks push failed for {e.short_id}: {exc}")
    if not quiet:
        print(f"gtasks: pushed {pushed}, failed {failed}")
    return 0 if failed == 0 else 1
