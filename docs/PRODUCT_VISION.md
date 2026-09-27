# Product Vision

**Phase 0 — LOCKED** (amended by council-review decisions D-041 – D-047). Changes require an explicit founder decision recorded in `DECISIONS.md`.

> **North star:** GridPulse continuously turns fragmented project information and real-world project
> events into an evidence-backed understanding of what changed, what may be affected, and what requires
> human attention.

## 1. Product category

**GridPulse is an evidence-backed AI project-intelligence layer** that reconstructs and continuously
maintains relationships between project information, changes, requirements, evidence, equipment,
suppliers, milestones, dependencies, tests, approvals and critical gates.

**Core promise: AI performs the project investigation. Experts make the decisions.**

**GridPulse is not another project-management system.** Project-management systems help teams manage
known tasks, schedules, documents and workflows. GridPulse focuses on a different problem:
understanding how fragmented project information and real-world changes propagate across a complex
infrastructure project. Its core capability is **evidence-backed change and dependency intelligence.**

| | Project-management / record systems | GridPulse |
|---|---|---|
| Primary job | Manage tasks, schedules, documents, workflows | Understand what changed, what it may affect, and why |
| Relationship to data | System of record | Reads across systems of record (read-only in MVP) |
| Authority | Authoritative / contractual record | Validated Project Intelligence — **not** the source of truth (D-021) |
| Output | Plans, records, approvals | Evidence-backed investigations routed to human experts |

- **Initial domain:** BESS and grid-connected energy infrastructure.
- **Possible later domains:** data centers, AI data centers, other large electrical infrastructure,
  other complex capital projects.

## 2. Above and alongside existing systems

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

Aconex, Primavera P6 / Primavera Cloud, Microsoft Project, SharePoint, Procore, engineering systems,
commissioning systems, spreadsheets and email **remain the systems of record** — e.g. Aconex for the
document/contractual record, Primavera for the schedule, engineering systems for engineering data.

**Validated Project Intelligence** is GridPulse's internally validated view of project information
derived from authoritative project sources and human review. It is not the contractual, legal,
engineering, scheduling or other authoritative source of truth for the project. GridPulse never
implies that its own state replaces a system of record, and never modifies one during the MVP (D-002).

GridPulse may display project information, milestones and dependencies because its intelligence
function requires them. **They are not the product's category.**

## 3. The problem

Complex infrastructure projects are not hard because information is missing. The information exists
everywhere: specifications, drawings, contracts, purchase orders, supplier documents, schedules, RFIs,
change orders, emails, meeting minutes, engineering studies, grid requirements, permits, commissioning
plans, test reports, site reports, procurement and delivery information, construction progress and
approval records.

**The hard problem is understanding the relationships between these pieces of information** — and how
a change in one propagates to the others.

```
Transformer delivery → installation → cable termination → protection testing
  → commissioning → grid compliance testing → energization
```

The evidence for each link is scattered across supplier emails, purchase orders, engineering
documents, schedules, commissioning plans and grid-connection requirements. Today a technical
professional reconstructs this by hand. GridPulse is designed to reduce that work.

## 4. The central question

> **What changed, what does it affect, what evidence supports that assessment, and what needs attention now?**

## 5. What GridPulse is not

- an AI project manager, project-management software, task-management or scheduling software
- a scheduling engine or Gantt-chart replacement
- a replacement for Primavera or Aconex, or a document-management system
- a generic AI chatbot or "chat with your PDFs" product
- an engineering approval system or an automatic grid-certification system
- an ERP, SCADA, EMS, BESS control system, BIM or CAD tool
- a portfolio-management or enterprise workflow platform
- a system of record, or the contractual/authoritative source of truth

**Guardrail:** a feature belongs in GridPulse only if it strengthens the core loop.

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
VALIDATED PROJECT INTELLIGENCE
    ↓
PROJECT INTELLIGENCE GRAPH
    ↓
IMPACT ANALYSIS
    ↓
