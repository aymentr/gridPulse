# Engineering Principles

Rules any implementation of GridPulse must respect, regardless of technology. They are derived from
the product vision and the founder decisions in `DECISIONS.md`. No framework, database, LLM or other
technology has been chosen.

---

## P1. Intelligence layer, not project management

GridPulse is an AI project-intelligence layer. It must not grow task management, Gantt editing,
scheduling, document management or other generic PM functionality. Displaying milestones and
dependencies is acceptable only in service of intelligence. It is not a scheduling engine.

## P2. Read-only against systems of record (MVP)

GridPulse does not modify Primavera, Aconex, SharePoint, external schedules, engineering systems or any
other external system during the MVP (D-002). Write-back is considered only if a customer need is
demonstrated later.

## P3. Not the source of truth

GridPulse maintains a validated intelligence state derived from authoritative sources and human review.
It must never present itself — in data, wording or UI — as the contractual or authoritative record (D-021).

## P4. Evidence or it didn't happen

Every important claim is traceable to source → record → version → location. A claim without evidence
must not be presented as fact.

## P5. Keep the three levels separate

Level 1 (fact, including deterministic calculations/comparisons), Level 2 (dependency/inference) and
Level 3 (engineering/project conclusion) must be distinguishable wherever claims are stored or shown.
GridPulse never promotes an inference to a fact and never produces Level 3 autonomously (D-005).

## P6. AI-detected events always start in NEEDS_REVIEW

In the MVP every AI-detected Project Event starts as `NEEDS_REVIEW`. Only an authorized user's manual
entry may create an event directly as `CONFIRMED` (D-001). AI output is never silently promoted into
the trusted project state.

## P7. The Review Queue is trust architecture

The Review Queue is the boundary between AI output and trusted state. It must expose what was detected,
why, the supporting source, what changed, the affected entity, confidence, possibly affected
dependencies and what remains uncertain.

## P8. Dependencies carry status

Every dependency is `CONFIRMED`, `INFERRED` or `REJECTED` (D-004). Impact analysis may use `INFERRED`
dependencies but must label them; it must not use `REJECTED` ones. Human confirmation strengthens the
graph.

## P9. Reconstruct, don't require manual modelling

The graph is reconstructed from existing project information (documents, imported schedules, manually
entered facts). Explicit schedule relationships are consumed, not re-derived. Manual seeding is
acceptable only where needed for benchmark ground truth (D-003). The architecture must allow AI to
discover and infer relationships.

## P10. One universal intake path

All information — manual entry, document upload, email, schedule update, integration, future systems —
flows through a single intake mechanism. Channels are adapters, not separate pipelines.

## P11. Change and Event are distinct

A Change is a difference between states or versions; an Event is something that happened in the real
project. A Change may generate a Potential Event (D-009). The model must not conflate them.

## P12. Small, extensible event taxonomy

Prefer broad categories with attributes (old/new value, reason, affected entity) over granular types.
Descriptive labels may be derived from the state change (D-007).

## P13. Impact is potential, and must be substantive

Impact output is framed as potential impact requiring human attention. It must still be a real
investigation: evidence, affected entities, dependency chain with statuses, deterministic calculations,
relevant milestones, uncertainty, suggested reviewers and unresolved questions.

## P14. Preserve history

Retain source versions, events (including rejected ones), review decisions and prior states so that
"what changed?" can be answered and evidence stays inspectable. (Exact semantics open — D-012.)

## P15. Measure investigation quality, not just speed

The critical metric is investigation compression **with** acceptable evidence precision and recall.
Stated time targets are hypotheses to validate.

## P16. Confidentiality-aware from the start, enterprise controls later

Prototype and benchmark use synthetic and public data only (D-015). The architecture must not preclude
encryption, authentication, authorization, tenant isolation, audit logs, retention, deletion, residency,
AI-provider data-handling controls and contractual confidentiality, all of which are required before
real customer data is used. Do not build an enterprise compliance program during the MVP.

## P17. Design for the first user

Optimize for the Owner's Engineer / technical project-control professional on large BESS projects
(D-013). Do not design simultaneously for other segments.

## P18. Every feature must reinforce the loop

Real world → information enters → detection → evidence → human review → trusted project event →
project intelligence graph → impact analysis → attention / action. Features that don't strengthen this
loop are challenged before they are built.

## P19. Do not silently make major decisions

Ambiguities are recorded in `DECISIONS.md` and left for founder review. Do not invent requirements.
