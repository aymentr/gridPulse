# Phase 1 — Domain & System Architecture

**Status:** **ARCHITECTURE REVIEWED — VALIDATION REQUIRED BEFORE IMPLEMENTATION.**
Phase 0 is locked; council-review amendments (D-041 – D-047) and the five blocking decisions
(D-026, D-027, D-032, D-033, D-037) are applied. Phase 2 is **BLOCKED — validation gate not yet passed**.

This document defines the GridPulse intelligence model precisely enough that Phase 2 can implement it
without inventing product semantics while coding. It is **conceptual architecture**:

- no technology stack, framework, database, LLM provider or hosting choice
- no database schema, migrations, API endpoints, UI components or AI agents
- attribute lists are *conceptual contents*, not table definitions

Open architecture questions raised here are logged in `DECISIONS.md` (D-026 onward) and referenced
inline as **[D-xxx]**.

---

## 0. Contents

1. Architectural overview
2. Source-of-truth architecture
3. Cross-cutting models: provenance, confidence & validation, time
4. Domain model
5. Claim model and the discovery / determination boundary
6. Evidence architecture
7. State machines
8. Change model
9. Project Intelligence Graph
10. Impact model
11. Validated Project Intelligence
12. AI pipeline boundaries
13. Ask GridPulse (narrow)
14. Gates (MVP)
15. Benchmark architecture
16. Canonical vertical slices (transformer divergence; PCS specification change)
17. Security architecture (requirements only)
18. Explicit non-goals
19. Architectural quality test
20. Readiness for Phase 2

---

## 1. Architectural overview

The core of GridPulse is an **intelligence model**, not an application. Every user-facing surface
(Review Queue, Changes, Impact, Ask GridPulse, dashboards) is a *reader* of, or a *review input to*, this
model.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ AUTHORITATIVE PROJECT SOURCES  (systems of record — GridPulse is read-only)  │
│ Aconex · Primavera/P6 · MS Project · SharePoint · Procore · Excel ·          │
│ engineering systems · commissioning systems · email · manual entry           │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │  one universal intake path
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ GRIDPULSE                                                                    │
│                                                                              │
│  Intake ─► Document / DocumentVersion (what GridPulse has read)              │
│                 │                                                            │
│                 ▼                                                            │
│  AI investigation pipeline (classification, extraction, change detection,   │
│  evidence linking, dependency discovery, impact analysis)                    │
│                 │  produces                                                  │
│                 ▼                                                            │
│  Claims · Changes · potential Events · Dependencies · Conflicts · Impacts    │
│  — packaged as FINDINGS, each backed by EVIDENCE                             │
│                 │                                                            │
│                 ▼                                                            │
│  HUMAN REVIEW  (CONFIRM · REJECT · REQUEST_INVESTIGATION · EDIT_FINDING)     │
│                 │                                                            │
│                 ▼                                                            │
│  VALIDATED PROJECT INTELLIGENCE  ◄──►  PROJECT INTELLIGENCE GRAPH            │
│                 │                                                            │
│                 ▼                                                            │
│  IMPACT ANALYSIS ─► ATTENTION / ACTION (routed to reviewers)                 │
│                                                                              │
│  Audit history of every GridPulse action (append-only)                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │ read
                                   ▼
        Surfaces: Review Queue · Changes · Impact · Gates · Ask GridPulse · Benchmark harness
```

Architectural invariants (each is enforced by the model, not by the UI):

| # | Invariant |
|---|---|
| I-1 | GridPulse never writes to an external system (MVP). |
| I-2 | Every important claim has at least one Evidence record. |
| I-3 | Only explicit human review — or an authorized user's manual entry — sets validation status to `CONFIRMED`. AI output, AI-extracted relationships and imported source data remain `UNVALIDATED` and labelled as such. Validated Project Intelligence contains only `CONFIRMED` items (D-027). |
| I-4 | Validated Project Intelligence changes only through a Review or an authorized manual entry. There is no direct edit path. |
| I-5 | Contradictory information is never silently resolved; it becomes a CONFLICT finding. |
| I-6 | GridPulse never produces a Level 3 determination. It may surface a candidate Level 3 implication only as *potential exposure — validation required*. |
| I-7 | Every state transition of every GridPulse object is recorded, with actor, time and reason. History is append-only. |
| I-8 | Inferred relationships are always labelled as inferred wherever they are used. |
| I-9 | The benchmark observes the product through the same intake path and the same model as a user; ground truth is never visible to the pipeline. |
| I-10 | One project per GridPulse instance of the model (MVP). Identifiers are project-scoped so multi-project is possible later. |

---

## 2. Source-of-truth architecture

```
AUTHORITATIVE PROJECT SOURCES
        ↓
    GRIDPULSE
        ↓
AI investigation / extraction / inference
        ↓
     HUMAN REVIEW
        ↓
VALIDATED PROJECT INTELLIGENCE
```

### 2.1 External systems — systems of record

Aconex, Primavera/P6, Microsoft Project, SharePoint, Procore, Excel, engineering systems, commissioning
systems, email. They remain authoritative for their domains, e.g.:

| Information | Typical authority (project-dependent) |
|---|---|
| Contractual correspondence, transmittals, controlled documents | Aconex / document-management system |
| Official schedule | Primavera / MS Project (often EPC-owned) |
| Engineering data and design | Engineering systems / engineering document register |
| Test certificates, commissioning records | Commissioning systems / test reports |

Which source is authoritative for which information is a *project configuration fact*, used for
display and conflict explanation only — never to auto-resolve conflicts **[D-036]**.

### 2.2 What GridPulse owns

- extracted intelligence (claims, entities, requirements extracted from sources)
- detected changes
- findings
- dependency interpretations (including inferred dependencies and their status)
- reviews and reviewer actions
- Validated Project Intelligence
- investigations and impact analyses
- audit history of GridPulse actions

### 2.3 What GridPulse does not own

- contractual truth
- engineering approval
- the official schedule
- the official document repository or its version history
- regulatory or grid certification

### 2.4 Divergence is information, not error

Validated Project Intelligence may legitimately differ from a system of record — e.g. a reviewer
validated the supplier's new delivery date while the EPC's schedule still shows the old one. GridPulse
shows both, with evidence, as a **source divergence**. It never "corrects" the system of record and
never hides the divergence.

---

## 3. Cross-cutting models

### 3.1 Provenance

Every Claim, Dependency, Change, Event and Finding records **how it came to exist** and **every
subsequent human action on it**. Provenance is a list, not a single value — e.g. a dependency can be
`AI_INFERRED` and later `HUMAN_CONFIRMED`.

| Provenance type | Meaning |
|---|---|
| `SCHEDULE_DERIVED` | Deterministically imported from explicit schedule data (dates, logic links) |
| `DOCUMENT_DERIVED` | Explicitly stated in a document/email/record |
| `AI_EXTRACTED` | Extracted from the source by AI (paired with `DOCUMENT_DERIVED` for AI-extracted explicit statements) |
| `STRUCTURED_IMPORT` | Deterministically imported from other structured data (e.g. a spreadsheet register) |
| `AI_INFERRED` | Reasoned by AI; not explicitly stated by any source |
| `CALCULATED` | Deterministic calculation over other claims (inputs recorded) |
| `MANUAL_ENTRY` | Entered by a named person; the entry itself is the source record |
| `HUMAN_CONFIRMED` | A reviewer confirmed it (Review reference) |
| `HUMAN_EDITED` | A reviewer edited it (Review reference, before/after preserved) |
| `HUMAN_REJECTED` | A reviewer rejected it (Review reference) |

The founder-required minimum for dependencies (`SCHEDULE_DERIVED`, `DOCUMENT_DERIVED`,
`HUMAN_CONFIRMED`, `AI_INFERRED`) is a subset. "The schedule says it" (`SCHEDULE_DERIVED`) and
"an engineer validated it" (`HUMAN_CONFIRMED`) are never collapsed into one label.

### 3.2 Confidence and validation — three separate axes

GridPulse does **not** have a single "AI confidence score". It prefers explicit states over
pseudo-precise percentages. No percentage is shown unless a future validated statistical basis exists.

**Evidence confidence** — how strongly the available source supports the *factual observation*.

| Value | Criterion (initial rubric) |
|---|---|
| `HIGH` | Direct, unambiguous statement at a verified location in an identified source version |
| `MEDIUM` | Direct but hedged, partial or ambiguous statement; or source identity/version incomplete |
| `LOW` | Indirect, stale (superseded version), or from a source whose relevance is uncertain |

Evidence confidence rates *support for the observation*, not truth of the world: "Supplier states
delivery is expected Feb 2" can be `HIGH` even though "expected" is a forecast.

**Relationship confidence** — how strongly the evidence supports a *relationship between two entities*.

| Value | Meaning |
|---|---|
| `EXPLICIT` | A source explicitly states the relationship (schedule logic link; document sentence) |
| `INFERRED` | The relationship is reasoned from evidence but not stated by any source |

(Graded strength of inferences is deferred; each inference carries its reasoning and evidence instead.)

**Validation status** — whether a human has validated it (D-027).

| Value | Meaning |
|---|---|
| `UNVALIDATED` | No human has confirmed it. Applies to all observed/extracted claims, AI-extracted and AI-inferred relationships, and imported source data (including schedule-derived data — D-049). Usable in investigation, always labelled. |
| `CONFIRMED` | Confirmed (or edited and confirmed) by an authorized reviewer through explicit review, or entered by an authorized user as a manual fact (`MANUAL_ENTRY`). |
| `REJECTED` | Rejected by an authorized reviewer. |

Whether an item is *currently in the Review Queue* is a property of its Finding (§7.1), not a
validation value. Only explicit human action produces `CONFIRMED`.

Relationship confidence and validation status are **independent**: an explicitly stated relationship
can be `EXPLICIT · UNVALIDATED`; an inferred one can be `INFERRED · CONFIRMED` after review.

Display example: `Evidence: HIGH · Relationship: INFERRED · Validation: UNVALIDATED`.

### 3.3 Time

Every Claim, Change and Event distinguishes:

| Time | Meaning |
|---|---|
| Source time | When the source says the information was issued (email sent, document revision date) |
| Ingested time | When GridPulse received the information |
| Detected time | When GridPulse detected the change/finding |
| Effective time | When the change takes effect in the real project (e.g. the new delivery date applies from receipt of notice) |
| Reviewed time | When a human reviewed it |
| Validity interval | When a validated claim was current in Validated Project Intelligence (from/to) |

This allows "as of" questions ("what did GridPulse know last week?") over GridPulse's own history
without recreating the history of external systems.

---

## 4. Domain model

### 4.1 Concept map

```
Project
 ├─ Source ──► Document ──► DocumentVersion ──► (location) ◄── Evidence ◄── Claim
 │                                                                 ▲         │ about
 │                                                                 │         ▼
 ├─ Entity  (kinds: Equipment · Party[Supplier] · Contract · Requirement ·
 │           Milestone · Activity · Test · Gate · DocumentArtifact)
 │     ▲  ▲                                                                   │
 │     │  └── Dependency (typed edge; status + provenance + relationship conf.)│
 │     └───── TestResult (reported outcome of a Test)                         │
 │                                                                            │
 ├─ Change  (difference between two observations)──generates──► Event (potential)
 │                                                                            │
 ├─ Finding (reviewable package: Change/Event, Dependency, Conflict, Stale/Missing
 │           evidence, Fact) ◄── Review ◄── Reviewer (configured role/person)
 │
 ├─ Investigation ──produces──► Findings, Impacts
 └─ Impact (potential effect of a confirmed Change/Event on an Entity/Milestone/Gate)
