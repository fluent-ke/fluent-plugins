"""Animate a model headless in Blender: a turntable orbit or a walkthrough along a path.

  blender -b -P animate_model.py -- OUT_DIR orbit MODEL [MODEL ...] [options]
  blender -b -P animate_model.py -- OUT_DIR path MODEL [MODEL ...] --path "x,y;x,y;..." [options]

MODEL: .stl .obj .ply .fbx .glb .gltf .usd/.usdz, or one .blend (opened as it is). STL with no
material takes --colour. Models from CAD are usually in millimetres: pass --scale 0.001 so the scene
is in metres. Path points are metres in the scene, walked at --eye height (default 1.6 m).

Options: --seconds 8 --fps 30 --size 1920x1080 --engine eevee|cycles --samples 64 --scale 1
         --colour #B9B4A8 --eye 1.6 --lens (35 orbit, 20 path) --still 1,120,240 (render only these frames, to check)
         --draft (half size, a quarter of the samples)

Writes OUT_DIR/scene.blend (open it in Blender to adjust), OUT_DIR/frames/0001.png ..., and, when
ffmpeg is on PATH, OUT_DIR/animation.mp4. --still writes OUT_DIR/still-N.png for each frame listed, and no video.
The Blender binary on macOS is /Applications/Blender.app/Contents/MacOS/Blender.
"""
import argparse
import math
import os
import shutil
import subprocess
import sys

import bpy
from mathutils import Vector

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("mode", choices=["orbit", "path"])
ap.add_argument("models", nargs="+")
ap.add_argument("--path", default="")
ap.add_argument("--seconds", type=float, default=8)
ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--size", default="1920x1080")
ap.add_argument("--engine", choices=["eevee", "cycles"], default="eevee")
ap.add_argument("--samples", type=int, default=64)
ap.add_argument("--scale", type=float, default=1.0)
ap.add_argument("--colour", default="#B9B4A8")
ap.add_argument("--eye", type=float, default=1.6)
ap.add_argument("--lens", type=float)
ap.add_argument("--still", help="comma-separated frame numbers")
ap.add_argument("--draft", action="store_true")
a = ap.parse_args(sys.argv[sys.argv.index("--") + 1:])
a.lens = a.lens or (35 if a.mode == "orbit" else 20)  # interiors need a wide lens at eye height
out = os.path.abspath(a.out)
os.makedirs(out, exist_ok=True)


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


def import_model(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".stl":
        bpy.ops.wm.stl_import(filepath=path)
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=path)
    elif ext == ".ply":
        bpy.ops.wm.ply_import(filepath=path)
    elif ext == ".fbx":
        (bpy.ops.wm.fbx_import if hasattr(bpy.ops.wm, "fbx_import") else bpy.ops.import_scene.fbx)(filepath=path)
    elif ext in (".glb", ".gltf"):
        bpy.ops.import_scene.gltf(filepath=path)
    elif ext in (".usd", ".usdz", ".usda", ".usdc"):
        bpy.ops.wm.usd_import(filepath=path)
    else:
        sys.exit(f"Unsupported model {path}: export STL, OBJ, FBX, glTF or USD from the CAD app")
    return list(bpy.context.selected_objects)


# Scene: a .blend opens as it is; anything else imports into an empty scene.
if len(a.models) == 1 and a.models[0].lower().endswith(".blend"):
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath(a.models[0]))
    objects = [o for o in bpy.context.scene.objects if o.type == "MESH"]
else:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objects = []
    for path in a.models:
        for obj in import_model(os.path.abspath(path)):
            if obj.parent is None:
                obj.scale = [s * a.scale for s in obj.scale]
            if obj.type == "MESH" and not obj.data.materials:
                obj.data.materials.append(material("model", a.colour, 0.5))
            objects.append(obj)
scene = bpy.context.scene
bpy.context.view_layer.update()

meshes = [o for o in objects if o.type == "MESH"] or objects
corners = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
low = Vector((min(p.x for p in corners), min(p.y for p in corners), min(p.z for p in corners)))
high = Vector((max(p.x for p in corners), max(p.y for p in corners), max(p.z for p in corners)))
centre, size = (low + high) / 2, max(high - low)
print(f"Model bounds {tuple(round(v, 3) for v in high - low)} (scene units)")

frames = round(a.seconds * a.fps)
scene.frame_start, scene.frame_end = 1, frames
scene.render.fps = a.fps

