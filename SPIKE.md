# Phase 1.5 Technical Spike (D-052)

**Status:** in progress. Phase 2 remains **BLOCKED — VALIDATION GATE NOT PASSED**. This spike is not
Phase 2 and not a product build.

**Question under test:** can fragmented project documents be turned into a defensible,
evidence-backed investigation — without unsupported engineering determinations?

## Scope

`documents → ingestion → document version → evidence → claims → change / conflict detection →
entity resolution → dependency graph → impact investigation → investigation bundle → review queue`,
for the two synthetic Kestrel Moor BESS scenarios in `validation/`. No UI, integrations, auth,
persistence, chat or SaaS features.

## Stack (spike only)

Python 3.11 standard library; in-memory store with an append-only audit log; `unittest`. No
third-party dependencies. Reversible; not the Phase 2 stack decision.

## Layout

| Module | Architecture concept |
|---|---|
| `src/gridpulse/model.py` | Document, DocumentVersion, Location, Evidence, Entity, EntityAlias, Claim, Dependency, Finding, Change, Conflict, Calculation, Review |
| `store.py` | In-memory store + audit log |
| `ingest.py` | Intake → immutable DocumentVersion; benchmark-isolation guard |
| `evidence.py` | Citation creation and mechanical verification; freshness |
| `extract.py` | Deterministic extraction of claims, entities, explicit relationships |
| `entities.py` | Entity resolution (tag / recorded alias only; no fuzzy merges) |
| `changes.py` | Change, Conflict and stale-reference detection |
| `calc.py` | Deterministic calculations with inputs and provenance |
| `inference.py` | Proposer interface + evidence-verified application (INFERRED · UNVALIDATED only) |
| `graph.py` | Typed dependency traversal (REJECTED never traversed) |
| `investigation.py` | Impact investigation → bundle (D-037 section structure) |
| `safety.py` | Level-3 conclusion guard |
| `review.py` | Review queue: CONFIRM / REJECT / REQUEST_INVESTIGATION / EDIT_FINDING |
| `cli.py` | `python -m gridpulse run <scenario-dir>` |

## Run

```
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m gridpulse run validation/scenario-a-transformer --standard-a   # standard run
PYTHONPATH=src python3 -m gridpulse run validation/scenario-a-transformer                # variant (with changed/)
PYTHONPATH=src python3 -m gridpulse run validation/scenario-b-pcs
```

## Known limitations (read before interpreting any output)

1. **No AI model is connected.** The inference step uses `HeuristicProposer`, a rule-based stand-in
   behind the `Proposer` interface. Its rules were written by the author of the benchmark, so its
   output on these scenarios is **not evidence** that GridPulse can infer dependencies. A real model
   must be plugged into the same interface before any benchmark evaluation.
2. **Extraction is deterministic and format-specific.** Parsers read the synthetic Markdown/CSV
   formats (tables, numbered clauses). They stand in for AI-assisted extraction and will not
   generalise to real documents.
3. Synthetic scenarios only; technical realism not independently validated (D-051).
4. Production code never reads `ground-truth/`; tests read it only to check forbidden conclusions.
5. **Observed gaps, not fixed by special-casing:**
   - Scenario B: the missing Appendix C capability curve (referenced by PCS Rev 8 cl. 5.3) is not
     raised as MISSING_EVIDENCE.
   - Scenario A: the progress-report statement that energization is maintained is not extracted as
     an observed claim.
   - The stand-in also proposes PCS → R-14 (clause 5.4, unchanged). It is INFERRED · UNVALIDATED
     and sits in the review queue for a reviewer to accept or reject.
6. The CSV schedule's `#` comment line is shown as the evidence "section" (cosmetic).

## Status

Scenario A (standard and variant) and Scenario B run end to end; 50 tests pass. The tests include
checks that no bundle states any forbidden conclusion listed in the frozen ground truth. **This is a
technical spike. It does not change the validation gate: Phase 2 remains BLOCKED — VALIDATION GATE
NOT PASSED.**