```

Design rule: **Entity is the single supertype for project "things".** Equipment, Supplier, Party,
Contract, Requirement, Milestone, Test and Gate are *kinds* of Entity with kind-specific attributes.
This avoids a separate table-of-everything per concept while keeping the vocabulary explicit.
Attributes of entities (e.g. a delivery date) are never stored as bare values — they are **Claims**.

### 4.2 Concept definitions

Each concept: **Purpose · Represents · Does NOT represent · Lifecycle · Relationships · Provenance.**

---

#### Project
- **Purpose:** the boundary of one intelligence model.
- **Represents:** one infrastructure project (MVP: one large BESS) with its configuration: sources,
  reviewers and roles, the fixed gate set, source-authority notes.
- **Does NOT represent:** a portfolio, a programme, a company, or a contractual entity.
- **Lifecycle:** created → configured → active. (Archival/closure deferred.)
- **Relationships:** owns every other object; exactly one per model instance in the MVP.
- **Provenance:** configuration changes are audited (who, when, what).

#### Source
- **Purpose:** identify where information comes from and via which intake channel.
- **Represents:** an origin system or channel — e.g. "EPC P6 export", "Supplier correspondence
  (uploaded)", "Aconex document export", "Manual entry".
- **Does NOT represent:** an individual document, or an integration implementation.
- **Lifecycle:** registered → active → retired.
- **Relationships:** has many Documents; may carry a project-configured authority note ("authoritative
  for planned dates") **[D-036]**.
- **Provenance:** who registered it, channel type, when.

#### Document
- **Purpose:** a stable identity for an information record GridPulse has read, across its versions.
- **Represents:** any ingested record — file (spec, drawing register, report, contract), email,
  schedule export, structured dataset, or a manual-entry record.
- **Does NOT represent:** the official controlled document (that remains in the system of record);
  GridPulse is not a document-management system.
- **Lifecycle:** first ingested → has versions → (optionally) withdrawn from GridPulse.
- **Relationships:** belongs to a Source; has DocumentVersions; may be represented in the graph as a
  `DocumentArtifact` entity when its *content* participates in dependencies (e.g. "PPC specification
  references PCS specification").
- **Provenance:** source, external identifier (e.g. Aconex doc number) when available, ingestion record.

#### DocumentVersion
- **Purpose:** the exact content that evidence points to.
- **Represents:** one revision/issue/snapshot of a Document as received by GridPulse (e.g. PCS spec
  Rev 8; schedule data date 2026-01-05; a specific email message).
- **Does NOT represent:** the full revision history of the external system — only versions GridPulse
  actually ingested.
- **Lifecycle:** `CURRENT` → `SUPERSEDED` (a newer version of the same Document is ingested) or
  `UNAVAILABLE` (withdrawn). Never edited in place.
- **Relationships:** belongs to a Document; referenced by Evidence; compared by Change detection.
- **Provenance:** source revision label, source time, ingested time, content fingerprint. (Whether
  GridPulse retains full content or a reference — **[D-030]**.)

#### Evidence
- **Purpose:** make a claim inspectable — "why does GridPulse believe this?"
- **Represents:** a pointer from a Claim to a precise location in a DocumentVersion, plus the quoted or
  extracted content at that location and its evidence confidence.
- **Does NOT represent:** the claim itself, or a judgement about the world.
- **Lifecycle:** `CURRENT` → `STALE` (its DocumentVersion was superseded, or the cited content no
  longer appears in the current version) / `UNAVAILABLE`.
- **Relationships:** supports one or more Claims; points to exactly one DocumentVersion location.
- **Provenance:** how the location was found (deterministic parse, AI extraction), verification result
  (see §6.3).

#### Claim
- **Purpose:** the atomic unit of assertion. Everything GridPulse "knows" or "says" is a Claim.
- **Represents:** a statement about an entity/attribute/relationship with a **level** (1, 2, or a
  human-authored 3), value, provenance, evidence, evidence confidence and validation status. An
  `UNVALIDATED` Level 1 claim is **observed information**; a `CONFIRMED` one is part of Validated
  Project Intelligence.
  Examples: "Supplier states transformer delivery expected Feb 2" (L1); "New delivery is 18 calendar
  days after planned installation" (L1, calculated); "Transformer installation precedes HV
  commissioning" (L2).
- **Does NOT represent:** an AI determination of consequences (Level 3 is never AI-authored).
- **Lifecycle:** `UNVALIDATED` → `CONFIRMED` | `REJECTED`; `CONFIRMED` → `SUPERSEDED` when a later
  confirmed claim replaces it. Most claims stay `UNVALIDATED` (observed information); only
  consequential ones are reviewed (D-026). Authorized manual entries enter as `CONFIRMED`.
- **Relationships:** about an Entity (or a Dependency); supported by Evidence; may be inputs to a
  calculated Claim; grouped into Findings.
- **Provenance:** required; see §3.1.

#### Entity
- **Purpose:** the nodes of project reality that intelligence is about.
- **Represents:** an identified project thing, of a kind: Equipment, Party (incl. Supplier), Contract,
  Requirement, Milestone, Activity, Test, Gate, DocumentArtifact.
- **Does NOT represent:** a task to be managed, a work package to be scheduled, or a BIM/CAD object.
- **Lifecycle:** `PROPOSED` (discovered) → `ACTIVE` (resolved identity) → `MERGED` (identified as the
  same as another entity) | `RETIRED`. Entity identity resolution (e.g. "main transformer" = "TX-01" =
  "Power Transformer T1") is a first-class step **[D-028]**.
- **Relationships:** subject of Claims; endpoints of Dependencies; affected by Changes/Events/Impacts.
- **Provenance:** the evidence where each alias/identifier was seen; merge decisions.

> *Activity* is used for dated work such as "transformer installation" or "HV commissioning", which
> are not zero-duration milestones. It carries only the dates needed for intelligence (as claims) — it
> is **not** a task-management object **[D-039]**.

#### Equipment
- **Purpose:** physical assets whose delivery, specification and testing drive project exposure.
- **Represents:** e.g. main power transformer, PCS, battery containers, MV/HV switchgear, protection
  relays, PPC, metering.
- **Does NOT represent:** asset management records, SCADA tags, BIM objects, or live operational data.
- **Lifecycle:** as Entity.
- **Relationships:** `SUPPLIED_BY` Supplier; `SPECIFIED_BY` DocumentArtifact/Requirement;
  `VERIFIED_BY` Test; `PART_OF` system; predecessor of Activities (delivery → installation).
- **Provenance:** as Entity; attribute values are Claims with evidence.

#### Party
- **Purpose:** identify organizations and people relevant to responsibility and communication.
- **Represents:** owner/developer, EPC, OE, supplier, grid operator, consultants, and their people.
- **Does NOT represent:** a CRM contact or an HR record.
- **Lifecycle:** as Entity.
- **Relationships:** `PARTY_TO` Contract; `SUPPLIES` Equipment (for suppliers); Reviewers may be
  linked to a Party.
- **Provenance:** as Entity.

#### Supplier
- **Purpose:** the Party kind whose statements most often generate delivery and specification changes.
- **Represents:** a manufacturer/vendor of equipment or services.
- **Does NOT represent:** procurement management or vendor rating.
- **Lifecycle / Relationships / Provenance:** as Party; `SUPPLIES` Equipment; linked to Contract/PO.

#### Contract
- **Purpose:** capture obligations that give changes contractual context (e.g. a delivery obligation).
- **Represents:** a contract or purchase order as an entity, with extracted obligations as Claims or
  Requirements.
- **Does NOT represent:** contractual truth, contract administration, claims management, or legal
  interpretation.
- **Lifecycle:** as Entity; contract revisions arrive as new DocumentVersions.
- **Relationships:** between Parties; `GOVERNS` Equipment/Milestones; source of Requirements.
- **Provenance:** Evidence into the contract DocumentVersion.

#### Requirement
- **Purpose:** what must be true (technical, grid, contractual, commissioning), so changes can be
  tested against it and missing evidence can be found.
- **Represents:** a requirement statement from a source (e.g. grid-code clause, specification clause,
  commissioning requirement), with its text as an L1 Claim.
- **Does NOT represent:** a compliance determination. GridPulse never certifies that a requirement is met.
- **Lifecycle:** `ACTIVE` → `CHANGED` (a Change to its text/values was confirmed) → `WITHDRAWN`.
- **Relationships:** `SPECIFIES` Equipment/Test; `VERIFIED_BY` Test; `CONTRIBUTES_TO` Gate; evidence
  of fulfilment links (documents, TestResults). Absence of fulfilment evidence can yield a
  `MISSING_EVIDENCE` finding.
- **Provenance:** Evidence to the source clause/version.

#### Milestone
- **Purpose:** key dated points against which exposure is described.
- **Represents:** a project milestone (e.g. "Transformer delivered", "Energization") whose planned,
  forecast or actual dates are Claims from one or more sources.
- **Does NOT represent:** GridPulse's own schedule. GridPulse does not compute milestone dates.
- **Lifecycle:** as Entity; its date claims change via Changes/Events.
- **Relationships:** `PRECEDES` / preceded by Activities/Milestones; `CONTRIBUTES_TO` Gate.
- **Provenance:** each date Claim carries its source (schedule, document, supplier, manual).

#### Gate (Checkpoint)
- **Purpose:** intelligence checkpoints where evidence and unresolved issues accumulate.
- **Represents:** one of the MVP fixed checkpoints (§14), e.g. ENERGIZATION CHECKPOINT. "Gate" is the
  domain term; user-facing names are neutral checkpoints (D-033).
- **Does NOT represent:** a contractual approval, a stage-gate workflow, or a readiness verdict.
  GridPulse never declares READY or NOT READY.
- **Lifecycle:** fixed set, always present in the MVP.
- **Relationships:** Milestones, Activities, Tests and Requirements `CONTRIBUTE_TO` Gates; Impacts
  may reach Gates.
- **Provenance:** gate definitions are product configuration; links to gates carry normal provenance.

#### Test
- **Purpose:** verification activities that link equipment and requirements to gates.
- **Represents:** a defined test or inspection (e.g. protection testing, HV commissioning tests, grid
  compliance tests).
- **Does NOT represent:** test execution management or test certification.
- **Lifecycle:** as Entity.
- **Relationships:** `VERIFIES` Requirement/Equipment; `PRECEDES`/preceded by Activities;
  `CONTRIBUTES_TO` Gate; has TestResults.
- **Provenance:** source test plans/procedures.

#### TestResult
- **Purpose:** capture reported outcomes so failures can generate changes and events.
- **Represents:** a reported result of a Test as stated in a test report (e.g. "FAIL — relay 87T
  trip time outside tolerance"), as L1 Claims.
- **Does NOT represent:** GridPulse's judgement of pass/fail or of compliance.
- **Lifecycle:** `REPORTED` → (superseded by a later result for the same test).
- **Relationships:** of a Test; may be evidence of fulfilment for a Requirement; a new result can
  produce a Change (e.g. PASS→FAIL or "not tested"→FAIL).
- **Provenance:** Evidence into the test report version.

#### Change
- **Purpose:** record *what differs* between two observations.
- **Represents:** a detected difference between two states, versions, records or observations of the
  same subject: (subject, attribute, old observation, new observation, evidence for both).
- **Does NOT represent:** something that happened in the world (that is an Event), nor a validated
  update (until confirmed).
- **Lifecycle:** `DETECTED` → `UNDER_REVIEW` → `CONFIRMED` | `REJECTED` (§7.2).
- **Relationships:** compares two Claims/DocumentVersions; may generate a potential Event; packaged in
  a Finding; confirmed Changes trigger impact Investigations.
- **Provenance:** detection method (deterministic comparison, AI-assisted comparison), both sides'
  evidence.

#### Event
- **Purpose:** record *what happened, or is reported to have happened,* in the real project.
- **Represents:** e.g. "Supplier informed the project that transformer delivery moved to Feb 2";
  "PCS specification Rev 8 issued"; "Protection test failed". Typed with a small taxonomy (§8.4).
- **Does NOT represent:** a GridPulse-internal difference (that is a Change) or a consequence.
- **Lifecycle:** `DETECTED` → `UNDER_REVIEW` → `CONFIRMED` | `REJECTED`; authorized manual entry
  → `CONFIRMED` directly (§7.3). Confirmed events are historical and are not "superseded" — later
  events change the *current validated claims*, not the fact that an earlier event occurred.
- **Relationships:** generated from a Change or entered manually; affects Entities; packaged in a
  Finding; triggers Investigations.
- **Provenance:** detection method or manual entry author; evidence; reviewer.

#### Finding
- **Purpose:** the **unit of human review**. Everything that needs a human decision is presented as a
  Finding.
- **Represents:** a package of Claims and evidence proposing something to the reviewer. Kinds:

  | Kind | Proposes |
  |---|---|
  | `CHANGE` | a Change and (usually) a potential Event |
  | `DEPENDENCY` | a new Dependency or a status change of one |
  | `CONFLICT` | that two sources disagree; asks the reviewer for the validated interpretation |
  | `STALE_EVIDENCE` | that evidence or a cross-document reference points to a superseded version |
  | `MISSING_EVIDENCE` | that a requirement/gate lacks supporting evidence |
  | `FACT` | a *consequential* extracted fact needing validation — not every extracted fact (D-026) |

- **Does NOT represent:** a task, a ticket, or a workflow case. No assignment chains, SLAs or approvals.
- **Lifecycle:** §7.1.
- **Relationships:** contains Claims; references Change/Event/Dependency; reviewed via Reviews; may
  have Investigations; routed to Reviewers.
- **Provenance:** producing pipeline stage and run; every revision (EDIT_FINDING) preserved.

#### Dependency
- **Purpose:** the edges along which change propagates.
- **Represents:** a typed, directed relationship between two Entities where a change to one may
  affect the other (§9.3), with relationship confidence, validation status, provenance and evidence.
- **Does NOT represent:** a schedule logic link to be calculated (no lags, float or CPM), nor a
  contractual obligation.
- **Lifecycle:** relationship confidence `EXPLICIT` | `INFERRED` (fixed at creation); validation
  `UNVALIDATED` → `CONFIRMED` | `REJECTED` (§7.4).
- **Relationships:** connects Entities; traversed by Impact analysis; proposed in DEPENDENCY Findings.
- **Provenance:** mandatory; `SCHEDULE_DERIVED`, `DOCUMENT_DERIVED` + `AI_EXTRACTED`, `AI_INFERRED`, `MANUAL_ENTRY`,
  plus `HUMAN_CONFIRMED` / `HUMAN_REJECTED` history.

#### Impact
- **Purpose:** state what a confirmed Change/Event **may** affect and why.
- **Represents:** a potential effect on an Entity reached through a dependency path, with the path,
  each link's status, evidence, deterministic calculations, relevant milestone/gate, uncertainty,
  suggested reviewer and unresolved question (§10.4).
- **Does NOT represent:** a determination that the entity *is* affected, a delay, or a redesign need.
- **Lifecycle:** `OPEN` → `ACKNOWLEDGED` | `DISMISSED` (by reviewer, with reason); `SUPERSEDED` when
  recomputed after the graph or validated intelligence changes **[D-029]**.
- **Relationships:** produced by an Investigation from a Change/Event; references Dependencies,
  Entities, Milestones, Gates; routed to Reviewers.
- **Provenance:** investigation run, graph snapshot used, dependency statuses at the time.

#### Investigation
- **Purpose:** a bounded, timed unit of investigative work — the thing whose duration GridPulse aims
  to compress.
- **Represents:** one of: `IMPACT` (triggered by a confirmed Change/Event), `REQUESTED` (triggered by
  REQUEST_INVESTIGATION on a Finding), `QUESTION` (an Ask GridPulse question).
- **Does NOT represent:** a project workflow, a case-management item, or an autonomous agent.
- **Lifecycle:** `REQUESTED` → `IN_PROGRESS` → `COMPLETED` (§7.5).
- **Relationships:** has a trigger (Finding, Change/Event, or question); produces Findings, Impacts
  or an Answer; records who/what performed it **[D-038]**.
- **Provenance:** trigger, inputs (graph and intelligence snapshot), timestamps, outputs.

#### Review
- **Purpose:** the auditable human decision at the trust boundary.
- **Represents:** one reviewer action on one Finding revision (or Impact).
- **Does NOT represent:** an engineering approval, a contractual acceptance, or a sign-off of the
  project; it validates *GridPulse's intelligence*, nothing more.
- **Lifecycle:** immutable once recorded.
- **Relationships:** by a Reviewer; on a Finding (revision); causes transitions of Finding, Change,
  Event, Dependency, Claims.
- **Provenance:** is itself provenance (§7.6 audit requirements).

#### Reviewer
- **Purpose:** make reviewer identity explicit so accountability exists now and authentication can be
  added later.
- **Represents:** a configured person with one or more project roles (e.g. Project Controls,
  Electrical Engineering, Commissioning, Grid Compliance) and the review actions each role may take
  (D-024).
- **Does NOT represent:** an authenticated account (no authentication in the prototype).
- **Lifecycle:** configured → active → deactivated.
- **Relationships:** performs Reviews; target of routing for Findings and Impacts; may be linked to a
  Party.
- **Provenance:** configuration audit.

---

## 5. Claim model and the discovery / determination boundary

### 5.1 Levels

| Level | Name | Definition | Examples | Authored by |
|---|---|---|---|---|
| **1** | **Fact** | Directly supported by evidence, or deterministically calculated from evidenced values | "Delivery date changed from Jan 12 to Feb 2." "The new delivery date is 18 calendar days after the planned installation date." | GridPulse (with evidence) or manual entry |
| **2** | **Dependency / inference** | A relationship or analytical inference supported by evidence | "The transformer delivery change may affect the transformer installation milestone." "Transformer installation appears to precede HV commissioning." | GridPulse, labelled with relationship confidence and validation status |
| **3** | **Engineering / project conclusion** | A consequential technical or project determination | "Energization will be delayed." "Protection settings must be redesigned." | **Humans only** |

### 5.2 Discovery vs determination

> **GridPulse must distinguish discovery from determination.**

| AI may discover / calculate | AI must not determine |
|---|---|
| PCS specification changed from Rev 7 to Rev 8. | The project will miss energization. |
| Rev 7 was referenced by the PPC specification. | Protection settings must be redesigned. |
| The PPC specification is referenced by the grid-compliance test plan. | The grid-compliance test will fail. |
| The new delivery date is 18 calendar days after the planned installation date. | Energization will be delayed by 18 days. |

Candidate Level 3 implications may be surfaced **only** in exposure form:

> *"Potential energization exposure identified. Engineering / project-control validation required."*

Rendering rules (apply to every surface, including Ask GridPulse):

1. Every claim displays its level.
2. Level 2 uses hedged relational language ("appears to", "may affect") and shows relationship
   confidence and validation status.
3. Level 3 is never phrased as an assertion by GridPulse. If a human records a Level 3 determination,
   it is attributed to that human **[D-031]**.
4. Deterministic calculations show their inputs (each an evidenced claim) and the operation.

### 5.3 Deterministic calculations permitted

- date differences (calendar days) between two evidenced dates
- ordering comparisons (A is before/after B)
- version comparisons (Rev 7 vs Rev 8; value X vs value Y)
- counts and set differences (requirements with/without fulfilment evidence)

Not permitted: forward/backward schedule passes, float/critical-path calculation, forecasting a
successor's date, working-day calendars (these belong to the scheduling system of record).
Conditional one-hop implications (e.g. "if this finish-to-start link holds, installation cannot start
before Feb 2") are an open question **[D-034]**.

---

## 6. Evidence architecture

### 6.1 Canonical chain

```
CLAIM
  ↓ supported by
