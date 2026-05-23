# src/analyzer.py
# Fault detection engine — applies threshold rules to telemetry data

from src.dtc_map import lookup_dtc


# ── Thresholds — easy to tune, all in one place ──────────────
THRESHOLDS = {
    "coolant_temp_warn":     90.0,   # °C
    "coolant_temp_critical": 105.0,  # °C
    "battery_warn":          11.5,   # V
    "battery_critical":      10.5,   # V
    "can_load_warn":         70.0,   # %
    "can_load_overload":     85.0,   # %
    "rpm_idle_max":          1000,   # RPM — above this while speed=0 is suspect
    "rpm_redline":           6500,   # RPM
}


def analyze(records):
    """
    Run all fault checks on every record.
    Returns a list of fault events.
    """
    faults = []

    for record in records:
        faults += _check_coolant(record)
        faults += _check_voltage(record)
        faults += _check_can_load(record)
        faults += _check_rpm(record)
        faults += _check_dtcs(record)

    return faults


# ── Individual check functions ────────────────────────────────

def _check_coolant(r):
    faults = []
    temp = r["coolant_temp_c"]

    if temp >= THRESHOLDS["coolant_temp_critical"]:
        faults.append(_make_fault(r, "CRITICAL", "Coolant",
            f"Coolant temp {temp}°C — CRITICAL overheat threshold breached"))

    elif temp >= THRESHOLDS["coolant_temp_warn"]:
        faults.append(_make_fault(r, "WARNING", "Coolant",
            f"Coolant temp {temp}°C — approaching overheat"))

    return faults


def _check_voltage(r):
    faults = []
    v = r["battery_voltage"]

    if v <= THRESHOLDS["battery_critical"]:
        faults.append(_make_fault(r, "CRITICAL", "Voltage",
            f"Battery {v}V — critical low voltage, ECU brownout risk"))

    elif v <= THRESHOLDS["battery_warn"]:
        faults.append(_make_fault(r, "WARNING", "Voltage",
            f"Battery {v}V — below normal operating range"))

    return faults


def _check_can_load(r):
    faults = []
    load = r["can_bus_load_pct"]

    if load >= THRESHOLDS["can_load_overload"]:
        faults.append(_make_fault(r, "CRITICAL", "CAN Bus",
            f"CAN bus load {load}% — overload, message loss likely"))

    elif load >= THRESHOLDS["can_load_warn"]:
        faults.append(_make_fault(r, "WARNING", "CAN Bus",
            f"CAN bus load {load}% — high utilisation"))

    return faults


def _check_rpm(r):
    faults = []
    rpm   = r["engine_rpm"]
    speed = r["speed_kmh"]

    if rpm > THRESHOLDS["rpm_redline"]:
        faults.append(_make_fault(r, "CRITICAL", "Engine",
            f"RPM {rpm} — redline exceeded"))

    elif rpm > THRESHOLDS["rpm_idle_max"] and speed == 0.0:
        faults.append(_make_fault(r, "WARNING", "Engine",
            f"RPM {rpm} at zero speed — possible runaway idle"))

    return faults


def _check_dtcs(r):
    faults = []

    for code in r["dtc_codes"]:
        info = lookup_dtc(code)
        if info:
            faults.append(_make_fault(r, info["severity"], info["system"],
                f"DTC {code}: {info['desc']} — {info['action']}"))
        else:
            faults.append(_make_fault(r, "UNKNOWN", "Unknown",
                f"DTC {code}: not found in database"))

    return faults


# ── Helper ────────────────────────────────────────────────────

def _make_fault(record, severity, system, message):
    return {
        "timestamp": record["timestamp"],
        "ecu_id":    record["ecu_id"],
        "severity":  severity,
        "system":    system,
        "message":   message,
    }