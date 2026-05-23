# SDV Fault Analyzer

A Python CLI tool that ingests vehicle telemetry data, detects faults using
rule-based logic, maps signals to DTC codes, and outputs a colour-coded
diagnostic report.

Built as Phase 1 of an AI-for-Automotive learning project.

---

## What it does

- Parses vehicle telemetry CSV (RPM, coolant temp, voltage, CAN bus load, DTCs)
- Applies threshold-based fault detection across 5 signal dimensions
- Maps active DTC codes to descriptions, severity, and recommended actions
- Outputs a colour-coded console report sorted by severity
- Exports full fault list to JSON for downstream processing

## Sample output
