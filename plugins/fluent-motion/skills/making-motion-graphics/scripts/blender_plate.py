# Template for a 3D plate: a Blender shot rendered headless to a transparent PNG sequence, which comp.html plays with
# SHOTS={NAME:{at:0,n:FRAMES,ext:'png'}} and plate('NAME', scale, ox, oy) — so the comp can move, scale and shake it and put
# text over it. Copy this file into the film's blender/ folder and replace build() and animate().
#   blender -b -P blender_plate.py -- still <frame> [pct]            → renders/still_<frame>.png (look at one moment)
#   blender -b -P blender_plate.py -- anim [pct] [first] [last]      → renders/<SHOT>/0001.png …, then link shots/<SHOT> to it
# Timing: at 120 BPM and 30 fps one music beat is 15 frames, so a hit on music beat 20 is frame 300. Put the shot's
# big moment on a whole beat and cue the score to the same beat with M(comp beat).
# Tested on Blender 5.2 (EEVEE, AgX). About 3 s a frame at 1080×1920 on an M1 with the settings below.
import bpy, math, sys, os, random
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else ['still', '1']
MODE = argv[0]
FRAME = int(argv[1]) if MODE == 'still' and len(argv) > 1 else 1
PCT = int(argv[2]) if MODE == 'still' and len(argv) > 2 else (int(argv[1]) if MODE == 'anim' and len(argv) > 1 else 100)
F0 = int(argv[2]) if MODE == 'anim' and len(argv) > 2 else 1
HERE = os.path.dirname(os.path.abspath(__file__))
SHOT, FPS, END = 'PLATE', 30, 180
F1 = int(argv[3]) if MODE == 'anim' and len(argv) > 3 else END
BLOOM = 0.0          # 0 = off. EEVEE lost its bloom switch in 4.2; this adds the compositor Glare node instead (0.3–0.8)

def hex_lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)
ACCENT, PAPER, BASE = hex_lin('#D97757'), hex_lin('#F5F4EE'), hex_lin('#141312')   # brand colours, sRGB hex → linear

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.fps = FPS
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.resolution_percentage = PCT
sc.view_settings.view_transform = 'AgX'
sc.view_settings.look = 'AgX - Medium High Contrast'
sc.frame_start, sc.frame_end = 1, END

def mat(name, col, rough=0.45, coat=0.0, sheen=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*col, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Coat Weight'].default_value = coat
    p.inputs['Sheen Weight'].default_value = sheen
    return m

# World: near-black at low strength. The film is transparent, so the world only lights and reflects; the comp draws the ground.
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (*BASE, 1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.12
# For real reflections swap in a CC0 HDRI from polyhaven.com (credit not required):
#   env = w.node_tree.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load('studio_small_09_2k.hdr')
#   w.node_tree.links.new(env.outputs['Color'], w.node_tree.nodes['Background'].inputs['Color'])

def light(name, loc, rot, energy, col=(1, 1, 1), size=5):
    d = bpy.data.lights.new(name, 'AREA'); d.energy = energy; d.color = col; d.size = size
    o = bpy.data.objects.new(name, d); sc.collection.objects.link(o)
    o.location = loc; o.rotation_euler = [math.radians(a) for a in rot]
    return o
light('key', (-8, -6, 8), (50, 0, -50), 3200, (1, 0.95, 0.88), 5)       # warm key, top left
light('rim', (7, 8, 4), (-70, 0, 140), 3800, (1, 0.55, 0.38), 4)        # accent-coloured rim from behind: separates shapes from a dark ground
light('fill', (6, -8, -4), (110, 0, 40), 120, (0.8, 0.85, 1), 8)        # faint cool fill keeps shadows from going dead

cam_d = bpy.data.cameras.new('cam'); cam_d.lens = 50; cam_d.sensor_fit = 'VERTICAL'; cam_d.sensor_height = 36
cam_d.dof.use_dof = True; cam_d.dof.aperture_fstop = 1.4     # shallow focus: background objects soften so text can sit over them
cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.rotation_euler = (math.radians(90), 0, 0)                # looks along +Y; the frame is the XZ plane
# At distance d the frame is 2·d·tan(atan(18/50)) = 0.72·d units tall: at d = 14, 1920 px ≈ 10 units, so 1 unit ≈ 190 px.

def ease_io(k): k = min(1, max(0, k)); return 4 * k ** 3 if k < .5 else 1 - (-2 * k + 2) ** 3 / 2
def ease_out(k): k = min(1, max(0, k)); return 1 - (1 - k) ** 3

# ── Replace these two with the shot. build() makes objects; animate(f) places everything at frame f as a pure function of f.
OBJS = []
def build():
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1)
    o = bpy.context.object; bpy.ops.object.shade_smooth(); o.data.materials.append(mat('accent', ACCENT, 0.32, coat=0.6))
    OBJS.append(o)

def animate(f):
    t = f / FPS
    cam.location = Vector((0, -14 + 1.5 * ease_io(t / (END / FPS)), 0))       # slow push in
    OBJS[0].location = Vector((0, 0, 3 * (1 - ease_out(t / 1.5))))             # drop in over 1.5 s
    OBJS[0].scale = (1,) * 3

build()
for f in range(1, END + 1):                   # keyframe every frame from the pure function: exact, and re-timable by editing animate()
    animate(f)
    cam.keyframe_insert('location', frame=f)
    for o in OBJS:
        o.keyframe_insert('location', frame=f); o.keyframe_insert('scale', frame=f); o.keyframe_insert('rotation_euler', frame=f)
cam_d.dof.focus_distance = 14.0

# ── Render: EEVEE, transparent film, motion blur, PNG RGBA with light compression (faster writes)
sc.render.engine = 'BLENDER_EEVEE'
ee = sc.eevee
for attr, v in (('taa_render_samples', 40), ('use_raytracing', True), ('use_shadows', True), ('shadow_ray_count', 2), ('shadow_step_count', 8)):
    if hasattr(ee, attr): setattr(ee, attr, v)
sc.render.use_motion_blur = True
sc.render.motion_blur_shutter = 0.5
sc.render.film_transparent = True
im = sc.render.image_settings
if hasattr(im, 'media_type'): im.media_type = 'IMAGE'   # 5.x: set before file_format
im.file_format = 'PNG'; im.color_mode = 'RGBA'; im.compression = 15

if BLOOM > 0:   # Blender 5.x compositor: a node group on the scene, Glare options are input sockets, output via Group Output
    t = bpy.data.node_groups.new('Comp', 'CompositorNodeTree'); sc.compositing_node_group = t
    rl = t.nodes.new('CompositorNodeRLayers'); g = t.nodes.new('CompositorNodeGlare')
    g.inputs['Type'].default_value = 'Bloom'; g.inputs['Strength'].default_value = BLOOM
    t.interface.new_socket(name='Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    o = t.nodes.new('NodeGroupOutput')
    t.links.new(rl.outputs['Image'], g.inputs['Image']); t.links.new(g.outputs['Image'], o.inputs['Image'])

out = os.path.join(HERE, 'renders')
if MODE == 'still':
    sc.frame_set(FRAME)
    sc.render.filepath = os.path.join(out, f'still_{FRAME}.png')
    bpy.ops.render.render(write_still=True)
else:
    sc.frame_start, sc.frame_end = F0, F1
    sc.render.filepath = os.path.join(out, SHOT, '####')
    bpy.ops.render.render(animation=True)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, f'{SHOT}.blend'))
