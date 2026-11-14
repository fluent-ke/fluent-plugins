"""Pass to FreeCAD at launch to start the FreeCAD MCP add-on's localhost RPC server (needs the add-on installed)."""
import FreeCAD, FreeCADGui
from rpc_server import rpc_server
FreeCADGui.activateWorkbench("PartWorkbench")
FreeCAD.Console.PrintMessage("[agent bridge] " + str(rpc_server.start_rpc_server()) + "\n")
