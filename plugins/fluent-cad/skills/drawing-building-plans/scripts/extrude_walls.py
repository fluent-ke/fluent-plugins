# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3"]
# ///
"""Raise a plan's walls into a simple 3D model (OBJ, metres) for a massing view or a walkthrough.

  uv run extrude_walls.py PLAN.dxf OUT.obj [--walls A-WALL-EXT,A-WALL-INT] [--height 2700]
                                           [--windows A-WIND,A-WIND-HIGH:1500:2100] [--doors A-DOOR]
                                           [--sill 900] [--head 2100]

Every closed polyline on a wall layer is extruded from 0 to --height (drawing units, millimetres).
--windows is a comma list of LAYER or LAYER:SILL:HEAD; a layer without its own sill and head takes
--sill and --head, and a layer missing from the drawing is skipped. The default reads ordinary windows
from A-WIND and high windows (toilets, stores) from A-WIND-HIGH at 1500 to 2100. Each closed polyline
on a window layer gets a sill block up to its sill and a lintel from its head to the wall height,
across its outline. Each door swing arc on the door layer (loose, or inside a door block) gets a head
from --head to the wall height across its opening; the wall thickness is read from the jamb at the
hinge. A door whose hinge does not touch a wall's end stays open to full height and is reported. A
floor slab, 150 mm thick with its top at 0, covers the walls' extents.
Written Y up (the OBJ convention), in metres (import at scale 1), with an MTL file beside it colouring
walls, floor, sills and lintels. Blender's default OBJ import turns it back to Z up, so plan X,Y in mm
become Blender X,Y in metres; other apps may need "Y up" chosen on import.
Window boxes follow the outline's bounding box, so angled walls need their windows checked.
A concept model for viewing, not a construction model.
"""
import argparse
import math
import os
import sys

from ezdxf import recover
from ezdxf.math.triangulation import mapbox_earcut_2d

ap = argparse.ArgumentParser()
ap.add_argument("dxf")
ap.add_argument("obj")
ap.add_argument("--walls", default="A-WALL-EXT,A-WALL-INT")
ap.add_argument("--windows", default="A-WIND,A-WIND-HIGH:1500:2100")
ap.add_argument("--doors", default="A-DOOR")
ap.add_argument("--height", type=float, default=2700)
ap.add_argument("--sill", type=float, default=900)
ap.add_argument("--head", type=float, default=2100)
a = ap.parse_args()

doc, _ = recover.readfile(a.dxf)
msp = doc.modelspace()
MM = 0.001
verts, faces, groups = [], [], []


def closed_outlines(layer):
    for e in msp.query(f'LWPOLYLINE POLYLINE[layer=="{layer}"]'):
        if e.dxftype() == "LWPOLYLINE" and e.closed:
            yield [(p[0], p[1]) for p in e.get_points("xy")]
        elif e.dxftype() == "POLYLINE" and e.is_closed:
            yield [(p[0], p[1]) for p in e.points()]


def prism(name, outline, z0, z1):
    if len(outline) > 2 and outline[0] == outline[-1]:
        outline = outline[:-1]
    n, base = len(outline), len(verts) + 1
    for z in (z0, z1):
        verts.extend((x * MM, y * MM, z * MM) for x, y in outline)
    start = len(faces)
    for i in range(n):
        j = (i + 1) % n
        faces.append((base + i, base + j, base + n + j, base + n + i))
    index = {p: i for i, p in enumerate(outline)}
    for tri in mapbox_earcut_2d(outline):
        ids = [index[(v.x, v.y)] for v in tri]
        faces.append(tuple(base + i for i in reversed(ids)))
        faces.append(tuple(base + n + i for i in ids))
    groups.append((name, start, len(faces)))


xs, ys, walls, edges = [], [], 0, []
for layer in a.walls.split(","):
    for outline in closed_outlines(layer):
        prism(layer, outline, 0, a.height)
        edges += [(p, outline[(i + 1) % len(outline)]) for i, p in enumerate(outline)]
        xs += [p[0] for p in outline]
        ys += [p[1] for p in outline]
        walls += 1
