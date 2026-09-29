# Technical Realism Review — Internal Coordination

**Status: NOT PERFORMED — OPTIONAL FOLLOW-UP VALIDATION.** No independent technical realism review
has been performed. No real BESS / grid practitioner has reviewed the packs. The report forms
`scenario-a-review.md` and `scenario-b-review.md` are blank. Neither scenario is technically reviewed.

The review is **non-blocking** for Route B (D-051). It remains desirable external evidence before any
claim that the scenarios represent real-world BESS workflows or engineering practice.

> This README is internal. **Do not give it to the reviewer.**

## Purpose

Establish whether the synthetic source documents are technically and operationally plausible for a
BESS / grid project. This is **not** a validation run and does not assess GridPulse, the business, or
the investigation bundles.

## Recruitment

See `OUTREACH.md` (internal): target profile, exclusions, candidate sources, outreach message
(EN/DE), delivery rules, outreach log and independence record. Status: no reviewer recruited.

## Who may perform it

A real practitioner with BESS / grid / project-controls experience who:

- did not author the packs (the packs were authored with AI assistance; the author's own check is not
  independent);
- **will not take part in Route B** as an expert investigator, since the review exposes them to the
  source documents;
- may still take part in Route A interviews, provided the interview does not discuss the packs.

Do not simulate a reviewer and do not record AI output as a review.

## What the reviewer receives — and only this

| Item | Path |
|---|---|
| Instructions | `reviewer-pack/REVIEWER_INSTRUCTIONS.md` |
| Pack 1 source documents (Scenario A, 15 files) | `reviewer-pack/pack-1/` |
| Pack 2 source documents (Scenario B, 12 files) | `reviewer-pack/pack-2/` |
| Report forms | `scenario-a-review.md`, `scenario-b-review.md` |

`pack-1/` and `pack-2/` are flat copies of the scenario source folders (`baseline/`, `changed/`,
`supporting/`, `schedule/`, `progress-report/`), **excluding** each `supporting/SOURCES.md`, which
describes the test design. Pack 1 includes the supplier letter used only in variant runs, because it is
part of the source material being assessed for realism.

## Never give the reviewer

`ground-truth/` · `investigation-bundle.md` · scenario `README.md` files · `SOURCES.md` ·
`docs/PHASE_1_ARCHITECTURE.md` · `docs/VALIDATION_PLAN.md` · `docs/DECISIONS.md` ·
`docs/COUNCIL_REVIEW.md` · `validation/scoring/` · this README · `OUTREACH.md` · benchmark expectations, finding counts,
forbidden-conclusion lists, the product hypothesis, or any previous GridPulse analysis.

Do not tell the reviewer which document carries a change or what either pack is meant to test.

## Keeping the copies in sync

The `reviewer-pack/` copies were taken at repository commit `0cd87d6` (validation materials frozen).
If any scenario source document changes, re-copy before sending, still excluding `SOURCES.md`.

## After the review — correction policy

| Result | Action |
|---|---|
| No CRITICAL issues | Change nothing automatically; evaluate each MAJOR issue individually |
| MAJOR issues | Correct only where the change improves realism **and** passes the protection check below |
| Any CRITICAL issue | Pause further Route B runs; fix the pack; repeat the technical realism review. Record which runs used the earlier version and interpret them accordingly |

### Protection check (every proposed correction)

A correction is **reported, not implemented**, if it would:

- reveal the intended change;
- reveal an intended dependency;
- make the investigation easier or the expected findings more obvious;
- remove legitimate ambiguity;
- change the ground truth (other than a citation made invalid by a wording change);
- introduce information an investigator could not otherwise obtain.

## Open technical-realism questions (internal — never give to investigators)

These were raised by the pack author, who is not independent. They are **open questions, not confirmed
errors**. The scenarios, ground truth, bundles and scoring were deliberately **not** changed because of
them (D-051).

| Scenario | Open question |
|---|---|
| A | Transformer installation / dressing duration |
| A | Terminology: pre-energization checks versus grid-compliance testing |
| A | Delivery / progress-report / schedule workflow assumptions |
| B | Low-output power-factor wording |
| B | Reactive-power interpretation |
| B | PCS capability versus grid requirement |
| B | PPC relationship |
| B | Compliance-test points |

## Status

- Architecture — ARCHITECTURE REVIEWED
- Benchmark — BENCHMARK CONSTRUCTED
- Technical realism — NOT INDEPENDENTLY VALIDATED
- Product validation — PENDING (Route B unblocked, not yet run)
- Phase 2 — BLOCKED UNTIL VALIDATION GATE IS PASSED
