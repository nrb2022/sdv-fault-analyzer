# src/reporter.py
# Formats fault data into console report and JSON output

import json
from collections import Counter


# Severity display order — most critical first
SEVERITY_ORDER = ["CRITICAL", "HIGH", "WARNING", "MEDIUM", "UNKNOWN"]

# Console colours for Windows PowerShell (ANSI codes)
COLOURS = {
    "CRITICAL": "\033[91m",  # red
    "HIGH":     "\033[33m",  # yellow
    "WARNING":  "\033[93m",  # light yellow
    "MEDIUM":   "\033[94m",  # blue
    "UNKNOWN":  "\033[90m",  # grey
    "RESET":    "\033[0m",
}


def print_report(faults):
    """Print full diagnostic report to console."""

    _print_header()
    _print_summary(faults)
    _print_by_ecu(faults)
    _print_fault_list(faults)
    _print_footer(faults)


def save_json(faults, filepath):
    """Save full fault list to JSON file."""
    with open(filepath, "w") as f:
        json.dump(faults, f, indent=2)
    print(f"\nReport saved → {filepath}")


# ── Internal print functions ──────────────────────────────────

def _print_header():
    print("\n" + "=" * 60)
    print("   SDV FAULT ANALYZER — DIAGNOSTIC REPORT")
    print("=" * 60)


def _print_summary(faults):
    print("\n[ SUMMARY ]")
    counts = Counter(f["severity"] for f in faults)
    for sev in SEVERITY_ORDER:
        if sev in counts:
            colour = COLOURS.get(sev, "")
            reset  = COLOURS["RESET"]
            bar    = "█" * counts[sev]
            print(f"  {colour}{sev:<10}{reset}  {counts[sev]:>3}  {bar}")


def _print_by_ecu(faults):
    print("\n[ FAULTS BY ECU ]")

    # Group faults by ECU
    ecu_map = {}
    for f in faults:
        ecu = f["ecu_id"]
        if ecu not in ecu_map:
            ecu_map[ecu] = []
        ecu_map[ecu].append(f)

    for ecu in sorted(ecu_map.keys()):
        ecu_faults = ecu_map[ecu]
        counts = Counter(f["severity"] for f in ecu_faults)
        summary = "  ".join(f"{s}:{counts[s]}" for s in SEVERITY_ORDER if s in counts)
        print(f"  {ecu:<15}  {len(ecu_faults)} fault(s)   [{summary}]")


def _print_fault_list(faults):
    print("\n[ FAULT DETAIL — sorted by severity ]")

    # Sort faults: CRITICAL first
    sorted_faults = sorted(
        faults,
        key=lambda f: SEVERITY_ORDER.index(f["severity"])
        if f["severity"] in SEVERITY_ORDER else 99
    )

    for f in sorted_faults:
        colour = COLOURS.get(f["severity"], "")
        reset  = COLOURS["RESET"]
        sev    = f"{colour}{f['severity']:<10}{reset}"
        print(f"  {f['timestamp']}  {f['ecu_id']:<12}  {sev}  {f['message']}")


def _print_footer(faults):
    critical = sum(1 for f in faults if f["severity"] == "CRITICAL")
    print("\n" + "=" * 60)
    if critical > 0:
        print(f"  {COLOURS['CRITICAL']}⚠  {critical} CRITICAL fault(s) — immediate action required{COLOURS['RESET']}")
    else:
        print("  All faults within manageable range.")
    print("=" * 60 + "\n")