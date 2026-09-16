#!/usr/bin/env python3
"""Turn a text file into an audio file with the computer's own speech engine.

macOS and Windows. Python 3 standard library only. No cloud service: the text
never leaves the computer at this step.

    python3 say_it.py --text-file briefing.txt --name "2026-09-18 - supplier contract - briefing" --out-dir "contracts/acme"

On macOS the result is an .m4a (small, plays on a phone). On Windows it is a .wav.
"""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path


def say_macos(text_file: Path, out_path: Path, voice: str | None) -> None:
    # No -v by default: the System Voice (Settings > Accessibility > Spoken Content)
    # is the best voice available, and Siri voices are reachable only that way.
    aiff = out_path.with_suffix(".aiff")
    cmd = ["say", "-f", str(text_file), "-o", str(aiff)]
    if voice:
        cmd[1:1] = ["-v", voice]
    subprocess.run(cmd, check=True)
    if aiff.is_file() and aiff.stat().st_size > 4096:
        converted = subprocess.run(
            ["afconvert", "-f", "m4af", "-d", "aac", str(aiff), str(out_path)],
            check=False,
        )
        if converted.returncode == 0 and out_path.is_file():
            aiff.unlink()
        else:
            aiff.rename(out_path.with_suffix(".aiff"))


def say_windows(text_file: Path, out_path: Path, voice: str | None) -> None:
    select = f'$s.SelectVoice("{voice}");' if voice else ""
    script = (
        "Add-Type -AssemblyName System.Speech;"
        "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
        f"{select}"
        f'$s.SetOutputToWaveFile("{out_path}");'
        f'$s.Speak([IO.File]::ReadAllText("{text_file}"));'
        "$s.Dispose();"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
        check=True,
    )


def open_default(path: Path) -> None:
    if platform.system() == "Darwin":
        subprocess.run(["open", str(path)], check=False)
    elif platform.system() == "Windows":
        os.startfile(str(path))  # type: ignore[attr-defined]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text-file", required=True, help="File holding the spoken text")
    parser.add_argument("--name", required=True, help="Output filename, no extension")
    parser.add_argument("--out-dir", default=".", help="Folder to save the audio in (default: current folder)")
    parser.add_argument("--voice", default=None, help="Use a named installed voice")
    parser.add_argument("--no-open", action="store_true", help="Save without playing")
    args = parser.parse_args()

    system = platform.system()
    if system not in ("Darwin", "Windows"):
        print(
            f"No speech engine on {system}. Audio briefings need an agent running on a Mac "
            "or Windows computer, not a browser chat or a cloud sandbox.",
            file=sys.stderr,
        )
        return 1

    text_file = Path(args.text_file).expanduser().resolve()
    if not text_file.is_file():
        print(f"No such text file: {text_file}", file=sys.stderr)
        return 1

    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = ".m4a" if system == "Darwin" else ".wav"
    out_path = out_dir / f"{args.name}{ext}"

    if system == "Darwin":
        say_macos(text_file, out_path, args.voice)
        if not out_path.is_file():
            out_path = out_path.with_suffix(".aiff")
    else:
        say_windows(text_file, out_path, args.voice)

    if not out_path.is_file() or out_path.stat().st_size <= 4096:
        print("The speech engine ran but produced no usable audio.", file=sys.stderr)
        return 1

    size_mb = out_path.stat().st_size / (1024 * 1024)
    words = len(text_file.read_text(encoding="utf-8", errors="replace").split())
    print(f"{out_path}  ({size_mb:.1f} MB, about {words / 180:.1f} min from {words} words)")

    if not args.no_open:
        open_default(out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
