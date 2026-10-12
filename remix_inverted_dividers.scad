source_file = "source.stl";
source_y_min = -395;
source_y_max = 0;
plate_source_y_min = source_y_min;
plate_source_y_max = source_y_max;
first_foot_row = 0;
last_foot_row = 9;

source_width = 110;
source_depth = 395;
target_width = 3 * 42 - 0.5;
target_depth = 10 * 42 - 0.5;
width_scale = target_width / source_width;
depth_scale = target_depth / source_depth;
tray_z_offset = 4.6;
tray_top_z = 57 + tray_z_offset;
$fn = 24;

function transformed_y(source_y) = source_y * depth_scale + target_depth / 2;
function transformed_z(source_z) = source_z + tray_z_offset;


module rounded_square(size, radius) {
    offset(r = radius)
        square([size[0] - 2 * radius, size[1] - 2 * radius], center = true);
}


module gridfinity_foot() {
    union() {
        linear_extrude(height = 0.8, scale = 37.2 / 35.6)
            rounded_square([35.6, 35.6], 3.75);
        translate([0, 0, 0.8])
            linear_extrude(height = 1.8)
                rounded_square([37.2, 37.2], 4.55);
        translate([0, 0, 2.6])
            linear_extrude(height = 2.15, scale = 41.5 / 37.2)
                rounded_square([37.2, 37.2], 4.55);
    }
}


module selected_gridfinity_feet() {
    for (column = [0:2], row = [first_foot_row:last_foot_row])
        translate([
            (column - 1) * 42,
            (row - 4.5) * 42,
            0
        ]) gridfinity_foot();
}


module transformed_source() {
    translate([-target_width / 2, target_depth / 2, tray_z_offset])
        scale([width_scale, depth_scale, 1])
            import(source_file, convexity = 10);
}


module continuous_bottom_plate() {
    intersection() {
        translate([0, 0, tray_z_offset])
            linear_extrude(height = 1.8)
                rounded_square([target_width, target_depth], 8);
        translate([
            -target_width,
            transformed_y(plate_source_y_min),
            tray_z_offset - 0.1
        ]) cube([
            2 * target_width,
            transformed_y(plate_source_y_max) - transformed_y(plate_source_y_min),
            2
        ]);
    }
}


module wedge(width, source_y_low, source_y_high, source_z_low, source_z_high, top_z) {
    half_width = width / 2;
    y_low = transformed_y(source_y_low);
    y_high = transformed_y(source_y_high);
    z_low = transformed_z(source_z_low);
    z_high = transformed_z(source_z_high);
    polyhedron(
        points = [
            [-half_width, y_low, z_low], [half_width, y_low, z_low],
            [half_width, y_high, z_high], [-half_width, y_high, z_high],
            [-half_width, y_low, top_z], [half_width, y_low, top_z],
            [half_width, y_high, top_z], [-half_width, y_high, top_z]
        ],
        faces = [
            [0, 3, 2, 1], [4, 5, 6, 7],
            [0, 1, 5, 4], [1, 2, 6, 5],
            [2, 3, 7, 6], [3, 0, 4, 7]
        ],
        convexity = 4
    );
}


module sloped_plate(width, source_y_low, source_y_high, source_z_low, source_z_high, thickness) {
    half_width = width / 2;
    y_low = transformed_y(source_y_low);
    y_high = transformed_y(source_y_high);
    z_low = transformed_z(source_z_low);
    z_high = transformed_z(source_z_high);
    polyhedron(
        points = [
            [-half_width, y_low, z_low], [half_width, y_low, z_low],
            [half_width, y_high, z_high], [-half_width, y_high, z_high],
            [-half_width, y_low, z_low - thickness], [half_width, y_low, z_low - thickness],
            [half_width, y_high, z_high - thickness], [-half_width, y_high, z_high - thickness]
        ],
        faces = [
            [0, 3, 2, 1], [4, 5, 6, 7],
            [0, 1, 5, 4], [1, 2, 6, 5],
            [2, 3, 7, 6], [3, 0, 4, 7]
        ],
        convexity = 4
    );
}


module divider(root_y) {
    source_y_low = max(root_y - 1, source_y_min);
    source_y_high = min(root_y + 100.3, source_y_max);
    if (source_y_high - source_y_low >= 30)
        translate([
            -1.7,
            transformed_y(source_y_low),
            tray_z_offset - 0.2
        ]) cube([
            3.4,
            transformed_y(source_y_high) - transformed_y(source_y_low),
            tray_top_z - tray_z_offset + 0.2
        ]);
}


module under_slope_divider(root_y) {
    source_y_low = max(root_y - 98.5, source_y_min);
    source_y_high = min(root_y + 1, source_y_max);
    bottom_z = tray_z_offset - 0.2;
    top_z_low = transformed_z(0.577 * (source_y_low - (root_y - 99)));
    top_z_high = min(
        transformed_z(0.577 * (source_y_high - (root_y - 99))),
        tray_top_z
    );
    if (source_y_min < root_y - 90 && source_y_max > root_y)
        polyhedron(
            points = [
                [-1.7, transformed_y(source_y_low), bottom_z],
                [1.7, transformed_y(source_y_low), bottom_z],
                [1.7, transformed_y(source_y_high), bottom_z],
                [-1.7, transformed_y(source_y_high), bottom_z],
                [-1.7, transformed_y(source_y_low), top_z_low],
                [1.7, transformed_y(source_y_low), top_z_low],
                [1.7, transformed_y(source_y_high), top_z_high],
                [-1.7, transformed_y(source_y_high), top_z_high]
            ],
            faces = [
                [0, 3, 2, 1], [4, 5, 6, 7],
                [0, 1, 5, 4], [1, 2, 6, 5],
                [2, 3, 7, 6], [3, 0, 4, 7]
            ],
            convexity = 4
        );
}


module merged_front_floor() {
    source_y_low = max(-391, source_y_min);
    source_y_high = min(-299.24, source_y_max);
    if (source_y_low < source_y_high)
        sloped_plate(
            target_width - 11,
            source_y_low,
            source_y_high,
            0.577 * (source_y_low + 398) + 1.5,
            57,
            2
        );
}


module rear_ramp_bridge() {
    if (source_y_max > -50)
        translate([
            -target_width / 2 + 2,
            transformed_y(-95),
            tray_z_offset
        ]) cube([
            target_width - 4,
            transformed_y(-88) - transformed_y(-95),
            7.5
        ]);
}


union() {
    difference() {
        transformed_source();
        wedge(
            5,
            -391,
            -302,
            0.577 * (-391 + 398) - 0.8,
            0.577 * (-302 + 398) - 0.8,
            tray_top_z + 1
        );
    }
    merged_front_floor();
    divider(-299.24);
    under_slope_divider(-299.24);
    divider(-200.49);
    divider(-101.73);
    continuous_bottom_plate();
    rear_ramp_bridge();
    selected_gridfinity_feet();
}
