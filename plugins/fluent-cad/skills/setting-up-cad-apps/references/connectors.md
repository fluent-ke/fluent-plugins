# Connect an agent to CAD and 3D apps

Official connectors first, then community bridges. Steps change often: when a menu named here is missing, open the vendor page linked in each section and follow it instead. Checked November 2026.

After connecting, test with a read-only request first ("list the objects in the open file"), then a small new object in a new file.

## Blender (official, by Blender)

Needs Claude Desktop (any plan) and Blender; the add-on page states the minimum version (reports say 5.1 or later for add-on 1.0).

1. Claude Desktop: **Customize > Connectors**, search "Blender", **Add**.
2. Open https://www.blender.org/lab/mcp-server/ beside Blender. Drag its install link into the Blender window and allow the **lab** extension repository; drag it in again to install the add-on.
3. Each session: **Edit > Preferences > Add-ons > BlenderMCP**, enable it and click **Start MCP server** (or tick auto start). It listens on `localhost:9876`.

Claude Code: the Desktop connector is not imported by `claude mcp add-from-claude-desktop`. Register the server the Desktop extension installed, from the project folder:

```bash
claude mcp add blender --scope project -- "<Claude Extensions folder>/ant.dir.gh.blender.blender-mcp/.venv/bin/blender-mcp"
```

The `Claude Extensions` folder sits in Claude Desktop's app-support folder (macOS: `~/Library/Application Support/Claude/Claude Extensions`). Restart the session; `claude mcp list` shows `blender` connected.

Blender's own notes say the server runs the agent's code without guards. Save the `.blend` first; changes reach disk only when the user saves.

Different project, same name: `ahujasid/blender-mcp` is a community server set up through `uvx blender-mcp`. Use one or the other, not both.

## Autodesk Fusion (official, by Autodesk)

Needs a Fusion subscription and Claude Desktop, Fusion running first.

1. Fusion: **Preferences > General > API**, tick **Fusion MCP Server (runs locally on this device)**. Endpoint `http://127.0.0.1:27182/mcp`.
2. Claude Desktop: **Settings > Connectors > Add > Browse connectors**, search "Fusion", install **Autodesk Fusion**. Not the separate "Fusion Data MCP Server", which is a cloud server.
3. Test: "create a 10 mm cube".

Claude Code, Codex and other clients take the same URL over Streamable HTTP: `claude mcp add --transport http fusion http://127.0.0.1:27182/mcp`.

Start Fusion before the agent; if the agent started first, restart it.

Help: https://help.autodesk.com/cloudhelp/ENU/ADSKMCP-FusionDesktopMcp/files/ADSKMCP_FusionDesktopMcp_connecting_to_the_fusion_mcp_server_html.html

## SketchUp (official, by Trimble)

Works in Claude on the web, desktop and mobile; needs a Trimble ID. Free SketchUp entitlements save up to 30 models.

1. Claude: **Customize > Connectors**, search "SketchUp", **Add**, then **Connect** and sign in with the Trimble ID. On a Team or Enterprise plan an Owner enables it first.
2. Describe the model, with sizes. Ask for metric: it works in inches unless told.
3. Download each `.skp` before the chat ends; models are not kept between sessions.

Version 1 builds new files only; it does not edit the user's existing models.

Help: https://help.sketchup.com/en/sketchup-claude-connector

## ArchiCAD (official, by Graphisoft, beta)

Needs ArchiCAD 30 on a subscription that includes the Public MCP Connection (such as Collaborate or Max), and a desktop agent.

1. ArchiCAD: **Options > Desktop AI Tool Connection**. Copy the command and argument it shows.
2. Claude Desktop: **Settings > Developer > Edit Config**, and add under `mcpServers`:
   ```json
   "Archicad Public MCP Server": { "command": "<command from ArchiCAD>", "args": ["<argument from ArchiCAD>"] }
   ```
   Claude Code: `claude mcp add archicad -- "<command>" "<argument>"`.
3. Quit Claude Desktop fully (File > Exit) and reopen. Test: "tell me the running Archicad instances".

Help: https://help.graphisoft.com/AC/30/INT/Topics/001_GettingHelp/AI_Assistant/public_mcp_connection.html

## Revit (official, by Autodesk, read-only)

Revit 2027 only. Download "Revit 2027 MCP Server Read-Tools Technical Preview" from **Products & Services > Extensions** in the Autodesk Account. It configures Claude Desktop itself. It reads model data, views and element properties, and exports views; it does not change the model.

Help: https://blog.autodesk.io/revit-2027-mcp-server-release/

## AutoCAD (no official connector)

There is no AutoCAD connector in Claude's directory. AutoCAD 2027's built-in MCP server serves only Autodesk Assistant. Three routes, safest first:

1. **DXF files** (any OS, no AutoCAD needed): the agent writes and measures DXF with `drawing-building-plans`; the user opens it in AutoCAD.
2. **AutoLISP**: the agent writes a `.lsp` command; the user loads it with `APPLOAD` and runs it. The user sees the code before it runs.
3. **Community MCP servers** (Windows only, they drive AutoCAD through COM), for example `puran-water/autocad-mcp`. Review the repository before installing; most are maintained by one person.
