# Decisions Log

Product and architecture decisions for GridPulse. Resolved decisions are **locked** for Phase 0 and
change only by explicit founder decision. Open decisions carry a recommendation for founder review.

Status values: `RESOLVED`, `OPEN`, `PARTIALLY RESOLVED`, `SUPERSEDED`.

| ID | Question | Status |
|---|---|---|
| D-001 | Which events require human review? | **RESOLVED** |
| D-002 | Does GridPulse write back to external systems? | **RESOLVED** |
| D-003 | How is the initial project state and graph established? | **RESOLVED** |
| D-004 | How are AI-inferred dependencies handled? | **RESOLVED** |
| D-005 | Where is the Level 2 / Level 3 line? | **RESOLVED** |
| D-006 | How is confidence represented? | OPEN |
| D-007 | How granular is the event taxonomy? | **RESOLVED** (principle); exact list open |
| D-008 | How are relevant reviewers identified? | OPEN |
| D-009 | What is the difference between an Event and a Change? | **RESOLVED** |
| D-010 | Which review actions are in the MVP? | PARTIALLY RESOLVED |
| D-011 | How are conflicting sources handled? | OPEN |
| D-012 | How much history does the trusted state keep? | OPEN |
| D-013 | Who is the initial MVP user? | **RESOLVED** |
| D-014 | Which intake channels does the MVP support? | PARTIALLY RESOLVED |
| D-015 | Data and confidentiality approach | **RESOLVED** |
| D-016 | How are gates defined and how is gate status determined? | OPEN |
| D-017 | How is investigation compression measured, and on what data? | OPEN |
| D-018 | Single project or portfolio? | OPEN |
| D-019 | Is "Ask GridPulse" in the MVP? | OPEN |
| D-020 | Can the trusted state be edited outside the event path? | PARTIALLY RESOLVED |
| D-021 | GridPulse's source of truth | **RESOLVED** |
| D-022 | How is "request more investigation" represented? | OPEN |
| D-023 | Does `CONFIRMED` dependency conflate source-explicit and human-confirmed? | OPEN |
| D-024 | What is an "authorized user" in the MVP? | OPEN |
| D-025 | Must the first demo exercise AI-inferred dependencies? | OPEN |

---

# Resolved decisions

## D-001 — Human review

**Decision.** In the MVP, **every AI-detected Project Event begins in `NEEDS_REVIEW`.** An authorized
user manually entering a known real-world event may create it directly as `CONFIRMED`.

| Origin | Example | Status |
|---|---|---|
| Manual | "Transformer delivery has been confirmed by the project manager as moving from Jan 12 to Feb 2." | `CONFIRMED` |
| AI | "Supplier email appears to change transformer delivery from Jan 12 to Feb 2." | `NEEDS_REVIEW` |

AI-detected information is never silently promoted into the trusted project state. Risk/confidence-based
review routing may come in future versions but is **not** part of the MVP.

**Status.** RESOLVED

---

## D-002 — Write-back

**Decision.** GridPulse is **read-only against external systems during the MVP.** It does not modify
Primavera, Aconex, SharePoint, external schedules or engineering systems. It maintains its own validated
intelligence state. Write-back may be considered later only if a customer need is demonstrated.

**Status.** RESOLVED

---

## D-003 — Initial project state / graph

**Decision.** GridPulse must **not** require users to manually construct the whole dependency graph.
Initial project intelligence is reconstructed from available project information. The MVP may use:

- project documents
- an imported project schedule
- manually entered project facts
- manually seeded relationships where necessary for the controlled benchmark (to establish ground truth)

The architecture must allow GridPulse to discover and infer relationships. The MVP is **not** a
scheduling engine: explicit relationships in a source schedule are consumed.

**Long-term goal:** AI reconstructs and maintains the project intelligence graph from the project's
existing information.

**Status.** RESOLVED

---

## D-004 — AI-inferred dependencies

**Decision.** Dependencies have a status:

| Status | Example |
|---|---|
| `CONFIRMED` | Schedule explicitly says Transformer Installation depends on Transformer Delivery |
| `INFERRED` | AI infers from several documents that Transformer Installation affects HV Commissioning |
| `REJECTED` | A human rejects that relationship |

The impact engine may use inferred dependencies but must clearly label them. An inferred relationship is
never presented as established fact. Human confirmation strengthens the trusted graph.

**Status.** RESOLVED (see D-023 for a residual question)

---

## D-005 — Level 2 vs Level 3

**Decision.** GridPulse **may** perform deterministic calculations and evidence-backed comparisons,
e.g. *"The new delivery date is 21 calendar days later than the previous planned date."* It may identify
evidence-backed project relationships, e.g. that transformer installation is scheduled relative to
delivery. It must **not** conclude *"Energization will be delayed by 21 days."*

- **Level 1 — Fact:** directly supported information (incl. deterministic calculations on evidenced values).
- **Level 2 — Dependency / Inference:** evidence-backed relationship or analytical inference.
- **Level 3 — Engineering / Project Conclusion:** consequential technical or project decision — **human only.**

**Status.** RESOLVED

---

## D-007 — Event taxonomy

