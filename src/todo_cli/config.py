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


def _structure() -> dict:
    """Load the canonical cockpit Todoist structure file, or {} if absent."""
    struct = Path(
        os.environ.get(
            "TODOIST_STRUCTURE",
            HOME / "Documents" / "cockpit" / "todoist-structure.json",
        )
    )
    try:
        return json.loads(struct.read_text())
    except Exception:
        return {}


def _default_project_id() -> str:
    env = os.environ.get("TODO_TODOIST_PROJECT_ID")
    if env:
        return env
    data = _structure()
    try:
        return data["projects"][data["routing"]["default_capture"]]["id"]
    except Exception:
        return TODOIST_INBOX_FALLBACK


def mirror_policy() -> dict:
    """Which Todoist tasks the `pull` mirror keeps.

    Defaults (no `mirror` block in the structure file): every personal project,
    drop shared/workspace projects (e.g. Team Inbox), active tasks only.
    """
    data = _structure().get("mirror", {})
    return {
        "exclude_shared": data.get("exclude_shared", True),
        "exclude_project_ids": list(data.get("exclude_project_ids", [])),
        "exclude_completed": data.get("exclude_completed", True),
    }


def taxonomy_labels() -> dict:
    """Known label families, used to attribute a mirrored task's source/project."""
    labels = _structure().get("labels", {})
    return {
        "source": list(labels.get("source", [])),
        "projects": list(labels.get("projects", [])),
        "areas": list(labels.get("areas", [])),
    }


TODOIST_PROJECT_ID = _default_project_id()

KEYCHAIN_SERVICE = "todo-cli"
