---
name: drawing-building-plans
description: Use when drawing or checking building drawings - a floor plan, site office, house or extension from a description or sketch, a DXF or DWG for AutoCAD, ArchiCAD or Revit, a room, door and window schedule, wall areas, block counts or other quantity take-offs from a drawing, a 3D model raised from a plan, or comparing two revisions of a plan.
license: MIT
metadata:
  author: fluent
  version: "0.2"
---

# Drawing building plans

## What this is for

A site agent describes a building in a few sentences. Someone then spends a day drafting it, and another day taking off the quantities by hand, and the two never quite agree.

**The drawing and the quantities come from one set of numbers, and the drawing is then measured separately to prove they agree.** The agent writes the drawing as a layered AutoCAD file (DXF) and the quantities as a workbook of formulas. A script that knows nothing about how the drawing was made then measures it.

The person is an architect, draughtsperson, QS, site engineer or contractor. They think in rooms, walls, openings and blocks, not code. Talk in those terms, and show code only if they ask.

A building drawing is checked by the engineer or architect who signs it. Every drawing says so, and the agent never states that a design meets building regulations.

`K` below is this skill's folder. Its scripts run with `uv run`, which fetches the libraries they need.

**First, check where you are running.** Claude on the web, the chat in Claude Desktop, and Cowork run in a sandbox, not on their computer: go to *In a browser*. Claude Code (the terminal, or the Code tab in Claude Desktop) and Codex run on their computer: carry on.

## The shape

1. Brief
2. Check the tools
3. Draw
4. Quantities
5. Measure
6. Look
7. Hand it over

The same skill also takes off quantities from their own drawings, produces revisions, and raises a plan into 3D. Those come after the main path.

## 1. Brief

Ask **one question at a time**, in plain words, and offer two or three options when they are unsure:

1. What is it, and what is it for? (a site office, a two-bedroom house, an extension)
2. Roughly how big outside, and which rooms with rough sizes?
3. The walls: thickness outside and inside (for example 200 mm and 150 mm block), and height.
4. Doors and windows: where the main door faces, which rooms get windows.
5. For the title block: client, project name, and who checks it.

If they have a sketch or a photo of one, read it first and only ask what it leaves open. Then play the building back in one short paragraph, list every assumption you are making, and ask "is that it?" Done when they say yes.

## 2. Check the tools

`uv --version`. Missing: use `setting-up-cad-apps` to install it, then carry on. Nothing else needs installing: `uv` fetches the drawing libraries. They need AutoCAD or another DWG/DXF app to open the result; if they have none, the PNG and the workbook still work, and the free LibreCAD or DraftSight opens DXF.

## 3. Draw

Start from `$K/scripts/example_house_plan.py`, a worked two-bedroom house that follows every rule below: copy it into the project folder and change its data. One Python script holds the building as data (walls by centreline and thickness, openings by wall and position, rooms) and draws from it. Run it with `uv run --with ezdxf --with matplotlib --with openpyxl draw_plan.py`, following the drawing rules below. A revision is the same script re-run with the next letter.

## 4. Quantities

A workbook (`openpyxl`) built from the **same data** as the drawing: a room schedule, a door and window schedule, and the wall quantities in [quantities.md](references/quantities.md). Every quantity is a formula over input cells, so a changed rate or size flows through. Rates come from the person; any rate you assume sits in a cell labelled as an assumption.

## 5. Measure

`uv run $K/scripts/measure_dxf.py plan.dxf --png check.png --text` measures the drawing layer by layer. Compare the report with the brief and the workbook:

- the wall layers' extents against the outside size (the whole drawing's extents include dimensions and the title block);
- each wall layer's enclosed area against centreline length × thickness, less openings;
- door and window counts;
- each room's area, measured from its outline on `A-AREA`. The room text was written by the same script, so it proves nothing.

Done when every figure agrees. When one does not, fix the script, not the numbers. When LibreOffice is installed, recalculate a copy of the workbook (`soffice --headless --convert-to xlsx --outdir recalc/ quantities.xlsx`) and read its values back.

## 6. Look

Read `check.png` yourself before showing anyone: walls closed, every door swinging into a room, no text over walls or dimensions, the title block complete. Say what the picture shows. Done when nothing on it is wrong.

## 7. Hand it over

Ask where it should be saved (suggest `~/Drawings/<project>/`), then save there: the DXF, the plan PNG (the deliverable; `check.png` is your check), the workbook, the drawing script and a `README.md` listing the assumptions.

Then give them:

1. **How to open it**, for the app they use. AutoCAD: File, Open, set the file type to DXF, pick the file. ArchiCAD: File, Open (or place it as a drawing). The drawing is in millimetres at full size.
2. **The check they can do themselves in a minute:** in AutoCAD type `DIST`, click both ends of one wall, and compare with the workbook. It is the moment the drawing earns their trust.
3. **What the engineer must check** before it is used: structure, foundations, roof, drainage, services, fire escape, and the approving authority's rules.

