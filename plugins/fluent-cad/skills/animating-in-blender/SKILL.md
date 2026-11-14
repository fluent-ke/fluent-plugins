---
name: animating-in-blender
description: Use when animating, rendering or editing video in Blender - a turntable or product spin of a model, a walkthrough or fly-through of a building, a render from a CAD or STL file, driving Blender live through its connector, batch changes to a Blender scene, or cutting clips, stills and music into one video in Blender's Video Sequencer.
license: MIT
metadata:
  author: fluent
  version: "0.2"
---

# Animating in Blender

## What this is for

A model sitting in a CAD file convinces nobody. A part turning on a table, or a walk through a building before it is built, does. Making either by hand in Blender takes an afternoon of keyframes for someone who knows Blender, and is out of reach for someone who does not.

**Every shot is checked as a still before it is rendered, and every video is checked after.** The scripts here make the common shots from any model in one command, and save a `.blend` the person can open and keep working on. The Blender connector covers live work on their own scene.

The person may be a Blender artist who wants the repetitive work done, or an architect or engineer who has never opened Blender. Ask which. For the second, never assume they know Blender's screens: give literal steps, and keep the work in the scripts.

`K` below is this skill's folder. The scripts run inside Blender, without its window: `blender -b -P $K/scripts/<script>.py -- <arguments>`. On macOS the Blender program is `/Applications/Blender.app/Contents/MacOS/Blender`.

**First, check where you are running.** Claude on the web, the chat in Claude Desktop, and Cowork run in a sandbox, not on their computer: go to *In a browser*. Claude Code (the terminal, or the Code tab in Claude Desktop) and Codex run on their computer: carry on.

## The shape

1. Brief
2. Check the tools
3. Stills first
4. Render
5. Edit
6. Check the video
7. Hand it over

## 1. Brief

Ask **one question at a time**, offering options when they are unsure:

1. What should the viewer see? (the model turning, a walk through the building, both)
2. How long, and where will it play? Widescreen 16:9 (`--size 1920x1080`) for screens and YouTube; vertical (`--size 1080x1920`) for Reels, TikTok and WhatsApp Status.
3. Which model files? STL and other exports from CAD apps are usually millimetres: pass `--scale 0.001`. The OBJ from `drawing-building-plans`' `extrude_walls.py` is already in metres: no scale.
4. For more than one shot: the order, any stills (the plan, a logo), and music they own or have a licence for.

Play the film back in one line ("an 8-second vertical turntable, then the walkthrough, with your track") and wait for a yes.

