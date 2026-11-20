// RT Hexadecimal + Snap-Circuit Medical Scanner Chassis (OpenSCAD)
// Integrates shocks.scad isolation mounts & RT thermal venting
$fn = 60;

// Main Handheld Dimensions (mm)
body_w = 90;
body_h = 160;
body_d = 28;
corner_r = 12;
wall = 2.5;

// Touchscreen & Snap-Circuit Buffer Bay
scr_w = 56;
scr_h = 86;
bay_w = 42;
bay_h = 24;
bay_d = 8;

module rounded_body(w, h, d, r) {
    hull() {
        for (x = [-w/2 + r, w/2 - r])
            for (y = [-h/2 + r, h/2 - r])
                translate([x, y, 0])
                    cylinder(h = d, r = r);
    }
}

// Shock-isolated pocket for Node A Double Latch Gate Buffer
module snap_buffer_bay() {
    difference() {
        cube([bay_w, bay_h, bay_d], center = true);
        // Corner mounts for shocks.scad rubber grommets
        for (x = [-bay_w/2 + 3, bay_w/2 - 3])
            for (y = [-bay_h/2 + 3, bay_h/2 - 3])
                translate([x, y, 0])
                    cylinder(h = bay_d + 2, r = 2.2, center = true);
    }
}

module main_scanner_chassis() {
    difference() {
        rounded_body(body_w, body_h, body_d, corner_r);
        
        // Internal cavity for 8-layer RT PCB + 3D Vapor Chamber
        translate([0, 0, wall])
            rounded_body(body_w - wall*2, body_h - wall*2, body_d, corner_r - wall);
            
        // Front Touchscreen Cutout
        translate([0, 22, -1])
            cube([scr_w, scr_h, wall + 2], center = true);
            
        // Lower Internal Recess for Snap-Circuit Buffer & Optical Transceiver
        translate([0, -48, wall + bay_d/2])
            snap_buffer_bay();
            
        // RT Centrifugal Exhaust Louvers
        for (y = [-15, -5, 5, 15, 25]) {
            translate([body_w/2 - wall/2, y, body_d/2])
                cube([wall + 2, 2.5, 10], center = true);
        }
    }
}

// Detachable Remote Sensor Pod (e.g., Blood Analyzer / Gut Monitor)
module remote_sensor_pod(pod_w = 36, pod_h = 54, pod_d = 14) {
    difference() {
        rounded_body(pod_w, pod_h, pod_d, 6);
        translate([0, 0, 2])
            rounded_body(pod_w - 4, pod_h - 4, pod_d, 4);
        // Sensor aperture on bottom face
        translate([0, 0, -1])
            cylinder(h = 4, r = 6);
    }
}

// Render Main Unit + Detached Sensor Pod side-by-side
main_scanner_chassis();
translate([75, -30, 0])
    remote_sensor_pod();
