"""Review queue — the trust boundary (architecture §7.1, §7.6).

Only a configured reviewer's explicit action moves a finding to CONFIRMED or REJECTED. Confirming a
DEPENDENCY finding is the only way an inferred relationship becomes CONFIRMED.
"""
from __future__ import annotations

from .model import (FindingKind, FindingStatus, Provenance, Review, ReviewAction, Reviewer,
                    Validation)
from .store import Store


class ReviewError(Exception):
    pass


class ReviewQueue:
    def __init__(self, store: Store):
        self.store = store

    def add_reviewer(self, reviewer_id: str, roles: list[str]) -> None:
        self.store.reviewers[reviewer_id] = Reviewer(reviewer_id, roles)

    def enqueue_detected(self) -> int:
        n = 0
        for f in self.store.findings.values():
            if f.status == FindingStatus.DETECTED:
                f.status = FindingStatus.UNDER_REVIEW
                self.store.log("finding.enqueued", finding=f.id)
                n += 1
        return n

    def pending(self):
        return [f for f in self.store.findings.values()
                if f.status in (FindingStatus.UNDER_REVIEW, FindingStatus.INVESTIGATION_REQUESTED)]

    def describe(self, finding_id: str) -> dict:
        s = self.store
        f = s.findings[finding_id]
        out = {"finding": f.id, "kind": f.kind.value, "status": f.status.value,
               "summary": f.summary, "affected_entity": f.subject,
               "evidence": [{"id": e, "citation": s.evidence[e].location.describe(),
                             "quote": s.evidence[e].quote, "verified": s.evidence[e].verified,
                             "confidence": s.evidence[e].confidence.value}
                            for e in f.evidence_ids]}
        if f.kind == FindingKind.DEPENDENCY:
            d = s.dependencies[f.ref_id]
            out["dependency"] = {"type": d.type.value, "source": d.source, "target": d.target,
                                 "confidence": d.confidence.value,
                                 "validation": d.validation.value,
                                 "provenance": [p.value for p in d.provenance],
                                 "reasoning": d.reasoning, "proposer": d.proposer}
        claim_ids = set(f.claim_ids)
        out["calculations"] = [{"operation": c.operation, "result": c.result, "unit": c.unit}
                               for c in s.calculations.values()
                               if claim_ids and {i["claim_id"] for i in c.inputs} <= claim_ids]
        return out

    # --- actions --------------------------------------------------------------------------
    def _authorize(self, reviewer_id: str, role: str) -> None:
        r = self.store.reviewers.get(reviewer_id)
        if r is None or role not in r.roles:
            raise ReviewError(f"{reviewer_id} is not configured for role '{role}'")

    def _record(self, f, reviewer_id, role, action, rationale, before=None, after=None):
        rv = Review(self.store.next_id("RV"), f.id, reviewer_id, role, action, rationale,
                    self.store.clock(), before, after)
        self.store.reviews.append(rv)
        self.store.log("review", finding=f.id, action=action.value, reviewer=reviewer_id,
                       role=role, status=f.status.value)
        return rv

    def _open(self, finding_id):
        f = self.store.findings[finding_id]
        if f.status not in (FindingStatus.UNDER_REVIEW, FindingStatus.INVESTIGATION_REQUESTED):
            raise ReviewError(f"{finding_id} is not open for review ({f.status.value})")
        return f

    def confirm(self, finding_id, reviewer_id, role, rationale=""):
        self._authorize(reviewer_id, role)
        f = self._open(finding_id)
        f.status = FindingStatus.CONFIRMED
        self._apply(f, Validation.CONFIRMED, Provenance.HUMAN_CONFIRMED)
        return self._record(f, reviewer_id, role, ReviewAction.CONFIRM, rationale)

    def reject(self, finding_id, reviewer_id, role, rationale):
        if not rationale.strip():
            raise ReviewError("a rationale is required to reject")
        self._authorize(reviewer_id, role)
        f = self._open(finding_id)
        f.status = FindingStatus.REJECTED
        self._apply(f, Validation.REJECTED, Provenance.HUMAN_REJECTED)
        return self._record(f, reviewer_id, role, ReviewAction.REJECT, rationale)

    def request_investigation(self, finding_id, reviewer_id, role, question):
        if not question.strip():
            raise ReviewError("the investigation question is required")
        self._authorize(reviewer_id, role)
        f = self._open(finding_id)
        f.status = FindingStatus.INVESTIGATION_REQUESTED    # intelligence unchanged
        return self._record(f, reviewer_id, role, ReviewAction.REQUEST_INVESTIGATION, question)

    def edit(self, finding_id, reviewer_id, role, summary, rationale):
        if not rationale.strip():
            raise ReviewError("a rationale is required to edit")
        self._authorize(reviewer_id, role)
        f = self._open(finding_id)
        before = {"summary": f.summary}
        f.revisions.append(before)
        f.summary = summary
        f.status = FindingStatus.UNDER_REVIEW
        return self._record(f, reviewer_id, role, ReviewAction.EDIT_FINDING, rationale,
                            before, {"summary": summary})

    def _apply(self, f, validation, provenance):
        s = self.store
        if f.kind == FindingKind.DEPENDENCY:
            d = s.dependencies[f.ref_id]
            d.validation = validation
            d.provenance.append(provenance)
        elif f.kind == FindingKind.CHANGE and validation == Validation.CONFIRMED:
            new = s.claims[s.changes[f.ref_id].new_claim]
            new.validation = Validation.CONFIRMED
            new.provenance.append(provenance)
