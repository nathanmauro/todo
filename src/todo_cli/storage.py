"""JSONL-backed store for TodoEntry plus a tiny append-only log."""
from __future__ import annotations

import contextlib
import fcntl
import json
import os
import sys
import time

from pydantic import ValidationError

from .config import LOG_FILE, TODO_DIR, TODOS_FILE
from .models import TodoEntry, now_iso

LOCK_TIMEOUT = 120.0


class LockTimeout(RuntimeError):
    """Could not acquire the store lock before the deadline."""


def ensure_store() -> None:
    TODO_DIR.mkdir(parents=True, exist_ok=True)
    TODOS_FILE.touch(exist_ok=True)


@contextlib.contextmanager
def file_lock(timeout: float = LOCK_TIMEOUT):
    """Serialize load_all -> write_all critical sections across processes.

    flock on a sidecar file (todos.lock) — locking todos.jsonl itself would be
    useless because write_all replaces it. On timeout this RAISES LockTimeout
    rather than proceeding unlocked: an unlocked read-modify-rewrite can
    silently destroy a concurrent local-origin append (which, unlike a
    mirrored row, would never re-converge from Todoist). Mutating verbs fail
    loudly and get retried — by the user interactively, or by the next
    launchd refresh tick.
    """
    ensure_store()
    f = (TODO_DIR / "todos.lock").open("w")
    deadline = time.monotonic() + timeout
    try:
        while True:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    log(f"file_lock: timeout after {timeout}s; giving up")
                    raise LockTimeout(
                        f"could not lock the todo store within {timeout:.0f}s "
                        "(another todo process is holding it); try again"
                    ) from None
                time.sleep(0.2)
        yield
    finally:
        with contextlib.suppress(OSError):
            fcntl.flock(f, fcntl.LOCK_UN)
        f.close()


def load_all() -> list[TodoEntry]:
    ensure_store()
    out: list[TodoEntry] = []
    bad: list[str] = []
    with TODOS_FILE.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(TodoEntry.model_validate_json(line))
            except (json.JSONDecodeError, ValidationError):
                bad.append(line)
    if bad:
        _quarantine(bad)
    return out


def _quarantine(lines: list[str]) -> None:
    """Preserve unparseable JSONL lines before write_all erases them.

    A torn append (crash mid-write) or a row from an incompatible client must
    not be silently destroyed by the next rewrite. Deduped against the rejects
    file so read-only verbs (ls) don't re-quarantine on every call. Best-effort:
    quarantine failure must never break a read path — but always warn.
    """
    rejects = TODO_DIR / "todos.rejects.jsonl"
    try:
        seen: set[str] = set()
        if rejects.exists():
            seen = set(rejects.read_text().splitlines())
        fresh = [line for line in lines if line not in seen]
        if not fresh:
            return
        with rejects.open("a") as f:
            for line in fresh:
                f.write(line + "\n")
        log(f"load_all: quarantined {len(fresh)} unparseable line(s) -> {rejects}")
    except OSError:
        pass
    print(
        f"todo: WARNING {len(lines)} unparseable line(s) in todos.jsonl "
        f"(quarantine: {rejects})",
        file=sys.stderr,
    )


def write_all(entries: list[TodoEntry]) -> None:
    ensure_store()
    # Per-process tmp name: two writers can't truncate each other's staging
    # file, so even a (bug-induced) unlocked overlap degrades to last-writer-
    # wins on the rename instead of publishing a torn file.
    tmp = TODOS_FILE.parent / f"{TODOS_FILE.name}.tmp.{os.getpid()}"
    try:
        with tmp.open("w") as f:
            for e in entries:
                f.write(e.model_dump_json(exclude_none=True) + "\n")
        tmp.replace(TODOS_FILE)
    except BaseException:
        with contextlib.suppress(OSError):
            tmp.unlink()
        raise


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
