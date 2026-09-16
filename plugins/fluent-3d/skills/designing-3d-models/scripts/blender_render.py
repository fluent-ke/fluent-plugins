"""Headless product render of coloured STL parts (exported in place, millimetres).

  Blender -b -P blender_render.py -- OUT.png PART.stl:#RRGGBB [PART.stl:#RRGGBB ...]

Matte-plastic materials in the given sRGB colours, a soft studio light on a warm ground,
front three-quarter camera. Cycles on the first GPU backend that has a device (OptiX, CUDA, HIP,
oneAPI, Metal), else CPU. The Blender binary on macOS is /Applications/Blender.app/Contents/MacOS/Blender.
"""
import math
import sys

import bpy
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
out, parts = args[0], [a.rsplit(":", 1) for a in args[1:]]

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


def linear(hex_colour):
    channels = (int(hex_colour.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels) + (1.0,)


def material(name, hex_colour, roughness):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = linear(hex_colour)
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


objects = []
for path, colour in parts:
    bpy.ops.wm.stl_import(filepath=path)
    obj = bpy.context.selected_objects[0]
    obj.scale = (0.001, 0.001, 0.001)  # STL millimetres -> scene metres
    obj.data.materials.append(material(obj.name, colour, 0.55))
    objects.append(obj)
bpy.context.view_layer.update()

corners = [obj.matrix_world @ Vector(c) for obj in objects for c in obj.bound_box]
low = Vector((min(p.x for p in corners), min(p.y for p in corners), min(p.z for p in corners)))
high = Vector((max(p.x for p in corners), max(p.y for p in corners), max(p.z for p in corners)))
centre, size = (low + high) / 2, max(high - low)

bpy.ops.mesh.primitive_plane_add(size=size * 30, location=(centre.x, centre.y, low.z))
bpy.context.object.data.materials.append(material("ground", "#E9E6DE", 0.9))


def add(obj_data, name, location):
    obj = bpy.data.objects.new(name, obj_data)
    scene.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (centre - obj.location).to_track_quat("-Z", "Y").to_euler()
    return obj


camera = bpy.data.cameras.new("camera")
camera.lens = 85
scene.camera = add(camera, "camera", centre + Vector((0.25, -1.0, 1.05)).normalized() * size * 3.4)

# Light power must scale with distance squared: small products sit ~0.3 m from the lights, and the
# room-scale energies Blender defaults to (tens of watts and up) blow black plastic out to grey.
distance = size * 4
key = bpy.data.lights.new("key", "AREA")
key.energy, key.size = 45 * distance ** 2, size * 5
add(key, "key", centre + Vector((-1.0, -0.8, 1.6)).normalized() * distance)
fill = bpy.data.lights.new("fill", "AREA")
fill.energy, fill.size = 12 * distance ** 2, size * 6
add(fill, "fill", centre + Vector((1.2, 0.4, 0.9)).normalized() * distance)

world = bpy.data.worlds.new("world")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = linear("#F5F4EE")
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.15
scene.world = world

scene.view_settings.view_transform = "Standard"  # AgX (the default) desaturates brand colours
scene.view_settings.exposure = -1.1  # Standard has no highlight roll-off; keeps cream and coral from clipping
scene.render.engine = "CYCLES"
scene.cycles.samples = 128
scene.cycles.use_denoising = True
prefs = bpy.context.preferences.addons["cycles"].preferences
for backend in ("OPTIX", "CUDA", "HIP", "ONEAPI", "METAL"):
    try:
        prefs.compute_device_type = backend  # raises TypeError when this build lacks the backend
        prefs.get_devices()
    except (TypeError, RuntimeError):
        continue
    if any(device.type != "CPU" for device in prefs.devices):
        for device in prefs.devices:
            device.use = True
        scene.cycles.device = "GPU"
        print("Rendering on GPU:", backend)
        break
else:
    print("No GPU backend available, rendering on CPU")
scene.render.resolution_x, scene.render.resolution_y = 1600, 1200
scene.render.filepath = out
bpy.ops.render.render(write_still=True)
print("RENDER_OK", out)
