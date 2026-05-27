"""Static paths, env-driven settings, and API constants."""
from __future__ import annotations

import os
from pathlib import Path

HOME = Path.home()
TODO_DIR = Path(os.environ.get("TODO_DIR", HOME / ".todo"))
TODOS_FILE = TODO_DIR / "todos.jsonl"
LOG_FILE = TODO_DIR / "todo.log"

LOGSEQ_GRAPH = Path(os.environ.get("TODO_LOGSEQ_GRAPH", HOME / "Notes"))

# Todoist REST API v2
TODOIST_API = "https://api.todoist.com/api/v1"
TODOIST_PROJECT_ID = os.environ.get(
    "TODO_TODOIST_PROJECT_ID", "6RqMQ6GcRcw7jJJ5"
)

KEYCHAIN_SERVICE = "todo-cli"
