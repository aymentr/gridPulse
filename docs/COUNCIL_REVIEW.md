# Council Review — Evaluation of the GridPulse Idea

**Date:** 2026-09-27 · **Scope:** Phase 0 product definition + Phase 1 architecture draft ·
**Outcome:** amendments D-041 – D-047 in `DECISIONS.md`, adopted on founder instruction.

The idea was evaluated from eight perspectives. All documents at the time were derived from the
founder's specification and Claude's synthesis; **no customer had yet validated them** — the council
treated that as the largest gap.

## Verdict

**Proceed — with changes to the demonstration scenarios and a validation gate before Phase 2.**

| Seat | Vote | Summary |
|---|---|---|
| Owner's Engineer (target user) | Conditional | "Useful, but supplier emails don't reach me; I see changes weeks later in the EPC's report." |
| Project scheduler | Conditional | "For a date change I'd update P6. Show me what P6 *can't* do." |
| Grid / electrical engineer | Proceed | "Specification changes rippling into grid compliance are the real pain." |
| AI engineer | Proceed | "Feasible, except entity resolution and dependency inference; a synthetic benchmark will flatter you." |
| Investor | Conditional | "Right trust design, growing market; buyer and budget unproven; incumbents are adding AI." |
| Legal / risk | Proceed | "Non-determination plus audit trail is correct; 'you flagged it' duty-of-care question remains." |
| Competitor analyst | Conditional | "Cross-system evidence + dependency intelligence is a real gap; defensible only if validated review data compounds." |
| Red team | Conditional | "Thousands of lines of specification, zero customer conversations. Stop writing, start testing." |

## Findings by seat

### Owner's Engineer
- Evidence trails and non-determination match OE professional practice ("potential exposure,
  validation required" is how OEs already write).
- **Information-flow mismatch:** suppliers write to the EPC, not the OE. The OE typically learns of a
  slip via the EPC monthly report, a schedule update or a meeting — late or softened.
- Recurring OE workload: monthly progress/schedule review, submittal and specification-revision
  review against requirements, open technical issues, owner reporting. OEs often cover several
  projects at once.
- Stronger killer question: *"What changed since the last reporting period, and is it consistent
  across the evidence?"*

### Project scheduler
- Date propagation is where P6 is strongest; GridPulse's refusal to calculate can look like weakness.
- GridPulse wins on links not in any schedule, on non-date changes, and on detecting that sources
  (report vs schedule) disagree.

### Grid / electrical engineer
- The PCS Rev 7 → Rev 8 → PPC → grid-compliance chain is high-consequence, cross-document and
  invisible to schedules.
- Drawings, single-line diagrams and protection-setting files hold much of the truth; text-only
  extraction will miss it. Domain precision (HV vs MV, test naming) is essential for credibility.

### AI engineer
- Feasible now: extraction of dates/revisions/references, citation verification, version diffing.
- Hard: **entity resolution** (make-or-break for impact paths) and **dependency inference** (noisy;
  precision matters more than recall because false links cost reviewer time).
- Author-written synthetic corpora are cleaner than reality; include degraded and public real
  documents early.

### Investor
- Positive: growing BESS/grid buildout; "intelligence layer" avoids head-on competition with
  Oracle/Procore.
- Open: who pays (OE firm vs owner/developer vs lender's technical advisor), pricing unit, and feature
  risk as incumbents add AI. Consider a services-led start (an OE firm delivering GridPulse-assisted
  reviews).

### Legal / risk
- Non-determination, "not the source of truth", reviewer attribution and immutable audit are right.
- Residual exposure: flagged-and-ignored records, and reliance on completeness. Position GridPulse as
  decision support, not a completeness guarantee. Start the security story before the first real pilot.

### Competitor analyst
- Adjacent categories exist (contract-risk AI for construction, AI schedule analytics, schedule
  optimisation, AI assistants inside Procore/Oracle). Their current feature sets were not verified in
  this review. None is framed as cross-system change → evidence → dependency → validated impact.
- Defensible assets: BESS/grid ontology and propagation rules; accumulated human-validated
  dependencies and corrections; trust from never overstating. Document search and summarisation are
  not defensible.

### Red team
- Over-architecture before observing the workflow.
- Review overload may be structural; the time-saving hypothesis could invert once review time counts.
- The decisive test: time an experienced OE on a real change case, manual vs GridPulse-style output.

## Adopted changes

| # | Change | Decision |
|---|---|---|
| 1 | Reframe intake around what the OE actually receives (reporting periods: EPC reports, schedule updates, submittals, minutes, copied correspondence) | D-041 |
| 2 | Make the PCS specification-change scenario co-primary with the transformer scenario | D-042 |
| 3 | Reframe the transformer demonstration as cross-source divergence detection, not date propagation | D-043 |
| 4 | Validation gate before Phase 2: interviews, real change stories, timed OE comparison, corpus realism tiers | D-044 |
| 5 | Buyer and pricing hypotheses written down and tested | D-045 (OPEN) |
| 6 | Freeze documentation; resolve only the five blocking decisions before Phase 2 | D-046 |
| 7 | Record drawings/SLDs/protection settings as a known MVP limitation | D-047 (OPEN) |

Also applied: inferred-dependency precision, entity-resolution accuracy, cross-source divergence
detection and review load added as benchmark metrics; legal positioning (decision support, not a
completeness guarantee) and incumbent-AI risk added to the risk register.

## What would change the verdict to "stop"

- Practitioners say change investigation is not a top-3 pain; or
- the timed comparison shows little or no saving once review time is included.
