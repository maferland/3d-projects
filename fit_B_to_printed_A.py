from pathlib import Path
import hashlib
import json
import manifold3d
import numpy as np
import trimesh


root = Path(__file__).resolve().parent
build = root / "build"
part_a_path = build / "compact_cutlery_tray_3x10_inverted_dividers_A.stl"
part_b_path = build / "compact_cutlery_tray_3x10_inverted_dividers_B.stl"
output_path = build / "compact_cutlery_tray_B_receiver_v2.stl"


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
added_joint = added_a ^ joint_bounds
clearance = 0.25
receiver = added_joint.minkowski_sum(
    manifold3d.Manifold.cube((2 * clearance,) * 3, center=True)
)
contact_relief = (solid_a ^ joint_bounds).minkowski_sum(
    manifold3d.Manifold.cube((0.1,) * 3, center=True)
)
revised_b = (solid_b - receiver - contact_relief).simplify(0.001)
result = mesh(revised_b)
result = trimesh.util.concatenate([
    component for component in result.split(only_watertight=False)
    if abs(component.volume) > 0.000001
])
assert result.is_watertight
assert (solid_a ^ manifold(result)).volume() < 0.001
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
    "output": str(output_path),
}
(build / "B_receiver_v2_fit_report.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
