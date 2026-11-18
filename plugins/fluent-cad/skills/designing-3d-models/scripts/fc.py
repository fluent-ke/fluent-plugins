"""Client for the FreeCAD MCP add-on's local XML-RPC bridge (the same calls the `freecad` MCP makes).

  python3 fc.py ping                              runs a one-line script: proves FreeCAD's window answers
  python3 fc.py exec script.py [NAME=value ...]   run a script on FreeCAD's GUI thread; each NAME=value
                                                  is defined as a Python string before the script runs
  python3 fc.py shot View out.png [--xray]       save the active 3D view: Hero, Isometric, Top, Front,
                                                  Right, Dimetric; --xray shows the parts 70% see-through
"""
import os
import socket
import sys
import xmlrpc.client

STUCK = ("FreeCAD's window has stopped answering. Force-quit FreeCAD (macOS: Option-Command-Esc; "
         "Windows: Task Manager), launch it again with start_freecad_bridge.py, and re-run the build "
         "script: it rebuilds the document from scratch.")


class Timeout(xmlrpc.client.Transport):
    def make_connection(self, host):
        connection = super().make_connection(host)
        connection.timeout = 120  # the bridge itself gives up on the GUI thread after 90 s
        return connection


bridge = xmlrpc.client.ServerProxy("http://127.0.0.1:9875", allow_none=True, transport=Timeout())


def run(code):
    result = bridge.execute_code(code)
    if not result.get("success"):
        sys.exit(STUCK if "GUI dispatch gave up" in str(result) else result)
    return result.get("message")


SHOT = """
import FreeCAD as App, FreeCADGui as Gui
doc = Gui.ActiveDocument
if doc is None or not hasattr(doc.ActiveView, "saveImage"):
    raise RuntimeError("no 3D view: open the document's 3D view tab")
view = doc.ActiveView
shown = [o.ViewObject for o in doc.Document.Objects
         if getattr(o, "ViewObject", None) and o.ViewObject.Visibility and hasattr(o.ViewObject, "Transparency")]
before = [vo.Transparency for vo in shown]
if XRAY:
    for vo in shown:
        vo.Transparency = 70
if VIEW == "Hero":
    view.setCameraOrientation(App.Rotation(App.Vector(0, 0, 1), -15).multiply(App.Rotation(App.Vector(1, 0, 0), 40)))
else:
    getattr(view, "view" + VIEW)()
view.fitAll()
view.saveImage(OUT, 1400, 1000, "Current")
for vo, t in zip(shown, before):
    vo.Transparency = t
"""

command = sys.argv[1] if len(sys.argv) > 1 else "ping"
try:
    if command == "ping":
        run("pass")
        print("bridge up")
    elif command == "exec":
        header = "".join(f"{name} = {value!r}\n" for name, value in (a.split("=", 1) for a in sys.argv[3:]))
        with open(sys.argv[2]) as script:
            print(run(header + script.read()))
    elif command == "shot":
        view, out = sys.argv[2], sys.argv[3]
        run(f"VIEW = {view!r}\nOUT = {os.path.abspath(out)!r}\nXRAY = {'--xray' in sys.argv}\n" + SHOT)
        print("saved", out)
except ConnectionRefusedError:
    sys.exit("FreeCAD bridge not running: in FreeCAD, pick the MCP Addon workbench and click Start RPC Server, "
             "or launch FreeCAD with start_freecad_bridge.py (see freecad-live.md)")
except (socket.timeout, TimeoutError):
    sys.exit(STUCK)
