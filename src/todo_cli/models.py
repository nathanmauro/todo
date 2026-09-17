"""Pydantic models for todo entries and their sync state.

Wire format is JSONL: one entry per line, written via `model_dump_json`.
`extra="allow"` keeps unknown fields round-trippable so older/newer clients
can share the same file without losing data.
"""
from __future__ import annotations

import datetime as dt
import secrets
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Status = Literal["open", "done"]


def new_id() -> str:
    """ULID-ish: ms timestamp + 8 random hex chars. Sortable, prefix-matchable."""
    ts = int(dt.datetime.now().timestamp() * 1000)
    return f"{ts:013d}{secrets.token_hex(4)}"


def now_iso() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


class LogseqSync(BaseModel):
    model_config = ConfigDict(extra="allow")
    file: str
    marker: str
    ts: str


class TodoistSync(BaseModel):
    model_config = ConfigDict(extra="allow")
    task_id: str
    url: str | None = None
    ts: str
    project_id: str | None = None
    # Set once this row's completion has reached Todoist (the task is closed
    # there). Gates the outbound completion push so a done row is never
    # re-closed and inbound-flipped rows are never pushed back.
    closed_ts: str | None = None


class GtasksSync(BaseModel):
    model_config = ConfigDict(extra="allow")
    task_id: str
    list_id: str
    url: str | None = None
    ts: str
    # Set once this row's completion has reached Google Tasks; same gating
    # contract as TodoistSync.closed_ts.
    closed_ts: str | None = None


class LinearSync(BaseModel):
    model_config = ConfigDict(extra="allow")
    issue_id: str
    identifier: str | None = None
    url: str | None = None
    ts: str
    # Set once this row's completion has reached Linear; same gating contract as
    # TodoistSync.closed_ts.
    closed_ts: str | None = None


class SyncState(BaseModel):
    model_config = ConfigDict(extra="allow")
    logseq: LogseqSync | None = None
    todoist: TodoistSync | None = None
    gtasks: GtasksSync | None = None
    linear: LinearSync | None = None


class TodoEntry(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str = Field(default_factory=new_id)
    ts: str = Field(default_factory=now_iso)
    text: str
    status: Status = "open"
    source: str = "cli"
    project: str | None = None
    sync: SyncState = Field(default_factory=SyncState)
    due: str | None = None
    done_ts: str | None = None
    done_source: str | None = None
    # "todoist" = mirrored in from Todoist (read-only); None/other = locally
    # originated. The push channel never re-pushes a "todoist" row.
    origin: str | None = None
    mirrored_at: str | None = None
    # Capture intent carried to the Linear backend: Todoist-style priority (p1..p4)
    # and destination (inbox | current | idea) from cockpit-task-sync / cockpit-capture.
    priority: str | None = None
    dest: str | None = None
    # Free-text body for the Linear issue (capture provenance, queue file, context).
    notes: str | None = None
    # Dormant: kept only so old todos.jsonl rows (written by the retired Notion
    # Capture Inbox drain, 2026-06-01) still parse. Nothing reads or sets it now.
    notion_inbox_id: str | None = None

    @property
    def short_id(self) -> str:
        """Display id: trailing 8 random hex chars (more unique than ts prefix)."""
        return self.id[-8:]
