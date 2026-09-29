> SYNTHETIC VALIDATION DOCUMENT — fictional project "Kestrel Moor BESS". Not a real project, company, standard, grid code or product. All technical values are illustrative.


# Grid Compliance Test Plan

| | |
|---|---|
| Document no. | KMB-EPC-GCT-PLN-004 Rev 1 |
| Date | 20 September 2026 |
| Issued by | EPC Contractor — Grid Compliance Lead |
| Status | For review by the Network Operator |

## 1. Basis

This plan implements compliance testing required by KMB-NO-GCR-001 clause R-20. Control modes and
setpoints are as defined in the PPC Functional Specification KMB-EPC-SPC-PPC-002 Rev 2.

## 2. Test list

| Test | Title | Requirement verified | Stage | Executed through |
|---|---|---|---|---|
| GC-01 | Protection and intertrip verification | Connection Agreement protection schedule | Stage 1 | Protection panels |
| GC-02 | SCADA and PPC signal verification | Connection Agreement Schedule 6 | Stage 1 | RTU-01, PPC-01 |
| GC-03 | Voltage control | R-10 | Stage 2 | PPC-01 |
| GC-04 | Reactive power capability | R-12 | Stage 2 | PPC-01 |
| GC-05 | Frequency response | R-18 | Stage 2 | PPC-01 |
| GC-06 | Fault ride-through verification (by simulation and record review) | R-14 | Stage 2 | — |

## 3. GC-04 Reactive power capability — procedure outline

3.1 With the facility exporting at active power levels of 0 %, 10 %, 25 %, 50 %, 75 % and 100 % of
Registered Capacity, the PPC shall command maximum leading and maximum lagging reactive power.

3.2 At each level, record POC active power, reactive power and voltage for 5 minutes.

3.3 Repeat at 50 % import.

3.4 **Acceptance.** Power factor at the POC within the range stated in R-12 at every test point.

## 4. Test stages and the grid compliance milestone

Acceptance of GC-01 to GC-06 by the Network Operator is required to achieve the grid compliance
milestone in the Connection Agreement.