ATTENTION / ACTION
```

## 7. Discovery vs determination — a fundamental boundary

> **GridPulse must distinguish discovery from determination.**

AI can discover: *"PCS specification changed from Rev 7 to Rev 8."* · *"Rev 7 was referenced by the
PPC specification."* · *"The PPC specification is referenced by the grid-compliance test plan."*

AI can calculate: *"The new delivery date is 18 calendar days after the planned installation date."*

AI must **not** autonomously determine: *"The project will miss energization."*

Instead: *"Potential energization exposure identified. Engineering / project-control validation required."*

| Level | | May GridPulse state it? |
|---|---|---|
| 1 — Fact | Directly supported, or deterministically calculated from evidenced values | Yes, with evidence |
| 2 — Dependency / Inference | Evidence-backed relationship or analytical inference | Yes, labelled with status |
| 3 — Engineering / Project Conclusion | Consequential technical or project determination | **No** — only surfaced as potential exposure requiring human validation |

AI may read, extract, compare, detect changes and contradictions, discover and infer dependencies,
trace chains, calculate, identify missing or stale evidence, suggest reviewers and summarize. AI must
not silently certify compliance, approve engineering, declare delays, approve changes, make
safety-critical decisions or replace professional judgment.

## 8. First user

**Owner's Engineer / technical project-control professional working on large BESS projects** (D-013).
The MVP is not designed simultaneously for developers, EPCs, grid operators, other consultants,
data-center operators, commissioning companies or investors.

This user often does **not** own the schedule (the EPC frequently does). GridPulse must be useful when
the schedule is incomplete or unavailable (D-003).

**What this user actually receives (D-041).** Suppliers usually communicate with the EPC, not the OE.
The OE typically learns of changes through reporting-period documents: EPC monthly progress reports,
schedule updates, submittals and document revisions, meeting minutes and correspondence copied to the
owner — often later and less precisely than the original. GridPulse is designed around that flow. The
killer question for this user:

> *"What changed since the last reporting period, what may it affect, and is it consistent across the
> evidence?"*

GridPulse reports inconsistencies between sources as facts with evidence; it never characterises any
party's intent.

**First question:** *Can GridPulse materially reduce the investigation workload of a technical
professional when project information changes?*

## 9. Initial wedge and long-term scope

**Initial wedge:** *AI-powered change, evidence and dependency intelligence for grid-connected
infrastructure projects.* MVP scope: **one project**; no portfolio functionality (D-018).

Long-term lifecycle coverage (not built now): project intake → data room → requirements → grid
maturity → grid application → grid offer → contracts → engineering → procurement → construction →
commissioning → grid compliance → energization → COD.

**Where GridPulse's value is most distinct (D-042, D-043).** Scheduling systems already propagate
date changes well. GridPulse's distinct value lies in:

1. **links no schedule contains** — e.g. PCS specification → PPC design basis → grid-compliance
   requirement and test;
2. **non-date changes** — specification revisions, requirement changes, test results;
3. **disagreement between sources** — e.g. progress report vs schedule update vs supplier statement.

**Long-term graph goal:** AI reconstructs and maintains the project intelligence graph from the
project's existing information, rather than humans modelling everything manually.

## 10. Value hypothesis and measurement

The goal is to **reduce the amount of expert investigation required after project information changes.**

> **Product hypothesis / target — not an industry fact, not validated evidence:**
> ~4 hours of manual investigation → ~15 minutes of AI investigation + 30–60 minutes of expert validation.

**Critical metric:** investigation compression while maintaining acceptable evidence precision and recall.

Measurement is part of the architecture from the beginning (D-017). The benchmark measures change
detection accuracy, direct- and secondary-impact recall, evidence precision, stale-evidence detection,
false-positive rate, reviewer routing accuracy, gate identification, investigation time and human
correction rate — and checks that no unsupported determinations are made.

"Review required" alone is not value. An investigation must deliver evidence, affected entities, the
dependency chain, deterministic calculations, relevant milestones, uncertainty, suggested reviewers
and unresolved questions.

## 11. Conditions for GridPulse to be useful

1. Knows what information changed.
2. Knows where the information came from.
3. Knows which project entity is affected.
4. Can connect the entity to relevant dependencies.
5. Can explain its reasoning with evidence.
6. Distinguishes fact from inference, and discovery from determination.
7. Allows humans to review and correct it.
8. Makes corrections part of Validated Project Intelligence.
9. Does not invent engineering conclusions.
10. Continuously updates as the project evolves.

## 12. Key risks

| # | Risk | Why it matters |
|---|---|---|
| 1 | **Graph quality** | The dependency graph may be harder to construct reliably than event detection; impact analysis is only as good as the graph. |
| 2 | **Review overload** | If everything requires human attention, GridPulse becomes another work queue. |
| 3 | **Weak output** | "Review required" alone is not enough; the investigation itself must be substantive. |
| 4 | **False engineering conclusions** | Unsupported technical conclusions must never appear authoritative — by wording, layout or implication. |
| 5 | **Data access** | The buyer may not control all project systems (e.g. the EPC owns the schedule). |
| 6 | **Confidentiality** | Infrastructure projects contain sensitive information; real data requires enterprise controls. |
| 7 | **Ground truth** | Reliable benchmark data is scarce; an author-written synthetic corpus is cleaner than real data and will flatter results (mitigation: corpus realism tiers, D-044). |
| 8 | **Scope creep** | Customers may request generic project-management features. |
| 9 | **Liability** | Incorrect or incomplete impact analysis could have commercial consequences, and a flagged-but-ignored exposure creates a discoverable record. GridPulse is positioned as decision support, not a guarantee of completeness; D-021 and the audit trail are part of the mitigation. |
| 10 | **Incumbent AI** | Oracle (Aconex/Primavera), Procore and others are adding AI. If the value is "AI reads our documents", incumbents win. GridPulse must win on cross-system dependency intelligence and accumulated validated review data. |
| 11 | **Intake mismatch** | If the first user does not receive the information the product assumes, the demonstrations do not reflect real use (D-041; tested by the validation gate). |
| 12 | **Unvalidated thesis** | The product definition precedes practitioner validation; Phase 2 is gated on `VALIDATION_PLAN.md` (D-044). |
