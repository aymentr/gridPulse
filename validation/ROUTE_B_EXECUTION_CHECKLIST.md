# Route B Execution Checklist

> **Internal facilitator document. Never give it to participants.**
> Operational checklist only. It does not change the experiment. Where it and
> `docs/VALIDATION_PLAN.md` or `validation/scoring/` differ, those documents govern.

**Terminology.** SOLO = the plan's **unassisted** task (time `T_raw`). ASSISTED = the plan's
**assisted** task (time `T_assisted`). "Expert" and "participant" mean the same person.

## Purpose

Route B is the controlled product-validation experiment (`VALIDATION_PLAN.md` §6). It tests whether the
GridPulse investigation approach can reduce total human investigation effort while maintaining
investigation quality and safety.

Route B results must be interpreted only within the limits documented in `VALIDATION_PLAN.md` §3.1–3.2.
Independent technical-realism review was not performed and is non-blocking (D-051).

---

## A. Before recruiting participants

### Repository

- [ ] Working tree clean before the experiment begins; record the commit hash used for all runs: `______`
- [ ] Benchmark source documents frozen (`scenario-*/baseline|changed|supporting|schedule|progress-report/`)
- [ ] Ground truth frozen (`scenario-*/ground-truth/`)
- [ ] Investigation bundles frozen (`scenario-*/investigation-bundle.md`)
- [ ] Scoring rubric frozen (`scoring/SCORING_RUBRIC.md`)
- [ ] Crossover design frozen (D-048; `VALIDATION_PLAN.md` §6)
- [ ] Participant packs assembled **once** and reused for every participant:
  - Scenario A — standard run: flattened files from `baseline/`, `supporting/`, `schedule/`,
    `progress-report/` (**not** `changed/`; the Scenario A bundle was prepared for the standard run)
  - Scenario B: flattened files from `baseline/`, `changed/`, `supporting/`, `schedule/`,
    `progress-report/`
  - Both: **exclude** `supporting/SOURCES.md`, scenario `README.md`, `investigation-bundle.md`,
    `ground-truth/`
- [ ] No benchmark files modified after participant testing begins

### Participant eligibility

For each participant, record:

- [ ] Participant ID
- [ ] Professional role
- [ ] Relevant project/investigation experience
- [ ] Relevant BESS/grid/project-control experience, if applicable
- [ ] Eligibility confirmed
- [ ] Participant is not the author of the benchmark
- [ ] Participant has not seen the ground truth
- [ ] Participant has not seen the investigation bundles before the relevant assisted run
- [ ] Participant has not reviewed the packs as a technical-realism reviewer (`technical-realism-review/README.md`)

Do not collect unnecessary personal information (no names, employers or project names in records).

---

## B. Participant assignment

Use the existing crossover design (D-048). Assign participants to groups in rotation.

| Group | Task 1 | Task 2 |
|---|---|---|
| G1 | Scenario A — SOLO | Scenario B — ASSISTED |
| G2 | Scenario B — SOLO | Scenario A — ASSISTED |
| G3 | Scenario A — ASSISTED | Scenario B — SOLO |
| G4 | Scenario B — ASSISTED | Scenario A — SOLO |

For each participant record:

- [ ] Participant ID
- [ ] Group (G1–G4)
- [ ] Scenario assigned to SOLO
- [ ] Scenario assigned to ASSISTED
- [ ] Task order recorded
- [ ] Assignment communicated without revealing the intended benchmark change (refer to "Pack 1" / "Pack 2" or document sets, not scenario descriptions)

---

## C. Before each scenario

- [ ] Correct source pack provided (see §A)
- [ ] Correct scenario for this task per the assignment
- [ ] Participant has not seen the ground truth
- [ ] Participant has not seen the investigation bundle for this scenario
- [ ] Task instructions given exactly as in `VALIDATION_PLAN.md` §6: *"What changed, what may it
      affect, what evidence supports that, who needs to look at it?"*
- [ ] Completion rule stated identically to every participant: the task ends when the participant
      declares their answer to that question complete
- [ ] Timing method ready
- [ ] Results capture ready (`scoring/TIMING_AND_RESULTS_SHEET.md`; participant record §J)

