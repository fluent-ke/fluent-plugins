"""Worked example: a two-bedroom house (Demo House), ground floor plan. Copy it, then change the data.

Geometry is data: walls by centreline and thickness, openings by wall and offset, rooms by clear
rectangle. Draws the DXF (mm, R2010), a PNG, and the quantities workbook from the same data.

  uv run --with ezdxf --with matplotlib --with openpyxl example_house_plan.py [REV]

Writes the DXF, PNG and workbook into the current folder.
"""
import datetime
import math
import sys

import ezdxf
from ezdxf.enums import TextEntityAlignment

REV = sys.argv[1] if len(sys.argv) > 1 else "A"
STEM = f"demo-house-plan-rev{REV}"
CLIENT, PROJECT, TITLE = "Example Builders Ltd", "Demo House", "Ground floor plan"

H = 2700            # wall height, mm
T_EXT, T_INT = 200, 150
BLOCKS_PER_M2, WASTE = 12.5, 0.05
SILL, HEAD = 900, 2100

# Walls: name -> (type, centreline start, end, thickness). Drawn as the centreline segment widened by
# t/2 each side, no extension along its length. External: south/north run the full 12 m (they take the
# corners), west/east run between them, so the drawn lengths sum to the true centreline ring (39.2 m).
# Internal walls run face to face between the walls they meet.
WALLS = {
    "S":  ("ext", (0, 100), (12000, 100), T_EXT),
    "N":  ("ext", (0, 7900), (12000, 7900), T_EXT),
    "W":  ("ext", (100, 200), (100, 7800), T_EXT),
    "E":  ("ext", (11900, 200), (11900, 7800), T_EXT),
    "I1": ("int", (200, 4500), (11800, 4500), T_INT),    # living/kitchen | north rooms
    "I2": ("int", (7500, 200), (7500, 4425), T_INT),     # living | kitchen
    "I3": ("int", (4000, 4575), (4000, 7800), T_INT),    # bedroom 1 | corridor, bath
    "I4": ("int", (4075, 5750), (7925, 5750), T_INT),    # corridor | bathroom
    "I5": ("int", (8000, 4575), (8000, 7800), T_INT),    # corridor, bath | bedroom 2
}

# Openings: id, kind, wall, offset from wall start, width, height, sill, swing side (+1 = left of
# start->end), hinge ("start"/"end").
OPENINGS = [
    ("D1", "door",   "S",  2500, 1000, 2100, 0,    +1, "start"),  # front door, into living room
    ("D2", "door",   "I2", 2600, 800,  2100, 0,    -1, "start"),  # living -> kitchen
    ("D3", "door",   "I1", 5400, 800,  2100, 0,    -1, "start"),  # living -> corridor (swings into living)
    ("D4", "door",   "I3", 150,  800,  2100, 0,    +1, "start"),  # corridor -> bedroom 1
    ("D5", "door",   "I4", 925,  800,  2100, 0,    +1, "start"),  # corridor -> bathroom
    ("D6", "door",   "I5", 150,  800,  2100, 0,    -1, "start"),  # corridor -> bedroom 2
    ("W1", "window", "S",  4800, 1800, 1200, SILL, 0, ""),        # living room
    ("W2", "window", "S",  9000, 1500, 1200, SILL, 0, ""),        # kitchen
    ("W3", "window", "N",  1300, 1500, 1200, SILL, 0, ""),        # bedroom 1
    ("W4", "window", "N",  5600, 600,  1200, SILL, 0, ""),        # bathroom
    ("W5", "window", "N",  9200, 1500, 1200, SILL, 0, ""),        # bedroom 2
]

