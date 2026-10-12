import bpy
import math
import mathutils
import os
import sys

arguments = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
source = os.path.abspath(arguments[0] if arguments else "build/compact_cutlery_tray_3x10_gridfinity_full.stl")
output_prefix = arguments[1] if len(arguments) > 1 else "compact_cutlery_tray_3x10"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath=source)
tray = bpy.context.active_object

material = bpy.data.materials.new("Blue PLA")
material.diffuse_color = (0.055, 0.24, 0.36, 1.0)
material.metallic = 0.0
material.roughness = 0.32
tray.data.materials.append(material)

bpy.ops.object.light_add(type="AREA", location=(180, -120, 330))
bpy.context.active_object.data.energy = 1500
bpy.context.active_object.data.shape = "DISK"
bpy.context.active_object.data.size = 250
bpy.ops.object.light_add(type="AREA", location=(-180, 100, 180))
bpy.context.active_object.data.energy = 900
bpy.context.active_object.data.size = 220

bpy.ops.object.camera_add(location=(330, -500, 360))
camera = bpy.context.active_object
bpy.context.scene.camera = camera


def point_camera(target):
    camera.rotation_euler = (mathutils.Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()


point_camera((0, 0, 25))
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.studio_light = "paint.sl"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = "BOTH"
scene.display.shading.background_type = "VIEWPORT"
scene.display.shading.background_color = (0.92, 0.92, 0.92)
scene.render.resolution_x = 900
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = os.path.abspath(f"build/{output_prefix}_preview.png")
scene.render.film_transparent = False
bpy.ops.render.render(write_still=True)

tray.rotation_euler.x = math.radians(180)
camera.location = (300, -480, 320)
point_camera((0, 0, -20))
scene.render.filepath = os.path.abspath(f"build/{output_prefix}_underside.png")
bpy.ops.render.render(write_still=True)
