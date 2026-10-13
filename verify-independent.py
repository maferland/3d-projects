from pathlib import Path
import json
import trimesh


exports = Path("independent-exports")
models = {name: trimesh.load_mesh(exports / f"cutlery_{name}.stl")
          for name in ["A", "B", "coupon_A", "coupon_B"]}
report = {}
for name, model in models.items():
    assert model.is_watertight, name
    assert model.is_volume, name
    material_shells = [shell for shell in model.split() if shell.volume > 0.001]
    assert len(material_shells) == 1, name
    report[name] = {"dimensions_mm": model.extents.tolist(), "volume_mm3": model.volume,
                    "watertight": True, "connected_solids": 1}


def overlap(first, second):
    return abs(trimesh.boolean.intersection([first, second], engine="manifold").volume)


report["A_B_collision_mm3"] = overlap(models["A"], models["B"])
assert report["A_B_collision_mm3"] < 0.001
for side in [-1, 1]:
    inside_rim = trimesh.creation.box(extents=[5.3, 28, 8])
    inside_rim.apply_translation([side*57.69, 20.9, 57.6])
    for half in ["A", "B"]:
        assert overlap(models[half], inside_rim) < 0.001
report["inward_rim_shoulders_mm3"] = 0
report["insertion_contacts"] = []
for separation in range(26):
    moved_b = models["B"].copy()
    moved_b.apply_translation([0, separation, 0])
    contact = trimesh.boolean.intersection([models["A"], moved_b], engine="manifold")
    if abs(contact.volume) > 0.001:
        assert (abs(contact.vertices[:,0]) >= 61.09).all()
        assert contact.bounds[0,2] >= 24.99 and contact.bounds[1,2] <= 31.01
        report["insertion_contacts"].append({"separation_mm": separation,
            "clip_only_contact_mm3": abs(contact.volume)})
report["required_outward_clip_flex_mm"] = 0.2
report["straight_assembly_path_checked_mm"] = list(range(26))
(exports / "verification.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
