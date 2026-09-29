# GridPulse Investigation Bundle — Main Transformer Delivery Information

> Illustrative GridPulse-style investigation output, prepared manually from the supplied project
> documents for validation purposes. It was not produced by GridPulse software.
> All project content is synthetic (fictional project "Kestrel Moor BESS").

| | |
|---|---|
| Project | Kestrel Moor BESS (100 MW / 400 MWh) |
| Initiated by | New reporting-period information: progress report KMB-EPC-PR-0012 and schedule update KMB-EPC-SCH-U12 |
| Investigation type | Impact investigation (pre-review) |
| Review status | **PRE-REVIEW** — no finding, claim or relationship in this bundle has been reviewed by a human. Validated information: **none**. |

---

## 0. Reviewer summary

1. **Source divergence.** Progress report 12 states that the supplier has advised a revised delivery
   date of **2 February 2027** for the main transformer (TX-01). Schedule update U12, with a data date
   in the same reporting period, still shows TX-01 delivery on **12 January 2027**.
2. **Relative to the plan.** 2 February 2027 is **18 calendar days after** the planned start of TX-01
   installation (15 January 2027) and **5 calendar days after** its planned finish (28 January 2027).
3. **Possible dependency.** The commissioning plan requires all HV equipment to be installed before HV
   commissioning; the equipment list classes TX-01 as HV equipment. The schedule contains no logic link
   from TX-01 installation to HV commissioning. The link is **inferred**, not stated.
4. **Reporting consistency.** The executive summary and programme section of progress report 12 do not
   mention the revised date; the programme section states that the 1 March 2027 energization date is
   maintained.
5. **Requires review:** Project Controls, Procurement, Commissioning Engineer, Owner's Engineer.

This bundle does **not** establish that any milestone will move. See §6.

---

## 1. Documents processed

| Document no. | Title | Rev / date | Used for |
|---|---|---|---|
| KMB-EPC-PR-0011 | Monthly Progress Report No. 11 | Rev 0, issued 25 Nov 2026 | Previous-period observations |
| KMB-EPC-PR-0012 | Monthly Progress Report No. 12 | Rev 0, issued 22 Dec 2026 | Current-period observations |
| KMB-EPC-SCH-U11 | Schedule update | Data date 20 Nov 2026 | Previous-period dates and logic |
| KMB-EPC-SCH-U12 | Schedule update | Data date 18 Dec 2026 | Current-period dates and logic |
| KMB-PO-0042 | Purchase Order — extract | Rev 1, 14 Mar 2026 | Contractual delivery date; equipment description |
| KMB-EPC-COM-PLN-001 | Commissioning Plan — extract | Rev 1, 2 Sep 2026 | HV commissioning preconditions |
| KMB-EPC-EQL-001 | Equipment List | Rev 4, 30 Oct 2026 | Equipment tags and voltage classes |
| KMB-EPC-GCT-PRG-001 | Grid Connection Test Programme | Rev 0, 16 Oct 2026 | Stage 1 / energization preconditions |
| KMB-MIN-PM-0012 | Progress Meeting No. 12 minutes | 3 Dec 2026 | Earlier status; open actions |
| KMB-SUP-A-LTR-0031 | Auxiliary transformer supplier letter | 10 Dec 2026 | Entity disambiguation |
| KMB-SUP-B-SHN-0219, KMB-EPC-RFI-0088, KMB-SUP-C-DN-0077 | Shipment notice; RFI; delivery note | Dec 2026 / Nov 2026 | Reviewed; no relationship to this investigation identified |
| KMB-DOC-REG-2026-12 | Document register extract | Status at 18 Dec 2026 | Current revisions |

**Legend.** Level 1 = fact (directly supported or deterministically calculated). Level 2 =
relationship or inference. Evidence confidence: HIGH / MEDIUM / LOW. Relationship confidence:
EXPLICIT / INFERRED. Validation: UNVALIDATED / CONFIRMED / REJECTED. All items in this bundle are
UNVALIDATED.

---

## 2. Findings

### F-A1 — CHANGE: main transformer delivery information changed between reporting periods

| | |
|---|---|
| Level | 1 — Fact |
| Potential event | `DELIVERY_DATE_CHANGE` — status: DETECTED → UNDER_REVIEW |
| Affected entity | TX-01, main power transformer (see F-A3) |
| Old observation | 12 January 2027 |
| New observation | 2 February 2027 |
| Evidence confidence | HIGH (explicit statements in both reports) |
| Validation | UNVALIDATED |

