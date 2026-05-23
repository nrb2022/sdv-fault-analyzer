# src/dtc_map.py
# DTC code database — maps fault codes to description, severity, system

DTC_DATABASE = {
    "P0300": {
        "desc": "Random/Multiple Cylinder Misfire Detected",
        "system": "Powertrain",
        "severity": "HIGH",
        "action": "Check ignition coils, spark plugs, fuel injectors"
    },
    "P0171": {
        "desc": "System Too Lean (Bank 1)",
        "system": "Powertrain",
        "severity": "MEDIUM",
        "action": "Check MAF sensor, vacuum leaks, fuel pressure"
    },
    "P0217": {
        "desc": "Engine Coolant Over Temperature",
        "system": "Powertrain",
        "severity": "CRITICAL",
        "action": "Stop vehicle immediately. Check coolant level, thermostat"
    },
    "U0100": {
        "desc": "Lost Communication with ECM/PCM",
        "system": "Network",
        "severity": "CRITICAL",
        "action": "Check CAN bus wiring, ECU power supply, ground connections"
    },
    "U0073": {
        "desc": "Control Module Communication Bus Off",
        "system": "Network",
        "severity": "HIGH",
        "action": "Check CAN-H/CAN-L lines for short circuit or termination"
    },
    "C0035": {
        "desc": "Left Front Wheel Speed Sensor Circuit",
        "system": "Chassis",
        "severity": "HIGH",
        "action": "Check wheel speed sensor, wiring harness, ABS module"
    },
    "B0001": {
        "desc": "Driver Frontal Stage 1 Deployment",
        "system": "Body",
        "severity": "CRITICAL",
        "action": "Airbag system fault — do not drive. Dealer inspection required"
    },
    "P0562": {
        "desc": "System Voltage Low",
        "system": "Powertrain",
        "severity": "HIGH",
        "action": "Check battery, alternator output, charging circuit"
    },
}


def lookup_dtc(code):
    """Return DTC info for a given code. Returns None if not found."""
    return DTC_DATABASE.get(code, None)


def get_all_codes():
    """Return list of all known DTC codes."""
    return list(DTC_DATABASE.keys())