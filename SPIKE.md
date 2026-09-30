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
| `inference.py` | Evidence-verified application of AI proposals (INFERRED · UNVALIDATED only); rule-based stand-in |
| `providers/` | Provider-agnostic LLM boundary (§1): `LLMProvider`, `MockProvider`, `AnthropicProvider`, config, trace |
| `prompts/` | Versioned prompt templates (`*_v1.md`); version recorded on every proposal |
| `graph.py` | Typed dependency traversal (REJECTED never traversed) |
| `investigation.py` | Impact investigation → bundle (D-037 section structure) |
| `safety.py` | Level-3 conclusion guard |
| `review.py` | Review queue: CONFIRM / REJECT / REQUEST_INVESTIGATION / EDIT_FINDING |
| `cli.py` | `python -m gridpulse run <scenario-dir> [--provider mock\|anthropic]` |

## Run

```
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m gridpulse run validation/scenario-a-transformer --standard-a   # standard run
PYTHONPATH=src python3 -m gridpulse run validation/scenario-a-transformer                # variant (with changed/)
PYTHONPATH=src python3 -m gridpulse run validation/scenario-b-pcs
```

## Milestone 2 — real LLM integration (provider-agnostic)

The rule-based AI stand-in is now behind a provider-agnostic boundary (`src/gridpulse/providers/`).
The core rule is enforced by construction: **LLMs propose; deterministic code verifies, calculates
and traverses; humans validate.**

- `LLMProvider` has three proposal operations — `propose_entity_links` (resolution, §5),
  `interpret_change_links` (semantic claim identity, §6; value comparison stays deterministic),
  `propose_dependencies` (inference, §7). The pipeline routes all three through it.
- `MockProvider` runs the whole pipeline and test-suite offline (no key). `AnthropicProvider` calls
  Claude with structured JSON output; the SDK is imported lazily and a client can be injected.
- Configuration is by environment (`GRIDPULSE_LLM_PROVIDER`, `GRIDPULSE_LLM_MODEL`,
  `ANTHROPIC_API_KEY`). Selecting the real provider without a key fails clearly; no key is needed
  for the deterministic tests. Secrets are never stored.
- The trust boundary is deterministic and backend-owned: every citation is re-verified against the
  document (fabricated evidence rejected); proposals carry no validation/confidence/level the model
  can set; reasoning containing Level-3 wording is rejected; accepted dependencies can only ever be
  `INFERRED · UNVALIDATED · AI_INFERRED`; entity links become UNVALIDATED aliases and never merge
  two entities; change links are corroborated against deterministic detection and never create a
  change. Confirmation requires a human review.
- Every AI invocation is traced (`store.ai_invocations`): provider, model, prompt template+version,
  input document versions, output, evidence refs, accepted/rejected, latency, tokens, cost.

```
GRIDPULSE_LLM_PROVIDER=anthropic ANTHROPIC_API_KEY=… \
  PYTHONPATH=src python3 -m gridpulse run validation/scenario-a-transformer --standard-a
```

## Known limitations (read before interpreting any output)

1. **The real LLM has not been executed, and its inference is not validated.** With no API key in
   this environment the runs above use `MockProvider`, whose dependency rules are the benchmark
   author's rule-based stand-in — **not evidence** that GridPulse can extract or infer with an AI
   model. The `AnthropicProvider` is implemented and unit-tested against a fake client, and the
   pipeline runs end-to-end through it, but a real model run against the scenarios is still
   outstanding. A green software test is an ENGINEERING result, not a VALIDATION result.
2. **Extraction is deterministic and format-specific.** Parsers read the synthetic Markdown/CSV
   formats (tables, numbered clauses). They seed canonical entities and directly-stated claims
   (structured import); the provider adds the semantic proposal layer on top. The parsers will not
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

Scenario A (standard and variant) and Scenario B run end to end through the provider abstraction
with `MockProvider`; 79 tests pass. The tests include the AI trust boundary (fabricated evidence,
attempted CONFIRMED, Level-3 reasoning, inferred-stays-UNVALIDATED, provider switching, trace and
prompt-version metadata) and checks that no bundle states any forbidden conclusion listed in the
frozen ground truth. The real model was **not** executed (no API key in this environment). **This is
a technical spike. It does not change the validation gate: Phase 2 remains BLOCKED — VALIDATION GATE
NOT PASSED.** A passing software test is not validation of the GridPulse hypothesis.
