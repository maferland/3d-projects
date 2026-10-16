from pathlib import Path
import hashlib
import json
import argparse
import manifold3d
import numpy as np
import trimesh


parser = argparse.ArgumentParser(description="Clear B against a reference A while protecting the original clips.")
parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parent)
parser.add_argument("--part-a", type=Path)
parser.add_argument("--part-b", type=Path)
parser.add_argument("--output", type=Path)
parser.add_argument("--report", type=Path)
arguments = parser.parse_args()
root = arguments.root.resolve()
build = root / "build"
part_a_path = arguments.part_a or build / "compact_cutlery_tray_3x10_inverted_dividers_A.stl"
part_b_path = arguments.part_b or build / "compact_cutlery_tray_3x10_inverted_dividers_B.stl"
output_path = arguments.output or build / "compact_cutlery_tray_B_original_clips_v3.stl"
report_path = arguments.report or build / "B_original_clips_v3_fit_report.json"


def manifold(mesh):
    return manifold3d.Manifold(manifold3d.Mesh(
        np.asarray(mesh.vertices, dtype=np.float32),
        np.asarray(mesh.faces, dtype=np.uint32),
    ))


def mesh(solid):
    result = solid.to_mesh()
    output = trimesh.Trimesh(result.vert_properties[:, :3], result.tri_verts)
    output.merge_vertices()
    return output


part_a = trimesh.load_mesh(part_a_path)
part_b = trimesh.load_mesh(part_b_path)
original_a = trimesh.load_mesh(root / "source/CutleryDrawA.stl")
original_a.apply_scale([125.5 / 110, 419.5 / 395, 1])
original_a.apply_translation([-62.75, 209.75, 4.6])

solid_a = manifold(part_a)
solid_b = manifold(part_b)
added_a = solid_a - manifold(original_a)
joint_bounds = manifold3d.Manifold.cube((130, 46, 66), center=True).translate((0, 0, 31))
divider_region = manifold3d.Manifold.cube((4.4, 46, 66), center=True).translate((0, 0, 31))
backing_region = manifold3d.Manifold.cube((130, 46, 9), center=True).translate((0, 0, 3.5))
repair_region = divider_region + backing_region
added_joint = added_a ^ joint_bounds ^ repair_region
clearance = 0.25
receiver = added_joint.minkowski_sum(
    manifold3d.Manifold.cube((2 * clearance,) * 3, center=True)
)
contact_relief = (solid_a ^ joint_bounds ^ repair_region).minkowski_sum(
    manifold3d.Manifold.cube((0.1,) * 3, center=True)
)
revised_b = (solid_b - receiver - contact_relief).simplify(0.00001)
result = mesh(revised_b)
result = trimesh.util.concatenate([
    component for component in result.split(only_watertight=False)
    if abs(component.volume) > 0.000001
])
assert result.is_watertight
assert (solid_a ^ manifold(result)).volume() < 0.001
clip_regions = manifold3d.Manifold.cube((7, 46, 46), center=True).translate((61.5, 0, 35))
clip_regions += manifold3d.Manifold.cube((7, 46, 46), center=True).translate((-61.5, 0, 35))
clip_change = ((solid_b ^ clip_regions) - (manifold(result) ^ clip_regions)).volume()
assert abs(clip_change) < 0.001
result.export(output_path)

before = (solid_a ^ solid_b).volume()
after = (solid_a ^ revised_b).volume()
report = {
    "printed_A_sha256": hashlib.sha256(part_a_path.read_bytes()).hexdigest(),
    "B_input_sha256": hashlib.sha256(part_b_path.read_bytes()).hexdigest(),
    "clearance_mm": clearance,
    "collision_before_mm3": before,
    "collision_after_mm3": after,
    "removed_B_mm3": solid_b.volume() - revised_b.volume(),
    "dimensions_mm": result.extents.tolist(),
    "watertight": bool(result.is_watertight),
    "original_clip_material_removed_mm3": clip_change,
    "output": str(output_path),
}
if arguments.part_a:
    report["reference_A_sha256"] = report.pop("printed_A_sha256")
report_path.write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
