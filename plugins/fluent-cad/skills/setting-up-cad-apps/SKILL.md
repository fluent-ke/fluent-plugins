---
name: setting-up-cad-apps
description: Use when installing, checking or connecting design software for CAD, architecture, engineering, 3D printing or 3D animation - AutoCAD, ArchiCAD, Revit, SketchUp, Fusion, FreeCAD, OpenSCAD, Blender, Bambu Studio, OrcaSlicer, PrusaSlicer or Cura - or connecting Claude or another agent to one of them through a connector or MCP server.
license: MIT
metadata:
  author: fluent
  version: "0.2"
---

# Setting up CAD apps

Get a computer ready for the work this person does: the apps that suit their job, installed and working, and the agent connected to the ones it can drive. After setup, hand over to the skill for the job:

| The person mainly | Skill |
|---|---|
| draws buildings: plans, sections, quantities | `drawing-building-plans` |
| designs parts and products | `designing-3d-models` |
| 3D prints | `designing-3d-models`, then `printing-3d-models` |
| animates, renders or edits video in Blender | `animating-in-blender` |

`K` below is this skill's folder. Run its scripts with `python3` (Windows: `py`).

## Steps

1. **Survey.** Run `python3 $K/scripts/check_setup.py`. It is read-only and prints the OS, each app it found with its path, what is missing, and which agent bridges are listening. Ask what the person makes, which apps they already use and pay for, and, for printing, the printer make and model and whether it has a multi-material unit (AMS, MMU). Done when you can name their job, OS, apps and every missing tool.
2. **Pick the stack.** One app per job from the tables below, starting from what they already use. Never move someone off an app they know and pay for; connect the agent to it instead. Done when the user agrees to the list.
3. **Install.** Look up each package ID with the search command, show the exact install commands, and run them after the user says yes. Paid apps (AutoCAD, ArchiCAD, Revit, Fusion, SketchUp Pro) the user installs from their own account. Done when `check_setup.py` reports every chosen tool.
4. **Connect the agent** to the apps it can drive: [connectors.md](references/connectors.md) for Blender, Fusion, SketchUp, ArchiCAD, Revit and AutoCAD; [freecad-mcp.md](references/freecad-mcp.md) for FreeCAD. Done when a read-only test call answers (list the objects in the open file).
5. **Workspace.** Create one folder for their work in their home folder (or where they say): `Drawings/` for building work, `3D Printing/` with `models/`, `slices/` and `print-log/` for printing, `Blender/` for animation.

## Stack by job

| Job | App | Agent connection | Pick it when |
|---|---|---|---|
| **2D drawings, plans** | AutoCAD, or any DWG/DXF app (BricsCAD, ZWCAD, DraftSight, LibreCAD) | none official. The agent writes DXF files that open in all of them (`drawing-building-plans`) | the default for building drawings in Kenya and most offices |
| **BIM** | ArchiCAD | Graphisoft's Public MCP Server (beta, ArchiCAD 30, some subscriptions) | the user's office models in ArchiCAD |
| | Revit | Autodesk's Revit 2027 MCP Server: read-only tech preview | the user's office models in Revit |
| **Concept massing, interiors** | SketchUp | official Claude connector by Trimble: builds new `.skp` files | quick 3D from a description or a sketch |
| **Parametric parts** | FreeCAD | FreeCAD MCP (community, MIT): live modelling | default: free, scriptable, the agent builds on screen |
| | Fusion | official Claude connector by Autodesk: needs a Fusion subscription | the user already designs in Fusion |
| | OpenSCAD | none needed: parts are code | parts described entirely in numbers |
| | Onshape, SolidWorks, Inventor, Tinkercad | none | the user exports STEP (to edit) or STL (to print) |
| **3D animation, rendering, video edit** | Blender | official Claude connector by Blender: live; or headless scripts | default: free, and the agent can script every frame |
| **Slicer** | Bambu Studio | none needed: the agent writes projects | Bambu Lab printers |
| | PrusaSlicer | | Prusa printers |
| | OrcaSlicer | | Creality, Elegoo, Anycubic, Voron and other Marlin or Klipper printers |
| | UltiMaker Cura | | UltiMaker printers, or the user knows Cura |
| **Helpers** | `uv` | runs the FreeCAD MCP and the DXF scripts with their libraries | always |
| | `ffmpeg` | joins rendered frames into video | animation |
| | admesh, assimp | optional STL checks and format conversion | printing |

Install one slicer: the one that matches the printer brand.

## Where each connection works

Connectors that drive an app on the user's computer need the app and the agent on the **same machine**: Claude Desktop, Claude Code or Codex. Claude on the web reaches only SketchUp (it runs in Trimble's cloud). Everything else there is advice and scripts the user runs.

## Install commands

Search first and use the exact ID the search returns; package names drift.

| OS | Search | Install |
|---|---|---|
| macOS (Homebrew) | `brew search <name>` | apps: `brew install --cask <id>`; CLIs: `brew install uv ffmpeg admesh assimp` |
| Windows (winget) | `winget search <name>` | `winget install --id <id> -e` |
| Linux (Flatpak) | `flatpak search <name>` | apps: `flatpak install flathub <id>`; CLIs: the distro's packages (Debian/Ubuntu: `sudo apt install ffmpeg admesh assimp-utils`) and `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

When Homebrew, winget or Flatpak is absent, download the app from its official site instead of installing a package manager unasked.

## Safety

- Every live connector runs code the agent writes inside the app, with the user's permissions. Work on a copy or a new file until the user trusts the flow, and ask before bulk deletes.
- Bridges listen on the user's own computer only. Leave remote-connection options off.
- Licences, Autodesk, Trimble and Graphisoft passwords and printer access codes stay with the user: they sign in themselves.
