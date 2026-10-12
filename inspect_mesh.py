import bpy
import sys

path = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath=path)
obj = bpy.context.active_object
print("FILE", path)
print("DIMENSIONS_MM", *(round(value, 3) for value in obj.dimensions))
print("BOUNDS_MIN", *(round(min(corner[i] for corner in obj.bound_box), 3) for i in range(3)))
print("BOUNDS_MAX", *(round(max(corner[i] for corner in obj.bound_box), 3) for i in range(3)))
print("VERTICES", len(obj.data.vertices), "TRIANGLES", len(obj.data.polygons))
