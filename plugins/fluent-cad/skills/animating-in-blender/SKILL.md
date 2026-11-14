---
name: animating-in-blender
description: Use when animating, rendering or editing video in Blender - a turntable or product spin of a model, a walkthrough or fly-through of a building, a render from a CAD or STL file, driving Blender live through its connector, batch changes to a Blender scene, or cutting clips, stills and music into one video in Blender's Video Sequencer.
license: MIT
metadata:
  author: fluent
  version: "0.1"
---

# Animating in Blender

Turn models into moving pictures: a part turning on a table, a walk through a building before it is built, and the clips cut into one video with music. Every shot is checked as a still before the full render, and every video is checked after it.

`K` below is this skill's folder. The scripts run inside Blender: `blender -b -P $K/scripts/<script>.py -- <arguments>` (macOS binary: `/Applications/Blender.app/Contents/MacOS/Blender`). Blender or ffmpeg missing: use `setting-up-cad-apps` first. A single still render of a printed part: `designing-3d-models`. A designed social film with kinetic type, logos and an original score: hand the clips to the `making-motion-graphics` skill (Fluent Motion plugin).

Keep work in the user's project folder, or `~/Blender/<project>/` when they have none. For a building drawn with `drawing-building-plans`, use that project's folder.

## Routes

| Job | Route |
|---|---|
| Change, light or debug the user's own scene while they watch | the Blender connector, live (`setting-up-cad-apps` connects it) |
| Turntable of a model or product | `scripts/animate_model.py ... orbit` |
| Walkthrough of a building | `drawing-building-plans`' `extrude_walls.py` makes the model from a DXF plan; then `animate_model.py ... path` |
| Cut clips, stills and music into one video | `scripts/edit_video.py` |
| Anything else (an exploded assembly, a camera move the scripts don't do) | open the `scene.blend` a script saved and change it through the connector or a short `bpy` script; render as below |

## Steps

1. **Brief.** What the viewer should see, length, where it plays (16:9 `--size 1920x1080`; Reels, TikTok and Status `--size 1080x1920`), the model files and their units. STL and other exports from CAD apps are usually millimetres: pass `--scale 0.001`. The OBJ from `extrude_walls.py` is already in metres: no scale. Done when each is answered.
2. **Stills first.** `--still 1,120,240 --draft` renders those frames at half size in one run. Check at least the first, middle and last frames and say what each shows. Done when the subject is framed, lit, and nothing passes through a wall.
3. **Render.** The same command without `--still`. `--draft` halves the size: use it for timing checks, not for clips going into the final edit (they come out soft when the edit scales them up). Each script prints `ANIMATION_OK` or `EDIT_OK` with the output path.
4. **Edit**, when there is more than one shot: `blender -b -P $K/scripts/edit_video.py -- OUT.mp4 plan.png orbit/animation.mp4 walk/animation.mp4 --size 1920x1080 --music track.mp3`, with `--size` matching the clips. Stills keep their shape with black bars: render a plan at the video's aspect (16:9) to fill the frame. Music must be the user's or licensed for this use.
5. **Check the video.** `ffprobe` for duration and size, and an audio stream when music was added; pull a frame from each shot and at each crossfade with `ffmpeg -ss <s> -i out.mp4 -frames:v 1 f.png` and look at them. Done when the duration matches the plan and every sampled frame is right.
6. **Hand over** the MP4 and the `.blend` it came from: the user can open it, adjust in Blender and render again.

## Walkthroughs

- Take path points from the drawing, not by eye: outside the main door, the centre of each door the camera passes through, then the room's middle. Model X,Y in metres are the plan's X,Y in millimetres ÷ 1000.
- Before the stills, check each path segment keeps at least 0.3 m from every wall outline in the plan.
- Walking pace is about 1.2 m/s: `--seconds` ≈ path length ÷ 1.2. The script prints the path length and speed.
- End facing into the room, towards a window, never close to a wall. The camera looks 1.5 m ahead along the path and carries on along the last segment at the end, so point the last segment at what it should end on.
- `--lens 20` (the default for paths) suits interiors at eye height; 35 suits a turntable.

## Live connector

- Ask the user to save the `.blend` first. Changes reach disk only when they save.
- Show the Python for any batch change (deleting, renaming or re-materialling many objects) and wait for a yes.
- Read the scene (objects, materials, cameras) before changing it, and screenshot the viewport after each visible change.

## Common mistakes

| Mistake | Fix |
|---|---|
| A tiny or giant model from CAD | `--scale 0.001` for millimetre files; the script prints the model's bounds |
| Rendering the whole film to find one bad frame | `--still N --draft` first |
| Washed-out colours | the scripts set the Standard view transform; keep it when editing the `.blend` |
| A walkthrough through a wall | path points from door centres in the drawing |
| Words baked into the 3D render | titles as text strips in the edit's `.blend`, or the clips go to Fluent Motion, so words stay sharp and editable |
