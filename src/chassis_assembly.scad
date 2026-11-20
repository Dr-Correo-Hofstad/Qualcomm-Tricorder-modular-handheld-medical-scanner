// RT Hexadecimal Medical Scanner Enclosure (OpenSCAD)
$fn = 60;

// Handheld Main Chassis Dimensions (mm)
body_w = 88;
body_h = 156;
body_d = 26; // Extra depth for RT 3D Vapor Chamber & battery
corner_r = 12;
wall = 2.5;

// Display & Dock Dimensions
scr_w = 56;
scr_h = 86;
dock_w = 34;
dock_h = 10;
dock_d = 6;

module rounded_chassis(w, h, d, r) {
    hull() {
        for (x = [-w/2 + r, w/2 - r])
            for (y = [-h/2 + r, h/2 - r])
                translate([x, y, 0])
                    cylinder(h = d, r = r);
    }
}

module hex_pogo_dock() {
    // Recessed 6-pin hex bus + alignment magnet pockets
    cube([dock_w, dock_h, dock_d], center = true);
    for (x = [-dock_w/2 - 4, dock_w/2 + 4]) {
        translate([x, 0, 0])
            cylinder(h = dock_d, r = 3.1, center = true); // 6mm neodymium magnet
    }
}

module main_scanner_body() {
    difference() {
        rounded_chassis(body_w, body_h, body_d, corner_r);
        
        // Internal cavity for 8-layer RT PCB & thermal armor
        translate([0, 0, wall])
            rounded_chassis(body_w - wall*2, body_h - wall*2, body_d, corner_r - wall);
        
        // Touchscreen cutout
        translate([0, 18, -1])
            cube([scr_w, scr_h, wall + 2], center = true);
            
        // Bottom Hex-Bus Pogo Dock (Blood / Gut / Temp modules)
        translate([0, -body_h/2 + dock_h/2 - 0.1, body_d/2])
            hex_pogo_dock();
            
        // Side centrifugal exhaust vents for RT cooling
        for (y = [-20, -10, 0, 10, 20]) {
            translate([body_w/2 - wall/2, y, body_d/2])
                cube([wall + 2, 3, 10], center = true);
        }
    }
}

main_scanner_body();
