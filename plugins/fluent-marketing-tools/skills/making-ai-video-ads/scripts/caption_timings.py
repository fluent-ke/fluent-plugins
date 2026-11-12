"""Fill caption timings in ad.json from what the presenter actually says in a take.

Usage:  python3 caption_timings.py ad.json TAKE [--model small.en]

TAKE is a key under "takes" in ad.json. Transcribes the take with Whisper (word timestamps), finds each
scripted line in the transcript, and writes [start, end] per line into takes.TAKE.times. Also suggests
takes.TAKE.cut (just after the last line) when it is not set, and reports any words spoken after the
last scripted line, which generated video often adds (an echoed line, an "Mm.").

Needs ffmpeg and Whisper: `pip install openai-whisper` (or the `whisper` command on PATH).
"""
import difflib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOLD = 0.3  # seconds a caption stays up after the line's last word


def norm(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def transcribe(video, model):
    tmp = Path(tempfile.mkdtemp())
    wav = tmp / "audio.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-ac", "1", "-ar", "16000", str(wav)], check=True)
    try:
        import whisper  # type: ignore
        result = whisper.load_model(model).transcribe(str(wav), word_timestamps=True, language="en")
    except ImportError:
        if not shutil.which("whisper"):
            sys.exit("Whisper not found: pip install openai-whisper")
        subprocess.run(["whisper", str(wav), "--model", model, "--word_timestamps", "True",
                        "--output_format", "json", "--output_dir", str(tmp)], check=True, capture_output=True)
        result = json.loads((tmp / "audio.json").read_text())
    return [(w["start"], w["end"], w["word"]) for s in result["segments"] for w in s.get("words", [])]


def align(lines, words):
    """Map each scripted line to transcript words by matching normalised characters."""
    chars, owner = "", []
    for i, (_, _, w) in enumerate(words):
        n = norm(w)
        chars += n
        owner += [i] * len(n)
    cursor, spans = 0, []
    for line in lines:
        target = norm(line)
        hit = chars.find(target, cursor)
        if hit < 0:  # fuzzy: best matching block from the cursor on
            sm = difflib.SequenceMatcher(None, chars[cursor:], target, autojunk=False)
            blocks = [b for b in sm.get_matching_blocks() if b.size]
            if not blocks:
                spans.append(None)
                continue
            first, last = blocks[0], blocks[-1]
            a, b = cursor + first.a, cursor + last.a + last.size - 1
        else:
            a, b = hit, hit + len(target) - 1
        wa, wb = owner[a], owner[min(b, len(owner) - 1)]
        spans.append((words[wa][0], words[wb][1]))
        cursor = b + 1
    tail_from = owner[cursor] if cursor < len(owner) else None
    return spans, tail_from


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "small.en"
    if "--model" in sys.argv:
        args.remove(model)
    if len(args) != 2:
        sys.exit(__doc__)
    cfg_path, take = Path(args[0]), args[1]
    cfg = json.loads(cfg_path.read_text())
    t = cfg["takes"][take]
    video = (cfg_path.parent / t["file"]).resolve()
    words = transcribe(video, model)
    spans, tail_from = align(cfg["lines"], words)
    times = []
    for line, span in zip(cfg["lines"], spans):
        if span is None:
            print(f"NOT FOUND, set by hand: {line}")
            times.append(None)
        else:
            times.append([round(span[0], 2), round(span[1] + HOLD, 2)])
            print(f"{span[0]:6.2f}-{span[1]:6.2f}  {line}")
    t["times"] = times
    found = [s for s in spans if s]
    extra_at = None
    if tail_from is not None:
        extra = " ".join(w for _, _, w in words[tail_from:]).strip()
        if extra:
            extra_at = words[tail_from][0]
            print(f"EXTRA speech after the script from {extra_at:.2f} s: {extra!r}. The cut must come before it.")
    if found and "cut" not in t:
        cut = found[-1][1] + 0.6
        if extra_at is not None:
            cut = min(cut, max(extra_at - 0.1, found[-1][1] + 0.15))
        t["cut"] = round(cut, 2)
        print(f"cut suggested at {t['cut']} s (after the last line); check it by eye and ear")
    cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
