# GridPulse

**GridPulse is an AI project-intelligence platform for complex infrastructure projects.**
It continuously turns fragmented project information and real-world project events into an
evidence-backed understanding of **what changed, what may be affected, and what requires human attention.**

The first target domain is **Battery Energy Storage Systems (BESS)** and other **grid-connected energy
infrastructure**. Possible later domains include data centers, AI data centers, other large electrical
infrastructure and other complex capital projects.

## What GridPulse is

GridPulse is an **intelligence layer that sits above the systems project teams already use**
(Aconex, Primavera P6 / Primavera Cloud, Microsoft Project, SharePoint, Procore, document-management,
engineering and commissioning systems, spreadsheets, email). It uses information from those systems;
it does not replace them.

The question it exists to answer:

> **What changed, what does it affect, what evidence supports that assessment, and what needs attention now?**

## What GridPulse is not

Not a project-management system, document-management system, Gantt replacement, ERP, SCADA, EMS,
BESS control system, CAD/BIM/engineering-design tool, grid-certification authority, generic chatbot,
"chat with your PDFs" product, autonomous engineering approver, or autonomous project manager.

## Core principle

> **AI performs the investigation. Experts make the decisions.**

The core product loop:

```
Detect → Evidence → Review → Understand → Impact → Act
```

Everything built should reinforce this loop.

## Project status

**Phase 0 — product specification.** No application code, technology stack, database schema,
AI agents, UI or integrations exist yet, by design. The documents below define the product before
implementation begins. Open questions awaiting founder decisions are tracked in
[`docs/DECISIONS.md`](docs/DECISIONS.md).

## Documentation

| Document | Purpose |
|---|---|
| [`docs/PRODUCT_VISION.md`](docs/PRODUCT_VISION.md) | Why GridPulse exists, the problem, positioning, customers, value hypothesis |
| [`docs/PRODUCT_WORKFLOW.md`](docs/PRODUCT_WORKFLOW.md) | The end-to-end loop from incoming information to human decision, incl. the first killer scenario |
| [`docs/CORE_CONCEPTS.md`](docs/CORE_CONCEPTS.md) | Vocabulary: Project Event, Evidence, Fact / Inference / Conclusion, Trusted Project State, Project Intelligence Graph, Gates… |
| [`docs/ENGINEERING_PRINCIPLES.md`](docs/ENGINEERING_PRINCIPLES.md) | Non-negotiable rules any implementation must respect |
| [`docs/MVP_BOUNDARIES.md`](docs/MVP_BOUNDARIES.md) | What the first build includes, excludes, and how it will be judged |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | Open product/architecture questions with options and recommendations |