**Evidence A (previous period)**
Document: KMB-EPC-PR-0011 — Monthly Progress Report No. 11
Location: §4 Procurement and deliveries, row "Main power transformer / TX-01"
Observation: "FAT completed 18 Nov 2026. Delivery on track" — planned delivery "12 Jan 2027".
Also §6 Programme, key dates table: "Main transformer delivery | 12 Jan 2027".

**Evidence B (current period)**
Document: KMB-EPC-PR-0012 — Monthly Progress Report No. 12
Location: §4 Procurement and deliveries, row "Main transformer (T1) / TX-01"
Observation: "The supplier has advised a revised delivery date of 2 February 2027. Contractor
reviewing with supplier." Planned delivery column: "See status".

**Interpretation.** The EPC Contractor's report for period 12 records a supplier advice of a revised
delivery date. The report attributes the date to the supplier and states that the Contractor is
reviewing it. The supplier communication itself is not among the supplied documents (see F-A8).

**Recommended reviewer:** Procurement; Project Controls.
Reason: the status of the supplier advice, and whether it changes the operative delivery date, is a
procurement and programme matter.

---

### F-A2 — CONFLICT: progress report and schedule update disagree on TX-01 delivery for the same period

| | |
|---|---|
| Level | 1 — Fact (both observations evidenced) |
| Finding type | CONFLICT — source divergence |
| Affected entity | TX-01 delivery (schedule activity A1000) |
| Evidence confidence | HIGH for both observations |
| Validation | UNVALIDATED |

**Evidence A**
Document: KMB-EPC-PR-0012 — Monthly Progress Report No. 12 (reporting period 21 Nov – 18 Dec 2026)
Location: §4, row "Main transformer (T1) / TX-01"
Observation: revised delivery date of 2 February 2027 advised by the supplier.

**Evidence B**
Document: KMB-EPC-SCH-U12 — Schedule update, data date 18 Dec 2026
Location: activity A1000 "Main power transformer TX-01 delivery to site"
Observation: finish 12-Jan-27; status "Not started".

**Evidence C (contractual reference, for context)**
Document: KMB-PO-0042 — Purchase Order extract
Location: Schedule 2 — Delivery, item 1
Observation: delivery date "12 January 2027".

**Interpretation.** The supplied documents contain divergent observations for the same reporting
period. The schedule update was attached to the same progress report (KMB-EPC-PR-0012 §6). The
documents do not establish which date is currently operative, whether the schedule update was prepared
before the supplier advice was received, or whether the purchase order delivery date has been
amended. GridPulse has not selected either source as authoritative.

**Recommended reviewer:** Project Controls.
Reason: reconciling the schedule update with reported progress is a project-controls determination.

---

### F-A3 — ENTITY RESOLUTION: identification of the main transformer; distinction from AUX-TX-02

| | |
|---|---|
| Level | 2 — Inference (identity resolution) |
| Evidence confidence | HIGH (shared tag TX-01 across sources) |
| Validation | UNVALIDATED |

**Names resolved to TX-01**

| Name as written | Document | Location |
|---|---|---|
| "Main power transformer", tag TX-01 | KMB-EPC-PR-0011 | §4 |
| "Main transformer (T1)", tag TX-01 | KMB-EPC-PR-0012 | §4 |
| "Main transformer delivery" | KMB-EPC-PR-0011 | §6 |
| "Main power transformer TX-01" | KMB-EPC-SCH-U11 / U12 | A1000, A1010 |
| "132/33 kV main power transformer, 120 MVA ONAN/ONAF, with OLTC", tag TX-01, class HV | KMB-EPC-EQL-001 Rev 4 | Equipment table |
| "132/33 kV, 120 MVA, ONAN/ONAF oil-immersed power transformer with on-load tap changer", tag TX-01 | KMB-PO-0042 | Schedule 1, item 1 |
| "Main transformer" | KMB-MIN-PM-0012 | Item 12.3 |

**Kept distinct: AUX-TX-02**