# Rooms: name -> clear internal rectangle (x0, y0, x1, y1)
ROOMS = {
    "Living room": (200, 200, 7425, 4425),
    "Kitchen":     (7575, 200, 11800, 4425),
    "Bedroom 1":   (200, 4575, 3925, 7800),
    "Corridor":    (4075, 4575, 7925, 5675),
    "Bathroom":    (4075, 5825, 7925, 7800),
    "Bedroom 2":   (8075, 4575, 11800, 7800),
}
# Where each room's clear-size dimensions sit (y of the E-W dim line, x of the N-S one), clear of doors.
DIM_AT = {"Living room": (1500, 1000), "Kitchen": (900, 11200), "Bedroom 1": (7150, 800),
          "Corridor": (4800, None), "Bathroom": (7250, 7450), "Bedroom 2": (7150, 11200)}

LAYERS = {"A-WALL-EXT": 7, "A-WALL-INT": 8, "A-DOOR": 1, "A-WIND": 5, "A-DIMS": 7, "A-TEXT": 7, "A-TITLE": 7}


def length(w):
    (x0, y0), (x1, y1) = w[1], w[2]
    return math.hypot(x1 - x0, y1 - y0)


def frame(w):
    """unit direction along the wall and left normal"""
    (x0, y0), (x1, y1) = w[1], w[2]
    L = length(w)
    d = ((x1 - x0) / L, (y1 - y0) / L)
    return (x0, y0), d, (-d[1], d[0])


def pt(origin, d, n, s, o):
    return (origin[0] + d[0] * s + n[0] * o, origin[1] + d[1] * s + n[1] * o)


def rect(origin, d, n, s0, s1, t):
    return [pt(origin, d, n, s0, -t / 2), pt(origin, d, n, s1, -t / 2),
            pt(origin, d, n, s1, t / 2), pt(origin, d, n, s0, t / 2)]


