> SYNTHETIC VALIDATION DOCUMENT — fictional project "Kestrel Moor BESS". Not a real project, company, standard, grid code or product. All technical values are illustrative.


# PCS Technical Specification

| | |
|---|---|
| Document no. | KMB-EPC-SPC-PCS-001 Rev 8 |
| Date | 4 December 2026 |
| Issued by | EPC Contractor — Electrical Engineering |
| Equipment | PCS-01 … PCS-28 (power conversion system skids) |

## 1. Scope

This specification defines the requirements for the 28 power conversion system (PCS) skids of the
Kestrel Moor BESS, each comprising bidirectional inverters, a 0.69/33 kV skid transformer, and
associated controls.

## 2. References

- KMB-NO-GCR-001 Grid Connection Requirements (Network Operator), Issue 3
- KMB-EPC-SPC-PPC-002 PPC Functional Specification
- KMB-EPC-EQL-001 Equipment List

## 3. Ratings

| Parameter | Value |
|---|---|
| Rated apparent power per skid | 3.8 MVA at 40 °C |
| Rated active power per skid | 3.6 MW |
| AC output voltage (inverter terminals) | 690 V ±10 % |
| Number of skids | 28 |

## 4. Environmental conditions

Ambient temperature −20 °C to +50 °C with derating above 40 °C per manufacturer's curve. Altitude
below 1,000 m.

## 5. Electrical performance

5.1 **Active power.** Each PCS shall be capable of continuous operation between −100 % and +100 % of
rated active power.

5.2 **Voltage range.** Continuous operation between 90 % and 110 % of nominal AC voltage.

5.3 **Reactive power capability.** Each PCS shall provide reactive power corresponding to a power
factor of 0.95 leading to 0.95 lagging at the PCS AC terminals across 20 % to 100 % of rated active power,
at nominal voltage. Below 20 % of rated active power, reactive power capability shall be in accordance with the
manufacturer's capability curve (Appendix C).

5.4 **Fault ride-through.** The PCS shall remain connected and provide reactive current during
voltage disturbances as required by KMB-NO-GCR-001.

5.5 **Harmonics.** Current harmonic distortion shall not exceed 3 % THD at rated output.

## 6. Controls and communications

6.1 **Control firmware.** PCS control firmware version v4.0.

6.2 **PPC interface.** Modbus TCP over the plant fibre network; setpoints for active power, reactive
power, power factor and voltage; update cycle ≤ 100 ms.

6.3 **Local HMI.** Each skid shall have a local HMI for status and alarm display.

## 7. Protection

The PCS shall include internal protection for over/under voltage, over/under frequency, overcurrent,
DC insulation fault and anti-islanding. Settings shall be coordinated with the plant protection study
KMB-EPC-PRT-STD-001.

## 8. Testing

8.1 Factory acceptance tests per the manufacturer's FAT procedure, witnessed by the Purchaser.

8.2 Site acceptance tests as part of LV/MV commissioning (KMB-EPC-COM-PLN-001).

## 9. Documentation

9.1 Datasheets, capability curves, single-line diagrams and O&M manuals.

9.2 Shipping documentation shall be provided in English and the language of the site country.

## Revision history

| Rev | Date | Description |
|---|---|---|
| 6 | 12-Apr-26 | Issued for review |
| 7 | 15-Jun-26 | Updated per comments on Rev 6 |
| 8 | 04-Dec-26 | General update |