| Evidence | Observation |
|---|---|
| KMB-EPC-EQL-001 Rev 4 | AUX-TX-02: "33/0.4 kV auxiliary transformer, 500 kVA", class MV |
| KMB-SUP-A-LTR-0031 (10 Dec 2026) | Delivery of AUX-TX-02 on "12 January 2027 as planned" |
| KMB-EPC-PR-0012 §4 | AUX-TX-02: "Supplier confirmed delivery", 12 Jan 2027 |
| KMB-EPC-SCH-U12 | A1020 AUX-TX-02 delivery 12-Jan-27 |

**Interpretation.** AUX-TX-02 has a different tag, rating, voltage class and supplier letter. Its
confirmed 12 January 2027 delivery does not relate to TX-01 and has not been used as evidence for
TX-01's delivery date.

**Recommended reviewer:** Owner's Engineer (confirm identity mapping).

---

### F-A4 — DETERMINISTIC CALCULATIONS

| | Calculation | Inputs (evidence) | Result |
|---|---|---|---|
| C1 | Planned delivery → planned installation start | A1000 finish 12-Jan-27; A1010 start 15-Jan-27 (KMB-EPC-SCH-U12) | 3 calendar days |
| C2 | Planned installation start → reported delivery | A1010 start 15-Jan-27 (SCH-U12); 2 Feb 2027 (PR-0012 §4) | Reported delivery is **18 calendar days after** planned installation start |
| C3 | Planned installation finish → reported delivery | A1010 finish 28-Jan-27 (SCH-U12); 2 Feb 2027 (PR-0012 §4) | Reported delivery is 5 calendar days after planned installation finish |
| C4 | Scheduled delivery → reported delivery | A1000 12-Jan-27 (SCH-U12); 2 Feb 2027 (PR-0012 §4) | 21 calendar days later |
| C5 | Reported delivery → planned HV commissioning start | 2 Feb 2027 (PR-0012 §4); A1100 start 10-Feb-27 (SCH-U12) | Reported delivery is 8 calendar days before planned HV commissioning start |

Level 1 — deterministic comparisons of evidenced dates. These are comparisons only. They do not
represent float, a revised installation date, or a forecast of any milestone. The schedule's "Float"
column is empty for all activities (KMB-EPC-SCH-U12), so float is not evidenced.

---

### F-A5 — OBSERVATION: the revised date appears only in the procurement table of progress report 12

| | |
|---|---|
| Level | 1 — Fact |
| Evidence confidence | HIGH |
| Validation | UNVALIDATED |

| Location in KMB-EPC-PR-0012 | Observation |
|---|---|
| §1 Executive summary | No mention of the main transformer. States: "The overall programme continues to target energization on 1 March 2027." |
| §4 Procurement and deliveries | Revised delivery date of 2 February 2027 advised by the supplier (F-A1). |
| §5 Construction | "transformer plinth and bund complete; ready to receive transformer." |
| §6 Programme, key dates table | Lists HV commissioning start, Stage 1 start and energization. **No row for main transformer delivery** (KMB-EPC-PR-0011 §6 included "Main transformer delivery \| 12 Jan 2027"). |
| §6 Programme | "Overall programme: energization date of 1 March 2027 maintained." |
| §7 Risks and issues | No entry concerning the main transformer. |

**Interpretation.** The report's summary sections and its detailed procurement table present different
levels of information about the main transformer. The statement that energization is maintained is
recorded as an observed claim by the EPC Contractor. The supplied documents do not show the basis for
that statement. GridPulse neither endorses nor contradicts it.

**Recommended reviewer:** Owner's Engineer.
Reason: reviewing the consistency and completeness of contractor reporting is an Owner's Engineer
function.

---

### F-A6 — OBSERVATION: schedule logic does not link TX-01 installation to HV commissioning

| | |
|---|---|
| Level | 1 — Fact (schedule content) |
| Evidence confidence | HIGH |
| Validation | UNVALIDATED |

**Evidence A**
Document: KMB-EPC-SCH-U12
Location: activity A1100 "HV commissioning"
Observation: predecessors "A0950 FS; A0500 FS" (HV cable installation and terminations; substation
control building complete). A1010 (TX-01 installation) is not a predecessor of A1100. Same logic in
KMB-EPC-SCH-U11.

**Evidence B**
Document: KMB-EPC-COM-PLN-001 Rev 1 — Commissioning Plan
Location: §5.1 Preconditions
Observation: "HV commissioning shall commence once all HV equipment is installed, terminated and has
passed pre-commissioning checks, and the substation control building is complete."