**Decision.** Keep the taxonomy **small and extensible**; prefer broad categories with attributes.
Use `DELIVERY_DATE_CHANGE` (old date, new date, reason, affected entity) rather than separate
`SHIPMENT_DELAY`, `SUPPLIER_DELAY`, `TRANSPORT_DELAY`, `LOGISTICS_DELAY`, `EQUIPMENT_DELAY` types.
Descriptive labels such as "delivery delay" may be derived from the state change.

**Consequence.** The original `SHIPMENT_DELAY` type is absorbed into `DELIVERY_DATE_CHANGE`.

**Still open.** The exact category list. Candidates for further consolidation during design:
`SCHEDULE_CHANGE` vs `DELIVERY_DATE_CHANGE` (a delivery date is a schedule date), and `TEST_FAILURE` vs
`EQUIPMENT_FAILURE`. Recommendation: settle the list when the data model is designed, using the same
"broad category + attributes" rule.

**Status.** RESOLVED (principle); list OPEN

---

## D-009 — Event vs Change

**Decision.** Related but conceptually different.

- **Change:** a difference between two states or versions (PCS specification Rev 7 → Rev 8;
  transformer delivery Jan 12 → Feb 2).
- **Event:** something that happened or is reported to have happened in the real project
  ("Supplier informed the project that transformer delivery has moved to February 2").

A Change may generate a Potential Event:

```
SOURCE → CHANGE DETECTED → POTENTIAL EVENT → HUMAN REVIEW → CONFIRMED PROJECT EVENT
```

The technical data model is designed later.

**Consequence.** The original UI description "Changes — confirmed changes to project state" is replaced
by "Changes — detected differences between states or versions". Not every Event originates from a
detected Change (e.g. a manually entered confirmed event, or an RFI being issued).

**Status.** RESOLVED

---

## D-013 — Initial user

**Decision.** Initial MVP user: **Owner's Engineer / technical project-control professional working on
large BESS projects.** The MVP optimizes for this workflow and is not designed simultaneously for
developers, EPCs, grid operators, other consultants, data-center operators, commissioning companies or
investors.

First question: *Can GridPulse materially reduce the investigation workload of a technical professional
when project information changes?*

**Status.** RESOLVED

---

## D-015 — Data and confidentiality

**Decision.** Prototype and benchmark use **synthetic and public data only**. Production enterprise
security is not required before proving the product, but the architecture must acknowledge that real
projects are highly confidential. Before real customer data is used, the product must address:
encryption, authentication, authorization, tenant isolation, audit logs, data retention, data deletion,
data residency, AI-provider data handling, contractual confidentiality and appropriate enterprise
security requirements. No enterprise compliance program during the MVP.

**Status.** RESOLVED

---

## D-021 — GridPulse's source of truth

**Decision.** GridPulse is **not the contractual or authoritative source of truth** for the project. It
maintains a **validated intelligence state** derived from authoritative project sources and human review.

- Aconex may remain the project document / contractual record.
- Primavera may remain the project scheduling system.
- Engineering systems may remain authoritative for engineering data.

GridPulse maintains an evidence-backed intelligence representation of what the information across these
systems collectively implies about the current project state.

**Reasoning.** Strategically, this keeps GridPulse in the intelligence category rather than competing
with systems of record. Legally, it limits the risk of GridPulse outputs being treated as the
authoritative project record.

**Consequence.** "Trusted project state" in these documents means this validated intelligence state —
trusted *within GridPulse*, not authoritative for the project.

**Status.** RESOLVED

---

# Open and partially resolved decisions

## D-006 — How is confidence represented?

**Options.** A. Numeric (0–1). B. Categorical (high/medium/low) with reasons. C. Derived from source
type and evidence quality, with reasons.

**Recommendation.** B or C shown to users; raw numbers kept internally for evaluation.

**Reasoning.** Model-produced numeric confidences are poorly calibrated and invite false trust; reasons
help reviewers more.

**Status.** OPEN

---

## D-008 — How are relevant reviewers identified?

**Context.** The first demo now requires GridPulse to "identify relevant reviewers" (step 10). That needs
some knowledge of people, roles and responsibilities.

**Options.** A. Manual assignment per event. B. A simple project role/responsibility map (entered or
seeded) used to suggest reviewers by entity/discipline. C. AI-inferred from documents (RACI, contracts,
org charts).

**Recommendation.** B for the MVP — a seeded role map in the synthetic benchmark project, with
suggestions shown as Level 2 (with the basis for the suggestion). C later, as suggestion only.

**Status.** OPEN

---

## D-010 — Which review actions are in the MVP?

**Resolved part.** The reviewer should *eventually* be able to confirm, reject, edit/correct and request
more investigation. Corrections become part of the trusted state.

**Open part.** Which of these are required in the MVP.

**Recommendation.** Confirm, reject and edit/correct in the MVP (store both the AI proposal and the
human correction — this is the raw data for measuring precision). "Request more investigation" can follow.

**Status.** PARTIALLY RESOLVED

---

## D-011 — How are conflicting sources handled?

