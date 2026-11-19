# /// script
# requires-python = ">=3.9"
# dependencies = ["ezdxf>=1.3", "matplotlib"]
# ///
"""Measure a DXF drawing layer by layer, independently of whoever drew it. Read-only.

  uv run measure_dxf.py PLAN.dxf                 report: audit, units, extents, per-layer measures
  uv run measure_dxf.py PLAN.dxf --png OUT.png   also render the drawing on white
  uv run measure_dxf.py PLAN.dxf --text          also list every text on every layer
  uv run measure_dxf.py PLAN.dxf --json          the same report as JSON
  uv run measure_dxf.py PLAN.dxf --rooms A-AREA  the room outline layer to list room by room (the default)

Per layer it reports: entity counts by type, the area enclosed by closed polylines (in drawing
units squared), the length of open lines, polylines and arcs, block inserts counted by name, and
each dimension's value measured from its own definition points. A dimension whose text was typed
over (not the measured "<>") is listed beside what it really measures, since that is where a drawing
and its quantities part ways.
On the --rooms layer every closed outline is also listed on its own: its area in m2 (drawing units
mm) and its bounding box width x height, so each room can be checked against the workbook.
Arcs inside polylines (bulges) are measured as straight segments; the report says when that
happened. DWG files must be saved as DXF first (AutoCAD: SAVEAS, DXF).
"""
import argparse
import json
import math
import sys
from collections import Counter, defaultdict

import ezdxf
from ezdxf import bbox, recover
from ezdxf.math import area

UNITS = {0: "unitless", 1: "inches", 2: "feet", 4: "millimetres", 5: "centimetres", 6: "metres"}


