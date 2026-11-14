---
name: designing-3d-models
description: Use when designing a 3D model, part or product - modelling in FreeCAD, Fusion, OpenSCAD or Blender (including scripted bpy work and editing an STL), turning a logo or SVG into a 3D object, checking or repairing a mesh, rendering a model, converting a mesh toward STEP, designing a pocket for an NFC tag, magnet or nut, a one-part press mould, or a mechanism such as a spring-return lever or a gimbal holder.
license: MIT
metadata:
  author: fluent
  version: "0.3"
---

# Designing 3D models

## What this is for

Someone needs a part: a bracket, a case, a keychain, a replacement for something broken. Described in a chat, it comes back as a picture or a mesh nobody can change. Built properly, it is a model whose every size is a number they can edit.

**Build the part in a real CAD app, on their screen, with every dimension in one table, and prove it with numbers and screenshots before exporting anything.** The person judges a design by looking at it in the app, so show it there before calling anything done.

The person may be an engineer who lives in Fusion, or a maker who has never modelled anything. Ask which. For a beginner, talk in sizes and shapes, not features and sketches, and keep the CAD work to yourself.

`K` below is this skill's folder. Run its scripts with `python3` (Windows: `py`).

**First, check where you are running.** Claude on the web, the chat in Claude Desktop, and Cowork run in a sandbox, not on their computer: go to *In a browser*. Claude Code (the terminal, or the Code tab in Claude Desktop) and Codex run on their computer: carry on.

## The shape

1. Brief
2. Check the tools
3. Model it live
4. Gate and export
5. Check the mesh
6. Render, when wanted
7. Hand it over

## 1. Brief

Ask **one question at a time**, offering options when they are unsure:

1. What is it, and what does it do? What does it attach to or hold?
2. The sizes that matter: overall size, holes, screws, mating parts. A photo or sketch with sizes beats a description.
3. How it will be made: 3D printed (which printer, nozzle, material), or sent to a workshop as STEP.
4. For prints: colours, and whether the printer has a multi-colour unit (AMS, MMU).
5. Anything sealed inside: an NFC tag, magnets, nuts.

Check their models folder for an earlier version first. Read sizes from their photos, spec sheets and measurements, and **say the sizes back before modelling** ("16 mm wide, 18 mm tall, 3 mm thick, 4 mm hole: right?"), so they can correct them. Work in millimetres, and say where a tool's own unit differs (Blender's is metres). Done when each is answered or they say "you choose".

When a shape is a matter of taste, offer numbered versions (v1, v2); they pick one and you iterate on it.

| The job | Tool | How | Details |
|---|---|---|---|
| Parametric part (default) | FreeCAD, live | `scripts/fc.py`, or the `freecad` MCP tools when loaded | [freecad-live.md](references/freecad-live.md) |
| They design in Fusion | Fusion + its Claude connector | model through the connector; they see it in Fusion and export STEP or STL | — |
| Fully scripted part | OpenSCAD | write `part.scad`; `openscad -o part.stl part.scad`; picture: `openscad -o view.png --imgsize=1200,900 --viewall --autocenter part.scad` | — |
| Part from Onshape, Tinkercad, SolidWorks | that app | they export STEP (to edit) or STL/3MF (to print) | — |
| Logo or SVG | FreeCAD SVG import | outlined paths become extruded faces | [freecad-live.md](references/freecad-live.md) |
| Organic shape, mesh edits, editing their STL (fill a hole, thicken a back) | Blender, by `bpy` script, not by clicking | keep the `.blend` and the script; export a separate STL | [blender-scripting.md](references/blender-scripting.md) |
| A one-part press mould (clay and similar) | FreeCAD or Blender | the part subtracted from a block, with draft and no undercuts | [moulds.md](references/moulds.md) |
| A mechanism: spring-return lever, gimbal or pivot holder | FreeCAD | patterns, not fixed sizes: re-derive for their motor, spring and load | [mechanism-design.md](references/mechanism-design.md) |
| They need STEP from a mesh | FreeCAD mesh to solid, or rebuild | a STEP made from a mesh is faceted, not a true solid: say so, and rebuild in CAD when they need to edit features | [blender-scripting.md](references/blender-scripting.md) |
| NFC tag, magnet or nut | — | a sealed pocket, filled during a print pause | [inserts.md](references/inserts.md) |
| A building rather than a part | — | `drawing-building-plans` | — |

