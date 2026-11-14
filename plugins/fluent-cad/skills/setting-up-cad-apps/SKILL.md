---
name: setting-up-cad-apps
description: Use when someone wants to start designing on their computer with AI help, or installing, checking or connecting design software for CAD, architecture, engineering, 3D printing or 3D animation - AutoCAD, ArchiCAD, Revit, SketchUp, Fusion, FreeCAD, OpenSCAD, Blender, Bambu Studio, OrcaSlicer, PrusaSlicer or Cura - or connecting Claude or another agent to one of them through a connector or MCP server.
license: MIT
metadata:
  author: fluent
  version: "0.2"
---

# Setting up CAD apps

## What this is for

Someone wants AI to help with the design work they already do: drawings, parts, prints or animation. The first hour usually goes on installing the wrong thing, or on an app that has never heard of the agent.

**Start from their job and the apps they already use. Connect the agent to those; never move them to something new.** An architect who drafts in AutoCAD keeps AutoCAD. The agent learns to hand them files it opens, or drives the app through its connector.

The person is usually not technical. They may never have opened a terminal. Ask before installing anything, give literal steps for the screen in front of them, and do not teach the machinery.

`K` below is this skill's folder. Run its scripts with `python3` (Windows: `py`).

**First, check where you are running.** Claude on the web, the chat in Claude Desktop, and Cowork run in a sandbox, not on their computer: go to *In a browser*. Claude Code (the terminal, or the Code tab in Claude Desktop) and Codex run on their computer: carry on.

## The shape

1. Find out what they make
2. Survey the computer
3. Pick the stack
4. Install
5. Connect the agent
6. Prove it
7. Hand over to the job

## 1. Find out what they make

Ask **one question at a time**, in plain words, and wait for each answer:

1. What do you design? (buildings, parts and products, things to 3D print, animations or renders)
2. Which design apps do you use now, and which do you pay for?
3. For printing only: which printer, and does it have a multi-colour unit (AMS, MMU)?

Their answer picks the skill they will use after setup:

| They mainly | Track | Skill after setup |
|---|---|---|
| draw buildings: plans, sections, quantities | Architecture and building | `drawing-building-plans` |
| design parts and products | Engineering and product design | `designing-3d-models` |
| 3D print | 3D printing and making | `designing-3d-models`, then `printing-3d-models` |
| animate, render or edit video | 3D animation and visualisation | `animating-in-blender` |

Many people sit in two tracks. Set up both.

## 2. Survey the computer

Run `python3 $K/scripts/check_setup.py`. It is read-only: it prints the operating system, each app it found and where, what is missing, and which agent connections are listening. Tell the person in one or two sentences what they have and what their track still needs. Done when you can name their OS, their apps and every missing tool.

## 3. Pick the stack

One app per job, starting from what they already have:

| Job | App | How the agent works with it | Pick it when |
|---|---|---|---|
| **2D drawings, plans** | AutoCAD, or any DWG/DXF app (BricsCAD, ZWCAD, DraftSight, LibreCAD) | no official connector: the agent writes DXF files they open (`drawing-building-plans`) | the default for building drawings |
| **BIM** | ArchiCAD | Graphisoft's Public MCP Server (beta, ArchiCAD 30, some subscriptions) | their office models in ArchiCAD |
| | Revit | Autodesk's Revit 2027 MCP Server: read-only preview | their office models in Revit |
| **Concept massing, interiors** | SketchUp | official Claude connector by Trimble: builds new `.skp` files | quick 3D from a description or sketch |
| **Parametric parts** | FreeCAD | FreeCAD MCP (community, MIT): live modelling | default: free, scriptable, the agent builds on screen |
| | Fusion | official Claude connector by Autodesk, needs a Fusion subscription | they already design in Fusion |
| | OpenSCAD | none needed: parts are code | parts described entirely in numbers |
| | Onshape, SolidWorks, Inventor, Tinkercad | none | they export STEP (to edit) or STL (to print) |
| **3D animation, rendering, video edit** | Blender | official Claude connector by Blender: live; or headless scripts | default: free, and the agent can script every frame |
| **Slicer** | Bambu Studio | none needed: the agent writes projects | Bambu Lab printers |
| | PrusaSlicer | | Prusa printers |
| | OrcaSlicer | | Creality, Elegoo, Anycubic, Voron and other Marlin or Klipper printers |
| | UltiMaker Cura | | UltiMaker printers, or they know Cura |
| **Helpers** | Python 3 | runs this plugin's scripts | always |
| | `uv` | runs the drawing scripts and the FreeCAD connection, fetching what they need | drawing and FreeCAD |
| | `ffmpeg` | turns rendered frames into video | animation |
| | admesh, assimp | optional STL checks and format conversion | printing |

One slicer only: the one that matches the printer brand. Play the list back in one line ("FreeCAD, Bambu Studio and uv; you already have Blender") and wait for a yes.

## 4. Install

Search first, then show the exact command and run it after they say yes. Package names drift, so use the ID the search returns.

