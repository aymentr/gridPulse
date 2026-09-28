# GridPulse Investigation Bundle — PCS Technical Specification Rev 8

> Illustrative GridPulse-style investigation output, prepared manually from the supplied project
> documents for validation purposes. It was not produced by GridPulse software.
> All project content is synthetic (fictional project "Kestrel Moor BESS"); technical values are
> illustrative.

| | |
|---|---|
| Project | Kestrel Moor BESS (100 MW / 400 MWh) |
| Initiated by | Transmittal KMB-EPC-TR-0457 (4 Dec 2026): KMB-EPC-SPC-PCS-001 Rev 8 and KMB-EPC-SPC-BCN-003 Rev 4, "For information" |
| Investigation type | Impact investigation (pre-review) |
| Review status | **PRE-REVIEW** — no finding, claim or relationship in this bundle has been reviewed by a human. Validated information: **none**. |

---

## 0. Reviewer summary

1. **Undescribed technical changes.** PCS specification Rev 8 changes clause 5.3 (reactive power
   capability range from **0–100 %** to **20–100 %** of rated active power, with capability below 20 %
   deferred to an **Appendix C that is not supplied**) and clause 6.1 (control firmware **v3.2 → v4.0**).
   The revision history and transmittal describe Rev 8 only as "General update".
2. **Stale reference.** The PPC functional specification Rev 2, clause 4.2, still defines the PPC
   design basis by reference to **PCS specification Rev 7, clause 5.3**.
3. **Possible dependency on a grid requirement.** Requirement R-12 requires reactive capability at the
   point of connection across 0–100 % of Registered Capacity. No document states that R-12 depends on
   PCS capability; the relationship is **inferred** from the supplied documents.
4. **Test coverage comparison.** Test GC-04 (verifying R-12) includes test points at 0 % and 10 %,
   below the 20 % lower bound stated in Rev 8 clause 5.3. The two values are stated on different bases.
5. **Requires review:** Electrical/Grid Engineer, EPC technical lead, Commissioning Engineer, Owner's
   Engineer.

This bundle does **not** establish whether any requirement is or is not met. See §6.

---

## 1. Documents processed

| Document no. | Title | Rev / date | Used for |
|---|---|---|---|
| KMB-EPC-SPC-PCS-001 | PCS Technical Specification | Rev 7, 15 Jun 2026 | Previous revision |
| KMB-EPC-SPC-PCS-001 | PCS Technical Specification | Rev 8, 4 Dec 2026 | Current revision |
| KMB-EPC-SPC-PPC-002 | PPC Functional Specification | Rev 2, 10 Jul 2026 | PPC design basis |
| KMB-NO-GCR-001 | Grid Connection Requirements (Network Operator) | Issue 3, 1 Mar 2026 | Requirements R-10 to R-31 |
| KMB-EPC-GCT-PLN-004 | Grid Compliance Test Plan | Rev 1, 20 Sep 2026 | GC-04 procedure |
| KMB-EPC-SPC-BCN-003 | Battery Container Specification | Rev 3 and Rev 4 | Second revision on the same transmittal |
| KMB-EPC-TR-0457 | Transmittal | 4 Dec 2026 | Reason for issue |
| KMB-EPC-SCH-U12 (milestone extract) | Schedule update milestones | Data date 18 Dec 2026 | Test timing |
| KMB-EPC-EQL-001 | Equipment List | Rev 4, 30 Oct 2026 | Plant equipment |
| KMB-EPC-SCD-PTL-001 | SCADA Points List — extract | Rev 3, 12 Nov 2026 | Reviewed; no relationship to this investigation identified |
| KMB-DOC-REG-2026-12 | Document register extract | Status at 18 Dec 2026 | Current revisions |

**Legend.** Level 1 = fact (directly supported or deterministically calculated). Level 2 =
relationship or inference. Evidence confidence: HIGH / MEDIUM / LOW. Relationship confidence:
EXPLICIT / INFERRED. Validation: UNVALIDATED / CONFIRMED / REJECTED. All items in this bundle are
UNVALIDATED.

---

## 2. Findings

### F-B1 — CHANGE: PCS reactive power capability range (clause 5.3)

| | |
|---|---|
| Level | 1 — Fact (version comparison) |
| Potential event | `SPECIFICATION_CHANGE` — status: DETECTED → UNDER_REVIEW |
| Affected entity | PCS-01 … PCS-28 (power conversion system skids) |
| Evidence confidence | HIGH |
| Validation | UNVALIDATED |

