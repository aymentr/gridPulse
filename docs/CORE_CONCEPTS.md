# Core Concepts

**Phase 0 — LOCKED.** This is the product vocabulary in summary form. The precise domain model —
purpose, boundaries, lifecycle, relationships and provenance for each concept — is in
`PHASE_1_ARCHITECTURE.md` §4, which takes precedence on detail.

---

## Validated Project Intelligence

GridPulse's internally validated view of project information derived from authoritative project
sources and human review. **It is not the contractual, legal, engineering, scheduling or other
authoritative source of truth for the project.** (Replaces the earlier term "trusted project state".)

```
AUTHORITATIVE PROJECT SOURCES → GRIDPULSE → AI investigation / extraction / inference
  → HUMAN REVIEW → VALIDATED PROJECT INTELLIGENCE
```

It changes only through review of findings or authorized manual entry with visible provenance. No
arbitrary direct edits.

## System of Record / Source

External systems (Aconex, Primavera/P6, MS Project, SharePoint, Procore, Excel, engineering and
commissioning systems, email) that remain authoritative. A **Source** is the origin system or channel
of information GridPulse reads.

## Document and DocumentVersion

Any ingested information record (file, email, schedule export, dataset, manual-entry record) and the
exact version GridPulse read. GridPulse keeps the versions it used — it does not recreate the external
system's document history.

## Evidence

The link from a claim to a precise, verified location in a document version:

```
CLAIM → EVIDENCE → DOCUMENT_VERSION → PAGE / SECTION / CHUNK (or message, activity/field, row, manual entry)
```

## Claim and the three levels

| Level | Name | Example | Who |
|---|---|---|---|
| 1 | **Fact** — directly supported or deterministically calculated | "Delivery date changed from Jan 12 to Feb 2." / "2 Feb is 18 calendar days after the planned 15 Jan installation." | GridPulse, with evidence |
| 2 | **Dependency / inference** — reasoned relationship supported by evidence | "The transformer delivery change may affect the transformer installation milestone." | GridPulse, labelled |
| 3 | **Engineering / project conclusion** | "Energization will be delayed." "Protection settings must be redesigned." | **Humans only** |

GridPulse may surface candidate Level 3 implications only as *potential exposure — validation required*.

## Observed information

Level 1 claims taken from sources that no human has validated (`UNVALIDATED`). Usable in
investigations and answers, always labelled; distinct from Validated Project Intelligence (D-026,
D-037).

## Discovery vs determination

AI **discovers** and **calculates**; humans **determine**. See `PRODUCT_VISION.md` §7.

## Change

**A detected difference between two states, versions, records or observations.** The Changes view
shows all detected changes, reviewed or not, with lifecycle:

```
DETECTED → UNDER_REVIEW → CONFIRMED | REJECTED
```

A detected change never silently becomes confirmed.

## Event

**Something that happened, or is reported to have happened, in the real project.** A Change may
generate a potential Event. Same lifecycle as Change; an authorized manual entry may be `CONFIRMED`
directly.

Event taxonomy is small and extensible: broad categories with attributes (old, new, reason, affected
entity) — e.g. `DELIVERY_DATE_CHANGE` rather than separate shipment/supplier/transport delay types.

## Finding

The **unit of human review**: a package of claims and evidence proposing a change/event, a dependency,
a conflict, stale or missing evidence, or a fact. Findings move `DETECTED → UNDER_REVIEW →
CONFIRMED | REJECTED`, with `INVESTIGATION_REQUESTED` as an unresolved side-state.

## Review and review actions

`CONFIRM` · `REJECT` · `REQUEST_INVESTIGATION` · `EDIT_FINDING`. Every review is attributed to a named
reviewer and is immutable.

## Reviewer / authorized user

A configured project role/person allowed to perform the relevant review action (D-024). No
authentication in the prototype; reviewer identity is always explicit.

## Conflict

Contradictory information from different sources. Represented as **CONFLICT DETECTED** with all
sources and evidence; never silently resolved.

## Confidence and validation

No single "AI confidence score". Three separate axes:

| Axis | Values |
|---|---|
| Evidence confidence — support for the factual observation | `HIGH` / `MEDIUM` / `LOW` |
| Relationship confidence — support for a relationship | `EXPLICIT` / `INFERRED` |
| Validation status | `UNVALIDATED` / `CONFIRMED` / `REJECTED` |

Only explicit human review (or an authorized manual entry) produces `CONFIRMED`. Everything else —
observed claims, AI-extracted and AI-inferred relationships, imported data — stays `UNVALIDATED` and
labelled (D-027). Relationship confidence and validation status are independent.

Example: `Evidence: HIGH · Relationship: INFERRED · Validation: UNVALIDATED`. No percentages without a
validated statistical basis.

## Source divergence

A difference between Validated Project Intelligence and a system of record (e.g. a validated delivery
date that the EPC schedule update does not yet reflect), or between sources for the same reporting
period. Divergence is **information, not an error**: GridPulse shows it with evidence, never corrects
the system of record, and never characterises a party's intent. Unresolved disagreements between
current sources are raised as CONFLICT findings.

## Reporting period

The cadence at which the first user typically receives project information (EPC progress report,
schedule update, submittals, minutes). "What changed since the last reporting period?" is the first
user's central question (D-041).

## Entity

Any project "thing": equipment, parties (incl. suppliers), contracts, requirements, milestones,
activities, tests, gates, document artifacts.

## Dependency

A typed relationship along which change may propagate, described by **relationship confidence**
(`EXPLICIT` / `INFERRED`) and **validation status** (`UNVALIDATED` / `CONFIRMED` / `REJECTED`). An
explicitly stated relationship extracted by AI is `EXPLICIT · UNVALIDATED · DOCUMENT_DERIVED/AI_EXTRACTED`
(D-027). **Provenance (at minimum):** `SCHEDULE_DERIVED` / `DOCUMENT_DERIVED` / `HUMAN_CONFIRMED` /
`AI_INFERRED`. Inferred relationships are never presented as established fact.

## Project Intelligence Graph

The central intelligence model: entities, requirements, evidence, dependencies, milestones, gates,
events, changes and impacts, each with provenance, confidence, validation status, timestamps and source
references. **Not a scheduling engine; not a replacement for Primavera/P6.**

## Impact

A potential effect of a confirmed change on an entity, milestone or gate, reached through a dependency
path, with evidence, calculations, uncertainty, reviewer and unresolved question. Never a determination.

## Investigation

A bounded, timed unit of investigative work: impact analysis after a confirmed change, a requested
investigation (`REQUESTED → IN_PROGRESS → COMPLETED`), or an Ask GridPulse question.

## Gate (MVP fixed set)

GRID CONNECTION CHECKPOINT · ENGINEERING CHECKPOINT · PROCUREMENT CHECKPOINT · CONSTRUCTION CHECKPOINT ·
COMMISSIONING CHECKPOINT · GRID COMPLIANCE CHECKPOINT · ENERGIZATION CHECKPOINT · COD / HANDOVER
CHECKPOINT (D-033). GridPulse identifies evidence and unresolved issues; it never declares READY or
NOT READY — experts determine readiness. **Intelligence checkpoints, not
contractual approvals.**

## Requirement · Test · TestResult · Milestone

Requirements (with supporting or missing evidence), tests that verify them, reported test results, and
dated milestones — all represented as evidence-backed claims, never as GridPulse's own determinations.

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
