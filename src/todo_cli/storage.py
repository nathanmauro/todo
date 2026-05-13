"""JSONL-backed store for TodoEntry plus a tiny append-only log."""
from __future__ import annotations

import json
import sys

from pydantic import ValidationError

from .config import LOG_FILE, TODO_DIR, TODOS_FILE
from .models import TodoEntry, now_iso


def ensure_store() -> None:
    TODO_DIR.mkdir(parents=True, exist_ok=True)
    TODOS_FILE.touch(exist_ok=True)


def load_all() -> list[TodoEntry]:
    ensure_store()
    out: list[TodoEntry] = []
    with TODOS_FILE.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(TodoEntry.model_validate_json(line))
            except (json.JSONDecodeError, ValidationError):
                continue
    return out


def write_all(entries: list[TodoEntry]) -> None:
    ensure_store()
    tmp = TODOS_FILE.with_suffix(".jsonl.tmp")
    with tmp.open("w") as f:
        for e in entries:
            f.write(e.model_dump_json(exclude_none=True) + "\n")
    tmp.replace(TODOS_FILE)


def append(entry: TodoEntry) -> None:
    ensure_store()
    with TODOS_FILE.open("a") as f:
        f.write(entry.model_dump_json() + "\n")


def find_by_prefix(entries: list[TodoEntry], needle: str) -> TodoEntry | None:
    """Match against full id, short_id, or any substring of full id."""
    matches = [
        e
        for e in entries
        if e.id == needle or e.short_id.startswith(needle) or needle in e.id
    ]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        sys.exit(f"ambiguous '{needle}' ({len(matches)} matches)")
    return None


def log(msg: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a") as f:
        f.write(f"{now_iso()} {msg}\n")
