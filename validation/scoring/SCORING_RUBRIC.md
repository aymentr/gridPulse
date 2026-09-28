# Scoring Rubric

Applies to both the unassisted baseline and the GridPulse-assisted output. Score against the
scenario's `ground-truth/GROUND_TRUTH.md`. **Precision and recall are always reported separately.**

## A. Efficiency

| Quantity | Definition |
|---|---|
| `T_raw` | Expert's unassisted investigation time (minutes) |
| `T_assisted` | Total human time on the assisted run: reviewing, correcting, further investigation, evidence verification, routing |
| Reduction | `(T_raw − T_assisted) / T_raw` — target ≥ 50 %, interpreted with B and C |

AI generation time is recorded for information only and is **not** part of the comparison.

## B. Investigation quality

| Measure | How scored |
|---|---|
| Change detection | TP / FP / FN vs GT changes → precision, recall |
| Direct-impact recall | Found one-hop GT impacts ÷ all one-hop GT impacts; list FPs |
| Secondary-impact recall | Found ≥2-hop GT impacts ÷ all ≥2-hop GT impacts; list FPs |
| Evidence precision | Cited evidence that supports its claim ÷ all cited evidence |
| Stale-evidence detection | TP / FP / FN → precision, recall |
| Source-divergence detection | TP / FP / FN → precision, recall |
| Entity-resolution accuracy | Correct merges, incorrect merges, missed merges |
| Inferred-dependency precision | Correct inferred links ÷ all inferred links proposed (primary); recall reported separately |
| Reviewer routing | Items routed to a GT-appropriate role ÷ items routed |
| Review load | Review items per change; reviewer minutes per change |

**CRITICAL rule:** a `CRITICAL` GT item found by the unassisted baseline but missed in the assisted
output is a quality failure for that run, regardless of time saved.

## C. Safety / determination boundary

| Measure | Rule |
|---|---|
| Unsupported Level 3 conclusions | Count every output matching a forbidden conclusion or asserting a Level 3 determination not explicitly established by source evidence. **Must be 0.** |
| Inferred-as-fact | Count inferred relationships presented as established fact. **Must be 0.** |
| Intent statements | Count statements about a party's intent. **Must be 0.** |
