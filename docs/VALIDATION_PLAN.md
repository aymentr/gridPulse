# Validation Plan — Gate Before Phase 2

**Status:** ACTIVE. **Phase 2 is BLOCKED until this gate passes** (D-044).
**Evidence collected to date:** none. No interviews, timed comparisons or benchmark runs have taken
place. Nothing in this repository should be read as validation evidence until recorded under
`validation/`.

---

## 1. The hypothesis under test

> **Change detection is the trigger, not the product.** The current economic hypothesis is **not**
> that detecting changes is valuable enough to buy. It is that the potential economic value lies in
> **compressing the cross-disciplinary investigation required after a meaningful change**.
>
> **This hypothesis is UNVALIDATED.** The validation experiment must test it directly.

The "4 h manual → 15 min AI + 30–60 min expert validation" figure is a **product target**, not an
industry fact and not evidence.

## 2. Integrity rules

These rules apply to everything recorded under this plan.

1. **Never fabricate** interviews, participants, quotes, expert approvals, willingness to pay,
   pilot commitments or benchmark results — including as placeholders or examples.
2. **Public research is not practitioner validation.** It may establish that Owner's Engineering, BESS
   project coordination, grid connection, commissioning and technical project-control services exist.
   It does not validate the GridPulse hypothesis.
3. **Route C is "External realism validation"**, never "customer validation".
4. Record only what is needed (`PRACTITIONER_INTERVIEW_TEMPLATE.md`); no unnecessary personal data.
5. Record negative and inconvenient results with the same care as positive ones.
6. Ground truth is never shown to an investigator before or during their investigation.

## 3. The gate — three dimensions

All three must pass. A strong result on one does not compensate for failure on another.

### A. Efficiency

**Measure:** total unassisted human investigation time vs total GridPulse-assisted investigation time.

**Assisted total time includes** every human minute spent on:

- reviewing the AI output
- correcting it
- any further investigation the expert still had to do
- verifying evidence
- routing to reviewers

AI generation time is **not** the metric.

**Target:** ≥ 50 % reduction in total investigation time. This is a **target, not a universal
pass/fail law**: results are interpreted together with dimensions B and C, the number of participants,
and the spread of results.

### B. Investigation quality

Compare the unassisted human baseline against the GridPulse-assisted output, per scenario:

| Measure | Reported as |
|---|---|
| Change detection | precision **and** recall |
| Direct-impact recall | recall (+ false positives listed) |
| Secondary-impact recall | recall (+ false positives listed) |
| Evidence precision | precision |
| Stale-evidence detection | precision **and** recall |
| Source-divergence detection | precision **and** recall |
| Entity-resolution accuracy | correct / incorrect merges |
| Inferred-dependency precision | precision (primary) **and** recall |
| Reviewer routing | share routed to an appropriate role |
| Review load | review items per change; reviewer minutes per change |

**A time saving does not count as success if the assisted output misses important
evidence-supported impacts.** Ground truth tags each expected item `CRITICAL` or `SUPPORTING`; any
missed `CRITICAL` item that the unassisted baseline found is a quality failure for that run.

**Completeness is not 100 % recall.** The product does not require perfect recall. For inferred
dependencies, **precision matters more than recall**: a false inferred link creates review work and
undermines trust. The validation report always shows **precision and recall as separate numbers** —
never a single combined score.

### C. Safety / determination boundary

**Unsupported Level 3 conclusions: MUST = 0.**

Forbidden unless the source evidence explicitly establishes the statement *and* its human validation
status is preserved:

- "The project will miss energization."
- "The equipment will fail grid compliance."
- "The network operator must be notified."
- "The protection study must be redone."
- Any statement about a party's intent.

Permitted form: *"Potential impact identified. Expert validation required."* Quoting a source that
itself states an obligation (e.g. the text of a notification clause) is observed information, not a
determination that the obligation is triggered.

## 4. Validation scenarios

Packs live in `validation/` (§8). Scenario definitions and expected outputs are also in
`PHASE_1_ARCHITECTURE.md` §16 — **investigators must not see that document or the ground truth**.

### Scenario A — Transformer source divergence (primary validation scenario)

**Inputs:** EPC progress report · schedule update · supplier information · relevant milestone
information (plus distractor documents).

| Source | Content |
|---|---|
| Schedule update | Transformer delivery **12 January**; installation **15 January** |
| Progress report | Transformer delivery **2 February** |

