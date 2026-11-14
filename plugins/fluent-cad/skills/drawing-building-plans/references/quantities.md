# Wall quantities

Every quantity is a formula over input cells, with its working visible. The rates are the user's; when the user has none, put a rate in an input cell labelled "assumed, confirm with the QS".

## Inputs (one cell each)

Wall height; external and internal wall thickness; each door and window width and height; blocks per m²; waste allowance.

## Quantities

| Quantity | Formula | Check against the drawing |
|---|---|---|
| Centreline length, per wall type | external: the centreline ring around the building (outside perimeter less 4 × thickness for a rectangle); internal: face to face between the walls each one meets | the two together make plan area = length × thickness exact at corners and T-junctions |
| Wall plan area, per wall type | centreline length × thickness − (opening widths in that wall type × thickness) | `measure_dxf.py`: the closed-polyline area on that wall layer, mm² ÷ 1,000,000 |
| Gross wall face area | centreline length × wall height | — |
| Net wall face area | gross face area − sum of (opening width × opening height) | — |
| Blocks | ROUNDUP(net face area × blocks per m² × (1 + waste), 0) | — |
| Room area | internal length × internal width | the room outline on `A-AREA` |

Worked example, from a tested site-office drawing: internal walls 22.90 m of centreline × 0.15 m = 3.435 m², less five doors totalling 3.9 m × 0.15 m = 0.585 m², gives 2.850 m², and the drawing measured 2,850,000 mm². External net face area 76.41 m² × 12.5 blocks per m² × 1.05 = 1,002.9, rounded up to 1,003 blocks.

## Blocks per m²

Use the user's figure. Otherwise compute it from the block face and joint and show the working: a 400 × 200 mm face with no joint gives 1 ÷ (0.40 × 0.20) = 12.5 per m²; with 10 mm joints, 1 ÷ (0.41 × 0.21) = 11.6 per m².

## In the workbook

- `openpyxl` writes formulas but does not calculate them. Excel calculates on opening. State the values you computed in Python in your answer, and when LibreOffice is installed recalculate a copy (`soffice --headless --convert-to xlsx --outdir recalc/ quantities.xlsx`) and read its values back.
- One sheet per schedule, one for quantities, one listing assumptions.
