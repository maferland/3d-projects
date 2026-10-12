import bpy
import mathutils
import os
import sys


part_a_path, part_b_path, output_name, transform_source = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True)


def import_part(path, name, color):
    bpy.ops.wm.stl_import(filepath=os.path.abspath(path))
    part = bpy.context.active_object
    part.name = name
    if transform_source == "yes":
        part.scale = (125.5 / 110, 419.5 / 395, 1)
        part.location = (-62.75, 209.75, 4.6)
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*color, 1)
    part.data.materials.append(material)
    return part


part_a = import_part(part_a_path, "A", (0.05, 0.32, 0.55))
part_b = import_part(part_b_path, "B", (0.08, 0.58, 0.38))
part_a.location.y -= 28
part_b.location.y += 28

bpy.ops.object.camera_add(location=(420, 0, 40))
camera = bpy.context.active_object
camera.data.type = "ORTHO"
camera.data.ortho_scale = 190
camera.rotation_euler = (mathutils.Vector((0, 0, 31)) - camera.location).to_track_quat("-Z", "Y").to_euler()

scene = bpy.context.scene
scene.camera = camera
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "FLAT"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = False
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = "WORLD"
scene.display.shading.background_type = "VIEWPORT"
scene.display.shading.background_color = (0.92, 0.92, 0.92)
scene.render.resolution_x = 1200
scene.render.resolution_y = 700
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = os.path.abspath(f"build/{output_name}.png")
bpy.ops.render.render(write_still=True)
