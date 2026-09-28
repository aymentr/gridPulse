# Scenario A — Transformer Source Divergence

**Role:** primary validation scenario. **Value tested:** detecting divergence between project
information sources — *not* schedule calculation.
**Status:** documents authored (synthetic; tier T1 with light T2 degradation). Not yet used in any
validation run.

## Canonical facts (D-032) — for pack authors only

| Item | Value | Where stated |
|---|---|---|
| Transformer delivery | 12 Jan 2027 | Schedule U11 and U12 (A1000); PO; progress report 11 |
| Transformer installation (planned) | 15 Jan 2027 | Schedule U11 and U12 (A1010) |
| HV commissioning | 10 Feb 2027 | Schedule (A1100); progress reports |
| Stage 1 grid compliance tests (pre-energization) | 20 Feb 2027 | Schedule (A1200); test programme |
| Energization | 1 Mar 2027 | Schedule (A1300); progress reports; test programme |
| Reported new delivery | 2 Feb 2027 | Progress report 12 (procurement table only); supplier letter (variant) |

Design note: to keep dates consistent with electrical practice, "grid compliance testing" on 20 Feb
is **Stage 1 pre-energization verification**; on-load compliance tests (Stage 2) follow energization.

## Document manifest

| ID | File | Document | Role in scenario |
|---|---|---|---|
| A-R1 | `progress-report/KMB-EPC-PR-0011.md` | Progress report 11 (period N-1) | Baseline: transformer delivery on track for 12 Jan |
| A-R2 | `progress-report/KMB-EPC-PR-0012.md` | Progress report 12 (period N) | **Carries the change**, only in the procurement table; executive summary silent; states energization "maintained"; also mentions PCS Rev 8 (out of scope here) |
| A-S1 | `schedule/KMB-EPC-SCH-U11.csv` | Schedule update U11 | Baseline dates and logic |
| A-S2 | `schedule/KMB-EPC-SCH-U12.csv` | Schedule update U12 | **Unchanged** transformer dates — the divergence; no logic link from A1010 to A1100 |
| A-B1 | `baseline/KMB-PO-0042-extract.md` | Purchase order extract | Contractual delivery 12 Jan; tag TX-01 and full equipment description |
| A-C1 | `changed/KMB-SUP-T-LTR-0107.md` | Supplier letter (cc Owner) | **Variant runs only** — direct supplier statement of 2 Feb with a reason |
| A-P1 | `supporting/KMB-EPC-COM-PLN-001_Rev1.md` | Commissioning plan | "HV commissioning shall commence once all HV equipment is installed…" — does not name the transformer |
| A-P2 | `supporting/KMB-EPC-EQL-001_Rev4.md` | Equipment list | Classes TX-01 as HV; AUX-TX-02 as MV |
| A-P3 | `supporting/KMB-EPC-GCT-PRG-001_Rev0.md` | Grid connection test programme | Stage 1 after HV commissioning; energization subject to Stage 1 acceptance |
| A-D1 | `supporting/KMB-MIN-PM-0012.md` | Progress meeting minutes (3 Dec) | Distractor; predates the change |
| A-D2 | `supporting/KMB-SUP-A-LTR-0031.md` | Auxiliary transformer supplier letter | **Near-miss distractor**: a different transformer, same 12 Jan date, unchanged |
| A-D3 | `supporting/KMB-SUP-B-SHN-0219.md` | Battery container shipment notice | Distractor |
| A-D4 | `supporting/KMB-EPC-RFI-0088.md` | RFI — drainage | Distractor |
| A-D5 | `supporting/KMB-SUP-C-DN-0077.md` | 33 kV cable delivery note | Distractor |
| A-D6 | `supporting/KMB-DOC-REG-2026-12.md` | Document register extract | Context |

Aliases used for the main transformer: "Main power transformer", "Main transformer (T1)", "TX-01",
"132/33 kV main power transformer", "132/33 kV, 120 MVA … power transformer".

## Investigator distribution

Standard run: flatten all files **except** `changed/` and `ground-truth/` into one folder (file names
are document numbers and do not reveal roles). Variant run: additionally include `changed/`.
