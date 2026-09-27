# Product Workflow

This document describes how information moves through GridPulse, from the real world to a human
decision. It is a **conceptual** workflow; no technical design is implied.

## 1. The end-to-end flow

```
REAL WORLD
   ↓
1. Intake ──────────── Information enters GridPulse (any channel)
   ↓
2. Extraction ──────── AI extracts facts and relationships, each linked to evidence
   ↓
3. Detection ───────── AI detects possible events / changes  → Potential Event (NEEDS REVIEW)
   ↓
4. Review ──────────── Human confirms, corrects or rejects consequential changes
   ↓
5. Trusted state ───── Confirmed event updates the trusted project state
   ↓
6. Graph update ────── Project Intelligence Graph is updated
   ↓
7. Impact analysis ─── Dependencies traced; potentially affected milestones, gates, risks and
   ↓                    responsible people identified
8. Human decision ──── Humans make the final project / engineering decision
```

This maps onto the core loop **Detect → Evidence → Review → Understand → Impact → Act**:

| Loop step | Workflow stages |
|---|---|
| Detect | 1 Intake, 3 Detection |
| Evidence | 2 Extraction (evidence attached to everything downstream) |
| Review | 4 Review |
| Understand | 5 Trusted state, 6 Graph update |
| Impact | 7 Impact analysis |
| Act | 8 Human decision |

## 2. Stage details

### 2.1 Intake

Information may enter through:

1. Manual entry
2. Document upload
3. Email
4. Schedule update
5. Integration
6. Future external systems

**Principle:** there is one **universal event/change intake mechanism**, regardless of origin. Channels
differ only in how raw information arrives; after intake, everything follows the same path.
The initial product will not build every channel (see `MVP_BOUNDARIES.md`), but the workflow must not
depend on any particular channel.

### 2.2 Extraction

AI reads the incoming information and extracts facts, entities, requirements and candidate
relationships. **Every extracted item carries a pointer to its evidence** (source → record → version →
page/section/chunk/location).

### 2.3 Detection

AI compares new information to the current trusted project state and proposes **Potential Events** —
things that may have happened or changed. A Potential Event includes (conceptually): event type,
affected entity, old state, new state, source, evidence, detected time, effective time, detection
method, confidence, and review status = **NEEDS REVIEW**.

AI detection is **not** truth. A Potential Event does not alter the trusted project state.

### 2.4 Review (Review Queue)

A human reviews each consequential Potential Event and can:

- **Confirm** — the event enters the trusted project state.
- **Correct** — fix what the AI got wrong; the correction becomes part of the trusted state.
- **Reject** — the event does not enter the trusted state.

The reviewer and review decision are recorded. (What counts as "consequential", and whether
corrections are a distinct action, are open questions — see `DECISIONS.md`.)

### 2.5 Trusted project state

Only reviewed, confirmed information becomes trusted project state. Confirmed events appear as
**Changes** — confirmed changes to project state.

### 2.6 Graph update

The Project Intelligence Graph is updated to reflect the confirmed change.

### 2.7 Impact analysis

GridPulse traces dependencies from the affected entity to identify **potentially** affected tasks,
milestones, gates, risks and responsible people. Output is framed as **potential impact requiring
review**, never as an engineering or project conclusion. Every link in an impact chain is backed by
evidence and labelled by its level (fact vs. inference).

### 2.8 Human decision

GridPulse routes the issue to the appropriate human expert(s). Humans decide whether the project is
delayed, whether engineering must change, whether compliance is affected, and what to do.

## 3. The first killer scenario

This is the first meaningful demonstration of GridPulse.

### Initial state

GridPulse holds evidence and relationships representing:

| Item | Date |
|---|---|
| Transformer delivery | January 12 |
| Transformer installation | January 15 |
| HV commissioning | February 10 |
| Grid compliance testing | February 20 |
| Energization | March 1 |

### New information arrives

Supplier email: *"Transformer delivery is now expected February 2 instead of January 12."*

### GridPulse detects

```
Potential Event:  MAIN TRANSFORMER DELIVERY DATE CHANGED
Type:             SHIPMENT / DELIVERY EVENT
Affected entity:  Main transformer
Old value:        January 12
New value:        February 2
Source:           Supplier email
Evidence:         <link to the exact sentence in the email>
Confidence:       <value>
Status:           NEEDS REVIEW
```

### Human reviews

The reviewer inspects the evidence and clicks **CONFIRM**.

### GridPulse updates and investigates

1. Trusted project state now records transformer delivery = February 2 (with evidence and reviewer).
2. GridPulse traces:

```
Transformer delivery → transformer installation → HV commissioning
  → grid compliance testing → energization
```

3. GridPulse reports **potential** impacts, e.g.:

> *"Potential downstream impact detected. Transformer installation appears to precede HV
> commissioning. Schedule and engineering review required."*

### What GridPulse must NOT say

> ✗ *"Project energization is delayed by 21 days."*

That is a Level 3 engineering/project conclusion. It is unsupported: float, resequencing, mitigation
and contractual context are for humans to assess. **This distinction is fundamental.**

## 4. What the user eventually experiences

A project manager opening GridPulse should eventually be able to see:

| Area | Purpose |
|---|---|
| **Project Overview** | Current project state |
| **Data Room** | Project information and documents |
| **Events** | Things that happened or may have changed |
| **Review Queue** | AI-detected events requiring human validation |
| **Changes** | Confirmed changes to project state |
| **Evidence** | Why GridPulse believes something |
| **Requirements** | Project/grid requirements and supporting evidence |
| **Dependencies** | Relationships between project elements |
| **Impact** | What a confirmed change may affect |
| **Gates** | Grid connection, engineering completion, procurement readiness, construction completion, commissioning, grid compliance, energization, COD |
| **Ask GridPulse** | Evidence-backed natural-language investigation |

Example "Ask GridPulse" questions:

- "What is currently blocking energization?"
- "What's changed since last week?"
- "Which supplier changes have potential schedule consequences?"
- "Which commissioning requirements do we not yet have evidence for?"
- "What changed in the latest transformer specification?"

Answers must remain evidence-backed. This list describes the eventual experience, **not** the MVP
scope (see `MVP_BOUNDARIES.md`).
