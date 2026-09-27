# Decisions Log

Open product and architecture questions identified while translating the product vision into
specification. **None of these are decided.** Each carries a recommendation for the founder to accept,
change or reject before implementation.

Status values: `OPEN` (awaiting founder), `ACCEPTED`, `REJECTED`, `SUPERSEDED`.

| ID | Question | Status |
|---|---|---|
| D-001 | Which events require human review? | OPEN |
| D-002 | How does GridPulse relate to source systems of record? | OPEN |
| D-003 | How is the initial project state and graph established? | OPEN |
| D-004 | Do AI-inferred dependencies require human confirmation? | OPEN |
| D-005 | Where exactly is the Level 2 / Level 3 line for date comparisons? | OPEN |
| D-006 | How is confidence represented? | OPEN |
| D-007 | Is the event taxonomy fixed or extensible? | OPEN |
| D-008 | How are reviewers and responsible people identified? | OPEN |
| D-009 | What is the relationship between an Event and a Change? | OPEN |
| D-010 | Is "correct" a distinct review action? | OPEN |
| D-011 | How are conflicting sources handled? | OPEN |
| D-012 | How much history does the trusted state keep? | OPEN |
| D-013 | Which customer/persona is the MVP designed around? | OPEN |
| D-014 | Which intake channel(s) does the MVP support? | OPEN |
| D-015 | What are the data-confidentiality and hosting expectations? | OPEN |
| D-016 | How are gates defined and how is gate status determined? | OPEN |
| D-017 | How is investigation compression measured, and on what data? | OPEN |
| D-018 | Single project or portfolio? | OPEN |
| D-019 | Is "Ask GridPulse" in the MVP? | OPEN |
| D-020 | Can the trusted state be edited outside the event path? | OPEN |

---

## D-001 — Which events require human review?

**Question.** The vision says "human reviews *consequential* changes" but does not define consequential.
Does every AI-detected event need review, or only some?

**Options.**
- A. Every AI-detected event requires review before entering the trusted state.
- B. Only events above a consequence threshold (by type, affected entity, or potential downstream
  impact) require review; others enter automatically.
- C. Configurable per project / customer.

**Recommendation.** A for the MVP.

**Reasoning.** Trust is the product. Until precision is measured, auto-accepting anything risks
polluting the trusted state. Review volume is a real risk (see risks) and B/C can be introduced once
data exists on which events are reliably low-consequence.

**Status.** OPEN

---

## D-002 — Relationship to source systems of record

**Question.** GridPulse maintains a "trusted project state", while P6/Aconex/etc. remain the systems
of record. When a reviewer confirms a new delivery date in GridPulse, what happens relative to P6?

**Options.**
- A. Strictly read-only: GridPulse never writes back; its trusted state may legitimately diverge from
  the source system until the source is updated, and GridPulse surfaces that divergence.
- B. Write-back: confirmed changes are pushed to source systems.
- C. Read-only for MVP, write-back as a later optional feature.

**Recommendation.** A for MVP (effectively C long-term, only if customers ask).

**Reasoning.** The vision positions GridPulse as an intelligence layer, not a replacement. Writing to
schedules crosses into project-control authority and conflicts with "not an autonomous project manager".
Divergence between "what the supplier says" and "what the schedule says" is itself valuable signal.

**Status.** OPEN

---

## D-003 — How is the initial project state and graph established?

**Question.** The killer scenario assumes GridPulse already holds dates and the delivery → installation
→ HV commissioning → grid compliance → energization chain with evidence. Where does that come from?

**Options.**
- A. Import from a schedule (e.g. P6/MS Project export) — activities, dates and logic links.
- B. AI extraction from project documents (schedules, commissioning plans, grid requirements).
- C. Manual seeding by a user.
- D. A combination (e.g. schedule import for logic + AI extraction for cross-document links).

**Recommendation.** D, with the MVP starting from a schedule export plus a small set of supporting
documents, and manual seeding allowed for gaps.

**Reasoning.** Schedule logic gives explicit, evidence-backed dependencies (Level 1-ish); documents
supply links schedules miss (e.g. grid-requirement → compliance test). Pure AI extraction for the
initial graph is the highest-risk path and would dominate MVP effort.

**Status.** OPEN

---

## D-004 — Do AI-inferred dependencies require human confirmation?

**Question.** Events are reviewed, but dependencies (Level 2) are also AI output. Must they be
confirmed before impact analysis uses them?

**Options.**
- A. Yes — only confirmed dependencies are used.
- B. No — inferred dependencies are used but always labelled as inference with evidence.
- C. Both are used; impact output distinguishes paths made entirely of confirmed/explicit links from
  paths containing unconfirmed inferences.

**Recommendation.** C.

**Reasoning.** A would make the graph too sparse to be useful early; B risks false impact chains
looking authoritative. C keeps recall high while making the evidence quality of each path visible.

**Status.** OPEN

---

## D-005 — The Level 2 / Level 3 line for date comparisons

