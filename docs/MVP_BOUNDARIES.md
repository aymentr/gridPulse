# MVP Boundaries

This document states what the first build of GridPulse should and should not include. It is derived
from the product vision; items that depend on unresolved decisions are marked **[pending D-xxx]**
(see `DECISIONS.md`). Nothing here selects a technology.

## 1. MVP goal

Demonstrate the **first killer scenario** end to end, credibly and with evidence:

> A supplier email moves the transformer delivery date from January 12 to February 2. GridPulse
> detects a Potential Event with old/new value, affected equipment, source, evidence and confidence;
> a human confirms it; GridPulse updates the trusted project state, traces
> delivery → installation → HV commissioning → grid compliance testing → energization, and reports
> **potential** impact requiring review — without declaring energization delayed.

The MVP succeeds if it proves the core loop **Detect → Evidence → Review → Understand → Impact → Act**
on this scenario.

## 2. In scope (minimum needed for the scenario)

| Capability | Why it is needed |
|---|---|
| A project with an initial state (entities, dates, dependencies) backed by evidence | Scenario starts from a known state **[pending D-003]** |
| Universal intake path with at least one channel | New information must enter **[pending D-014]** |
| AI extraction of facts with evidence pointers | Evidence principle |
| AI detection of a Potential Event (delivery date change) with the attributes in `CORE_CONCEPTS.md` | Detect step |
| Review Queue: confirm / reject (and correct **[pending D-010]**) | Human review is fundamental |
| Trusted project state updated only by confirmed events | Trusted-state principle |
| Project Intelligence Graph sufficient to hold the scenario's dependency chain | Impact tracing |
| Impact analysis that traces the chain and outputs *potential* impacts, each link labelled Fact / Inference with evidence | Impact step, three-level principle |
| Evidence inspection for every shown claim | "Why does GridPulse believe this?" |
| Audit of who reviewed what and when | Review record |
| A way to measure investigation time and evidence precision/recall on the scenario | Critical metric **[pending D-017]** |

## 3. Explicitly out of scope for the MVP

- Building all intake channels or any production integration (Aconex, P6, SharePoint, Procore, …)
- Replacing or writing back to any source system **[pending D-002]**
- Generic PM features: task management, Gantt editing, resource planning, document management
- Automatic delay, cost or float conclusions; compliance certification; engineering approval
- Full lifecycle coverage (grid application, grid offer, contracts, …) — architecture must allow it later
- Domains beyond BESS / grid-connected infrastructure
- Full event taxonomy handling — the scenario needs delivery/shipment events; others may be recognised
  but need not be fully supported **[pending D-007]**
- Full "Ask GridPulse" natural-language investigation **[pending D-019]**
- Full Gates and Requirements views **[pending D-016]**
- Automated reviewer routing beyond a simple assignment **[pending D-008]**

## 4. Deferred, but the architecture must not block

- Additional intake channels and integrations
- Additional event types and domains
- Later lifecycle stages
- Gates, requirements-evidence coverage, contradiction detection, version comparison
- Evidence-backed natural-language investigation
- Reports

## 5. Not decided here

Technology stack, database schema, AI provider/model, deployment/hosting model, UI design and
pricing are **not** decided in Phase 0.

## 6. Exit criteria for the MVP (proposed)

1. The killer scenario runs end to end from raw supplier email to routed potential impact.
2. Every displayed claim links to its evidence and shows its level (Fact / Inference).
3. No output states or implies a Level 3 conclusion.
4. Rejected and corrected events are handled and recorded.
5. Investigation time and evidence precision/recall are measured against a manual baseline.

These criteria are a proposal for founder review.
