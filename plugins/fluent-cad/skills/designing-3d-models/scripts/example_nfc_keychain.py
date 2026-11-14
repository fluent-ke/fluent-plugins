"""Example: a three-colour NFC keychain, as a parametric FreeCAD model.

Run inside FreeCAD (Macro > Macros... > Execute, or `fc.py exec example_nfc_keychain.py`).
It builds the document `NFC_Keychain`. Every dimension lives in the `Params`
spreadsheet: edit a cell there and press Recompute (Ctrl+R, Cmd+R on macOS).

A black keychain with a four-dot logo in cream and one coral dot on top.
Each colour sits at its own height, so it prints with an AMS or with manual filament swaps.

Parts:
  Body       black, printed back-side down, with a sealed 26 mm NFC pocket inside
  CreamMark  the four-dot mark in canvas cream, on top of the body
  CoralDot   the lower-right dot in coral, on top of the cream
  TagGhost   a see-only 25 mm tag disc showing where the NFC sticker sits (never exported)
"""
import FreeCAD as App
import FreeCADGui as Gui

DOC = "NFC_Keychain"

PARAMS = [
    ("lobe_r", 15.0, "Logo dot radius (mm)"),
    ("grid", 25.0, "Dot centre-to-centre spacing (mm)"),
    ("rim", 1.0, "Black border around the logo, seen from the top (0 = none)"),
    ("body_h", 3.4, "Black body thickness (mm)"),
    ("cream_h", 0.8, "Cream logo layer thickness; 0.8 mm hides the black below"),
    ("coral_h", 0.6, "Coral dot height above the cream (mm)"),
    ("tag_d", 26.0, "NFC pocket diameter: 25 mm tag + 1 mm clearance"),
    ("tag_depth", 1.0, "NFC pocket depth (26 x 1 mm slot per tag vendors; must be >= tag thickness)"),
    ("tag_floor", 1.4, "Plastic under the tag (mm)"),
    ("loop_y", 36.5, "Keyring loop centre, measured up from logo centre (mm)"),
    ("loop_r", 7.5, "Keyring loop outer radius (mm)"),
    ("hole_d", 5.0, "Keyring hole diameter (mm)"),
    ("neck_w", 10.0, "Width of the neck joining loop to logo (mm)"),
]

INK = (0x1F / 255, 0x1E / 255, 0x1D / 255)
CREAM = (0xF5 / 255, 0xF4 / 255, 0xEE / 255)
CORAL = (0xD9 / 255, 0x77 / 255, 0x57 / 255)
TAG = (0.55, 0.75, 0.95)

if DOC in App.listDocuments():
    App.closeDocument(DOC)
doc = App.newDocument(DOC)

sheet = doc.addObject("Spreadsheet::Sheet", "Params")
for row, (alias, value, label) in enumerate(PARAMS, start=1):
    sheet.set(f"A{row}", label)
    sheet.set(f"B{row}", str(value))
    sheet.setAlias(f"B{row}", alias)
doc.recompute()


def cylinder(name, radius, height, x="0", y="0", z="0"):
    obj = doc.addObject("Part::Cylinder", name)
    obj.setExpression("Radius", radius)
    obj.setExpression("Height", height)
    obj.setExpression("Placement.Base.x", x)
    obj.setExpression("Placement.Base.y", y)
    obj.setExpression("Placement.Base.z", z)
    return obj


def fuse(name, shapes):
    obj = doc.addObject("Part::MultiFuse", name)
    obj.Shapes = shapes
    obj.Refine = True
    return obj


def four_dots(prefix, radius, height, z="0"):
    return [
        cylinder(f"{prefix}_TL", radius, height, f"-{half}", half, z),
        cylinder(f"{prefix}_TR", radius, height, half, half, z),
        cylinder(f"{prefix}_BL", radius, height, f"-{half}", f"-{half}", z),
        cylinder(f"{prefix}_BR", radius, height, half, f"-{half}", z),
    ]


half = "Params.grid / 2"
top = "Params.body_h"

# Black body: the mark grown by the rim, plus the neck and keyring loop.
dots = fuse("BodyDots", four_dots("BodyDot", "Params.lobe_r + Params.rim", top))
neck = doc.addObject("Part::Box", "Neck")
neck.setExpression("Length", "Params.neck_w")
neck.setExpression("Width", f"Params.loop_y - {half}")
neck.setExpression("Height", top)
neck.setExpression("Placement.Base.x", "-Params.neck_w / 2")
neck.setExpression("Placement.Base.y", half)
loop = cylinder("Loop", "Params.loop_r", top, y="Params.loop_y")
# No dot covers the logo's centre; fill it so the tag pocket stays sealed.
centre_fill = cylinder("CentreFill", half, top)
blank = fuse("BodyBlank", [dots, neck, loop, centre_fill])

key_hole = cylinder("KeyHole", "Params.hole_d / 2", f"{top} + 2", y="Params.loop_y", z="-1")
tag_pocket = cylinder("TagPocket", "Params.tag_d / 2", "Params.tag_depth", z="Params.tag_floor")
body = doc.addObject("Part::Cut", "Body")
body.Base, body.Tool = blank, fuse("Cutters", [key_hole, tag_pocket])
body.Refine = True

# Cream covers all four dots (the coral dot needs something under it when printed with filament swaps).
cream = fuse("CreamMark", four_dots("CreamDot", "Params.lobe_r", "Params.cream_h", top))
coral = cylinder("CoralDot", "Params.lobe_r", "Params.coral_h", half, f"-{half}", f"{top} + Params.cream_h")
ghost = cylinder("TagGhost", "12.5", "0.3", z="Params.tag_floor + 0.1")

doc.recompute()


def paint(obj, rgb):
    vo = obj.ViewObject
    try:
        material = App.Material()
        material.DiffuseColor = rgb
        vo.ShapeAppearance = [material]
    except Exception:
        vo.ShapeColor = rgb


shown = {"Body": INK, "CreamMark": CREAM, "CoralDot": CORAL, "TagGhost": TAG}
for obj in doc.Objects:
    if obj.TypeId.startswith("Part::"):
        obj.ViewObject.Visibility = obj.Name in shown
        if obj.Name in shown:
            paint(obj, shown[obj.Name])

view = Gui.getDocument(DOC).ActiveView
view.setCameraOrientation(App.Rotation(App.Vector(0, 0, 1), -15).multiply(App.Rotation(App.Vector(1, 0, 0), 40)))
view.fitAll()

shape = body.Shape
bb = shape.BoundBox.united(cream.Shape.BoundBox).united(coral.Shape.BoundBox)
print(f"Body valid={shape.isValid()} solids={len(shape.Solids)} shells={len(shape.Shells)} "
      f"(2 shells = sealed internal NFC pocket); cream valid={cream.Shape.isValid()}")
print(f"Overall {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength:.1f} mm")
print(f"Colour heights: black 0-{sheet.body_h:.1f}, cream {sheet.body_h:.1f}-{sheet.body_h + sheet.cream_h:.1f}, "
      f"coral {sheet.body_h + sheet.cream_h:.1f}-{sheet.body_h + sheet.cream_h + sheet.coral_h:.1f} mm; "
      f"tag pause at z = {sheet.tag_floor + sheet.tag_depth:.1f} mm")
