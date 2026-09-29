# Technical Realism Review — Instructions for the Reviewer

Thank you for reviewing these documents.

## What you are reviewing

Two packs of **synthetic** project documents for a fictional battery energy storage project
("Kestrel Moor BESS", 100 MW / 400 MWh). The companies, values and requirements are invented.

- `pack-1/` — 15 documents
- `pack-2/` — 12 documents

## The question

> **Could a practitioner reasonably encounter a project-information package resembling this in a
> real BESS / grid-connected infrastructure project?**

The question is **not** whether every detail matches how your own projects work. Organizations differ
in naming conventions, reporting structures, schedule conventions, specifications, approval workflows
and terminology. Please record such differences as **observations**, not defects.

The packs are not expected to be perfectly consistent. Inconsistencies between documents are a normal
feature of real project information. Where you see one, please assess whether it is a **plausible**
inconsistency, not whether it should be removed.

## Please do not

- rewrite or edit the documents;
- remove contradictions, add missing information or resolve ambiguities;
- try to improve or simplify the packs;
- assess any software product, business or commercial question.

Please only report what you find, using the report forms `scenario-a-review.md` (for `pack-1/`) and
`scenario-b-review.md` (for `pack-2/`).

## Review dimensions

| | Dimension | What to look for |
|---|---|---|
| A | Technical plausibility | Impossible configurations; contradictory engineering assumptions; implausible equipment relationships; nonsensical requirements; unrealistic commissioning/testing sequences; unrealistic PCS/grid interactions |
| B | Project-control plausibility | Whether the progress reports, schedules, procurement tables, equipment lists, commissioning plans, test plans, specifications, transmittals, revision histories and meeting/reporting structures could plausibly exist |
| C | Information-flow realism | Information in an unexpected document; duplication; stale references; inconsistent revisions; conflicting dates; terminology variation; information present in one document and absent from another |
| D | Naming realism | Whether naming variation for equipment, suppliers and abbreviations is plausible and recoverable |
| E | Schedule realism | Date formats; durations; working-day / calendar-day conventions; sequencing; commissioning timing; procurement-to-installation relationships; testing stages |
| F | Electrical / grid realism | PCS operating ranges; reactive power requirements; PPC references; grid requirements; test points; firmware revisions; compliance-testing concepts; relationship between equipment capability and point-of-connection requirements |
| G | Document realism | Headings; language; information density; convenient placement of facts; revision descriptions; tables; cross-references |

For electrical/grid points, please distinguish between what is (1) technically plausible,
(2) explicitly documented, and (3) something that would require engineering verification. You are
**not** asked to determine whether any requirement or test would pass or fail.

## Severity

| Severity | Meaning |
|---|---|
| **CRITICAL** | Makes the pack materially unrealistic or unusable as a realistic project-information package |
| **MAJOR** | Substantially reduces realism, or could cause a practitioner to reject the pack |
| **MINOR** | Noticeable, but does not materially affect realism |
| **OBSERVATION** | Differs from your experience but is not necessarily incorrect |

Please avoid "pass/fail" for individual details unless you consider a pack genuinely unusable.

## How to record an issue

For every issue, please separate what the document says from your judgement:

| Field | Content |
|---|---|
| Document | Document number |
| Location | Section / table / row |
| Observed | What the document actually says |
| Reviewer interpretation | Why you consider it potentially unrealistic |
| Severity | CRITICAL / MAJOR / MINOR / OBSERVATION |
| Confidence | High / Medium / Low |
| Suggested correction | If any |

## Confidentiality

Please do not include your name, employer, project names or any client information in the forms.
