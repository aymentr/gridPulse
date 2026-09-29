> SYNTHETIC VALIDATION DOCUMENT — fictional project "Kestrel Moor BESS". Not a real project, company, standard, grid code or product. All technical values are illustrative.


# PPC Functional Specification

| | |
|---|---|
| Document no. | KMB-EPC-SPC-PPC-002 Rev 2 |
| Date | 10 July 2026 |
| Issued by | EPC Contractor — Controls Engineering |
| Equipment | PPC-01 power plant controller |

## 1. Scope

The power plant controller (PPC) coordinates the 28 PCS skids to control active and reactive power,
voltage and frequency response at the point of connection (POC).

## 2. Measurements

The PPC shall use POC voltage and current from the revenue-grade metering VTs and CTs (MTR-01).

## 3. Active power control

3.1 Active power setpoint dispatch to PCS units with ramp-rate limiting.

3.2 Frequency response modes as instructed by the Network Operator.

## 4. Reactive power and voltage control

4.1 Control modes: reactive power setpoint, power factor setpoint and voltage control at the POC, as
instructed by the Network Operator.

4.2 Reactive power control shall be designed to the PCS capability defined in PCS specification
KMB-EPC-SPC-PCS-001 Rev 7, clause 5.3.

4.3 The PPC shall distribute reactive power setpoints across available PCS units in proportion to
their available capability.

## 5. Communications

Modbus TCP to PCS units (see PCS specification clause 6.2); IEC 60870-5-104 to the Network Operator
via RTU-01.

## 6. Testing

Factory tests with PCS simulation; site tests as part of LV/MV commissioning and grid compliance
testing (KMB-EPC-GCT-PLN-004).