**Evidence A (Rev 7)**
Document: KMB-EPC-SPC-PCS-001 Rev 7 — PCS Technical Specification
Location: §5.3 Reactive power capability
Observation: "… 0.95 leading to 0.95 lagging at the PCS AC terminals across 0 % to 100 % of rated
active power, at nominal voltage."

**Evidence B (Rev 8)**
Document: KMB-EPC-SPC-PCS-001 Rev 8 — PCS Technical Specification
Location: §5.3 Reactive power capability
Observation: "… 0.95 leading to 0.95 lagging at the PCS AC terminals across 20 % to 100 % of rated
active power, at nominal voltage. Below 20 % of rated active power, reactive power capability shall be
in accordance with the manufacturer's capability curve (Appendix C)."

**Change.** Lower bound of the stated range: 0 % → 20 % of rated active power. New sentence deferring
capability below 20 % to Appendix C. Power-factor range, measurement point (PCS AC terminals) and
voltage condition unchanged.

**Recommended reviewer:** Electrical/Grid Engineer.
Reason: the technical significance of the revised range requires engineering interpretation.

---

### F-B2 — CHANGE: PCS control firmware version (clause 6.1)

| | |
|---|---|
| Level | 1 — Fact (version comparison) |
| Potential event | `SPECIFICATION_CHANGE` — status: DETECTED → UNDER_REVIEW |
| Affected entity | PCS-01 … PCS-28 control firmware |
| Evidence confidence | HIGH |
| Validation | UNVALIDATED |

Evidence A: KMB-EPC-SPC-PCS-001 Rev 7 §6.1 — "PCS control firmware version v3.2."
Evidence B: KMB-EPC-SPC-PCS-001 Rev 8 §6.1 — "PCS control firmware version v4.0."

**Interpretation.** The supplied documents do not describe what changed between firmware v3.2 and
v4.0. Clause 6.2 (PPC interface) is unchanged between revisions.

**Recommended reviewer:** EPC technical lead; Electrical/Grid Engineer.

---

### F-B3 — CHANGE: shipping documentation language (clause 9.2)

| | |
|---|---|
| Level | 1 — Fact (version comparison) |
| Evidence confidence | HIGH |
| Validation | UNVALIDATED |

Evidence A: Rev 7 §9.2 — "Shipping documentation shall be provided in English."
Evidence B: Rev 8 §9.2 — "… in English and the language of the site country."

No relationship from this clause to other supplied project information was identified. Not carried
into impact analysis.

---

### F-B4 — OBSERVATION: revision issued without a description of the changes

| | |
|---|---|
| Level | 1 — Fact |
| Evidence confidence | HIGH |
| Validation | UNVALIDATED |

| Document / location | Observation |
|---|---|
| KMB-EPC-SPC-PCS-001 Rev 8, Revision history | "8 \| 04-Dec-26 \| General update" |
| KMB-EPC-TR-0457, document table | Rev 8, reason for issue "General update"; purpose "For information"; "No response required." |
| KMB-DOC-REG-2026-12 | PCS spec current revision Rev 8, status "For information" |

**Interpretation.** F-B1 to F-B3 were identified by comparing Rev 7 and Rev 8, not from any change
description in the supplied documents.

**Recommended reviewer:** Owner's Engineer.

---

### F-B5 — STALE REFERENCE: PPC functional specification references PCS specification Rev 7

| | |
|---|---|
| Level | 1 — Fact |
| Finding type | STALE_EVIDENCE (cross-document reference to a superseded revision) |
| Evidence confidence | HIGH |
| Validation | UNVALIDATED |

**Evidence A**
Document: KMB-EPC-SPC-PPC-002 Rev 2 — PPC Functional Specification
Location: §4.2
Observation: "Reactive power control shall be designed to the PCS capability defined in PCS
specification KMB-EPC-SPC-PCS-001 Rev 7, clause 5.3."

**Evidence B**
Document: KMB-DOC-REG-2026-12 — Document register extract
Observation: KMB-EPC-SPC-PCS-001 current revision "Rev 8" (04-Dec-26); KMB-EPC-SPC-PPC-002 current
revision "Rev 2" (10-Jul-26), status "For construction".

**Evidence C**
Document: KMB-EPC-SPC-PCS-001 Rev 8 §5.3 — clause 5.3 content changed (F-B1).