if not walls:
    sys.exit(f"No closed polylines on {a.walls}: walls must be closed outlines")

windows, window_count = [], 0
for spec in a.windows.split(","):
    layer, *heights = spec.split(":")
    sill, head = (float(v) for v in heights) if heights else (a.sill, a.head)
    n = 0
    for outline in closed_outlines(layer):
        x0, x1 = min(p[0] for p in outline), max(p[0] for p in outline)
        y0, y1 = min(p[1] for p in outline), max(p[1] for p in outline)
        box = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        prism("sill", box, 0, sill)
        prism("lintel", box, head, a.height)
        n += 1
    window_count += n
    if n:
        windows.append(f"{n} on {layer} ({sill:g}-{head:g})")

def door_arcs():
    for e in msp.query(f'ARC INSERT[layer=="{a.doors}"]'):
        if e.dxftype() == "ARC":
            yield e
        else:
            yield from (v for v in e.virtual_entities() if v.dxftype() == "ARC")


def jamb_depth(h, inward):
    """Length of the wall end face that starts at the hinge and runs along `inward`: the wall thickness."""
    for p, q in edges:
        for s0, s1 in ((p, q), (q, p)):
            if math.dist(s0, h) < 1:
                v = (s1[0] - s0[0], s1[1] - s0[1])
                n = math.hypot(*v)
                if n and (v[0] * inward[0] + v[1] * inward[1]) / n > 0.999:
                    return n
    return None


doors, open_doors = 0, 0
for arc in door_arcs():
    h, r = (arc.dxf.center.x, arc.dxf.center.y), arc.dxf.radius
    ends = [(p.x, p.y) for p in (arc.start_point, arc.end_point)]
    for jamb, leaf in (ends, ends[::-1]):
        inward = ((h[0] - leaf[0]) / r, (h[1] - leaf[1]) / r)  # from the swing side into the wall
        t = jamb_depth(h, inward)
        if t:
            box = [h, jamb, (jamb[0] + inward[0] * t, jamb[1] + inward[1] * t), (h[0] + inward[0] * t, h[1] + inward[1] * t)]
            prism("lintel", box, a.head, a.height)
            doors += 1
            break
    else:
        open_doors += 1

slab = [(min(xs), min(ys)), (max(xs), min(ys)), (max(xs), max(ys)), (min(xs), max(ys))]
prism("floor", slab, -150, 0)

COLOURS = {"wall": (0.86, 0.84, 0.80), "floor": (0.42, 0.38, 0.34), "sill": (0.95, 0.95, 0.93), "lintel": (0.95, 0.95, 0.93)}
mtl = a.obj.rsplit(".", 1)[0] + ".mtl"
with open(mtl, "w") as f:
    for name, (r, g, b) in COLOURS.items():
        f.write(f"newmtl {name}\nKd {r} {g} {b}\n\n")
with open(a.obj, "w") as f:
    f.write("# extrude_walls.py: concept model, metres, Y up (the OBJ convention)\n")
    f.write(f"mtllib {os.path.basename(mtl)}\n")
    f.writelines(f"v {x:.4f} {z:.4f} {-y:.4f}\n" for x, y, z in verts)
    for name, s, e in groups:
        f.write(f"g {name}\nusemtl {name if name in COLOURS else 'wall'}\n")
        f.writelines("f " + " ".join(map(str, face)) + "\n" for face in faces[s:e])
if open_doors:
    print(f"{open_doors} door arcs on {a.doors} have no wall end at the hinge: those openings stay full height")
print(f"{walls} wall pieces, {window_count} windows ({', '.join(windows) or 'none'}), {doors} door heads, floor {(max(xs) - min(xs)) * MM:.2f} x "
      f"{(max(ys) - min(ys)) * MM:.2f} m -> {a.obj}")
