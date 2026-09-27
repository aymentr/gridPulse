# Product Workflow

How information moves through GridPulse, from the real world to human attention and action.
This is a **conceptual** workflow; no technical design, schema or UI is implied.

## 1. The canonical loop

```
REAL WORLD
    ↓
INFORMATION ENTERS ────────── any channel, one universal intake path
    ↓
DETECTION ─────────────────── changes detected; potential events proposed
    ↓
EVIDENCE ──────────────────── every claim linked to source → version → location
    ↓
HUMAN REVIEW ──────────────── Review Queue: confirm / reject / edit / request more investigation
    ↓
TRUSTED PROJECT EVENT ─────── confirmed event updates the validated intelligence state
    ↓
PROJECT INTELLIGENCE GRAPH ── entities and dependencies (CONFIRMED / INFERRED / REJECTED)
    ↓
IMPACT ANALYSIS ───────────── traverse dependencies; potential impacts; facts vs inferences
    ↓
ATTENTION / ACTION ────────── routed to relevant humans, who make the decisions
```

## 2. Stages

### 2.1 Information enters

Information may enter through manual entry, document upload, email, schedule update, integration or
future external systems. There is **one universal event/change intake mechanism**; channels are only
different ways for raw information to arrive. GridPulse is **read-only** against external systems in
the MVP (D-002).

### 2.2 Detection

Detection covers two related concepts (D-009):

- A **Change** is a difference between two states or versions — e.g. PCS specification Rev 7 → Rev 8,
  or transformer delivery Jan 12 → Feb 2.
- An **Event** is something that happened, or is reported to have happened, in the real project — e.g.
  *"Supplier informed the project that transformer delivery has moved to February 2."*

```
SOURCE → CHANGE DETECTED → POTENTIAL EVENT → HUMAN REVIEW → CONFIRMED PROJECT EVENT
```

A detected Change may generate a Potential Event. **Every AI-detected Project Event starts as
`NEEDS_REVIEW`** (D-001).

**Exception — manual entry by an authorized user.** An authorized user entering a known real-world
event may create it directly as `CONFIRMED`:

| Origin | Example | Initial status |
|---|---|---|
| Manual entry by authorized user | "Transformer delivery has been confirmed by the project manager as moving from Jan 12 to Feb 2." | `CONFIRMED` |
| AI detection | "Supplier email appears to change transformer delivery from Jan 12 to Feb 2." | `NEEDS_REVIEW` |

AI-detected information is **never** silently promoted into the trusted project state.

### 2.3 Evidence

Every extracted fact, detected change, potential event and inferred dependency carries evidence:
source → record → version → page/section/chunk/location. Manually entered events record who entered
them and on what basis.

### 2.4 Human review — the Review Queue

The Review Queue is **part of the trust architecture**, not an administrative feature. It is the
boundary between AI output and the trusted project state.

For each item the reviewer should be able to see:

- what GridPulse detected
- why it detected it
- what source supports it
- what changed (old → new)
- which entity is affected
- what confidence exists
- which dependencies may be affected
- what remains uncertain

The reviewer should eventually be able to:

- **confirm**
- **reject**
- **edit / correct**
- **request more investigation**

The exact UI is deferred. (Which actions are in the MVP, and how "request more investigation" is
represented, are open — D-010, D-022.)

### 2.5 Trusted project event

A confirmed Project Event updates GridPulse's **trusted project state** — its validated intelligence
state. This state is derived from authoritative sources plus human review; it is **not** the
authoritative or contractual record (D-021).

### 2.6 Project intelligence graph

The graph holds project entities and their dependencies. Dependencies carry a status (D-004):

| Status | Meaning | Example |
|---|---|---|
| `CONFIRMED` | Explicit in a source (e.g. schedule logic) or confirmed by a human | Schedule: "Transformer Installation depends on Transformer Delivery" |
| `INFERRED` | Proposed by AI from project information, with evidence | AI infers from several documents that installation affects HV commissioning |
| `REJECTED` | A human rejected the relationship | Reviewer rejects the inferred link |

The initial graph is **reconstructed from available project information** (documents, imported
schedule, manually entered facts), with manual seeding only where needed to establish ground truth for
the controlled benchmark (D-003). GridPulse consumes explicit schedule relationships; it is **not** a
scheduling engine.

### 2.7 Impact analysis