**Interpretation.** The PPC design basis cites a clause whose content has changed in a later
revision. The supplied documents do not show whether the PPC design has been reviewed against Rev 8.
PPC Rev 2 §4.3 also states that the PPC distributes reactive power setpoints "in proportion to their
available capability".

**Recommended reviewer:** EPC technical lead.
Reason: whether the PPC design basis requires revision is an engineering determination.

---

### F-B6 — MISSING EVIDENCE: Appendix C capability curve

| | |
|---|---|
| Level | 1 — Fact |
| Evidence confidence | HIGH (reference present; appendix absent) |
| Validation | UNVALIDATED |

Document: KMB-EPC-SPC-PCS-001 Rev 8 §5.3 refers to "the manufacturer's capability curve (Appendix C)"
for capability below 20 % of rated active power. Appendix C is not included in the supplied Rev 8
document or elsewhere in the supplied documents. §9.1 lists "capability curves" among required
documentation.

Reactive capability below 20 % of rated active power: **insufficient evidence in the supplied project
information.**

**Recommended reviewer:** Electrical/Grid Engineer; EPC technical lead.

---

### F-B7 — COMPARISON: Rev 8 stated range vs requirement R-12 stated range

| | |
|---|---|
| Level | 1 — Fact (deterministic comparison of stated ranges) |
| Evidence confidence | HIGH for both statements |
| Validation | UNVALIDATED |

**Evidence A**
Document: KMB-EPC-SPC-PCS-001 Rev 8 §5.3
Observation: 0.95 leading to 0.95 lagging, at the **PCS AC terminals**, across **20 % to 100 % of
rated active power** (per PCS), at nominal voltage.

**Evidence B**
Document: KMB-NO-GCR-001 Issue 3, R-12
Observation: "any power factor between 0.95 leading and 0.95 lagging at the POC across the full active
power range from 0 % to 100 % of Registered Capacity, for both import and export."

**Comparison.** The range stated in Rev 8 §5.3 does not cover the 0–20 % portion of the range stated
in R-12. The two statements differ in:

| | Rev 8 §5.3 | R-12 |
|---|---|---|
| Measurement point | PCS AC terminals | Point of connection (POC) |
| Basis | % of rated active power of each PCS | % of Registered Capacity of the facility |
| Direction | Not stated | Import and export |
| Voltage condition | Nominal voltage | Not stated in R-12 |

This is a comparison of stated ranges only. Because the measurement points and bases differ, the
comparison does not show whether R-12 is or is not met. Capability below 20 % is deferred to Appendix
C (F-B6).

**Recommended reviewer:** Electrical/Grid Engineer.

---

### F-B8 — COMPARISON: GC-04 test points vs Rev 8 stated range

| | |
|---|---|
| Level | 1 — Fact (deterministic comparison) |
| Evidence confidence | HIGH |
| Validation | UNVALIDATED |

**Evidence A**
Document: KMB-EPC-GCT-PLN-004 Rev 1 — Grid Compliance Test Plan
Location: §3.1 (GC-04 procedure outline)
Observation: facility exporting at "0 %, 10 %, 25 %, 50 %, 75 % and 100 % of Registered Capacity";
§3.3 "Repeat at 50 % import"; §3.4 acceptance: "Power factor at the POC within the range stated in
R-12 at every test point."

**Evidence B**
Document: KMB-EPC-SPC-PCS-001 Rev 8 §5.3 — stated range 20 % to 100 % of rated active power.

**Comparison.** Two of the six export test points (0 % and 10 %) lie below the 20 % lower bound
stated in Rev 8 §5.3. The test points are expressed as % of Registered Capacity at the POC; the Rev 8
range as % of rated active power at the PCS terminals (see F-B7).

**Recommended reviewer:** Commissioning Engineer; Electrical/Grid Engineer.

---

### F-B9 — OBSERVATION: requirement clauses concerning changes to plant or control systems

| | |
|---|---|
| Level | 1 — Fact (clause text) |
| Evidence confidence | HIGH |
| Validation | UNVALIDATED |

Document: KMB-NO-GCR-001 Issue 3

- **R-30:** "The connecting party shall notify the Network Operator of any change to plant equipment
  or control systems that may affect compliance with these requirements, before compliance testing of
  the affected capability."
- **R-31:** "Where a change to plant or control systems affects the dynamic performance of the
  facility, the connecting party shall submit updated simulation models to the Network Operator."

