"""Static paths, env-driven settings, and Notion API constants."""
from __future__ import annotations

import os
from pathlib import Path

HOME = Path.home()
TODO_DIR = Path(os.environ.get("TODO_DIR", HOME / ".todo"))
TODOS_FILE = TODO_DIR / "todos.jsonl"
LOG_FILE = TODO_DIR / "todo.log"

LOGSEQ_GRAPH = Path(os.environ.get("TODO_LOGSEQ_GRAPH", HOME / "Notes"))

NOTION_DB_ID = os.environ.get(
    "TODO_NOTION_DB_ID", "353b9be9-bd58-8049-b5c5-e577f0a49756"
)
NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

KEYCHAIN_ACCOUNT = "notion"
KEYCHAIN_SERVICE = "todo-cli"
