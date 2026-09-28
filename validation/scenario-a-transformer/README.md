# Scenario A — Transformer Source Divergence

**Role:** primary validation scenario. **Value tested:** detecting divergence between project
information sources — *not* schedule calculation.
**Status:** specification only — documents not yet authored.

## Canonical facts (D-032) — for pack authors only

| Item | Value |
|---|---|
| Transformer delivery (schedule, periods N-1 and N) | 12 January |
| Transformer installation (planned) | 15 January |
| HV commissioning | 10 February |
| Grid compliance testing | 20 February |
| Energization | 1 March |
| Progress report, period N | "the supplier has advised a revised delivery date of 2 February" |

## Planned document manifest

| ID | Folder | Document | Key content | Notes |
|---|---|---|---|---|
| A-B1 | baseline | EPC progress report, period N-1 | Transformer delivery on track for 12 Jan | |
| A-B2 | baseline | Purchase order extract (main transformer) | Delivery 12 Jan; equipment ID TX-01 | Uses a different equipment name than the report |
| A-S1 | schedule | Schedule update, period N-1 | Delivery 12 Jan; installation 15 Jan; logic link delivery → installation | Tabular export |
| A-S2 | schedule | Schedule update, period N | **Unchanged**: delivery 12 Jan; installation 15 Jan | The divergence |
| A-C1 | progress-report | EPC progress report, period N | "Main transformer: supplier has advised revised delivery date of 2 February" | Buried among other items |
| A-C2 | changed | Supplier letter copied to owner (optional variant) | "Transformer delivery is now expected February 2" | Use in variant runs only |
| A-P1 | supporting | Commissioning plan | "HV commissioning shall commence once all HV equipment is installed" | Source of the inferable link — must NOT name the transformer |
| A-P2 | supporting | Equipment list | Classes TX-01 ("132/33 kV main power transformer") as HV equipment | Alias variation |
| A-P3 | supporting | Grid-connection test programme | HV commissioning → grid compliance testing; energization dates | |
| A-D* | supporting | Distractors | Unrelated progress items, other equipment deliveries, minutes | 5–10 documents |

Target pack size: ~15–30 documents including distractors.