camera = bpy.data.objects.new("camera", bpy.data.cameras.new("camera"))
camera.data.lens = a.lens
camera.data.clip_end = max(1000, size * 20)
scene.collection.objects.link(camera)
scene.camera = camera


def aim(obj, target):
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


if a.mode == "orbit":
    # Turntable: camera circles the model once, at a three-quarter height, framing its largest side.
    radius = size * 1.3 * 35 / a.lens + size / 2
    for f in range(1, frames + 1):
        t = 2 * math.pi * (f - 1) / frames
        camera.location = centre + Vector((math.sin(t) * radius, -math.cos(t) * radius, radius * 0.45))
        aim(camera, centre)
        camera.keyframe_insert("location", frame=f)
        camera.keyframe_insert("rotation_euler", frame=f)
    bpy.ops.mesh.primitive_plane_add(size=size * 400, location=(centre.x, centre.y, low.z))
    bpy.context.object.data.materials.append(material("ground", "#E9E6DE", 0.9))
else:
    # Walkthrough: constant walking speed along the path, looking 1.5 m ahead so corners turn smoothly.
    pts = [Vector((float(x), float(y), low.z + a.eye)) for x, y in (p.split(",") for p in a.path.split(";") if p)]
    if len(pts) < 2:
        sys.exit("path mode needs --path with at least two points, e.g. --path \"1,-3;1,2;4,2\"")
    seg = [(p, q, (q - p).length) for p, q in zip(pts, pts[1:])]
    total = sum(s[2] for s in seg)

    def at(d):
        d = min(max(d, 0), total)
        for p, q, n in seg:
            if d <= n:
                return p.lerp(q, d / n if n else 0)
            d -= n
        return pts[-1]

    look = 1.5
    print(f"Path length {total:.1f} m: {total / a.seconds:.2f} m/s (walking is about 1.2)")
    for f in range(1, frames + 1):
        d = total * (f - 1) / max(frames - 1, 1)
        camera.location = at(d)
        ahead = at(d + look) if d + look <= total else at(total) + (at(total) - at(total - look)).normalized() * look
        aim(camera, ahead)
        camera.keyframe_insert("location", frame=f)
        camera.keyframe_insert("rotation_euler", frame=f)

# Light: a soft sky plus a sun, sized to the model so small parts and whole buildings both read.
if not scene.world:
    scene.world = bpy.data.worlds.new("world")
    scene.world.use_nodes = True
    bg = scene.world.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = linear("#F2F1EC")
    bg.inputs["Strength"].default_value = 0.8
    sun = bpy.data.objects.new("sun", bpy.data.lights.new("sun", "SUN"))
    sun.data.energy = 1.8
    sun.data.angle = math.radians(8)
    sun.rotation_euler = (math.radians(50), 0, math.radians(35))
    scene.collection.objects.link(sun)

scale = 0.5 if a.draft else 1.0
w, h = (int(v) for v in a.size.lower().split("x"))
scene.render.resolution_x, scene.render.resolution_y = int(w * scale), int(h * scale)
samples = max(4, a.samples // 4) if a.draft else a.samples
if a.engine == "cycles":
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples
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
            break
else:
    scene.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items else "BLENDER_EEVEE_NEXT"
    scene.eevee.taa_render_samples = samples
scene.view_settings.view_transform = "Standard"  # AgX (the default) desaturates brand colours
scene.render.image_settings.file_format = "PNG"

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, "scene.blend"), check_existing=False)
if os.path.exists(os.path.join(out, "scene.blend1")):
    os.remove(os.path.join(out, "scene.blend1"))  # Blender's backup of the previous save

if a.still is not None:
    for n in (int(f) for f in a.still.split(",")):
        scene.frame_set(n)
        scene.render.filepath = os.path.join(out, f"still-{n}.png")
        bpy.ops.render.render(write_still=True)
        print("STILL_OK", scene.render.filepath)
    sys.exit(0)

scene.render.filepath = os.path.join(out, "frames", "")
bpy.ops.render.render(animation=True)
mp4 = os.path.join(out, "animation.mp4")
if shutil.which("ffmpeg"):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(a.fps), "-i",
                    os.path.join(out, "frames", "%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "18", "-movflags", "+faststart", mp4], check=True)
    print("ANIMATION_OK", mp4)
else:
    print("ANIMATION_OK frames only (no ffmpeg on PATH):", os.path.join(out, "frames"))