A brief with about six rooms takes 8 to 20 minutes from start to finish. Tell them before you start, and in front of an audience start it early.

## Drawing rules

- Millimetres, full size, `doc.header["$INSUNITS"] = 4`. Save as DXF R2010 (`ezdxf.new("R2010", setup=True)`) so dimensions stay live in AutoCAD.
- Layers: `A-WALL-EXT`, `A-WALL-INT`, `A-DOOR` (leaf and swing arc), `A-WIND`, `A-DIMS`, `A-TEXT` (room name and area), `A-AREA` (one closed outline per room at its clear internal size, for measuring; set not to plot), `A-TITLE`. Use their office's layer names when they have a standard.
- Walls as closed outlines, one closed polyline per wall piece between openings, never single lines: the measured area is then the wall's plan area.
- Each window as one closed polyline on `A-WIND` spanning the wall thickness across the opening, plus its glazing lines. `extrude_walls.py` builds sills and lintels from these outlines.
- Text colour 7: black on white paper, white on AutoCAD's dark screen. Yellow and cyan text vanish on paper.
- Dimensions with `add_linear_dim(...).render()`: overall sizes and each room's clear internal size, along a wall with no door so they clear the swings and room text. At full size the default 2.5-unit text is invisible: set the dimension style for 1:100, `dimtxt` 250, `dimasz` 150, `dimexe` 100, `dimexo` 100, `dimgap` 50, and room text about 250 high.
- A title block with client, project, drawing title, revision, scale, date and "Drawn by AI. To be checked by the engineer."

## Revisions

Keep the old file. Re-run the script with the next revision letter and list every change with its quantity effect: "Office 2 one metre longer: external wall centreline +2.0 m, and the new block count from the workbook."

## Commands inside AutoCAD

When they want AutoCAD itself to do something (total every wall and opening, renumber doors), write an AutoLISP command in a `.lsp` file and show them the code first. They load it: type `APPLOAD`, pick the file, click **Load**, then **Close**, then type the command's name. This route has not been tested here; check its result against `measure_dxf.py` the first time.

## Take-offs from their drawing

1. They save the DWG as DXF (AutoCAD: `SAVEAS`, file type DXF).
2. `uv run $K/scripts/measure_dxf.py drawing.dxf --text --png drawing.png`: entities, closed areas, open lengths and block counts per layer.
3. Ask what each layer means before using it. Layer names are a drawer's habit, not a standard.
4. Doors and windows drawn as blocks are counted by block name. Drawn as loose geometry, count the closed outlines or swing arcs per layer, check against the PNG, and say which you counted.
5. Each figure goes in the workbook with the layer it came from.

## In 3D

`uv run $K/scripts/extrude_walls.py plan.dxf model.obj` raises the walls into a simple 3D model (OBJ, in metres; the plan's X,Y in millimetres become X,Y in metres), with window sills and lintels. Doors stay open to full height. For a turntable or a walkthrough, hand the model to `animating-in-blender`. For a SketchUp massing, the SketchUp connector builds one from the same brief. For a solid, editable model: `designing-3d-models` in FreeCAD.

## In a browser

On claude.ai or Claude Desktop's chat with code execution turned on (Settings, Capabilities), the same steps can run in Claude's sandbox and hand back the DXF, PNG and workbook as downloads they save and open in AutoCAD. This route has not been tested yet. If the sandbox cannot install `ezdxf`, write the DXF text directly. The measuring step still applies. Tell them once that Claude Desktop's **Code** tab saves straight into their project folder with no terminal (install Claude Desktop, click **Code**, choose a folder), and leave the choice with them.

## Common mistakes

| What happens | What it actually is |
|---|---|
| Quantities typed from the agent's own arithmetic | Unchecked numbers. Formulas in the workbook, then the drawing measured and compared |
| Room areas checked against the room text | The script agreeing with itself. Measure the `A-AREA` outlines |
| Single-line walls | Nothing to measure. Closed outlines, so areas and thicknesses can be checked |
| Drawing in metres, or no units header | A drawing that opens a thousand times too small. Millimetres and `$INSUNITS = 4` |
| Yellow room names | Invisible on paper. Colour 7 |
| "This plan complies with the building code" | A claim only the signing engineer can make. The engineer's checklist instead |
| A real client's drawing used as the example in a shared folder | Their material, shared without asking. Ask first, or swap the names |

## Red flags — stop

- You are about to state that a design is safe, approved or compliant
- You are about to hand over figures the measuring step has not confirmed
- You are about to overwrite their only copy of a drawing instead of writing a new revision
- You are saving a named client's drawing somewhere shared without asking

---

Stuck, or want to send feedback on this skill? Read the `about-fluent` skill if Fluent AI Skills is installed, or visit fluent.ke.
