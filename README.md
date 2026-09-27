# GridPulse

**GridPulse is an evidence-backed AI project-intelligence layer for complex infrastructure projects.**

It reconstructs and continuously maintains the relationships between project information, changes,
requirements, evidence, equipment, suppliers, milestones, dependencies, tests, approvals and critical
gates — and turns them into an understanding of **what changed, what may be affected, and what requires
human attention.**

> **AI performs the project investigation. Experts make the decisions.**

The first target domain is **Battery Energy Storage Systems (BESS)** and other **grid-connected energy
infrastructure**.

## GridPulse is not another project-management system

Project-management systems help teams manage known tasks, schedules, documents and workflows.

GridPulse focuses on a different problem: **understanding how fragmented project information and
real-world changes propagate across a complex infrastructure project.** Its core capability is
**evidence-backed change and dependency intelligence.**

GridPulse is **not**: an AI project manager, project-management or scheduling software, a
document-management replacement, a replacement for Primavera or Aconex, a generic chatbot, an
engineering approval system, an automatic grid-certification system, an ERP, or a system of record.

## Where GridPulse sits

```
AUTHORITATIVE PROJECT SOURCES   (Aconex, Primavera/P6, MS Project, SharePoint, Procore,
        ↓                         engineering & commissioning systems, spreadsheets, email)
    GRIDPULSE                     read-only in the MVP
        ↓
AI investigation / extraction / inference
        ↓
     HUMAN REVIEW
        ↓
VALIDATED PROJECT INTELLIGENCE
```

**Validated Project Intelligence** is GridPulse's internally validated view of project information,
derived from authoritative project sources and human review. It is **not** the contractual, legal,
engineering, scheduling or other authoritative source of truth. The systems of record stay the
systems of record.

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
VALIDATED PROJECT INTELLIGENCE
    ↓
PROJECT INTELLIGENCE GRAPH
    ↓
IMPACT ANALYSIS
    ↓
ATTENTION / ACTION
```

## Discovery, not determination

GridPulse **discovers** ("PCS specification changed from Rev 7 to Rev 8"; "the new delivery date is
18 calendar days after the planned installation date"). It does **not determine** ("the project will
miss energization"). Instead: *"Potential energization exposure identified. Engineering /
project-control validation required."*

## First user and first demonstration

- **First user:** Owner's Engineer / technical project-control professional on large BESS projects.
- **First question:** can GridPulse materially reduce this person's investigation workload when
  project information changes?
- **What the OE actually sees:** changes usually arrive through reporting-period documents — EPC
  progress reports, schedule updates, submittals and revisions, meeting minutes — not direct supplier
  emails. The killer question is *"what changed since the last reporting period, and is it consistent
  across the evidence?"*
- **Two co-primary demonstrations**, each with at least one **AI-inferred** dependency:
  1. **Transformer delivery divergence** — the EPC progress report says delivery moved to 2 February
     while the schedule update still shows 15 January. GridPulse surfaces the change *and* the
     disagreement, traces potential exposure, and never concludes that energization is delayed.
  2. **PCS specification change** — PCS spec Rev 7 → Rev 8. GridPulse finds the PPC specification
     still referencing Rev 7, connects the change to grid-compliance requirements and tests, and
     leaves every engineering determination to engineers.

## Project status

| Phase | Status |
|---|---|
| **Phase 0 — Product definition** | **LOCKED** |
| **Phase 1 — Domain & system architecture** | Draft — **frozen** pending validation |
| **Validation gate** | **Active** — interviews, real change stories, timed comparison ([`docs/VALIDATION_PLAN.md`](docs/VALIDATION_PLAN.md)) |
| Phase 2 — Implementation | Not started; blocked on the validation gate. No code, stack, schema, UI, agents or integrations exist. |

## Documentation

| Document | Purpose |
|---|---|
| [`docs/PRODUCT_VISION.md`](docs/PRODUCT_VISION.md) | Category, problem, positioning, first user, value hypothesis, risks |
| [`docs/PRODUCT_WORKFLOW.md`](docs/PRODUCT_WORKFLOW.md) | The core loop, Review Queue, Ask GridPulse, first demonstration |
| [`docs/CORE_CONCEPTS.md`](docs/CORE_CONCEPTS.md) | Product vocabulary (summary; precise definitions in Phase 1) |
| [`docs/ENGINEERING_PRINCIPLES.md`](docs/ENGINEERING_PRINCIPLES.md) | Rules any implementation must respect |
| [`docs/MVP_BOUNDARIES.md`](docs/MVP_BOUNDARIES.md) | MVP scope, data policy, exit criteria |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | Resolved and open decisions |
| [`docs/PHASE_1_ARCHITECTURE.md`](docs/PHASE_1_ARCHITECTURE.md) | Domain model, state machines, evidence, graph, change & impact models, AI boundaries, benchmark, vertical slices |
| [`docs/COUNCIL_REVIEW.md`](docs/COUNCIL_REVIEW.md) | Multi-perspective evaluation of the idea and the changes it led to |
| [`docs/VALIDATION_PLAN.md`](docs/VALIDATION_PLAN.md) | The gate before Phase 2: interviews, change stories, timed comparison, buyer hypotheses |