EVIDENCE           (quote/extract, evidence confidence, freshness, verification)
  ↓ located in
DOCUMENT_VERSION   (revision / issue / snapshot as ingested)
  ↓ at
LOCATION           (page / section / chunk / field / message / row)
  ↑
DOCUMENT ← SOURCE
```

### 6.2 Location types by record kind

| Record kind | Location granularity |
|---|---|
| Document file (spec, report, contract, plan) | page, section/clause, chunk, quoted span |
| Email / supplier communication | message (sender, date, subject), paragraph/quoted span, attachment reference |
| Schedule export | activity ID, field (planned start/finish, logic link), data date |
| Structured data (spreadsheet/register) | sheet, row key, column |
| Manual entry | the manual-entry record: author, role, time, entered statement, stated basis |

Manual entries are evidence of *what a named person asserted*, not of the underlying world. Their
provenance is always `MANUAL_ENTRY` and visible.

### 6.3 Evidence verification

AI-cited evidence must be **mechanically verified** before a claim is shown: the quoted span (or field
value) must exist at the cited location in the cited version. Unverifiable citations are discarded or
downgraded to `LOW` and flagged. This is a deterministic anti-hallucination control, and its results
are auditable.

### 6.4 Freshness and stale evidence

- When a new DocumentVersion supersedes an old one, evidence pointing to the old version becomes
  `STALE` if the cited content changed or cannot be re-verified in the new version.
- A **stale reference** occurs when a current document references a superseded version of another
  document (e.g. the current PPC specification references PCS specification Rev 7 after Rev 8 was
  issued).
- Both produce `STALE_EVIDENCE` findings. They are measured by the benchmark (§15).

### 6.5 Rule

Every important AI-generated statement — every Claim of Level 1 or 2 shown to a user, every Impact,
every Ask GridPulse answer sentence — must resolve to at least one verified Evidence record. If it
cannot, GridPulse must say that it has no supporting evidence.

---

## 7. State machines

All transitions are recorded in the append-only audit history with: object, from-state, to-state,
actor (pipeline stage + run, or Reviewer), time, reason, and the Review reference when applicable.

### 7.1 Finding (the review unit)

```
            ┌────────────── EDIT_FINDING (new revision) ─────────────┐
            ▼                                                          │