**Evidence C**
Document: KMB-EPC-EQL-001 Rev 4 — Equipment List
Location: row TX-01
Observation: voltage class "HV".

**Interpretation.** The commissioning plan's precondition refers to all HV equipment; TX-01 is
classified HV; the schedule logic for HV commissioning does not include TX-01 installation. Whether
the schedule logic reflects the intended sequence is for Project Controls to determine. This
observation is the basis of inferred relationship R-A-I1 (§3).

**Recommended reviewer:** Project Controls; Commissioning Engineer.

---

### F-A7 — STALE / SUPERSEDED OBSERVATIONS

| Observation | Document / location | Status relative to newer information |
|---|---|---|
| "Delivery on track" for 12 Jan 2027 | KMB-EPC-PR-0011 §4 (period to 20 Nov 2026) | Superseded in the next report by the revised date (F-A1) |
| TX-01 delivery 12-Jan-27, "Not started" | KMB-EPC-SCH-U12, A1000 (data date 18 Dec 2026) | Diverges from the same period's progress report (F-A2); may not reflect the supplier advice |
| "Main transformer: FAT report issued … Shipping arrangements in progress." | KMB-MIN-PM-0012, item 12.3 (3 Dec 2026) | Predates the revised date reported in PR-0012 |

Evidence confidence for the schedule's delivery date as a *current* observation: LOW until the
divergence in F-A2 is resolved. Validation: UNVALIDATED.

**Recommended reviewer:** Project Controls.

---

### F-A8 — MISSING EVIDENCE

| Expected evidence | Why relevant | Status in supplied documents |
|---|---|---|
| Supplier communication advising the revised date | Primary source for the date reported in PR-0012 §4; reason for revision | Not supplied. PR-0012 reports it second-hand. |
| Shipping plan for the main transformer | Action "Issue shipping plan", owner EPC, due 17 Dec (KMB-MIN-PM-0012 item 12.3) | Not supplied; no evidence the action was closed |
| Amendment to KMB-PO-0042 delivery date | Contractual delivery date remains 12 January 2027 in the supplied extract | Not supplied |
| Revised installation plan for TX-01 | Would show how installation (A1010) is planned relative to the reported delivery | Not supplied |
| Float / critical path information | Needed to interpret C2–C5 | Float column empty in SCH-U12 |

**Recommended reviewer:** Procurement (supplier communication, PO); Project Controls (installation
plan, float).

---

## 3. Relationships used in this investigation

| ID | Relationship | Type | Confidence | Validation | Provenance | Evidence |
|---|---|---|---|---|---|---|
| R-A-E1 | TX-01 delivery (A1000) → TX-01 installation (A1010) | `PRECEDES` (FS) | EXPLICIT | UNVALIDATED | SCHEDULE_DERIVED | KMB-EPC-SCH-U12, A1010 predecessor "A1000 FS" (also U11) |
| R-A-E2 | HV commissioning (A1100) → Stage 1 grid compliance tests (A1200) | `PRECEDES` | EXPLICIT | UNVALIDATED | SCHEDULE_DERIVED; DOCUMENT_DERIVED / AI_EXTRACTED | SCH-U12 A1200 predecessor "A1100 FS"; KMB-EPC-GCT-PRG-001 §2.1 "Stage 1 shall commence on completion of HV commissioning"; KMB-EPC-COM-PLN-001 §6 |
| R-A-E3 | Stage 1 grid compliance tests (A1200) → Energization (A1300) | `PRECEDES` / condition | EXPLICIT | UNVALIDATED | SCHEDULE_DERIVED; DOCUMENT_DERIVED / AI_EXTRACTED | SCH-U12 A1300 predecessor "A1200 FS"; KMB-EPC-GCT-PRG-001 §2.2 "Energization is subject to the Network Operator's acceptance of the Stage 1 results" |
| R-A-I1 | TX-01 installation (A1010) → HV commissioning (A1100) | `PRECEDES` | **INFERRED** | UNVALIDATED | AI_INFERRED | KMB-EPC-COM-PLN-001 §5.1 (all HV equipment installed before HV commissioning) + KMB-EPC-EQL-001 Rev 4 (TX-01 class HV). **Not stated** in the schedule (F-A6) or elsewhere. |

