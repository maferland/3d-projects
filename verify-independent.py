from pathlib import Path
import json
import trimesh


exports = Path("independent-exports")
models = {name: trimesh.load_mesh(exports / f"cutlery_{name}.stl")
          for name in ["A", "B", "key", "coupon_A", "coupon_B"]}
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
    placed_key = models["key"].copy()
    placed_key.apply_translation([side * (125.5 / 2 - 3), 0.38 * (61.6 - 6.6), 61.6 - 5.25])
    for half in ["A", "B"]:
        assert overlap(models[half], placed_key) < 0.001
report["key_collisions_mm3"] = 0
for separation in [0, 0.5, 2, 10, 25]:
    moved_b = models["B"].copy()
    moved_b.apply_translation([0, separation, 0])
    assert overlap(models["A"], moved_b) < 0.001
report["straight_assembly_path_checked_mm"] = [0, 0.5, 2, 10, 25]
(exports / "verification.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