**Interpretation.** These clauses concern changes to plant equipment and control systems; F-B1 and
F-B2 are changes to a plant-equipment specification and its control firmware. Whether either clause
applies is a human determination. GridPulse has not determined that either clause applies.

**Recommended reviewer:** Electrical/Grid Engineer; Owner's Engineer.

---

### F-B10 — SEPARATE CHANGE: battery container finish colour (not related to the PCS change)

| | |
|---|---|
| Level | 1 — Fact |
| Evidence confidence | HIGH |
| Validation | UNVALIDATED |

KMB-EPC-SPC-BCN-003 Rev 3 §6.3 "RAL 7035 (light grey)" → Rev 4 §6.3 "RAL 9002 (grey white)";
revision history "Finish colour updated"; issued on the same transmittal KMB-EPC-TR-0457. No
relationship to the PCS change or to grid requirements was identified. Not carried into impact
analysis.

---

### F-B11 — ENTITY RESOLUTION: PCS terminology

| | |
|---|---|
| Level | 2 — Inference (identity resolution) |
| Evidence confidence | HIGH |
| Validation | UNVALIDATED |

| Name as written | Document / location |
|---|---|
| "PCS-01 … PCS-28 (power conversion system skids)"; "bidirectional inverters" | KMB-EPC-SPC-PCS-001 Rev 7/8, header and §1 |
| "PCS skid: 3.8 MVA power conversion system with 0.69/33 kV skid transformer", class MV | KMB-EPC-EQL-001 Rev 4 |
| "PCS units" | KMB-EPC-SPC-PPC-002 Rev 2 §4.3, §5 |
| "Inverter-Based Storage Facilities" (document title) | KMB-NO-GCR-001 Issue 3 |

---

## 3. Relationships used in this investigation

| ID | Relationship | Type | Confidence | Validation | Provenance | Evidence |
|---|---|---|---|---|---|---|
| R-B-E1 | PPC design basis → PCS spec **Rev 7** cl. 5.3 | `REFERENCES` | EXPLICIT | UNVALIDATED | DOCUMENT_DERIVED / AI_EXTRACTED | KMB-EPC-SPC-PPC-002 Rev 2 §4.2; see also §4.3 |
| R-B-E2 | Grid compliance test plan → PPC functional spec Rev 2 | `REFERENCES` | EXPLICIT | UNVALIDATED | DOCUMENT_DERIVED / AI_EXTRACTED | KMB-EPC-GCT-PLN-004 Rev 1 §1 |
| R-B-E3 | Test GC-04 → requirement R-12 | `VERIFIES` | EXPLICIT | UNVALIDATED | DOCUMENT_DERIVED / AI_EXTRACTED | KMB-EPC-GCT-PLN-004 Rev 1 §2 (GC-04 row); §3.4 |
| R-B-E4 | Test GC-04 → PPC-01 | executed through | EXPLICIT | UNVALIDATED | DOCUMENT_DERIVED / AI_EXTRACTED | KMB-EPC-GCT-PLN-004 Rev 1 §2 (GC-04 row, "Executed through: PPC-01") |
| R-B-E5 | Tests GC-01 … GC-06 → grid compliance milestone | `CONTRIBUTES_TO` | EXPLICIT | UNVALIDATED | DOCUMENT_DERIVED / AI_EXTRACTED | KMB-EPC-GCT-PLN-004 Rev 1 §4 |
| R-B-E6 | GC-04 → Stage 2 grid compliance tests (A1400, 2–15 Mar 2027) | part of | EXPLICIT | UNVALIDATED | SCHEDULE_DERIVED; DOCUMENT_DERIVED | KMB-EPC-SCH-U12 milestone extract, A1400 "incl. GC-03 to GC-06"; test plan §2 (Stage 2) |
| R-B-E7 | PCS spec → Grid Connection Requirements (fault ride-through, cl. 5.4) | `REFERENCES` | EXPLICIT | UNVALIDATED | DOCUMENT_DERIVED / AI_EXTRACTED | KMB-EPC-SPC-PCS-001 Rev 7/8 §2 and §5.4. **Concerns fault ride-through only**; no PCS clause references R-12 |
| R-B-I1 | PCS reactive power capability (cl. 5.3) → facility reactive capability under R-12 | `SPECIFIES` / contributes to | **INFERRED** | UNVALIDATED | AI_INFERRED | See reasoning below |

