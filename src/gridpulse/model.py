"""Domain model for the Phase 1.5 spike (PHASE_1_ARCHITECTURE.md §3–§9).

Values are never stored as bare fields on entities: every attribute value is a Claim that carries
provenance, evidence and validation status.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from enum import Enum


class Level(Enum):
    FACT = 1            # directly supported or deterministically calculated
    INFERENCE = 2       # evidence-backed relationship or analytical inference
    DETERMINATION = 3   # human only — never produced by the system


class Validation(str, Enum):
    UNVALIDATED = "UNVALIDATED"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


class RelConfidence(str, Enum):
    EXPLICIT = "EXPLICIT"
    INFERRED = "INFERRED"


class EvidenceConfidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Freshness(str, Enum):
    CURRENT = "CURRENT"
    STALE = "STALE"
    UNAVAILABLE = "UNAVAILABLE"


class Provenance(str, Enum):
    SCHEDULE_DERIVED = "SCHEDULE_DERIVED"
    DOCUMENT_DERIVED = "DOCUMENT_DERIVED"
    STRUCTURED_IMPORT = "STRUCTURED_IMPORT"
    AI_EXTRACTED = "AI_EXTRACTED"
    AI_INFERRED = "AI_INFERRED"
    CALCULATED = "CALCULATED"
    MANUAL_ENTRY = "MANUAL_ENTRY"
    HUMAN_CONFIRMED = "HUMAN_CONFIRMED"
    HUMAN_EDITED = "HUMAN_EDITED"
    HUMAN_REJECTED = "HUMAN_REJECTED"


class EntityKind(str, Enum):
    EQUIPMENT = "EQUIPMENT"
    PARTY = "PARTY"
    CONTRACT = "CONTRACT"
    REQUIREMENT = "REQUIREMENT"
    MILESTONE = "MILESTONE"
    ACTIVITY = "ACTIVITY"
    TEST = "TEST"
    GATE = "GATE"
    DOCUMENT_ARTIFACT = "DOCUMENT_ARTIFACT"


class DepType(str, Enum):
    PRECEDES = "PRECEDES"
    REFERENCES = "REFERENCES"
    SPECIFIES = "SPECIFIES"
    VERIFIES = "VERIFIES"
    CONTRIBUTES_TO = "CONTRIBUTES_TO"
    SUPPLIES = "SUPPLIES"


class FindingKind(str, Enum):
    CHANGE = "CHANGE"
    DEPENDENCY = "DEPENDENCY"
    CONFLICT = "CONFLICT"
    STALE_EVIDENCE = "STALE_EVIDENCE"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    FACT = "FACT"


class FindingStatus(str, Enum):
    DETECTED = "DETECTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    INVESTIGATION_REQUESTED = "INVESTIGATION_REQUESTED"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class ReviewAction(str, Enum):
    CONFIRM = "CONFIRM"
    REJECT = "REJECT"
    REQUEST_INVESTIGATION = "REQUEST_INVESTIGATION"
    EDIT_FINDING = "EDIT_FINDING"


# --- documents and evidence -----------------------------------------------------------------

@dataclass(frozen=True)
class Document:
    doc_id: str
    series: str
    title: str


@dataclass(frozen=True)
class DocumentVersion:
    """Immutable once ingested. A changed file becomes a new version, never an overwrite."""
    doc_id: str
    version_no: int
    revision_label: str
    source_path: str
    source_date: dt.date | None
    ingested_at: dt.datetime
    content_hash: str
    lines: tuple[str, ...]

    @property
    def key(self) -> str:
        return f"{self.doc_id}@v{self.version_no}"


@dataclass(frozen=True)
class Location:
    doc_id: str
    version_no: int
    line_start: int          # 1-based, inclusive
    line_end: int            # 1-based, inclusive
    section: str = ""

    def describe(self) -> str:
        span = f"line {self.line_start}" if self.line_start == self.line_end \
            else f"lines {self.line_start}–{self.line_end}"
        sec = f", {self.section}" if self.section else ""
        return f"{self.doc_id} v{self.version_no}{sec}, {span}"


@dataclass
class Evidence:
    id: str
    location: Location
    quote: str
    verified: bool
    confidence: EvidenceConfidence
    freshness: Freshness = Freshness.CURRENT
    note: str = ""


# --- entities and claims --------------------------------------------------------------------

@dataclass
class Entity:
    id: str
    kind: EntityKind
    name: str


@dataclass
class EntityAlias:
    entity_id: str
    alias: str
    basis: str                      # why this alias maps to the entity
    evidence_id: str | None
    validation: Validation = Validation.UNVALIDATED


@dataclass(frozen=True)
class ClaimValue:
    kind: str                       # DATE | TEXT | RANGE | NUMBER | LIST
    value: object
    unit: str = ""
    text: str = ""


@dataclass
class Claim:
    id: str
    subject: str                    # entity id
    attribute: str
    value: ClaimValue
    level: Level
    provenance: list[Provenance]
    evidence_ids: list[str]
    validation: Validation
    evidence_confidence: EvidenceConfidence
    created_at: dt.datetime
    qualifier: str = ""             # e.g. "reported: supplier advised"
    meta: dict = field(default_factory=dict)


# --- relationships, findings, analysis ------------------------------------------------------

@dataclass
class Dependency:
    id: str
    type: DepType
    source: str                     # entity id
    target: str                     # entity id
    confidence: RelConfidence
    validation: Validation
    provenance: list[Provenance]
    evidence_ids: list[str]
    created_at: dt.datetime
    reasoning: str = ""
    proposer: str = ""
    source_attribute: str = ""
    meta: dict = field(default_factory=dict)


@dataclass
class Change:
    id: str
    subject: str
    attribute: str
    old_claim: str
    new_claim: str


@dataclass
class Conflict:
    id: str
    subject: str
    attribute: str
    claim_ids: list[str]


@dataclass
class Finding:
    id: str
    kind: FindingKind
    status: FindingStatus
    summary: str
    subject: str
    ref_id: str | None              # Change / Conflict / Dependency id where applicable
    claim_ids: list[str]
    evidence_ids: list[str]
    created_at: dt.datetime
    revisions: list[dict] = field(default_factory=list)


@dataclass
class Calculation:
    id: str
    operation: str
    inputs: list[dict]              # each: {label, value, claim_id}
    result: object
    unit: str
    note: str = ""
    provenance: Provenance = Provenance.CALCULATED


@dataclass
class Reviewer:
    id: str
    roles: list[str]


@dataclass
class Review:
    id: str
    finding_id: str
    reviewer_id: str
    role: str
    action: ReviewAction
    rationale: str
    at: dt.datetime
    before: dict | None = None
    after: dict | None = None
