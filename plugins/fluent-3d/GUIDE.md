# Using Fluent 3D

Describe what you want in plain words; the right skill starts on its own. To call one by name, type `/` in Claude Code or `$` in Codex and pick it from the list.

| Skill | Starts when you ask to |
|---|---|
| `setting-up-3d-apps` | set up a computer, install or check 3D apps, connect the agent to FreeCAD |
| `designing-3d-models` | design or change a part, turn a logo into a 3D object, fix a mesh, render a model |
| `printing-3d-models` | slice a model, print in several colours, pause for an insert, fix a failed first layer |

Not installed yet? See [INSTALL.md](INSTALL.md).

## Your first project

**1. Set up the computer.** Say:

> Set up this computer for 3D printing. My printer is a Bambu Lab A1 with an AMS lite.

The agent lists what is installed and what is missing, suggests the apps that suit your printer, and installs them once you say yes. If you want to watch it model, it also connects to FreeCAD. You type any printer access code or account password yourself.

**2. Design the part.** Say:

> Design a keychain with my initials, 50 mm wide, black with white letters, for my A1. Build it in FreeCAD so I can watch.

The agent asks what it still needs, builds the model in FreeCAD while you watch, and shows you screenshots. Every size lives in a `Params` sheet you can edit. Once you approve, it checks the geometry and exports the print files.

**3. Print it.** Say:

> Get this ready to print.

The agent builds the slicer project, slices it, shows you the preview with any pauses marked, and writes a print-day checklist. You start the print and send a photo of the first layer; if it looks wrong, the agent tells you what to fix.

## More things to ask

| Goal | Say |
|---|---|
| Check an existing setup | "Check my 3D printing setup and tell me what's missing." |
| Logo on a part | "Turn this SVG logo into a 4 mm coaster, logo raised 1 mm in white." |
| Tap-to-open object | "Design a keychain with an NFC tag inside that opens my website." |
| Magnets or nuts | "Add pockets for two 10 x 3 mm magnets and pause the print so I can drop them in." |
| Existing file | "Check this STL for problems before I print it." |
| Change a design | "Make the keychain 10% bigger and the walls 2 mm thick." |
| Multi-colour without an AMS | "Set this up to print in three colours on one spool with filament swaps." |
| Picture for sharing | "Render the model for a product photo." |
| Printing went wrong | "The first layer isn't sticking. Here's a photo." |

## Where your files go

Unless you name a folder, everything goes in `3D Printing/` in your home folder:

| Folder | Holds |
|---|---|
| `models/<project>/` | the editable model, print files (STL, STEP), images, and a README |
| `slices/<date>-<project>/` | slicer projects, ready to open |
| `print-log/<date>-<project>.md` | settings, the print-day checklist, results and photos |

## You stay in charge

- The agent asks before installing anything.
- You approve each design on screen before it is exported.
- You start every print. The agent touches the printer only when you ask, and names the printer, the action and the file first.
- Passwords and printer access codes stay with you.

## When something goes wrong

| Problem | Fix |
|---|---|
| The skills don't appear | Start a new session. Check `claude plugin list` or `codex plugin list` shows `fluent-3d` enabled. |
| "FreeCAD bridge not running" | In FreeCAD, switch to the **MCP Addon** workbench and click **Start RPC Server**. |
| The agent can't install apps or reach the internet | Your agent's sandbox is blocking it. Approve the command when asked, or run the install command yourself. |
| "Bambu Studio not found" | Open Bambu Studio once. If it's installed somewhere unusual, tell the agent where. |
| The print didn't pause | The printer profile's pause G-code is empty. Ask the agent to check it and re-slice. |
| Anything else | Open an issue at [fluent-ke/fluent-plugins](https://github.com/fluent-ke/fluent-plugins/issues) with what you asked, what happened, and the output of `check_setup.py`. |