DETECTED ─► UNDER_REVIEW ──────────────────────────────────────────────┘
               │   │   │
               │   │   └─ REQUEST_INVESTIGATION ─► INVESTIGATION_REQUESTED
               │   │                                   │ investigation COMPLETED
               │   │                                   └──────────► UNDER_REVIEW
               │   ├─ CONFIRM ─► CONFIRMED ─┐
               │   └─ REJECT  ─► REJECTED  ─┴─► SUPERSEDED (later finding replaces it)
```

| From | To | Trigger | Notes |
|---|---|---|---|
| — | `DETECTED` | Pipeline creates finding | Evidence verification and pre-review impact preview run here |
| `DETECTED` | `UNDER_REVIEW` | Finding complete and routed | Enters Review Queue |
| `UNDER_REVIEW` | `UNDER_REVIEW` | `EDIT_FINDING` | New revision; original preserved; reviewer then confirms or rejects |
| `UNDER_REVIEW` | `INVESTIGATION_REQUESTED` | `REQUEST_INVESTIGATION` | Creates an Investigation; Validated Project Intelligence unchanged; finding stays unresolved |
| `INVESTIGATION_REQUESTED` | `UNDER_REVIEW` | Investigation completed | New evidence/claims attached |
| `UNDER_REVIEW` | `CONFIRMED` | `CONFIRM` | Applies the finding to Validated Project Intelligence |
| `UNDER_REVIEW` | `REJECTED` | `REJECT` | Rationale required; nothing applied |
| `CONFIRMED`/`REJECTED` | `SUPERSEDED` | A later finding on the same subject is resolved | History retained |

Duplicate detections (e.g. a second email repeating the same new date) attach as additional evidence
to the open finding rather than creating a new one.

**Review Queue scope and priority (D-026).** Review is *consequential and selective*. Most extracted
claims and relationships are never queued; they remain `UNVALIDATED`, labelled, and usable. Findings
are raised and ordered as:

1. consequential changes
2. source conflicts
3. inferred dependencies involved in an active investigation
4. stale evidence
5. missing evidence relevant to a critical investigation

Goal: GridPulse must not create more review work than it saves. Review load is measured (§15.4).

### 7.2 Change

```
DETECTED ─► UNDER_REVIEW ─┬─► CONFIRMED
                          └─► REJECTED
```

A Change mirrors its Finding. While the Finding is `INVESTIGATION_REQUESTED`, the Change stays
`UNDER_REVIEW` (unresolved). A detected change never silently becomes confirmed.

### 7.3 Event

```
AI-detected:    DETECTED ─► UNDER_REVIEW ─┬─► CONFIRMED
                                          └─► REJECTED

Manual entry by authorized user:   ─────────► CONFIRMED   (provenance MANUAL_ENTRY)
Manual entry by non-authorized user: ───────► UNDER_REVIEW
```

Confirmed events are historical records and stay `CONFIRMED`. When a later event changes the same
attribute (e.g. supplier revises again to Feb 9), the *validated claim* for the delivery date is
superseded; the earlier event remains a true record that the supplier said Feb 2.

### 7.4 Dependency

A dependency has two independent axes, fixed at different times:

- **Relationship confidence** — set at creation from how the relationship was found:
  `EXPLICIT` (stated by a source: `SCHEDULE_DERIVED`, `DOCUMENT_DERIVED` + `AI_EXTRACTED`,
  `STRUCTURED_IMPORT`) or `INFERRED` (`AI_INFERRED`). Review does not change it.
- **Validation status** — changed only by explicit human action:

```
any origin (schedule, document, AI-extracted, AI-inferred) ─► UNVALIDATED
UNVALIDATED ──CONFIRM──► CONFIRMED  (+HUMAN_CONFIRMED)
UNVALIDATED ──REJECT───► REJECTED   (+HUMAN_REJECTED)
CONFIRMED   ──REJECT───► REJECTED   (new finding with new evidence)
REJECTED    ──CONFIRM──► CONFIRMED  (new finding with new evidence)
authorized MANUAL_ENTRY ─► CONFIRMED
```

The D-004 labels map onto these axes: "INFERRED" = relationship confidence `INFERRED`;
"CONFIRMED" / "REJECTED" = validation status.

| Rule | |
|---|---|
| D1 | Relationship confidence and validation status are separate and both always displayed, together with provenance. "The schedule says it" (`SCHEDULE_DERIVED`, `EXPLICIT`) is never shown as "an engineer validated it" (`HUMAN_CONFIRMED`). |
| D2 | Impact analysis may traverse `UNVALIDATED` and `CONFIRMED` links; never `REJECTED`. Paths containing any `INFERRED` or `UNVALIDATED` link are labelled accordingly. |
| D3 | An explicitly stated relationship extracted by AI is `EXPLICIT · UNVALIDATED · DOCUMENT_DERIVED/AI_EXTRACTED`. It never becomes `CONFIRMED` automatically (D-027). |
| D4 | If a schedule-derived link disappears in a newer schedule version, its evidence becomes `STALE` and a `CHANGE` finding is raised; nothing changes silently. |
| D5 | Rejecting a schedule-derived link changes GridPulse's intelligence only; the schedule is untouched and the divergence is shown **[D-040]**. |
| D6 | Deterministically imported schedule logic is `EXPLICIT · UNVALIDATED · SCHEDULE_DERIVED` (D-049). |

### 7.5 Investigation

```
REQUESTED ─► IN_PROGRESS ─► COMPLETED   (outcome: findings produced | impacts produced |
                                          answer produced | insufficient evidence)
