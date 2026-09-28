# Validation Packs

Materials for the validation gate defined in `docs/VALIDATION_PLAN.md`. **No application code.**

**Current state:** synthetic scenario documents for Scenarios A and B are authored (realism tier T1
with light T2 degradation). The GridPulse-style investigation bundles for Route B are prepared
(`scenario-a-transformer/investigation-bundle.md`, `scenario-b-pcs/investigation-bundle.md`). They were
prepared manually, not by GridPulse software, and have not been reviewed by any expert. **No
validation run has occurred and no validation evidence exists** — no interviews, timed comparisons or
benchmark runs have been recorded.

Status: Phase 1 — ARCHITECTURE REVIEWED — VALIDATION REQUIRED BEFORE IMPLEMENTATION.
Phase 2 — BLOCKED — VALIDATION GATE NOT YET PASSED.

| Folder | Contents |
|---|---|
| `scenario-a-transformer/` | Scenario A — transformer source divergence (primary validation scenario) |
| `scenario-b-pcs/` | Scenario B — PCS specification change (primary intelligence scenario) |
| `scoring/` | Scoring rubric, timing sheet, results template |
| `interview/` | Interview log and records (real interviews only) |

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
- Investigators must not receive `ground-truth/`, `scoring/`, `docs/VALIDATION_PLAN.md` or
  `docs/PHASE_1_ARCHITECTURE.md` (which contains the scenario definitions).
- The investigation bundle (`investigation-bundle.md`) is given only in the **assisted** task of the
  crossover design, together with the raw documents. It is never included in an unassisted pack.
- Scenario READMEs describe document roles and are never given to investigators.

## Data rules

- Synthetic or public material only (D-015). Every public document records its source and licence in
  the scenario's `supporting/SOURCES.md`.
- Synthetic values are illustrative and must not be presented as any real grid code, standard or
  project.
- Route C material is labelled **External realism validation**, never customer validation.
