"""PARA classifier — decide where a captured note belongs in the Logseq graph.

A small local model (qwen3-4b MLX via LM Studio, OpenAI-compatible) picks the
single best destination among existing pages, or JOURNAL for fleeting/daily
thoughts. The decision is gated by confidence:

    conf >= CLASSIFY_PAGE_THRESHOLD  -> file to that topic page
    floor <= conf <  page_threshold  -> quarantine to the inbox-capture page
    conf <  CLASSIFY_QUARANTINE_FLOOR -> journal (treat as fleeting)
    model picked JOURNAL              -> journal
    model unreachable / unparseable   -> journal  (never drop, never guess)

Optional `claude -p` escalation (CLASSIFY_ESCALATE) gives a borderline capture a
second opinion. Off by default so the 15-min launchd job stays keyless/offline.
"""
from __future__ import annotations

import json
import re
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass, field

from .config import (
    CLASSIFY_ENDPOINT,
    CLASSIFY_ESCALATE,
    CLASSIFY_MODEL,
    CLASSIFY_PAGE_THRESHOLD,
    CLASSIFY_QUARANTINE_FLOOR,
    INBOX_CAPTURE_PAGE,
)
from .storage import log

_JOURNAL = "JOURNAL"

_SYSTEM = (
    "You file a single captured note into a personal Logseq PARA wiki. "
    "Choose the ONE best destination among the EXISTING page names provided, "
    "or 'JOURNAL' for a fleeting thought, daily log, or note with no clear home. "
    "Never invent a page name; only use one from the list or 'JOURNAL'. "
    "Prefer JOURNAL when unsure — a wrong topic page is worse than the journal. "
    "Respond with ONLY a JSON object, no prose, of the form: "
    '{"target": "<exact existing page name or JOURNAL>", '
    '"confidence": <0..1>, '
    '"links": ["<up to 3 existing page names to cross-link>"], '
    '"reason": "<short>"}'
)


@dataclass
class Decision:
    action: str            # "page" | "inbox" | "journal"
    target_file: str | None = None   # filename when action == "page"/"inbox"
    page_name: str | None = None     # human page name when action == "page"
    links: list[str] = field(default_factory=list)
    confidence: float = 0.0
    reason: str = ""
    via: str = "local"     # "local" | "claude" | "fallback"


def _extract_json(text: str) -> dict | None:
    if not text:
        return None
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def _call_lmstudio(text: str, page_names: list[str], timeout: float = 30.0) -> dict | None:
    body = {
        "model": CLASSIFY_MODEL,
        "temperature": 0,
        "max_tokens": 300,
        "messages": [
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": (
                "EXISTING PAGES (choose one, exactly as written, or JOURNAL):\n"
                + ", ".join(page_names)
                + f"\n\nNOTE TO FILE:\n{text}"
            )},
        ],
    }
    req = urllib.request.Request(
        CLASSIFY_ENDPOINT,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
        content = data["choices"][0]["message"]["content"]
        return _extract_json(content)
    except (urllib.error.URLError, KeyError, IndexError, ValueError) as exc:
        log(f"classify lmstudio error: {exc}")
        return None


def _call_claude(text: str, page_names: list[str], timeout: float = 60.0) -> dict | None:
    prompt = (
        _SYSTEM
        + "\n\nEXISTING PAGES:\n" + ", ".join(page_names)
        + f"\n\nNOTE TO FILE:\n{text}"
    )
    try:
        r = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True, text=True, timeout=timeout, check=False,
        )
        if r.returncode != 0:
            log(f"classify claude rc={r.returncode}: {r.stderr[:200]}")
            return None
        return _extract_json(r.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        log(f"classify claude error: {exc}")
        return None


def _decide(raw: dict | None, pages: dict[str, str], via: str) -> Decision | None:
    """Turn a model JSON result into a routing Decision, or None if unusable."""
    if not raw:
        return None
    target = str(raw.get("target", "")).strip()
    try:
        conf = float(raw.get("confidence", 0.0))
    except (TypeError, ValueError):
        conf = 0.0
    links = [l for l in (raw.get("links") or []) if l in pages][:3]
    reason = str(raw.get("reason", ""))[:200]

    if not target or target.upper() == _JOURNAL or target not in pages:
        return Decision("journal", links=links, confidence=conf, reason=reason, via=via)
    if conf >= CLASSIFY_PAGE_THRESHOLD:
        return Decision("page", target_file=pages[target], page_name=target,
                        links=links, confidence=conf, reason=reason, via=via)
    if conf >= CLASSIFY_QUARANTINE_FLOOR:
        return Decision("inbox", links=links, confidence=conf, reason=reason, via=via)
    return Decision("journal", links=links, confidence=conf, reason=reason, via=via)


def classify(text: str, pages: dict[str, str]) -> Decision:
    """Decide where `text` should be filed. `pages` maps page name -> filename."""
    page_names = list(pages.keys())
    local = _decide(_call_lmstudio(text, page_names), pages, "local")
    if local is None:
        # Model unreachable or unparseable: never drop, never guess.
        return Decision("journal", via="fallback")
    if CLASSIFY_ESCALATE and local.action == "inbox":
        esc = _decide(_call_claude(text, page_names), pages, "claude")
        if esc is not None and esc.action == "page":
            return esc
    return local
