"""Obsidian vault capture writer — one Markdown file per capture.

The Obsidian vault is the canonical memory store (see plan-transition.md,
2026-06-01): Notion is read-only reference, Logseq is a frozen archive, and
every phone/CLI capture becomes its own Markdown file here. One file per
capture means no shared inbox.md for two sync clients to fight over — the key
to keeping a Google-Drive-synced vault conflict-free.

Layout:   captures/YYYY-MM-DD/<HHMMSS>-<source>-<id8>.md
Frontmatter contract (do not over-design): id, created, source, type, status, tags.
Tasks are written as a "- [ ] ..." checkbox so Obsidian renders them as tasks;
notes and ideas are plain body text.
"""

from __future__ import annotations

import datetime as dt
import json
import secrets
import urllib.parse
from pathlib import Path
from typing import Any

from .config import OBSIDIAN_VAULT
from .storage import log

KINDS = ("note", "idea", "task")


def captures_root() -> Path:
    """Captures dir under the (possibly monkeypatched) vault root."""
    return OBSIDIAN_VAULT / "captures"


def attachments_root() -> Path:
    """Attachments dir under the (possibly monkeypatched) vault root."""
    return OBSIDIAN_VAULT / "Attachments"


def vault_relative(path: Path) -> str:
    """`path` as a vault-relative string; unchanged when it lies outside the vault."""
    try:
        return str(path.relative_to(OBSIDIAN_VAULT))
    except ValueError:
        return str(path)


def unique_path(path: Path) -> Path:
    """`path`, or its first free `-2`, `-3`, ... sibling when it already exists."""
    if not path.exists():
        return path
    for i in range(2, 1000):
        candidate = path.with_name(f"{path.stem}-{i}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise OSError(f"could not allocate unique attachment path for {path}")


def deep_link(path: Path) -> str:
    """An obsidian:// URI that opens `path` in the desktop or mobile app.

    The vault name is the directory name of OBSIDIAN_VAULT (e.g. "obsidian").
    The file parameter is vault-relative and URL-encoded (spaces become %20).
    """
    vault_name = urllib.parse.quote(OBSIDIAN_VAULT.name)
    encoded = urllib.parse.quote(vault_relative(path), safe="/")
    return f"obsidian://open?vault={vault_name}&file={encoded}"


def _yaml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, int | float):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def _frontmatter(
    id8: str,
    created: str,
    source: str,
    kind: str,
    status: str,
    tags: list[str],
    metadata: dict[str, Any] | None = None,
) -> str:
    body = (
        "---\n"
        f"id: {id8}\n"
        f"created: {created}\n"
        f"source: {source}\n"
        f"type: {kind}\n"
        f"status: {status}\n"
        f"tags: [{', '.join(tags)}]\n"
    )
    for key, value in (metadata or {}).items():
        body += f"{key}: {_yaml_value(value)}\n"
    return body + "---\n"


def write_capture(
    text: str,
    kind: str = "note",
    source: str = "cli",
    *,
    id8: str | None = None,
    created: str | None = None,
    tags: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
    extra_body: str | None = None,
) -> Path:
    """Write one capture as its own Markdown file; return the path.

    `kind` is one of note|idea|task. Tasks become a Markdown checkbox so they
    surface in Obsidian's task views; status starts "open" for everything (the
    janitor flips to filed/done). The filename's random id8 keeps it unique even
    for two captures in the same second, so writes never collide.
    """
    if kind not in KINDS:
        kind = "note"
    now = dt.datetime.now().astimezone()
    created = created or now.isoformat(timespec="seconds")
    id8 = id8 or secrets.token_hex(4)
    tags = tags if tags is not None else []

    folder = captures_root() / now.strftime("%Y-%m-%d")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{now.strftime('%H%M%S')}-{source}-{id8}.md"

    body = f"- [ ] {text}" if kind == "task" else text
    if extra_body:
        body = body.rstrip() + "\n\n" + extra_body.strip()
    path.write_text(
        _frontmatter(id8, created, source, kind, "open", tags, metadata=metadata)
        + "\n"
        + body
        + "\n"
    )
    log(f"obsidian capture {kind} -> {path}")
    return path
