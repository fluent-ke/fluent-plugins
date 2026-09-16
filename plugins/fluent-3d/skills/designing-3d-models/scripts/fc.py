"""Client for the FreeCAD MCP add-on's local XML-RPC bridge (the same calls the `freecad` MCP makes).

  python3 fc.py ping
  python3 fc.py exec script.py [NAME=value ...]   run a script on FreeCAD's GUI thread; each NAME=value
                                                  is defined as a Python string before the script runs
  python3 fc.py shot View out.png [object]       save the 3D view: Isometric, Top, Front, Right, Dimetric...
"""
import base64
import sys
import xmlrpc.client

bridge = xmlrpc.client.ServerProxy("http://127.0.0.1:9875", allow_none=True)
command = sys.argv[1] if len(sys.argv) > 1 else "ping"
try:
    if command == "ping":
        print("bridge up" if bridge.ping() else "bridge not responding")
    elif command == "exec":
        header = "".join(f"{name} = {value!r}\n" for name, value in (a.split("=", 1) for a in sys.argv[3:]))
        with open(sys.argv[2]) as script:
            result = bridge.execute_code(header + script.read())
        print(result.get("message") if result.get("success") else result)
        sys.exit(0 if result.get("success") else 1)
    elif command == "shot":
        image = bridge.get_active_screenshot(sys.argv[2], 1400, 1000, sys.argv[4] if len(sys.argv) > 4 else None)
        if not image:
            sys.exit("no screenshot: the active tab must be a 3D view")
        with open(sys.argv[3], "wb") as out:
            out.write(base64.b64decode(image))
        print("saved", sys.argv[3])
except ConnectionRefusedError:
    sys.exit("FreeCAD bridge not running: in FreeCAD, pick the MCP Addon workbench and click Start RPC Server, "
             "or launch FreeCAD with start_freecad_bridge.py (see freecad-live.md)")
