"""Notion API sync + reconcile."""
from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request

from .config import (
    KEYCHAIN_ACCOUNT,
    KEYCHAIN_SERVICE,
    NOTION_API,
    NOTION_DB_ID,
    NOTION_VERSION,
)
from .models import NotionSync, TodoEntry, now_iso
from .storage import log


def token() -> str | None:
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


def _headers(tok: str, content_type: bool = False) -> dict[str, str]:
    h = {
        "Authorization": f"Bearer {tok}",
        "Notion-Version": NOTION_VERSION,
    }
    if content_type:
        h["Content-Type"] = "application/json"
    return h


def fetch_page(tok: str, page_id: str) -> dict:
    req = urllib.request.Request(
        f"{NOTION_API}/pages/{page_id}",
        method="GET",
        headers=_headers(tok),
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def create_page(
    tok: str,
    text: str,
    project: str | None = None,
    source: str | None = None,
) -> dict:
    properties: dict = {
        "Task name": {"title": [{"text": {"content": text}}]},
        "Status": {"status": {"name": "Not started"}},
    }
    if project:
        properties["Project"] = {"select": {"name": project}}
    if source:
        properties["Source"] = {"select": {"name": source}}
    body = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": properties,
    }
    req = urllib.request.Request(
        f"{NOTION_API}/pages",
        data=json.dumps(body).encode(),
        method="POST",
        headers=_headers(tok, content_type=True),
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def sync(entries: list[TodoEntry]) -> int:
    tok = token()
    if not tok:
        print(
            "notion: no token. store one: security add-generic-password "
            f"-a {KEYCHAIN_ACCOUNT} -s {KEYCHAIN_SERVICE} -w <token>"
        )
        return 1
    pending = [e for e in entries if e.status == "open" and e.sync.notion is None]
    if not pending:
        print("notion: nothing to sync")
        return 0
    created = 0
    failed = 0
    for e in pending:
        try:
            page = create_page(tok, e.text, project=e.project, source=e.source)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode(errors="replace")
            print(f"notion: {e.id[:8]} FAIL {exc.code} {body[:200]}")
            log(f"notion fail id={e.id} code={exc.code} body={body[:500]}")
            failed += 1
            continue
        except urllib.error.URLError as exc:
            print(f"notion: {e.id[:8]} network error: {exc}")
            failed += 1
            continue
        e.sync.notion = NotionSync(
            page_id=page.get("id"),
            url=page.get("url"),
            ts=now_iso(),
        )
        created += 1
    print(f"notion: created {created}, failed {failed}")
    log(f"notion sync created={created} failed={failed}")
    return 0 if failed == 0 else 1


def reconcile(entries: list[TodoEntry]) -> int:
    tok = token()
    if not tok:
        print("notion: no token; skipping reconcile")
        return 1
    checked = 0
    flipped = 0
    archived = 0
    failed = 0
    for e in entries:
        if e.sync.notion is None or e.status != "open":
            continue
        page_id = e.sync.notion.page_id
        if not page_id:
            continue
        checked += 1
        try:
            page = fetch_page(tok, page_id)
        except urllib.error.HTTPError as exc:
            print(f"notion: {e.short_id} FAIL {exc.code}")
            failed += 1
            continue
        except urllib.error.URLError as exc:
            print(f"notion: {e.short_id} network error {exc}")
            failed += 1
            continue
        if page.get("archived") or page.get("in_trash"):
            archived += 1
            continue
        status = (
            page.get("properties", {}).get("Status", {}).get("status") or {}
        )
        name = (status.get("name") or "").lower()
        if name == "done":
            e.status = "done"
            e.done_ts = now_iso()
            e.done_source = "notion"
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
