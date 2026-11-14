---
name: drawing-building-plans
description: Use when drawing or checking building drawings - a floor plan, site office, house or extension from a description or sketch, a DXF or DWG for AutoCAD, ArchiCAD or Revit, a room, door and window schedule, wall areas, block counts or other quantity take-offs from a drawing, or comparing two revisions of a plan.
license: MIT
metadata:
  author: fluent
  version: "0.1"
---

# Drawing building plans

Turn a brief in plain words, a sketch or an existing drawing into a layered CAD drawing that opens in AutoCAD, with schedules and quantities that agree with it. A building drawing is checked by the engineer or architect who signs it: every output says so, and the agent never states that a design meets building regulations.

`K` below is this skill's folder. Its scripts run with `uv run` (it fetches their libraries); a missing `uv` or app: use `setting-up-cad-apps` first.

Save work in the user's project folder, or `~/Drawings/<project>/` when they have none: the drawing script, the DXF, the plan PNG (the deliverable; `check.png` from step 4 is your check), the quantities workbook and a `README.md`. Animation of the same project goes in the same folder.

## Routes

| The user has | Route |
|---|---|
| AutoCAD or any DWG/DXF app (default) | Write the DXF with Python and `ezdxf`; they open it. Revisions: re-run the script with a new revision letter |
| An existing DWG | They save it as DXF (`SAVEAS`, DXF); measure it with `measure_dxf.py` |
| ArchiCAD 30 or Revit 2027 with the connector | Read the model through the connector (Revit's is read-only). New layouts still go in as DXF, which they place as a drawing or link |
| SketchUp connector | A quick 3D massing of the same plan, for the client, alongside the DXF |
| A 3D model of the plan | `uv run $K/scripts/extrude_walls.py plan.dxf model.obj` raises the walls (OBJ in metres, plan X,Y in mm = model X,Y in metres); turntable or walkthrough with `animating-in-blender`. A solid, editable model: FreeCAD (`designing-3d-models`) |

## Steps

1. **Brief.** Building type and use, outside size, rooms and rough sizes, wall build-up (for example 200 mm external, 150 mm internal block), wall height, doors and windows, which side faces the road or north, client and project name for the title block. Write down every assumption you make. Done when each is answered or listed as an assumption.
2. **Draw by script.** One Python script holds the geometry as data (walls by centreline and thickness, openings by wall and offset, rooms) and draws from it. Run it with `uv run --with ezdxf --with matplotlib --with openpyxl draw_plan.py`. Follow the drawing rules below.
3. **Quantities from the same data.** A workbook (`openpyxl`) with a room schedule, a door and window schedule and the quantities in [quantities.md](references/quantities.md), each quantity a formula that refers to input cells, so a changed rate or size flows through. Rates the user gives; any rate you assume is labelled as an assumption in the sheet.
4. **Measure independently.** `uv run $K/scripts/measure_dxf.py plan.dxf --png check.png --text`. Compare the report with the brief and the workbook: the wall layers' extents (the drawing extents include dimensions and the title block), the wall layers' enclosed area against centreline length × thickness less openings, door and window counts, and each room's area measured from its outline on `A-AREA` (the room text was written by the same script, so it proves nothing). Done when every figure agrees; when one does not, fix the script, not the numbers. For a real recalculation of the workbook, `soffice --headless --convert-to xlsx --outdir recalc/ quantities.xlsx` when LibreOffice is installed.
5. **Look at it.** Read `check.png`: walls closed, every door swinging into a room, no text over walls, the title block complete. Done when you have described what the picture shows.
6. **Hand over.** The files, the assumptions, and a short list of what the engineer must check: structure, foundations, roof, drainage, services, fire escape, the approving authority's rules.

## Drawing rules

- Millimetres, full size, `doc.header["$INSUNITS"] = 4`. Save as DXF R2010 (`ezdxf.new("R2010", setup=True)`) so dimensions stay live in AutoCAD.
- Layers: `A-WALL-EXT`, `A-WALL-INT`, `A-DOOR` (leaf and swing arc), `A-WIND`, `A-DIMS`, `A-TEXT` (room name and area), `A-AREA` (one closed outline per room, its clear internal size, for measuring; set it not to plot), `A-TITLE`. Use the user's office layer names instead when they have a standard.
- Walls as closed outlines, one closed polyline per wall piece between openings, never single lines: the measured area is then the wall's plan area.
- Each window as one closed polyline on `A-WIND` spanning the wall thickness across the opening, plus its glazing lines. `extrude_walls.py` builds sills and lintels from these outlines.
- Text colour 7 (black on white paper, white on AutoCAD's dark screen). Yellow and cyan text vanish on paper.
- Dimensions with `add_linear_dim(...).render()`: overall sizes and each room's clear internal size, placed along a wall with no door so they clear the swings and room text. At full size in millimetres the default 2.5-unit text is invisible: set the dimension style for 1:100, `dimtxt` 250, `dimasz` 150, `dimexe` 100, `dimexo` 100, `dimgap` 50, and room text about 250 high (title block text to suit the sheet).
- A title block with client, project, drawing title, revision, scale, date and "Drawn by AI. To be checked by the engineer."
- Changing a revision: keep the old file, re-run with the next letter, and list every change with its quantity effect.

## Take-offs from someone else's drawing

1. `measure_dxf.py drawing.dxf --text`: entities, closed areas, open lengths and block counts per layer.
2. Ask what each layer means before using it. Layer names are a drawer's habit, not a standard.
3. Doors and windows drawn as blocks are counted by block name; drawn as loose geometry, count closed outlines or swing arcs per layer, check against the PNG, and say which you counted.
4. Put each measured figure in the workbook with the layer it came from.

## Common mistakes

| Mistake | Fix |
|---|---|
| Quantities typed from the agent's own arithmetic | Formulas in the workbook, then measured from the DXF and compared |
| Single-line walls | Closed outlines, so areas and thicknesses can be checked |
| Drawing in metres, or with no units header | Millimetres and `$INSUNITS = 4` |
| "This plan complies with the building code" | Never claimed; the engineer's checklist instead |
| Running long work in front of an audience | A brief with 6 rooms takes 8 to 20 minutes end to end; start it early |