| Job | How |
|---|---|
| Turntable of a model or product | `scripts/animate_model.py ... orbit` |
| Walkthrough of a building | `extrude_walls.py` from the drawing, then `animate_model.py ... path` |
| Several shots, stills and music in one video | `scripts/edit_video.py` |
| Change, light or debug their own scene while they watch | the Blender connector, live |
| Anything else (an exploded assembly, a camera move the scripts don't do) | open the `scene.blend` a script saved, change it through the connector or a short `bpy` script, render as below |

## 2. Check the tools

Blender (the scripts need 4.2 or later and were tested on 5.2; the live connector needs the version its add-on page states, 5.1 or later at the time of writing) and `ffmpeg`. Missing: use `setting-up-cad-apps` to install them, then carry on. For live work, the connector must be connected too; `setting-up-cad-apps` does that.

## 3. Stills first

`--still 1,120,240 --draft` renders those frames at half size in one run, in seconds. Look at least at the first, middle and last frames, and say what each shows. Done when the subject is framed and lit, and nothing passes through a wall. Rendering the whole video to find one bad frame wastes minutes each time.

## 4. Render

The same command without `--still`. `--draft` halves the size: use it to check timing, not for clips going into the final edit, which come out soft when the edit scales them up. The script prints `ANIMATION_OK` with the path of `animation.mp4`, and saves `scene.blend` beside it.

## 5. Edit

Only when there is more than one shot:

```
blender -b -P $K/scripts/edit_video.py -- film.mp4 plan.png orbit/animation.mp4 walk/animation.mp4 --size 1920x1080 --music track.mp3
```

Set `--size` to match the clips. Each cut is a crossfade, the film fades in and out, and the music fades out at the end. Stills keep their shape with black bars at the sides, so render a plan at the video's shape (16:9) to fill the frame. The script prints `EDIT_OK` and saves `film.blend`, which opens in Blender's Video Editing workspace.

## 6. Check the video

`ffprobe film.mp4` for duration and size, and an audio stream when music was added. Then pull a frame from each shot and from each crossfade (`ffmpeg -ss <seconds> -i film.mp4 -frames:v 1 f.png`) and look at them. Done when the duration matches the plan (the shots added up, less half a second per cut) and every frame you sampled is right.

## 7. Hand it over

The MP4 and the `.blend` it came from, saved where they say (suggest `~/Blender/<project>/`, or the drawing's project folder for a building). Then the literal steps to change it themselves: open Blender, File, Open, pick `film.blend`. The Video Editing workspace shows the shots as strips, which they can drag to retime. Render, Render Animation writes a new video.

**Smoke test:** play the MP4 once, with sound, before sending it anywhere.

## Walkthroughs

- Take the path points from the drawing, not by eye: outside the main door, the centre of each door the camera passes through, then the room's middle. Model X,Y in metres are the plan's X,Y in millimetres ÷ 1000.
- Before the stills, check each path segment keeps at least 0.3 m from every wall outline in the plan.
- Walking pace is about 1.2 m/s: `--seconds` ≈ path length ÷ 1.2. The script prints the length and speed.
- End facing into the room, towards a window, never close to a wall. The camera looks 1.5 m ahead and, at the end, carries on along the last segment, so point the last segment at what it should end on.
- `--lens 20` (the default for walkthroughs) suits interiors at eye height; 35 suits a turntable.

## Live, with the connector

- Ask them to save the `.blend` first. Changes reach disk only when they save.
- Read the scene (objects, materials, cameras) before changing it, and take a screenshot of the viewport after each visible change.
- Show the Python for any batch change (deleting, renaming or re-materialling many objects) and wait for a yes.

## Words on screen

Titles and captions go on in the edit, as text strips in `film.blend`, never in the 3D render, so they stay sharp and can be changed. For a designed social film with kinetic type, logos and an original score, the clips go to a motion-graphics tool; with Fluent Motion installed, its `making-motion-graphics` skill takes them as footage.

## In a browser

Blender runs on their computer, so claude.ai cannot drive it. The Blender connector needs Claude Desktop, and the scripts need Claude Code or Codex. Tell them once that Claude Desktop's **Code** tab runs the scripts on their computer with no terminal (install Claude Desktop, click **Code**, choose a folder), and its chat drives Blender live through the connector.

## Common mistakes

| What happens | What it actually is |
|---|---|
| A tiny or giant model | Millimetres read as metres. `--scale 0.001` for CAD exports; the script prints the model's size |
| Rendering the whole film to find one bad frame | Minutes lost per mistake. Stills first |
| Washed-out, grey colours | Blender's default colour setting. The scripts use Standard; keep it when editing the `.blend` |
| A walkthrough through a wall | Points guessed by eye. Door centres from the drawing |
| Soft final video | Draft clips upscaled in the edit. Render final clips at full size |
| Words baked into the 3D render | Text nobody can fix. Text strips in the edit |
| Music pulled from the internet | Someone else's track. Theirs, or licensed |

## Red flags — stop

- A batch change through the connector is about to run on a scene they have not saved
- You are about to deliver a video you have not sampled frame by frame
- The music's rights are unknown and the video is going public

---

Stuck, or want to send feedback on this skill? Read the `about-fluent` skill if Fluent AI Skills is installed, or visit fluent.ke.