Do not explain what the benchmark is expected to find. Give no hints about transformer dates, PCS
revisions, the PPC, grid requirements, inferred relationships, conflicts, critical findings or
expected answers.

---

## D. SOLO run (unassisted, `T_raw`)

**Start**

- [ ] Start timer
- [ ] Record start time

**During the investigation.** The participant investigates using the provided source pack only. Give
no benchmark-specific assistance.

**End.** Stop timing when the participant declares the investigation complete under the completion
rule.

Record:

- [ ] End time
- [ ] Total investigation time (`T_raw`)
- [ ] Participant findings
- [ ] Evidence / citations supplied
- [ ] Identified relationships / dependencies
- [ ] Identified conflicts / disagreements
- [ ] Identified downstream impacts
- [ ] Questions requiring human validation
- [ ] Any conclusions stated by the participant

Do not score the participant during the run in any way that reveals missed findings.

**Optional correction/trust observation** (`VALIDATION_PLAN.md` §6): only after `T_raw` is recorded,
the participant may be shown the bundle for this same scenario. Record that time separately; it is
never used in the efficiency comparison. The participant must not afterwards do an ASSISTED run on this
scenario (the crossover already prevents this).

---

## E. ASSISTED run (`T_assisted`)

Provide the raw source pack **and** the frozen investigation bundle together, exactly as frozen. Do
not modify the bundle for the participant.

- [ ] Start timer
- [ ] Record start time
- [ ] Participant reviews the GridPulse investigation output
- [ ] Participant checks evidence
- [ ] Participant validates / rejects / corrects findings
- [ ] Participant identifies additional issues if necessary

**Timing rule.** `T_assisted` includes all review and correction time. Do not stop the timer because
the bundle has been displayed. The measurement ends only when the participant declares their answer
complete under the completion rule.

Record:

- [ ] End time
- [ ] Total assisted investigation + review/correction time (`T_assisted`)
- [ ] Findings accepted
- [ ] Findings rejected
- [ ] Findings corrected
- [ ] Additional findings discovered
- [ ] Evidence / citation corrections
- [ ] Dependency corrections
- [ ] Conflict corrections
- [ ] Questions requiring human validation
- [ ] Unsupported conclusions, if any
- [ ] Qualitative notes the plan asks for: trust in the evidence chain; whether "potential impact —
      expert validation required" was useful or too thin

---

## F. Post-run scoring

Use the frozen rubric (`scoring/SCORING_RUBRIC.md`) against the scenario's `ground-truth/`. Scoring
happens after the session, never in front of the participant. Do not add metrics during the experiment.
Report precision and recall separately wherever the rubric defines both.

Measures defined by the frozen rubric and results sheet:

| Area | Measure (as defined in the rubric) |
|---|---|
| Efficiency | `T_raw`, `T_assisted`, reduction `(T_raw − T_assisted) / T_raw` — target ≥ 50 %, interpreted with quality and safety |
| Quality | Change detection (precision, recall) |
| | Direct-impact recall, with false positives listed |
| | Secondary-impact recall, with false positives listed |
| | Evidence precision |
| | Stale-evidence detection (precision, recall) |
| | Source-divergence detection (precision, recall) |
| | Entity-resolution accuracy |
| | Inferred-dependency precision (primary), recall reported separately |
| | Reviewer routing |
| | Review load |
| Results sheet | Bundle items corrected / rejected; expert findings not in bundle; CRITICAL items missed (assisted) |
| Safety | Unsupported Level 3 conclusions; inferred-as-fact; intent statements — each must be 0 |

**Critical-finding rule (rubric).** A `CRITICAL` ground-truth item found by the unassisted baseline but
missed in the assisted output is a quality failure for that run, regardless of time saved. Under the
crossover design, the unassisted baseline for a scenario is the SOLO runs of that scenario by other
participants.

**Safety rule.** Unsupported Level 3 conclusions must remain zero.

Do not introduce new thresholds.

---

## G. Participant corrections

Treat corrections as experimental data. Do **not** automatically classify a participant disagreement as
a benchmark error.

For every material correction, record:

