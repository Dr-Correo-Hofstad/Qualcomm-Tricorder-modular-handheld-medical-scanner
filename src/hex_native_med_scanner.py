"""
RT Hexadecimal + Snap-Circuit Medical Scanner Driver
Maps biometric sensor readings to 0.0V-1.0V (0.0625V step) 16-state analog logic
and synchronizes detached probe telemetry via paired double-latch gate buffers.
"""

HEX_STEP_VOLTS = 0.0625
HEX_STATES = 16

MODULE_IDS = {
    0x0: "NONE",
    0x1: "BLOOD_ANALYZER_PPG",
    0x2: "IR_THERMOMETER",
    0x3: "GASTROINTESTINAL_MONITOR",
}


def quantize_to_hex_voltage(normalized_value: float) -> tuple[int, float]:
    """Converts a 0.0-1.0 normalized sensor reading into a 4-bit hex state and exact RT voltage."""
    clamped = max(0.0, min(1.0, normalized_value))
    state = min(HEX_STATES - 1, int(round(clamped / HEX_STEP_VOLTS)))
    return state, round(state * HEX_STEP_VOLTS, 4)


class SnapCircuitLatchBuffer:
    """Models the air-gapped double-latch gate buffer linking Node B (probe) to Node A (handheld)."""

    def __init__(self, module_code: int):
        self.module_code = module_code
        self.entangled = True
        self.latched_channels = {"HX_SIG_1": 0.0, "HX_SIG_2": 0.0}

    def transfer_probe_state(self, sig1_norm: float, sig2_norm: float) -> dict:
        if not self.entangled:
            raise RuntimeError("Snap-Circuit covalent link severed: unauthorized state change detected.")
        s1, v1 = quantize_to_hex_voltage(sig1_norm)
        s2, v2 = quantize_to_hex_voltage(sig2_norm)
        self.latched_channels["HX_SIG_1"] = v1
        self.latched_channels["HX_SIG_2"] = v2
        return {
            "module": MODULE_IDS.get(self.module_code, "UNKNOWN"),
            "HX_MOD_ID_V": round(self.module_code * HEX_STEP_VOLTS, 4),
            "HX_SIG_1": {"hex": hex(s1), "volts": v1},
            "HX_SIG_2": {"hex": hex(s2), "volts": v2},
        }


class RTMedicalScannerChip:
    """Virtual silicon block discovered by main.py recursive BIOS loader."""

    def __init__(self):
        self.thermal_interface = "RTPhaseChangeThermalInterface"
        self.guard_ring_enabled = True
        self.buffers = {
            "blood": SnapCircuitLatchBuffer(0x1),
            "temp": SnapCircuitLatchBuffer(0x2),
            "gut": SnapCircuitLatchBuffer(0x3),
        }

    def sample_blood_analyzer(self, heart_rate_bpm: float, spo2_pct: float) -> dict:
        hr_norm = (heart_rate_bpm - 40.0) / 160.0      # Maps 40-200 BPM to 0.0V-1.0V
        spo2_norm = (spo2_pct - 85.0) / 15.0           # Maps 85%-100% SpO2 to 0.0V-1.0V
        return self.buffers["blood"].transfer_probe_state(hr_norm, spo2_norm)

    def sample_thermometer(self, temp_celsius: float) -> dict:
        temp_norm = (temp_celsius - 35.0) / 7.5        # Maps 35.0C-42.5C in 0.5C steps
        return self.buffers["temp"].transfer_probe_state(temp_norm, 0.0)

    def sample_gut_monitor(self, acoustic_db: float) -> dict:
        gut_norm = acoustic_db / 80.0                  # Maps 0-80 dB bowel acoustic envelope
        return self.buffers["gut"].transfer_probe_state(gut_norm, 0.0)


if __name__ == "__main__":
    scanner = RTMedicalScannerChip()
    print("Blood Telemetry:", scanner.sample_blood_analyzer(76.0, 98.0))
    print("Temp Telemetry: ", scanner.sample_thermometer(37.0))
    print("Gut Telemetry:  ", scanner.sample_gut_monitor(32.0))
