"""
Generates a KiCad S-expression netlist for the RT Hexadecimal Tricorder Mainboard
and Snap-Circuit Double-Latch Sensor Modules.
"""

from pathlib import Path

KICAD_NETLIST_TEMPLATE = """(export (version "E")
  (design
    (source "build_tricorder_kicad.py")
    (tool "RT-Hex-KiCad-Generator 1.0")
  )
  (components
    (comp (ref "U1") (value "RT_TENSOR_HEX_MCU") (footprint "Package_BGA:BGA-256_17x17mm_Layout16x16_P1.0mm"))
    (comp (ref "U2") (value "SNAP_LATCH_BUFFER_NODE_A") (footprint "Connector_M2:M2_Socket_Key_M"))
    (comp (ref "J1") (value "RT_HEX_POGO_DOCK_6PIN") (footprint "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical"))
    (comp (ref "GR1") (value "RT_GUARD_RING_SHIELD") (footprint "Fiducial:Fiducial_1.5mm_Mask3mm"))
    (comp (ref "TH1") (value "RT_PHASE_CHANGE_THERMAL_PAD") (footprint "Heatsink:Heatsink_3D_VaporChamber_40x40mm"))
  )
  (nets
    (net (code "1") (name "1.0V_HEX_REF") (node (ref "U1") (pin "A1")) (node (ref "U2") (pin "1")) (node (ref "J1") (pin "1")))
    (net (code "2") (name "GND_RT_2OZ") (node (ref "U1") (pin "A2")) (node (ref "U2") (pin "2")) (node (ref "J1") (pin "2")) (node (ref "GR1") (pin "1")))
    (net (code "3") (name "HX_SIG_1") (node (ref "U1") (pin "B1")) (node (ref "U2") (pin "3")) (node (ref "J1") (pin "3")))
    (net (code "4") (name "HX_SIG_2") (node (ref "U1") (pin "B2")) (node (ref "U2") (pin "4")) (node (ref "J1") (pin "4")))
    (net (code "5") (name "HX_MOD_ID") (node (ref "U1") (pin "B3")) (node (ref "U2") (pin "5")) (node (ref "J1") (pin "5")))
    (net (code "6") (name "THERMAL_SYNC") (node (ref "U1") (pin "C1")) (node (ref "TH1") (pin "1")) (node (ref "J1") (pin "6")))
  )
)
"""

if __name__ == "__main__":
    out_file = Path("tricorder_rt_mainboard.net")
    out_file.write_text(KICAD_NETLIST_TEMPLATE, encoding="utf-8")
    print(f"Exported KiCad netlist to {out_file.resolve()}")