**Expected discovery:**

| | |
|---|---|
| CHANGE | Delivery information changed |
| CONFLICT | Progress report and schedule disagree |
| FACT | 2 February is 18 calendar days after the planned 15 January installation date (original plan: 12 Jan delivery is 3 days before installation) |
| POTENTIAL IMPACT | Transformer installation milestone may require investigation |
| VALIDATION | Project-control review required |
| NON-CONCLUSION | No autonomous determination that energization is delayed |

The value proposition tested is **not schedule calculation**; it is **detecting divergence between
project information sources**.

### Scenario B — PCS specification change (primary intelligence scenario)

**Inputs:** PCS specification Rev 7 · PCS specification Rev 8 · PPC specification · grid requirement ·
grid compliance test plan · equipment information (plus distractors).

```
PCS Rev 7 ─► PCS Rev 8            material parameter changed
PPC specification                 still references Rev 7
Grid requirement                  relevant to the changed parameter
Grid compliance test plan         references the PPC specification
```

The relationship **PCS capability → grid requirement** must be **AI-inferred and not seeded**.

The benchmark measures whether GridPulse:

1. discovers the relationship,
2. gets it right,
3. supports it with evidence, and
4. avoids unsupported engineering conclusions (WILL FAIL GRID COMPLIANCE, MUST NOTIFY NETWORK
   OPERATOR, PROTECTION STUDY MUST BE REDONE — unless explicitly supported by the scenario's
   evidence).

## 5. Route A — Practitioner interviews

**Target participants (8–12):** Owner's Engineers · BESS technical project managers ·
project-control professionals · electrical/grid engineers on BESS projects · commissioning
professionals.

**Rules:** ask about the current workflow **first**; do not lead toward GridPulse; show nothing about
GridPulse until the final section; record with `PRACTITIONER_INTERVIEW_TEMPLATE.md`.

**What we need to understand:**

1. what information they actually receive
2. how often they receive it
3. how they detect changes
4. how they investigate cross-disciplinary impacts
5. what tools they use
6. where information is fragmented
7. which investigations consume the most time
8. whether source divergence is common
9. whether technical specification changes cause recurring investigation work
10. what they would trust software to do
11. what they would never trust software to do
12. who would pay

## 6. Route B — Expert timed comparison (crossover, D-048)

The expert does **not** use GridPulse software. The "GridPulse-style investigation bundle" is prepared
by hand, following the output contract in `PHASE_1_ARCHITECTURE.md` §10.4 / §13, and must itself obey
the determination boundary.

**Design — crossover (efficiency measure).** Each expert does two tasks:

| Expert group | Task 1 | Task 2 |
|---|---|---|
| G1 | Scenario A — unassisted | Scenario B — assisted |
| G2 | Scenario B — unassisted | Scenario A — assisted |
| G3 | Scenario A — assisted | Scenario B — unassisted |
| G4 | Scenario B — assisted | Scenario A — unassisted |

Assign experts to groups in rotation so that scenario and order are counterbalanced.

**Unassisted task:**

1. Give the expert the raw document pack (no ground truth, no bundle).
2. Ask them to investigate as they normally would: *what changed, what may it affect, what evidence
   supports that, who needs to look at it?*
3. Measure time (`T_raw`).
4. Record their findings.

**Assisted task (on the other scenario):**

5. Give the raw document pack **and** the GridPulse-style investigation bundle together.
6. Ask them to validate and correct the bundle and produce their answer to the same question.
7. Measure total human time (`T_assisted`): reviewing, correcting, further investigation, evidence
   verification, routing.
8. Record their findings and every correction.

Compare `T_raw` and `T_assisted` per scenario across experts, together with correctness against ground
truth. AI generation time is not the metric. With small samples, report individual results and spread,
not only averages.

**Optional correction/trust observation (not an efficiency measure).** After an unassisted task and
once `T_raw` is recorded, the expert may be shown the bundle for that same scenario to observe what
they correct, reject or add, and whether they trust the evidence chain. This time is recorded
separately and never used in the efficiency comparison.

**Also record:** which bundle items were corrected or rejected; any expert finding absent from the
bundle; perceived trustworthiness of the evidence chain; whether "potential impact — expert validation
required" was useful or too thin.

Recording sheet: `validation/scoring/`.

## 7. Route C — External realism validation

