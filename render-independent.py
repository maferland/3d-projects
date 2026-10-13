from pathlib import Path
import numpy as np
import trimesh
import matplotlib.pyplot as plt


exports = Path("independent-exports")
models = {half: trimesh.load_mesh(exports / f"cutlery_{half}.stl") for half in ["A", "B"]}


def render(name, camera, exploded=False, detail=False):
    view = np.asarray(camera, dtype=float)
    view /= np.linalg.norm(view)
    right = np.cross([0, 0, 1], view)
    right /= np.linalg.norm(right)
    up = np.cross(view, right)
    transform = np.array([right, up, view]).T
    items = []
    for half, color in [("A", [0.09, 0.43, 0.65]), ("B", [0.12, 0.57, 0.38])]:
        triangles = models[half].triangles.copy()
        normals = models[half].face_normals
        if detail:
            selected = (triangles[:, :, 1].max(axis=1) > -35) & (triangles[:, :, 1].min(axis=1) < 55)
            triangles, normals = triangles[selected], normals[selected]
        if exploded:
            triangles[:, :, 1] += -15 if half == "A" else 15
        items.append((triangles @ transform, normals, np.asarray(color)))
    projected = np.concatenate([item[0].reshape(-1, 3) for item in items])
    low, high = projected[:, :2].min(axis=0), projected[:, :2].max(axis=0)
    image_width, image_height = 1400, 850
    scale = min((image_width-100)/(high[0]-low[0]), (image_height-100)/(high[1]-low[1]))
    center = (low+high)/2
    canvas = np.full((image_height, image_width, 3), [0.94, 0.95, 0.97])
    depth = np.full((image_height, image_width), -np.inf)
    light = np.array([0.3, -0.5, 0.8])
    light /= np.linalg.norm(light)
    for triangles, normals, color in items:
        triangles[:, :, 0] = (triangles[:, :, 0]-center[0])*scale+image_width/2
        triangles[:, :, 1] = -(triangles[:, :, 1]-center[1])*scale+image_height/2
        for triangle, normal in zip(triangles, normals):
            x0, y0 = np.floor(triangle[:, :2].min(axis=0)).astype(int)
            x1, y1 = np.ceil(triangle[:, :2].max(axis=0)).astype(int)
            x0, y0, x1, y1 = max(x0,0), max(y0,0), min(x1,image_width-1), min(y1,image_height-1)
            if x1 < x0 or y1 < y0:
                continue
            first, second, third = triangle
            denominator = (second[1]-third[1])*(first[0]-third[0])+(third[0]-second[0])*(first[1]-third[1])
            if abs(denominator) < 1e-8:
                continue
            pixels_y, pixels_x = np.mgrid[y0:y1+1, x0:x1+1]
            pixels_x, pixels_y = pixels_x+0.5, pixels_y+0.5
            weight_a = ((second[1]-third[1])*(pixels_x-third[0])+(third[0]-second[0])*(pixels_y-third[1]))/denominator
            weight_b = ((third[1]-first[1])*(pixels_x-third[0])+(first[0]-third[0])*(pixels_y-third[1]))/denominator
            weight_c = 1-weight_a-weight_b
            pixel_depth = weight_a*first[2]+weight_b*second[2]+weight_c*third[2]
            region = depth[y0:y1+1, x0:x1+1]
            visible = (weight_a >= -1e-7) & (weight_b >= -1e-7) & (weight_c >= -1e-7) & (pixel_depth > region)
            region[visible] = pixel_depth[visible]
            brightness = 0.55+0.45*max(0, np.dot(normal,light))
            canvas[y0:y1+1, x0:x1+1][visible] = color*brightness
    plt.imsave(exports / f"{name}.png",canvas)


render("assembled", [300,-420,330])
render("joint", [300,-380,260], exploded=True, detail=True)
render("underside", [300,-420,-280])
