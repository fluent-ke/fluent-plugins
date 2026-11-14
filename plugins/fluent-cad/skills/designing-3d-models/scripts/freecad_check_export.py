"""Gate, then export, a multi-part FreeCAD model. Run it through the bridge:

  python3 fc.py exec freecad_check_export.py DOC=MyDoc OUT=/abs/path/Prefix \
          PARTS=Body:black,CreamMark:cream,CoralDot:coral SEALED=Body

- Every part must be valid and a single solid. A part listed in SEALED must have exactly 2 shells
  (outer skin + the enclosed insert pocket); 1 shell means the pocket is open to the air.
- Only if all checks pass: writes Prefix_<suffix>.stl per part (fine tessellation, exported in place so
  the parts stack) and Prefix.step, then reports mesh health and Z range per part.
"""
import FreeCAD as App
import MeshPart
import Part


def main(doc_name, out, parts, sealed):
    doc = App.getDocument(doc_name)
    pairs = [p.split(":") for p in parts.split(",")]
    sealed = {s for s in sealed.split(",") if s}
    failed = []
    for name, _ in pairs:
        shape = doc.getObject(name).Shape
        need = 2 if name in sealed else len(shape.Shells)
        ok = shape.isValid() and len(shape.Solids) == 1 and len(shape.Shells) == need
        print(f"{name}: valid={shape.isValid()} solids={len(shape.Solids)} shells={len(shape.Shells)}"
              f"{' (sealed: needs 2)' if name in sealed else ''} -> {'OK' if ok else 'FAIL'}")
        if not ok:
            failed.append(name)
    if failed:
        raise RuntimeError(f"Nothing exported; failed checks: {failed}")
    for name, suffix in pairs:
        mesh = MeshPart.meshFromShape(Shape=doc.getObject(name).Shape, LinearDeflection=0.02,
                                      AngularDeflection=0.1, Relative=False)
        path = f"{out}_{suffix}.stl"
        mesh.write(path)
        box = mesh.BoundBox
        print(f"{path}: {mesh.CountFacets} facets, solid={mesh.isSolid()}, "
              f"non-manifolds={mesh.hasNonManifolds()}, z {box.ZMin:.2f}-{box.ZMax:.2f}")
    Part.export([doc.getObject(name) for name, _ in pairs], f"{out}.step")
    print(f"{out}.step written")


# The bridge keeps one namespace across runs, so take the arguments out of it to avoid stale values.
main(globals().pop("DOC"), globals().pop("OUT"), globals().pop("PARTS"), globals().pop("SEALED", ""))
