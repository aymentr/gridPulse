# Decisions Log

**Phase 0 decisions: LOCKED.** They change only by explicit founder decision.
**Phase 1 decisions (D-026 – D-040):** the five blocking decisions (D-026, D-027, D-032, D-033, D-037)
are **RESOLVED**; the rest remain OPEN.
**Status:** ARCHITECTURE REVIEWED · BENCHMARK CONSTRUCTED · TECHNICAL REALISM: NOT INDEPENDENTLY VALIDATED ·
PRODUCT VALIDATION: PENDING · PHASE 2: BLOCKED UNTIL VALIDATION GATE IS PASSED.
**Council-review amendments (D-041 – D-047):** adopted on founder instruction after `COUNCIL_REVIEW.md`;
they amend the locked Phase 0 documents where noted.

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
| D-026 | Baseline validation scope | RESOLVED |
| D-027 | Initial status of AI-extracted explicit dependencies | RESOLVED |
| D-028 | Entity resolution review | OPEN |
| D-029 | Impact disposition | OPEN |
| D-030 | Document content retention | OPEN |
| D-031 | Recording human Level 3 determinations | OPEN |
| D-032 | Canonical scenario dates | RESOLVED |
| D-033 | Gate readiness verdicts | RESOLVED |
| D-034 | Conditional one-hop implications | OPEN |
| D-035 | Impact propagation matrix | OPEN |
| D-036 | Source-authority configuration | OPEN |
| D-037 | Ask GridPulse over unvalidated intelligence | RESOLVED |
| D-038 | Who performs requested investigations | OPEN |
| D-039 | Activity as an entity kind | OPEN |
| D-040 | Rejecting schedule-derived dependencies | OPEN |
| D-041 | Intake framed around what the OE actually receives | RESOLVED (subject to validation) |
| D-042 | PCS specification-change scenario co-primary | RESOLVED |
| D-043 | Transformer demo reframed as divergence detection | RESOLVED |
| D-044 | Validation gate before Phase 2 (three dimensions) | RESOLVED |
| D-045 | Buyer and pricing hypotheses | OPEN (to be tested) |
| D-046 | Documentation freeze | RESOLVED |
| D-047 | Drawings, SLDs and protection-setting files | OPEN |
| D-048 | Timed-comparison design (order bias) | RESOLVED — crossover |
| D-049 | Validation status of schedule-derived data | RESOLVED — EXPLICIT + UNVALIDATED |
| D-050 | Economic hypothesis: investigation compression, not change detection | RECORDED — UNVALIDATED |
| D-051 | External technical-realism review is non-blocking | RESOLVED |
| D-052 | Phase 1.5 technical spike in parallel with validation | RESOLVED |

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
*Amended by D-027:* validation status values are `UNVALIDATED` / `CONFIRMED` / `REJECTED`; only explicit
human action produces `CONFIRMED`.

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
the MVP a gate-management system. **RESOLVED** — *names amended by D-033* to neutral checkpoints.

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
says so. **RESOLVED** — *source scope and answer structure amended by D-037.*

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

## D-026 — Baseline review scope
**Decision.** Consequential / selective review. Human review of every extracted fact is **not**
required. The baseline may contain observed claims, AI-extracted claims, inferred relationships and
document-derived relationships, explicitly marked `UNVALIDATED` where appropriate. The Review Queue
prioritises:
1. consequential changes
2. source conflicts
3. inferred dependencies involved in an investigation
4. stale evidence
5. missing evidence relevant to a critical investigation

Objective: GridPulse must not create more review work than it saves.
**Status.** RESOLVED

## D-027 — Explicit AI-extracted dependencies
**Decision.** An explicitly stated relationship extracted by AI is: relationship confidence `EXPLICIT`,
validation status `UNVALIDATED`, provenance `DOCUMENT_DERIVED` / `AI_EXTRACTED`. It never becomes
human-confirmed automatically; only explicit human review changes validation status to `CONFIRMED`.
Relationship confidence is kept separate from validation status.
**Consequences.** Validation status values are `UNVALIDATED` / `CONFIRMED` / `REJECTED` (replacing
`REQUIRED` / `VALIDATED` / `NOT_REQUIRED`). The D-004 labels map to the two axes: "INFERRED" is a
relationship-confidence value; "CONFIRMED"/"REJECTED" are validation values. Validated Project
Intelligence contains only `CONFIRMED` items. See D-049 for schedule-derived data.
**Status.** RESOLVED

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

