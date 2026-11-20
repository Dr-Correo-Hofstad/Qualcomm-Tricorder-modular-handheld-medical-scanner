// Detachable Snap-Circuit Sensor Modules (Blood, Gut, IR Thermometer)
// Mates with the 6-pin hex pogo dock or operates air-gapped via Node B buffer
$fn = 60;

module rounded_pod(w, h, d, r) {
    hull() {
        for (x = [-w/2 + r, w/2 - r])
            for (y = [-h/2 + r, h/2 - r])
                translate([x, y, 0])
                    cylinder(h = d, r = r);
    }
}

module shock_grommets(w, h, d) {
    for (x = [-w/2 + 4, w/2 - 4])
        for (y = [-h/2 + 4, h/2 - 4])
            translate([x, y, 0])
                cylinder(h = d + 2, r = 2.1, center = true);
}

// Module 1: Optical Blood Analyzer Wand (PPG / SpO2)
module blood_analyzer_module() {
    difference() {
        rounded_pod(28, 72, 14, 6);
        translate([0, 0, 2])
            rounded_pod(24, 68, 14, 4);
        // Fingertip / skin optical sensor window
        translate([0, 22, -1])
            cylinder(h = 4, r = 5.5);
        // Node B Snap-Circuit shock isolation mounts
        translate([0, -15, 7])
            shock_grommets(22, 24, 14);
    }
}

// Module 2: Gastrointestinal / Acoustic Monitor Pad
module gut_monitor_module() {
    difference() {
        rounded_pod(46, 38, 13, 7);
        translate([0, 0, 2])
            rounded_pod(42, 34, 13, 5);
        // Acoustic diaphragm aperture
        translate([0, 0, -1])
            cylinder(h = 4, r = 11);
        translate([0, 0, 6.5])
            shock_grommets(38, 30, 13);
    }
}

// Module 3: Non-Contact IR Thermometer Head
module ir_thermometer_module() {
    difference() {
        rounded_pod(32, 42, 15, 6);
        translate([0, 0, 2])
            rounded_pod(28, 38, 15, 4);
        // Thermopile collimating cone
        translate([0, 10, -1])
            cylinder(h = 4, r1 = 6, r2 = 3.5);
    }
}

// Layout all three modules for 3D printing / assembly check
translate([-60, 0, 0]) blood_analyzer_module();
translate([0, 0, 0])   gut_monitor_module();
translate([60, 0, 0])  ir_thermometer_module();
