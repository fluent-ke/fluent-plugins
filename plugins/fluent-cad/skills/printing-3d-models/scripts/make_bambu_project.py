#!/usr/bin/env python3
"""Build a ready-to-open Bambu Studio 3MF project from multi-colour STL parts.

  make_bambu_project.py OUT.3mf PART.stl:#RRGGBB [PART.stl:#RRGGBB ...] --pause Z [--pause Z ...]
                        [--single-spool] [--printer NAME] [--process NAME] [--filament NAME]
                        [--bambu PATH] [--profiles DIR]

- All parts merge into ONE object and keep the positions they were exported with.
- Each part gets its own filament slot and colour (AMS). --single-spool puts every part on
  filament 1 for printers without an AMS: add a --pause at each colour's first layer and swap by hand.
- --pause Z stops the printer BEFORE the layer whose top is Z (Bambu Studio labels layers by top height).
- Finds Bambu Studio and its BBL system profiles on macOS, Windows and Linux; --bambu and --profiles override.
- Only writes the 3MF. It never slices, uploads or talks to a printer.
"""
import argparse
import glob
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile

SYSTEM = platform.system()
HOME = os.path.expanduser("~")
BAMBU_CANDIDATES = {
    "Darwin": ["/Applications/BambuStudio.app/Contents/MacOS/BambuStudio",
               f"{HOME}/Applications/BambuStudio.app/Contents/MacOS/BambuStudio"],
    "Windows": [os.path.join(os.environ.get("ProgramFiles", r"C:\Program Files"), "Bambu Studio", "bambu-studio.exe")],
}.get(SYSTEM, [])
USER_DATA = {
    "Darwin": f"{HOME}/Library/Application Support/BambuStudio",
    "Windows": os.path.join(os.environ.get("APPDATA", ""), "BambuStudio"),
}.get(SYSTEM, f"{HOME}/.config/BambuStudio")


def find_bambu():
    found = [p for p in BAMBU_CANDIDATES if os.path.exists(p)] + [shutil.which(n) for n in ("bambu-studio", "BambuStudio")]
    return next((p for p in found if p), None)


def find_profiles(bambu):
    # The user-data copy is refreshed by the app's profile updates; the bundled copy ships with the install.
    app_dir = os.path.dirname(os.path.realpath(bambu))
    for folder in (os.path.join(USER_DATA, "system", "BBL"),
                   os.path.join(app_dir, "..", "Resources", "profiles", "BBL"),  # macOS app bundle
                   os.path.join(app_dir, "resources", "profiles", "BBL")):  # Windows and Linux installs
        if os.path.isdir(os.path.join(folder, "machine")):
            return os.path.normpath(folder)
    return None


ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("parts", nargs="+", help="path.stl:#RRGGBB, bottom part first")
ap.add_argument("--pause", type=float, action="append", default=[])
ap.add_argument("--single-spool", action="store_true")
ap.add_argument("--printer", default="Bambu Lab A1 0.4 nozzle")
ap.add_argument("--process", default="0.20mm Standard @BBL A1")
ap.add_argument("--filament", default="Bambu PLA Matte @BBL A1")
ap.add_argument("--bambu", help="Bambu Studio executable")
ap.add_argument("--profiles", help="folder holding the BBL machine/, process/ and filament/ presets")
args = ap.parse_args()

BAMBU = args.bambu or find_bambu()
if not BAMBU or not os.path.isfile(BAMBU):
    sys.exit(f"Bambu Studio not found{f' at {BAMBU}' if BAMBU else ''}; pass --bambu with the path to its executable.")
PROFILES = args.profiles or find_profiles(BAMBU)
if not PROFILES:
    sys.exit("Bambu Studio's BBL profiles not found; open Bambu Studio once, or pass --profiles.")

out = os.path.abspath(args.out)
parts = [p.rsplit(":", 1) for p in args.parts]
slots = 1 if args.single_spool else len(parts)
work = tempfile.mkdtemp()

