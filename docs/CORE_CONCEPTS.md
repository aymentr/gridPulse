# Core Concepts

The shared vocabulary for GridPulse. Definitions are **conceptual**; exact technical schemas will be
designed later. Where a definition required interpretation beyond the product vision, it is marked
*(interpretation — see DECISIONS.md)*.

---

## Project

A single complex infrastructure undertaking (initially a BESS or other grid-connected asset — e.g. a
100 MW / 400 MWh BESS). GridPulse builds and maintains an evidence-backed representation of each project.

## Source System

An external system where project information lives and remains owned: Aconex, Primavera P6 /
Primavera Cloud, Microsoft Project, SharePoint, Procore, document-management systems, engineering and
commissioning systems, spreadsheets, email. GridPulse **reads from** these; it does not replace them.

## Source Record

A specific item of information that entered GridPulse: a document, drawing, email, schedule, RFI,
change order, meeting minutes, test report, etc. Source records have **versions**.

## Evidence

The traceable link between a claim and the exact place in a source that supports it:

```
CLAIM → SOURCE → DOCUMENT / EMAIL / SCHEDULE / OTHER RECORD → VERSION → PAGE / SECTION / CHUNK / LOCATION
```

Every important AI-generated claim must have evidence. A user must always be able to ask
"why does GridPulse believe this?" and inspect the answer.

## Three Levels of Information

| Level | Name | Definition | Example | Who may assert it |
|---|---|---|---|---|
| **1** | **Fact** | Directly supported by evidence | "Supplier states transformer delivery moved from January 12 to February 2." | AI may extract; human review applies to consequential facts |
| **2** | **Dependency / Inference** | A relationship inferred from project information; must have supporting evidence | "Transformer installation appears to be a predecessor of HV commissioning." | AI may propose, clearly labelled as inference |
| **3** | **Engineering / Project Conclusion** | A consequential decision or technical conclusion | "Energization will be delayed by 21 days." | **Humans only.** GridPulse gathers evidence and routes to the right expert |

Every claim GridPulse shows should carry its level. Presenting Level 2 as Level 1, or producing
Level 3 autonomously, is a defect.

## Project Event

Something that **happened or may have changed** in the real project.

Initial event types:

`SHIPMENT_DELAY` · `DELIVERY_DATE_CHANGE` · `SPECIFICATION_CHANGE` · `TEST_FAILURE` ·
`SCHEDULE_CHANGE` · `RFI` · `CHANGE_ORDER` · `PERMIT_CHANGE` · `GRID_OPERATOR_DECISION` ·
`CONSTRUCTION_PROGRESS` · `EQUIPMENT_FAILURE` · `OTHER`

Conceptual attributes:

| Attribute | Meaning |
|---|---|
| Event type | One of the types above |
| Affected entity | The project entity that changed (e.g. main transformer) |
| Old state | Value before the change |
| New state | Value after the change |
| Source | Where the information came from |
| Evidence | Pointer(s) to the exact supporting location |
| Detected time | When GridPulse detected it |
| Effective time | When the change takes effect in the real world |
| Detection method | How it was detected (e.g. manual entry, AI extraction from an email) |
| Confidence | How confident the detection is |
| Review status | e.g. NEEDS REVIEW, confirmed, rejected |
| Reviewer | Who reviewed it |
| Review decision | What the reviewer decided |

## Potential Event

A Project Event proposed by AI (or otherwise not yet reviewed) with status **NEEDS REVIEW**.
It does **not** change the trusted project state.

## Review / Review Queue

The human validation step. Reviewers confirm, correct or reject Potential Events. The Review Queue
lists AI-detected events awaiting validation.

## Change

A **confirmed** change to the trusted project state, resulting from a reviewed Project Event.
*(interpretation — the vision lists "Events" and "Changes" as separate views; the precise
relationship is recorded in DECISIONS.md.)*

## Trusted Project State

GridPulse's current, human-validated understanding of the project. It changes only as a result of
reviewed events and human corrections. It is what impact analysis runs against.

## Project Entity

Anything the project is made of or governed by. Examples from the vision: requirements, documents,
equipment, suppliers, contracts, parties, engineering information, tasks, milestones, dependencies,
risks, issues, events, changes, tests, approvals, gates.

BESS examples: battery containers, PCS, transformers, MV equipment, HV equipment, protection systems,
PPC, EMS, SCADA, metering, communications, fire protection, grid connection, EPC, suppliers,
construction activities, commissioning tests, grid compliance tests, energization, COD.

## Project Intelligence Graph

The central technical/product concept: a connected representation of project entities and their
relationships, each backed by evidence. It lets GridPulse investigate the consequences of changes.

```
Transformer → Delivery → Installation → HV Commissioning → Grid Compliance Testing → Energization
```

## Dependency

A relationship where one project element depends on another (e.g. installation depends on delivery).
Dependencies may come from explicit sources (e.g. schedule logic) or be inferred (Level 2). Either way
they carry evidence.

## Impact / Impact Analysis

Tracing dependencies from a confirmed change to identify what **may** be affected: tasks, milestones,
gates, risks, responsible people. Impact output is **potential impact requiring review** — never a
Level 3 conclusion.

## Requirement

A project or grid requirement (technical, contractual, grid-code, commissioning, etc.) with
supporting evidence. GridPulse can identify requirements and flag where evidence of fulfilment is missing.

## Gate

An important project checkpoint. Examples: grid connection, engineering completion, procurement
readiness, construction completion, commissioning, grid compliance, energization, COD.

## Reviewer / Responsible Person

The human expert to whom GridPulse routes a review or potential impact. GridPulse may **identify**
relevant reviewers; humans make the decisions.

## Investigation

The work of determining what changed, what it affects and what evidence supports it. GridPulse's
purpose is to compress the time humans spend on investigation while preserving evidence precision
and recall.

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
| RFI | Request for Information |
| COD | Commercial Operation Date |
| OE | Owner's Engineer |
