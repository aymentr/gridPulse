# Core Concepts

The shared vocabulary for GridPulse. Definitions are **conceptual**; the technical data model will be
designed in a later phase. No database schema is implied.

---

## Project

A single complex infrastructure undertaking (initially a large BESS — e.g. 100 MW / 400 MWh — or other
grid-connected asset).

## System of Record

An external system that is authoritative for some part of the project: Aconex (documents / contractual
record), Primavera P6 / Primavera Cloud or Microsoft Project (schedule), SharePoint, Procore,
engineering systems (engineering data), commissioning systems, spreadsheets, email.
GridPulse **reads from** these and, in the MVP, **never writes to them** (D-002).

## Source Record

A specific item of information that entered GridPulse: a document, drawing, email, schedule, RFI,
change order, meeting minutes, test report, manual entry, etc. Source records have **versions**.

## Evidence

The traceable link between a claim and the exact place in a source that supports it:

```
CLAIM → SOURCE → DOCUMENT / EMAIL / SCHEDULE / OTHER RECORD → VERSION → PAGE / SECTION / CHUNK / LOCATION
```

A user must always be able to ask "why does GridPulse believe this?" and inspect the answer.

## Three Levels of Information

| Level | Name | Definition | Example | Who asserts it |
|---|---|---|---|---|
| **1** | **Fact** | Directly supported information, including **deterministic calculations and comparisons** on evidenced values | "Supplier states delivery moved from Jan 12 to Feb 2." / "The new delivery date is 21 calendar days later than the previous planned date." | GridPulse, with evidence |
| **2** | **Dependency / Inference** | An evidence-backed relationship or analytical inference | "Transformer installation appears to precede HV commissioning." | GridPulse, labelled as dependency/inference with status |
| **3** | **Engineering / Project Conclusion** | A consequential technical or project decision | "Energization will be delayed by 21 days." | **Humans only** |

Every claim GridPulse shows carries its level. Presenting Level 2 as Level 1, or producing Level 3
autonomously, is a defect (D-005).

## Change

**A difference between two states or versions** (D-009).

Examples: PCS specification Rev 7 → Rev 8; transformer delivery Jan 12 → Feb 2.

A Change is detected by comparing information. A detected Change may generate a Potential Event.

## Project Event

**Something that happened, or is reported to have happened, in the real project** (D-009).

Example: *"Supplier informed the project that transformer delivery has moved to February 2."*

Conceptual attributes: event type, affected entity, old state, new state, reason, source, evidence,
detected time, effective time, detection method (e.g. AI detection, manual entry), confidence, review
status, reviewer, review decision.

### Relationship between Change and Event

```
SOURCE → CHANGE DETECTED → POTENTIAL EVENT → HUMAN REVIEW → CONFIRMED PROJECT EVENT
```

### Event review status

| Status | Meaning |
|---|---|
| `NEEDS_REVIEW` | Proposed (every AI-detected event starts here in the MVP); does **not** affect the trusted state |
| `CONFIRMED` | Accepted by a reviewer, or entered manually by an authorized user; updates the trusted state |
| `REJECTED` | Rejected by a reviewer; does not affect the trusted state |

(How "request more investigation" is represented is open — D-022.)

### Event types

Keep the taxonomy **small and extensible** (D-007). Prefer broad categories with attributes over
granular types. For example, use `DELIVERY_DATE_CHANGE` with old date, new date, reason and affected
entity — **not** separate `SHIPMENT_DELAY`, `SUPPLIER_DELAY`, `TRANSPORT_DELAY`, `LOGISTICS_DELAY`,
`EQUIPMENT_DELAY` types. Descriptive labels such as "delivery delay" may be derived from the underlying
state change.

Working category list (to be refined in design, see D-007):

`DELIVERY_DATE_CHANGE` · `SPECIFICATION_CHANGE` · `SCHEDULE_CHANGE` · `TEST_FAILURE` ·
`EQUIPMENT_FAILURE` · `RFI` · `CHANGE_ORDER` · `PERMIT_CHANGE` · `GRID_OPERATOR_DECISION` ·
`CONSTRUCTION_PROGRESS` · `OTHER`

(The original `SHIPMENT_DELAY` type is absorbed into `DELIVERY_DATE_CHANGE`.)

## Review Queue

The set of items awaiting human validation. It is **part of the trust architecture**: the only path by
which AI-detected information can enter the trusted project state. See `PRODUCT_WORKFLOW.md` §2.4 for
what a reviewer sees and can do.

## Trusted Project State (Validated Intelligence State)

GridPulse's current, human-validated understanding of the project — an evidence-backed representation
of what the information across authoritative systems collectively implies about the current project
state. It changes only through confirmed Project Events and human corrections.

It is **not** the contractual or authoritative source of truth (D-021). Where it differs from a system
of record (e.g. a confirmed supplier date that P6 does not yet reflect), that difference is itself
useful information, not an error to overwrite.

## Project Entity

Anything the project is made of or governed by: requirements, documents, equipment, suppliers,
contracts, parties, engineering information, tasks, milestones, risks, issues, tests, approvals, gates.

BESS examples: battery containers, PCS, transformers, MV equipment, HV equipment, protection systems,
PPC, EMS, SCADA, metering, communications, fire protection, grid connection, EPC, suppliers,
construction activities, commissioning tests, grid compliance tests, energization, COD.

## Dependency

A relationship where one project element depends on or affects another. Every dependency carries
evidence and a **status** (D-004):

| Status | Meaning | Example |
|---|---|---|
| `CONFIRMED` | Explicit in a source, or confirmed by a human | Schedule states Transformer Installation depends on Transformer Delivery |
| `INFERRED` | Proposed by AI from project information | AI infers installation affects HV commissioning |
| `REJECTED` | Rejected by a human | Reviewer rejects that inferred link |

Impact analysis may use `INFERRED` dependencies but must label them. An inferred relationship is never
presented as established fact. Human confirmation strengthens the trusted graph.

## Project Intelligence Graph

The central concept: a connected representation of project entities, events and dependencies, each
backed by evidence. Reconstructed from existing project information (D-003); lets GridPulse
investigate the consequences of changes.

```
Transformer → Delivery → Installation → HV Commissioning → Grid Compliance Testing → Energization
```

## Impact Analysis

Traversing dependencies from a confirmed event to identify what **may** be affected — entities,
milestones, gates, risks, relevant reviewers — with deterministic calculations, stated uncertainty and
unresolved questions. Output is **potential impact requiring human attention**, never a Level 3
conclusion.

## Requirement

A project or grid requirement with supporting evidence. GridPulse can identify requirements and flag
where evidence is missing.

## Gate

An important project checkpoint: grid connection, engineering completion, procurement readiness,
construction completion, commissioning, grid compliance, energization, COD.

## Authorized User / Reviewer

A person permitted to confirm, reject or correct events and dependencies, and to enter confirmed events
manually. GridPulse may **identify** relevant reviewers; humans make the decisions.

## Investigation

The work of determining what changed, what it affects and what evidence supports it. GridPulse's
purpose is to compress the time a technical professional spends on investigation while preserving
evidence precision and recall.

## Glossary of domain acronyms

| Term | Meaning |
|---|---|
| BESS | Battery Energy Storage System |
| PCS | Power Conversion System |
| PPC | Power Plant Controller |
| EMS | Energy Management System |
| SCADA | Supervisory Control and Data Acquisition |
| MV / HV | Medium Voltage / High Voltage |
| EPC | Engineering, Procurement and Construction (contractor) |
| OE | Owner's Engineer |
| RFI | Request for Information |
| COD | Commercial Operation Date |
