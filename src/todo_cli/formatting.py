"""Display helpers for the `ls` output."""
from __future__ import annotations

import datetime as dt

from .models import TodoEntry


def human_ago(iso: str) -> str:
    try:
        t = dt.datetime.fromisoformat(iso)
    except ValueError:
        return iso
    delta = dt.datetime.now().astimezone() - t
    secs = int(delta.total_seconds())
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    days = secs // 86400
    if days < 30:
        return f"{days}d ago"
    return t.strftime("%Y-%m-%d")


def sync_badges(entry: TodoEntry) -> str:
    parts = []
    if entry.sync.logseq:
        parts.append("logseq")
    if entry.sync.todoist:
        parts.append("todoist")
    return " ".join(f"[{p}]" for p in parts)
