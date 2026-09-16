---
name: setting-up-3d-apps
description: Use when installing, checking or connecting 3D software - CAD, mesh and slicer apps such as FreeCAD, Blender, OpenSCAD, Bambu Studio, OrcaSlicer, PrusaSlicer or Cura - or connecting an AI agent to FreeCAD through its MCP add-on.
license: MIT
metadata:
  author: fluent
  version: "0.1"
---

# Setting up 3D apps

Get a computer ready to design and print: the apps that suit this printer and this person, installed and working, and the agent able to drive FreeCAD. After setup, design work belongs to `designing-3d-models` and slicing and printing to `printing-3d-models`.

`K` below is this skill's folder. Run its scripts with `python3` (Windows: `py`).

## Steps

1. **Survey.** Run `python3 $K/scripts/check_setup.py`. It is read-only and prints the OS, each tool it found with its path, what is missing, and whether the FreeCAD bridge is running. Ask for the printer make and model, whether it has a multi-material unit (AMS, MMU), and what the user wants to make. Done when you can name the OS, the printer and every missing tool.
2. **Pick the stack.** One app per job from the table below, starting from what the user already has. Done when the user agrees to the list.
3. **Install.** Look up each package ID with the search command, show the exact install commands, and run them after the user says yes. Done when `check_setup.py` reports every chosen tool.
4. **Connect the agent to FreeCAD**, when the user wants the agent to model live: follow [freecad-mcp.md](references/freecad-mcp.md). Done when `check_setup.py` reports the bridge running.
5. **Workspace.** Create `3D Printing/` in the user's home (or where they say) with `models/`, `slices/` and `print-log/`.

## Stack

| Job | App | Pick it when |
|---|---|---|
| Slicer | Bambu Studio | Bambu Lab printers |
| | PrusaSlicer | Prusa printers |
| | OrcaSlicer | Creality, Elegoo, Anycubic, Voron and other Marlin or Klipper printers |
| | UltiMaker Cura | UltiMaker printers, or the user already knows Cura |
| Parametric CAD | FreeCAD | default: free, scriptable, and the agent can build in it live |
| | OpenSCAD | parts described entirely in code |
| | Fusion, Onshape, Tinkercad, SolidWorks | the user already uses one; the agent guides and works from STEP or STL exports |
| Mesh, sculpt, render | Blender | organic shapes, mesh fixes, product renders |
| Mesh checks | admesh, assimp | optional command-line STL checks and format conversion |
| Agent to FreeCAD | FreeCAD MCP add-on + `uv` | live modelling |

Install one slicer: the one that matches the printer brand.

## Install commands

Search first and use the exact ID the search returns; package names drift.

| OS | Search | Install |
|---|---|---|
| macOS (Homebrew) | `brew search <name>` | apps: `brew install --cask <id>`; CLIs: `brew install admesh assimp uv` |
| Windows (winget) | `winget search <name>` | `winget install --id <id> -e` |
| Linux (Flatpak) | `flatpak search <name>` | apps: `flatpak install flathub <id>`; CLIs: the distro's packages (Debian/Ubuntu: `sudo apt install admesh assimp-utils`) and `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

When Homebrew, winget or Flatpak is absent, download the app from its official site instead of installing a package manager unasked.