## D-032 — Canonical transformer dates
**Decision.** Original delivery **12 January**; planned installation **15 January**; new supplier
delivery (via progress report) **2 February**. Permitted calculations: 12 Jan → 15 Jan = 3 calendar
days; 2 Feb is 18 calendar days after the planned 15 January installation date (and 21 days after the
scheduled delivery). No conclusion that energization will be delayed. The demonstration centres on
source divergence (progress report 2 Feb vs schedule 12 Jan / installation 15 Jan): change,
conflict/divergence, affected milestone, evidence, uncertainty — never party intent.
**Status.** RESOLVED

## D-033 — Checkpoint terminology
**Decision.** Neutral checkpoints: GRID CONNECTION CHECKPOINT · ENGINEERING CHECKPOINT · PROCUREMENT
CHECKPOINT · CONSTRUCTION CHECKPOINT · COMMISSIONING CHECKPOINT · GRID COMPLIANCE CHECKPOINT ·
ENERGIZATION CHECKPOINT · COD / HANDOVER CHECKPOINT. GridPulse never declares READY or NOT READY; it
identifies evidence and unresolved issues relevant to a checkpoint. Human experts determine readiness.
**Status.** RESOLVED

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

## D-037 — Ask GridPulse
**Decision.** Ask GridPulse may use validated project intelligence, observed/unvalidated information,
inferred relationships and deterministic calculations — but every answer distinguishes them. Minimum
structure: VALIDATED INFORMATION · OBSERVED INFORMATION · INFERRED RELATIONSHIPS · DETERMINISTIC
CALCULATIONS · POTENTIAL EXPOSURES · HUMAN VALIDATION REQUIRED · EVIDENCE. It must not hide
uncertainty. If evidence is insufficient: *"GridPulse does not have sufficient evidence to determine
this."*
**Status.** RESOLVED

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

---

# Council-review amendments

Source: `COUNCIL_REVIEW.md`. Adopted on founder instruction ("do the changes").

## D-041 — Intake framed around what the OE actually receives
**Context.** Suppliers usually communicate with the EPC, not the Owner's Engineer. The OE typically
learns of changes through reporting-period documents.
**Decision.** Scenarios, benchmark corpus and intake assumptions are organised by **reporting period**:
EPC monthly progress reports, schedule updates, submittals and document revisions, meeting minutes and
correspondence copied to the owner. Direct supplier communications remain a supported variant, not the
default assumption. The first user and single-project scope (D-013, D-018) are unchanged.
**Amends.** Phase 0 demonstration framing in `PRODUCT_WORKFLOW.md` and `MVP_BOUNDARIES.md`.
**Status.** RESOLVED — subject to confirmation by the validation gate (assumption A2).

## D-042 — PCS specification-change scenario co-primary
**Decision.** The first demonstration consists of **two co-primary vertical slices**:
(A) transformer delivery divergence and (B) PCS specification Rev 7 → Rev 8 propagating to the PPC
specification (stale reference) and grid-compliance requirements/tests. Each includes at least one
AI-inferred, unseeded dependency (D-025).
**Reasoning.** Scenario B shows propagation through links no schedule contains — where GridPulse's
value is most distinct.
**Status.** RESOLVED

## D-043 — Transformer demo reframed as divergence detection
**Decision.** The transformer scenario's primary value is **detecting that sources disagree** (EPC
progress report states 2 Feb; schedule update still shows 15 Jan) and tracing potential exposure — not
propagating dates, where schedulers and P6 are already strong. GridPulse never characterises a party's
intent (e.g. "the EPC is concealing the delay").
**Status.** RESOLVED

## D-044 — Validation gate before Phase 2
**Decision.** Phase 2 does not start until `VALIDATION_PLAN.md` passes on three dimensions:
**A. Efficiency** — total unassisted vs total assisted human investigation time (assisted time includes
review, correction, further investigation, evidence verification, routing); target ≥ 50 % reduction,
a target rather than a universal pass/fail law. **B. Investigation quality** — change detection,
direct/secondary-impact recall, evidence precision, stale-evidence, source-divergence, entity
resolution, inferred-dependency precision, routing, review load; a time saving does not count if
important evidence-supported impacts are missed. **C. Safety** — unsupported Level 3 conclusions must
be 0. Completeness is not 100 % recall; precision and recall are always reported separately, with
precision prioritised for inferred dependencies. Three routes: practitioner interviews, expert timed
comparison, external realism validation. No fabricated validation evidence.
**Status.** RESOLVED

## D-045 — Buyer and pricing hypotheses
**Question.** Who pays, and per what unit?
**Hypotheses (not decisions).** H1 OE/technical-advisory firm; H2 owner/developer; H3 lender's
technical advisor/lender; H4 services-led start through a partner OE firm. See `VALIDATION_PLAN.md` §5.
**Recommendation.** Test H1 and H4 first — they match the first user (D-013) and avoid a long software
procurement cycle.
**Status.** OPEN

