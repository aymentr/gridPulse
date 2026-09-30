"""AI-assisted dependency inference boundary (architecture §12).

    documents → candidate relationship → Proposer (AI) → evidence verification → INFERRED · UNVALIDATED

A Proposer returns structured proposals with citations. `apply_proposals` verifies every citation
mechanically; a proposal with any unverifiable citation is rejected. Accepted proposals can only
ever become INFERRED · UNVALIDATED — confirmation requires a human review.

`HeuristicProposer` is a rule-based STAND-IN for an AI model. Its rules were written by the author
of the benchmark; its output on the benchmark scenarios is not evidence of inference capability.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Protocol

from .changes import new_finding
from .entities import resolve
from .evidence import cite
from .model import (Dependency, DepType, EntityKind, FindingKind, Location, Provenance,
                    RelConfidence, Validation)
from .store import Store


@dataclass(frozen=True)
class Citation:
    doc_id: str
    version_no: int
    line_start: int
    line_end: int
    quote: str


@dataclass
class DependencyProposal:
    type: DepType
    source: str
    target: str
    reasoning: str
    citations: list[Citation] = field(default_factory=list)
    source_attribute: str = ""


class Proposer(Protocol):
    name: str

    def propose(self, store: Store) -> list[DependencyProposal]: ...


def _cite_from_evidence(store: Store, evidence_id: str) -> Citation:
    ev = store.evidence[evidence_id]
    loc = ev.location
    return Citation(loc.doc_id, loc.version_no, loc.line_start, loc.line_end, ev.quote)


def apply_proposals(store: Store, proposals: list[DependencyProposal], proposer: str):
    accepted, rejected = [], []
    for p in proposals:
        if p.source not in store.entities or p.target not in store.entities:
            rejected.append((p, "unknown entity"))
            continue
        if not p.citations:
            rejected.append((p, "no citations"))
            continue
        evs = [cite(store, Location(c.doc_id, c.version_no, c.line_start, c.line_end), c.quote)
               for c in p.citations]
        if not all(e.verified for e in evs):
            rejected.append((p, "citation could not be verified"))
            store.log("proposal.rejected", source=p.source, target=p.target,
                      reason="unverified citation", proposer=proposer)
            continue
        if any(d.type == p.type and d.source == p.source and d.target == p.target
               for d in store.dependencies.values()):
            rejected.append((p, "relationship already exists"))
            continue
        dep = Dependency(
            id=store.next_id("DEP"), type=p.type, source=p.source, target=p.target,
            confidence=RelConfidence.INFERRED, validation=Validation.UNVALIDATED,
            provenance=[Provenance.AI_INFERRED], evidence_ids=[e.id for e in evs],
            created_at=store.clock(), reasoning=p.reasoning, proposer=proposer,
            source_attribute=p.source_attribute)
        assert dep.validation is Validation.UNVALIDATED     # inference can never confirm
        store.dependencies[dep.id] = dep
        store.log("dependency.inferred", dependency=dep.id, source=p.source, target=p.target,
                  proposer=proposer)
        new_finding(store, FindingKind.DEPENDENCY,
                    f"Inferred: {p.source} {p.type.value} {p.target}"
                    + (f" ({p.source_attribute})" if p.source_attribute else ""),
                    p.target, dep.id, [], dep.evidence_ids)
        accepted.append(dep)
    return accepted, rejected


_PRECONDITION = re.compile(
    r"(?P<act>[A-Z][\w ]+?) shall (?:commence|start) once all (?P<cls>[A-Z]{2}) equipment "
    r"is installed")


class HeuristicProposer:
    """STAND-IN for an AI proposer. Two generic rules; see module docstring."""
    name = "heuristic-stand-in-v0"

    def propose(self, store: Store) -> list[DependencyProposal]:
        return self._precondition_rule(store) + self._same_capability_rule(store)

    def _precondition_rule(self, store):
        """'<Activity> shall commence once all <CLASS> equipment is installed' + equipment of that
        class with a scheduled installation activity → installation PRECEDES activity."""
        out = []
        for v in store.all_latest_versions():
            for i, line in enumerate(v.lines, start=1):
                m = _PRECONDITION.search(line)
                if not m:
                    continue
                target = resolve(store, m.group("act"))
                if not target:
                    continue
                for c in store.claims.values():
                    if c.attribute != "voltage_class" or c.value.value != m.group("cls"):
                        continue
                    for inst in store.claims_for(c.subject, "installation_start"):
                        act = inst.meta.get("activity")
                        if not act:
                            continue
                        out.append(DependencyProposal(
                            DepType.PRECEDES, act, target[0],
                            reasoning=(f"'{m.group(0)}' ({v.doc_id}); {c.subject} is classified "
                                       f"{m.group('cls')} equipment; {act} is the scheduled "
                                       f"installation of {c.subject}. No source states this "
                                       f"relationship for {c.subject} specifically."),
                            citations=[Citation(v.doc_id, v.version_no, i, i, m.group(0)),
                                       _cite_from_evidence(store, c.evidence_ids[0]),
                                       _cite_from_evidence(store, inst.evidence_ids[0])]))
        return out

    def _same_capability_rule(self, store):
        """A facility-level requirement and an equipment specification clause with the same
        capability title → the equipment clause may contribute to the requirement."""
        out = []
        reqs = [c for c in store.claims.values() if c.attribute == "text"
                and store.entities[c.subject].kind == EntityKind.REQUIREMENT
                and "facility" in str(c.value.value).lower()]
        for req in reqs:
            title = req.meta.get("title", "").lower()
            for cl in store.claims.values():
                if not cl.meta.get("clause") or cl.meta.get("title", "").lower() != title:
                    continue
                if store.entities[cl.subject].kind != EntityKind.EQUIPMENT:
                    continue
                v = store.claim_version(cl)
                if v is not store.latest_version(v.doc_id):
                    continue
                keyword = title.split()[0]
                others = sorted({c.subject for c in store.claims.values()
                                 if c.attribute == "description" and c.subject != cl.subject
                                 and keyword in str(c.value.value).lower()})
                basis = (f"no other equipment description mentions '{keyword}'" if not others
                         else f"other equipment mentioning '{keyword}': {', '.join(others)}")
                out.append(DependencyProposal(
                    DepType.SPECIFIES, cl.subject, req.subject,
                    reasoning=(f"{req.subject} ('{req.meta.get('title')}') is a facility-level "
                               f"requirement; {v.doc_id} {v.revision_label} clause "
                               f"{cl.meta['clause']} has the same capability title for "
                               f"{cl.subject}; {basis}. No source states this relationship."),
                    citations=[_cite_from_evidence(store, req.evidence_ids[0]),
                               _cite_from_evidence(store, cl.evidence_ids[0])],
                    source_attribute=f"clause {cl.meta['clause']}"))
        return out
