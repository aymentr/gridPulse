# MVP Boundaries

**Phase 0 — LOCKED.** Nothing here selects a technology, schema or UI. Items depending on open Phase 1
decisions are marked **[D-xxx]**.

## 1. MVP goal

> **Can GridPulse materially reduce the investigation workload of an Owner's Engineer / technical
> project-control professional on a large BESS project when project information changes — without
> making unsupported conclusions?**

Demonstrated on **one project**, with **synthetic/public data**, through the transformer delivery
change vertical slice (`PHASE_1_ARCHITECTURE.md` §16), which must include **at least one AI-inferred
dependency**.

## 2. In scope

| Capability | Basis |
|---|---|
| Inputs: documents, schedule (optional), supplier communications, manual project facts, other imported information | D-003, D-014 |
| One universal intake path | P13 |
| Extraction of claims with verified evidence | D-005, P5 |
| Change detection with lifecycle `DETECTED → UNDER_REVIEW → CONFIRMED / REJECTED` | D-009 |
| Conflict detection — never silently resolved | D-011 |
| Stale-evidence and missing-evidence detection | D-017 |
| Review Queue with `CONFIRM`, `REJECT`, `REQUEST_INVESTIGATION`, `EDIT_FINDING` | D-010 |
| Authorized manual entry as `CONFIRMED` with `MANUAL_ENTRY` provenance | D-001, D-024 |
| Validated Project Intelligence changed only via review/manual entry | D-020 |
| Dependencies with status + provenance; at least one AI-inferred dependency in the demo | D-004, D-023, D-025 |
| Impact analysis: direct → secondary → milestones → gates → potential exposure | Phase 1 §10 |
| Deterministic calculations and comparisons | D-005 |
| Three confidence/validation axes | D-006 |
| Fixed MVP gate set as intelligence checkpoints | D-016 |
| Narrow Ask GridPulse over Validated Project Intelligence with evidence | D-019 [D-037] |
| Configured reviewers/roles; routing suggestions | D-024 [D-008] |
| Complete history of GridPulse's own actions | D-012 |
| Benchmark harness and metrics | D-017 |

## 3. Data policy

- **Synthetic and public data only** (D-015).
- No production enterprise security in the MVP; production requirements are documented
  (`PHASE_1_ARCHITECTURE.md` §17) and must be met before any real customer data is used.

## 4. Explicitly out of scope

- Write-back to any external system (D-002)
- Production integrations; live mailbox connection
- Project management, task management, scheduling/CPM, Gantt editing, document management
- Portfolio / multi-project functionality (D-018)
- Configurable enterprise gate management; gate readiness verdicts [D-033]
- Elaborate review workflow (multi-step approvals, SLAs, delegation)
- Risk/confidence-based auto-acceptance of AI findings (D-001)
- Automatic delay, float or cost conclusions; compliance certification; engineering approval
- General-purpose chatbot or document Q&A
- Authentication/authorization implementation (D-024)
- Enterprise compliance program (D-015)
- BIM, CAD, SCADA, EMS, trading, ERP, project accounting, IoT

## 5. Deferred, but the architecture must not block

AI maintenance of the full graph · more channels and integrations · configurable gates · multiple
projects · risk-based review routing · write-back (only if a customer need is demonstrated) ·
production security · additional domains and lifecycle stages.

## 6. Not decided yet

Technology stack, frameworks, database, LLM/AI provider, data schema, API, UI design, authentication
approach, hosting, pricing — Phase 2 or later.

## 7. MVP exit criteria

1. The transformer slice runs end to end through the normal intake path.
2. At least one dependency in the slice is AI-inferred (not seeded), labelled `INFERRED`, and shown
   with evidence and `Validation: REQUIRED`.
3. Every displayed claim links to verified evidence and shows its level; every dependency shows status
   and provenance.
4. Deterministic calculations are correct.
5. **Zero** unsupported determinations (e.g. "energization will be delayed").
6. No AI-detected finding reaches Validated Project Intelligence without review; no direct edits exist.
7. Conflicts are surfaced, not resolved.
8. Benchmark metrics are produced for the slice, including investigation time against a manual
   baseline — treated as evidence for or against the hypothesis, not as proof.
