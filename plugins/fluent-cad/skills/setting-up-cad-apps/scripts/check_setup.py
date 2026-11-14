#!/usr/bin/env python3
"""Report which CAD, 3D and printing tools this computer has. Read-only: it installs and launches nothing.

  python3 check_setup.py        (Windows: py check_setup.py)
"""
import glob
import os
import platform
import shutil
import socket
import subprocess

SYSTEM = platform.system()  # Darwin, Windows or Linux
HOME = os.path.expanduser("~")
PROGRAM_DIRS = [os.environ.get(v) for v in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")]

# name, job, commands on PATH, macOS .app name pattern, Windows exe pattern under Program Files, Flatpak ID
TOOLS = [
    ("AutoCAD", "2D drawings (DWG)", ["acad"], "Autodesk/AutoCAD*/AutoCAD*.app", "Autodesk/AutoCAD*/acad.exe", None),
    ("ArchiCAD", "BIM", [], "Graphisoft/Archicad*/Archicad*.app", "Graphisoft/Archicad*/Archicad.exe", None),
    ("Revit", "BIM (Windows)", [], None, "Autodesk/Revit*/Revit.exe", None),
    ("SketchUp", "concept 3D", [], "SketchUp*/SketchUp.app", "SketchUp/SketchUp*/SketchUp.exe", None),
    ("Fusion", "parametric CAD", [], "Autodesk Fusion*.app", None, None),
    ("FreeCAD", "parametric CAD", ["freecad", "FreeCAD"], "FreeCAD*.app", "FreeCAD*/bin/freecad.exe", "org.freecad.FreeCAD"),
    ("OpenSCAD", "code CAD", ["openscad"], "OpenSCAD*.app", "OpenSCAD*/openscad.exe", "org.openscad.OpenSCAD"),
    ("Blender", "mesh, sculpt, render", ["blender"], "Blender*.app", "Blender Foundation/Blender*/blender.exe", "org.blender.Blender"),
    ("Bambu Studio", "slicer: Bambu Lab", ["bambu-studio"], "BambuStudio*.app", "Bambu Studio/bambu-studio.exe", "com.bambulab.BambuStudio"),
    ("PrusaSlicer", "slicer: Prusa", ["prusa-slicer"], "PrusaSlicer*.app", "Prusa3D/PrusaSlicer/prusa-slicer.exe", "com.prusa3d.PrusaSlicer"),
    ("OrcaSlicer", "slicer: most brands", ["orca-slicer"], "OrcaSlicer*.app", "OrcaSlicer/orca-slicer.exe", "io.github.softfever.OrcaSlicer"),
    ("UltiMaker Cura", "slicer", ["cura", "UltiMaker-Cura"], "UltiMaker Cura*.app", "UltiMaker Cura*/UltiMaker-Cura.exe", "com.ultimaker.cura"),
    ("admesh", "STL check (optional)", ["admesh"], None, None, None),
    ("assimp", "mesh conversion (optional)", ["assimp"], None, None, None),
    ("uv", "runs MCPs and DXF scripts", ["uv"], None, None, None),
    ("ffmpeg", "frames to video", ["ffmpeg"], None, None, None),
]

FREECAD_USER_DIRS = {
    "Darwin": [f"{HOME}/Library/Application Support/FreeCAD"],
    "Windows": [os.path.join(os.environ.get("APPDATA", ""), "FreeCAD")],
}.get(SYSTEM, [f"{HOME}/.local/share/FreeCAD", f"{HOME}/.FreeCAD", f"{HOME}/snap/freecad/common",
               f"{HOME}/.var/app/org.freecad.FreeCAD/data/FreeCAD"])


def find(commands, mac_app, windows_exe, flatpak_id):
    for command in commands:
        if shutil.which(command):
            return shutil.which(command)
    if SYSTEM == "Darwin" and mac_app:
        hits = glob.glob(f"/Applications/{mac_app}") + glob.glob(f"{HOME}/Applications/{mac_app}")
    elif SYSTEM == "Windows" and windows_exe:
        hits = [h for d in PROGRAM_DIRS if d for h in glob.glob(os.path.join(d, windows_exe))]
    elif flatpak_id and shutil.which("flatpak"):
        installed = subprocess.run(["flatpak", "info", flatpak_id], capture_output=True).returncode == 0
        hits = [f"flatpak {flatpak_id}"] if installed else []
    else:
        hits = []
    return sorted(hits)[-1] if hits else None


def bridge_running(port):
    try:
        socket.create_connection(("127.0.0.1", port), timeout=0.5).close()
        return True
    except OSError:
        return False


print(f"{platform.system()} {platform.release()} ({platform.machine()}), Python {platform.python_version()}")
missing = []
for name, job, commands, mac_app, windows_exe, flatpak_id in TOOLS:
    path = find(commands, mac_app, windows_exe, flatpak_id)
    print(f"  {'ok' if path else 'missing':8} {name:15} {job:27} {path or ''}")
    if not path:
        missing.append(name)

addons = [h for d in FREECAD_USER_DIRS for h in glob.glob(os.path.join(glob.escape(d), "**", "Mod", "FreeCADMCP"), recursive=True)]
print(f"  {'ok' if addons else 'missing':8} {'FreeCAD MCP':15} {'add-on inside FreeCAD':27} {addons[0] if addons else ''}")
for name, port in (("FreeCAD bridge", 9875), ("Blender MCP", 9876), ("Fusion MCP", 27182)):
    print(f"  {'running' if bridge_running(port) else 'stopped':8} {name:15} {f'127.0.0.1:{port}':27}")
print("Missing: " + (", ".join(missing) if missing else "nothing") +
      ". Install only what the user's job needs: one slicer (the printer's brand), and paid apps only if they use them.")
if SYSTEM == "Linux":
    print("AppImages are not detected; ask the user whether one is in use.")