**Reasoning for R-A-I1.** The commissioning plan makes installation of *all HV equipment* a
precondition for HV commissioning and states that the equipment list classification governs the
applicable phase (§3). The equipment list classifies TX-01 as HV. From these two statements, TX-01
installation appears to be a precondition of HV commissioning. No document states this relationship
for TX-01 specifically, and the schedule does not model it. This inference requires validation.

---

## 4. Potential Impact Preview

All items are **potentially affected** and **require review**. None is a conclusion.

### Direct

| Entity | Association with the observed change | Evidence |
|---|---|---|
| TX-01 delivery (A1000) | Subject of the divergent observations | F-A1, F-A2 |
| TX-01 installation (A1010, planned 15–28 Jan 2027) | Explicit successor of delivery (R-A-E1); reported delivery falls after planned installation start and finish (C2, C3) | R-A-E1; F-A4 |

### Propagation

| Path | Relationship status |
|---|---|
| Delivery → installation | EXPLICIT · UNVALIDATED (R-A-E1) |
| Installation → HV commissioning | **INFERRED · UNVALIDATED** (R-A-I1) — possible dependency |
| HV commissioning → Stage 1 tests → energization | EXPLICIT · UNVALIDATED (R-A-E2, R-A-E3) |

Any path beyond TX-01 installation passes through the inferred relationship R-A-I1 and is therefore an
**inferred path**.

### Secondary

| Entity | Planned date | Why it may require review |
|---|---|---|
| HV commissioning (A1100) | 10–17 Feb 2027 | Possible dependency on TX-01 installation (R-A-I1); reported delivery is 8 calendar days before planned start (C5) |
| Stage 1 grid compliance tests (A1200) | 20–26 Feb 2027 | Explicit successor of HV commissioning (R-A-E2), via inferred path |
| Energization (A1300) | 1 Mar 2027 | Explicit successor of Stage 1 (R-A-E3), via inferred path; PR-0012 states the date is "maintained" (F-A5) |

### Checkpoints

| Checkpoint | Why it may warrant investigation |
|---|---|
| PROCUREMENT CHECKPOINT | Divergent delivery observations for TX-01 (F-A1, F-A2); missing supplier communication and PO amendment (F-A8) |
| CONSTRUCTION CHECKPOINT | TX-01 installation planned before the reported delivery date (C2, C3) |
| COMMISSIONING CHECKPOINT | Possible dependency of HV commissioning on TX-01 installation (R-A-I1) |
| GRID COMPLIANCE CHECKPOINT | Stage 1 tests follow HV commissioning (R-A-E2), via inferred path |
| ENERGIZATION CHECKPOINT | Energization is conditional on Stage 1 acceptance (R-A-E3), via inferred path |

Potential exposure: the evidence indicates a potential exposure of the TX-01 installation milestone
and, through an inferred path, of downstream commissioning and energization milestones. Expert
validation required.

---

## 5. Reviewer routing

| Finding / item | Recommended reviewer | Reason |
|---|---|---|
| F-A1, F-A8 (supplier communication, PO) | Procurement | Status of the supplier advice and the contractual delivery date |
| F-A2, F-A7, C1–C5 | Project Controls | Reconciliation of schedule and reported progress; interpretation of date comparisons |
| F-A6, R-A-I1 | Project Controls; Commissioning Engineer | Whether HV commissioning depends on TX-01 installation and whether the schedule logic reflects it |
| F-A5 | Owner's Engineer | Consistency and completeness of contractor reporting |
| F-A3 | Owner's Engineer | Confirmation of the equipment identity mapping |
| Installation re-planning (Q-A3) | EPC technical lead | Installation method and duration are outside the supplied evidence |

---

## 6. What This Investigation Does NOT Establish

The supplied evidence does **not** establish that:

- the main transformer will actually be delivered on 2 February 2027, or on any other date;
- 2 February 2027 has replaced 12 January 2027 as the operative or contractual delivery date;
- the schedule update or the progress report is incorrect;
- TX-01 installation will start or finish on any date other than the planned dates;
- HV commissioning actually depends on TX-01 installation (the relationship is inferred and unvalidated);
- HV commissioning, Stage 1 grid compliance tests or energization will move;
- the 1 March 2027 energization date can or cannot be maintained;
- there is or is not float between TX-01 installation and HV commissioning;
- any party intended to omit or present information in any particular way;
- any contractual consequence (for example under the purchase order) has arisen.