def draw():
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4
    doc.header["$MEASUREMENT"] = 1
    for name, colour in LAYERS.items():
        doc.layers.add(name, color=colour)
    area_layer = doc.layers.add("A-AREA", color=3)  # room outlines for measuring: hidden, never plotted
    area_layer.dxf.plot = 0
    area_layer.off()
    ds = doc.dimstyles.new("MM100")  # 1:100 on paper -> 2.5 mm text = 250 drawing units
    ds.dxf.dimtxt, ds.dxf.dimasz, ds.dxf.dimexo, ds.dxf.dimexe = 150, 100, 0, 0
    ds.dxf.dimgap, ds.dxf.dimdec, ds.dxf.dimtad, ds.dxf.dimtsz = 50, 0, 1, 80
    ds.dxf.dimclrt = 7
    ds.dxf.dimtxsty = "Standard"
    msp = doc.modelspace()

    for wname, w in WALLS.items():
        layer = "A-WALL-EXT" if w[0] == "ext" else "A-WALL-INT"
        origin, d, n = frame(w)
        cuts = sorted((o[3], o[3] + o[4]) for o in OPENINGS if o[2] == wname)
        s = 0
        for c0, c1 in cuts + [(length(w), length(w))]:
            if c0 > s:
                msp.add_lwpolyline(rect(origin, d, n, s, c0, w[3]), close=True, dxfattribs={"layer": layer})
            s = c1

    for oid, kind, wname, off, width, ht, sill, side, hinge in OPENINGS:
        w = WALLS[wname]
        origin, d, n = frame(w)
        t = w[3]
        if kind == "window":
            msp.add_lwpolyline(rect(origin, d, n, off, off + width, t), close=True, dxfattribs={"layer": "A-WIND"})
            for o in (-25, 25):
                msp.add_line(pt(origin, d, n, off, o), pt(origin, d, n, off + width, o), dxfattribs={"layer": "A-WIND"})
            continue
        # door: leaf perpendicular to the wall at the face on the swing side, arc back to the far jamb
        hs, fs = (off, off + width) if hinge == "start" else (off + width, off)
        face = side * t / 2
        hinge_pt = pt(origin, d, n, hs, face)
        leaf_end = pt(origin, d, n, hs, face + side * width)
        jamb = pt(origin, d, n, fs, face)
        msp.add_lwpolyline([hinge_pt, leaf_end], dxfattribs={"layer": "A-DOOR"})
        a1 = math.degrees(math.atan2(leaf_end[1] - hinge_pt[1], leaf_end[0] - hinge_pt[0]))
        a2 = math.degrees(math.atan2(jamb[1] - hinge_pt[1], jamb[0] - hinge_pt[0]))
        # ARC runs counter-clockwise from start to end; pick the 90-degree sweep
        start, end = (a1, a2) if (a2 - a1) % 360 == 90 else (a2, a1)
        msp.add_arc(hinge_pt, width, start, end, dxfattribs={"layer": "A-DOOR"})
        mid = pt(origin, d, n, off + width / 2, 0)
        msp.add_text(oid, height=120, dxfattribs={"layer": "A-TEXT", "color": 7}).set_placement(
            pt(origin, d, n, off + width / 2, side * (t / 2 + 250)), align=TextEntityAlignment.MIDDLE_CENTER)
    for oid, kind, wname, off, width, *_ in OPENINGS:
        if kind == "window":
            w = WALLS[wname]
            origin, d, n = frame(w)
            outward = -1 if wname == "S" else 1  # label outside the building
            msp.add_text(oid, height=120, dxfattribs={"layer": "A-TEXT", "color": 7}).set_placement(
                pt(origin, d, n, off + width / 2, -outward * 0 + (-350 if wname == "S" else 350)),
                align=TextEntityAlignment.MIDDLE_CENTER)

    for name, (x0, y0, x1, y1) in ROOMS.items():
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "A-AREA"})
        area = (x1 - x0) * (y1 - y0) / 1e6
        if name == "Corridor":
            msp.add_text(f"{name}  {area:.2f} m2", height=150, dxfattribs={"layer": "A-TEXT", "color": 7}).set_placement(
                (cx, cy + 150), align=TextEntityAlignment.MIDDLE_CENTER)
        else:
            msp.add_text(name, height=200, dxfattribs={"layer": "A-TEXT", "color": 7}).set_placement(
                (cx, cy + 150), align=TextEntityAlignment.MIDDLE_CENTER)
            msp.add_text(f"{area:.2f} m2", height=150, dxfattribs={"layer": "A-TEXT", "color": 7}).set_placement(
                (cx, cy - 150), align=TextEntityAlignment.MIDDLE_CENTER)
        hy, vx = DIM_AT[name]
        if hy is not None:
            msp.add_linear_dim(base=(x0, hy), p1=(x0, hy), p2=(x1, hy), dimstyle="MM100",
                               dxfattribs={"layer": "A-DIMS"}).render()
        if vx is not None:
            msp.add_linear_dim(base=(vx, y0), p1=(vx, y0), p2=(vx, y1), angle=90, dimstyle="MM100",
                               dxfattribs={"layer": "A-DIMS"}).render()

    # overall dims
    msp.add_linear_dim(base=(0, -1100), p1=(0, 0), p2=(12000, 0), dimstyle="MM100", dxfattribs={"layer": "A-DIMS"}).render()
    msp.add_linear_dim(base=(-900, 0), p1=(0, 0), p2=(0, 8000), angle=90, dimstyle="MM100", dxfattribs={"layer": "A-DIMS"}).render()

    # north arrow
    msp.add_lwpolyline([(13000, 6600), (13250, 7400), (13500, 6600), (13250, 6800)], close=True, dxfattribs={"layer": "A-TITLE"})
    msp.add_text("N", height=250, dxfattribs={"layer": "A-TITLE", "color": 7}).set_placement((13250, 7700), align=TextEntityAlignment.MIDDLE_CENTER)

    # title block below the plan
    x0, y0, x1, y1 = 0, -4200, 12000, -1700
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "A-TITLE"})
    msp.add_line((7600, y0), (7600, y1), dxfattribs={"layer": "A-TITLE"})
    rows = [f"Client: {CLIENT}", f"Project: {PROJECT}", f"Drawing: {TITLE}",
            f"Revision: {REV}    Scale: 1:100 at A3    Date: {datetime.date.today():%d %b %Y}",
            "Drawn by AI. To be checked by the engineer."]
    for i, r in enumerate(rows):
        msp.add_text(r, height=200, dxfattribs={"layer": "A-TITLE", "color": 7}).set_placement((x0 + 200, y1 - 400 - i * 430))
    notes = ["Dimensions in mm.", "Walls 200 ext / 150 int block,", f"height {H} mm.", "Windows: sill 900, head 2100.", "Doors: 2100 high."]
    for i, r in enumerate(notes):
        msp.add_text(r, height=170, dxfattribs={"layer": "A-TITLE", "color": 7}).set_placement((7800, y1 - 400 - i * 430))

    doc.saveas(f"{STEM}.dxf")
    return doc


