---
name: printing-3d-models
description: Use when preparing or running a 3D print - slicing in Bambu Studio, OrcaSlicer, PrusaSlicer or Cura, a multi-colour print or filament swaps, pausing a print to add an insert, adding a printer profile, a first print on a new printer, or a failed first layer.
license: MIT
metadata:
  author: fluent
  version: "0.1"
---

# Printing 3D models

Turn exported parts into a slicer project that opens ready to print, then see the print onto the plate. The agent prepares and checks; the user starts the printer.

`K` below is this skill's folder. Run its scripts with `python3` (Windows: `py`). No slicer installed: use `setting-up-3d-apps` first. Nothing to print yet: use `designing-3d-models`.

Save projects to `slices/<date>-<project>/` and notes to `print-log/<date>-<project>.md` in the user's project folder, or under `~/3D Printing/` when they have none.

## Steps

1. **Printer profile.** In the slicer, select the exact printer, nozzle size, plate type and the filament actually loaded, adding them through the setup wizard if needed. Done when a screenshot shows them selected.
2. **Orient.** For strength along the load, a flat first layer and the fewest supports, not minimum time. Parts exported to stack keep their positions.
3. **Build the project.** Bambu Studio: `scripts/make_bambu_project.py`. Other slicers: by hand. Both are in [slicers.md](references/slicers.md).
   - Multi-colour with an AMS or MMU: one filament slot per part.
   - One spool: a pause at each new colour's first layer (band bottom + one layer height) to swap filament by hand.
   - Insert: pause height and what to do at the pause are in `designing-3d-models`' [inserts.md](../designing-3d-models/references/inserts.md).
4. **Slice and review.** Check supports, walls, seams, small features, pause markers, print time and grams. Done when a screenshot of the sliced preview shows each planned pause at its layer.
5. **Print-day checklist** in the print log: which file to load, filament per slot, and the layer number and action for each pause.
6. **First layer.** The user starts the print. Ask for a photo of the first layer. If it is failing, have them stop the print, name the fault from the photo, fix it and retry. Done when the user reports a clean first layer.
7. **Log the outcome:** settings, result, photos, and what to change next. For a functional part, suggest a small fit test first and feed measured errors back into the model's parameters, not into a scaled mesh.

On a new printer, print a small test model from the slicer's library, or a calibration cube from Printables or MakerWorld, before the user's own part.

## Printer boundary

- The agent writes files and slices locally. Uploading, starting, pausing, heating, moving or cancelling a printer happens only when the user asks in the current turn. Then name the printer, the action and the file, and wait for a yes.
- Printer access codes, passwords and cloud tokens stay with the user: they type them into the slicer. Keep them out of chat, files, git and MCP configs.
- LAN-only mode and cloud accounts are the user's choice; leave printer network settings as they are.
- Report a print as successful only from the user's word or a photo.

## Common mistakes

| Mistake | Fix |
|---|---|
| Raw `bambu-studio --load-settings` with a system preset | `make_bambu_project.py`; its last line must show the real bed size and pause G-code |
| A pause whose G-code is empty | Check the printer profile's pause G-code before slicing |
| Pause one layer late | Pause at the pocket roof + one layer height; re-check when the first layer is thicker |
| Trusting auto-orient and auto-supports | Review contact areas, overhangs and seams in the preview |