```

Every Investigation records start/end timestamps and the reviewer time spent on its outputs — the raw
data for the investigation-time metric. (Cancellation is deferred.)

### 7.6 Review — actions and audit

| Action | Effect | Rationale required |
|---|---|---|
| `CONFIRM` | Finding → `CONFIRMED`; subject objects transition; claims enter Validated Project Intelligence | Optional |
| `REJECT` | Finding → `REJECTED`; nothing enters Validated Project Intelligence | **Yes** |
| `REQUEST_INVESTIGATION` | Finding → `INVESTIGATION_REQUESTED`; Investigation created; no intelligence change | **Yes** (the question) |
| `EDIT_FINDING` | New finding revision with corrected content; stays `UNDER_REVIEW` | **Yes** (what and why) |

Audit record for every Review: reviewer identity, role(s) used, authorization rule satisfied, action,
finding ID and revision, before/after content (for edits), rationale, timestamp, and the resulting
transitions. Reviews are immutable. No elaborate workflow (no multi-step approvals, SLAs,
delegation) in the MVP.

### 7.7 Impact

```
OPEN ─┬─► ACKNOWLEDGED (reviewer has taken it up)
      ├─► DISMISSED    (reviewer judges it not relevant — reason required)
      └─► SUPERSEDED   (recomputed)
```

"Acknowledged" never means "impact confirmed" in the Level 3 sense **[D-029]**.

---

## 8. Change model

### 8.1 Definition

> **Change = a detected difference between two states, versions, records or observations of the same
> subject.**

A Change always has: subject (entity + attribute, or document), old observation (claim + evidence),
new observation (claim + evidence), and the deterministic calculation of the difference where one
exists.

### 8.2 Flow

```
SOURCE
  ↓  intake (new DocumentVersion)
EXTRACTION → new Claims with Evidence
  ↓
CHANGE DETECTION  — compare new claims to current claims on the same subject
  ├─ same value ................................ no change (evidence added)
  ├─ different value, newer source supersedes .. CHANGE finding (+ potential Event)
  └─ different value, sources both current ..... CONFLICT finding
  ↓
POTENTIAL EVENT  (DETECTED → UNDER_REVIEW)
  ↓
HUMAN REVIEW  — CONFIRM / REJECT / REQUEST_INVESTIGATION / EDIT_FINDING
  ↓
CONFIRMED EVENT & CHANGE → Validated Project Intelligence updated → impact Investigation
REJECTED → nothing applied; retained in history
```

**Supersede vs conflict.** A newer version of the *same* document or the same party's later statement
normally supersedes (→ `CHANGE`). Disagreement between *different* current sources (supplier email vs
EPC schedule; spec vs drawing) is a `CONFLICT`. When the classification itself is uncertain, GridPulse
raises a `CONFLICT` — it never picks a winner. In the transformer scenario both apply: a Change
(supplier's new date vs previous validated date) and a divergence from the EPC schedule, which remains
visible after confirmation (§2.4).

### 8.3 Examples

| Case | Old observation | New observation | Change | Potential Event | Review outcome effect |
|---|---|---|---|---|---|
| Delivery date | Schedule update / previous progress report: delivery 12 Jan | Progress report: "revised delivery date of 2 February" | Transformer delivery date 12 Jan → 2 Feb (+21 cd) | `DELIVERY_DATE_CHANGE` (reason: as stated by supplier, if given) | Confirmed → validated delivery claim = 2 Feb; impact investigation starts |
| Equipment specification | PCS spec Rev 7 | PCS spec Rev 8 | Clause-level differences (e.g. rated output, protection interface) | `SPECIFICATION_CHANGE` | Confirmed → requirement/spec claims updated; documents referencing Rev 7 checked for stale references |
| Test result | Protection test: not yet tested | Test report: FAIL (stated reason) | Result state not-tested → FAIL | `TEST_FAILURE` | Confirmed → TestResult validated; impact on verified requirement, successors and gate |
| Requirement | Grid requirement v1: parameter X | Grid operator letter / v2: parameter Y | Requirement value X → Y | `GRID_OPERATOR_DECISION` or `SPECIFICATION_CHANGE` | Confirmed → requirement updated; linked tests/equipment evaluated for exposure |
| Schedule milestone | Schedule (data date 1): HV commissioning 10 Feb | Schedule (data date 2): 17 Feb | Milestone date 10 Feb → 17 Feb (+7 cd) | `SCHEDULE_CHANGE` | Confirmed → milestone claim updated (source: schedule); downstream exposure |
| Supplier statement | — (no prior statement) or previous letter | Supplier: "component X will be replaced by model Y" | Equipment component identity X → Y | `SPECIFICATION_CHANGE` (supplier-initiated) | Confirmed → equipment claim updated; requirements/tests referencing X flagged |

### 8.4 Event taxonomy (working list)

Small and extensible; broad categories with attributes (old, new, reason, affected entity) — D-007.

`DELIVERY_DATE_CHANGE` · `SPECIFICATION_CHANGE` · `SCHEDULE_CHANGE` · `TEST_FAILURE` ·
`EQUIPMENT_FAILURE` · `RFI` · `CHANGE_ORDER` · `PERMIT_CHANGE` · `GRID_OPERATOR_DECISION` ·
`CONSTRUCTION_PROGRESS` · `OTHER`

Descriptive labels ("delivery delay", "delivery pulled forward") are derived from old/new values, not
separate types. Final consolidation remains D-007.

---

## 9. Project Intelligence Graph

The graph is the central intelligence model. **It is not a scheduling engine and not a replacement
for Primavera/P6**: it holds typed relationships and evidence-backed claims; it does not compute dates.

### 9.1 Node types

| Node | Notes |
|---|---|
| Entity (all kinds: Equipment, Party/Supplier, Contract, Requirement, Milestone, Activity, Test, Gate, DocumentArtifact) | Project reality |
| Claim | Attribute values and assertions, with level |
| Evidence → DocumentVersion → Document → Source | Evidence chain (§6) |
| Change, Event | What differs / what happened |
| Finding, Review | Trust boundary |
| Impact, Investigation | Analysis outputs |

### 9.2 Relationship categories

| Category | Relationship types | Propagates impact? |
|---|---|---|
| **Dependency** (traversed by impact analysis) | `PRECEDES` (temporal/logical order), `REFERENCES` (content of A relies on content of B), `SPECIFIES` (requirement/spec defines entity/test), `VERIFIES` (test verifies requirement/equipment), `CONTRIBUTES_TO` (to a gate), `SUPPLIES` (supplier → equipment) | Yes, per matrix (§10.3) |
| **Structural** | `PART_OF`, `PARTY_TO`, `GOVERNS`, `SAME_AS` (entity resolution) | No (used for context and routing) |
| **Evidence** | `ABOUT` (claim → entity/dependency), `SUPPORTED_BY` (claim → evidence), `LOCATED_IN` (evidence → version), `VERSION_OF`, `FROM_SOURCE` | No |
| **Change/Event** | `COMPARES` (change → old/new claims), `GENERATES` (change → event), `AFFECTS` (change/event → entity) | Origin of propagation |
| **Review/analysis** | `PROPOSES` (finding → object), `REVIEWS` (review → finding), `TRIGGERED_BY`, `REACHES` (impact → entity), `ROUTED_TO` | No |

### 9.3 Attributes on every Dependency edge

| Attribute | Content |
|---|---|
| Type | One of the dependency types above |
| Provenance | List (§3.1) |
| Relationship confidence | `EXPLICIT` / `INFERRED` |
| Validation status | `UNVALIDATED` / `CONFIRMED` / `REJECTED` |
| Evidence | Evidence records (and, for inferences, the reasoning) |
| Source references | Documents/versions/activities supporting it |
| Timestamps | created, status changes, last verified against current sources |

Every other claim-bearing element carries the same provenance/confidence/validation/timestamp fields.

### 9.4 Construction

The graph is **reconstructed from available project information** — documents, a schedule when
available, supplier communications, manual facts, other imported data (D-003). A schedule is preferred
but not required; without it, `PRECEDES` links come from documents (e.g. commissioning plans,
method statements) or inference. GridPulse does not assume the first user controls the schedule.
Manual relationship seeding is permitted only to establish benchmark ground truth, never for the
dependencies the benchmark expects GridPulse to infer (§15.4).

---

## 10. Impact model

### 10.1 Flow

```
Confirmed Change / Event
  ↓