**Reasoning for R-B-I1.**

- R-12 (KMB-NO-GCR-001) sets a reactive capability requirement for the *facility* at the POC.
- The PPC controls reactive power at the POC (PPC Rev 2 §1, §4.1) and distributes reactive setpoints
  across PCS units in proportion to their available capability (§4.3); its design basis is the PCS
  capability in PCS spec cl. 5.3 (§4.2).
- GC-04 verifies R-12 through the PPC (test plan §2).
- The equipment list (KMB-EPC-EQL-001 Rev 4) lists no reactive power equipment other than the PCS
  skids (no capacitor banks, reactors or similar devices are listed).

From these statements, the PCS reactive capability appears to contribute to the facility's reactive
capability under R-12. No supplied document states this relationship. The contribution of other plant
equipment (for example transformers and cables) to reactive power at the POC is not evidenced. The
relationship is inferred and requires technical validation.

---

## 4. Potential Impact Preview

All items are **potentially affected** and **require review**. None is a conclusion.

### Direct

| Entity / document | Association with the observed change | Evidence |
|---|---|---|
| PCS-01 … PCS-28 reactive capability | Stated range changed (F-B1); capability below 20 % not evidenced (F-B6) | PCS spec Rev 7/8 §5.3 |
| PCS-01 … PCS-28 control firmware | Version changed (F-B2) | PCS spec Rev 7/8 §6.1 |

### Propagation

| Path | Relationship status |
|---|---|
| PCS spec cl. 5.3 → PPC design basis | EXPLICIT · UNVALIDATED (R-B-E1) — reference is to the superseded Rev 7 |
| PCS capability → facility capability under R-12 | **INFERRED · UNVALIDATED** (R-B-I1) — possible dependency |
| R-12 → GC-04 → PPC-01 | EXPLICIT · UNVALIDATED (R-B-E3, R-B-E4) |
| GC-04 → grid compliance milestone | EXPLICIT · UNVALIDATED (R-B-E5) |

### Secondary

| Entity / document | Why it may require review |
|---|---|
| PPC functional specification Rev 2 §4.2–4.3 | Design basis cites Rev 7 cl. 5.3, whose content changed (F-B5) |
| GC-04 procedure (test plan §3.1, §3.4) | Test points at 0 % and 10 % lie below the Rev 8 stated lower bound (F-B8); possible dependency via R-B-I1 |
| Stage 2 grid compliance tests (A1400, 2–15 Mar 2027) | Contains GC-04 (R-B-E6) |
| PPC site tests within LV/MV commissioning (A1150, 15–26 Feb 2027) | PPC design basis references the superseded clause (F-B5) |
| Firmware-related requirements R-30 / R-31 | Clause text concerns changes to plant or control systems (F-B9); applicability not determined |

### Checkpoints

| Checkpoint | Why it may warrant investigation |
|---|---|
| ENGINEERING CHECKPOINT | PCS specification changed without change description (F-B4); PPC design basis references superseded revision (F-B5); Appendix C missing (F-B6) |
| COMMISSIONING CHECKPOINT | PPC site tests within LV/MV commissioning (A1150) rely on the PPC design (F-B5) |
| GRID COMPLIANCE CHECKPOINT | GC-04 verifies R-12 (R-B-E3); possible dependency of R-12 on PCS capability (R-B-I1); test-point comparison (F-B8) |

Potential exposure: the supplied evidence shows a potentially relevant relationship between the
revised PCS operating range and requirement R-12. The relationship is inferred rather than explicitly
stated and requires technical validation. Potential impact identified. Expert validation required.

---

## 5. Reviewer routing

| Finding / item | Recommended reviewer | Reason |
|---|---|---|
| F-B1, F-B7, R-B-I1 | Electrical/Grid Engineer | The relationship between the revised PCS capability and the grid requirement requires technical interpretation beyond evidence extraction |
| F-B2, F-B9 | Electrical/Grid Engineer; EPC technical lead | Content of firmware v4.0 and applicability of R-30 / R-31 are outside the supplied evidence |
| F-B5 | EPC technical lead | Whether the PPC design basis requires revision is an engineering determination |
| F-B6 | EPC technical lead | Appendix C to be obtained |
| F-B8 | Commissioning Engineer; Electrical/Grid Engineer | Relationship between GC-04 test points and the revised PCS range |
| F-B4 | Owner's Engineer | Revision issued "for information" without a description of technical changes |

