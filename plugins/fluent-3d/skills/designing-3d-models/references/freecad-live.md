# FreeCAD live modelling

Needs FreeCAD 1.0 or newer with the FreeCAD MCP add-on installed (see the `setting-up-3d-apps` skill).

## Start and connect

Start the bridge from FreeCAD (**MCP Addon** workbench, **Start RPC Server**), or launch FreeCAD with the start-up script:

| OS | Command |
|---|---|
| macOS | `open -a FreeCAD --args "$K/scripts/start_freecad_bridge.py"` |
| Windows | `& "C:\Program Files\FreeCAD 1.1\bin\freecad.exe" "$K\scripts\start_freecad_bridge.py"` (adjust the version folder) |
| Linux | `freecad "$K/scripts/start_freecad_bridge.py"` |

```bash
python3 $K/scripts/fc.py ping                          # "bridge up"
python3 $K/scripts/fc.py exec build.py NAME=value      # runs the script on FreeCAD's GUI thread
python3 $K/scripts/fc.py shot Top top.png              # Isometric, Top, Front, Right, Dimetric ...
```

- When the `freecad` MCP tools (`execute_code`, `get_view`, `get_objects`) are loaded, they use the same bridge; `fc.py` is the fallback.
- The bridge keeps one Python namespace across runs. Pass arguments as `NAME=value` and read them with `globals().pop("NAME")` so stale values can't leak into the next run.
- The first launch shows a Welcome panel on the Start tab. It is not modal; click Done.
- The dark default background hides black parts. Per view: `Gui.getDocument(DOC).ActiveView.getViewer().setBackgroundColor(0.9, 0.9, 0.88)`.
- Hero camera: `view.setCameraOrientation(App.Rotation(App.Vector(0, 0, 1), -15).multiply(App.Rotation(App.Vector(1, 0, 0), 40)))`, then `view.fitAll()`.
- X-ray: set `ViewObject.Transparency = 70` on the shown parts, screenshot, then set it back to 0.
- Colour (1.0+): `m = App.Material(); m.DiffuseColor = rgb; obj.ViewObject.ShapeAppearance = [m]`.

## Build pattern

Worked example: [example_nfc_keychain.py](../scripts/example_nfc_keychain.py), a three-colour keychain with a sealed NFC pocket.

- The script creates the document from scratch, closing an open one of the same name, so re-running is safe.
- A `Spreadsheet::Sheet` named `Params` holds every dimension as an alias. Primitives take expressions: `obj.setExpression("Radius", "Params.lobe_r")`, `obj.setExpression("Placement.Base.x", "Params.grid / 2")`. The user edits a cell and presses Ctrl+R (Cmd+R on macOS).
- Combine with `Part::MultiFuse` and `Part::Cut` (`Refine = True`). Hide the intermediates.
- One final object per print colour. Colour by height: each colour gets its own Z band resting on the band below. A light colour over a dark one needs at least 0.8 mm.
- Put every band boundary and pocket floor and roof on a multiple of the layer height (usually 0.2 mm).
- Shapes built from overlapping circles can leave an uncovered centre. Fill the body below the top band, or a pocket there opens to the air.
- Tell the user before saving, then `doc.saveAs("/abs/path/models/<project>/<Name>.FCStd")`.

## Logos from SVG

An SVG with `width="55mm"` and a matching `viewBox` imports at exactly that size (checked headless with `freecadcmd`).

```python
import FreeCAD, Part, importSVG
importSVG.insert("/abs/logo.svg", doc.Name)
faces = [Part.Face(w) for o in doc.Objects if hasattr(o, "Shape") for w in o.Shape.Wires if w.isClosed()]
solid = faces[0].fuse(faces[1:]).removeSplitter().extrude(FreeCAD.Vector(0, 0, height))
```

Export the SVG with text and strokes converted to outlines; open paths make no faces. For a PNG-only logo built from simple shapes, redraw it with primitives instead of tracing.

## Gates

- `python3 $K/scripts/fc.py exec $K/scripts/freecad_check_export.py DOC=Name OUT=/abs/prefix PARTS=Obj:suffix,... SEALED=Obj`
- Probe a pocket with `shape.isInside(App.Vector(x, y, z), 1e-6, True)`: void inside it, solid above and below.
- Compare the Top view with the reference artwork; the x-ray view must show inserts fully enclosed.
