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
CHECKED_BY = "the engineer"  # who signs the drawing
NORTH = "North is up; the road and front door face south."

H = 2700            # wall height, mm
T_EXT, T_INT = 200, 150
BLOCKS_PER_M2, WASTE = 12.5, 0.05
MORTAR_EXT, MORTAR_INT = 0.020, 0.015  # m3 of mortar per m2 of wall face, 200 and 150 mm block
RATES_FROM = "assumed: confirm with the QS"  # or "brief" when the person gave the rates
SILL, HEAD = 900, 2100  # windows at another sill go on A-WIND-HIGH; extrude_walls.py reads its sill from there

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

# Rooms: name -> clear internal rectangle (x0, y0, x1, y1). A room narrower than 1.6 m gets its name and
# area on one smaller line. TEXT_AT moves a room's text off a door swing or dimension: name -> (x, y).
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

TEXT_AT = {}

LAYERS = {"A-WALL-EXT": 7, "A-WALL-INT": 8, "A-DOOR": 1, "A-WIND": 5, "A-WIND-HIGH": 5, "A-DIMS": 7, "A-TEXT": 7, "A-TITLE": 7}


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


def extents():
    """Outside faces of the external walls: (x0, y0, x1, y1)."""
    pts = [p for w in WALLS.values() if w[0] == "ext" for p in rect(*frame(w), 0, length(w), w[3])]
    return min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)


def window_layer(sill):
    return "A-WIND" if sill == SILL else "A-WIND-HIGH"


def draw():
    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4
    doc.header["$MEASUREMENT"] = 1
    for name, colour in LAYERS.items():
        doc.layers.add(name, color=colour)
    area_layer = doc.layers.add("A-AREA", color=3)  # room outlines for measuring: hidden, never plotted
    area_layer.dxf.plot = 0
    area_layer.off()
    ds = doc.dimstyles.new("MM100")  # 1:100 on paper: 150 drawing units = 1.5 mm text, to fit small rooms
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
            layer = window_layer(sill)
            msp.add_lwpolyline(rect(origin, d, n, off, off + width, t), close=True, dxfattribs={"layer": layer})
            for o in (-25, 25):
                msp.add_line(pt(origin, d, n, off, o), pt(origin, d, n, off + width, o), dxfattribs={"layer": layer})
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
    X0, Y0, X1, Y1 = extents()
    centre = ((X0 + X1) / 2, (Y0 + Y1) / 2)
    for oid, kind, wname, off, width, *_ in OPENINGS:
        if kind == "window":  # label on the side of the wall away from the building's centre: outside
            origin, d, n = frame(WALLS[wname])
            label = max((pt(origin, d, n, off + width / 2, o) for o in (-350, 350)), key=lambda p: math.dist(p, centre))
            msp.add_text(oid, height=120, dxfattribs={"layer": "A-TEXT", "color": 7}).set_placement(
                label, align=TextEntityAlignment.MIDDLE_CENTER)

    for name, (x0, y0, x1, y1) in ROOMS.items():
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "A-AREA"})
        area = (x1 - x0) * (y1 - y0) / 1e6
        cx, cy = TEXT_AT.get(name, (cx, cy))
        if min(x1 - x0, y1 - y0) < 1600:
            msp.add_text(f"{name}  {area:.2f} m2", height=120, dxfattribs={"layer": "A-TEXT", "color": 7}).set_placement(
                (cx, cy), align=TextEntityAlignment.MIDDLE_CENTER)
        else:
            msp.add_text(name, height=200, dxfattribs={"layer": "A-TEXT", "color": 7}).set_placement(
                (cx, cy + 150), align=TextEntityAlignment.MIDDLE_CENTER)
            msp.add_text(f"{area:.2f} m2", height=150, dxfattribs={"layer": "A-TEXT", "color": 7}).set_placement(
                (cx, cy - 150), align=TextEntityAlignment.MIDDLE_CENTER)
        hy, vx = DIM_AT.get(name, (None, None))
        if hy is not None:
            msp.add_linear_dim(base=(x0, hy), p1=(x0, hy), p2=(x1, hy), dimstyle="MM100",
                               dxfattribs={"layer": "A-DIMS"}).render()
        if vx is not None:
            msp.add_linear_dim(base=(vx, y0), p1=(vx, y0), p2=(vx, y1), angle=90, dimstyle="MM100",
                               dxfattribs={"layer": "A-DIMS"}).render()

    # overall dims, from the outside faces of the external walls
    msp.add_linear_dim(base=(X0, Y0 - 1100), p1=(X0, Y0), p2=(X1, Y0), dimstyle="MM100", dxfattribs={"layer": "A-DIMS"}).render()
    msp.add_linear_dim(base=(X0 - 900, Y0), p1=(X0, Y0), p2=(X0, Y1), angle=90, dimstyle="MM100", dxfattribs={"layer": "A-DIMS"}).render()

    # north arrow, right of the plan
    ax, ay = X1 + 1250, Y1 - 1000
    msp.add_lwpolyline([(ax - 250, ay - 400), (ax, ay + 400), (ax + 250, ay - 400), (ax, ay - 200)], close=True, dxfattribs={"layer": "A-TITLE"})
    msp.add_text("N", height=250, dxfattribs={"layer": "A-TITLE", "color": 7}).set_placement((ax, ay + 700), align=TextEntityAlignment.MIDDLE_CENTER)

    # title block below the plan, at least 12 m wide so its text always fits
    x0, x1, y1 = X0, X0 + max(X1 - X0, 12000), Y0 - 1700
    y0 = y1 - 2900
    split = x1 - 4400  # notes column
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "A-TITLE"})
    msp.add_line((split, y0), (split, y1), dxfattribs={"layer": "A-TITLE"})
    rows = [f"Client: {CLIENT}", f"Project: {PROJECT}", f"Drawing: {TITLE}",
            f"Revision: {REV}    Scale: 1:100 at A3    Date: {datetime.date.today():%d %b %Y}",
            f"Checked by: {CHECKED_BY}", "Drawn by AI. To be checked by the engineer."]
    for i, r in enumerate(rows):
        msp.add_text(r, height=200, dxfattribs={"layer": "A-TITLE", "color": 7}).set_placement((x0 + 200, y1 - 400 - i * 430))
    door_h = door_heights()
    notes = ["Dimensions in mm.", f"Walls {T_EXT} ext / {T_INT} int block,", f"height {H} mm.",
             f"Windows: sill {SILL}, head {HEAD}", "unless noted.", f"Doors: {'/'.join(map(str, door_h))} high."]
    for i, r in enumerate(notes):
        msp.add_text(r, height=170, dxfattribs={"layer": "A-TITLE", "color": 7}).set_placement((split + 200, y1 - 400 - i * 430))

    doc.saveas(f"{STEM}.dxf")
    return doc


