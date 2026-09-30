"""Entity resolution: tags and recorded aliases only. No fuzzy matching; ambiguity → unresolved."""
from __future__ import annotations

import re

from .store import Store

_GROUP = re.compile(r"^(?P<pre>(?:[A-Z]+-)+)(?P<a>\d+)\s*…\s*(?P<rest>.+)$")


def normalize_tag(raw: str) -> str:
    """'PCS-01 … PCS-28' / 'PCS-01…28' → 'PCS-01…PCS-28'. Plain tags are returned stripped."""
    t = raw.strip()
    m = _GROUP.match(t)
    if not m:
        return t
    rest = m.group("rest").strip()
    if rest.isdigit():
        rest = m.group("pre") + rest
    return f"{m.group('pre')}{m.group('a')}…{rest}"


TAG_TOKEN = re.compile(r"(?:[A-Z]{1,4}-)+\d+(?:\s*…\s*(?:(?:[A-Z]{1,4}-)+)?\d+)?")


def tags_in(text: str) -> list[str]:
    return [normalize_tag(m.group(0)) for m in TAG_TOKEN.finditer(text)]


def resolve(store: Store, text: str) -> tuple[str, str] | None:
    """Return (entity_id, basis) or None. Unique exact tag or unique recorded alias only."""
    t = normalize_tag(text)
    if t in store.entities:
        return t, "exact identifier"
    matches = {a.entity_id for a in store.aliases if a.alias.lower() == text.strip().lower()}
    if len(matches) == 1:
        eid = matches.pop()
        return eid, "recorded alias"
    return None


def known_tags_in(store: Store, text: str) -> list[str]:
    return [t for t in tags_in(text) if t in store.entities]
