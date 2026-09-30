"""Change, conflict and stale-reference detection (architecture §8).

Change   = a later observation in the same source lineage differs from an earlier one.
Conflict = the latest observations from different source lineages disagree.
Both can exist for the same subject; neither decides which source is right.
"""
from __future__ import annotations

import re
from collections import defaultdict

from .calc import calendar_days
from .model import (Change, Claim, Conflict, DepType, Finding, FindingKind, FindingStatus)
from .store import Store


def lineage(store: Store, claim: Claim) -> str:
    v = store.claim_version(claim)
    return store.documents[v.doc_id].series


def _order(store: Store, claim: Claim):
    v = store.claim_version(claim)
    return (v.source_date is None, v.source_date, v.version_no)


def _same(a: Claim, b: Claim) -> bool:
    if a.value.kind == "TEXT":
        return re.sub(r"\s+", " ", str(a.value.value)).strip() == \
            re.sub(r"\s+", " ", str(b.value.value)).strip()
    return a.value.value == b.value.value


def _fmt(c: Claim) -> str:
    return c.value.value.strftime("%d %b %Y") if c.value.kind == "DATE" else str(c.value.value)


def new_finding(store, kind, summary, subject, ref_id, claim_ids, evidence_ids) -> Finding:
    f = Finding(id=store.next_id("F"), kind=kind, status=FindingStatus.DETECTED, summary=summary,
                subject=subject, ref_id=ref_id, claim_ids=claim_ids, evidence_ids=evidence_ids,
                created_at=store.clock())
    store.findings[f.id] = f
    store.log("finding.detected", finding=f.id, kind=kind.value, subject=subject)
    return f


def _source(store, c: Claim) -> str:
    v = store.claim_version(c)
    return f"{v.doc_id} {v.revision_label}".strip()


def detect_changes(store: Store) -> list[Finding]:
    out = []
    groups = defaultdict(lambda: defaultdict(list))
    for c in store.claims.values():
        if c.evidence_ids:
            groups[(c.subject, c.attribute)][lineage(store, c)].append(c)
    for (subject, attribute), by_lineage in groups.items():
        for claims in by_lineage.values():
            claims.sort(key=lambda c: _order(store, c))
            for old, new in zip(claims, claims[1:]):
                if _same(old, new):
                    continue
                ch = Change(store.next_id("CHG"), subject, attribute, old.id, new.id)
                store.changes[ch.id] = ch
                if old.value.kind == "DATE":
                    calendar_days(store, old, new, f"{attribute} ({_source(store, old)})",
                                  f"{attribute} ({_source(store, new)})")
                label = old.meta.get("title") or attribute
                summary = (f"{subject} — {label}: {_fmt(old)} → {_fmt(new)}"
                           if old.value.kind != "TEXT" else
                           f"{subject} — {attribute} ({label}) text differs between "
                           f"{_source(store, old)} and {_source(store, new)}")
                out.append(new_finding(store, FindingKind.CHANGE, summary, subject, ch.id,
                                       [old.id, new.id], old.evidence_ids + new.evidence_ids))
        latest = [sorted(cs, key=lambda c: _order(store, c))[-1] for cs in by_lineage.values()]
        dated = [c for c in latest if c.value.kind == "DATE"]
        if len(dated) >= 2 and len({c.value.value for c in dated}) > 1:
            cf = Conflict(store.next_id("CNF"), subject, attribute, [c.id for c in dated])
            store.conflicts[cf.id] = cf
            parts = "; ".join(f"{_source(store, c)}: {_fmt(c)}" for c in dated)
            out.append(new_finding(store, FindingKind.CONFLICT,
                                   f"{subject} — {attribute}: current sources disagree ({parts})",
                                   subject, cf.id, [c.id for c in dated],
                                   [e for c in dated for e in c.evidence_ids]))
    return out


def detect_stale_references(store: Store) -> list[Finding]:
    out = []
    for d in store.dependencies.values():
        cited_rev = d.meta.get("cited_revision")
        if d.type != DepType.REFERENCES or not cited_rev or d.target not in store.versions:
            continue
        latest = store.latest_version(d.target)
        if latest.revision_label and latest.revision_label != cited_rev:
            clause = f", {d.source_attribute}" if d.source_attribute else ""
            out.append(new_finding(
                store, FindingKind.STALE_EVIDENCE,
                f"{d.source} references {d.target} {cited_rev}{clause}; the latest ingested "
                f"revision is {latest.revision_label}", d.source, d.id, [], list(d.evidence_ids)))
    return out
