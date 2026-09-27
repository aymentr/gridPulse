# Product Vision

> **North star:** GridPulse continuously turns fragmented project information and real-world project
> events into an evidence-backed understanding of what changed, what may be affected, and what requires
> human attention.

## 1. What GridPulse is

GridPulse is an **AI project-intelligence platform** for complex infrastructure projects.

- **Initial domain:** Battery Energy Storage Systems (BESS) and grid-connected energy infrastructure.
- **Possible later domains:** data centers, AI data centers, other large electrical infrastructure,
  other complex capital projects.

GridPulse is an **intelligence layer above existing systems**, not a system of record. Project teams
already use tools such as Aconex, Primavera P6 / Primavera Cloud, Microsoft Project, SharePoint,
Procore, document-management systems, engineering systems, commissioning systems, spreadsheets and
email. GridPulse **uses information from these systems rather than replacing them.**

## 2. The problem

Complex infrastructure projects are not hard because information is missing. The information exists
everywhere: specifications, drawings, contracts, purchase orders, supplier documents, schedules, RFIs,
change orders, emails, meeting minutes, engineering studies, grid requirements, permits, commissioning
plans, test reports, site reports, procurement and delivery information, construction progress and
approval records.

**The hard problem is understanding the relationships between these pieces of information.**

Example: a supplier moves a transformer delivery date. That single event may ripple through:

```
Transformer delivery → installation → cable termination → protection testing
  → commissioning → grid compliance testing → energization
```

…but the evidence for each link is scattered across a supplier email, a purchase order, an engineering
document, a construction schedule, a commissioning plan and a grid-connection requirement. Today a
human team reconstructs this manually. GridPulse is designed to reduce that work.

## 3. The central question

> **What changed, what does it affect, what evidence supports that assessment, and what needs attention now?**

This matters more than letting users chat with documents. GridPulse must understand the project as a
**connected system**, and it must keep that understanding current as the real project changes.

## 4. What GridPulse is not

GridPulse is **not**:

- a replacement for Aconex or Primavera
- generic project-management or document-management software
- a generic AI chatbot or "chat with your PDFs" product
- a Gantt-chart replacement
- an ERP, SCADA, EMS or BESS control system
- an engineering-design, CAD or BIM tool
- a grid-certification authority
- an autonomous engineering-approval system or autonomous project manager

**Guardrail:** do not let GridPulse drift into a collection of generic project-management features.
A feature belongs in GridPulse only if it strengthens the core loop (see below).

## 5. The core loop

```
Detect → Evidence → Review → Understand → Impact → Act
```

| Step | Meaning |
|---|---|
| **Detect** | Notice that something in the real project may have changed |
| **Evidence** | Tie every claim to the exact source that supports it |
| **Review** | A human confirms, corrects or rejects consequential changes |
| **Understand** | Confirmed changes update the trusted project state and intelligence graph |
| **Impact** | Trace dependencies to identify what may be affected |
| **Act** | Route the issue to the right humans, who make the decision |

## 6. Role of AI

**AI performs the investigation. Experts make the decisions.**

AI may: read documents, extract structured information, identify entities and requirements, compare
versions, detect changes, find contradictions, identify candidate dependencies, trace dependency chains,
identify potentially affected milestones, identify missing evidence, identify relevant reviewers,
summarize investigations and generate reports.

AI must not **silently**: certify compliance, approve engineering, declare a project delayed, approve
changes, make safety-critical decisions, or replace professional engineering judgment.

## 7. Target customers

Initial users are expected to be professional organizations, not consumers:

- BESS developers
- Owner's Engineers
- Project-control consultancies
- Grid consultants
- Technical due-diligence firms
- EPCs
- Commissioning consultants
- Infrastructure project-management firms

The product should be designed around the workflows of these users. (Which one to design the MVP
around first is an open decision — see `DECISIONS.md`.)

## 8. Initial wedge and long-term scope

**Initial wedge:** *AI-powered change, evidence and dependency intelligence for grid-connected
infrastructure projects.*

**Long-term lifecycle coverage (not to be built immediately):**

```
Project intake → Data room → Requirements → Grid maturity → Grid application → Grid offer
  → Contracts → Engineering → Procurement → Construction → Commissioning → Grid compliance
  → Energization → COD
```

The underlying intelligence architecture should be capable of eventually supporting these stages.

## 9. Value hypothesis

The goal is not merely faster document search. It is to **reduce the amount of expert investigation
required after project information changes.**

| | Today (hypothesis) | GridPulse target |
|---|---|---|
| Investigation of a change | ~4 hours of manual investigation | ~15 min AI investigation + 30–60 min expert validation |

> ⚠️ These numbers are **product targets, not established industry averages.** They must be validated
> experimentally.

**Critical metric:** *investigation compression while maintaining acceptable evidence precision and recall.*

## 10. Conditions for GridPulse to be useful

GridPulse only works if it:

1. Knows what information changed.
2. Knows where the information came from.
3. Knows which project entity is affected.
4. Can connect the entity to relevant dependencies.
5. Can explain its reasoning with evidence.
6. Distinguishes fact from inference.
7. Allows humans to review and correct it.
8. Makes corrections part of the trusted project state.
9. Does not invent engineering conclusions.
10. Continuously updates as the project evolves.