def png(doc):
    import matplotlib
    matplotlib.use("Agg")
    from ezdxf.addons.drawing import matplotlib as draw
    draw.qsave(doc.modelspace(), f"{STEM}.png", bg="#FFFFFF", dpi=200)


def workbook():
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    bold = Font(bold=True)
    inp = wb.active
    inp.title = "Inputs"
    inputs = [("Wall height (m)", H / 1000, "brief"),
              ("External wall thickness (m)", T_EXT / 1000, "brief"),
              ("Internal wall thickness (m)", T_INT / 1000, "brief"),
              ("Blocks per m2", BLOCKS_PER_M2, "brief (user)"),
              ("Waste allowance", WASTE, "brief (user)")]
    inp.append(["Input", "Value", "Source"])
    for r in inputs:
        inp.append(list(r))
    # B2 height, B3 ext t, B4 int t, B5 blocks/m2, B6 waste

    ws = wb.create_sheet("Walls")
    ws.append(["Wall", "Type", "Centreline length (m)", "Note"])
    for name, w in WALLS.items():
        ws.append([name, w[0], length(w) / 1000, "drawn centreline, face to face (see Assumptions)"])
    nw = len(WALLS) + 1

    op = wb.create_sheet("Doors and windows")
    op.append(["Mark", "Kind", "Wall", "Wall type", "Width (m)", "Height (m)", "Sill (m)", "Area (m2)"])
    for i, (oid, kind, wname, off, width, ht, sill, *_rest) in enumerate(OPENINGS, start=2):
        op.append([oid, kind, wname, f'=VLOOKUP(C{i},Walls!A:B,2,FALSE)', width / 1000, ht / 1000, sill / 1000, f"=E{i}*F{i}"])
    no = len(OPENINGS) + 1
    op.append([])
    op.append(["Doors", f'=COUNTIF(B2:B{no},"door")'])
    op.append(["Windows", f'=COUNTIF(B2:B{no},"window")'])

    rs = wb.create_sheet("Rooms")
    rs.append(["Room", "Internal length E-W (m)", "Internal width N-S (m)", "Area (m2)", "Window"])
    win = {"Living room": "W1", "Kitchen": "W2", "Bedroom 1": "W3", "Bathroom": "W4", "Bedroom 2": "W5", "Corridor": "none (internal)"}
    for i, (name, (x0, y0, x1, y1)) in enumerate(ROOMS.items(), start=2):
        rs.append([name, (x1 - x0) / 1000, (y1 - y0) / 1000, f"=B{i}*C{i}", win[name]])
    nr = len(ROOMS) + 1
    rs.append(["Total", None, None, f"=SUM(D2:D{nr})"])

    q = wb.create_sheet("Quantities")
    q.append(["Quantity", "External", "Internal", "Unit", "Working"])
    O = f"'Doors and windows'!"
    rows = [
        ("Centreline length", f'=SUMIF(Walls!B2:B{nw},"ext",Walls!C2:C{nw})', f'=SUMIF(Walls!B2:B{nw},"int",Walls!C2:C{nw})', "m", "sum of wall centreline lengths"),
        ("Wall thickness", "=Inputs!B3", "=Inputs!B4", "m", "input"),
        ("Opening widths in this wall type", f'=SUMIF({O}D2:D{no},"ext",{O}E2:E{no})', f'=SUMIF({O}D2:D{no},"int",{O}E2:E{no})', "m", "sum of door + window widths"),
        ("Wall plan area", "=B2*B3-B4*B3", "=C2*C3-C4*C3", "m2", "CL x t - openings x t; check vs measure_dxf"),
        ("Gross wall face area", "=B2*Inputs!$B$2", "=C2*Inputs!$B$2", "m2", "CL x height"),
        ("Openings face area", f'=SUMIF({O}D2:D{no},"ext",{O}H2:H{no})', f'=SUMIF({O}D2:D{no},"int",{O}H2:H{no})', "m2", "sum of width x height"),
        ("Net wall face area", "=B6-B7", "=C6-C7", "m2", "gross - openings"),
        ("Blocks", "=ROUNDUP(B8*Inputs!$B$5*(1+Inputs!$B$6),0)", "=ROUNDUP(C8*Inputs!$B$5*(1+Inputs!$B$6),0)", "no.", "ROUNDUP(net x blocks/m2 x (1+waste))"),
    ]
    for r in rows:
        q.append(list(r))
    q.append(["Total blocks (200 + 150 mm)", "=B9+C9", None, "no.", "two block sizes, order separately"])

    a = wb.create_sheet("Assumptions")
    a.append(["Assumption"])
    for t in [
        "Blocks per m2 (12.5) and waste (5%) given by the user; the two block sizes are ordered separately.",
        "Centreline length: external walls = centreline ring (39.2 m); internal walls measured face to face between the walls they meet.",
        "Window size 1200 high, sill 900, head 2100 (bathroom 600 wide). Assumed, confirm.",
        "Doors 2100 high: front 1000 wide, internal 800 wide. Assumed, confirm.",
        "Corridor is internal and has no window (it has no external wall).",
        "Block count ignores lintels, gables, bond beams and ring beams; face areas from finished floor to wall top.",
        "North is up; the road and front door face south.",
    ]:
        a.append([t])
    for s in wb.worksheets:
        for c in s[1]:
            c.font = bold
        s.column_dimensions["A"].width = 34
        for col in "BCDE":
            s.column_dimensions[col].width = 18
    wb.save(f"{STEM}-quantities.xlsx")

    # values computed in Python, to compare with Excel and the measured DXF
    cl = {k: sum(length(w) for w in WALLS.values() if w[0] == k) / 1000 for k in ("ext", "int")}
    t = {"ext": T_EXT / 1000, "int": T_INT / 1000}
    ow = {k: sum(o[4] for o in OPENINGS if WALLS[o[2]][0] == k) / 1000 for k in t}
    oa = {k: sum(o[4] * o[5] for o in OPENINGS if WALLS[o[2]][0] == k) / 1e6 for k in t}
    for k in t:
        plan = cl[k] * t[k] - ow[k] * t[k]
        net = cl[k] * H / 1000 - oa[k]
        print(f"{k}: CL {cl[k]:.3f} m, plan area {plan:.5f} m2, gross face {cl[k]*H/1000:.4f}, net face {net:.4f}, "
              f"blocks {math.ceil(round(net * BLOCKS_PER_M2 * (1 + WASTE), 6))}")
    for name, (x0, y0, x1, y1) in ROOMS.items():
        print(f"room {name}: {(x1-x0)/1000:.3f} x {(y1-y0)/1000:.3f} = {(x1-x0)*(y1-y0)/1e6:.4f} m2")


if __name__ == "__main__":
    doc = draw()
    png(doc)
    workbook()
    print("wrote", STEM + ".dxf", STEM + ".png", STEM + "-quantities.xlsx")
