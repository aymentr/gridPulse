# Route B Assignment Mechanism (D-048)

> Internal. **Do not assign participants until the experiment is explicitly started.**

## Internal mapping — never disclose

| Participant-facing name | Scenario |
|---|---|
| `participant-materials/set-1/` (14 files) | Scenario A — standard run (no `changed/` supplier letter) |
| `participant-materials/set-2/` (12 files) | Scenario B |
| `participant-materials/assisted/bundle-set-1.md` | Scenario A investigation bundle (byte-identical copy) |
| `participant-materials/assisted/bundle-set-2.md` | Scenario B investigation bundle (byte-identical copy) |

The `set-1`/`set-2` names are deliberately different from the realism-review `pack-1`/`pack-2`, whose
Pack 1 also contains the supplier-letter variant.

## Rotation

Assign in order of confirmed enrolment, cycling G1 → G2 → G3 → G4 → G1 …

| Group | Task 1 | Task 2 |
|---|---|---|
| G1 | Set 1 — documents only (SOLO) | Set 2 — with bundle (ASSISTED) |
| G2 | Set 2 — documents only (SOLO) | Set 1 — with bundle (ASSISTED) |
| G3 | Set 1 — with bundle (ASSISTED) | Set 2 — documents only (SOLO) |
| G4 | Set 2 — with bundle (ASSISTED) | Set 1 — documents only (SOLO) |

Each completed cycle of four participants covers every scenario × condition × order combination once.
The validation plan does not define a Route B sample size; this is a property of the design, not a
statistical requirement, and the sample is not representative of any population.

## Assignment log

| Enrolment # | Candidate ID | Participant code | Group | Date assigned |
|---|---|---|---|---|

*No assignments.*

## Hand-out rules

- Task instructions (`participant-materials/TASK_INSTRUCTIONS.md`) at the start.
- For each task, hand out **only** that task's set; the bundle only at the start of the ASSISTED task.
- Never hand out the whole `participant-materials/` folder at once.
- Run each session with `validation/ROUTE_B_EXECUTION_CHECKLIST.md`.
