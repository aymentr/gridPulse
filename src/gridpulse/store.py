"""In-memory store with deterministic ids and an append-only audit log (architecture I-7)."""
from __future__ import annotations

import datetime as dt
from collections import defaultdict
from typing import Callable

from .model import (Claim, Calculation, Change, Conflict, Dependency, Document, DocumentVersion,
                    Entity, EntityAlias, Evidence, Finding, Review, Reviewer)


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


class Store:
    def __init__(self, clock: Callable[[], dt.datetime] = utc_now):
        self.clock = clock
        self._counters: dict[str, int] = defaultdict(int)
        self.documents: dict[str, Document] = {}
        self.versions: dict[str, list[DocumentVersion]] = defaultdict(list)
        self.evidence: dict[str, Evidence] = {}
        self.entities: dict[str, Entity] = {}
        self.aliases: list[EntityAlias] = []
        self.claims: dict[str, Claim] = {}
        self.dependencies: dict[str, Dependency] = {}
        self.changes: dict[str, Change] = {}
        self.conflicts: dict[str, Conflict] = {}
        self.findings: dict[str, Finding] = {}
        self.calculations: dict[str, Calculation] = {}
        self.reviewers: dict[str, Reviewer] = {}
        self.reviews: list[Review] = []
        self.audit: list[dict] = []

    def next_id(self, prefix: str) -> str:
        self._counters[prefix] += 1
        return f"{prefix}-{self._counters[prefix]:04d}"

    def log(self, event: str, **data) -> None:
        self.audit.append({"at": self.clock().isoformat(), "event": event, **data})

    # --- documents ------------------------------------------------------------------------
    def version(self, doc_id: str, version_no: int) -> DocumentVersion:
        for v in self.versions[doc_id]:
            if v.version_no == version_no:
                return v
        raise KeyError(f"{doc_id} v{version_no}")

    def latest_version(self, doc_id: str) -> DocumentVersion:
        return self.versions[doc_id][-1]

    def all_latest_versions(self) -> list[DocumentVersion]:
        return [vs[-1] for vs in self.versions.values() if vs]

    # --- entities --------------------------------------------------------------------------
    def entity(self, entity_id: str) -> Entity:
        return self.entities[entity_id]

    def add_entity(self, entity: Entity) -> Entity:
        if entity.id not in self.entities:
            self.entities[entity.id] = entity
            self.log("entity.created", entity=entity.id, kind=entity.kind.value)
        return self.entities[entity.id]

    def add_alias(self, alias: EntityAlias) -> None:
        for a in self.aliases:
            if a.entity_id == alias.entity_id and a.alias.lower() == alias.alias.lower():
                return
        self.aliases.append(alias)
        self.log("alias.recorded", entity=alias.entity_id, alias=alias.alias, basis=alias.basis)

    # --- claims ----------------------------------------------------------------------------
    def add_claim(self, claim: Claim) -> Claim:
        self.claims[claim.id] = claim
        self.log("claim.created", claim=claim.id, subject=claim.subject, attribute=claim.attribute,
                 level=claim.level.name, validation=claim.validation.value)
        return claim

    def claims_for(self, subject: str, attribute: str | None = None) -> list[Claim]:
        return [c for c in self.claims.values()
                if c.subject == subject and (attribute is None or c.attribute == attribute)]

    def claim_version(self, claim: Claim) -> DocumentVersion | None:
        if not claim.evidence_ids:
            return None
        loc = self.evidence[claim.evidence_ids[0]].location
        return self.version(loc.doc_id, loc.version_no)
