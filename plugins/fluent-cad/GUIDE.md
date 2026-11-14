# Using Fluent CAD

Describe what you want in plain words; the right skill starts on its own. To call one by name, type `/` in Claude Code or `$` in Codex and pick it from the list. Not installed yet? See [INSTALL.md](INSTALL.md).

## First, for everyone

> Set up this computer for my work. I'm a *what you do*, and I use *your apps*.

The agent lists what is installed and missing, suggests the apps that fit, installs free ones once you say yes, and connects itself to the apps it can drive. Paid apps (AutoCAD, ArchiCAD, Revit, Fusion) you install and sign in to yourself.

## Track 1: architecture and building

> Draw a site office for a construction site: about 10 by 6 m outside, two offices, a meeting room, a small store and a toilet. 200 mm block outside, 150 mm inside, main door facing the road on the south, a window in every room except the store, walls 2.7 m high. Give me the DXF, a PNG and the block count in Excel.

You get a layered drawing that opens in AutoCAD, a picture of it, and a workbook whose quantities are formulas. The agent measures the drawing separately and shows that the two agree. Allow 10 to 20 minutes.

| Goal | Say |
|---|---|
| Quantities from your drawing | "Here's our DWG saved as DXF. Take off the wall lengths and count the doors and windows by layer." |
| A revision | "Make office 2 one metre longer and give me Rev B with what changed in the quantities." |
| A 3D view of a plan | "Raise this plan into a 3D model and give me a turntable." |
| A concept in SketchUp | "Make a SketchUp massing of the same plan." (SketchUp connector) |

## Track 2: engineering and product design

> Design a wall bracket for a 5 kg shelf, 3 mm screws, in FreeCAD so I can watch. Put every size in a table I can change.

The agent builds it live in FreeCAD, shows screenshots, and keeps every dimension in a `Params` sheet. With the Fusion connector, say "in Fusion" instead.

| Goal | Say |
|---|---|
| Change a design | "Make the bracket 20% deeper and the walls 4 mm." |
| A part from a sketch | "Here's a photo of my sketch with sizes. Model it." |
| STEP for a workshop | "Export STEP and STL." |

## Track 3: 3D printing

> Design a keychain with my initials, 50 mm wide, black with white letters, for my Bambu A1. Then get it ready to print.

The agent models it, checks the geometry, builds the slicer project, shows the sliced preview with any pauses marked, and writes a print-day checklist. You start the print and send a photo of the first layer.

| Goal | Say |
|---|---|
| Tap-to-open object | "A keychain with an NFC tag inside that opens my website." |
| Magnets | "Pockets for two 10 x 3 mm magnets, pause so I can drop them in." |
| Check a file | "Check this STL before I print it." |
| Failed first layer | "The first layer isn't sticking. Here's a photo." |

## Track 4: 3D animation and visualisation

> Make an 8-second turntable of this model for Instagram, vertical.

> Walk me through this building from the front door into the meeting room, then cut it with the plan and a turntable, with this music.

The agent checks single frames before rendering, renders the video, and hands back the MP4 and the `.blend` so you can keep editing in Blender. With the Blender connector in Claude Desktop, it can also work live on your own scene: "light this scene for a product shot", "rename every object by its material".

## Where your files go

Unless you name a folder: `Drawings/<project>/` for building work, `3D Printing/` for models, slices and print logs, `Blender/<project>/` for animation, all in your home folder.

## You stay in charge

- The agent asks before installing anything, and before bulk changes inside an app.
- Drawings are marked "To be checked by the engineer"; you approve designs on screen before export.
- You start every print. Passwords, licences and access codes stay with you.

## When something goes wrong

| Problem | Fix |
|---|---|
| The skills don't appear | Start a new session. Check `claude plugin list` or `codex plugin list` shows `fluent-cad` enabled. |
| The same skill appears twice | Fluent 3D is still installed: `claude plugin uninstall fluent-3d@fluent`. |
| A connector shows no tools | Open the app first, start its server (Blender: Preferences > Add-ons > BlenderMCP; Fusion: Preferences > General > API), then restart the agent. |
| "uv not found" for the drawing scripts | Ask the agent to install uv, or see `setting-up-cad-apps`. |
| A drawing opens tiny or huge in AutoCAD | Units: the drawing is in millimetres. Set your template to millimetres. |
| Anything else | Open an issue at [fluent-ke/fluent-plugins](https://github.com/fluent-ke/fluent-plugins/issues) with what you asked, what happened, and the output of `check_setup.py`. |
