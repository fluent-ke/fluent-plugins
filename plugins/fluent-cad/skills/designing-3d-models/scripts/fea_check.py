"""A first stress check of one part in FreeCAD FEM: one fixed face set, one load, linear static.

Run through the bridge (re-running replaces the earlier analysis):
  python3 fc.py exec fea_check.py DOC=ShelfBracket PART=Bracket FIXED=x=min LOAD=x=max FORCE=50 DIR=-y \
                                  E=2000 NU=0.38 MESH=3

FIXED and LOAD pick the part's flat faces lying on one side of its bounding box: x=min, x=max, y=min,
y=max, z=min, z=max. FORCE is newtons, spread over the LOAD faces; DIR is the axis it pushes along
(-y = down when Y is up). E is Young's modulus in MPa and NU Poisson's ratio (PLA about 3500 / 0.36,
PETG about 2000 / 0.38: datasheet values vary, so say they are typical). MESH is the largest element
size in mm. Prints max von Mises stress and max displacement. Needs FreeCAD's FEM workbench with
Gmsh and CalculiX, which the standard FreeCAD download includes.
"""
import time

import FreeCAD as App
import ObjectsFem
from femmesh.gmshtools import GmshTools
from femtools import ccxtools

args = {k: globals().pop(k) for k in ("DOC", "PART", "FIXED", "LOAD", "FORCE", "DIR", "E", "NU", "MESH")}
t0 = time.time()
doc = App.getDocument(args["DOC"])
part = doc.getObject(args["PART"])
shape = part.Shape
bb = shape.BoundBox


def faces_at(side):
    axis, end = side.split("=")
    lo, hi = getattr(bb, axis.upper() + "Min"), getattr(bb, axis.upper() + "Max")
    plane = lo if end == "min" else hi
    picked = [f"Face{i + 1}" for i, f in enumerate(shape.Faces)
              if abs(getattr(f.BoundBox, axis.upper() + "Min") - plane) < 1e-6
              and abs(getattr(f.BoundBox, axis.upper() + "Max") - plane) < 1e-6]
    if not picked:
        raise RuntimeError(f"no flat face at {side}")
    return picked


for name in [o.Name for o in doc.Objects if o.TypeId.startswith("Fem::")]:
    if doc.getObject(name):
        doc.removeObject(name)

analysis = ObjectsFem.makeAnalysis(doc, "Analysis")
analysis.addObject(ObjectsFem.makeSolverCalculiXCcxTools(doc, "Solver"))
material = ObjectsFem.makeMaterialSolid(doc, "Material")
props = material.Material
props.update({"Name": "Print material", "YoungsModulus": f"{args['E']} MPa", "PoissonRatio": args["NU"]})
material.Material = props
analysis.addObject(material)
fixed = ObjectsFem.makeConstraintFixed(doc, "Fixed")
fixed.References = [(part, faces_at(args["FIXED"]))]
analysis.addObject(fixed)
load = ObjectsFem.makeConstraintForce(doc, "Load")
load.References = [(part, faces_at(args["LOAD"]))]
load.Force = f"{args['FORCE']} N"
axis = args["DIR"].lstrip("+-")
edge = next(f"Edge{i + 1}" for i, e in enumerate(shape.Edges)
            if hasattr(e.Curve, "Direction") and abs(abs(getattr(e.Curve.Direction, axis)) - 1) < 1e-9)
load.Direction = (part, [edge])
analysis.addObject(load)
doc.recompute()
if (getattr(load.DirectionVector, axis) > 0) != (not args["DIR"].startswith("-")):
    load.Reversed = True
    doc.recompute()
mesh = ObjectsFem.makeMeshGmsh(doc, "Mesh")
mesh.Shape = part
mesh.CharacteristicLengthMax = f"{args['MESH']} mm"
analysis.addObject(mesh)
doc.recompute()
GmshTools(mesh).create_mesh()

fea = ccxtools.FemToolsCcx(analysis)
fea.purge_results()
fea.run()
result = next(o for o in analysis.Group if o.TypeId == "Fem::FemResultObjectPython")
print(f"{mesh.FemMesh.NodeCount} nodes; max von Mises {max(result.vonMises):.2f} MPa, "
      f"max displacement {max(result.DisplacementLengths):.2f} mm; {time.time() - t0:.0f} s")
