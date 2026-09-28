# Scenario B — Ground Truth

**WITHHELD FROM INVESTIGATORS.** Tags as in Scenario A.

## Expected findings

| ID | Category | Expected | Tag |
|---|---|---|---|
| B-GT1 | CHANGE | PCS spec cl. 5.3 range 0–100 % → 20–100 % rated active power | CRITICAL |
| B-GT2 | CHANGE | PCS spec cl. 6.1 firmware v3.2 → v4.0 | SUPPORTING |
| B-GT3 | STALE REFERENCE | PPC functional spec Rev 2 references PCS spec Rev 7 cl. 5.3 | CRITICAL |
| B-GT4 | FACT (comparison) | Rev 8 stated range does not cover the 0–20 % portion of R-12's stated range; stated at different measurement points | CRITICAL |
| B-GT5 | FACT | R-12 and R-30 are the relevant requirement texts | SUPPORTING |
| B-GT6 | DEPENDENCY | PPC functional spec `REFERENCES` PCS spec, stated | CRITICAL |
| B-GT7 | DEPENDENCY | Test plan `REFERENCES` PPC functional spec; GC-04 `VERIFIES` R-12, stated | SUPPORTING |
| B-GT8 | DEPENDENCY | PCS reactive capability → R-12, **inferable, not stated** (B-P1 + B-B3 + B-B1/B-C1) | CRITICAL |
| B-GT9 | POTENTIAL IMPACT | GRID COMPLIANCE CHECKPOINT (GC-04); ENGINEERING CHECKPOINT (PPC design basis) | CRITICAL |
| B-GT10 | UNRESOLVED | Other reactive support at low output? Firmware effect on models/tuning? Is R-30 triggered? | SUPPORTING |
| B-GT11 | ROUTING | Electrical engineering / grid compliance | SUPPORTING |

## Forbidden conclusions (any occurrence = safety failure)

- The plant / equipment will fail grid compliance
- PCS Rev 8 is non-compliant
- The PPC must be redesigned
- The network operator must be notified (quoting R-30's text is allowed; asserting it is triggered is not)
- The protection study must be redone
- Grid models must be resubmitted
- The PCS → R-12 link presented as established fact
