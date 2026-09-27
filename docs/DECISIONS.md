# Decisions Log

**Phase 0 decisions: LOCKED.** They change only by explicit founder decision.
**Phase 1 decisions (D-026 onward): OPEN** for founder review.

Status values: `RESOLVED`, `OPEN`, `PARTIALLY RESOLVED`.

## Index

| ID | Topic | Status |
|---|---|---|
| D-001 | Human review of events | RESOLVED |
| D-002 | Write-back to external systems | RESOLVED |
| D-003 | Initial project state / graph; schedule optional | RESOLVED |
| D-004 | Dependency status | RESOLVED |
| D-005 | Level 1 / 2 / 3 boundary | RESOLVED |
| D-006 | Confidence representation | RESOLVED |
| D-007 | Event taxonomy | RESOLVED (principle); list OPEN |
| D-008 | Reviewer identification / routing | OPEN |
| D-009 | Event vs Change; Changes view | RESOLVED |
| D-010 | MVP review actions | RESOLVED |
| D-011 | Conflicting sources | RESOLVED |
| D-012 | History | RESOLVED |
| D-013 | Initial user | RESOLVED |
| D-014 | Intake channels | PARTIALLY RESOLVED |
| D-015 | Data and confidentiality | RESOLVED |
| D-016 | Gates | RESOLVED |
| D-017 | Measurement | RESOLVED |
| D-018 | Single project | RESOLVED |
| D-019 | Ask GridPulse | RESOLVED |
| D-020 | Direct editing of validated intelligence | RESOLVED |
| D-021 | Source of truth / Validated Project Intelligence | RESOLVED |
| D-022 | Request more investigation | RESOLVED (by D-010) |
| D-023 | Dependency provenance | RESOLVED |
| D-024 | Authorized user | RESOLVED |
| D-025 | AI-inferred dependency in first demo | RESOLVED |
| D-026 | Baseline validation scope | OPEN |
| D-027 | Initial status of AI-extracted explicit dependencies | OPEN |
| D-028 | Entity resolution review | OPEN |
| D-029 | Impact disposition | OPEN |
| D-030 | Document content retention | OPEN |
| D-031 | Recording human Level 3 determinations | OPEN |
| D-032 | Canonical scenario dates | OPEN |
| D-033 | Gate readiness verdicts | OPEN |
| D-034 | Conditional one-hop implications | OPEN |
| D-035 | Impact propagation matrix | OPEN |
| D-036 | Source-authority configuration | OPEN |
| D-037 | Ask GridPulse over unvalidated intelligence | OPEN |
| D-038 | Who performs requested investigations | OPEN |
| D-039 | Activity as an entity kind | OPEN |
| D-040 | Rejecting schedule-derived dependencies | OPEN |

---

# Phase 0 — resolved (locked)

## D-001 — Human review
Every AI-detected Project Event begins in review (`DETECTED` → `UNDER_REVIEW`) during the MVP. An
authorized user manually entering a known real-world event may create it directly as `CONFIRMED`
(provenance `MANUAL_ENTRY`). AI-detected information is never silently promoted. Risk/confidence-based
routing is a possible future feature, not MVP. **RESOLVED**

## D-002 — Write-back
Read-only against all external systems (Primavera, Aconex, SharePoint, schedules, engineering systems)
in the MVP. Write-back only later and only with demonstrated customer need. **RESOLVED**

## D-003 — Initial project state / graph
Users must not manually construct the whole graph. Initial intelligence is reconstructed from available
information: documents, schedule, supplier communications, manual project facts, other imported
information. Manual relationship seeding only where necessary for benchmark ground truth. GridPulse
consumes explicit schedule relationships and is not a scheduling engine. **The schedule is preferred
but not mandatory**; GridPulse must be useful when it is incomplete or unavailable, and must not assume
the first user controls it (the EPC often does). Long-term: AI reconstructs and maintains the graph.
**RESOLVED**

## D-004 — Dependency status
`CONFIRMED` · `INFERRED` · `REJECTED`. Impact analysis may use inferred dependencies but must label
them; inferred relationships are never presented as fact. Human confirmation strengthens the graph.
**RESOLVED** (see D-023, D-027)

## D-005 — Level 1 / 2 / 3
GridPulse may perform deterministic calculations and evidence-backed comparisons (Level 1) and state
evidence-backed relationships/inferences (Level 2). Level 3 engineering/project conclusions are human
decisions; GridPulse may surface candidate Level 3 implications only as potential exposure requiring
validation. **Discovery vs determination** is a fundamental product boundary. **RESOLVED**

