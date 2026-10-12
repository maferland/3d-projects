import bpy
import mathutils
import os
import sys


source = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
output_prefix = sys.argv[sys.argv.index("--") + 2]

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath=source)
tray = bpy.context.active_object

material = bpy.data.materials.new("Orange PLA")
material.diffuse_color = (0.82, 0.24, 0.035, 1)
material.roughness = 0.38
tray.data.materials.append(material)

for location, energy, size in [((160, -80, 240), 1300, 180), ((-120, 120, 160), 800, 150)]:
    bpy.ops.object.light_add(type="AREA", location=location)
    light = bpy.context.active_object
    light.data.energy = energy
    light.data.size = size

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
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"


def render(name, camera_location, target, lens=62):
    camera.location = camera_location
    camera.data.lens = lens
    camera.rotation_euler = (mathutils.Vector(target) - camera.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.abspath(f"build/{output_prefix}_{name}.png")
    bpy.ops.render.render(write_still=True)


render("oblique", (185, -80, 115), (0, 3, 37), 68)
render("opposite", (-185, 25, 105), (0, 3, 37), 68)
render("top", (0, 0, 420), (0, 0, 0), 60)
render("front_bucket", (165, -315, 115), (0, -155, 38), 62)

bpy.context.view_layer.objects.active = tray
tray.select_set(True)
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.mesh.bisect(
    plane_co=(0, 0, 0),
    plane_no=(1, 0, 0),
    use_fill=False,
    clear_outer=True,
)
bpy.ops.object.mode_set(mode="OBJECT")
render("center_cutaway", (245, -35, 95), (0, 0, 32), 58)