Direct impacts        — entities one dependency hop from the changed entity
  ↓
Dependency propagation — traverse permitted relationship types (matrix) over INFERRED/CONFIRMED links
  ↓
Secondary impacts     — entities two or more hops away
  ↓
Milestones            — dated points on or adjacent to the paths
  ↓
Checkpoints           — checkpoints (gates) reached via CONTRIBUTES_TO
  ↓
Potential exposure    — candidate Level 3 implications, phrased as exposure requiring validation
```

### 10.2 Two phases

| Phase | When | Purpose | Effect on intelligence |
|---|---|---|---|
| **Pre-review preview** | Finding is `DETECTED`/`UNDER_REVIEW` | Show the reviewer "what dependencies may be affected" | None; labelled preview |
| **Impact investigation** | After `CONFIRMED` | Full impact analysis and routing | Produces Impacts (`OPEN`) |

### 10.3 Propagation matrix (initial — to be validated by the benchmark) **[D-035]**

| Change kind | Traverses |
|---|---|
| Date / timing (delivery, milestone, activity) | `PRECEDES`, `CONTRIBUTES_TO` |
| Specification / technical | `REFERENCES`, `SPECIFIES`, `VERIFIES`, `CONTRIBUTES_TO` |
| Test result | `VERIFIES` (to requirement), `PRECEDES`, `CONTRIBUTES_TO` |
| Requirement | `SPECIFIES`, `VERIFIES`, `REFERENCES`, `CONTRIBUTES_TO` |
| Supplier / party | `SUPPLIES`, then per resulting change kind |

Traversal stops at gates, at a configured depth limit, or where no permitted relationship continues.
`REJECTED` links are never traversed. Any path with an `INFERRED` link is an inferred path.

### 10.4 Impact result contract

Every Impact exposes:

| Field | Example |
|---|---|
| Affected entity | HV commissioning (Activity) |
| Relationship | Transformer installation `PRECEDES` HV commissioning |
| Dependency status | Relationship: `INFERRED` · Validation: `UNVALIDATED` · Provenance: `AI_INFERRED` |
| Evidence | Commissioning plan §x: "HV commissioning shall commence once all HV equipment is installed" |
| Deterministic calculations | New delivery (2 Feb) is 18 cd after planned installation (15 Jan); 8 cd before planned HV commissioning (10 Feb) |
| Relevant milestone | HV commissioning (planned Feb 10, source: …) |
| Checkpoint | COMMISSIONING CHECKPOINT → ENERGIZATION CHECKPOINT |
| Uncertainty | Link is inferred; installation duration, float and resequencing options not evidenced |
| Reviewer | Electrical Engineering; Project Controls |
| Unresolved question | "Can transformer installation and HV commissioning be resequenced within the Feb 10 window?" |

Calculations are comparisons only; "8 cd before HV commissioning" does **not** mean 8 days of float.

---

## 11. Validated Project Intelligence

**Definition.** Validated Project Intelligence is GridPulse's internally validated view of project
information derived from authoritative project sources and human review. It is not the contractual,
legal, engineering, scheduling or other authoritative source of truth for the project.

**Contents:**

- current `CONFIRMED` Claims (human-reviewed, or entered by an authorized user)
- `CONFIRMED` Dependencies (with provenance showing origin and who confirmed)
- `CONFIRMED` Changes and Events
- the full review and audit history

**Not contents:** `UNVALIDATED` claims (observed information), `UNVALIDATED` dependencies (explicit or
inferred), unresolved findings, open impacts. These live in the graph, labelled, and may be used for
investigation and in Ask GridPulse answers — they are not validated intelligence (D-026, D-037).

**How it changes — the only path:**

```
SOURCE → DETECTION → FINDING → REVIEW → VALIDATED PROJECT INTELLIGENCE
```

plus authorized `MANUAL_ENTRY` (itself a recorded source with provenance). There is **no direct
edit**. Corrections are made through `EDIT_FINDING` or a new manual entry, both audited.

**History.** GridPulse retains the complete history of its own detected changes, findings, reviews,
confirmations, rejections, dependency status changes, evidence associations, investigation requests
and reviewer actions. It does **not** recreate Aconex-style document history or Primavera-style
schedule history — only the versions it ingested and used **[D-030]**.

---

## 12. AI pipeline boundaries

Conceptual stages — not agents, not an orchestration design, no model/provider choices.

| Stage | Inputs | Outputs | Deterministic / AI-assisted | Human validation | Must be auditable |
|---|---|---|---|---|---|
| **Ingestion** | Files, emails, schedule exports, structured data, manual entries | Document, DocumentVersion, fingerprint | Deterministic | No | Source, time, version, content fingerprint |
| **Classification** | DocumentVersion | Record type (spec, email, schedule, test report…), related entities (candidate) | AI-assisted (deterministic for structured imports) | No (errors surface downstream) | Classification result, method, run |
| **Extraction** | DocumentVersion (+ classification) | Claims (L1), entities & aliases, requirements, explicit relationships, each with location — all `UNVALIDATED` | AI-assisted (deterministic for schedule/structured) | Selective — only consequential items become findings (D-026) | Extracted items, locations, run |
| **Change detection** | New claims vs current claims per subject | Changes, CONFLICT findings, potential Events | Deterministic comparison once subjects resolved; AI-assisted for unstructured semantic diffs (e.g. spec clauses) and entity resolution | Yes — every AI-detected Change/Event | Both observations, comparison method |
| **Evidence linking** | Claims + cited locations | Verified Evidence, evidence confidence, freshness, STALE_EVIDENCE findings | Deterministic verification; AI-assisted confidence rationale | No (verification is mechanical) | Verification result per citation |
| **Dependency discovery** | Claims, entities, documents, existing graph | Dependencies (`EXPLICIT`: `SCHEDULE_DERIVED`, `DOCUMENT_DERIVED`/`AI_EXTRACTED`; `INFERRED`: `AI_INFERRED`), all `UNVALIDATED`, with reasoning | Deterministic for schedule logic; AI-assisted otherwise | Only explicit review makes any dependency `CONFIRMED`; inferred links in an active investigation are prioritised for review | Evidence, reasoning, provenance |
| **Impact analysis** | Confirmed Change/Event, graph, validated intelligence | Impacts with the §10.4 contract; exposure statements | Deterministic traversal + calculations; AI-assisted for explanation, uncertainty, unresolved questions, reviewer suggestion | Reviewers acknowledge/dismiss; Level 3 always human | Graph snapshot, paths, statuses, calculations |
| **Review** | Findings (with preview) | Reviews; state transitions | Human | Is the validation | Full review audit (§7.6) |
| **Validated Project Intelligence** | Confirmed findings, authorized manual entries | Updated validated claims/dependencies/events | Deterministic application of review outcome | — | Validity intervals, cause of every change |

Cross-stage guardrails:

- Everything AI produces or imports is `UNVALIDATED` until explicit human review; only an authorized
  manual entry starts as `CONFIRMED`.
- No stage may emit a Level 3 claim.
- Every AI-assisted output records the stage, run, inputs and evidence used, so it can be re-examined
  and benchmarked.

---

## 13. Ask GridPulse (narrow)

Included in the MVP (D-019, D-037). It is an **Investigation of kind `QUESTION`** over the intelligence
model — **not a general-purpose chatbot** and not document Q&A. It may use validated intelligence,
observed (unvalidated) information, inferred relationships and deterministic calculations, but every
answer must keep them distinct and must not hide uncertainty.

Minimum answer structure:

| Section | Content |
|---|---|
| **VALIDATED INFORMATION** | `CONFIRMED` claims and dependencies, with who confirmed them |
| **OBSERVED INFORMATION** | `UNVALIDATED` Level 1 claims from sources, with source and evidence confidence |
| **INFERRED RELATIONSHIPS** | `INFERRED` dependencies and other Level 2 inferences, with reasoning and validation status |
| **DETERMINISTIC CALCULATIONS** | Calculations with their inputs |
| **POTENTIAL EXPOSURES** | Candidate Level 3 implications phrased as exposure |
| **HUMAN VALIDATION REQUIRED** | What must be validated, and by which role |
| **EVIDENCE** | Verified evidence for every statement above |

If evidence is insufficient, the answer is:

> *"GridPulse does not have sufficient evidence to determine this."*

Level 3 questions ("Will we miss energization?") are answered with exposure, evidence and routing —
never a determination.

---

## 14. Checkpoints (MVP)

Small fixed set of neutral checkpoints (D-016, D-033):

```
GRID CONNECTION CHECKPOINT → ENGINEERING CHECKPOINT → PROCUREMENT CHECKPOINT
  → CONSTRUCTION CHECKPOINT → COMMISSIONING CHECKPOINT → GRID COMPLIANCE CHECKPOINT
  → ENERGIZATION CHECKPOINT → COD / HANDOVER CHECKPOINT
