# Product Workflow

**Phase 0 — LOCKED.** Conceptual workflow; the precise model (states, objects, rules) is defined in
`PHASE_1_ARCHITECTURE.md`.

## 1. The canonical loop

```
REAL WORLD
    ↓
INFORMATION ENTERS ──────────── one universal intake path; read-only against external systems
    ↓
DETECTION ───────────────────── changes, potential events, conflicts, stale/missing evidence
    ↓
EVIDENCE ────────────────────── every claim linked to source → version → location, verified
    ↓
HUMAN REVIEW ────────────────── CONFIRM · REJECT · REQUEST_INVESTIGATION · EDIT_FINDING
    ↓
VALIDATED PROJECT INTELLIGENCE ─ GridPulse's validated view; not the source of truth
    ↓
PROJECT INTELLIGENCE GRAPH ──── entities, dependencies (status + provenance), evidence
    ↓
IMPACT ANALYSIS ─────────────── direct → secondary → milestones → gates → potential exposure
    ↓
ATTENTION / ACTION ──────────── routed to reviewers; humans make determinations
```

The auditable chain for every change to Validated Project Intelligence:

```
SOURCE → DETECTION → FINDING → REVIEW → VALIDATED PROJECT INTELLIGENCE
```

There is no direct-edit path (D-020).

## 2. Stages

### 2.1 Information enters

Supported inputs: **documents, schedules, supplier communications, manual project facts, other
imported information.** A schedule is preferred when available but **not required** — the first user
often does not control it (D-003). All inputs use one universal intake path.

### 2.2 Detection

- A **Change** is a detected difference between two states, versions, records or observations
  (e.g. transformer delivery 15 Jan → 2 Feb; PCS spec Rev 7 → Rev 8).
- An **Event** is something that happened, or is reported to have happened, in the real project
  (e.g. "Supplier informed the project that transformer delivery has moved to 2 February").

```
SOURCE → CHANGE DETECTED → POTENTIAL EVENT → HUMAN REVIEW → CONFIRMED / REJECTED
```

Every AI-detected event starts `DETECTED` and moves to `UNDER_REVIEW`. An authorized user's manual
entry of a known event may be created directly as `CONFIRMED`, with `MANUAL_ENTRY` provenance (D-001).

**Conflicts.** If sources contradict each other (Source A: delivery 15 Jan; Source B: delivery 2 Feb),
GridPulse raises **CONFLICT DETECTED** with both sources, their versions/dates and evidence. It may
explain the conflict but never chooses which source is authoritative. Human review determines the
validated interpretation (D-011).

### 2.3 Evidence

Every claim is traceable: claim → evidence → document version → page/section/chunk (or email message,
schedule activity/field, data row, manual-entry record). Cited evidence is mechanically verified.
Evidence that points to superseded versions is flagged as stale.

### 2.4 Human review — the Review Queue

The Review Queue is **part of the trust architecture**: it is the boundary between AI output and
Validated Project Intelligence.

The reviewer sees: what GridPulse detected · why · the supporting source · what changed · the affected
entity · evidence confidence, relationship confidence and validation status · dependencies that may be
affected (preview) · what remains uncertain.

MVP review actions (D-010):

| Action | Effect |
|---|---|
| `CONFIRM` | Finding applied to Validated Project Intelligence |
| `REJECT` | Nothing applied; rationale recorded |
| `REQUEST_INVESTIGATION` | Creates `INVESTIGATION_REQUESTED`; finding/change stays unresolved; intelligence unchanged |
| `EDIT_FINDING` | Corrects the finding (original preserved); reviewer then confirms or rejects |

No elaborate workflow management. The exact UI is deferred.

### 2.5 Validated Project Intelligence

Confirmed findings update GridPulse's validated view. It may legitimately diverge from a system of
record (e.g. a validated supplier date that the EPC schedule does not yet reflect); the divergence is
shown, never hidden or "corrected".

### 2.6 Project intelligence graph

Dependencies carry a **status** (`INFERRED` / `CONFIRMED` / `REJECTED`) and **provenance**
(`SCHEDULE_DERIVED`, `DOCUMENT_DERIVED`, `AI_INFERRED`, `HUMAN_CONFIRMED`, …). "The schedule says it"
and "an engineer validated it" are never treated as the same kind of evidence (D-023).

### 2.7 Impact analysis

```
Change → direct impacts → dependency propagation → secondary impacts → milestones → gates → potential exposure
```

GridPulse may use inferred dependencies (labelled), perform deterministic calculations and comparisons,
and surface candidate Level 3 implications **only** as potential exposure requiring validation.

### 2.8 Attention / action

GridPulse suggests relevant reviewers (configured project roles) and routes impacts to them. Humans
make the determinations.

## 3. What an investigation must contain

"Review required" alone is not enough. Every impact exposes: affected entity · relationship ·
dependency status · evidence · deterministic calculations · relevant milestone · uncertainty ·
reviewer · unresolved question.

## 4. Ask GridPulse (MVP, narrow)

Ask GridPulse answers questions from Validated Project Intelligence with evidence. It is **not** a
general-purpose chatbot. Each answer contains: answer · supporting evidence · affected entities ·
dependency chain · uncertainty · reviewer/validation status. If an answer cannot be supported by
evidence, GridPulse says so (D-019).

Example: *"What is currently blocking energization?"*

## 5. The first product demonstration — transformer delivery change

Canonical definition: `PHASE_1_ARCHITECTURE.md` §16.

| Item | Date |
|---|---|
| Transformer delivery (original) | 15 January |
| Transformer installation | 15 January |
| HV commissioning | 10 February |
| Grid compliance testing | 20 February |
| Energization | 1 March |

Supplier communication: *"Transformer delivery is now expected February 2."*

GridPulse:

1. detects the change
2. extracts old and new dates
3. links the evidence
4. creates a potential event
5. marks it for review (`DETECTED` → `UNDER_REVIEW`)
6. human confirms it
7. updates Validated Project Intelligence
8. traverses project dependencies — including **at least one AI-inferred dependency** (D-025)
9. identifies potential downstream impact
10. identifies relevant reviewers
11. clearly separates facts, inferences and conclusions

Expected output:

| | |
|---|---|
| CHANGE | Delivery date changed 15 Jan → 2 Feb |
| FACT | 18 calendar days difference relative to the planned installation date |
| DEPENDENCY | Transformer delivery → transformer installation |
| SECONDARY DEPENDENCY | Transformer installation → downstream commissioning activity (**AI-inferred, validation required**) |
| POTENTIAL EXPOSURE | Downstream milestone may require review |
| VALIDATION | Project-control / electrical engineering review required |

GridPulse must **not** say: *"Energization will be delayed."* Exact downstream engineering
consequences are never asserted without evidence.

## 6. What the user eventually experiences

These are views over the intelligence model, not generic PM features.

| Area | Purpose |
|---|---|
| Project Overview | Current Validated Project Intelligence |
| Data Room | Information GridPulse has read (not a document-management system) |
| Events | What happened or is reported to have happened |
| Review Queue | Trust boundary — items requiring validation |
| Changes | All detected changes with lifecycle `DETECTED → UNDER_REVIEW → CONFIRMED / REJECTED` |
| Evidence | Why GridPulse believes something |
| Requirements | Requirements and supporting / missing evidence |
| Dependencies | Relationships with status and provenance |
| Impact | What a confirmed change may affect |
| Gates | The fixed MVP gate set as intelligence checkpoints |
| Ask GridPulse | Narrow, evidence-backed questions |
