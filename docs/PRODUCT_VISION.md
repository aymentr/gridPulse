# Product Vision

> **North star:** GridPulse continuously turns fragmented project information and real-world project
> events into an evidence-backed understanding of what changed, what may be affected, and what requires
> human attention.

## 1. Product category

**GridPulse is an AI project-intelligence layer for complex infrastructure projects.**

**GridPulse is not another project-management system.**

Project-management systems help teams manage known tasks, schedules, documents and workflows.
GridPulse focuses on a different problem: understanding how fragmented project information and
real-world changes propagate across a complex infrastructure project. Its core capability is
**evidence-backed change and dependency intelligence.**

| | Project-management / record systems | GridPulse |
|---|---|---|
| Primary job | Manage tasks, schedules, documents, workflows | Understand what changed, what it may affect, and why |
| Relationship to data | System of record | Reads across systems of record (read-only in MVP) |
| Authority | Authoritative / contractual record | Validated intelligence state — **not** the source of truth (D-021) |
| Output | Plans, records, approvals | Evidence-backed investigations routed to human experts |

- **Initial domain:** BESS and grid-connected energy infrastructure.
- **Possible later domains:** data centers, AI data centers, other large electrical infrastructure,
  other complex capital projects.

## 2. Above and alongside existing systems

Project teams already use Aconex, Primavera P6 / Primavera Cloud, Microsoft Project, SharePoint,
Procore, engineering systems, commissioning systems, spreadsheets and email. **These remain systems of
record where appropriate.** For example:

- Aconex may remain the document / contractual record.
- Primavera may remain the scheduling system.
- Engineering systems may remain authoritative for engineering data.

GridPulse's purpose is to understand the information **across** these systems and continuously maintain
an evidence-backed representation of what that information collectively implies about the project's
current state. GridPulse does not modify these systems during the MVP (D-002).

GridPulse may display project information, milestones and dependencies because they are necessary for
its intelligence function. **They are not the product's category.**

## 3. The problem

Complex infrastructure projects are not hard because information is missing. The information exists
everywhere: specifications, drawings, contracts, purchase orders, supplier documents, schedules, RFIs,
change orders, emails, meeting minutes, engineering studies, grid requirements, permits, commissioning
plans, test reports, site reports, procurement and delivery information, construction progress and
approval records.

**The hard problem is understanding the relationships between these pieces of information** — and
how a change in one propagates to the others.

Example: a supplier moves a transformer delivery date. That may ripple through:

```
Transformer delivery → installation → cable termination → protection testing
  → commissioning → grid compliance testing → energization
```

…but the evidence for each link is scattered across a supplier email, a purchase order, an engineering
document, a construction schedule, a commissioning plan and a grid-connection requirement. Today a
technical professional reconstructs this by hand. GridPulse is designed to reduce that work.

## 4. The central question

> **What changed, what does it affect, what evidence supports that assessment, and what needs attention now?**

This matters more than letting users chat with documents. GridPulse understands the project as a
**connected system** and keeps that understanding current as the real project changes.

## 5. What GridPulse is not

GridPulse is **not**:

- project-management software, task-management software or scheduling software
- a Gantt-chart replacement
- a replacement for Primavera or Aconex
- generic document-management software
- a generic AI chatbot or "chat with your PDFs" product
- an ERP, SCADA, EMS or BESS control system
- an engineering-design, CAD or BIM tool
- a grid-certification authority
- the contractual or authoritative source of truth for a project
- an autonomous engineering-approval system or autonomous project manager

**Guardrail:** a feature belongs in GridPulse only if it strengthens the core loop below. Requests for
generic PM features are a known risk (Risk 8), not a roadmap.

## 6. The core loop

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

Every feature must reinforce this loop. `PRODUCT_WORKFLOW.md` describes each stage.

## 7. Role of AI

**AI performs the investigation. Experts make the decisions.**