**Example.** Supplier email says Feb 2; latest schedule still says Jan 12; minutes say "late January".

**Options.** A. Latest source wins. B. Surface a contradiction as a reviewable item with all evidence.
C. Source-authority ranking as a hint.

**Recommendation.** B, optionally informed by C. Note that under D-021 a difference between GridPulse's
validated state and a system of record is expected and should be surfaced, not overwritten.

**Status.** OPEN

---

## D-012 — How much history does the trusted state keep?

**Options.** A. Current state plus event log. B. Full history, reconstructable as of any time on both
the detected-time and effective-time axes.

**Recommendation.** B conceptually, via an append-only record of changes, events and reviews.

**Reasoning.** "What changed since last week?", auditability and evaluation all require it.

**Status.** OPEN

---

## D-014 — Which intake channels does the MVP support?

**Resolved part.** D-003 establishes project documents, an imported schedule and manual entry as MVP
inputs.

**Open part.** How the supplier communication arrives in the demo — as an uploaded document/email file,
or via a live mailbox connection.

**Recommendation.** Uploaded email/document file. Live mailbox ingestion is an integration and is out
of MVP scope.

**Status.** PARTIALLY RESOLVED

---

## D-016 — Gates

**Options.** A. Gates as graph nodes reachable by impact analysis, no status logic. B. Gates with
evidence checklists showing missing evidence. C. Computed "ready / not ready".

**Recommendation.** A for MVP; B later. Avoid C — a computed readiness status risks becoming a Level 3
conclusion.

**Status.** OPEN

---

## D-017 — Measuring investigation compression

**Context.** D-015 restricts the prototype and benchmark to synthetic and public data.

**Options.** A. Synthetic BESS project with hand-built ground truth and scripted events. B. Anonymised
real project data with experts timing manual investigations. C. A, then B once enterprise controls exist.

**Recommendation.** C. Define acceptable precision/recall thresholds with target users before claiming
the 4 h → 15 min + 30–60 min targets. Recognise that synthetic data can show *feasibility* but cannot by
itself validate real-world time savings.

**Status.** OPEN

---

## D-018 — Single project or portfolio?

**Recommendation.** Single project in the MVP; model entities (e.g. suppliers) so cross-project views
are possible later.

**Status.** OPEN

---

## D-019 — Is "Ask GridPulse" in the MVP?

**Options.** A. Exclude. B. Narrow version over the validated state and graph, evidence-backed.
C. General document Q&A.

**Recommendation.** A for the first demo, B soon after. Avoid C (drifts toward "chat with your PDFs").

**Status.** OPEN

---

## D-020 — Can the trusted state be edited outside the event path?

**Resolved part.** D-001 provides a path for authorized manual entry of `CONFIRMED` events.

**Open part.** Whether any direct edit that bypasses events is allowed (e.g. fixing an extracted value).

**Recommendation.** No direct edits; all changes go through events or review corrections, so history
and evidence remain complete.

**Status.** PARTIALLY RESOLVED

---

## D-022 — How is "request more investigation" represented?

**Question.** The reviewer can eventually request more investigation. The event statuses are
`NEEDS_REVIEW`, `CONFIRMED`, `REJECTED`. Does "more investigation" keep the item in `NEEDS_REVIEW` with
a note, or need its own status?

**Options.** A. Stays `NEEDS_REVIEW` with a recorded request. B. A distinct status (e.g. under
investigation).

**Recommendation.** A — keeps the status set minimal; the request is recorded on the item.

**Status.** OPEN

---

## D-023 — What does `CONFIRMED` mean for a dependency?

**Question.** Under D-004, a dependency is `CONFIRMED` both when a schedule explicitly states it and when
a human confirms it. These differ: a schedule link is evidenced by an authoritative source, not by a
GridPulse reviewer; and schedules can themselves be wrong or out of date.

**Options.** A. Single `CONFIRMED` status, with the basis (source-explicit vs human-confirmed) recorded
as an attribute. B. Separate statuses.

**Recommendation.** A — keeps D-004's three statuses while preserving provenance for the evidence view.

**Status.** OPEN

---

## D-024 — What is an "authorized user" in the MVP?

**Question.** D-001 lets an *authorized* user create `CONFIRMED` events, but D-015 defers authentication
and authorization. How is authorization represented in the prototype?

**Options.** A. A simple role flag on benchmark users (no real authentication). B. Defer; treat all MVP
users as authorized.

**Recommendation.** A — the concept of "who may confirm" is part of the trust architecture and should
exist in the model even before real security is built.

**Status.** OPEN

---

## D-025 — Must the first demo exercise AI-inferred dependencies?

**Question.** D-003 allows the benchmark graph to be built from schedule links and manual seeding.
If every link in the demo is `CONFIRMED`, the demo never shows `INFERRED` handling — yet Risk 1 (graph
quality) is the largest technical risk.

**Options.** A. Demo uses only schedule/seeded links. B. Demo includes at least one AI-inferred link
(e.g. installation → HV commissioning inferred from a commissioning plan), scored against seeded
ground truth.

**Recommendation.** B — it tests the riskiest capability and shows labelling of inferences.

**Status.** OPEN
