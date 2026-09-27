# Engineering Principles

Rules any implementation of GridPulse must respect, regardless of technology stack. They are derived
directly from the product vision. Where a principle is a derivation rather than an explicit statement
in the vision, it is marked *(derived)*.

These principles are technology-neutral. No framework, database or AI provider has been chosen.

---

## P1. Evidence or it didn't happen

Every important AI-generated claim must be traceable to evidence down to
source → record → version → page/section/chunk/location. A claim without evidence must not be
presented as fact. Users must always be able to inspect *why* GridPulse believes something.

## P2. Keep the three levels separate

Fact (Level 1), Dependency/Inference (Level 2) and Engineering/Project Conclusion (Level 3) must be
distinguishable everywhere a claim is stored or shown. GridPulse must never promote an inference to a
fact silently, and must never produce a Level 3 conclusion autonomously.

## P3. AI proposes; humans decide

AI detection is not truth. Consequential changes pass through human review before entering the trusted
project state. AI must not silently certify compliance, approve engineering, declare delays, approve
changes, or make safety-critical decisions.

## P4. The trusted project state changes only through reviewed events

The trusted state is changed by confirmed Project Events and human corrections — not by raw AI output.
Reviewer and decision are recorded. Human corrections become part of the trusted state.

## P5. One universal intake path

All information — manual entry, document upload, email, schedule update, integration, future systems —
flows through a single event/change intake mechanism. New channels are adapters onto that path, never
separate pipelines with separate semantics.

## P6. Intelligence layer, not system of record

GridPulse reads from existing systems (Aconex, P6, SharePoint, Procore, email, …) and does not try to
replace them. Features that duplicate generic project-management, document-management or scheduling
functionality are out of scope unless they directly serve the core loop.

## P7. Events are first-class; the project is not static

GridPulse models a project that changes continuously. Real-world events are a core object, with old
state, new state, detected time and effective time — not an afterthought to document analysis.

## P8. Preserve history *(derived)*

To answer "what changed?" and to keep evidence inspectable, GridPulse must retain source versions,
events (including rejected ones), review decisions and prior states rather than overwriting them.
(Exact retention semantics are an open decision — see DECISIONS.md.)

## P9. Impact is "potential" until a human says otherwise

Impact analysis identifies what *may* be affected and who should look at it. Its language and data
model must make that explicit ("Potential impact detected. Review required.").

## P10. Measure investigation quality, not just speed

The critical metric is **investigation compression while maintaining acceptable evidence precision
and recall.** Time savings that come at the cost of missed or wrong evidence are not success.
Stated targets (4 h → 15 min AI + 30–60 min expert) are hypotheses to be validated experimentally.

## P11. Domain-first, not domain-locked *(derived)*

BESS / grid-connected infrastructure is the first domain and the design should be driven by its real
workflows. The underlying intelligence architecture should not preclude later domains (data centers,
other capital projects) or later lifecycle stages (intake through COD).

## P12. Every feature must reinforce the loop

**Detect → Evidence → Review → Understand → Impact → Act.** A proposed feature that does not strengthen
this loop should be challenged before it is built.

## P13. Do not silently make major decisions

Product and architecture ambiguities are recorded in `DECISIONS.md` with options, a recommendation and
reasoning, and left for founder review. Do not invent requirements absent from the product vision.
