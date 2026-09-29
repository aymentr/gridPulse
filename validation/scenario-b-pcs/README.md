# Scenario B — PCS Specification Change

**Role:** primary intelligence scenario. **Value tested:** propagation through links no schedule
contains, and the discovery / determination boundary.
**Status:** documents authored (synthetic; tier T1 with light T2 degradation). Not yet used in any
validation run. Values are illustrative, not a real grid code or product.

## Document manifest

| ID | File | Document | Role in scenario |
|---|---|---|---|
| B-B1 | `baseline/KMB-EPC-SPC-PCS-001_Rev7.md` | PCS specification Rev 7 | Cl. 5.3: ±0.95 PF at PCS terminals across 0–100 %; cl. 6.1 firmware v3.2 |
| B-C1 | `changed/KMB-EPC-SPC-PCS-001_Rev8.md` | PCS specification Rev 8 | **The change**: cl. 5.3 now 20–100 % (below 20 % per Appendix C, not provided); firmware v4.0; cl. 9.2 language (trivial). Revision history says only "General update" |
| B-B2 | `baseline/KMB-EPC-SPC-PPC-002_Rev2.md` | PPC functional specification Rev 2 | Cl. 4.2 references **PCS spec Rev 7, cl. 5.3** — becomes a stale reference |
| B-B3 | `baseline/KMB-NO-GCR-001_Issue3.md` | Grid connection requirements | R-12 (±0.95 PF at POC, 0–100 %); R-30 notification; R-31 models |
| B-B4 | `baseline/KMB-EPC-GCT-PLN-004_Rev1.md` | Grid compliance test plan Rev 1 | GC-04 verifies R-12 via the PPC at 0, 10, 25, 50, 75, 100 %; references PPC spec Rev 2 |
| B-B5 | `baseline/KMB-EPC-SPC-BCN-003_Rev3.md` | Battery container spec Rev 3 | Distractor baseline |
| B-C2 | `changed/KMB-EPC-SPC-BCN-003_Rev4.md` | Battery container spec Rev 4 | **Non-consequential change** (finish colour) on the same transmittal |
| B-R1 | `progress-report/KMB-EPC-TR-0457.md` | Transmittal | Lists Rev 8 "General update" and Rev 4 — changes not described |
| B-S1 | `schedule/KMB-EPC-SCH-U12-milestones.md` | Milestone extract | GC-04 in Stage 2 (2–15 Mar 2027) |
| B-P1 | `supporting/KMB-EPC-EQL-001_Rev4.md` | Equipment list | PCS units, PPC; **no other reactive compensation listed** |
| B-D1 | `supporting/KMB-EPC-SCD-PTL-001_Rev3-extract.md` | SCADA points extract | Distractor |
| B-D2 | `supporting/KMB-DOC-REG-2026-12.md` | Document register extract | Shows PCS Rev 8 current, PPC Rev 2 current |

The relationship **PCS reactive capability → R-12** is stated in no document. It is inferable from
B-B1/B-C1 cl. 5.3, B-B3 R-12 and the absence of other reactive sources in B-P1 (plus the PPC → PCS
reference chain).

## Investigator distribution

Flatten the files in `baseline/`, `changed/`, `supporting/`, `schedule/` and `progress-report/` into
one folder. File names are document numbers. Never include `supporting/SOURCES.md`, this README, `investigation-bundle.md`
(assisted task only) or `ground-truth/`.