| Field | Content |
|---|---|
| Bundle statement | What the GridPulse bundle stated |
| Participant change | What the participant changed |
| Category | evidence · entity matching · change detection · dependency · impact · terminology · interpretation · unsupported conclusion |
| Resolvable from the frozen benchmark? | yes / no / unclear |
| Review after the experiment? | yes / no |

Do not modify the benchmark during the participant session.

---

## H. Safety check (every ASSISTED run)

- [ ] No unsupported Level 3 conclusion
- [ ] No claim of automatic engineering determination
- [ ] No claim of automatic grid-compliance determination
- [ ] No claim that a milestone will definitely be delayed unless directly supported and permitted by
      the frozen benchmark rules
- [ ] Inferred relationships remain clearly identified as inferred / unvalidated where applicable
- [ ] Evidence remains traceable

Record every safety violation. Do not silently edit it away.

---

## I. Scenario integrity check (after each participant)

- [ ] Source documents unchanged (`git diff` against the recorded commit is empty)
- [ ] Ground truth unchanged
- [ ] Investigation bundle unchanged
- [ ] Scoring rubric unchanged
- [ ] Architecture unchanged
- [ ] Validation plan unchanged
- [ ] No benchmark leakage occurred
- [ ] Participant did not receive ground truth
- [ ] Participant did not receive internal validation documentation (this checklist, `VALIDATION_PLAN.md`,
      `validation/README.md`, scenario READMEs, `SOURCES.md`, `technical-realism-review/`, architecture)

If any contamination occurs, stop and document it before continuing.

---

## J. Participant-level result record

Enter each run in `scoring/TIMING_AND_RESULTS_SHEET.md` (one row per run). In addition, keep one
record per participant:

```
Participant ID:
Group (G1–G4):
Role:
Relevant experience:

SOLO
  Scenario:
  Start:
  End:
  Total time (T_raw):

ASSISTED
  Scenario:
  Start:
  End:
  Total time (T_assisted):

SOLO findings:
ASSISTED findings:
Accepted findings:
Rejected findings:
Corrected findings:
Additional findings:
Critical findings missed:
Critical findings correctly identified:
Unsupported Level 3 conclusions:
Evidence corrections:
Dependency corrections:
Conflict corrections:
Participant qualitative observations:
Optional correction/trust observation (time recorded separately, not in T_assisted):
```

No personal identifying information unless necessary and consented to. Never pre-fill, estimate or
invent values.

---

## K. Experiment-level integrity (after all planned participants)

- [ ] All participant records complete
- [ ] All timings complete
- [ ] All corrections recorded
- [ ] All critical findings checked
- [ ] All safety checks completed
- [ ] All contamination checks completed
- [ ] Frozen scoring rubric applied consistently
- [ ] No post-hoc benchmark changes made to improve results

---

## L. Validation conclusion

Do not declare success based on intuition. Evaluate the results against the gate in
`VALIDATION_PLAN.md` §3 and §11. Report individual results and spread, not only averages.

| Dimension | Question |
|---|---|
| Efficiency | Did assisted investigation reduce total investigation time, including review/correction? |
| Quality | Did the assisted workflow preserve the required investigation quality (including the critical-finding rule)? |
| Safety | Were unsupported Level 3 conclusions zero? |

Clearly distinguish:

- observed benchmark result
- benchmark limitation (synthetic scenarios; technical realism not independently validated)
- unresolved real-world validation question
- future validation requirement

Do not claim customer validation, willingness to pay, market validation, real-world workflow
validation, practitioner endorsement or technical certification unless independently supported by
evidence outside this experiment.

`VALIDATION_PLAN.md` §11 also includes interview findings (Route A) and the stop/continue conditions
(§10) in the gate report. State explicitly which of these are available; do not treat missing Route A
evidence as supportive.

---

## M. Final experiment status

The final Route B report ends with exactly one of:

- **VALIDATION GATE PASSED**
- **VALIDATION GATE NOT PASSED**
- **VALIDATION GATE INCONCLUSIVE** — if the evidence is incomplete

The conclusion must reference the predefined gate criteria. No subjective overall score or ranking.

---

**Current status:** Route B — READY FOR EXECUTION (not started). Phase 2 — BLOCKED UNTIL VALIDATION
GATE PASSES.
