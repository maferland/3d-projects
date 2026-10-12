// Elumara lamp-base mold box
// Export two copies of each panel. Units: mm.

part = "long"; // "long", "short", or "layout"

inside_width = 175;
inside_height = 90;
skin = 1.2;
rib_depth = 3;
rib_width = 4;
corner_overlap = 3;

module ribbed_panel(width) {
    union() {
        cube([width, inside_height, skin]);

        // Perimeter ribs resist bowing under silicone pressure.
        cube([width, rib_width, rib_depth]);
        translate([0, inside_height - rib_width, 0])
            cube([width, rib_width, rib_depth]);
        cube([rib_width, inside_height, rib_depth]);
        translate([width - rib_width, 0, 0])
            cube([rib_width, inside_height, rib_depth]);

        for (x = [30 : 30 : width - 20])
            translate([x, 0, 0]) cube([rib_width, inside_height, rib_depth]);

        for (y = [30 : 30 : inside_height - 20])
            translate([0, y, 0]) cube([width, rib_width, rib_depth]);
    }
}

module long_panel() {
    ribbed_panel(inside_width + 2 * corner_overlap);
}

module short_panel() {
    ribbed_panel(inside_width);
}

if (part == "long") {
    long_panel();
} else if (part == "short") {
    short_panel();
} else {
    long_panel();
    translate([0, inside_height + 8, 0]) long_panel();
    translate([inside_width + 2 * corner_overlap + 8, 0, 0]) short_panel();
    translate([inside_width + 2 * corner_overlap + 8, inside_height + 8, 0])
        short_panel();
}
