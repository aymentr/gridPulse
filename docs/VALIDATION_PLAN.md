# Validation Plan — Gate Before Phase 2

**Status:** ACTIVE. Phase 2 (implementation) does not begin until this gate passes (D-044).

This plan tests the assumptions the architecture rests on, before building it. It involves people and
documents, not code. A human producing GridPulse-style output behind the scenes ("concierge" /
Wizard-of-Oz) is acceptable for the timed comparison.

## 1. Assumptions under test

| # | Assumption | Source | Tested by |
|---|---|---|---|
| A1 | Investigating the consequences of project changes is a top-3 pain for OEs / technical project-control professionals | Product vision | Interviews |
| A2 | The OE receives changes through reporting-period documents (EPC reports, schedule updates, submittals, minutes, copied correspondence) rather than direct supplier communication | D-041 | Interviews, real change stories |
| A3 | Cross-document technical changes (specification → design → grid compliance) are more painful and less well served than date changes | D-042 | Interviews, change stories |
| A4 | Detecting disagreement between sources (report vs schedule) is valued | D-043 | Interviews, timed comparison |
| A5 | An evidence-backed investigation bundle materially reduces investigation time **including** review time | Value hypothesis (not a fact) | Timed comparison |
| A6 | "Potential exposure — validation required" output is acceptable and useful to practitioners (not "too thin") | D-005 | Timed comparison debrief |
| A7 | Someone will pay, and who | D-045 | Interviews |

## 2. Practitioner interviews

**Who:** 8–12 people. Priority: Owner's Engineers and technical project-control professionals on
large BESS / grid-connected projects. Include 2–3 adjacent roles for contrast (developer project
director, lender's technical advisor, EPC project controls) — without redesigning for them (D-013).

**Guide (45 min, open questions; do not pitch until the end):**

1. Walk me through the last time a project change landed on your desk and you had to work out what it
   affected. What was it? How did you hear about it?
2. Which documents do you routinely receive from the EPC, and how often? Which do you *not* see?
3. How long did that investigation take? Who else did you involve? What did you produce at the end?
4. What was the hardest part — finding the information, connecting it, or deciding what it meant?
5. Tell me about a change you or a colleague **missed** or caught late. What did it cost?
6. How do you handle specification or submittal revisions? How do you check what references the old
   revision?
7. When the progress report and the schedule disagree, what do you do?
8. How many projects do you cover at once?
9. What tools do you use today for this (P6 viewer, Aconex, Excel trackers, email)?
10. *(After showing a GridPulse-style output mock-up)* Would you trust this? What would you need to
    see? What is missing? Is "potential exposure — validation required" useful or frustrating?
11. Who in your organisation or your client's would pay for time saved here? How are these reviews
    budgeted (fixed fee, time-based, per project)?

**Record per interview:** role, organisation type, project size/stage, answers to A1–A7, quotes,
documents they offered to share (anonymised).

## 3. Real change stories

Collect **3–5 anonymised real change cases** (from interviewees, public sources or the founder's own
experience) with: the triggering information, where it arrived, what it affected, how long the
investigation took, and what the right outcome was. These become:

- the realism check for the canonical scenarios, and
- candidate T3 benchmark cases (subject to confidentiality — synthetic/public only in the prototype,
  D-015; real stories are used as *patterns* unless explicitly cleared).

## 4. Timed comparison

**Participants:** 3–5 experienced OEs / project-control professionals.

**Cases:** the two canonical scenarios (transformer divergence; PCS specification change) prepared as
realistic document packs (≈15–30 documents each, with distractors), plus one real-story case if
available.

**Protocol:**

| Arm | What the participant gets | Measured |
|---|---|---|
| Manual | The document pack; task: "What changed this period, what may it affect, what evidence supports that, who needs to look at it?" | Time to answer; completeness vs ground truth; errors; confidence |
| Assisted | The same pack plus a GridPulse-style investigation bundle (produced by hand, following `PHASE_1_ARCHITECTURE.md` §10.4 and §16) with review items | Time to validate and answer; review items processed; corrections made; completeness; errors |

Counterbalance order across participants and cases. Debrief on trust, usefulness and wording.

**Pass criteria (proposed — founder to confirm):**

- Assisted time (including review) is clearly lower than manual on both scenarios — a target of at
  least ~50 % reduction; the 4 h → 15 min + 30–60 min figure remains a hypothesis, not a pass mark.
- No loss of completeness vs manual (direct and secondary impacts, stale reference, divergence).
- Participants judge the output trustworthy and not "too thin" (A6).
- Review load is acceptable to participants (items per change, minutes per change).

## 5. Buyer and pricing hypotheses (D-045 — to be tested, not decided)

| Hypothesis | Buyer | Why they might pay | Possible pricing unit |
|---|---|---|---|
| H1 | OE / technical-advisory firm | Deliver reviews faster, with better evidence, at fixed fee | Per project per month; per seat |
| H2 | Owner / developer | Earlier visibility of exposure across its project(s) | Per project; per MW under construction |
| H3 | Lender's technical advisor / lender | Evidence-backed monitoring for construction-phase lending | Per monitored project |
| H4 | Services-led start | GridPulse-assisted OE services sold by a partner firm before a software sale | Revenue share / service fee |

## 6. Gate outcome

| Outcome | Condition | Next step |
|---|---|---|
| **Pass** | A1, A2 (or an adjusted A2), A5 and A6 supported; pass criteria met | Resolve blocking decisions; fold findings into Phase 1 as amendments; start Phase 2 |
| **Pivot** | Pain confirmed but intake or scenario assumptions wrong | Amend D-041 – D-043 and the scenarios; repeat the timed comparison |
| **Stop** | Change investigation is not a top-3 pain, or no clear saving once review time counts | Revisit the product thesis |