**Question.** In the scenario, the new delivery date (Feb 2) is after the planned installation date
(Jan 15). Stating "delivery is now after planned installation start" is arithmetic on two facts.
Stating "energization is delayed 21 days" is a conclusion. Where between these may GridPulse go?

**Options.**
- A. GridPulse may state deterministic comparisons between evidenced dates (e.g. "new delivery date is
  18 days after the planned installation date"), labelled as such, but never propagate delays through
  the chain.
- B. GridPulse may also compute a *hypothetical* propagation ("if all links are finish-to-start with no
  float, energization would move to X") clearly labelled as hypothetical.
- C. GridPulse states only that a potential impact exists, with no date arithmetic.

**Recommendation.** A for MVP.

**Reasoning.** A is still Level 1/2 and dramatically improves usefulness ("this is clearly a conflict")
without asserting schedule outcomes. B is close to a delay claim and easy to misread; it should be a
deliberate founder decision. C likely under-delivers against a 4-hour manual investigation.

**Status.** OPEN

---

## D-006 — How is confidence represented?

**Question.** Events carry "confidence". Numeric score, categories, or something else?

**Options.**
- A. Numeric (0–1) from the model.
- B. Categorical (high / medium / low) with stated reasons.
- C. Evidence-based: confidence derived from source type and quality of evidence, plus reasons.

**Recommendation.** B or C shown to users; raw numbers kept internally for evaluation.

**Reasoning.** LLM-produced numeric confidences are poorly calibrated; a precise-looking number invites
false trust. Reasons ("explicit statement from supplier in email dated…") are more useful to reviewers.

**Status.** OPEN

---

## D-007 — Is the event taxonomy fixed or extensible?

**Question.** The vision lists 12 event types including OTHER. Is this the fixed set?

**Options.**
- A. Fixed list.
- B. Initial list, extensible later (by GridPulse), OTHER as catch-all.
- C. Customer-definable types.

**Recommendation.** B. For MVP, only delivery/shipment events need full support.

**Reasoning.** A fixed core keeps impact logic tractable; extensibility supports later domains without
the complexity of customer-defined semantics.

Also open: the vision lists both `SHIPMENT_DELAY` and `DELIVERY_DATE_CHANGE`, and the scenario calls its
event "SHIPMENT / DELIVERY EVENT". Are these distinct types (shipment in transit vs. contractual
delivery date change) or one?

**Status.** OPEN

---

## D-008 — How are reviewers and responsible people identified?

**Question.** GridPulse should "identify relevant reviewers" and "responsible people". That needs
knowledge of people, roles and responsibilities. Where does it come from?

**Options.**
- A. Manual assignment per event in MVP.
- B. A simple project role/responsibility matrix entered by users, used for suggestions.
- C. AI-inferred from documents (RACI, contracts, org charts, email patterns).

**Recommendation.** A for MVP, B next, C only as suggestion with evidence.

**Reasoning.** Routing is not the core of the killer scenario; wrong automatic routing is costly.

**Status.** OPEN

---

## D-009 — Relationship between Event and Change

**Question.** The UI vision lists "Events" (things that happened or may have changed) and "Changes"
(confirmed changes to project state). Are Changes a separate object, or a filtered view of confirmed
events?

**Options.**
- A. A Change is a confirmed Event (same object, different status/view).
- B. A Change is a separate record of a state transition produced by one or more confirmed Events
  (e.g. several emails confirm one date move).
- C. Undefined for now.

**Recommendation.** B.

**Reasoning.** Multiple sources often report the same real-world change; and some confirmed events
(e.g. an RFI issued) may not change any tracked state value. Separating them avoids double-counting and
keeps "what changed?" answers clean.

**Status.** OPEN

---

## D-010 — Is "correct" a distinct review action?

**Question.** The scenario shows only CONFIRM; the vision says humans can "review and correct". Can a
reviewer edit the AI's proposal (e.g. fix the date or the affected entity) and confirm?

**Options.**
- A. Confirm / reject only; corrections via a new manual event.
- B. Confirm / correct-and-confirm / reject, storing both the AI proposal and the human correction.

**Recommendation.** B.

**Reasoning.** "Corrections become part of the trusted project state" is an explicit requirement, and
retaining the AI-vs-human delta is the raw material for measuring and improving precision.

**Status.** OPEN

---

## D-011 — Conflicting sources

**Question.** What if sources disagree (supplier email says Feb 2; latest P6 update still says Jan 12;
a meeting minute says "late January")?

**Options.**
- A. Latest source wins automatically.
- B. Surface a contradiction as its own reviewable item, showing all evidence; the human decides.
- C. Source-authority ranking (e.g. contract/PO > supplier email > minutes).

**Recommendation.** B, optionally informed by C as a hint.

**Reasoning.** "Find contradictions" is an explicit AI capability, and deciding which source is right
is a human judgement consistent with the review principle.

**Status.** OPEN

---

## D-012 — How much history does the trusted state keep?

**Question.** "What's changed since last week?" and evidence versioning imply GridPulse must know
past states. How much history is kept?

**Options.**
- A. Current state only, plus an event log.
- B. Full history: every state value is reconstructable as of any past time (by detected time and by
  effective time).

**Recommendation.** B, conceptually — implemented as an append-only record of events and reviews.

**Reasoning.** Auditability, "what changed" questions and evaluation all need it; retrofitting history
later is expensive. Note the two time axes (detected vs effective) both matter.

**Status.** OPEN

---

## D-013 — Which customer/persona is the MVP designed around?

**Question.** Eight customer types are listed. Their workflows differ (e.g. an Owner's Engineer
reviews others' information; an EPC owns the schedule; a TDD firm works point-in-time).

**Options.** BESS developer · Owner's Engineer · project-control consultancy · EPC · other.

**Recommendation.** Founder decision based on design-partner access. Owner's Engineers / developers'
project-control teams appear closest to the "investigate impact of a change and route to experts"
workflow, and are not themselves the schedule owner (consistent with D-002).

**Reasoning.** The MVP should be designed around real workflows of one user type rather than an
average of eight.

**Status.** OPEN

---

## D-014 — Which intake channel(s) does the MVP support?

**Question.** Six channels are listed; the MVP should not build all.

**Options.**
- A. Manual entry only.
- B. Document upload (including emails exported/uploaded as files) + manual entry.
- C. Live email ingestion (mailbox connection).
- D. Schedule import.

**Recommendation.** B, plus D as a one-off import for the initial state (see D-003).

**Reasoning.** The killer scenario starts from a supplier email; uploading that email exercises AI
detection without the security/integration work of mailbox access.

**Status.** OPEN

---

## D-015 — Data confidentiality and hosting

**Question.** Project data (contracts, grid documents, supplier pricing) is commercially sensitive and
sometimes subject to critical-infrastructure rules. The vision does not address this.

**Options.** Multi-tenant cloud · single-tenant cloud · customer-hosted / on-prem · per-customer choice.
Plus: which AI providers customers will accept processing their data.

**Recommendation.** No recommendation yet — gather requirements from the first design partners before
choosing a stack, because the answer constrains architecture and AI-provider choices.

**Status.** OPEN

---

## D-016 — Gates: definition and status

**Question.** Gates (grid connection, engineering completion, procurement readiness, construction
completion, commissioning, grid compliance, energization, COD) are listed, but not how a gate's status
is determined.

**Options.**
- A. Gates as graph nodes that impact analysis can reach, with no status logic (MVP).
- B. Gates with evidence checklists (requirements that must be evidenced), showing missing evidence.
- C. Gates with a computed "ready / not ready" status.

**Recommendation.** A for MVP; B later. Avoid C unless explicitly a human sign-off.

**Reasoning.** A computed "ready" status risks becoming a Level 3 conclusion; missing-evidence
checklists stay within GridPulse's role.

**Status.** OPEN

---

## D-017 — Measuring investigation compression

**Question.** The critical metric is investigation compression with acceptable evidence precision and
recall. What is the baseline, what is "acceptable", and what data is used?

**Options.**
- A. Synthetic BESS project dataset with a hand-built ground-truth graph and scripted events.
- B. Anonymised real project data from a design partner, with experts timing manual investigations.
- C. A followed by B.

**Recommendation.** C. Define acceptable precision/recall thresholds with design partners before
claiming the targets.

**Reasoning.** Synthetic data allows early, repeatable evaluation; only real data can validate the
4 h → 15 min + 30–60 min hypothesis.

**Status.** OPEN

---

## D-018 — Single project or portfolio?

**Question.** Is the unit of use one project, or do users need cross-project views (e.g. the same
transformer supplier slipping on several projects)?

**Options.** Single project in MVP · portfolio from the start.

**Recommendation.** Single project in MVP; keep entities (e.g. suppliers) modelled so that
cross-project views are possible later.

**Status.** OPEN

---

## D-019 — Is "Ask GridPulse" in the MVP?

**Question.** Natural-language investigation is part of the eventual experience, but the vision warns
against becoming "chat with your PDFs".

**Options.**
- A. Exclude from MVP.
- B. Include a narrow version answering over the trusted state and graph, always with evidence.
- C. Include general document Q&A.

**Recommendation.** A for the first demo; B soon after. Avoid C.

**Reasoning.** The killer scenario does not need it; building it first risks drifting into the
generic-chatbot positioning the vision rejects.

**Status.** OPEN

---

## D-020 — Can the trusted state be edited outside the event path?

**Question.** Can a user directly edit a value in the trusted state (e.g. fix a wrong date), or must
every change be an event?

**Options.**
- A. Direct edits allowed.
- B. All changes are events; "manual entry" is an intake channel producing an event that is recorded
  (and, if entered by an authorised reviewer, confirmed immediately).

**Recommendation.** B.

**Reasoning.** Keeps a single intake mechanism (P5) and a complete, evidence-bearing history (P8).

**Status.** OPEN
