# Engineering Principles

**Phase 0 — LOCKED.** Rules any implementation must respect, regardless of technology. No framework,
database, LLM or other technology has been chosen.

---

## P1. Intelligence layer, not project management
No task management, Gantt editing, scheduling, document management, portfolio management or enterprise
workflow. Milestones and dependencies are displayed only in service of intelligence. GridPulse is not a
scheduling engine.

## P2. Read-only against systems of record (MVP)
GridPulse modifies no external system (D-002).

## P3. Validated Project Intelligence is not the source of truth
GridPulse's validated view must never be presented — in data, wording or UI — as the contractual,
legal, engineering, scheduling or authoritative record (D-021). Divergence from a system of record is
shown, not hidden or corrected.

## P4. Discovery, not determination
AI discovers, extracts, compares, infers and calculates. It never determines Level 3 conclusions;
candidate implications appear only as *potential exposure — validation required*.

## P5. Evidence or it didn't happen
Every important statement resolves to verified evidence. If it cannot, GridPulse says it has no
supporting evidence.

## P6. Keep the three levels separate
Level 1 (fact, including deterministic calculations), Level 2 (dependency/inference), Level 3
(human-only conclusion) are distinguishable wherever claims are stored or shown.

## P7. No silent promotion; no direct edits
AI-detected findings start `DETECTED`/`UNDER_REVIEW`. Only explicit human review or authorized manual
entry produces `CONFIRMED`; everything else stays `UNVALIDATED` and labelled (D-027). Validated Project
Intelligence changes only via `SOURCE → DETECTION → FINDING → REVIEW`, or authorized manual entry with
`MANUAL_ENTRY` provenance (D-001, D-020). Review is selective and prioritised — consequential changes,
conflicts, inferred links in active investigations, stale and critical missing evidence (D-026).

## P8. The Review Queue is trust architecture
Reviewers see what, why, source, change, entity, confidence axes, possibly affected dependencies and
uncertainty. Actions: `CONFIRM`, `REJECT`, `REQUEST_INVESTIGATION`, `EDIT_FINDING`. No elaborate workflow.

## P9. Never silently resolve conflicts
Contradictions become CONFLICT findings with all sources and evidence (D-011).

## P10. Separate confidence axes; no pseudo-precision
Evidence confidence, relationship confidence and validation status are separate. No percentages
without a validated statistical basis (D-006).

## P11. Dependencies carry confidence, validation and provenance
Relationship confidence (`EXPLICIT` / `INFERRED`) and validation status (`UNVALIDATED` / `CONFIRMED` /
`REJECTED`) are separate axes; provenance distinguishes schedule-derived, document-derived,
AI-extracted, AI-inferred and human-confirmed (D-004, D-023, D-027).

## P12. Reconstruct from existing information; schedule optional
The graph is reconstructed from documents, schedules, supplier communications, manual facts and other
imports. A schedule is preferred, never required. Manual seeding only for benchmark ground truth.

## P13. One universal intake path
All channels are adapters onto one intake mechanism.

## P14. Complete history of GridPulse's own actions
Retain detected changes, findings, reviews, confirmations, rejections, dependency status changes,
evidence associations, investigation requests and reviewer actions. Do not recreate external document
or schedule history (D-012).

## P15. Measurement is built in
Every stage records what is needed for the benchmark metrics (D-017). The 4 h → 15 min + 30–60 min
figure is a hypothesis only.

## P16. Explicit reviewer identity
Reviewer identity and role are explicit on every action so authentication can be added later (D-024).

## P17. Confidentiality-aware; synthetic data only for now
Prototype and benchmark use synthetic/public data only. The architecture must not preclude the
production security requirements in `PHASE_1_ARCHITECTURE.md` §17 (D-015).

## P18. Single project, extensible
MVP is one project; nothing prevents multi-project later (D-018).

## P19. Design for the first user
Owner's Engineer / technical project-control professional on large BESS projects (D-013).

## P20. Every feature must reinforce the loop
Real world → information enters → detection → evidence → human review → Validated Project
Intelligence → project intelligence graph → impact analysis → attention / action.

## P21. The model must stand without the UI
Remove the dashboard, chatbot and UI: evidence, changes, dependencies, impact and Validated Project
Intelligence must still form a coherent model.

## P22. Inferred-dependency precision over recall
A false inferred link costs reviewer time and erodes trust. Prefer fewer, well-evidenced inferences;
inferred-dependency precision is a primary benchmark metric (D-044).

## P23. Review load is a cost, measured
Every review item a change generates counts against the investigation saving. Review load (items and
minutes per change) is measured, not assumed away (Risk 2, D-044).

## P24. Report disagreement, never intent
When sources disagree, GridPulse states the disagreement with evidence. It never characterises a
party's motives or competence (D-043).

## P25. Validate before building
Assumptions about users, information flow and value are tested with practitioners before
implementation (D-044). Documentation is frozen except for blocking decisions and validated
amendments (D-046).

## P26. Never fabricate validation evidence
No invented interviews, participants, quotes, approvals, willingness to pay or benchmark results.
Public research is not practitioner validation (D-044).

## P27. Precision and recall are reported separately
Never collapse them into one score; completeness does not mean 100 % recall (D-044).

## P28. Do not silently make major decisions
Ambiguities go to `DECISIONS.md` for founder review.
