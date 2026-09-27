# MVP Boundaries

What the first build of GridPulse includes and excludes. Items depending on still-open decisions are
marked **[open D-xxx]**. Nothing here selects a technology, schema or UI.

## 1. MVP goal

Answer one question for one user:

> **Can GridPulse materially reduce the investigation workload of an Owner's Engineer / technical
> project-control professional on a large BESS project when project information changes?**

Demonstrated through the **transformer delivery change** scenario (`PRODUCT_WORKFLOW.md` §4), end to
end, with evidence, on synthetic/public data.

## 2. In scope

| Capability | Decision basis |
|---|---|
| Initial project state reconstructed from project documents, an imported schedule and manually entered facts; manual relationship seeding only where needed for benchmark ground truth | D-003 |
| Consuming explicit relationships from a source schedule (no scheduling engine) | D-003 |
| One universal intake path with the channels needed for the scenario | D-014 [open D-014] |
| Change detection and Potential Event creation with old/new values, affected entity, source, evidence, confidence | D-009 |
| Every AI-detected event starts `NEEDS_REVIEW`; authorized manual entry may be `CONFIRMED` | D-001 |
| Review Queue exposing what, why, source, change, entity, confidence, possibly affected dependencies, uncertainty; at least confirm / reject | D-001 [open D-010, D-022] |
| Trusted project state updated only by confirmed events | D-001, D-021 |
| Dependencies with `CONFIRMED` / `INFERRED` / `REJECTED` status | D-004 |
| Impact analysis traversing dependencies, labelling inferred links, with deterministic calculations and comparisons | D-004, D-005 |
| Investigation output: evidence, affected entities, dependency chain, calculations, relevant milestones, uncertainty, suggested reviewers, unresolved questions | Risk 3 [open D-008] |
| Clear Level 1 / 2 / 3 separation; no Level 3 conclusions | D-005 |
| Record of who reviewed what and when | D-001 |
| Measurement of investigation time and evidence precision/recall on the benchmark | [open D-017] |

## 3. Data policy for the MVP

- **Synthetic and public data only** for the prototype and benchmark (D-015).
- Production enterprise security is **not** required to prove the product.
- Before any real customer data is used, the product must address: encryption, authentication,
  authorization, tenant isolation, audit logs, data retention, data deletion, data residency,
  AI-provider data handling, contractual confidentiality and applicable enterprise security
  requirements.

## 4. Explicitly out of scope

- Any write-back to external systems (Primavera, Aconex, SharePoint, schedules, engineering systems) — D-002
- Production integrations; building every intake channel
- Task management, Gantt editing, scheduling / CPM calculation, resource planning, document management
- Automatic delay, float or cost conclusions; compliance certification; engineering approval — D-005
- Risk/confidence-based review routing (auto-accepting AI events) — D-001
- Designing for users other than the Owner's Engineer / technical project-control professional — D-013
- Domains beyond BESS; lifecycle stages beyond what the scenario needs
- Enterprise compliance program — D-015
- Granular event taxonomies — D-007
- Full "Ask GridPulse" [open D-019], full Gates and Requirements views [open D-016]

## 5. Deferred, but the architecture must not block

- AI discovery and maintenance of the full project intelligence graph (long-term goal, D-003)
- Additional channels, integrations, event categories, domains and lifecycle stages
- Risk/confidence-based review routing
- Write-back, if a customer need is demonstrated
- Enterprise security and compliance controls
- Evidence-backed natural-language investigation, reports, gates, requirement-evidence coverage

## 6. Not decided in Phase 0

Technology stack, frontend/backend frameworks, database, LLM/AI provider, data model, API design, UI
design, authentication approach, hosting and pricing.

## 7. MVP exit criteria (proposed)

1. The transformer scenario runs end to end: supplier communication → `NEEDS_REVIEW` event → human
   confirmation → trusted state update → dependency traversal → investigation routed to reviewers.
2. Every displayed claim links to its evidence and shows its level; every dependency shows its status.
3. Deterministic calculations are correct (e.g. 21 calendar days; Feb 2 is after Jan 15 installation).
4. No output states or implies a Level 3 conclusion (e.g. "energization will be delayed").
5. No AI-detected event reaches the trusted state without review.
6. Rejected events and rejected dependencies are recorded and excluded from impact analysis.
7. Investigation time and evidence precision/recall are measured against a manual baseline.