| OS | Search | Install |
|---|---|---|
| macOS (Homebrew) | `brew search <name>` | apps: `brew install --cask <id>`; tools: `brew install python uv ffmpeg admesh assimp` |
| Windows (winget) | `winget search <name>` | `winget install --id <id> -e`; Python: `winget install --id Python.Python.3.12 -e`; ffmpeg: `winget install --id Gyan.FFmpeg -e` |
| Linux (Flatpak) | `flatpak search <name>` | apps: `flatpak install flathub <id>`; tools: the distro's packages (Debian/Ubuntu: `sudo apt install ffmpeg admesh assimp-utils`) and `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

- When Homebrew, winget or Flatpak is missing, send them to the app's official download page instead of installing a package manager unasked. Python: python.org/downloads (on Windows, tick "Add python.exe to PATH"). `uv` has its own installer on every system: macOS and Linux `curl -LsSf https://astral.sh/uv/install.sh | sh`; Windows PowerShell `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`.
- On a new Mac, the first `python3` may open a box offering Apple's command line tools. Tell them to click Install and wait; it is safe and needed once.
- Paid apps (AutoCAD, ArchiCAD, Revit, Fusion, SketchUp Pro) they install from their own account and sign in to themselves.
- A sandbox may block downloads or writing outside the project. Say so, and either ask them to approve the command or give it to them to run.

Done when `check_setup.py` reports every chosen tool.

## 5. Connect the agent

To the apps it can drive: [connectors.md](references/connectors.md) for Blender, Fusion, SketchUp, ArchiCAD, Revit and AutoCAD; [freecad-mcp.md](references/freecad-mcp.md) for FreeCAD. Give the steps one screen at a time, and wait for them to say each is done.

A connector that drives an app on their computer needs the app and the agent on **the same machine**: Claude Desktop, Claude Code or Codex.

Some connections need the agent restarted before their tools appear. Before asking for a restart, tell them what to say afterwards: "carry on setting up CAD apps". On a Mac, taking screenshots of their apps needs the screen-recording permission: System Settings, Privacy & Security, Screen Recording, switch on the app the agent runs in, and reopen it.

## 6. Prove it

For each connected app, make one **read-only** request first: "list the objects in the open file". Then one small new thing in a **new file**: a 10 mm cube. Show them the result in the app. If a connection answers nothing, the app is usually not open, or its server is not started: the fixes are in the references.

Then make the workspace. Ask where their work should live, and suggest a folder in their home folder: `Drawings/` for building work; `3D Printing/` with `models/`, `slices/` and `print-log/` for printing; `Blender/` for animation.

## 7. Hand over to the job

**Smoke test, theirs:** they open the app themselves and see the test object the agent made. Then tell them, in one or two lines, what is now set up and what to say next for their track:

| Track | Say |
|---|---|
| Architecture | "Draw a site office, 10 by 6 m, two offices, a meeting room, a store and a toilet, with the block count." |
| Engineering | "Design a wall bracket for a 5 kg shelf in FreeCAD so I can watch." |
| Printing | "Design a keychain with my initials and get it ready for my printer." |
| Animation | "Make an 8-second turntable of this model." |

## In a browser

On claude.ai, the chat in Claude Desktop or Cowork there is no access to the person's computer. Only the SketchUp connector works there, because it runs in Trimble's cloud. Everything else is advice and scripts they run themselves.

Tell them once what the desktop adds: Claude Desktop's connectors drive Blender, Fusion and ArchiCAD from its chat, and its **Code** tab works on their computer itself, installing apps, running the scripts and checking results, with no terminal to learn. The literal steps: install Claude Desktop from claude.ai/download, sign in, click **Code** at the top, choose a folder for their work, and type there. One sentence on the gain, then leave the choice with them.

## Safety

- Every live connector runs code the agent writes inside the app, with the person's permissions. Work in a new file or a copy until they trust it, and ask before bulk deletes.
- Connections listen on their own computer only. Leave remote-connection options off.
- Licences, Autodesk, Trimble and Graphisoft passwords and printer access codes stay with them: they sign in themselves.

## Common mistakes

| What happens | What it actually is |
|---|---|
| Installs FreeCAD for an architect who uses AutoCAD | Moving them off their app. Write files AutoCAD opens instead |
| Installs every slicer "to be safe" | Three apps fighting over the same files. One, matching the printer |
| Five questions in one message | Homework. One at a time, with options when they are unsure |
| "Open a terminal and run…" to someone who has never seen one | The step where they stop. Run it for them, or give the literal clicks |
| Says a connector works without a test call | An assertion. Prove it with a read and a small new object |
| Asks for their Autodesk password to sign in for them | Not yours to hold. They sign in |

## Red flags — stop

- You are about to install something they did not agree to
- You are about to type a password, licence key or printer access code
- A connector is about to change their real project file, not a copy, before they have seen a test
- You are telling them setup is done without having run `check_setup.py` and a test call

---

Stuck, or want to send feedback on this skill? Read the `about-fluent` skill if Fluent AI Skills is installed, or visit fluent.ke.
