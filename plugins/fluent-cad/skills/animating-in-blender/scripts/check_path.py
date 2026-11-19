# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3", "shapely>=2"]
# ///
"""Check a walkthrough path against the plan's walls before rendering. Read-only.

  uv run check_path.py PLAN.dxf --path "x,y;x,y;..." [--clearance 0.3] [--walls A-WALL-EXT,A-WALL-INT]

The path is the one given to animate_model.py: metres in the scene, which are the plan's millimetres
divided by 1000. Every closed polyline on the wall layers is a wall. For each segment it prints the
nearest wall distance, and FAIL when the segment passes through a wall or comes closer than
--clearance. It also prints the path length and the --seconds that walks it at 1.2 m/s.
Exit code 1 when any segment fails.
"""
import argparse
import sys

from ezdxf import recover
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

ap = argparse.ArgumentParser()
ap.add_argument("dxf")
ap.add_argument("--path", required=True)
ap.add_argument("--clearance", type=float, default=0.3)
ap.add_argument("--walls", default="A-WALL-EXT,A-WALL-INT")
a = ap.parse_args()

doc, _ = recover.readfile(a.dxf)
msp = doc.modelspace()
outlines = []
for layer in a.walls.split(","):
    for e in msp.query(f'LWPOLYLINE POLYLINE[layer=="{layer}"]'):
        if e.dxftype() == "LWPOLYLINE" and e.closed:
            outlines.append([(p[0] / 1000, p[1] / 1000) for p in e.get_points("xy")])
        elif e.dxftype() == "POLYLINE" and e.is_closed:
            outlines.append([(p[0] / 1000, p[1] / 1000) for p in e.points()])
if not outlines:
    sys.exit(f"No closed polylines on {a.walls}: walls must be closed outlines")
walls = unary_union([Polygon(o).buffer(0) for o in outlines if len(o) > 2])

points = [tuple(float(v) for v in p.split(",")) for p in a.path.split(";")]
failed = False
for i, p in enumerate(points):
    if walls.contains(Point(p)):
        print(f"point {i + 1} {p}: FAIL, inside a wall")
        failed = True
for i, (p, q) in enumerate(zip(points, points[1:])):
    seg = LineString([p, q])
    d = seg.distance(walls)
    verdict = "FAIL, through a wall" if seg.intersects(walls) else "FAIL, too close" if d < a.clearance else "ok"
    failed |= verdict != "ok"
    print(f"segment {i + 1} {p} -> {q}: {seg.length:.2f} m, nearest wall {d:.2f} m  {verdict}")
length = LineString(points).length if len(points) > 1 else 0
print(f"path {length:.2f} m; at 1.2 m/s use --seconds {max(length / 1.2, 1):.0f}")
print("PATH_FAIL" if failed else "PATH_OK")
sys.exit(1 if failed else 0)
