"""
RT Virtual BIOS & Medical Scanner Runtime (src/main.py)
Recursively loads native silicon modules and executes POST diagnostics.
"""

import importlib.util
import os
from pathlib import Path


def load_virtual_silicon(target_dir: str) -> list:
    loaded_modules = []
    for root, _, files in os.walk(target_dir):
        for filename in sorted(files):
            if filename.endswith(".py") and not filename.startswith("__"):
                file_path = Path(root) / filename
                mod_name = file_path.stem
                spec = importlib.util.spec_from_file_location(mod_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    loaded_modules.append(module)
                    print(f"[BIOS POST] Loaded virtual silicon: {file_path}")
    return loaded_modules


def boot_tricorder():
    print("=== RT HEXADECIMAL UEFI-HX FIRMWARE BOOT ===")
    chips_dir = Path(__file__).parent / "chips" / "native"
    modules = load_virtual_silicon(str(chips_dir))

    scanner = None
    for mod in modules:
        if hasattr(mod, "RTMedicalScannerChip"):
            scanner = mod.RTMedicalScannerChip()
            break

    if scanner is None:
        raise RuntimeError("[BIOS HALT] RTMedicalScannerChip not found in src/chips/native/.")

    print(f"[BIOS POST] Thermal Interface : {scanner.thermal_interface}")
    print(f"[BIOS POST] RTGuardRing Active: {scanner.guard_ring_enabled}")
    print("[BIOS POST] Executing Diagnostic Telemetry Sweep (0.0V-1.0V, 0.0625V/step)...\n")

    readings = [
        scanner.sample_blood_analyzer(heart_rate_bpm=74.0, spo2_pct=98.5),
        scanner.sample_thermometer(temp_celsius=36.8),
        scanner.sample_gut_monitor(acoustic_db=28.0),
    ]
    for packet in readings:
        print(f"  -> {packet['module']} (ID={packet['HX_MOD_ID_V']}V): "
              f"SIG1={packet['HX_SIG_1']} | SIG2={packet['HX_SIG_2']}")


if __name__ == "__main__":
    boot_tricorder()
