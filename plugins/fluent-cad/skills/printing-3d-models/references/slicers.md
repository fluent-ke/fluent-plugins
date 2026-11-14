# Slicer projects

## Bambu Studio: build the project with the script

```bash
python3 $K/scripts/make_bambu_project.py out_AMS.3mf body.stl:#1F1E1D top.stl:#F5F4EE dot.stl:#D97757 --pause 2.6
python3 $K/scripts/make_bambu_project.py out_single-spool.3mf body.stl:#1F1E1D top.stl:#F5F4EE dot.stl:#D97757 \
        --single-spool --pause 2.6 --pause 3.6 --pause 4.4
```

Defaults: `--printer "Bambu Lab A1 0.4 nozzle" --process "0.20mm Standard @BBL A1" --filament "Bambu PLA Matte @BBL A1"`. Other names are the preset file names (without `.json`) under the profile folder's `machine/`, `process/` and `filament/`. The script finds Bambu Studio and its profiles on macOS, Windows and Linux; pass `--bambu PATH` or `--profiles DIR` when it can't.

What the script handles, and why:

- **One object:** `--load-assemble-list` with `assemble_index: [1]` on every part merges them; `0` leaves separate objects. `pos_*` is added to the STL's own coordinates, so 0 keeps the exported stack.
- **Real printer settings:** the CLI resolves neither a preset's `inherits` chain nor its `include` template files, where printers such as the A1 keep their start, end, filament-change and layer-change G-code. Unresolved, the project silently gets a 200x200 bed, a generic start G-code and an empty pause G-code, so pauses do nothing. The script merges both. Its last line must print the real bed (A1: `256x256`) and pause G-code (A1: `M400 U1`).
- **Pauses:** written to `Metadata/custom_gcode_per_layer.xml` as `<layer top_z="2.6" type="1" .../>`. Types: 0 colour change, 1 pause, 2 tool change, 3 template, 4 custom.
- It never slices, uploads or contacts a printer.

Audit any Bambu 3MF: `unzip -p file.3mf Metadata/project_settings.config` (printer, `printable_area`, G-code, `filament_colour`) and `Metadata/model_settings.config` (objects, parts, filament slots).

### Verify in the GUI

1. Open the 3MF in Bambu Studio. On Prepare, check the printer, plate, filament slots and the object on the plate.
2. **Slice plate** runs locally. In Preview, check the layer count, the Pause markers on the layer slider, and grams per filament.
3. A pause at `top_z = Z` stops before the layer that ends at Z. Layer number = Z / layer height when the first layer equals the layer height.

## OrcaSlicer, PrusaSlicer, Cura: build it by hand

The script targets Bambu Studio only. For other slicers, walk the user through it and screenshot each step:

1. **Load the parts as one object.** Select every STL in one import. PrusaSlicer and OrcaSlicer ask whether to load them as a single object with multiple parts: answer yes. In Cura, select all the parts and merge them (Ctrl+Alt+G).
2. **Assign a filament or extruder** to each part, or all to one for a single spool.
3. **Add pauses by height.**
   - OrcaSlicer and PrusaSlicer: slice, then in Preview right-click the `+` on the vertical layer slider at the pause layer and choose the pause option.
   - Cura: Extensions > Post Processing > Modify G-Code > Add a script > **Pause at height**, with the method that matches the printer's firmware.
4. **Check the pause G-code is not empty** in the printer profile's machine G-code settings. Typical values: Bambu `M400 U1`, Prusa `M601`, Klipper `PAUSE`, Marlin `M600` or `M0`. Use the profile's value; a pause with empty G-code prints straight through.
5. Slice and confirm a pause marker sits at each planned layer.

Re-check pause layers whenever the first-layer height differs from the layer height.

## Without a multi-material unit

Pause at each new colour's first layer (band bottom + one layer height) and swap filament from the printer. Pauses work on any printer; colour-change markers need a multi-material mapping.
