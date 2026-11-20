"""
Generates a KiCad 8/9 PCB file (tricorder_rt_mainboard.kicad_pcb)
Sized for tricorder_chassis.scad with RTGuardRing shielding & 6-pin Hex Dock pads.
"""

from pathlib import Path

KICAD_PCB_CONTENT = """(kicad_pcb (version 20240108) (generator "RT-Hex-PCB-Builder")
  (general
    (thickness 1.6)
  )
  (paper "A4")
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (36 "B.SilkS" user)
    (37 "F.SilkS" user)
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (44 "Edge.Cuts" user)
  )
  (net 0 "")
  (net 1 "1.0V_HEX_REF")
  (net 2 "GND_RT_2OZ")
  (net 3 "HX_SIG_1")
  (net 4 "HX_SIG_2")
  (net 5 "HX_MOD_ID")
  (net 6 "THERMAL_SYNC")

  ;; Board Outline (78mm x 146mm to fit 88mm x 156mm OpenSCAD cavity)
  (gr_rect (start 50 30) (end 128 176)
    (stroke (width 0.15) (type solid)) (fill none) (layer "Edge.Cuts"))

  ;; Silkscreen Label
  (gr_text "RT HEX TRICORDER MAINBOARD (0.0V-1.0V)" (at 89 40 0)
    (layer "F.SilkS") (effects (font (size 1.5 1.5) (thickness 0.25))))

  ;; 6-Pin Hex Pogo Dock Pads at bottom edge (J1)
  (footprint "RT_Hex_Dock_6Pin" (layer "F.Cu") (at 89 170)
    (pad "1" smd rect (at -6.35 0) (size 1.6 3.2) (layers "F.Cu" "F.Mask") (net 1 "1.0V_HEX_REF"))
    (pad "2" smd rect (at -3.81 0) (size 1.6 3.2) (layers "F.Cu" "F.Mask") (net 2 "GND_RT_2OZ"))
    (pad "3" smd rect (at -1.27 0) (size 1.6 3.2) (layers "F.Cu" "F.Mask") (net 3 "HX_SIG_1"))
    (pad "4" smd rect (at  1.27 0) (size 1.6 3.2) (layers "F.Cu" "F.Mask") (net 4 "HX_SIG_2"))
    (pad "5" smd rect (at  3.81 0) (size 1.6 3.2) (layers "F.Cu" "F.Mask") (net 5 "HX_MOD_ID"))
    (pad "6" smd rect (at  6.35 0) (size 1.6 3.2) (layers "F.Cu" "F.Mask") (net 6 "THERMAL_SYNC"))
  )

  ;; Protected 0.0625V-Step Hex Signal Traces (No Crossings)
  (segment (start 87.73 170) (end 87.73 110) (width 0.35) (layer "F.Cu") (net 3))
  (segment (start 90.27 170) (end 90.27 110) (width 0.35) (layer "F.Cu") (net 4))

  ;; RTGuardRing Ground Shield Zone around Hex Bus
  (zone (net 2) (net_name "GND_RT_2OZ") (layer "F.Cu")
    (hatch edge 0.5)
    (connect_pads (clearance 0.3))
    (min_thickness 0.25)
    (polygon
      (pts
        (xy 78 105) (xy 100 105) (xy 100 166) (xy 78 166)
      )
    )
  )
)
"""

if __name__ == "__main__":
    out_pcb = Path("tricorder_rt_mainboard.kicad_pcb")
    out_pcb.write_text(KICAD_PCB_CONTENT, encoding="utf-8")
    print(f"Generated KiCad PCB layout: {out_pcb.resolve()}")