Insufficient evidence in the supplied project information for each of the above. These are matters
for human review.

---

## 7. Unresolved questions

| ID | Question | Who can answer / what evidence would answer it |
|---|---|---|
| Q-A1 | Which TX-01 delivery date is currently operative — 12 January or 2 February 2027 — and has the purchase order delivery date been amended? | Procurement; supplier communication; PO amendment |
| Q-A2 | Will the next schedule update reflect the reported delivery date, and was U12 prepared before the supplier advice was received? | Project Controls; next schedule update |
| Q-A3 | Has TX-01 installation (A1010) been re-planned relative to the reported delivery date, and what is the installation duration from delivery? | EPC technical lead; installation plan |
| Q-A4 | Does HV commissioning require TX-01 to be installed (validation of R-A-I1), and should the schedule logic include this link? | Commissioning Engineer; Project Controls |
| Q-A5 | What is the basis for the statement that the 1 March 2027 energization date is maintained? | EPC Contractor via Owner's Engineer; programme analysis |
| Q-A6 | Was the shipping plan (minutes item 12.3, due 17 Dec) issued, and what reason did the supplier give for the revision? | Procurement; shipping plan; supplier communication |
| Q-A7 | What float exists between TX-01 installation and HV commissioning? | Project Controls; schedule with float data |

---

## 8. Ask GridPulse — example

Structure: canonical Ask GridPulse answer structure (D-037).

**Question:** *"Is the main transformer delivery date consistent across the latest project documents?"*

**VALIDATED INFORMATION**
None. No finding, claim or relationship in this investigation has been reviewed by a human.

**OBSERVED INFORMATION**
- No — the latest supplied documents are not consistent. For the reporting period ending 18 December
  2026, progress report KMB-EPC-PR-0012 reports a supplier-advised revised delivery date of 2 February
  2027 for TX-01; schedule update KMB-EPC-SCH-U12 shows 12 January 2027; the purchase order extract
  shows 12 January 2027. (UNVALIDATED; evidence confidence HIGH for each observation.)
- Entity: TX-01, main power transformer (also written "Main transformer (T1)"). AUX-TX-02 is a
  separate transformer whose 12 January 2027 delivery is separately confirmed; it is not part of this
  answer.
- Explicit relationship: TX-01 delivery → TX-01 installation (EXPLICIT · UNVALIDATED ·
  SCHEDULE_DERIVED).

**INFERRED RELATIONSHIPS**
- TX-01 installation → HV commissioning (INFERRED · UNVALIDATED · AI_INFERRED), from the commissioning
  plan precondition that all HV equipment is installed before HV commissioning and the equipment
  list's HV classification of TX-01. Not stated in any supplied document.

**DETERMINISTIC CALCULATIONS**
- 12 Jan 2027 → 2 Feb 2027: 21 calendar days.
- 15 Jan 2027 (planned installation start) → 2 Feb 2027: 18 calendar days.

**POTENTIAL EXPOSURES**
- TX-01 installation milestone (A1010) — potentially affected; requires review.
- Via the inferred relationship: HV commissioning (A1100) — possible dependency; requires review.

**HUMAN VALIDATION REQUIRED**
- Which delivery date is currently operative, and whether the purchase order has been amended —
  Procurement; Project Controls. GridPulse does not have sufficient evidence to determine this.
- Whether HV commissioning depends on TX-01 installation — Commissioning Engineer; Project Controls.

**EVIDENCE**
- KMB-EPC-PR-0012 §4, row "Main transformer (T1) / TX-01": "The supplier has advised a revised
  delivery date of 2 February 2027."
- KMB-EPC-SCH-U12, activity A1000: finish 12-Jan-27; activity A1010: start 15-Jan-27, predecessor
  "A1000 FS".
- KMB-PO-0042, Schedule 2, item 1: "12 January 2027".
- KMB-EPC-COM-PLN-001 Rev 1 §5.1; KMB-EPC-EQL-001 Rev 4, row TX-01 (class HV).
- KMB-EPC-EQL-001 Rev 4, row AUX-TX-02; KMB-SUP-A-LTR-0031.
