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

# --- Notion Capture Inbox (mobile -> Logseq journal pull) -------------------
# A row in this Notion database is a phone-captured note/idea/task. The
# `notion-sync` verb pulls unsynced rows DOWN into today's Logseq journal
# (append-only) and flips Synced=true. Notion is never the source of truth for
# notes once pulled — Logseq owns them. Tasks route through the normal todo
# store so they reach Todoist like any other task.
NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
NOTION_KEYCHAIN_ACCOUNT = os.environ.get("TODO_NOTION_KEYCHAIN_ACCOUNT", "notion")
# Capture Inbox database id (under Notion: Journal -> Capture Inbox).
NOTION_INBOX_DB = os.environ.get(
    "TODO_NOTION_INBOX_DB", "2e7f85cb-883b-406b-a47a-666b3bfbf79f"
)
NOTION_SYNC_DIR = Path(os.environ.get("TODO_NOTION_SYNC_DIR", HOME / ".notion-sync"))
NOTION_SYNC_STATE = NOTION_SYNC_DIR / "state.json"

# --- PARA auto-filing ledger ------------------------------------------------
# Maps each pulled Capture Inbox row (page_id) to where it was filed, so a
# re-run after a classifier returned a *different* target page can't double
# file. LLM placement is non-deterministic; the in-file `<!-- nx:<id> -->`
# marker only guards the one target it happened to choose, so the ledger is the
# authoritative "already handled" record. See `ledger.py`.
FILED_LEDGER = NOTION_SYNC_DIR / "filed.json"

# Quarantine page for low-confidence placements: filed here for human triage in
# Logseq rather than guessed into a topic page (the graph is hand-curated).
INBOX_CAPTURE_PAGE = os.environ.get("TODO_INBOX_CAPTURE_PAGE", "inbox-capture")

# --- Local PARA classifier (LM Studio, OpenAI-compatible) -------------------
# A capture is classified by a small local model first (qwen3-4b MLX via LM
# Studio, the same model sba-agentic uses). On unreachable/parse failure/low
# confidence the capture falls back to the journal (never dropped, never
# guessed). Optional escalation to `claude -p` is OFF by default to keep the
# 15-min launchd job keyless and offline-tolerant.
CLASSIFY_ENABLED = os.environ.get("TODO_CLASSIFY", "1") != "0"
CLASSIFY_ENDPOINT = os.environ.get(
    "TODO_CLASSIFY_ENDPOINT", "http://localhost:1234/v1/chat/completions"
)
CLASSIFY_MODEL = os.environ.get(
    "TODO_CLASSIFY_MODEL", "qwen3-4b-instruct-2507-mlx"
)
# Route to a topic page only at/above this confidence; below the lower bound a
# clear non-journal capture is quarantined to INBOX_CAPTURE_PAGE.
CLASSIFY_PAGE_THRESHOLD = float(os.environ.get("TODO_CLASSIFY_PAGE_THRESHOLD", "0.7"))
CLASSIFY_QUARANTINE_FLOOR = float(os.environ.get("TODO_CLASSIFY_QUARANTINE_FLOOR", "0.4"))
# `claude -p` second opinion for borderline cases (off by default).
CLASSIFY_ESCALATE = os.environ.get("TODO_CLASSIFY_ESCALATE", "0") == "1"

# --- Telegram capture lane --------------------------------------------------
# A @BotFather bot is an additional capture *producer*: getUpdates long-poll
# (no public endpoint, works behind NAT), voice notes transcribed locally, then
# one create_row into the Capture Inbox so the existing drain files it. Token
# from the login keychain (account 'telegram', service 'todo-cli').
TELEGRAM_API = "https://api.telegram.org"
TELEGRAM_KEYCHAIN_ACCOUNT = os.environ.get("TODO_TELEGRAM_KEYCHAIN_ACCOUNT", "telegram")
TELEGRAM_STATE = NOTION_SYNC_DIR / "telegram-state.json"
TELEGRAM_ENABLED = os.environ.get("TODO_TELEGRAM", "1") != "0"
# whisper.cpp CLI for voice-note transcription (brew install whisper-cpp).
WHISPER_BIN = os.environ.get("TODO_WHISPER_BIN", "whisper-cli")
# ggml model path; "" disables voice transcription (text captures still work).
# Default points at the brew whisper.cpp base.en model if present.
_WHISPER_DEFAULT = HOME / ".cache" / "whisper" / "ggml-base.en.bin"
WHISPER_MODEL = os.environ.get(
    "TODO_WHISPER_MODEL", str(_WHISPER_DEFAULT) if _WHISPER_DEFAULT.exists() else ""
)
