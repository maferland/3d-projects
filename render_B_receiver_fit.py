from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import trimesh


build = Path(__file__).resolve().parent / "build"
part_a = trimesh.load_mesh(build / "compact_cutlery_tray_3x10_inverted_dividers_A.stl")
part_b = trimesh.load_mesh(build / "compact_cutlery_tray_B_receiver_v2.stl")


def render(name, exploded):
    figure = plt.figure(figsize=(12, 8), facecolor="#eef1f5")
    axes = figure.add_subplot(111, projection="3d", facecolor="#eef1f5")
    for part, color, shift in [(part_a, "#2686b2", -15), (part_b, "#39a17d", 15)]:
        triangles = part.triangles.copy()
        selected = (triangles[:, :, 1].max(axis=1) > -48) & (triangles[:, :, 1].min(axis=1) < 48)
        triangles = triangles[selected]
        if exploded:
            triangles[:, :, 1] += shift
        collection = Poly3DCollection(triangles, facecolors=color, shade=True, linewidths=0)
        axes.add_collection3d(collection)
    axes.set_xlim(-65, 65)
    axes.set_ylim(-65, 65)
    axes.set_zlim(0, 65)
    axes.set_box_aspect((130, 130, 65))
    axes.view_init(elev=32, azim=-38)
    axes.set_axis_off()
    figure.suptitle("A (blue) + revised B (green) — joint detail" + (" / separated" if exploded else " / assembled"))
    figure.savefig(build / f"{name}.png", dpi=160, bbox_inches="tight")
    plt.close(figure)


render("B_receiver_v2_joint_assembled", False)
render("B_receiver_v2_joint_separated", True)