def door_heights():
    return sorted({o[5] for o in OPENINGS if o[1] == "door"})


def png(doc):
    import matplotlib
    matplotlib.use("Agg")
    from ezdxf.addons.drawing import matplotlib as draw
    draw.qsave(doc.modelspace(), f"{STEM}.png", bg="#FFFFFF", dpi=300)


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
              ("Blocks per m2", BLOCKS_PER_M2, RATES_FROM),
              ("Waste allowance", WASTE, RATES_FROM),
              ("Mortar per m2, external (m3)", MORTAR_EXT, RATES_FROM),
              ("Mortar per m2, internal (m3)", MORTAR_INT, RATES_FROM)]
    inp.append(["Input", "Value", "Source"])
    for r in inputs:
        inp.append(list(r))
    # B2 height, B3 ext t, B4 int t, B5 blocks/m2, B6 waste, B7 mortar ext, B8 mortar int

    ws = wb.create_sheet("Walls")
    ws.append(["Wall", "Type", "Centreline length (m)", "Note"])
    for name, w in WALLS.items():
        ws.append([name, w[0], length(w) / 1000, "centreline, part of the external ring" if w[0] == "ext"
                   else "centreline, face to face between the walls it meets"])
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
    def windows_of(x0, y0, x1, y1):  # windows whose middle lies within a wall thickness of the room
        found = []
        for oid, kind, wname, off, width, *_ in OPENINGS:
            if kind == "window":
                mx, my = pt(*frame(WALLS[wname]), off + width / 2, 0)
                if x0 - T_EXT <= mx <= x1 + T_EXT and y0 - T_EXT <= my <= y1 + T_EXT:
                    found.append(oid)
        return ", ".join(found) or "none"
    for i, (name, (x0, y0, x1, y1)) in enumerate(ROOMS.items(), start=2):
        rs.append([name, (x1 - x0) / 1000, (y1 - y0) / 1000, f"=B{i}*C{i}", windows_of(x0, y0, x1, y1)])
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
    q.append(["Total blocks", "=B9+C9", None, "no.", "two block sizes, order separately"])
    q.append(["Mortar", "=ROUND(B8*Inputs!$B$7,2)", "=ROUND(C8*Inputs!$B$8,2)", "m3", "net face x mortar per m2"])

    a = wb.create_sheet("Assumptions")
    a.append(["Assumption"])
    ring = sum(length(w) for w in WALLS.values() if w[0] == "ext") / 1000
    widths = sorted({o[4] for o in OPENINGS if o[1] == "door"})
    for t in [
        f"Blocks per m2 ({BLOCKS_PER_M2}), waste ({WASTE:.0%}) and mortar per m2: {RATES_FROM}. The two block sizes are ordered separately.",
        f"Centreline length: external walls = centreline ring ({ring:.1f} m); internal walls measured face to face between the walls they meet.",
        f"Windows sill {SILL}, head {HEAD} unless listed otherwise in 'Doors and windows'. Assumed, confirm.",
        f"Doors {'/'.join(str(h) for h in door_heights())} high, {'/'.join(map(str, widths))} wide. Assumed, confirm.",
        "Rooms with no external wall have no window.",
        "Block count ignores lintels, gables, bond beams and ring beams; face areas from finished floor to wall top.",
        NORTH,
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
