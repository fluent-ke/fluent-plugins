# Connect an agent to FreeCAD

The [FreeCAD MCP](https://github.com/neka-nat/freecad-mcp) (MIT) has two halves: an add-on inside FreeCAD that serves a localhost RPC bridge, and an MCP server the agent launches with `uvx`. These skills were tested with add-on commit `5dbfe2c` and package `0.1.23`.

The bridge runs any Python the agent sends inside FreeCAD, with the user's file permissions. It listens on localhost only; keep the add-on's **Remote Connections** option off.

## 1. Install uv and FreeCAD

Check with `check_setup.py`; install what is missing (see the install table in this skill's `SKILL.md`).

## 2. Install the add-on

```bash
git clone https://github.com/neka-nat/freecad-mcp.git
```

Find FreeCAD's user folder rather than guessing it; it differs by OS, version and install type:

| OS | Command |
|---|---|
| macOS | `/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd -c "import FreeCAD; print(FreeCAD.getUserAppDataDir())"` |
| Windows | `& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "import FreeCAD; print(FreeCAD.getUserAppDataDir())"` |
| Linux | `freecadcmd -c "import FreeCAD; print(FreeCAD.getUserAppDataDir())"` |

Or, inside FreeCAD, open View > Panels > Python console and run `App.getUserAppDataDir()`.

Copy `freecad-mcp/addon/FreeCADMCP` into `<that folder>/Mod/`, so the result is `Mod/FreeCADMCP`. Restart FreeCAD.

## 3. Register the MCP server with the agent

| Agent | Command |
|---|---|
| Claude Code | `claude mcp add freecad -s user -- uvx freecad-mcp` |
| Codex | `codex mcp add freecad -- uvx freecad-mcp` |
| Anything else | add `{"mcpServers": {"freecad": {"command": "uvx", "args": ["freecad-mcp"]}}}` to its MCP config |

Pin the tested release with `freecad-mcp@0.1.23`. Restart the agent so the `freecad` tools load.

## 4. Start the bridge and check it

In FreeCAD, pick the **MCP Addon** workbench and click **Start RPC Server**. To have it start with FreeCAD from now on, tick **Auto-Start Server** in the FreeCAD MCP menu; to start it only for one session, launch FreeCAD with the `designing-3d-models` skill's `scripts/start_freecad_bridge.py` (commands in its `references/freecad-live.md`).

Done when `scripts/check_setup.py` reports the bridge as running.
