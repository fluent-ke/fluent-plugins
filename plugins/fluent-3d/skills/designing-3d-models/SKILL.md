---
name: designing-3d-models
description: Use when designing a 3D model or part - modelling in FreeCAD, OpenSCAD or Blender, turning a logo or SVG into a 3D object, checking or repairing a mesh, rendering a model, or designing a pocket for an NFC tag, magnet or nut.
license: MIT
metadata:
  author: fluent
  version: "0.1"
---

# Designing 3D models

Build the part in a real CAD app, prove it with numbers and screenshots, and export parts a slicer can use as they are. The user judges a design by looking at it in the app, so show it there before calling anything done.

`K` below is this skill's folder. Run its scripts with `python3` (Windows: `py`). A tool is missing: use `setting-up-3d-apps` first. The model is ready to slice: use `printing-3d-models`.

Keep work in the user's project folder, or `~/3D Printing/models/<project>/` when they have none: the source file (`.FCStd`, `.scad`, `.blend`), STL and STEP exports, and `images/`. Keep the source and export copies from it; scratch tests go to a temp folder.

## Tool routing

| Stage | Tool | How | Details |
|---|---|---|---|
| Parametric part (default) | FreeCAD + MCP bridge | `scripts/fc.py`, or the `freecad` MCP tools when loaded | [freecad-live.md](references/freecad-live.md) |
| Fully scripted part | OpenSCAD | write `part.scad`; `openscad -o part.stl part.scad`; check it with `openscad -o view.png --imgsize=1200,900 --viewall --autocenter part.scad` | — |
| Part from Fusion, Onshape, Tinkercad, SolidWorks | that app | the user exports STEP (to edit) or STL/3MF (to print) | — |
| Logo or SVG | FreeCAD SVG import | outlined paths become extruded faces | [freecad-live.md](references/freecad-live.md) |
| Organic shape, mesh edits | Blender | keep the `.blend`; export a separate STL | — |
| Render for approval or sharing | Blender, headless | `blender -b -P $K/scripts/blender_render.py -- out.png part.stl:#RRGGBB ...` (about 1 min on a GPU, several on CPU) | — |
| Independent mesh check | admesh | `admesh part.stl` (read-only); a sealed pocket shows as 2 parts | — |
| Format conversion | assimp | `assimp export part.stl part.glb`; slicer 3MF projects lose their settings through it | — |
| NFC tag, magnet or nut | — | sealed pocket, filled during a print pause | [inserts.md](references/inserts.md) |

On macOS the Blender binary is `/Applications/Blender.app/Contents/MacOS/Blender`.

## Steps

1. **Brief.** Object and use, size, printer and nozzle, material, colours and whether a multi-material unit (AMS, MMU) exists, inserts, load direction and mating parts. Check the models folder for prior art. Done when each is answered or the user has said "you choose".
2. **Live model.** Script a parametric document with every dimension in a `Params` sheet. Screenshot Top, a hero angle and an x-ray view. Done when the user approves what is on screen.
3. **Gate and export.** `python3 $K/scripts/fc.py exec $K/scripts/freecad_check_export.py DOC=Name OUT=/abs/prefix PARTS=Body:black,Top:white SEALED=Body`. It exports nothing unless every part is valid, one solid, and each sealed part has 2 shells.
4. **Mesh check.** `admesh` on each STL: 0 degenerate facets, 0 disconnected, 0 backwards edges. Repair only a copy, and report exactly what the repair changed.
5. **Render** when the user wants to see or share it.
6. **Record.** A `README.md` beside the model: what it is, dimensions, colour bands, pause heights for inserts, files, images. Done when someone else could slice it from the README alone.

## Working on the user's screen

- After each visible change, take a screenshot and look at it before describing it: `scripts/fc.py shot` for FreeCAD's 3D view, the OS screenshot tool for whole windows (macOS: `screencapture -x out.png`).
- Before clicking or typing into an app, confirm it is the frontmost window. The user may be working in other windows; if so, verify from files instead.
- Close only windows you opened.
- macOS: double-clicking a title bar minimises the window. Resize with System Events: `osascript -e 'tell application "System Events" to set size of window 1 of process "FreeCAD" to {1440, 875}'`.

## Common mistakes

| Mistake | Fix |
|---|---|
| Voxel or hand-rolled mesh generators | Real CAD solids with true arcs |
| Calling it done from script output | Screenshot the app; compare the Top view with the reference artwork |
| Two prints glued around an insert | One print with a pause |
| Silent automatic mesh repair | Repair a copy, list what changed, re-check |
| Colour or pocket boundaries between layers | Put every boundary on a multiple of the layer height |
