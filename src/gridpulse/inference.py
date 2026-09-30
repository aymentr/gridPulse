"""Deterministic application of AI proposals (architecture §12; milestone §4, §5, §7, §8).

    documents → candidate (LLM proposal) → evidence verification → INFERRED · UNVALIDATED → review

The LLM (any provider) only PROPOSES. Everything trust-bearing happens here, deterministically:
- every citation is re-verified mechanically against the document (`evidence.cite`);
- a proposal whose reasoning contains Level-3 wording is rejected (`safety`);
- accepted dependencies can only ever be INFERRED · UNVALIDATED · AI_INFERRED;
- accepted entity links are recorded as UNVALIDATED aliases and never merge two entities;
- change links are corroborated against deterministic detection and never create a change.

Confirmation always requires a human review (see gridpulse.review).

`HeuristicProposer` is a rule-based STAND-IN used by MockProvider so the pipeline runs offline. Its
rules were written by the author of the benchmark; its output is not evidence of AI capability.
"""
from __future__ import annotations

import re

from . import safety
from .changes import new_finding
from .entities import resolve
from .evidence import cite
from .model import (Dependency, DepType, EntityAlias, EntityKind, FindingKind, Location, Provenance,
                    RelConfidence, Validation)
from .providers.base import (Citation, ChangeLinkProposal, DependencyProposal, EntityLinkProposal)
from .store import Store


def _cite_from_evidence(store: Store, evidence_id: str) -> Citation:
    ev = store.evidence[evidence_id]
    loc = ev.location
    return Citation(loc.doc_id, loc.version_no, loc.line_start, loc.line_end, ev.quote)


def _reasoning_is_safe(reasoning: str) -> bool:
    return not safety.violations(reasoning or "")


def apply_proposals(store: Store, proposals: list[DependencyProposal], proposer: str,
                    invocation=None):
    """Verify and apply dependency proposals. Returns (accepted, rejected)."""
    accepted, rejected = [], []
    for p in proposals:
        if p.source not in store.entities or p.target not in store.entities:
            rejected.append((p, "unknown entity"))
            continue
        if not _reasoning_is_safe(p.reasoning):                 # §8 — backend-enforced boundary
            rejected.append((p, "level-3 wording in reasoning"))
            store.log("proposal.rejected", source=p.source, target=p.target,
                      reason="level-3 wording", proposer=proposer)
            continue
        if not p.citations:
            rejected.append((p, "no citations"))
            continue
        evs = [cite(store, Location(c.doc_id, c.version_no, c.line_start, c.line_end), c.quote)
               for c in p.citations]
        if not all(e.verified for e in evs):                    # §4 — no fabricated evidence
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
        assert dep.validation is Validation.UNVALIDATED         # inference can never confirm
        assert dep.confidence is RelConfidence.INFERRED
        store.dependencies[dep.id] = dep
        store.log("dependency.inferred", dependency=dep.id, source=p.source, target=p.target,
                  proposer=proposer)
        new_finding(store, FindingKind.DEPENDENCY,
                    f"Inferred: {p.source} {p.type.value} {p.target}"
                    + (f" ({p.source_attribute})" if p.source_attribute else ""),
                    p.target, dep.id, [], dep.evidence_ids)
        accepted.append(dep)
    if invocation is not None:
        invocation.accepted, invocation.rejected = len(accepted), len(rejected)
        invocation.evidence_refs = [e for d in accepted for e in d.evidence_ids]
    return accepted, rejected


def apply_entity_links(store: Store, proposals: list[EntityLinkProposal], proposer: str,
                       invocation=None):
    """Record proposed free-text → entity links as UNVALIDATED aliases (milestone §5).

    The deterministic layer decides the representation: a link becomes an alias on an EXISTING
    entity. It never merges two canonical entities, and it never marks a link CONFIRMED.
    Returns (accepted, rejected)."""
    accepted, rejected = [], []
    for p in proposals:
        if p.entity_id not in store.entities:
            rejected.append((p, "unknown entity"))
            continue
        if not _reasoning_is_safe(p.reasoning):
            rejected.append((p, "level-3 wording in reasoning"))
            continue
        # A mention that itself resolves to a DIFFERENT canonical entity must not be relabelled:
        # that would be an entity merge, which the backend never allows.
        existing = resolve(store, p.mention)
        if existing and existing[0] != p.entity_id and p.mention in store.entities:
            rejected.append((p, "refusing to merge two canonical entities"))
            store.log("entity_link.rejected", mention=p.mention, entity=p.entity_id,
                      reason="merge refused", proposer=proposer)
            continue
        if any(a.entity_id == p.entity_id and a.alias.lower() == p.mention.lower()
               for a in store.aliases):
            accepted.append(p)                                  # already recorded; no re-citation
            continue
        ev = None
        if p.citation is not None:
            c = p.citation
            ev = cite(store, Location(c.doc_id, c.version_no, c.line_start, c.line_end), c.quote)
            if not ev.verified:                                 # §4 — no fabricated evidence
                rejected.append((p, "citation could not be verified"))
                store.log("entity_link.rejected", mention=p.mention, entity=p.entity_id,
                          reason="unverified citation", proposer=proposer)
                continue
        store.add_alias(EntityAlias(entity_id=p.entity_id, alias=p.mention,
                                    basis=f"AI-proposed link ({proposer}); verified citation",
                                    evidence_id=ev.id if ev else None,
                                    validation=Validation.UNVALIDATED))
        accepted.append(p)
    if invocation is not None:
        invocation.accepted, invocation.rejected = len(accepted), len(rejected)
    return accepted, rejected


def apply_change_links(store: Store, proposals: list[ChangeLinkProposal], proposer: str,
                       invocation=None):
    """Corroborate proposed claim-identity links against deterministic change/conflict detection
    (milestone §6). The backend OWNS change creation: this never writes to store.changes or
    store.conflicts. A link is accepted only if the claims exist, share the subject, and a
    deterministic CHANGE or CONFLICT already exists for that (subject, attribute).
    Returns (accepted, rejected)."""
    accepted, rejected = [], []
    detected = {(c.subject, c.attribute) for c in store.changes.values()}
    detected |= {(c.subject, c.attribute) for c in store.conflicts.values()}
    for p in proposals:
        if not _reasoning_is_safe(p.reasoning):
            rejected.append((p, "level-3 wording in reasoning"))
            continue
        claims = [store.claims[i] for i in p.claim_ids if i in store.claims]
        if len(claims) != len(p.claim_ids) or len(claims) < 2:
            rejected.append((p, "unknown or insufficient claims"))
            continue
        if any(c.subject != p.subject for c in claims):
            rejected.append((p, "claims do not share the proposed subject"))
            continue
        if (p.subject, p.attribute) not in detected:
            rejected.append((p, "no deterministic change/conflict corroborates this link"))
            continue
        store.log("change_link.corroborated", subject=p.subject, attribute=p.attribute,
                  claims=",".join(p.claim_ids), proposer=proposer)
        accepted.append(p)
    if invocation is not None:
        invocation.accepted, invocation.rejected = len(accepted), len(rejected)
    return accepted, rejected


# --- rule-based STAND-IN (used by MockProvider so the pipeline runs offline) ----------------

_PRECONDITION = re.compile(
    r"(?P<act>[A-Z][\w ]+?) shall (?:commence|start) once all (?P<cls>[A-Z]{2}) equipment "
    r"is installed")


class HeuristicProposer:
    """Rule-based dependency proposer. See module docstring — not evidence of AI capability."""
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
