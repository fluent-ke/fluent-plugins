---
name: printing-3d-models
description: Use when preparing or running a 3D print - slicing in Bambu Studio, OrcaSlicer, PrusaSlicer or Cura, a multi-colour print or filament swaps, pausing a print to add an insert, small or fine parts, adding a printer profile, a first print on a new printer, a failed first layer, or operating a real Bambu Lab printer through an MCP server or CLI.
license: MIT
metadata:
  author: fluent
  version: "0.2"
---

# Printing 3D models

## What this is for

A model is finished, and the slicer opens on a screen of a hundred settings. Most failed prints are decided there: the wrong profile, a pause that never fires, a part standing the weak way.

**The agent prepares and checks the print; the person starts the printer.** It builds a slicer project that opens ready to print, shows the sliced preview with every pause marked, writes a print-day checklist, and reads the first layer from a photo.

The person may be printing for the first time. Name settings by what they do ("how thick each layer is"), and never ask them to type a printer code or password into the chat.

`K` below is this skill's folder. Run its scripts with `python3` (Windows: `py`).

**First, check where you are running.** Claude on the web, the chat in Claude Desktop, and Cowork run in a sandbox, not on their computer: go to *In a browser*. Claude Code (the terminal, or the Code tab in Claude Desktop) and Codex run on their computer: carry on.

## The shape

1. Check the tools and the printer
2. Printer profile
3. Orient
4. Build the project
5. Slice and review
6. Hand it over: the print-day checklist
7. First layer
8. Log it

## 1. Check the tools and the printer

The slicer for their printer must be installed: `python3 $K/../setting-up-cad-apps/scripts/check_setup.py`. Missing: use `setting-up-cad-apps`, then carry on. Nothing to print yet: `designing-3d-models`.

Ask, one at a time: which printer, which filament is loaded (material and colour), and whether there is a multi-colour unit.

## 2. Printer profile

In the slicer, select the exact printer, nozzle size, plate type and the filament actually loaded, adding them through the slicer's setup wizard if needed. Done when a screenshot shows them selected.

## 3. Orient

For strength along the load, a flat first layer and the fewest supports, not the shortest time. Parts exported to stack keep their positions.

Small or fine parts (thin charms, small holes): a fine layer height (0.1 to 0.15 mm), a 0.4 mm nozzle or smaller, and at least 2 perimeters. Holes that must take a pin or cord printed 0.1 to 0.3 mm oversize. Supports only where overhangs pass about 45°, and none inside small cavities such as a mould cavity or an insert pocket. These are common practice: tune them per printer.

## 4. Build the project

Bambu Studio: `scripts/make_bambu_project.py`. Other slicers: by hand. Both are in [slicers.md](references/slicers.md).

- Several colours with an AMS or MMU: one filament slot per part.
- One spool: a pause at each new colour's first layer (the band bottom plus one layer height) to swap filament by hand.
- An insert: the pause height and what to do at the pause are in `designing-3d-models`' [inserts.md](../designing-3d-models/references/inserts.md).

## 5. Slice and review

Check supports, walls, seams, small features, pause markers, print time and grams. Done when a screenshot of the sliced preview shows each planned pause at its layer.

## 6. Hand it over: the print-day checklist

Ask where their print files live (suggest `~/3D Printing/`), then save projects in `slices/<date>-<project>/` and notes in `print-log/<date>-<project>.md` there. The checklist in the print log says, in plain words: which file to open, which filament goes in which slot, and for each pause, the layer number and exactly what to do ("drop the tag in the pocket, flat side down, then press Resume").

## 7. First layer

They send it to the printer and start it themselves. In Bambu Studio: the printer must be bound once (Device tab, add the printer, signing in themselves); then open the project, press **Slice plate**, then **Print plate**, check the filament slots, and **Send**. Without a network connection: **Export plate sliced file** to the printer's microSD card, and start it from the printer's screen. Other slicers: [slicers.md](references/slicers.md).

Ask for a photo of the first layer. If it is failing, have them stop the print, name the fault from the photo, fix it and retry. Done when they report a clean first layer.

On a new printer, first print a small test from the slicer's own library, or a calibration cube from Printables or MakerWorld.

## 8. Log it

Settings, result, photos, and what to change next time. For a part that must fit something, suggest a small fit test first, and feed the measured error back into the model's sizes, not into a scaled mesh.

## Printer boundary

- The agent writes files and slices on their computer. Uploading, starting, pausing, heating, moving or cancelling a printer happens only when they ask in the current turn. Then name the printer, the action and the file, and wait for a yes.
- Printer access codes, passwords and cloud tokens stay with them: they type them into the slicer. Keep them out of chat, files, git and connector settings.
- LAN-only mode and cloud accounts are their choice; leave printer network settings as they are.
- Report a print as successful only from their word or a photo.

## Operating a real Bambu printer

This is for people who have already connected a printer-control server themselves; `setting-up-cad-apps` does not install one, and a beginner does not need it. When the job drives a physical Bambu Lab printer through an MCP server or CLI (status, AMS reads, uploading, starting, pausing or cancelling a job, any G-code), read [bambu-safety.md](references/bambu-safety.md) first and follow it in full: read-only by default, one approval per physical action, pre-flight checks, and redacting the printer's serial number and access code before anything reaches the chat, a log or git.

## In a browser

On claude.ai the slicer is out of reach. It can still read a photo of a first layer, explain settings, and write the print-day checklist. Tell them once that Claude Code or Codex builds and slices the project on their computer.

## Common mistakes

| What happens | What it actually is |
|---|---|
| Raw `bambu-studio --load-settings` with a system preset | A 200 mm bed and empty pause code. `make_bambu_project.py`; its last line shows the real bed size and pause code |
| A pause whose G-code is empty | A pause that never stops the printer. Check the profile's pause G-code before slicing |
| Pause one layer late | A tag printed over. Pocket roof plus one layer height; re-check when the first layer is thicker |
| Trusting auto-orient and auto-supports | A weak or scarred part. Review contact areas, overhangs and seams in the preview |

## Red flags — stop

- You are about to start, heat, move or upload to a printer that they did not ask for in this turn
- A printer code or password is about to go into the chat, a file or a config
- You are reporting a print as good without their word or a photo
- A printer status response with a serial number or access code is about to be shown or saved unredacted

---

Stuck, or want to send feedback on this skill? Read the `about-fluent` skill if Fluent AI Skills is installed, or visit fluent.ke.
