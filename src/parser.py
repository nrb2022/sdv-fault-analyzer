# src/parser.py
# Reads vehicle telemetry CSV and returns structured data

import csv
from datetime import datetime


def load_telemetry(filepath):
    """
    Load vehicle telemetry from CSV file.
    Returns a list of dicts — one dict per row.
    """
    records = []

    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            record = {
                "timestamp":       row["timestamp"],
                "ecu_id":          row["ecu_id"],
                "engine_rpm":      int(row["engine_rpm"]),
                "coolant_temp_c":  float(row["coolant_temp_c"]),
                "battery_voltage": float(row["battery_voltage"]),
                "speed_kmh":       float(row["vehicle_speed_kmh"]),
                "can_bus_load_pct":float(row["can_bus_load_pct"]),
                "dtc_codes":       _parse_dtcs(row["dtc_codes"]),
            }
            records.append(record)

    return records


def _parse_dtcs(raw):
    """
    Convert raw DTC string to a list.
    'P0217|C0035' --> ['P0217', 'C0035']
    ''            --> []
    """
    if not raw or raw.strip() == "":
        return []
    return [code.strip() for code in raw.split("|")]


def summary(records):
    """Print a quick summary of loaded data."""
    print(f"Loaded {len(records)} records")
    print(f"ECUs seen: {sorted(set(r['ecu_id'] for r in records))}")
    print(f"Time range: {records[0]['timestamp']} → {records[-1]['timestamp']}")
    dtc_rows = [r for r in records if r["dtc_codes"]]
    print(f"Rows with DTCs: {len(dtc_rows)}")