```

- Checkpoints are **intelligence checkpoints, not contractual approvals**.
- A checkpoint aggregates the **evidence and unresolved issues** relevant to it: linked
  milestones/activities/tests/requirements, open Impacts reaching it, `MISSING_EVIDENCE` and
  `STALE_EVIDENCE` findings, and conflicts.
- GridPulse **never** declares a checkpoint `READY` or `NOT READY`. Human experts determine readiness.
- Checkpoints are Entities of kind Gate, so configurable checkpoints can be added later without
  making the MVP a gate-management system.

---

## 15. Benchmark architecture

### 15.1 Purpose

Measure whether GridPulse **reduces investigation workload while avoiding unsupported conclusions**.
The benchmark explicitly separates:

- **Correct discovery** — detected the change, found the right evidence, traced the right
  dependencies, reached the right milestones/checkpoints, routed to the right reviewers.
- **Correct engineering determination** — *not produced by GridPulse*. The benchmark checks that
  GridPulse **did not** assert one.

### 15.2 Components

```
┌──────────────────────────┐     same intake path      ┌──────────────────────┐
│ Benchmark corpus          │ ─────────────────────────►│ GridPulse pipeline    │
│ (synthetic/public BESS    │                            │ + intelligence model  │
│  project: EPC reports,    │   scripted reporting       │                       │
│  schedule updates, specs, │   periods / change events  │                       │
│  submittals, manual facts)│ ─────────────────────────►│                       │
└──────────────────────────┘                            └──────────┬───────────┘
┌──────────────────────────┐                                         │ read outputs
│ Ground truth (sealed)     │                                         ▼
│ entities & aliases,       │ ─────────────► Scorer ◄── findings, claims, evidence,
│ dependencies (stated vs   │                           impacts, routing, answers,
│ inferable), expected      │                           audit timestamps
│ changes/conflicts/impacts,│
│ gates, reviewers,         │   Simulated / real reviewer actions (timed)
│ forbidden conclusions     │
└──────────────────────────┘
```

- The corpus enters through the **same intake path** as real data (I-9). No back door.
- Ground truth is stored separately and **never** visible to the pipeline.
- The corpus is organised the way an Owner's Engineer receives information: **by reporting period**
  (EPC monthly report, schedule update, submittals and revisions, meeting minutes, correspondence
  copied to the owner) — not as a stream of supplier emails the OE would not normally see (D-041).
- The scorer reads the product's own objects (Findings, Claims, Evidence, Impacts, routing, Reviews,
  audit timestamps).
- Human reviewers (or scripted reviewer decisions for automated runs) act through the normal review
  actions, so review time and correction rate are measured the same way as in real use.

### 15.3 Corpus realism tiers

A synthetic corpus written by the team is cleaner than real project data and will flatter results.
The benchmark therefore reports every metric **per tier** (D-044):

| Tier | Content | Purpose |
|---|---|---|
| T1 — Clean synthetic | Consistent naming, text-native documents | Functional correctness of the loop |
| T2 — Degraded synthetic | Inconsistent equipment names and revision labels, tables, scanned-style PDFs, long email chains, partial information | Robustness, entity resolution |
| T3 — Public real documents | Publicly available grid-connection requirements, tender specifications, test procedures, where licensing allows | Realism check against non-authored text |

Drawings, single-line diagrams and protection-setting files are **out of MVP scope** and recorded as a
known limitation (D-047).

### 15.4 Metrics

| Metric | Definition (initial) |
|---|---|
| Change detection | Precision and recall of detected Changes vs ground truth (subject, old, new correct) |
| **Cross-source divergence detection** | Recall of ground-truth disagreements between current sources (e.g. progress report vs schedule update) raised as CONFLICT findings (D-043) |
| Direct-impact recall | Share of ground-truth one-hop impacted entities surfaced |
| Secondary-impact recall | Share of ground-truth ≥2-hop impacted entities surfaced |
| **Inferred-dependency precision** (primary) | Share of `AI_INFERRED` dependencies that are correct per ground truth. Prioritised over recall: every false inferred link costs reviewer time |
| Entity-resolution accuracy | Correct vs incorrect alias merges (e.g. "main transformer" = TX-01 = "T1 132/33 kV") |
| Evidence precision | Share of cited evidence that actually supports its claim (location verified *and* semantically supportive) |
| Stale-evidence detection | Recall of ground-truth stale evidence / stale cross-document references |
| False-positive rate | Findings/impacts not in ground truth ÷ all findings/impacts |
| Reviewer routing | Share of findings/impacts routed to a ground-truth appropriate role |
| Checkpoint identification | Precision/recall of checkpoints reported as potentially exposed |
| **Review load** | Review items generated per real change, and reviewer minutes per change — tests Risk 2 directly |
| Investigation time | GridPulse processing time + measured reviewer time per investigation, vs a manual expert baseline on the same scenario |
| Human correction rate | Share of reviewed findings that were edited or rejected |
| **Unsupported-determination violations** (guardrail) | Outputs asserting a Level 3 conclusion, presenting an inferred link as fact, or characterising a party's intent. Target: **0** |

Every metric with a precision and a recall component is reported as **both numbers** — never
collapsed into a single score. Perfect recall is not required; for inferred dependencies precision
takes priority.

The **4 h manual → 15 min AI + 30–60 min expert** figure is a **product hypothesis/target only**, not
an industry fact and not validated evidence. The benchmark, and the timed comparison in
`VALIDATION_PLAN.md`, exist to test it. Review load and reviewer minutes count *against* the saving.

### 15.5 Ground-truth rules

- Ground truth marks each dependency as **stated** (explicit in a source) or **inferable** (not
  stated, but supported by evidence).
- Each canonical scenario has at least one inferable dependency that is **not** seeded anywhere the
  pipeline can see it (D-025).
- Ground truth lists **forbidden conclusions** per scenario that must never appear.
- Ground-truth domain content is synthetic and must not be presented as any real grid code or
  equipment standard.
- Synthetic and public data only (D-015).

---

## 16. Canonical vertical slices

Two co-primary scenarios (D-042). They exercise different strengths:

| | 16.A Transformer delivery divergence | 16.B PCS specification change |
|---|---|---|
| Change kind | Date | Technical specification |
| What it proves | Cross-source divergence detection and exposure tracing | Propagation through links **no schedule contains** |
| Where incumbents are strong | Schedulers propagate dates in P6 — GridPulse's value is *detecting that sources disagree*, not recalculating dates | Nowhere — this chain lives across documents |
| AI-inferred dependency | Transformer installation → HV commissioning | PCS reactive capability → grid reactive power requirement |
| Role in validation | Primary validation scenario (source divergence) | Primary **intelligence** scenario |

### 16.A Transformer delivery divergence

The value demonstrated here is **not schedule calculation** — it is **detecting divergence between
project information sources** (D-043).

#### 16.A.1 Project data (synthetic, D-032)

| Item | Value | Source in corpus |
|---|---|---|
| Transformer delivery (original) | **12 January** | Schedule update; previous period's progress report; purchase order |
| Transformer installation (planned) | **15 January** | Schedule update |
| HV commissioning | 10 February | Schedule update / commissioning plan |
| Grid compliance testing | 20 February | Schedule update / grid-connection test programme |
| Energization | 1 March | Schedule update / grid-connection agreement |

Dependency ground truth:

| Link | Type | Ground truth | Expected GridPulse labelling |
|---|---|---|---|
| Transformer delivery → transformer installation | `PRECEDES` | Stated (schedule logic) | `EXPLICIT · UNVALIDATED · SCHEDULE_DERIVED` |
| Transformer installation → HV commissioning | `PRECEDES` | **Inferable, not stated.** Commissioning plan: "HV commissioning shall commence once all HV equipment is installed"; equipment list classes the main transformer as HV equipment. | `INFERRED · UNVALIDATED · AI_INFERRED` — **must not be seeded** |
| HV commissioning → grid compliance testing | `PRECEDES` | Stated (grid test programme) | `EXPLICIT · UNVALIDATED · DOCUMENT_DERIVED/AI_EXTRACTED` |
| Grid compliance testing → ENERGIZATION CHECKPOINT | `CONTRIBUTES_TO` | Stated (grid-connection agreement) | `EXPLICIT · UNVALIDATED · DOCUMENT_DERIVED/AI_EXTRACTED` |

#### 16.A.2 New information (as the OE receives it)

Reporting period N delivers:

- **EPC progress report, period N:** *"Main transformer: the supplier has advised a revised delivery
  date of 2 February."*
- **EPC schedule update, period N:** transformer delivery still **12 January**; installation
  **15 January**.
- Supporting: supplier information (letter copied to the owner, where available) and milestone
  information from the commissioning plan.

#### 16.A.3 Expected behaviour

1. **Ingestion** — report, schedule update and supporting documents ingested as DocumentVersions.
2. **Extraction** — observed claims: report states 2 Feb; schedule update states 12 Jan (delivery)
   and 15 Jan (installation); "main transformer" resolved to TX-01 (alias recorded).
3. **Change detection** — CHANGE finding: delivery information 12 Jan (period N-1) → 2 Feb (period N
   report); potential Event `DELIVERY_DATE_CHANGE`.
4. **Conflict detection** — CONFLICT finding: progress report (2 Feb) and schedule update (12 Jan)
   disagree for the same period. GridPulse does not choose between them.
5. **Evidence linking** — quoted sentence and schedule fields verified; Evidence: `HIGH` for both.
6. **Pre-review preview** — possibly affected: transformer installation milestone; HV commissioning
   via the inferred link.
7. Findings `DETECTED` → `UNDER_REVIEW`, routed to Project Controls (priority: consequential change,
   source conflict).
8. **Review** — the reviewer confirms, rejects, edits or requests investigation; the validated
   interpretation of the conflict is recorded by the human.
9. **Validated Project Intelligence** — only what the reviewer confirmed; the schedule update remains
   a visible **source divergence** (§2.4).
10. **Impact investigation** — traversal and Impacts.

#### 16.A.4 Expected discovery

| Category | Output |
|---|---|
| CHANGE | Transformer delivery information changed: 12 Jan → 2 Feb. *(L1, evidence: progress report period N vs period N-1)* |
| CONFLICT | Progress report (2 Feb) and schedule update (12 Jan) disagree. *(L1, both evidenced)* |
| FACT (calculation) | Original plan: delivery 12 Jan is 3 calendar days before planned installation 15 Jan. |
| FACT (calculation) | 2 February is **18 calendar days after** the planned 15 January installation date. |
| FACT (calculation) | Reported delivery is 21 calendar days later than the scheduled delivery date. |
| DEPENDENCY | Transformer delivery → transformer installation. *(L2 · EXPLICIT · UNVALIDATED · SCHEDULE_DERIVED)* |
| SECONDARY DEPENDENCY | Transformer installation → HV commissioning. *(L2 · INFERRED · UNVALIDATED · AI_INFERRED)* |
| POTENTIAL IMPACT | Transformer installation milestone may require investigation; downstream: HV commissioning (10 Feb), ENERGIZATION CHECKPOINT. |
| VALIDATION | Project-control review required. |
| UNCERTAINTY | Which source reflects the current plan; installation duration, float and resequencing options are not evidenced. |
| NON-CONCLUSION | No autonomous determination that energization is delayed. |

**Forbidden outputs:** "Energization will be delayed", "Energization will be delayed by 18/21 days",
"HV commissioning will slip", "The schedule is wrong", any statement about a party's intent, and any
presentation of the installation → HV commissioning link as established fact.

### 16.B PCS specification change

#### 16.B.1 Project data (synthetic — values are illustrative, not a real grid code)

| Document | Relevant content |
|---|---|
| PCS specification **Rev 7** | Cl. 5.3: reactive power capability ±0.95 power factor at PCS terminals across **0–100 %** rated active power. Cl. 6.1: control firmware v3.2. |
| PPC functional specification Rev 2 | "Reactive power control shall be designed to the PCS capability defined in **PCS specification Rev 7, clause 5.3**." |
| Grid connection requirements | Cl. R-12: facility shall provide ±0.95 power factor at the point of connection across the **full** active power range. Cl. R-30: the connecting party shall notify the network operator of any change to plant equipment or control systems that **may affect** compliance before compliance testing. |
| Grid compliance test plan Rev 1 | Test GC-04 "Reactive power capability" verifies R-12, executed through the PPC; references the PPC functional specification Rev 2. |
| Equipment list | PCS units, PPC, main transformer, no other reactive compensation listed. |

Dependency ground truth:

| Link | Type | Ground truth | Expected provenance/status |
|---|---|---|---|
| PPC functional spec → PCS spec (cl. 5.3) | `REFERENCES` | Stated | `EXPLICIT · UNVALIDATED · DOCUMENT_DERIVED/AI_EXTRACTED` (D-027) |
| Test GC-04 → requirement R-12 | `VERIFIES` | Stated | `EXPLICIT · UNVALIDATED · DOCUMENT_DERIVED/AI_EXTRACTED` |
| Grid compliance test plan → PPC functional spec | `REFERENCES` | Stated | `EXPLICIT · UNVALIDATED · DOCUMENT_DERIVED/AI_EXTRACTED` |
| GC-04 → GRID COMPLIANCE CHECKPOINT | `CONTRIBUTES_TO` | Stated (test plan) | `EXPLICIT · UNVALIDATED · DOCUMENT_DERIVED/AI_EXTRACTED` |
| **PCS reactive capability (cl. 5.3) → requirement R-12** | `SPECIFIES` / contributes to | **Inferable, not stated.** No document links them; the equipment list shows PCS as the only listed reactive source, so plant reactive capability at the point of connection depends on it. | `INFERRED · UNVALIDATED · AI_INFERRED` — **must not be seeded** |

#### 16.B.2 New information (as the OE receives it)

Submittal: **PCS specification Rev 8.** Cl. 5.3 now reads "across **20–100 %** rated active power";
cl. 6.1 now states firmware v4.0.

#### 16.B.3 Expected outputs

| Category | Output |
|---|---|
| CHANGE | PCS spec cl. 5.3 capability range changed from 0–100 % to 20–100 % rated active power; cl. 6.1 firmware v3.2 → v4.0. *(L1, evidence: Rev 7 and Rev 8)* |
| STALE_EVIDENCE | PPC functional specification Rev 2 references PCS specification **Rev 7** cl. 5.3, which Rev 8 supersedes. *(L1)* |
| FACT (comparison) | The Rev 8 stated range (20–100 %, at PCS terminals) does not cover the 0–20 % portion of the range stated in R-12 (full range, at point of connection). The two are stated at different measurement points. *(L1, calculated)* |
| FACT | R-12 and R-30 are the grid requirements whose text concerns reactive capability and equipment/control changes. *(L1)* |
| DEPENDENCY | PPC functional spec references PCS spec cl. 5.3; grid compliance test plan references the PPC functional spec. *(L2 · EXPLICIT · UNVALIDATED)* |
| INFERRED DEPENDENCY | PCS reactive capability appears to contribute to plant capability under R-12. *(L2 · INFERRED · UNVALIDATED · AI_INFERRED, evidence: equipment list + R-12 + cl. 5.3)* |
| POTENTIAL EXPOSURE | GRID COMPLIANCE CHECKPOINT (test GC-04) and ENGINEERING CHECKPOINT (PPC design basis) may require review. Potential impact identified; expert validation required. |
| VALIDATION | Electrical engineering / grid compliance review required. |
| UNRESOLVED | Does other plant equipment provide reactive support at low active power? Does the firmware change affect submitted models or PPC tuning? Is R-30 notification triggered? |

**Forbidden outputs:** "The plant will fail grid compliance testing", "PCS Rev 8 is non-compliant",
"The PPC must be redesigned", "The network operator must be notified", "The protection study must be
redone", "Grid models must be resubmitted", and any presentation of the PCS → R-12 link as
established fact. Quoting R-30's text as an observed fact is allowed; determining that R-30 is
*triggered* is not.

This scenario is the clearest demonstration of **discovery vs determination**: GridPulse discovers a
revision change, a stale reference, a range gap between stated values and the relevant requirements —
and leaves every determination to engineers.

---

## 17. Security architecture (requirements only — not implemented)

Prototype and benchmark use **synthetic and public data only**. Before any real customer data:

| Area | Requirement to be designed |
|---|---|
| Authentication | Verified identity for every user; replaces configured reviewer identities |
| Authorization | Role-based rights over review actions, manual entry and data access; per-project scope |
| Tenant isolation | Strict separation of customer projects and their data, including AI processing |
| Encryption | In transit and at rest, including stored document content and derived intelligence |
| Audit logging | Tamper-evident log of access and every state-changing action (extends §7 audit) |
| Data retention | Configurable retention for documents, derived intelligence and audit |
| Deletion | Verifiable deletion of customer data, including derived data and AI-provider copies |
| Backups | Encrypted, tested, subject to retention/deletion rules |
| Data residency | Ability to keep data in a required jurisdiction |
| AI-provider data handling | No training on customer data; retention/processing terms; provider selection constraints |
| Document access controls | Respect source-system access restrictions; users see only evidence they may see |
| Secrets management | Credentials for future integrations held and rotated securely |

The architecture already makes reviewer identity and every action explicit (§7.6), so authentication
and authorization can be added without changing the intelligence model.

---

## 18. Explicit non-goals

Phase 1 does **not** expand GridPulse into: project-management software · an Aconex replacement ·
a Primavera replacement · a scheduling engine · BIM · CAD · SCADA · EMS · trading · ERP · project
accounting · IoT · automatic engineering approval · automatic grid certification · portfolio
management · an enterprise workflow platform · a general-purpose chatbot · a system of record.

Watch-points in this architecture where drift could start: Activity (must not become tasks), Gate
(must not become stage-gate approvals), Investigation/Finding (must not become ticketing), Milestone
(must not become schedule calculation).

---

## 19. Architectural quality test

> *If I remove the dashboard, chatbot and UI, does the underlying intelligence model still make sense?*

**Yes.** Without any UI:

- Sources produce DocumentVersions; the pipeline produces Claims with verified Evidence.
- Change detection produces Changes and potential Events as Findings.
- Reviews (which are data records with explicit reviewer identity) move Findings to terminal states.
- Validated Project Intelligence is a well-defined set with a single audited change path.
- The graph holds typed, status- and provenance-labelled dependencies.
- Impact analysis is a deterministic traversal plus labelled explanations, producing Impacts with a
  fixed contract.
- The benchmark exercises and scores all of this through the intake path and the model alone.

Surfaces (Review Queue, Changes, Impact, Gates, Ask GridPulse) are views and inputs over
**Evidence + Changes + Dependencies + Impact + Validated Project Intelligence**. Ask GridPulse is
itself modelled as an Investigation, not as a separate system.

---

## 20. Readiness for Phase 2

**Phase 1:** ARCHITECTURE REVIEWED — VALIDATION REQUIRED BEFORE IMPLEMENTATION.
**Phase 2:** BLOCKED — VALIDATION GATE NOT YET PASSED.

The five blocking decisions (D-026, D-027, D-032, D-033, D-037) are resolved. Phase 2 starts only when
the validation gate in `VALIDATION_PLAN.md` passes on all three dimensions — efficiency, investigation
quality, and the determination boundary — and the founder approves. Validation findings are folded back
into this document as founder-approved amendments (D-046). Technology selection is a Phase 2 decision.