GridPulse traverses dependencies from the affected entity and identifies **potential** downstream
impact. It may use `INFERRED` dependencies but must label them as inferred; it never uses `REJECTED`
ones and never presents an inference as established fact.

GridPulse may perform **deterministic calculations and evidence-backed comparisons** (Level 1). It must
**not** produce engineering/project conclusions (Level 3) (D-005).

### 2.8 Attention / action

GridPulse identifies relevant reviewers and routes the investigation to them. Humans decide whether the
project is delayed, whether engineering must change, whether compliance is affected, and what to do.

## 3. What an impact investigation must contain

"Review required" alone is not enough (Risk 3). A GridPulse investigation should present:

| Element | Example (transformer scenario) |
|---|---|
| Evidence | Link to the exact sentence in the supplier communication |
| Affected entities | Main transformer |
| Dependency chain | Delivery → installation → HV commissioning → grid compliance testing → energization, each link with status and evidence |
| Deterministic calculations | Delivery moved 21 calendar days; new delivery is 18 calendar days after planned installation start |
| Relevant milestones / gates | HV commissioning, grid compliance testing, energization |
| Uncertainty | Which links are INFERRED; what information is missing (e.g. float, resequencing options) |
| Suggested reviewers | Relevant roles for schedule and engineering review |
| Unresolved questions | Questions a human must answer before any conclusion |

Each item is labelled Level 1 (fact) or Level 2 (dependency / inference).

## 4. The first product demonstration — transformer delivery change

### Initial project state

| Item | Date |
|---|---|
| Transformer delivery | January 12 |
| Transformer installation | January 15 |
| HV commissioning | February 10 |
| Grid compliance testing | February 20 |
| Energization | March 1 |

### New information

A supplier communication arrives: *"Transformer delivery is now expected February 2."*

### What GridPulse does

1. **Detects the change** in the supplier communication.
2. **Extracts old and new dates** — January 12 → February 2.
3. **Links the evidence** — the exact location in the communication.
4. **Creates a potential event** — `DELIVERY_DATE_CHANGE`, affected entity: main transformer.
5. **Marks it `NEEDS_REVIEW`.**
6. **Human confirms it** in the Review Queue.
7. **Updates the trusted project state** — transformer delivery = February 2, with evidence and reviewer.
8. **Traverses project dependencies** — delivery → installation → HV commissioning → grid compliance
   testing → energization.
9. **Identifies potential downstream impact.**
10. **Identifies relevant reviewers.**
11. **Clearly separates facts, inferences and conclusions.**

### Example output (illustrative wording)

| Level | Statement |
|---|---|
| 1 — Fact | Supplier states transformer delivery is now expected February 2 (previously January 12). *[evidence]* |
| 1 — Fact (calculation) | The new delivery date is 21 calendar days later than the previous planned date. |
| 1 — Fact (comparison) | The new delivery date (Feb 2) is after the planned transformer installation date (Jan 15). *[schedule evidence]* |
| 2 — Dependency | Transformer installation depends on transformer delivery. *[CONFIRMED — schedule logic]* |
| 2 — Inference | Transformer installation appears to precede HV commissioning. *[INFERRED — evidence: …]* |
| Attention | Potential downstream impact on HV commissioning, grid compliance testing and energization. Schedule and engineering review required. Suggested reviewers: … |

### What GridPulse must NOT say

> ✗ *"Energization will be delayed by 21 days."*

That is a Level 3 project/engineering conclusion. Float, resequencing, mitigation and contractual
context are for humans to assess.

## 5. What the user eventually experiences

These areas describe the eventual experience, **not** MVP scope, and exist to serve the core loop —
not as generic PM features.

| Area | Purpose |
|---|---|
| Project Overview | Current validated intelligence state |
| Data Room | Project information and documents GridPulse has read |
| Events | Things that happened or are reported to have happened |
| Review Queue | Items requiring human validation (trust boundary) |
| Changes | Detected differences between states or versions |
| Evidence | Why GridPulse believes something |
| Requirements | Project/grid requirements and supporting evidence |
| Dependencies | Relationships between project elements, with status |
| Impact | What a confirmed event may affect |
| Gates | Grid connection, engineering completion, procurement readiness, construction completion, commissioning, grid compliance, energization, COD |
| Ask GridPulse | Evidence-backed natural-language investigation |