## D-046 — Documentation freeze
**Decision.** No new documentation layers. Before Phase 2, only: (1) the five blocking decisions
(D-026, D-027, D-032, D-033, D-037), and (2) founder-approved amendments arising from the validation
gate, folded into existing documents.
**Status.** RESOLVED

## D-047 — Drawings, SLDs and protection-setting files
**Question.** Much engineering truth lives in drawings, single-line diagrams and protection-setting
files, which text-based extraction will miss.
**Options.** A. Out of MVP scope, recorded as a known limitation; evidence can still cite a drawing's
register entry / revision. B. Basic support (title block, revision, drawing register) in MVP.
C. Full drawing understanding in MVP.
**Recommendation.** A for the MVP; revisit using the interview findings on how often drawing changes
drive investigations.
**Status.** OPEN

---

# Validation-preparation decisions

## D-048 — Timed-comparison design (order bias)
**Question.** In the specified Route B protocol the expert investigates the raw documents first and
then reviews the bundle. Having already investigated, their review time understates what a fresh
reviewer would need, biasing `T_assisted` downward.
**Options.** A. As specified (single expert, raw then bundle). B. Crossover: each expert does one
scenario unassisted and the other assisted-first, order counterbalanced. C. Separate expert groups per
arm.
**Decision.** B — crossover. Each expert investigates one scenario unassisted and the other scenario
assisted, with scenario assignment and task order counterbalanced across experts. The crossover is the
basis for the efficiency measure. The sequential steps (bundle shown after an unassisted investigation)
may still be used after `T_raw` is recorded, only to observe correction behaviour and trust — never for
the efficiency measure.
**Status.** RESOLVED

## D-049 — Validation status of schedule-derived data
**Question.** D-004's example treated a relationship explicitly stated in the schedule as `CONFIRMED`.
D-027 states that only explicit human review changes validation status to `CONFIRMED`, and D-023 says
"the schedule says it" is not "an engineer validated it".
**Options.** A. Schedule-derived items are `EXPLICIT · UNVALIDATED · SCHEDULE_DERIVED`. B. Schedule-
derived items are `CONFIRMED` without review.
**Decision.** A — schedule-derived items are `EXPLICIT · UNVALIDATED · SCHEDULE_DERIVED`, consistent
with D-023 and D-027. They are usable in impact analysis and displayed as explicitly stated; only
explicit human review makes them `CONFIRMED`. D-004's schedule example is amended accordingly.
**Status.** RESOLVED

## D-050 — Economic hypothesis
**Statement.** The economic hypothesis is **not** that change detection is valuable enough to buy.
Change detection is the trigger; the potential economic value is **compressing the cross-disciplinary
investigation required after a meaningful change**.
**Status.** RECORDED — **UNVALIDATED**; tested directly by the validation gate.

## D-051 — External technical-realism review is non-blocking
**Decision.** Independent BESS/grid practitioner realism review is recommended but is not a
prerequisite for executing the controlled Route B benchmark. If unavailable, the project must
explicitly record the absence of independent realism validation and must not interpret benchmark
results as evidence of real-world workflow representativeness.
**Rationale.** Blocking the controlled product experiment indefinitely on external reviewer
availability would prevent testing the core investigation hypothesis. The missing review is retained
as an explicit limitation and future validation item.
**Consequences.** Route B may proceed. Benchmark conclusions remain limited to the constructed
scenarios. Real-world workflow and technical realism remain unvalidated. The product-validation gate
(D-044: efficiency, quality, zero unsupported Level 3 conclusions) is unchanged and still governs
Phase 2. No independent review has been performed; none is claimed. The review package in
`validation/technical-realism-review/` is kept as an optional follow-up.
**Status.** RESOLVED

## D-052 — Phase 1.5 technical spike in parallel with validation
**Decision.** On founder instruction, a Phase 1.5 technical vertical slice ("spike") is built in
parallel with Route B. It implements the Phase 1 model for the two synthetic scenarios only, to test
whether fragmented documents can be turned into an evidence-backed investigation without unsupported
determinations. Spike stack: Python 3.11 standard library, in-memory store, `unittest` — chosen as the
smallest reversible option. It is **not** the Phase 2 technology decision, which remains open.
**Constraints.** No change to Phase 0, the Phase 1 architecture, the benchmark, ground truth, bundles,
scoring or the validation gate. Production code never reads ground truth. Phase 2 remains
**BLOCKED — VALIDATION GATE NOT PASSED**.
**Status.** RESOLVED
