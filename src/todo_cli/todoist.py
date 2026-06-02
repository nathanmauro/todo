"""Todoist API v1 sync + reconcile."""
from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request

from .config import (
    KEYCHAIN_SERVICE,
    TODOIST_API,
    TODOIST_PROJECT_ID,
    mirror_policy,
    taxonomy_labels,
)
from .models import TodoistSync, TodoEntry, now_iso
from .storage import log

KEYCHAIN_ACCOUNT = "todoist"


def token() -> str | None:
    env = os.environ.get("TODOIST_TOKEN")
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


def _headers(tok: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {tok}",
        "Content-Type": "application/json",
    }


def ensure_label(tok: str, name: str) -> None:
    """Create the label if it does not exist (dynamic project tags).

    Best-effort: any API hiccup is swallowed so capture never fails on this.
    """
    try:
        req = urllib.request.Request(
            f"{TODOIST_API}/labels?limit=200",
            method="GET",
            headers={"Authorization": f"Bearer {tok}"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        rows = data.get("results", data) if isinstance(data, dict) else data
        if any(l["name"] == name for l in rows):
            return
        create = urllib.request.Request(
            f"{TODOIST_API}/labels",
            data=json.dumps({"name": name}).encode(),
            method="POST",
            headers=_headers(tok),
        )
        urllib.request.urlopen(create, timeout=15)
    except (urllib.error.URLError, urllib.error.HTTPError):
        pass


def create_task(
    tok: str,
    text: str,
    project_id: str | None = None,
    labels: list[str] | None = None,
    due_string: str | None = None,
) -> dict:
    body: dict = {"content": text}
    if project_id:
        body["project_id"] = project_id
    if labels:
        body["labels"] = labels
    if due_string:
        body["due_string"] = due_string
    req = urllib.request.Request(
        f"{TODOIST_API}/tasks",
        data=json.dumps(body).encode(),
        method="POST",
        headers=_headers(tok),
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def fetch_task(tok: str, task_id: str) -> dict:
    req = urllib.request.Request(
        f"{TODOIST_API}/tasks/{task_id}",
        method="GET",
        headers={"Authorization": f"Bearer {tok}"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def complete_task(tok: str, task_id: str) -> None:
    """Close a task in Todoist (POST /tasks/{id}/close → 204).

    For a non-recurring task close == done. For a recurring task close
    completes the *current occurrence* and advances the due date (the task
    stays active); `mirror` then reopens the local row on the next pull, so a
    recurring task tracks Todoist's next occurrence. Raises on HTTP/network
    error so the caller decides whether a 404 (already gone) counts as success.
    """
    req = urllib.request.Request(
        f"{TODOIST_API}/tasks/{task_id}/close",
        data=b"",
        method="POST",
        headers=_headers(tok),
    )
    urllib.request.urlopen(req, timeout=15)


def create_candidates(entries: list[TodoEntry]) -> list[TodoEntry]:
    """Open local-origin rows eligible to be created in Todoist."""
    return [
        e
        for e in entries
        if e.status == "open"
        and e.sync.todoist is None
        and e.origin != "todoist"
    ]


def completion_candidates(entries: list[TodoEntry]) -> list[TodoEntry]:
    """Done rows with a remote task that still need a close pushed."""
    return [
        e
        for e in entries
        if e.status == "done"
        and e.sync.todoist is not None
        and e.sync.todoist.task_id
        and not e.sync.todoist.closed_ts
    ]


def sync(entries: list[TodoEntry]) -> int:
    tok = token()
    if not tok:
        print(
            "todoist: no token. store one:\n"
            "  security add-generic-password -a todoist -s todo-cli -w '<token>'\n"
            "  (get from https://app.todoist.com/app/settings/integrations/developer)"
        )
        return 1
    # Never re-push a row that was mirrored in from Todoist. (Imported rows
    # already carry a task_id, so `sync.todoist is None` excludes them too;
    # the origin check is explicit defense against an echo loop.)
    pending = create_candidates(entries)

    ensured: set[str] = set()
    created = 0
    failed = 0
    for e in pending:
        project_id = TODOIST_PROJECT_ID
        labels = []

        if e.source:
            labels.append(e.source)

        # Project association is a label now (Inbox/Current Work have no sections).
        # Auto-create the label so starting a new project just works.
        if e.project:
            labels.append(e.project)
            if e.project not in ensured:
                ensure_label(tok, e.project)
                ensured.add(e.project)

        try:
            task = create_task(
                tok,
                e.text,
                project_id=project_id,
                labels=labels if labels else None,
                due_string=e.due,
            )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode(errors="replace")
            print(f"todoist: {e.short_id} FAIL {exc.code} {body[:200]}")
            log(f"todoist fail id={e.id} code={exc.code} body={body[:500]}")
            failed += 1
            continue
        except OSError as exc:
            # URLError, socket timeout, connection reset — all OSError. Skip
            # this row; created rows already stamped still get written.
            print(f"todoist: {e.short_id} network error: {exc}")
            failed += 1
            continue

        task_id = str(task.get("id", ""))
        e.sync.todoist = TodoistSync(
            task_id=task_id,
            url=f"https://app.todoist.com/app/task/{task_id}",
            ts=now_iso(),
        )
        created += 1

    # Outbound completion flush: close anything done locally but still open in
    # Todoist (offline `done`s, failed inline pushes). This is what makes
    # `todo sync` the catch-up for "done here -> done there".
    closed, close_failed = push_completions(entries, tok)

    if created == 0 and closed == 0 and failed == 0 and close_failed == 0:
        print("todoist: nothing to sync")
        return 0

    print(f"todoist: created {created}, closed {closed}, failed {failed}")
    log(
        f"todoist sync created={created} closed={closed} "
        f"failed={failed} close_failed={close_failed}"
    )
    return 0 if (failed + close_failed) == 0 else 1


def push_completions(
    entries: list[TodoEntry], tok: str | None = None
) -> tuple[int, int]:
    """Close in Todoist every locally-completed row not yet closed there.

    The outbound completion leg of "done here -> done there": acts on rows that
    are `status == "done"`, carry a `task_id`, and have no `closed_ts` yet
    (rows flipped done *by* Todoist via reconcile/mirror are already stamped, so
    they're skipped — no echo). A 404 means the task is already gone, which is
    success. Network/HTTP errors leave `closed_ts` unset so the next sync
    retries. Returns (closed, failed). Silent: callers own the summary line.
    """
    tok = tok or token()
    if not tok:
        return (0, 0)
    closed = 0
    failed = 0
    for e in entries:
        if e.status != "done":
            continue
        st = e.sync.todoist
        if not st or not st.task_id or st.closed_ts:
            continue
        try:
            complete_task(tok, st.task_id)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                st.closed_ts = now_iso()
                closed += 1
                continue
            print(f"todoist: close {e.short_id} FAIL {exc.code}")
            log(f"todoist close fail id={e.id} code={exc.code}")
            failed += 1
            continue
        except OSError as exc:
            # URLError, socket timeout (TimeoutError), connection reset — all
            # OSError subclasses. Leave closed_ts unset so the next sync
            # retries; crucially, never let this escape and abort the caller's
            # write_all (which would lose the local completion).
            log(f"todoist close net err id={e.id} {exc}")
            failed += 1
            continue
        st.closed_ts = now_iso()
        closed += 1
    return (closed, failed)


def reconcile(entries: list[TodoEntry]) -> int:
    tok = token()
    if not tok:
        print("todoist: no token; skipping reconcile")
        return 1
    checked = 0
    flipped = 0
    failed = 0
    for e in entries:
        if e.sync.todoist is None or e.status != "open":
            continue
        task_id = e.sync.todoist.task_id
        if not task_id:
            continue
        checked += 1
        try:
            task = fetch_task(tok, task_id)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                e.status = "done"
                e.done_ts = now_iso()
                e.done_source = "todoist"
                e.sync.todoist.closed_ts = now_iso()  # already closed there
                flipped += 1
                continue
            print(f"todoist: {e.short_id} FAIL {exc.code}")
            failed += 1
            continue
        except urllib.error.URLError as exc:
            print(f"todoist: {e.short_id} network error {exc}")
            failed += 1
            continue
        if task.get("checked"):
            e.status = "done"
            e.done_ts = now_iso()
            e.done_source = "todoist"
            e.sync.todoist.closed_ts = now_iso()  # already closed there
            flipped += 1

    print(
        f"todoist reconcile: checked {checked}, flipped {flipped}, "
        f"failed {failed}"
    )
    log(
        f"todoist reconcile checked={checked} flipped={flipped} failed={failed}"
    )
    return 0 if failed == 0 else 1


# --- inbound mirror (Todoist -> local) ---------------------------------------


def _get(tok: str, path: str) -> dict | list:
    req = urllib.request.Request(
        f"{TODOIST_API}{path}",
        method="GET",
        headers={"Authorization": f"Bearer {tok}"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def _get_paginated(tok: str, base: str) -> list[dict]:
    """Walk a v1 list endpoint's {results, next_cursor} pages into one list."""
    out: list[dict] = []
    cursor: str | None = None
    sep = "&" if "?" in base else "?"
    while True:
        path = base
        if cursor:
            path = f"{base}{sep}cursor={urllib.parse.quote(cursor)}"
        data = _get(tok, path)
        if isinstance(data, dict):
            out.extend(data.get("results", []))
            cursor = data.get("next_cursor")
        else:
            out.extend(data)
            cursor = None
        if not cursor:
            return out


def list_projects(tok: str) -> list[dict]:
    return _get_paginated(tok, "/projects?limit=200")


def list_active_tasks(tok: str) -> list[dict]:
    """All active (unchecked) tasks across the account, paginated."""
    return _get_paginated(tok, "/tasks?limit=200")


def _due_str(due: object) -> str | None:
    if not due:
        return None
    if isinstance(due, dict):
        return due.get("date") or due.get("string")
    return str(due)


def _first_in(labels: list[str], known: set[str]) -> str | None:
    for label in labels:
        if label in known:
            return label
    return None


def _included_project_ids(projects: list[dict], policy: dict) -> set[str]:
    excluded = set(policy["exclude_project_ids"])
    out: set[str] = set()
    for p in projects:
        if p.get("is_deleted") or p.get("is_archived"):
            continue
        if policy["exclude_shared"] and p.get("is_shared"):
            continue
        if p["id"] in excluded:
            continue
        out.add(p["id"])
    return out


def mirror(entries: list[TodoEntry], *, dry_run: bool = False) -> int:
    """Mirror in-scope Todoist tasks into the local store.

    Todoist is the source of truth: new remote tasks are imported as
    `origin="todoist"` rows; existing rows (matched by task_id) get their
    text/due/project refreshed; mirrored rows whose task vanished from the
    active set are flipped to done. Because Todoist owns mirrored rows, a
    mirrored row that is `done` locally but reappears in the active set
    (un-completed on web/phone, or a recurring occurrence that advanced) is
    reopened to track Todoist. Status of *locally-originated* rows is left to
    `sync`/`reconcile`/`done` — this never reopens a locally-done task.
    """
    tok = token()
    if not tok:
        print("todoist: no token; skipping pull")
        return 1

    policy = mirror_policy()
    tax = taxonomy_labels()
    src_labels = set(tax["source"])
    proj_labels = set(tax["projects"])

    try:
        included = _included_project_ids(list_projects(tok), policy)
        tasks = [
            t
            for t in list_active_tasks(tok)
            if t.get("project_id") in included and not t.get("is_deleted")
        ]
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        print(f"todoist pull: list failed: {exc}")
        return 1

    by_task = {
        e.sync.todoist.task_id: e
        for e in entries
        if e.sync.todoist and e.sync.todoist.task_id
    }
    seen: set[str] = set()
    created = updated = flipped = reopened = 0

    for t in tasks:
        tid = str(t["id"])
        seen.add(tid)
        content = t.get("content", "")
        due = _due_str(t.get("due"))
        labels = t.get("labels") or []
        existing = by_task.get(tid)

        if existing is not None:
            changed = existing.text != content or existing.due != due
            # Todoist owns mirrored rows: a done mirror back in the active set
            # was un-completed remotely (or is a recurring task that advanced),
            # so follow Todoist and reopen. Only mirrored rows — never a
            # locally-done task.
            reopen = existing.origin == "todoist" and existing.status == "done"
            if changed:
                updated += 1
            if reopen:
                reopened += 1
            if not dry_run:
                existing.text = content
                existing.due = due
                if existing.sync.todoist:
                    existing.sync.todoist.project_id = t.get("project_id")
                existing.mirrored_at = now_iso()
                if reopen:
                    existing.status = "open"
                    existing.done_ts = None
                    existing.done_source = None
                    if existing.sync.todoist:
                        existing.sync.todoist.closed_ts = None
            continue

        created += 1
        if dry_run:
            continue
        e = TodoEntry(
            text=content,
            status="open",
            source=_first_in(labels, src_labels) or "todoist",
            project=_first_in(labels, proj_labels),
            origin="todoist",
            due=due,
            mirrored_at=now_iso(),
        )
        e.sync.todoist = TodoistSync(
            task_id=tid,
            url=f"https://app.todoist.com/app/task/{tid}",
            ts=now_iso(),
            project_id=t.get("project_id"),
        )
        entries.append(e)

    # Completion/deletion sweep: a mirrored row whose task is no longer in the
    # active set of an in-scope project was completed or deleted remotely.
    for e in entries:
        if e.origin != "todoist" or e.status != "open":
            continue
        st = e.sync.todoist
        if not st or not st.task_id or st.project_id not in included:
            continue
        if st.task_id not in seen:
            flipped += 1
            if not dry_run:
                e.status = "done"
                e.done_ts = now_iso()
                e.done_source = "todoist"
                st.closed_ts = now_iso()  # gone from Todoist = already closed

    prefix = "todoist pull (dry-run):" if dry_run else "todoist pull:"
    print(
        f"{prefix} {len(tasks)} in-scope tasks; "
        f"created {created}, updated {updated}, completed {flipped}, "
        f"reopened {reopened}"
    )
    if not dry_run:
        log(
            f"todoist pull created={created} updated={updated} "
            f"completed={flipped} reopened={reopened} scope_tasks={len(tasks)}"
        )
    return 0
