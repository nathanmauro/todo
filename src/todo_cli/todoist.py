"""Todoist API v1 sync + reconcile."""
from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request

from .config import KEYCHAIN_SERVICE, TODOIST_API, TODOIST_PROJECT_ID
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


def _find_section_id(tok: str, project_id: str, name: str) -> str | None:
    query = urllib.parse.quote(name)
    req = urllib.request.Request(
        f"{TODOIST_API}/sections/search?query={query}&project_id={project_id}",
        method="GET",
        headers={"Authorization": f"Bearer {tok}"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    for s in data.get("results", []):
        if s["name"].lower() == name.lower():
            return s["id"]
    return None


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
    section_id: str | None = None,
    labels: list[str] | None = None,
    due_string: str | None = None,
) -> dict:
    body: dict = {"content": text}
    if project_id:
        body["project_id"] = project_id
    if section_id:
        body["section_id"] = section_id
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


def sync(entries: list[TodoEntry]) -> int:
    tok = token()
    if not tok:
        print(
            "todoist: no token. store one:\n"
            "  security add-generic-password -a todoist -s todo-cli -w '<token>'\n"
            "  (get from https://app.todoist.com/app/settings/integrations/developer)"
        )
        return 1
    pending = [e for e in entries if e.status == "open" and e.sync.todoist is None]
    if not pending:
        print("todoist: nothing to sync")
        return 0

    ensured: set[str] = set()
    created = 0
    failed = 0
    for e in pending:
        project_id = TODOIST_PROJECT_ID
        section_id = None
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
                section_id=section_id,
                labels=labels if labels else None,
                due_string=e.due,
            )
        except urllib.error.HTTPError as exc:
            body = exc.read().decode(errors="replace")
            print(f"todoist: {e.short_id} FAIL {exc.code} {body[:200]}")
            log(f"todoist fail id={e.id} code={exc.code} body={body[:500]}")
            failed += 1
            continue
        except urllib.error.URLError as exc:
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

    print(f"todoist: created {created}, failed {failed}")
    log(f"todoist sync created={created} failed={failed}")
    return 0 if failed == 0 else 1


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
            flipped += 1

    print(
        f"todoist reconcile: checked {checked}, flipped {flipped}, "
        f"failed {failed}"
    )
    log(
        f"todoist reconcile checked={checked} flipped={flipped} failed={failed}"
    )
    return 0 if failed == 0 else 1