AI may: read documents, extract structured information, identify entities and requirements, compare
versions, detect changes, find contradictions, identify candidate dependencies, trace dependency chains,
perform deterministic calculations and evidence-backed comparisons, identify potentially affected
milestones, identify missing evidence, identify relevant reviewers, summarize investigations and
generate reports.

AI must not **silently**: certify compliance, approve engineering, declare a project delayed, approve
changes, make safety-critical decisions, or replace professional engineering judgment.

GridPulse distinguishes three levels of information (D-005):

| Level | | May GridPulse state it? |
|---|---|---|
| 1 — Fact | Directly supported information, incl. deterministic calculations on evidenced values | Yes, with evidence |
| 2 — Dependency / Inference | Evidence-backed relationship or analytical inference | Yes, labelled as such |
| 3 — Engineering / Project Conclusion | Consequential technical or project decision | **No — human decision** |

## 8. First user

**Initial MVP user: Owner's Engineer / technical project-control professional working on large BESS
projects** (D-013).

The first version is optimized for this user's workflow. It is **not** designed simultaneously for
developers, EPCs, grid operators, other consultants, data-center operators, commissioning companies or
investors; these may become later segments.

**The first question GridPulse must answer:** *Can GridPulse materially reduce the investigation
workload of a technical professional when project information changes?*

## 9. Initial wedge and long-term scope

**Initial wedge:** *AI-powered change, evidence and dependency intelligence for grid-connected
infrastructure projects.*

**Long-term lifecycle coverage (not to be built now):**

```
Project intake → Data room → Requirements → Grid maturity → Grid application → Grid offer
  → Contracts → Engineering → Procurement → Construction → Commissioning → Grid compliance
  → Energization → COD
```

The intelligence architecture should be capable of eventually supporting these stages.

**Long-term graph goal:** AI reconstructs and maintains the project intelligence graph from the
project's existing information, rather than requiring humans to model everything manually (D-003).

## 10. Value hypothesis

The goal is not faster document search. It is to **reduce the amount of expert investigation required
after project information changes.**

| | Today (hypothesis) | GridPulse target |
|---|---|---|
| Investigation of a change | ~4 hours of manual investigation | ~15 min AI investigation + 30–60 min expert validation |

> ⚠️ These are **product targets, not established industry averages.** They must be validated
> experimentally.

**Critical metric:** *investigation compression while maintaining acceptable evidence precision and recall.*

"Review required" alone is not value. An investigation must deliver evidence, affected entities, the
dependency chain, deterministic calculations, relevant milestones, stated uncertainty, suggested
reviewers and unresolved questions (see `PRODUCT_WORKFLOW.md` §3).

## 11. Conditions for GridPulse to be useful

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

## 12. Key risks

| # | Risk | Why it matters |
|---|---|---|
| 1 | **Graph quality** | The dependency graph may be harder to construct reliably than event detection. Impact analysis is only as good as the graph. |
| 2 | **Review overload** | If everything requires human attention, GridPulse becomes another work queue instead of reducing work. |
| 3 | **Weak output** | "Review required" alone is not enough. Value requires a real investigation: evidence, affected entities, dependency chain, deterministic calculations, relevant milestones, uncertainty, suggested reviewers, unresolved questions. |
| 4 | **False engineering conclusions** | The product must never make unsupported technical conclusions appear authoritative — including through wording, layout or implication. |
| 5 | **Data access** | The buyer (e.g. an Owner's Engineer) may not control all project systems; schedules and records are often owned by EPCs or developers. |
| 6 | **Confidentiality** | Infrastructure projects contain commercially and sometimes security-sensitive information. Real data requires enterprise controls (D-015). |
| 7 | **Ground truth** | Reliable benchmark data is scarce; precision/recall and time-saving claims need it. |
| 8 | **Scope creep** | Customers may request generic project-management features that pull GridPulse out of its category. |
| 9 | **Liability** | Incorrect or incomplete impact analysis could have commercial consequences, even with human review. D-021 (not the source of truth) is part of the mitigation. |