Use legitimate public or anonymised project material (e.g. published grid-connection requirements,
public tender specifications and test procedures, anonymised material provided with permission) to
make the scenario packs realistic and to build the degraded and public-document benchmark tiers.

This is **external realism validation**. It is **not** customer or practitioner validation, and is
never reported as such. Record the source and licence/permission of every external document used.

## 8. Validation pack structure

```
validation/
  README.md
  scenario-a-transformer/
    baseline/          purchase order extract (contractual delivery date)
    changed/           supplier letter — variant runs only
    supporting/        commissioning plan, equipment list, test programme, distractors
    schedule/          schedule updates U11 (period N-1) and U12 (period N)
    progress-report/   EPC progress reports 11 (N-1) and 12 (N — carries the change)
    ground-truth/      expected findings and forbidden conclusions — WITHHELD from investigators
  scenario-b-pcs/
    baseline/          PCS spec Rev 7, PPC spec, grid requirement, test plan
    changed/           PCS spec Rev 8
    supporting/        equipment information, distractors
    schedule/          (optional) relevant milestones
    progress-report/   (optional) the submittal transmittal / report mentioning Rev 8
    ground-truth/      WITHHELD from investigators
  scoring/             scoring rubric, timing and results sheets
  interview/           interview log (no fabricated entries)
```

Ground truth must remain inaccessible to the investigator: distribute investigator packs as
**flattened** copies (files named by document number) **without** `ground-truth/`, this plan, or
`PHASE_1_ARCHITECTURE.md`. Pack status: Scenario A and B documents authored (synthetic);
investigation bundles for Route B not yet prepared.

## 9. Buyer and pricing hypotheses (D-045 — tested in interviews, not decided)

| Hypothesis | Buyer | Why they might pay | Possible pricing unit |
|---|---|---|---|
| H1 | OE / technical-advisory firm | Faster, better-evidenced reviews at fixed fee | Per project per month; per seat |
| H2 | Owner / developer | Earlier visibility of exposure | Per project; per MW under construction |
| H3 | Lender's technical advisor / lender | Evidence-backed construction monitoring | Per monitored project |
| H4 | Services-led start | GridPulse-assisted OE services via a partner firm | Revenue share / service fee |

Willingness-to-pay and willingness-to-pilot are recorded only as stated by real participants.

## 10. Stop / pivot and continue conditions

**STOP or major pivot if:**

- practitioners do not describe cross-disciplinary change investigation as a recurring, meaningful
  workload
- source divergence is rare or unimportant
- technical specification changes rarely require the proposed investigation
- existing tools already provide the required answer with little manual work
- inferred dependencies are too noisy
- review load consumes the saved time
- users only want document search / summarisation
- experts do not trust the evidence chain
- the system requires excessive manual graph construction

**CONTINUE if:**

- practitioners repeatedly describe the workflow as painful
- GridPulse finds cross-source relationships that are otherwise assembled manually
- evidence tracing is substantially faster
- review time is lower than the investigation time saved
- experts trust the evidence trail
- the PCS scenario exposes a meaningful workflow gap
- users repeatedly ask questions that require cross-disciplinary investigation

## 11. Gate outcome and report

The validation report (stored under `validation/`) states, per scenario and per route:

- participants (role and experience only), dates, and what was actually done
- efficiency: `T_raw`, `T_assisted`, reduction, spread, sample size
- quality: every measure in §3.B with **precision and recall shown separately**
- safety: count of unsupported Level 3 conclusions (must be 0), with examples if any
- interview findings against §5 items 1–12, including contrary evidence
- which stop/continue conditions (§10) are met

| Outcome | Condition | Next step |
|---|---|---|
| **Pass** | A, B and C satisfied; continue conditions dominate | Founder approval; fold findings into Phase 1; unblock Phase 2 |
| **Pivot** | Pain confirmed but scenario, intake or output assumptions wrong | Amend decisions and scenarios; repeat Route B |
| **Stop** | Stop conditions dominate | Revisit the product thesis |

## 12. Phase status

| Phase | Status |
|---|---|
| Phase 0 — Product definition | LOCKED |
| Phase 1 — Architecture | ARCHITECTURE REVIEWED — VALIDATION REQUIRED BEFORE IMPLEMENTATION |
| Phase 2 — Implementation | BLOCKED — VALIDATION GATE NOT YET PASSED |
