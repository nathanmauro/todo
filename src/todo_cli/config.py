"""Static paths, env-driven settings, and API constants."""

from __future__ import annotations

import json
import os
from pathlib import Path

HOME = Path.home()
TODO_DIR = Path(os.environ.get("TODO_DIR", HOME / ".todo"))
TODOS_FILE = TODO_DIR / "todos.jsonl"
LOG_FILE = TODO_DIR / "todo.log"

_LOGSEQ_GRAPH_RAW = Path(
    os.environ.get("TODO_LOGSEQ_GRAPH", HOME / "Notes" / "logseq")
).expanduser()
if _LOGSEQ_GRAPH_RAW == HOME / "Notes":
    _LOGSEQ_GRAPH_RAW = HOME / "Notes" / "logseq"
LOGSEQ_GRAPH = _LOGSEQ_GRAPH_RAW

# Obsidian vault — the canonical capture/memory store (plan-transition.md,
# 2026-06-01). Phone (Slack) and CLI captures each land as one Markdown file
# under <vault>/captures/YYYY-MM-DD/. Override the path here when the vault moves
# onto Google Drive for cross-device read/write — a single env flip, no code change.
OBSIDIAN_VAULT = Path(os.environ.get("TODO_OBSIDIAN_VAULT", HOME / "Notes" / "obsidian"))

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

# --- Task backend (2026-08-20 Todoist -> Google Tasks migration) ------------
# Where outbound task captures push: "todoist" (default until cutover) or
# "gtasks". Cutover = TODO_TASK_BACKEND=gtasks in the daemon/shell environment
# (or flip this default in one commit once the migrated board is trusted).
# Either way the local todos.jsonl row lands first, so a capture survives any
# backend outage and `todo sync` retries it.
GWS_BIN = os.environ.get("TODO_GWS_BIN", "gws")
GTASKS_PRIMARY_LIST = os.environ.get("TODO_GTASKS_LIST", "Tasks")


# --- Linear backend (2026-09-17 Todoist + Google Tasks -> Linear migration) --
# Linear is the sole ongoing task destination. Personal API key lives in the login
# keychain (`security add-generic-password -a linear -s todo-cli -w`, paste at the prompt) or
# TODO_LINEAR_API_KEY. Without it every push fails closed (local row kept, retried).
LINEAR_API = os.environ.get("TODO_LINEAR_API", "https://api.linear.app/graphql")
LINEAR_TEAM_KEY = os.environ.get("TODO_LINEAR_TEAM", "NAT")
LINEAR_DEFAULT_PROJECT = os.environ.get("TODO_LINEAR_PROJECT", "Personal")
LINEAR_CAPTURE_LABEL = os.environ.get("TODO_LINEAR_CAPTURE_LABEL", "capture")
LINEAR_KEYCHAIN_ACCOUNT = "linear"


def task_backend() -> str:
    """Active outbound task backend: "linear" (default since 2026-09-17), "gtasks", or "todoist".

    The legacy backends stay selectable by env for a one-off replay, but nothing
    routes to them by default any more.
    """
    return os.environ.get("TODO_TASK_BACKEND", "linear").strip().lower()


KNOWN_BACKENDS = ("linear", "gtasks", "todoist")


def require_backend() -> str:
    """The active backend, or a ValueError for an unknown value (never fall through to Todoist)."""
    backend = task_backend()
    if backend not in KNOWN_BACKENDS:
        raise ValueError(
            f"TODO_TASK_BACKEND={backend!r} is not a known backend {KNOWN_BACKENDS}; refusing to route tasks"
        )
    return backend


# --- Logseq task sync (frozen archive; OFF by default) ----------------------
# Logseq (~/Notes/logseq) became a FROZEN read-only archive on 2026-06-01. The
# CLI no longer writes task blocks/journal lines there unless this flag is
# explicitly turned on (TODO_LOGSEQ_SYNC=1) — every Logseq write is otherwise a
# no-op. Kept behind a flag (rather than ripped out) so the writers can be
# re-enabled for a one-off backfill without resurrecting code.
LOGSEQ_SYNC_ENABLED = os.environ.get("TODO_LOGSEQ_SYNC", "0") == "1"

# --- Action registry (actionable notifications) -------------------------------
# A notification button carries only a short id; the full action (verb + payload)
# lives here as one JSON file, written at send time and executed when the click
# arrives. Other tools read these files (Job Scout's career learning), so the
# directory is shared state, not a private cache.
ACTIONS_DIR = Path(os.environ.get("TODO_ACTIONS", TODO_DIR / "actions"))

# --- Slack transport (the mobile front door since 2026-11-03) -----------------
# A Socket Mode app: `todo slack-listen` holds an outbound websocket (no public
# endpoint, works behind NAT) and `todo notify` posts with the bot token. Two
# keychain items under service 'todo-cli': the bot token (xoxb-, account
# 'slack-bot') and the app-level token (xapp-, account 'slack-app', scope
# connections:write). Channel ids are local config, never code.
SLACK_API = os.environ.get("TODO_SLACK_API", "https://slack.com/api")
SLACK_BOT_KEYCHAIN_ACCOUNT = os.environ.get("TODO_SLACK_BOT_KEYCHAIN_ACCOUNT", "slack-bot")
SLACK_APP_KEYCHAIN_ACCOUNT = os.environ.get("TODO_SLACK_APP_KEYCHAIN_ACCOUNT", "slack-app")
# {"default": "<channel id>", "routes": {"capture": "<id>", "agents": "<id>", ...}}
SLACK_ROUTES = Path(os.environ.get("TODO_SLACK_ROUTES", TODO_DIR / "slack-routes.json"))
# Recently seen Socket Mode event ids (redelivery dedupe) and last-error stamps.
SLACK_STATE = Path(os.environ.get("TODO_SLACK_STATE", TODO_DIR / "slack-state.json"))
SLACK_ENABLED = os.environ.get("TODO_SLACK", "1") != "0"
# Single-user lock: comma-separated Slack user ids (U...). Empty = open mode,
# which still files captures but refuses agent commands.
SLACK_ALLOWED_USERS = [
    u.strip() for u in os.environ.get("SLACK_ALLOWED_USER_ID", "").split(",") if u.strip()
]

# whisper.cpp CLI for voice-note transcription (brew install whisper-cpp).
WHISPER_BIN = os.environ.get("TODO_WHISPER_BIN", "whisper-cli")
# ggml model path; "" disables voice transcription (text captures still work).
# Default points at the brew whisper.cpp base.en model if present.
_WHISPER_DEFAULT = HOME / ".cache" / "whisper" / "ggml-base.en.bin"
WHISPER_MODEL = os.environ.get(
    "TODO_WHISPER_MODEL", str(_WHISPER_DEFAULT) if _WHISPER_DEFAULT.exists() else ""
)
# Parakeet TDT v3 via parakeet-mlx (`uv tool install parakeet-mlx`): preferred
# engine when installed — more accurate and faster than whisper base.en on Apple
# Silicon. whisper.cpp stays the fallback. "" disables Parakeet.
_PARAKEET_DEFAULT = HOME / ".local" / "bin" / "parakeet-mlx"
PARAKEET_BIN = os.environ.get(
    "TODO_PARAKEET_BIN", str(_PARAKEET_DEFAULT) if _PARAKEET_DEFAULT.exists() else ""
)