## 2. Check the tools

`python3 $K/../setting-up-cad-apps/scripts/check_setup.py` shows what is installed and whether the FreeCAD connection is running. Anything missing: use `setting-up-cad-apps`, then carry on.

## 3. Model it live

Script a parametric document with every dimension in a `Params` sheet, so "make it 10% bigger" is one edit. After each visible change take a screenshot and look at it before describing it: `scripts/fc.py shot` for FreeCAD's 3D view, the system screenshot tool for whole windows (macOS: `screencapture -x out.png`). Show them the top view, a hero angle and an x-ray view. Done when they approve what is on screen.

## 4. Gate and export

`python3 $K/scripts/fc.py exec $K/scripts/freecad_check_export.py DOC=Name OUT=/abs/prefix PARTS=Body:black,Top:white SEALED=Body`. It exports nothing unless every part is valid and one solid, and each sealed part has its 2 shells.

## 5. Check the mesh

`admesh part.stl` on each export (read-only): 0 degenerate facets, 0 disconnected, 0 backwards edges. A sealed pocket shows as 2 parts, which is correct. Repair only a copy, and say exactly what the repair changed.

## 6. Render, when wanted

`blender -b -P $K/scripts/blender_render.py -- out.png part.stl:#RRGGBB ...` makes a product shot (about a minute on a graphics card, several without). On macOS the Blender program is `/Applications/Blender.app/Contents/MacOS/Blender`. For a turning video of it: `animating-in-blender`.

## 7. Hand it over

Ask where it should be saved (suggest `~/3D Printing/models/<project>/`), then save there: the source (`.FCStd`, `.scad`, `.blend`, and the generating script), the STL and STEP exports (with the faceted-solid caveat when the STEP came from a mesh), `images/`, and a `README.md` with what it is, its sizes, colour bands, pause heights for inserts and the file list. Done when someone else could print or machine it from the README alone.

Then the literal steps to change it themselves: open the `.FCStd` in FreeCAD, double-click `Params` in the tree on the left, change a number, press Ctrl+R (Cmd+R on a Mac) to recompute. **Smoke test:** they change one size and watch the part follow.

Ready to print: `printing-3d-models`.

## Working on their screen

- Before clicking or typing into an app, confirm it is the front window. If they are working in other windows, verify from files instead.
- Close only windows you opened.
- macOS: double-clicking a title bar minimises the window. Resize with System Events: `osascript -e 'tell application "System Events" to set size of window 1 of process "FreeCAD" to {1440, 875}'`.

## In a browser

On claude.ai the model cannot reach their apps. It can still write an OpenSCAD or FreeCAD script for them to run, and talk them through the design. Tell them once that Claude Code or Codex builds it on their screen and checks it, and leave the choice with them.

## Common mistakes

| What happens | What it actually is |
|---|---|
| A voxel or hand-rolled mesh generator | A lumpy part nobody can edit. Real CAD solids with true arcs |
| "Done" from script output | An unseen part. Screenshot the app; compare the top view with the reference |
| Two prints glued around an insert | A weak seam. One print with a pause |
| Silent automatic mesh repair | Changed geometry nobody asked for. Repair a copy and list what changed |
| Colour or pocket boundaries between layers | A boundary the printer can't make. Every boundary on a multiple of the layer height |
| Sizes typed into features | A part that breaks when one number changes. Every size in `Params` |

## Red flags — stop

- You are about to export a part that failed the gate
- You are calling a design done that they have not seen in the app
- A repair is about to overwrite their only copy of a mesh

---

Stuck, or want to send feedback on this skill? Read the `about-fluent` skill if Fluent AI Skills is installed, or visit fluent.ke.
