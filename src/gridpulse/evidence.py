"""Evidence and citation integrity (architecture §6).

A citation is accepted only if the quoted text actually occurs within the cited lines of the cited
document version. Unverifiable citations are kept visible but downgraded (verified=False, LOW).
"""
from __future__ import annotations

import re

from .model import Evidence, EvidenceConfidence, Freshness, Location
from .store import Store


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("*", "")).strip().lower()


def quote_at(store: Store, loc: Location, quote: str) -> bool:
    try:
        version = store.version(loc.doc_id, loc.version_no)
    except KeyError:
        return False
    if not (1 <= loc.line_start <= loc.line_end <= len(version.lines)):
        return False
    span = " ".join(version.lines[loc.line_start - 1:loc.line_end])
    return bool(quote.strip()) and _norm(quote) in _norm(span)


def cite(store: Store, loc: Location, quote: str,
         confidence: EvidenceConfidence = EvidenceConfidence.HIGH) -> Evidence:
    """Create evidence; mechanically verified at creation time."""
    ok = quote_at(store, loc, quote)
    ev = Evidence(
        id=store.next_id("EV"), location=loc, quote=quote.strip(), verified=ok,
        confidence=confidence if ok else EvidenceConfidence.LOW,
        note="" if ok else "citation could not be verified at the cited location")
    store.evidence[ev.id] = ev
    store.log("evidence.created", evidence=ev.id, location=loc.describe(), verified=ok)
    return ev


def reverify(store: Store, evidence_id: str) -> bool:
    ev = store.evidence[evidence_id]
    ok = quote_at(store, ev.location, ev.quote)
    if not ok and ev.verified:
        ev.verified = False
        ev.confidence = EvidenceConfidence.LOW
        ev.note = "citation failed re-verification"
        store.log("evidence.downgraded", evidence=ev.id)
    return ok


def refresh_freshness(store: Store) -> None:
    """Evidence pointing at a superseded version is STALE if the quote no longer appears in the
    latest version of the same document (architecture §6.4)."""
    for ev in store.evidence.values():
        latest = store.latest_version(ev.location.doc_id)
        if latest.version_no == ev.location.version_no:
            continue
        text = _norm(" ".join(latest.lines))
        if _norm(ev.quote) not in text and ev.freshness != Freshness.STALE:
            ev.freshness = Freshness.STALE
            store.log("evidence.stale", evidence=ev.id)


def line_of(version, needle: str, start: int = 1) -> int | None:
    """1-based line number of the first line (from `start`) containing needle."""
    n = _norm(needle)
    for i in range(start - 1, len(version.lines)):
        if n in _norm(version.lines[i]):
            return i + 1
    return None
