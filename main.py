# main.py
# Entry point — CLI interface for SDV Fault Analyzer

import argparse
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="SDV Fault Analyzer — Vehicle telemetry diagnostic tool",
        epilog="Example: python main.py --input data/vehicle_telemetry.csv --save"
    )
    parser.add_argument(
        "--input", "-i",
        default="data/vehicle_telemetry.csv",
        help="Path to telemetry CSV file (default: data/vehicle_telemetry.csv)"
    )
    parser.add_argument(
        "--save", "-s",
        action="store_true",
        help="Save JSON report to data/report.json"
    )
    parser.add_argument(
        "--severity", "-f",
        choices=["CRITICAL", "HIGH", "WARNING", "MEDIUM"],
        help="Filter output to one severity level only"
    )
    parser.add_argument(
        "--ecu", "-e",
        help="Filter output to one ECU only (e.g. ZCU_Front)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # ── 1. Validate input file exists ────────────────────────
    if not os.path.exists(args.input):
        print(f"ERROR: File not found — {args.input}")
        sys.exit(1)

    # ── 2. Load telemetry ─────────────────────────────────────
    from src.parser import load_telemetry, summary
    print(f"\nLoading telemetry from: {args.input}")
    records = load_telemetry(args.input)
    summary(records)

    # ── 3. Run fault analysis ─────────────────────────────────
    from src.analyzer import analyze
    faults = analyze(records)

    # ── 4. Apply filters if requested ────────────────────────
    if args.severity:
        faults = [f for f in faults if f["severity"] == args.severity]
        print(f"Filter applied: severity = {args.severity}")

    if args.ecu:
        faults = [f for f in faults if f["ecu_id"] == args.ecu]
        print(f"Filter applied: ecu = {args.ecu}")

    # ── 5. Print report ───────────────