def measure(path, want_text, rooms_layer="A-AREA"):
    doc, auditor = recover.readfile(path)
    msp = doc.modelspace()
    layers = defaultdict(lambda: {"types": Counter(), "closed_area": 0.0, "closed_count": 0,
                                  "open_length": 0.0, "inserts": Counter(), "texts": [], "bulges": 0, "dims": [], "typed_dims": []})
    rooms = []
    for e in msp:
        kind, L = e.dxftype(), layers[e.dxf.layer]
        L["types"][kind] += 1
        if kind == "LWPOLYLINE" or (kind == "POLYLINE" and e.is_2d_polyline):
            pts = [(p[0], p[1]) for p in (e.get_points("xy") if kind == "LWPOLYLINE" else e.points())]
            if kind == "LWPOLYLINE" and any(b for *_, b in e.get_points("xyb")):
                L["bulges"] += 1
            if e.closed if kind == "LWPOLYLINE" else e.is_closed:
                L["closed_area"] += abs(area(pts))
                L["closed_count"] += 1
                if e.dxf.layer == rooms_layer:
                    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
                    rooms.append({"area_m2": round(abs(area(pts)) / 1e6, 6),
                                  "width": round(max(xs) - min(xs), 1), "height": round(max(ys) - min(ys), 1),
                                  "at": [round(min(xs), 1), round(min(ys), 1)]})
            else:
                L["open_length"] += sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
        elif kind == "LINE":
            L["open_length"] += e.dxf.start.vec2.distance(e.dxf.end.vec2)
        elif kind == "ARC":
            sweep = (e.dxf.end_angle - e.dxf.start_angle) % 360
            L["open_length"] += e.dxf.radius * math.radians(sweep)
        elif kind == "INSERT":
            L["inserts"][e.dxf.name] += 1
        elif kind == "DIMENSION":
            value = e.get_measurement()
            if isinstance(value, (int, float)):
                L["dims"].append(round(value, 1))
                typed = e.dxf.get("text", "")
                if typed not in ("", "<>") and "<>" not in typed:
                    L["typed_dims"].append({"text": typed, "measures": round(value, 1)})
        elif kind in ("TEXT", "MTEXT") and want_text:
            L["texts"].append(e.plain_text() if kind == "MTEXT" else e.dxf.text)

    box = bbox.extents(msp)
    report = {
        "file": path,
        "dxf_version": doc.dxfversion,
        "audit_errors": len(auditor.errors),
        "audit_fixes": len(auditor.fixes),
        "units": UNITS.get(doc.header.get("$INSUNITS", 0), f"code {doc.header.get('$INSUNITS')}"),
        "extents": [round(box.size.x, 3), round(box.size.y, 3)] if box.has_data else None,
        "layers": {},
        "rooms": {"layer": rooms_layer, "outlines": rooms},
    }
    for name in sorted(layers):
        L = layers[name]
        lb = bbox.extents(msp.query(f'*[layer=="{name}"]'))
        report["layers"][name] = {
            "entities": dict(L["types"]),
            "closed_polylines": L["closed_count"],
            "closed_area": round(L["closed_area"], 3),
            "open_length": round(L["open_length"], 3),
            "inserts": dict(L["inserts"]),
            **({"dimensions": L["dims"]} if L["dims"] else {}),
            **({"typed_over_dimensions": L["typed_dims"]} if L["typed_dims"] else {}),
            "extents": [round(lb.size.x, 3), round(lb.size.y, 3)] if lb.has_data else None,
            **({"bulged_polylines": L["bulges"]} if L["bulges"] else {}),
            **({"texts": L["texts"]} if want_text else {}),
        }
    return doc, report


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dxf")
    ap.add_argument("--png", help="render the drawing to this PNG")
    ap.add_argument("--text", action="store_true", help="list texts per layer")
    ap.add_argument("--json", action="store_true", help="print JSON")
    ap.add_argument("--rooms", default="A-AREA", help="layer of room outlines to list one by one")
    a = ap.parse_args()
    try:
        doc, r = measure(a.dxf, a.text, a.rooms)
    except (IOError, ezdxf.DXFStructureError) as err:
        sys.exit(f"Cannot read {a.dxf}: {err}")

    if a.png:
        import matplotlib
        matplotlib.use("Agg")
        from ezdxf.addons.drawing import matplotlib as draw
        draw.qsave(doc.modelspace(), a.png, bg="#FFFFFF", dpi=200)
        r["png"] = a.png

    if a.json:
        print(json.dumps(r, indent=2))
        return
    print(f"{r['file']}  DXF {r['dxf_version']}  units: {r['units']}  "
          f"audit: {r['audit_errors']} errors, {r['audit_fixes']} fixes")
    if r["extents"]:
        print(f"Drawing extents: {r['extents'][0]} x {r['extents'][1]}")
    for name, L in r["layers"].items():
        print(f"\n[{name}]  extents {L['extents'][0]} x {L['extents'][1]}" if L["extents"] else f"\n[{name}]")
        print("  entities: " + ", ".join(f"{k} {v}" for k, v in sorted(L["entities"].items())))
        if L["closed_polylines"]:
            print(f"  closed polylines: {L['closed_polylines']}, enclosed area {L['closed_area']}")
        if L["open_length"]:
            print(f"  open length: {L['open_length']}")
        if L["inserts"]:
            print("  blocks: " + ", ".join(f"{k} x{v}" for k, v in sorted(L["inserts"].items())))
        if L.get("dimensions"):
            print(f"  dimensions ({len(L['dimensions'])}): " + ", ".join(f"{v:g}" for v in L["dimensions"]))
        for d in L.get("typed_over_dimensions", []):
            print(f"  TYPED-OVER dimension: shows '{d['text']}', measures {d['measures']:g}")
        if L.get("bulged_polylines"):
            print(f"  note: {L['bulged_polylines']} polylines have arcs, measured as straight segments")
        for t in L.get("texts", []):
            print(f"  text: {t}")
    rooms = r["rooms"]["outlines"]
    if rooms:
        unit = "" if r["units"] == "millimetres" else f"  (drawing is in {r['units']}: areas assume mm)"
        print(f"\nRooms on {a.rooms} ({len(rooms)}): area m2, bounding box width x height, lower-left corner{unit}")
        for i, room in enumerate(rooms, 1):
            print(f"  room {i}: {room['area_m2']} m2, {room['width']:g} x {room['height']:g}, at {room['at'][0]:g},{room['at'][1]:g}")
    else:
        print(f"\nRooms: no closed outlines on {a.rooms}")
    if a.png:
        print(f"\nRendered {a.png}")


if __name__ == "__main__":
    main()
