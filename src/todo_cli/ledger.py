"""Filed-capture ledger — the authoritative "already handled" record.

Each pulled Capture Inbox row is keyed by its Notion `page_id`. Because the
PARA classifier is non-deterministic, a retry could pick a *different* target
page than a prior run, and the in-file `<!-- nx:<page_id> -->` marker would not
be found in the new target → a duplicate. The ledger closes that gap: once a
row's `page_id` is recorded here it is never filed again, regardless of what
the classifier would say on a second look.

The server-side `Synced=false` filter is still the primary guard; this ledger
plus the nx marker are the belt-and-suspenders for the window between
"appended to a file" and "flipped Synced=true".
"""
from __future__ import annotations

import datetime as dt
import json

from .config import FILED_LEDGER


def _load() -> dict:
    try:
        return json.loads(FILED_LEDGER.read_text())
    except Exception:
        return {}


def has(page_id: str) -> bool:
    return page_id in _load()


def record(page_id: str, target_file: str, *, confidence: float | None = None,
           source: str = "") -> None:
    """Mark a row filed. Idempotent — re-recording just refreshes the entry."""
    data = _load()
    data[page_id] = {
        "target_file": target_file,
        "confidence": confidence,
        "source": source,
        "filed_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    FILED_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    FILED_LEDGER.write_text(json.dumps(data, indent=2, sort_keys=True))


def target_for(page_id: str) -> str | None:
    entry = _load().get(page_id)
    return entry.get("target_file") if entry else None
