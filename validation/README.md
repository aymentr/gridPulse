# Validation Packs

Materials for the validation gate defined in `docs/VALIDATION_PLAN.md`. **No application code.**

**Current state:** structure and specifications only. The scenario documents have **not** been
authored yet, and **no validation evidence exists** — no interviews, timed comparisons or benchmark
results have been recorded.

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

- Investigator packs are distributed as copies containing **only** `baseline/`, `changed/`,
  `supporting/`, `schedule/` and `progress-report/`.
- Investigators must not receive `ground-truth/`, `scoring/`, `docs/VALIDATION_PLAN.md` or
  `docs/PHASE_1_ARCHITECTURE.md` (which contains the scenario definitions).
- The GridPulse-style investigation bundle for Route B is handed over only at step 5 of the protocol.

## Data rules

- Synthetic or public material only (D-015). Every public document records its source and licence in
  the scenario's `supporting/SOURCES.md`.
- Synthetic values are illustrative and must not be presented as any real grid code, standard or
  project.
- Route C material is labelled **External realism validation**, never customer validation.
