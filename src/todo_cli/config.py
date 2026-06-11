"""Static paths, env-driven settings, and API constants."""
from __future__ import annotations

import json
import os
from pathlib import Path

HOME = Path.home()
TODO_DIR = Path(os.environ.get("TODO_DIR", HOME / ".todo"))
TODOS_FILE = TODO_DIR / "todos.jsonl"
LOG_FILE = TODO_DIR / "todo.log"

_LOGSEQ_GRAPH_RAW = Path(os.environ.get("TODO_LOGSEQ_GRAPH", HOME / "Notes" / "logseq")).expanduser()
if _LOGSEQ_GRAPH_RAW == HOME / "Notes":
    _LOGSEQ_GRAPH_RAW = HOME / "Notes" / "logseq"
LOGSEQ_GRAPH = _LOGSEQ_GRAPH_RAW

# Obsidian vault — the canonical capture/memory store (plan-transition.md,
# 2026-06-01). Phone (Telegram) and CLI captures each land as one Markdown file
# under <vault>/captures/YYYY-MM-DD/. Override the path here when the vault moves
# onto Google Drive for cross-device read/write — a single env flip, no code change.
OBSIDIAN_VAULT = Path(
    os.environ.get("TODO_OBSIDIAN_VAULT", HOME / "Notes" / "obsidian")
)

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
            HOME / "Developer" / "proj" / "cockpit" / "todoist-structure.json",
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


def project_role_ids() -> dict[str, str]:
    """Structure project-key -> Todoist project id (inbox, current_work,
    idea_cooker, resource, archive). Empty if the structure file is absent.
    Lets `todo backlog` classify a task's lane without hard-coding ids."""
    out: dict[str, str] = {}
    for key, val in _structure().get("projects", {}).items():
        if isinstance(val, dict) and val.get("id"):
            out[key] = val["id"]
    return out


def idea_cooker_sections() -> dict[str, str]:
    """Idea Cooker section name -> section id (dreamer, cooking, shaped,
    board_ready, parked). Empty if absent."""
    ic = _structure().get("projects", {}).get("idea_cooker", {})
    return dict(ic.get("sections", {}))


TODOIST_PROJECT_ID = _default_project_id()

KEYCHAIN_SERVICE = "todo-cli"

# --- Logseq task sync (frozen archive; OFF by default) ----------------------
# Logseq (~/Notes/logseq) became a FROZEN read-only archive on 2026-06-01. The
# CLI no longer writes task blocks/journal lines there unless this flag is
# explicitly turned on (TODO_LOGSEQ_SYNC=1) — every Logseq write is otherwise a
# no-op. Kept behind a flag (rather than ripped out) so the writers can be
# re-enabled for a one-off backfill without resurrecting code.
LOGSEQ_SYNC_ENABLED = os.environ.get("TODO_LOGSEQ_SYNC", "0") == "1"

# --- Telegram -> Obsidian capture lane --------------------------------------
# A @BotFather bot is the mobile front door. `todo telegram-poll --loop` runs a
# getUpdates long-poll daemon (no public endpoint, works behind NAT); each
# message becomes one Markdown file in the Obsidian vault under
# captures/YYYY-MM-DD/ (see obsidian.py). "+t" tasks also push to Todoist. Voice
# notes are transcribed locally with whisper.cpp. Token from the login keychain
# (account 'telegram', service 'todo-cli'). The last update_id is persisted as
# the exactly-once offset cursor; the sender chat_id is persisted so the bot can
# proactively message back (see TELEGRAM_CHAT below).
TELEGRAM_API = "https://api.telegram.org"
TELEGRAM_KEYCHAIN_ACCOUNT = os.environ.get("TODO_TELEGRAM_KEYCHAIN_ACCOUNT", "telegram")
# Exactly-once offset cursor. Lives under the neutral store dir (was under
# ~/.notion-sync/ before the 2026-06-01 cutover; the live offset was migrated
# across when the Notion lane was retired).
TELEGRAM_STATE = Path(
    os.environ.get("TODO_TELEGRAM_STATE", TODO_DIR / "telegram-state.json")
)
# Last sender chat_id, persisted so `todo telegram-send` can message Nathan back
# (delivery enabler — the bot becomes a two-way channel, not just an inbox).
TELEGRAM_CHAT = Path(
    os.environ.get("TODO_TELEGRAM_CHAT", TODO_DIR / "telegram-chat.json")
)
TELEGRAM_ENABLED = os.environ.get("TODO_TELEGRAM", "1") != "0"
# Action registry for actionable notifications: callback_data is capped at 64
# bytes, so an inline button carries only a short id and the full action (verb +
# payload) lives here as one JSON file, written at send time and executed when
# the tap's callback_query arrives through the same long poll.
TELEGRAM_ACTIONS = Path(
    os.environ.get("TODO_TELEGRAM_ACTIONS", TODO_DIR / "telegram-actions")
)
# Single-user lock: comma-separated numeric chat ids allowed to drive the bot.
# Empty = accept any chat (and the bot's reply tells you your chat_id so you can
# lock it). A non-empty list silently drops messages from any other chat.
TELEGRAM_ALLOWED_CHATS = [
    c.strip()
    for c in os.environ.get("TELEGRAM_ALLOWED_CHAT_ID", "").split(",")
    if c.strip()
]
# whisper.cpp CLI for voice-note transcription (brew install whisper-cpp).
WHISPER_BIN = os.environ.get("TODO_WHISPER_BIN", "whisper-cli")
# ggml model path; "" disables voice transcription (text captures still work).
# Default points at the brew whisper.cpp base.en model if present.
_WHISPER_DEFAULT = HOME / ".cache" / "whisper" / "ggml-base.en.bin"
WHISPER_MODEL = os.environ.get(
    "TODO_WHISPER_MODEL", str(_WHISPER_DEFAULT) if _WHISPER_DEFAULT.exists() else ""
)
