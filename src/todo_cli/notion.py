"""Notion Capture Inbox -> Logseq journal pull.

Phone captures land as rows in a Notion "Capture Inbox" database. This module
pulls unsynced rows DOWN into today's Logseq journal (append-only) and flips
each row's Synced checkbox true.

Idempotency = a grep-able `<!-- nx:<page_id> -->` marker in the journal plus the
server-side Synced=false filter (double guard): a re-run after a failed flip
re-finds the marker, skips the append, and retries the flip. Notion is never the
source of truth once a row is pulled — Logseq owns it; editing a synced row in
Notion does not re-sync.

Notes/ideas are written straight to the journal. Task-flagged rows become normal
TodoEntry rows (handled by the command layer) so they reach Todoist + the journal
through the existing `sync` path.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass

from .config import (
    KEYCHAIN_SERVICE,
    NOTION_API,
    NOTION_INBOX_DB,
    NOTION_KEYCHAIN_ACCOUNT,
    NOTION_SYNC_DIR,
    NOTION_SYNC_STATE,
    NOTION_VERSION,
)
from .storage import log


@dataclass
class InboxRow:
    page_id: str
    text: str
    idea: bool
    task: bool
    source: str


def token() -> str | None:
    env = os.environ.get("NOTION_TOKEN")
    if env:
        return env
    try:
        r = subprocess.run(
            ["security", "find-generic-password",
             "-a", NOTION_KEYCHAIN_ACCOUNT, "-s", KEYCHAIN_SERVICE, "-w"],
            capture_output=True, text=True, check=False,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except FileNotFoundError:
        pass
    return None


def _headers(tok: str) -> dict:
    return {
        "Authorization": f"Bearer {tok}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _request(method: str, url: str, tok: str, body: dict | None = None,
             timeout: float = 15.0) -> dict | None:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, headers=_headers(tok), method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:200]
        log(f"notion {method} {url} -> HTTP {exc.code} {detail}")
        return None
    except urllib.error.URLError as exc:
        log(f"notion {method} {url} -> {exc}")
        return None


def _title(props: dict, name: str = "Text") -> str:
    arr = (props.get(name) or {}).get("title") or []
    return "".join(t.get("plain_text", "") for t in arr).strip()


def _checkbox(props: dict, name: str) -> bool:
    return bool((props.get(name) or {}).get("checkbox"))


def _select(props: dict, name: str) -> str:
    sel = (props.get(name) or {}).get("select") or {}
    return sel.get("name") or ""


def query_unsynced(tok: str) -> list[InboxRow] | None:
    """All Capture Inbox rows with Synced=false, oldest first.

    Returns None (not []) when the DB is unreachable — e.g. the integration is
    not yet connected (HTTP 404) — so the caller can distinguish "can't reach"
    from "genuinely empty". Detail is written to the log by `_request`.
    """
    body: dict = {
        "filter": {"property": "Synced", "checkbox": {"equals": False}},
        "sorts": [{"timestamp": "created_time", "direction": "ascending"}],
        "page_size": 100,
    }
    url = f"{NOTION_API}/databases/{NOTION_INBOX_DB}/query"
    rows: list[InboxRow] = []
    cursor: str | None = None
    got_response = False
    while True:
        if cursor:
            body["start_cursor"] = cursor
        result = _request("POST", url, tok, body)
        if result is None:
            break
        got_response = True
        for r in result.get("results", []):
            props = r.get("properties", {}) or {}
            text = _title(props, "Text")
            if not text:
                continue
            rows.append(InboxRow(
                page_id=r["id"],
                text=text,
                idea=_checkbox(props, "Idea"),
                task=_checkbox(props, "Task"),
                source=_select(props, "Source") or "mobile",
            ))
        if not result.get("has_more"):
            break
        cursor = result.get("next_cursor")
        if not cursor:
            break
    return rows if got_response else None


def mark_synced(tok: str, page_id: str) -> bool:
    url = f"{NOTION_API}/pages/{page_id}"
    body = {"properties": {"Synced": {"checkbox": True}}}
    return _request("PATCH", url, tok, body) is not None


def create_row(tok: str, text: str, source: str = "claude",
               idea: bool = False, task: bool = False) -> str | None:
    """Create a Capture Inbox row (used by tests / desktop capture-to-Notion)."""
    url = f"{NOTION_API}/pages"
    body = {
        "parent": {"database_id": NOTION_INBOX_DB},
        "properties": {
            "Text": {"title": [{"text": {"content": text}}]},
            "Source": {"select": {"name": source}},
            "Synced": {"checkbox": False},
            "Idea": {"checkbox": idea},
            "Task": {"checkbox": task},
        },
    }
    result = _request("POST", url, tok, body)
    return result.get("id") if result else None


def nx_marker(page_id: str) -> str:
    """Grep-able idempotency marker for a pulled journal line."""
    return f"<!-- nx:{page_id} -->"


def write_state(pulled: int, tasks: int, rows_seen: int) -> None:
    NOTION_SYNC_DIR.mkdir(parents=True, exist_ok=True)
    NOTION_SYNC_STATE.write_text(json.dumps({
        "last_run": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "last_pulled_notes": pulled,
        "last_pulled_tasks": tasks,
        "last_rows_seen": rows_seen,
    }, indent=2))
