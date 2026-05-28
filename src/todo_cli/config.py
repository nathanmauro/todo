"""Static paths, env-driven settings, and API constants."""
from __future__ import annotations

import json
import os
from pathlib import Path

HOME = Path.home()
TODO_DIR = Path(os.environ.get("TODO_DIR", HOME / ".todo"))
TODOS_FILE = TODO_DIR / "todos.jsonl"
LOG_FILE = TODO_DIR / "todo.log"

LOGSEQ_GRAPH = Path(os.environ.get("TODO_LOGSEQ_GRAPH", HOME / "Notes"))

# Todoist API v1
TODOIST_API = "https://api.todoist.com/api/v1"

# Default capture project resolves: env override -> canonical cockpit structure
# file (todoist-structure.json) -> Inbox. Keeps the CLI in sync with the rest of
# the toolchain instead of hard-coding a project id that goes stale.
TODOIST_INBOX_FALLBACK = "6CrgHvjH3RPXmHCg"


def _default_project_id() -> str:
    env = os.environ.get("TODO_TODOIST_PROJECT_ID")
    if env:
        return env
    struct = Path(
        os.environ.get(
            "TODOIST_STRUCTURE",
            HOME / "Documents" / "cockpit" / "todoist-structure.json",
        )
    )
    try:
        data = json.loads(struct.read_text())
        return data["projects"][data["routing"]["default_capture"]]["id"]
    except Exception:
        return TODOIST_INBOX_FALLBACK


TODOIST_PROJECT_ID = _default_project_id()

KEYCHAIN_SERVICE = "todo-cli"
