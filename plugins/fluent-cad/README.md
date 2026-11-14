# Fluent CAD

Skills for people who design things on a computer: buildings, parts and products, 3D prints, and the animations that show them off. One install. Say what you want to make and the right skill starts: it sets up your apps, connects your agent to the ones it can drive, does the work, and checks it with numbers and pictures before calling it done.

![A house plan drawn from a plain-words brief, as a layered AutoCAD drawing](images/demo-house-plan.png)

![The same plan raised into 3D and rendered in Blender](images/demo-house-3d.jpg)

One brief, "a two-bedroom house, about 12 by 8 m", became the drawing, a room schedule and block count in Excel, this 3D model, a turntable, a walkthrough and a finished video.

## Find your track

| You | Say something like | Skills that do it |
|---|---|---|
| **Architecture and building**: architects, draughtspeople, QSs, site engineers, contractors | "Draw a site office, 10 by 6 m, two offices, a meeting room, a store and a toilet, with the block count." | `drawing-building-plans` |
| **Engineering and product design**: mechanical and product designers, students | "Design a wall bracket for a 5 kg shelf in FreeCAD so I can watch." | `designing-3d-models` |
| **3D printing and making**: makers, printer owners, print shops, schools | "Make a keychain from my logo with an NFC tag inside, ready for my Bambu A1." | `designing-3d-models`, `printing-3d-models` |
| **3D animation and visualisation**: Blender artists, motion designers, arch-viz | "Turn this plan into a walkthrough video, then cut it with the drawing and a turntable." | `animating-in-blender` |
| **Everyone, first** | "Set up this computer for my work. I'm an architect and I use AutoCAD." | `setting-up-cad-apps` |

Many people sit in two tracks: an engineer who prints parts uses tracks 2 and 3; arch-viz uses 1 and 4.

## The five skills

- **setting-up-cad-apps**: checks what the computer has, installs the apps that fit the job, and connects the agent to Blender, Fusion, SketchUp, ArchiCAD, Revit or FreeCAD.
- **drawing-building-plans**: a brief in plain words becomes a layered AutoCAD drawing (DXF) with room, door and window schedules and wall quantities in Excel. A separate script measures the drawing to check them. It also takes off quantities from your own drawings and raises a plan into a 3D model.
- **designing-3d-models**: parts in FreeCAD (live, on your screen), Fusion, OpenSCAD or Blender; logos into 3D objects; mesh checks; pockets for NFC tags, magnets and nuts.
- **printing-3d-models**: slicer projects in Bambu Studio, OrcaSlicer, PrusaSlicer or Cura, multi-colour prints, pauses for inserts, and the first layer.
- **animating-in-blender**: turntables and building walkthroughs rendered from any model, and clips, stills and music cut into one video in Blender's Video Sequencer, with the `.blend` handed back so you can keep editing.

## Where they work

The skills run scripts and apps on your own computer, so they need an agent that works there.

| App | What works |
|---|---|
| Claude Code: terminal, desktop app, IDE extensions | Everything |
| Codex: CLI, desktop app, IDE extension | Everything |
| Claude Desktop with connectors | Live work in Blender, Fusion, SketchUp and ArchiCAD through their connectors, plus advice |
| Claude chat on the web and Cowork | Advice, scripts and the SketchUp connector. Code there runs in a sandbox, not on your computer, so it can't reach your apps |

## Install

Open Claude Code or Codex and paste:

> Install the Fluent CAD plugin by following https://github.com/fluent-ke/fluent-plugins/blob/main/plugins/fluent-cad/INSTALL.md

The agent installs the plugin and checks it worked. To run the commands yourself, see [INSTALL.md](INSTALL.md). Then start a new session and say what you make. [GUIDE.md](GUIDE.md) has a first project for each track.

## What's inside

```
skills/setting-up-cad-apps/
  scripts/check_setup.py              read-only report of CAD, 3D and print apps and agent bridges
  references/connectors.md            Blender, Fusion, SketchUp, ArchiCAD, Revit and AutoCAD connections
  references/freecad-mcp.md           connect any agent to FreeCAD
skills/drawing-building-plans/
  scripts/measure_dxf.py              measures any DXF by layer: areas, lengths, block counts, texts, a PNG
  scripts/extrude_walls.py            raises a plan's walls into a 3D model for viewing
  references/quantities.md            wall areas, openings and block counts, with a worked example
skills/designing-3d-models/           FreeCAD bridge client, export gate, Blender render, NFC example
skills/printing-3d-models/            Bambu Studio project builder, slicer notes
skills/animating-in-blender/
  scripts/animate_model.py            turntable or walkthrough, still or full video, saves the .blend
  scripts/edit_video.py               clips, stills and music into one video in Blender's Video Sequencer
```

## Safety

- Drawings say "Drawn by AI. To be checked by the engineer." The agent never claims a design meets building regulations.
- Quantities are formulas you can audit, and the drawing is measured separately to check them.
- Connectors run code the agent writes inside your app. Save first; the agent asks before bulk changes.
- You start every print. The agent touches a printer only when you ask, and names the printer, action and file first.
- Passwords, licences and printer access codes stay with you.

## Tested

On macOS with Blender 5.2.1, FreeCAD 1.1.3 and Bambu Studio 02.08. `measure_dxf.py` reproduced the wall areas of two independently drawn plans exactly (AutoCAD 2010 and R12 DXF). `animate_model.py` and `edit_video.py` rendered a turntable, a walkthrough and a three-shot edit with music. A fresh agent given only the skills and the house brief above produced the drawing, workbook, 3D model, turntable, walkthrough and a 19-second edit in about 10 minutes, and every measured wall and room area agreed with its workbook. The gaps it reported were fixed, except three known limits: doors stay open to full height in the 3D model, `measure_dxf.py` does not read dimension values, and walkthrough wall clearance is checked by the agent rather than a script. The connectors' steps follow the vendors' pages as of November 2026 and have not been run end to end here. Windows, Linux and the OrcaSlicer, PrusaSlicer and Cura steps have not been run. If something fails, open an issue with what you asked, what happened and the output of `check_setup.py`.

## Licence

[MIT](../../LICENSE).