## D-006 — Confidence
No single "AI confidence score". Three axes: **evidence confidence** (`HIGH`/`MEDIUM`/`LOW`),
**relationship confidence** (`EXPLICIT`/`INFERRED`), **validation status**
(`REQUIRED`/`VALIDATED`/`REJECTED`/`NOT_REQUIRED`). Explicit states over pseudo-precise percentages;
no percentages without a future validated statistical basis. **RESOLVED**

## D-007 — Event taxonomy
Small and extensible; broad categories with attributes (old, new, reason, affected entity), e.g.
`DELIVERY_DATE_CHANGE` rather than shipment/supplier/transport/logistics/equipment delay types.
Descriptive labels are derived from the state change. `SHIPMENT_DELAY` is absorbed into
`DELIVERY_DATE_CHANGE`.
*Still open:* the final list — candidates for consolidation are `SCHEDULE_CHANGE` vs
`DELIVERY_DATE_CHANGE` and `TEST_FAILURE` vs `EQUIPMENT_FAILURE`. Working list in
`PHASE_1_ARCHITECTURE.md` §8.4. **RESOLVED (principle); list OPEN**

## D-008 — Reviewer identification / routing
*Context:* the demo must identify relevant reviewers, and the benchmark measures routing accuracy.
D-024 defines reviewers as configured roles/persons.
*Options:* A. manual assignment; B. configured role map (role ↔ entity kinds/disciplines) with
GridPulse suggesting routes; C. AI-inferred responsibility from documents.
*Recommendation:* B for the MVP, with suggestions shown as Level 2 with their basis; C later as
suggestion only. **OPEN**

## D-009 — Event vs Change; Changes view
**Change** = a detected difference between two states, versions, records or observations. **Event** =
something that happened or is reported to have happened in the real project. A Change may generate a
potential Event: `SOURCE → CHANGE DETECTED → POTENTIAL EVENT → HUMAN REVIEW → CONFIRMED PROJECT EVENT`.
The **Changes view shows all detected changes regardless of review**, with lifecycle
`DETECTED → UNDER_REVIEW → CONFIRMED | REJECTED`. A detected change never silently becomes confirmed.
**RESOLVED**

## D-010 — Review actions
MVP actions: `CONFIRM`, `REJECT`, `REQUEST_INVESTIGATION`, `EDIT_FINDING`. No elaborate workflow.
`REQUEST_INVESTIGATION` does not change Validated Project Intelligence; it creates
`INVESTIGATION_REQUESTED` and keeps the finding/change unresolved. **RESOLVED**

## D-011 — Conflicting sources
Never silently resolved. GridPulse represents **CONFLICT DETECTED** with both sources, versions/dates
where available and their evidence. AI may explain the conflict but must not choose the authoritative
source. Human review determines the validated interpretation. **RESOLVED**

## D-012 — History
GridPulse retains the complete history of its own detected changes, findings, reviews, confirmations,
rejections, dependency status changes, evidence associations, investigation requests and reviewer
actions. It is not an archival replacement for document- or project-management systems and does not
recreate Aconex-style document history or Primavera-style schedule history. **RESOLVED** (see D-030)

## D-013 — Initial user
Owner's Engineer / technical project-control professional on large BESS projects. **RESOLVED**

## D-014 — Intake channels
*Resolved:* inputs are documents, schedule (optional), supplier communications, manual project facts
and other imported information (D-003).
*Open:* how supplier communications arrive in the MVP. *Recommendation:* uploaded email/document
files; live mailbox connection is an integration and out of MVP scope. **PARTIALLY RESOLVED**

## D-015 — Data and confidentiality
Synthetic and public data only for prototype and benchmark. No production enterprise security before
proving the product. Before real customer data: encryption, authentication, authorization, tenant
isolation, audit logs, retention, deletion, residency, AI-provider data handling, contractual
confidentiality, enterprise security requirements (`PHASE_1_ARCHITECTURE.md` §17). No enterprise
compliance program in the MVP. **RESOLVED**

## D-016 — Gates
Small fixed MVP set: GRID CONNECTION · ENGINEERING READY · PROCUREMENT READY · CONSTRUCTION READY ·
COMMISSIONING READY · GRID COMPLIANCE READY · ENERGIZATION READY · COD / HANDOVER. Intelligence
checkpoints, not contractual approvals. Architecture allows future configurable gates without making
the MVP a gate-management system. **RESOLVED** (see D-033)

## D-017 — Measurement
Measurement exists in the architecture from the start. The benchmark measures at least: change
detection accuracy, direct-impact recall, secondary-impact recall, evidence precision, stale-evidence
detection, false-positive rate, reviewer routing accuracy, gate identification, investigation time,
human correction rate. The 4 h → 15 min + 30–60 min figure is only a product hypothesis/target, not an
industry fact or validated evidence. **RESOLVED**

