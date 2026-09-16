# Fluent 3D

Skills that take you from "I have a 3D printer" to a checked print on the plate. Your agent sets up the software, models the part live in FreeCAD while you watch, checks the geometry, and builds a slicer project with pauses for inserts or colour swaps. You approve the design on screen and start the print yourself.

![Render of a three-colour NFC keychain designed with these skills](images/nfc-keychain-render.png)

Three skills:

- **setting-up-3d-apps** — checks what the computer has, installs the CAD, mesh and slicer apps that fit your printer, and connects the agent to FreeCAD.
- **designing-3d-models** — models parts in FreeCAD, OpenSCAD or Blender, turns logos into 3D objects, checks meshes, renders, and designs pockets for NFC tags, magnets and nuts.
- **printing-3d-models** — builds slicer projects in Bambu Studio, OrcaSlicer, PrusaSlicer or Cura, handles multi-colour prints and pauses, and gets you through the first layer.

They work on macOS, Windows and Linux, and run in Claude, Codex and other tools that support the open [Agent Skills](https://agentskills.io) standard.

## Install in Claude Code

```
/plugin marketplace add fluent-ke/fluent-plugins
/plugin install fluent-3d@fluent
```

On claude.ai and Cowork: **Customize → Plugins**.

## Use them anywhere else

Copy the folders in [`skills/`](skills/) into your tool's skills directory (Codex: `~/.codex/skills`).

For an assistant that can run commands but doesn't load skills, paste this:

> Download https://github.com/fluent-ke/fluent-plugins and follow `plugins/fluent-3d/skills/setting-up-3d-apps/SKILL.md` to set up this computer for 3D printing. My printer is a *make and model* and this computer runs *Windows / macOS / Linux*. Ask before installing anything. Then follow `printing-3d-models` to walk me through my first print.

## Get started

> Set up this computer for 3D printing. My printer is a *make and model*. Ask before installing anything.

> Design a *thing* that is *size*, in *colours*, for my *printer*. Build it in FreeCAD so I can watch.

## What's inside

```
skills/setting-up-3d-apps/
  scripts/check_setup.py              read-only report of installed 3D tools and the FreeCAD bridge
  references/freecad-mcp.md           connect Claude Code, Codex or any MCP client to FreeCAD
skills/designing-3d-models/
  scripts/fc.py                       command-line client for the FreeCAD bridge
  scripts/freecad_check_export.py     refuses to export invalid parts or open insert pockets
  scripts/blender_render.py           headless product render of coloured STL parts
  scripts/example_nfc_keychain.py     worked example: a three-colour keychain with a sealed NFC tag
  references/freecad-live.md          live modelling, parametric build pattern, SVG logos
  references/inserts.md               NFC tags, magnets and nuts sealed in with a print pause
skills/printing-3d-models/
  scripts/make_bambu_project.py       multi-colour Bambu Studio project with working pauses
  references/slicers.md               Bambu Studio by script; pauses in OrcaSlicer, PrusaSlicer and Cura
```

## Safety

- The agent writes files and slices on your computer. It uploads to, starts, heats or moves a printer only when you ask, and names the printer, action and file first.
- Printer access codes, passwords and cloud tokens stay with you: type them into your slicer yourself.
- The FreeCAD bridge runs Python the agent sends inside FreeCAD. It listens only on your own computer; keep the add-on's remote connections off.

## Tested

Tested end to end on macOS with FreeCAD 1.1.3, Blender 5.2.1, Bambu Studio 02.08 and a Bambu Lab A1 profile ([pause marker in the sliced project](images/bambu-studio-slice-pause-marker.png), [x-ray of the sealed NFC pocket](images/freecad-xray-sealed-tag.png)). The Windows and Linux paths, and the OrcaSlicer, PrusaSlicer and Cura steps, have not been run yet. If something fails, open an issue with what you asked for, what happened, and the output of `check_setup.py`.

The FreeCAD connection uses [neka-nat/freecad-mcp](https://github.com/neka-nat/freecad-mcp) (MIT).

## Licence

[MIT](../../LICENSE).
