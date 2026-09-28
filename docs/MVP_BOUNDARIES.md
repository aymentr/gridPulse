# MVP Boundaries

**Phase 0 — LOCKED** (amended by council-review decisions D-041 – D-047). Nothing here selects a technology, schema or UI. Items depending on open Phase 1
decisions are marked **[D-xxx]**.

## 1. MVP goal

> **Can GridPulse materially reduce the investigation workload of an Owner's Engineer / technical
> project-control professional on a large BESS project when project information changes — without
> making unsupported conclusions?**

Demonstrated on **one project**, with **synthetic/public data**, through **two co-primary vertical
slices** (`PHASE_1_ARCHITECTURE.md` §16, D-042): **transformer delivery divergence** and **PCS
specification change**, each including **at least one AI-inferred, unseeded dependency**. Inputs are
framed as the OE receives them — by reporting period (D-041).

**Precondition:** implementation starts only after the validation gate passes
(`VALIDATION_PLAN.md`, D-044).

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
| Dependencies with relationship confidence, validation status and provenance; at least one AI-inferred dependency per scenario | D-004, D-023, D-025, D-027 |
| Impact analysis: direct → secondary → milestones → checkpoints → potential exposure | Phase 1 §10 |
| Deterministic calculations and comparisons | D-005 |
| Three confidence/validation axes (`UNVALIDATED` / `CONFIRMED` / `REJECTED`) | D-006, D-027 |
| Selective, prioritised Review Queue — not every extracted fact | D-026 |
| Fixed MVP checkpoints (neutral names; never READY / NOT READY) | D-016, D-033 |
| Narrow Ask GridPulse distinguishing validated / observed / inferred / calculated information | D-019, D-037 |
| Configured reviewers/roles; routing suggestions | D-024 [D-008] |
| Complete history of GridPulse's own actions | D-012 |
| Benchmark harness and metrics, reported per corpus realism tier; incl. inferred-dependency precision, entity-resolution accuracy, divergence detection, review load | D-017, D-044 |
| Cross-source divergence detection (report vs schedule update) | D-043 |

## 3. Data policy

- **Synthetic and public data only** (D-015).
- No production enterprise security in the MVP; production requirements are documented
  (`PHASE_1_ARCHITECTURE.md` §17) and must be met before any real customer data is used.

## 4. Explicitly out of scope

- Write-back to any external system (D-002)
- Production integrations; live mailbox connection
- Project management, task management, scheduling/CPM, Gantt editing, document management
- Portfolio / multi-project functionality (D-018)
- Configurable enterprise gate management; checkpoint readiness verdicts (D-033)
- Elaborate review workflow (multi-step approvals, SLAs, delegation)
- Risk/confidence-based auto-acceptance of AI findings (D-001)
- Automatic delay, float or cost conclusions; compliance certification; engineering approval
- General-purpose chatbot or document Q&A
- Authentication/authorization implementation (D-024)
- Enterprise compliance program (D-015)
- BIM, CAD, SCADA, EMS, trading, ERP, project accounting, IoT
- Understanding drawings, single-line diagrams and protection-setting files — **known limitation**;
  evidence may still cite a drawing's register entry and revision [D-047]

## 5. Deferred, but the architecture must not block

AI maintenance of the full graph · more channels and integrations · configurable gates · multiple
projects · risk-based review routing · write-back (only if a customer need is demonstrated) ·
production security · additional domains and lifecycle stages.

## 6. Not decided yet

Technology stack, frameworks, database, LLM/AI provider, data schema, API, UI design, authentication
approach, hosting, pricing — Phase 2 or later.

## 7. MVP exit criteria

1. Both vertical slices run end to end through the normal intake path.
2. Each slice includes at least one AI-inferred (not seeded) dependency, labelled `INFERRED`, shown
   with evidence and `Validation: UNVALIDATED`.
3. The transformer slice raises the report-vs-schedule disagreement as a CONFLICT; the PCS slice
   raises the PPC specification's stale reference to Rev 7.
4. Every displayed claim links to verified evidence and shows its level; every dependency shows status
   and provenance.
5. Deterministic calculations are correct.
6. **Zero** unsupported determinations (e.g. "energization will be delayed", "the plant will fail grid
   compliance testing") and no statements about a party's intent.
7. No AI-detected finding reaches Validated Project Intelligence without review; no direct edits exist.
8. Conflicts are surfaced, not resolved.
9. Benchmark metrics are produced for both slices and all corpus tiers, including review load and
   investigation time against a manual baseline — treated as evidence for or against the hypothesis,
   not as proof.
