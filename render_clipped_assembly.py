import bpy
import mathutils
import os
import sys


arguments = sys.argv[sys.argv.index("--") + 1:]
part_a_path, part_b_path, output_prefix = arguments[:3]
transform_source = len(arguments) > 3 and arguments[3] == "yes"
bpy.ops.wm.read_factory_settings(use_empty=True)


def import_part(path, name, color):
    bpy.ops.wm.stl_import(filepath=os.path.abspath(path))
    part = bpy.context.active_object
    part.name = name
    if transform_source:
        part.scale = (125.5 / 110, 419.5 / 395, 1)
        part.location = (-62.75, 209.75, 4.6)
    material = bpy.data.materials.new(f"{name} PLA")
    material.diffuse_color = (*color, 1)
    material.roughness = 0.35
    part.data.materials.append(material)
    return part


part_a = import_part(part_a_path, "Part A", (0.04, 0.32, 0.52))
part_b = import_part(part_b_path, "Part B", (0.08, 0.55, 0.38))

bpy.ops.object.camera_add()
camera = bpy.context.active_object
bpy.context.scene.camera = camera

scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.studio_light = "paint.sl"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = "BOTH"
scene.display.shading.background_type = "VIEWPORT"
scene.display.shading.background_color = (0.9, 0.9, 0.9)
scene.render.resolution_x = 1200
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"


def render(name, location, target, lens):
    camera.location = location
    camera.data.lens = lens
    camera.rotation_euler = (mathutils.Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.abspath(f"build/{output_prefix}_{name}.png")
    bpy.ops.render.render(write_still=True)


render("assembled", (330, -475, 335), (0, 0, 25), 54)
render("joint", (235, -175, 115), (0, 0, 35), 60)

part_a.location.x = -7
part_b.location.x = 7
render("exploded", (300, -370, 265), (0, 0, 25), 58)
render("underside_exploded", (300, -370, -230), (0, 0, 8), 58)
