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


class NotionSync(BaseModel):
    model_config = ConfigDict(extra="allow")
    page_id: str | None = None
    url: str | None = None
    ts: str


class SyncState(BaseModel):
    model_config = ConfigDict(extra="allow")
    logseq: LogseqSync | None = None
    notion: NotionSync | None = None


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

    @property
    def short_id(self) -> str:
        """Display id: trailing 8 random hex chars (more unique than ts prefix)."""
        return self.id[-8:]