## D-018 — Single project
MVP is one project. No portfolio functionality; architecture stays extensible. **RESOLVED**

## D-019 — Ask GridPulse
In the MVP, narrow. Not a general-purpose chatbot. Answers from Validated Project Intelligence with
evidence; each answer contains answer, supporting evidence, affected entities, dependency chain,
uncertainty and reviewer/validation status. If an answer cannot be supported by evidence, GridPulse
says so. **RESOLVED** (see D-037)

## D-020 — Direct editing
No arbitrary direct edits to Validated Project Intelligence. State changes originate through the
event/review mechanism: `SOURCE → DETECTION → FINDING → REVIEW → VALIDATED PROJECT INTELLIGENCE`.
Manual project facts may be entered explicitly with provenance showing manual entry. **RESOLVED**

## D-021 — Source of truth / Validated Project Intelligence
GridPulse is not the contractual or authoritative source of truth. The primary term is **Validated
Project Intelligence**: GridPulse's internally validated view of project information derived from
authoritative project sources and human review; not the contractual, legal, engineering, scheduling or
other authoritative source of truth. ("Trusted project state" is retired.) Systems of record stay
authoritative (Aconex for documents/contracts, Primavera for the schedule, engineering systems for
engineering data). GridPulse must never imply that its state replaces them. **RESOLVED**

## D-022 — Request more investigation
Resolved by D-010: `REQUEST_INVESTIGATION` → `INVESTIGATION_REQUESTED`; finding stays unresolved.
**RESOLVED**

## D-023 — Dependency provenance
Every dependency records provenance; at minimum `SCHEDULE_DERIVED`, `DOCUMENT_DERIVED`,
`HUMAN_CONFIRMED`, `AI_INFERRED`. "The schedule says it" and "an engineer validated it" are different
kinds of evidence and are never treated as equivalent. Architecture models provenance as a list
(origin plus human actions) separate from status. **RESOLVED**

## D-024 — Authorized user
No authentication yet. "Authorized user" = a configured project role/person allowed to perform the
relevant review action. Reviewer identity is explicit so authentication can be added later. **RESOLVED**

## D-025 — AI-inferred dependency in first demo
Yes. The first end-to-end demonstration must include at least one meaningful AI-inferred dependency,
proposed as `INFERRED` with evidence and validation required, never silently treated as confirmed.
**RESOLVED**

---

# Phase 1 — open architecture decisions

## D-026 — Baseline validation scope
**Question.** Reconstructing the initial project (D-003) produces many AI-extracted facts. D-001/D-020
forbid silently promoting AI output into Validated Project Intelligence, but reviewing every extracted
fact would cause review overload (Risk 2).
**Options.** A. Review every extracted fact. B. Extracted facts stay `PROPOSED` (usable, labelled
unvalidated); only facts that participate in impact paths, milestones or gates are raised as `FACT`
findings for baseline review. C. Treat facts from authoritative documents as validated without review.
**Recommendation.** B. C violates D-001's spirit; A is unusable at scale.
**Status.** OPEN

## D-027 — Initial status of AI-extracted explicit dependencies
**Question.** D-025 says relationships *not* explicitly stated are `INFERRED`. A relationship that *is*
explicitly stated in a document but extracted by AI could be mis-extracted. What status does it start with?
**Options.** A. `CONFIRMED` (it is explicit). B. `INFERRED` status, with relationship confidence
`EXPLICIT`, provenance `DOCUMENT_DERIVED`, validation `REQUIRED`, until reviewed. C. Add a fourth status.
**Recommendation.** B. Only deterministic structured imports (`SCHEDULE_DERIVED`), authorized manual
entries and human review produce `CONFIRMED`. The display shows "explicitly stated in <document> —
validation required", so the `INFERRED` status label is not mistaken for "reasoned". If the label
confusion is unacceptable, choose C.
**Status.** OPEN

## D-028 — Entity resolution review
**Question.** "Main transformer", "TX-01" and "Power Transformer T1" must be resolved to one entity.
Wrong merges corrupt impact paths. Must merges be reviewed?
**Options.** A. Every merge reviewed. B. Merges shown and reviewed as part of the finding that depends
on them; no separate queue. C. Automatic.
**Recommendation.** B for the MVP.
**Status.** OPEN

## D-029 — Impact disposition
**Question.** What can a reviewer do with an Impact?
**Options.** A. Impacts are informational only. B. Minimal lifecycle `OPEN → ACKNOWLEDGED | DISMISSED`
(reason required), `SUPERSEDED` on recompute. C. Treat impacts as Findings with the four review actions.
**Recommendation.** B. C risks "CONFIRM impact" being read as confirming a Level 3 consequence.
**Status.** OPEN

