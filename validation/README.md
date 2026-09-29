# Validation Packs

Materials for the validation gate defined in `docs/VALIDATION_PLAN.md`. **No application code.**

**Current state:** synthetic scenario documents for Scenarios A and B are authored (realism tier T1
with light T2 degradation). The GridPulse-style investigation bundles for Route B are prepared
(`scenario-a-transformer/investigation-bundle.md`, `scenario-b-pcs/investigation-bundle.md`). They were
prepared manually, not by GridPulse software, and have not been reviewed by any expert. **No
validation run has occurred and no validation evidence exists** — no interviews, timed comparisons or
benchmark runs have been recorded.

| Item | Status |
|---|---|
| Architecture | ARCHITECTURE REVIEWED |
| Benchmark | BENCHMARK CONSTRUCTED (synthetic) |
| Technical realism | NOT INDEPENDENTLY VALIDATED — see below |
| Product validation | PENDING — **Route B unblocked** (D-051), not yet run |
| Phase 2 | BLOCKED UNTIL VALIDATION GATE IS PASSED |

| Folder | Contents |
|---|---|
| `scenario-a-transformer/` | Scenario A — transformer source divergence (primary validation scenario) |
| `scenario-b-pcs/` | Scenario B — PCS specification change (primary intelligence scenario) |
| `scoring/` | Scoring rubric, timing sheet, results template |
| `interview/` | Interview log and records (real interviews only) |
| `technical-realism-review/` | Blind reviewer pack and blank report forms — NOT PERFORMED, optional follow-up |

Each scenario folder:

| Subfolder | Purpose |
|---|---|
| `baseline/` | Information as it stood before the change (period N-1 / earlier revisions) |
| `changed/` | Information carrying the change (period N / new revision) |
| `supporting/` | Context documents and distractors |
| `schedule/` | Schedule updates or milestone information |
| `progress-report/` | EPC progress reports / submittal transmittals |
| `ground-truth/` | Expected findings, labels and forbidden conclusions — **withheld from investigators** |

## Access rules

- Investigator packs are distributed as **flattened** copies (one folder, files named by document
  number) so folder names such as `baseline/` or `changed/` do not reveal where the change is. See each
  scenario README for which folders to include.
- Investigators must not receive `ground-truth/`, `scoring/`, `docs/VALIDATION_PLAN.md`,
  `docs/PHASE_1_ARCHITECTURE.md` (which contains the scenario definitions), this README, or anything in
  `technical-realism-review/`.
- The investigation bundle (`investigation-bundle.md`) is given only in the **assisted** task of the
  crossover design, together with the raw documents. It is never included in an unassisted pack.
- Scenario READMEs and each `supporting/SOURCES.md` describe document roles or test design and are
  never given to investigators or to the technical realism reviewer.
- **Technical realism review: NOT PERFORMED — optional, non-blocking** (D-051). See
  `technical-realism-review/README.md`. If a review happens later, that reviewer does not take part in
  Route B.

## Independent Technical Realism Review — limitation

Independent BESS/grid practitioner review was sought but was not obtained before Route B. Candidate
sources and outreach material were prepared (`technical-realism-review/OUTREACH.md`); no outreach is
recorded there and no review took place.

The scenarios therefore remain **synthetic** benchmark scenarios whose technical and workflow realism
has **not been independently validated**.

This does not prevent the controlled benchmark from being executed. However, benchmark results must be
interpreted narrowly: they measure GridPulse-style investigation performance against the constructed
scenarios and their defined ground truth. They do not establish that the scenarios are representative
of real-world BESS projects.

No reviewer approval, practitioner endorsement or external technical validation is claimed.

Open technical-realism questions (not confirmed errors; scenarios deliberately left unchanged) are
listed in `technical-realism-review/README.md`. That file is internal and never given to investigators.

The product-validation requirements are unchanged and remain mandatory: zero unsupported Level 3
conclusions; critical findings cannot be silently missed; evidence remains traceable; inferred
dependencies remain distinguishable from confirmed ones; human review remains authoritative; review
and correction time counts toward total investigation time.

## Data rules

- Synthetic or public material only (D-015). Every public document records its source and licence in
  the scenario's `supporting/SOURCES.md`.
- Synthetic values are illustrative and must not be presented as any real grid code, standard or
  project.
- Route C material is labelled **External realism validation**, never customer validation.
