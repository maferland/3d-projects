// Independently constructed geometry. No imported source meshes.
part = "A"; // A, B, coupon_A, coupon_B, assembled
width = 125.5;
depth = 419.5;
height = 61.6;
wall = 2.4;
base_z = 4.6;
floor_z = 6.6;
pitch = depth / 4;
divider_width = 3.4;
joint_gap = 0.3;
joint_slope = 0.38;
joint_top_y = joint_slope * (height - floor_z);
$fn = 32;

module rounded_rectangle(size, radius) {
    offset(r=radius)
        square([size[0]-2*radius, size[1]-2*radius], center=true);
}

module foot() {
    linear_extrude(height=0.8, scale=37.2/35.6)
        rounded_rectangle([35.6,35.6],3.75);
    translate([0,0,0.8]) linear_extrude(height=1.8)
        rounded_rectangle([37.2,37.2],4.55);
    translate([0,0,2.6]) linear_extrude(height=2.15,scale=41.5/37.2)
        rounded_rectangle([37.2,37.2],4.55);
}

module feet(half) {
    for(column=[-1:1],row=[0:4])
        translate([column*42,(row+(half=="A" ? 0 : 5)-4.5)*42,0]) foot();
}

module slope_solid(span, low_y, high_y, low_z, high_z, thickness) {
    polyhedron(
        points=[
            [-span/2,low_y,low_z], [span/2,low_y,low_z],
            [span/2,high_y,high_z], [-span/2,high_y,high_z],
            [-span/2,low_y,low_z-thickness], [span/2,low_y,low_z-thickness],
            [span/2,high_y,high_z-thickness], [-span/2,high_y,high_z-thickness]
        ],
        faces=[[0,1,2,3],[7,6,5,4],[4,5,1,0],[5,6,2,1],[6,7,3,2],[7,4,0,3]]
    );
}

module ramp(index) {
    start = -depth/2 + index*pitch;
    end_y = start+pitch-(index==3 ? wall+2 : 1);
    slope_solid(width-2*wall+0.4,start+wall,end_y,8.6,height-2,2.4);
}

module front_tunnel_divider() {
    low_y = -depth/2+wall;
    high_y = -depth/2+pitch-1;
    low_top = 7.4;
    high_top = height-3.2;
    polyhedron(
        points=[
            [-divider_width/2,low_y,6.4],[divider_width/2,low_y,6.4],
            [divider_width/2,high_y,6.4],[-divider_width/2,high_y,6.4],
            [-divider_width/2,low_y,low_top],[divider_width/2,low_y,low_top],
            [divider_width/2,high_y,high_top],[-divider_width/2,high_y,high_top]
        ],
        faces=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]
    );
    translate([-divider_width/2,high_y,6.4]) cube([divider_width,1.4,height-6.4]);
}

module mirrored_sides() {
    children();
    mirror([1,0,0]) children();
}

module outside_clip() {
    // B's cantilever occupies A's recessed outer wall, within the 3U envelope.
    translate([width/2-1.2,-12,25]) cube([1.1,27,6]);
    translate([0,0,25]) linear_extrude(height=6)
        polygon([[width/2-1.2,-11],[width/2-1.65,-9],
            [width/2-1.65,-7],[width/2-1.2,-7]]);
}

module outside_receiver() {
    translate([width/2-1.45,-12.3,24.75]) cube([1.7,27.6,6.5]);
    // Catch pocket: only 0.2 mm outward flex is needed to pass the entry lip.
    translate([width/2-1.75,-11.25,24.75]) cube([0.7,4.5,6.5]);
}

module continuous_tray() {
        union() {
            translate([0,0,base_z]) linear_extrude(height=2)
                rounded_rectangle([width,depth],8);
            translate([0,0,6.4]) linear_extrude(height=height-6.4)
                difference() {
                    rounded_rectangle([width,depth],8);
                    rounded_rectangle([width-2*wall,depth-2*wall],8-wall);
                }
            for(index=[0:3]) ramp(index);
            translate([-divider_width/2,-depth/2+pitch-0.2,6.4])
                cube([divider_width,depth-pitch-wall+0.2,height-6.4]);
            front_tunnel_divider();
        }
}

module diagonal_bounds(half) {
    // Extrude a y/z profile along x.
    seam = half=="A" ? -joint_gap/2 : joint_gap/2;
    translate([-width,0,0]) rotate([90,0,90]) linear_extrude(height=2*width)
        polygon(half=="A" ?
            [[-depth,-1],[seam,-1],[seam,floor_z],
             [joint_top_y+seam,height+0.1],[-depth,height+0.1]] :
            [[seam,-1],[depth,-1],[depth,height+0.1],
             [joint_top_y+seam,height+0.1],[seam,floor_z]]);
}

module tray_half(half) {
    union() {
        difference() {
            intersection() {
                continuous_tray();
                diagonal_bounds(half);
            }
            if(half=="A") mirrored_sides() outside_receiver();
        }
        feet(half);
        if(half=="B") mirrored_sides() outside_clip();
    }
}

module coupon(half) {
    intersection() {
        tray_half(half);
        translate([-width,-25,-1]) cube([2*width,73,height+2]);
    }
}

if(part=="coupon_A") coupon("A");
else if(part=="coupon_B") coupon("B");
else if(part=="assembled") {
    tray_half("A");
    tray_half("B");
} else tray_half(part);