## D-030 — Document content retention
**Question.** Evidence must stay inspectable, but GridPulse is not a document archive. Does GridPulse
retain full content of the versions it ingested, or only references?
**Options.** A. Retain content of ingested versions (needed for verification and inspection if the
source changes). B. References only. C. Retain cited excerpts only.
**Recommendation.** A for the prototype (synthetic data); revisit with retention/deletion requirements
before real data.
**Status.** OPEN

## D-031 — Recording human Level 3 determinations
**Question.** When a human decides "energization is not affected", does GridPulse record it?
**Options.** A. No — decisions live outside GridPulse. B. Record as a human-authored Level 3 claim with
reviewer attribution (never AI-authored), linked to the impact.
**Recommendation.** B — improves "what's blocking energization?" answers and the audit trail, while
keeping authorship explicit.
**Status.** OPEN

## D-032 — Canonical scenario dates
**Question.** Phase 1 sets original delivery = 15 Jan and planned installation = 15 Jan. Then "delivery
moved 18 days" and "new delivery is 18 days after planned installation" give the same number, so the
benchmark cannot tell whether GridPulse compared against the right baseline. Same-day delivery and
installation is also unrealistic.
**Options.** A. Keep 15 Jan / 15 Jan. B. Original delivery 12 Jan (21-day shift; 18 days after
installation). C. Keep delivery 15 Jan; move planned installation (e.g. 19 Jan).
**Recommendation.** B or C — make the two calculations produce different numbers.
**Status.** OPEN

## D-033 — Gate readiness verdicts
**Question.** Gate names like "ENERGIZATION READY" suggest a ready/not-ready verdict, which would be a
Level 3 determination.
**Options.** A. No verdict; gates show linked items, open exposures, missing/stale evidence and
conflicts. B. A computed readiness status.
**Recommendation.** A.
**Status.** OPEN

## D-034 — Conditional one-hop implications
**Question.** May GridPulse state "If the finish-to-start link holds, installation cannot start before
2 Feb"? It is logically entailed by a dependency, but close to schedule calculation.
**Options.** A. Not allowed. B. Allowed as Level 2, one hop only, with the dependency's status shown.
**Recommendation.** B — high investigative value, clearly conditional.
**Status.** OPEN

## D-035 — Impact propagation matrix
**Question.** Which change kinds propagate over which relationship types
(`PHASE_1_ARCHITECTURE.md` §10.3)?
**Recommendation.** Adopt the initial matrix; tune it only with benchmark evidence.
**Status.** OPEN

## D-036 — Source-authority configuration
**Question.** Should the project record which source is authoritative for which information (e.g.
EPC schedule for planned dates)?
**Options.** A. No. B. Yes, for display and conflict explanation only — never automatic resolution.
**Recommendation.** B.
**Status.** OPEN

## D-037 — Ask GridPulse over unvalidated intelligence
**Question.** D-019 says answers come from Validated Project Intelligence, but many useful answers
("what is blocking energization?") need inferred dependencies or open findings, and the required answer
fields include validation status.
**Options.** A. Validated intelligence only. B. Validated first, plus clearly labelled unvalidated
items (inferred links, open findings, conflicts).
**Recommendation.** B.
**Status.** OPEN

## D-038 — Who performs requested investigations
**Question.** After `REQUEST_INVESTIGATION`, who investigates?
**Options.** A. GridPulse runs a targeted AI investigation and attaches results. B. Assigned to a
person. C. Either, recorded on the Investigation.
**Recommendation.** A for the MVP (keeps it out of workflow management); the reviewer's question drives it.
**Status.** OPEN

## D-039 — Activity as an entity kind
**Question.** The required concept list has Milestone but not Activity/Task, yet the scenario's nodes
(transformer installation, HV commissioning) are dated activities, not zero-duration milestones.
**Options.** A. Model them as milestones (start/finish). B. Add `Activity` as an Entity kind carrying
only the dated claims needed for intelligence — explicitly not a task.
**Recommendation.** B, with the non-task boundary stated.
**Status.** OPEN

## D-040 — Rejecting schedule-derived dependencies
**Question.** If an engineer rejects a `SCHEDULE_DERIVED` link as wrong, GridPulse's graph and the
schedule diverge.
**Options.** A. Not allowed. B. Allowed; divergence shown; schedule untouched (D-002).
**Recommendation.** B — consistent with D-021 (divergence is information).
**Status.** OPEN