---

## 6. What This Investigation Does NOT Establish

The supplied evidence does **not** establish that:

- the facility meets, or does not meet, requirement R-12;
- GC-04, or any other compliance test, will pass or fail;
- the PCS Rev 8 capability is insufficient for any purpose;
- R-30 or R-31 applies to the Rev 8 changes, or that the Network Operator is to be notified or
  provided with updated models;
- the PPC design, the protection study, the test plan or any other document requires revision;
- firmware v4.0 changes the dynamic behaviour of the PCS or its interaction with the PPC;
- any other plant equipment does or does not provide reactive power at the POC;
- Appendix C provides, or does not provide, reactive capability below 20 % of rated active power;
- the PCS reactive capability actually determines facility compliance with R-12 (the relationship is
  inferred and unvalidated);
- energization, commissioning or grid compliance dates are affected.

Insufficient evidence in the supplied project information for each of the above. These are matters
for human review.

---

## 7. Unresolved questions

| ID | Question | Who can answer / what evidence would answer it |
|---|---|---|
| Q-B1 | What reactive power capability does Appendix C specify below 20 % of rated active power? | EPC technical lead; Appendix C from the PCS manufacturer |
| Q-B2 | Taking all plant equipment into account, does the facility's reactive capability at the POC meet R-12 with PCS Rev 8? | Electrical/Grid Engineer; reactive capability study |
| Q-B3 | Is any reactive power equipment installed or planned that is not listed in the equipment list Rev 4? | EPC technical lead; equipment list, single-line diagram |
| Q-B4 | Will the PPC functional specification be revised to reference PCS Rev 8, and has the PPC design been reviewed against the revised clause 5.3? | EPC technical lead; PPC specification revision |
| Q-B5 | What changed between firmware v3.2 and v4.0, and does the change affect the PPC interface or dynamic performance? | EPC technical lead; PCS manufacturer release notes |
| Q-B6 | Do R-30 and/or R-31 apply to the Rev 8 changes? | Electrical/Grid Engineer; Owner's Engineer (human determination) |
| Q-B7 | Does the GC-04 procedure need review against Rev 8, in particular the 0 % and 10 % test points? | Commissioning Engineer; Electrical/Grid Engineer |
| Q-B8 | Was a description of the Rev 8 changes provided elsewhere? | Owner's Engineer; EPC document control |

---

## 8. Ask GridPulse — example

**Question:** *"Which project documents still reference PCS specification Rev 7?"*

**1. Answer**
- VALIDATED INFORMATION: none — no human review has occurred.
- OBSERVED INFORMATION: Among the supplied documents, the PPC functional specification
  KMB-EPC-SPC-PPC-002 Rev 2 references PCS specification Rev 7 (clause 5.3) in §4.2. The current
  revision of the PCS specification is Rev 8.
- DETERMINISTIC CALCULATIONS: not applicable.
- POTENTIAL EXPOSURES: PPC design basis; indirectly, GC-04, which the test plan executes through the
  PPC and which references PPC Rev 2.

**2. Evidence**
- KMB-EPC-SPC-PPC-002 Rev 2 §4.2: "… PCS capability defined in PCS specification KMB-EPC-SPC-PCS-001
  Rev 7, clause 5.3."
- KMB-DOC-REG-2026-12: KMB-EPC-SPC-PCS-001 current revision Rev 8 (04-Dec-26).
- KMB-EPC-GCT-PLN-004 Rev 1 §1: references PPC Functional Specification Rev 2 (not the PCS
  specification directly).

**3. Affected entities**
PPC-01 (design basis); PCS-01 … PCS-28 (clause 5.3).

**4. Dependency chain**
Test plan → PPC functional spec Rev 2 (EXPLICIT · UNVALIDATED) → PCS spec Rev 7 cl. 5.3 (EXPLICIT ·
UNVALIDATED; superseded revision). INFERRED RELATIONSHIPS: none used in this answer.

**5. Uncertainty / validation status**
HUMAN VALIDATION REQUIRED. Only the supplied documents were searched; documents not supplied (for
example the protection study or PCS manufacturer documentation) may also reference Rev 7. GridPulse
does not have sufficient evidence to determine this for documents it has not received.

**6. Relevant reviewer**
EPC technical lead; Owner's Engineer (document control).

**7. Unresolved question**
Will the PPC functional specification be revised to reference Rev 8?
