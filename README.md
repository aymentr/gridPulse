# GridPulse

**GridPulse is an AI project-intelligence layer for complex infrastructure projects.**

It continuously turns fragmented project information and real-world project events into an
evidence-backed understanding of **what changed, what may be affected, and what requires human attention.**

The first target domain is **Battery Energy Storage Systems (BESS)** and other **grid-connected energy
infrastructure**. Possible later domains include data centers, AI data centers, other large electrical
infrastructure and other complex capital projects.

## GridPulse is not another project-management system

Project-management systems help teams manage known tasks, schedules, documents and workflows.

GridPulse focuses on a different problem: **understanding how fragmented project information and
real-world changes propagate across a complex infrastructure project.** Its core capability is
**evidence-backed change and dependency intelligence.**

GridPulse sits **above and alongside** the systems project teams already use — Aconex, Primavera P6 /
Primavera Cloud, Microsoft Project, SharePoint, Procore, engineering systems, commissioning systems,
spreadsheets and email. Those systems remain the systems of record. GridPulse reads from them
(read-only in the MVP), understands the information across them, and maintains its own validated,
evidence-backed representation of the project's current state.

GridPulse is **not the contractual or authoritative source of truth** for a project
(see [D-021](docs/DECISIONS.md#d-021--gridpulses-source-of-truth)).

GridPulse may *display* milestones, dependencies and project information because its intelligence
function requires them — but it is not task-management, Gantt, scheduling, document-management or
generic PM software, and it does not replace Primavera or Aconex.

## The central question

> **What changed, what does it affect, what evidence supports that assessment, and what needs attention now?**

## The core loop

```
REAL WORLD
    ↓
INFORMATION ENTERS
    ↓
DETECTION
    ↓
EVIDENCE
    ↓
HUMAN REVIEW
    ↓
TRUSTED PROJECT EVENT
    ↓
PROJECT INTELLIGENCE GRAPH
    ↓
IMPACT ANALYSIS
    ↓
ATTENTION / ACTION
```

> **AI performs the investigation. Experts make the decisions.**

## First user and first demonstration

- **First user:** an Owner's Engineer / technical project-control professional on large BESS projects.
- **First question to answer:** can GridPulse materially reduce this person's investigation workload
  when project information changes?
- **First demonstration:** a supplier moves the main transformer delivery from January 12 to
  February 2. GridPulse detects it, links the evidence, queues it for review, and — once confirmed —
  traces potential downstream impact without ever concluding that energization is delayed.

## Project status

**Phase 0 — product definition.** No application code, technology stack, database schema, AI agents,
UI or integrations exist yet, by design. Founder decisions are recorded in
[`docs/DECISIONS.md`](docs/DECISIONS.md).

## Documentation

| Document | Purpose |
|---|---|
| [`docs/PRODUCT_VISION.md`](docs/PRODUCT_VISION.md) | Category, problem, positioning, first user, value hypothesis, risks |
| [`docs/PRODUCT_WORKFLOW.md`](docs/PRODUCT_WORKFLOW.md) | The core loop stage by stage, the Review Queue, and the first demonstration |
| [`docs/CORE_CONCEPTS.md`](docs/CORE_CONCEPTS.md) | Vocabulary: Change, Event, Evidence, three levels of information, dependency status, trusted state… |
| [`docs/ENGINEERING_PRINCIPLES.md`](docs/ENGINEERING_PRINCIPLES.md) | Rules any implementation must respect |
| [`docs/MVP_BOUNDARIES.md`](docs/MVP_BOUNDARIES.md) | What the MVP includes and excludes, data policy, exit criteria |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | Resolved and open product decisions |