# assemble_index > 0 is what merges the files into one object (0 keeps them separate).
# pos_* is ADDED to the STL's own coordinates, so 0 keeps the exported stack-up.
objects = [{"path": os.path.abspath(stl), "count": 1, "filaments": [min(i + 1, slots)],
            "assemble_index": [1], "pos_x": [0], "pos_y": [0], "pos_z": [0]}
           for i, (stl, _) in enumerate(parts)]
with open(os.path.join(work, "assemble.json"), "w") as f:
    json.dump({"plates": [{"plate_name": os.path.splitext(os.path.basename(out))[0],
                           "need_arrange": True, "objects": objects}]}, f)

def load_preset(kind, name):
    paths = glob.glob(os.path.join(glob.escape(PROFILES), kind, "**", glob.escape(name) + ".json"), recursive=True)
    if not paths:
        sys.exit(f"No {kind} preset named {name!r} under {PROFILES}")
    with open(paths[0]) as f:
        return json.load(f)


def flattened(kind, name):
    """System presets only hold overrides on top of an `inherits` chain, and the CLI does not
    resolve it: passing the preset file directly yields a 200x200 bed, a stub start G-code and an
    empty pause G-code. Printers such as the A1 also keep their start/end/filament-change G-code in
    separate "template" files listed under `include`. Merge both, root-first, into one file."""
    chain = []
    while name:
        chain.append(load_preset(kind, name))
        name = chain[-1].get("inherits")
    merged = {}
    for layer in reversed(chain):
        for include in layer.get("include", []):
            merged.update(load_preset(kind, include))
        merged.update(layer)
    merged.pop("inherits", None)
    merged.pop("include", None)
    path = os.path.join(work, f"{kind}.json")
    with open(path, "w") as f:
        json.dump(merged, f)
    return path


filament = flattened("filament", args.filament)
cmd = [BAMBU, "--load-settings", f"{flattened('machine', args.printer)};{flattened('process', args.process)}",
       "--load-filaments", ";".join([filament] * slots),
       "--load-assemble-list", os.path.join(work, "assemble.json"),
       "--outputdir", work, "--export-3mf", "project.3mf"]  # --outputdir must be absolute
run = subprocess.run(cmd, capture_output=True, text=True, cwd=work)
project = os.path.join(work, "project.3mf")
if not os.path.exists(project):
    sys.exit("Bambu Studio export failed:\n" + run.stdout[-3000:] + run.stderr[-3000:])

with zipfile.ZipFile(project) as z:
    entries = {name: z.read(name) for name in z.namelist()}

settings = json.loads(entries["Metadata/project_settings.config"])
settings["filament_colour"] = [colour for _, colour in parts][:slots]
entries["Metadata/project_settings.config"] = json.dumps(settings, indent=4).encode()

pause_gcode = settings.get("machine_pause_gcode")
if args.pause and not pause_gcode:
    sys.exit("Project has no machine_pause_gcode: the printer profile did not resolve, pauses would be ignored.")

if args.pause:
    # Format from BambuStudio src/libslic3r/Format/bbs_3mf.cpp; type 1 = PausePrint.
    layers = "".join(f'<layer top_z="{z:g}" type="1" extruder="1" color="" extra="" gcode="{pause_gcode}"/>\n'
                     for z in sorted(args.pause))
    mode = "SingleExtruder" if slots == 1 else "MultiExtruder"
    entries["Metadata/custom_gcode_per_layer.xml"] = (
        '<?xml version="1.0" encoding="utf-8"?>\n<custom_gcodes_per_layer>\n<plate>\n<plate_info id="1"/>\n'
        f'{layers}<mode value="{mode}"/>\n</plate>\n</custom_gcodes_per_layer>\n').encode()

os.makedirs(os.path.dirname(out), exist_ok=True)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for name, data in entries.items():
        z.writestr(name, data)
print(f"wrote {out}: {len(parts)} parts in one object, {slots} filament slot(s), pauses at {sorted(args.pause)} mm; "
      f"printer {settings['printer_settings_id']}, bed {settings['printable_area'][2]}, pause G-code {pause_gcode!r}")
