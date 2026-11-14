"""Cut clips and stills into one video in Blender's Video Sequencer, headless, with crossfades and music.

  blender -b -P edit_video.py -- OUT.mp4 ITEM [ITEM ...] [--music TRACK] [options]

ITEM: a video (.mp4 .mov .mkv .webm .avi) or a still (.png .jpg .jpeg .tif .webp), in running order.
A still holds for --still-seconds. Each cut is a crossfade of --fade seconds; the film fades in from
and out to black, and the music fades out over the last two seconds and stops at the film's end.

Options: --still-seconds 3 --fade 0.5 --fps 30 --size 1920x1080 --volume 0.8

Writes OUT.mp4 (H.264 + AAC) and OUT.blend: open the .blend in Blender's Video Editing workspace
to move cuts, retime or add titles, then render again from there.
The Blender binary on macOS is /Applications/Blender.app/Contents/MacOS/Blender.
"""
import argparse
import glob
import os
import sys

import bpy

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("items", nargs="+")
ap.add_argument("--music")
ap.add_argument("--still-seconds", type=float, default=3)
ap.add_argument("--fade", type=float, default=0.5)
ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--size", default="1920x1080")
ap.add_argument("--volume", type=float, default=0.8)
a = ap.parse_args(sys.argv[sys.argv.index("--") + 1:])
out = os.path.abspath(a.out)
STILLS = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp")

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = a.fps
scene.render.resolution_x, scene.render.resolution_y = (int(v) for v in a.size.lower().split("x"))
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = "Standard"  # AgX (the default) dims and greys footage that is already graded
editor = scene.sequence_editor_create()
strips = editor.strips if hasattr(editor, "strips") else editor.sequences  # Blender 5 renamed sequences
fade = round(a.fade * a.fps)

# Clips alternate between channels 1 and 2 and overlap by the fade; the upper one crosses over the lower.
start, placed = 1, []
for i, path in enumerate(a.items):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        sys.exit(f"Missing item: {path}")
    channel, name = 1 + i % 2, f"{i + 1:02d} {os.path.basename(path)}"
    if path.lower().endswith(STILLS):
        strip = strips.new_image(name, path, channel, start, fit_method="FIT")
        strip.frame_final_duration = round(a.still_seconds * a.fps)
    else:
        strip = strips.new_movie(name, path, channel, start, fit_method="FIT")
    strip.blend_type = "CROSS"
    placed.append(strip)
    start = strip.frame_final_end - fade

first, last = placed[0], placed[-1]
end = last.frame_final_end - 1
scene.frame_start, scene.frame_end = 1, end


def ramp(strip, frame_a, value_a, frame_b, value_b, prop="blend_alpha"):
    setattr(strip, prop, value_a)
    strip.keyframe_insert(prop, frame=frame_a)
    setattr(strip, prop, value_b)
    strip.keyframe_insert(prop, frame=frame_b)


for strip in placed[1:]:  # crossfade in over the overlap with the clip before
    ramp(strip, strip.frame_final_start, 0.0, strip.frame_final_start + fade, 1.0)
ramp(first, 1, 0.0, 1 + fade, 1.0)  # in from black; the last clip goes out to black
last.blend_alpha = 1.0
last.keyframe_insert("blend_alpha", frame=end - fade)
last.blend_alpha = 0.0
last.keyframe_insert("blend_alpha", frame=end)

# A movie's own sound comes in as a separate strip only when added; keep clips silent under the music.
if a.music:
    music = strips.new_sound("music", os.path.abspath(a.music), 5, 1)
    if music.frame_final_end > end + 1:
        music.frame_final_end = end + 1
    ramp(music, 1, a.volume, 1, a.volume, prop="volume")
    ramp(music, max(1, end - 2 * a.fps), a.volume, end, 0.0, prop="volume")

if hasattr(scene.render.image_settings, "media_type"):  # Blender 5: choose video before the format
    scene.render.image_settings.media_type = "VIDEO"
scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.ffmpeg.constant_rate_factor = "HIGH"
scene.render.ffmpeg.audio_codec = "AAC" if a.music else "NONE"
scene.render.ffmpeg.audio_bitrate = 192
stem = os.path.splitext(out)[0]
scene.render.filepath = stem + "_"
scene.render.use_file_extension = True

bpy.ops.wm.save_as_mainfile(filepath=stem + ".blend")
bpy.ops.render.render(animation=True)

# Blender names the file with the frame range (stem_0001-0450.mp4); give it the name asked for.
rendered = sorted(glob.glob(glob.escape(stem) + "_*.mp4"), key=os.path.getmtime)
if not rendered:
    sys.exit("Render finished but no .mp4 was written")
os.replace(rendered[-1], out)
print(f"EDIT_OK {out}  {end} frames, {end / a.fps:.1f} s, {len(placed)} items  project: {stem}.blend")
