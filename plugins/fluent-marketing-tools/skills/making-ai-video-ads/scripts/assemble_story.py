"""Join silent chapters and a separate narration into one master take per format, for build_ad.py.

Usage:  python3 assemble_story.py story.json [TAKE ...] [--standin] [--model small.en]

Reads story.json (schema: references/story-ads.md). For each take key (e.g. wide, tall) it trims and
joins the chapters, lays each narration piece over its chapter with the generated room tone kept low,
softens any flagged screen regions with a feathered blur, and appends an optional closing clip with its
own audio. It writes build/master-TAKE.mov and fills ad.json (lines, takes.TAKE.file/times/cut), so
the next step is simply:  python3 build_ad.py ad.json

Caption times come from each voice's "captions" ([start, end, text] in the voice file's own time), or,
when a voice lists "lines" instead, from Whisper word timestamps on that file (cached beside it as
FILE.captions.json, so check and correct that file once and it is reused).
--standin fills a missing chapter with the first chapter, to preview timing before every chapter exists.
Needs Python 3 and ffmpeg; Whisper only for "lines".
"""
import json
import subprocess
import sys
from pathlib import Path

ROOM_DB = -14   # generated room tone under the narration
EDGE = 0.25     # audio fade at each chapter edge
FEATHER = 80    # px of soft edge on a blur region that sits inside the frame
HOLD = 0.25     # seconds a caption stays up after its last word


def probe(p, entries):
    out = subprocess.run(["ffprobe", "-v", "error", *entries, "-of", "csv=p=0", str(p)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return out


def dur(p):
    return float(probe(p, ["-show_entries", "format=duration"]))


def size(p):
    w, h = probe(p, ["-select_streams", "v", "-show_entries", "stream=width,height"]).split(",")
    return int(w), int(h)


def has_audio(p):
    return bool(probe(p, ["-select_streams", "a", "-show_entries", "stream=index"]))


def add_clip(inputs, chain, src, a, b, n, frame):
    """Input a clip trimmed to [a, b], scaled and padded to the frame; returns (video label, audio label, next n).
    A clip without sound gets silence, so the join never fails on a missing stream."""
    W, H = frame
    L = b - a
    inputs += ["-i", str(src)]
    vi = n
    n += 1
    chain.append(f"[{vi}:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=24,scale={W}:{H}:force_original_aspect_ratio=decrease,"
                 f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,format=yuv420p,setsar=1[v{vi}a]")
    if has_audio(src):
        alabel = f"{vi}:a"
        chain.append(f"[{alabel}]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,"
                     f"aformat=channel_layouts=stereo[s{vi}]")
    else:
        inputs += ["-f", "lavfi", "-t", str(L), "-i", "anullsrc=r=48000:cl=stereo"]
        chain.append(f"[{n}:a]anull[s{vi}]")
        n += 1
    return f"v{vi}a", f"s{vi}", vi, n


def voice_captions(root, name, v, model):
    """[[start, end, text], ...] in the voice file's own time."""
    if "captions" in v:
        return v["captions"]
    src = root / v["file"]
    cache = src.with_name(src.name + ".captions.json")
    if cache.exists():
        return json.loads(cache.read_text())
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from caption_timings import align, transcribe  # same folder
    words = transcribe(src, model)
    spans, _ = align(v["lines"], words)
    caps = []
    for line, span in zip(v["lines"], spans):
        if span is None:
            sys.exit(f"voice {name}: line not heard, add it to {cache.name} by hand: {line}")
        caps.append([round(span[0], 2), round(span[1], 2), line])
    cache.write_text(json.dumps(caps, indent=2, ensure_ascii=False) + "\n")
    print(f"timed {len(caps)} lines in {v['file']}; check {cache.name} by ear")
    return caps


def blur_chain(label, regions, frame, a, tag):
    """Feathered gblur over [x, y, w, h] regions between chapter times; returns (filters, out_label)."""
    fw, fh = frame
    chain, last = [], label
    for j, (fa, fb, x, y, w, h, *rest) in enumerate(regions):
        sig = rest[0] if rest else 6  # optional 7th value: blur strength
        F = max(4, min(FEATHER, w // 4, h // 4))  # a small box keeps a solid centre
        edges = ["1"]
        if x > 0:
            edges.append(f"X/{F}")
        if x + w < fw:
            edges.append(f"(W-X)/{F}")
        if y > 0:
            edges.append(f"Y/{F}")
        if y + h < fh:
            edges.append(f"(H-Y)/{F}")
        alpha = "min(" * (len(edges) - 1) + edges[0] + "".join(f",{e})" for e in edges[1:])
        k, s, b, o = f"bk{tag}{j}", f"bs{tag}{j}", f"bb{tag}{j}", f"bo{tag}{j}"
        chain += [f"[{last}]split[{k}][{s}]",
                  f"[{s}]crop={w}:{h}:{x}:{y},gblur=sigma={sig},format=yuva420p,"
                  f"geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':a='255*{alpha}'[{b}]",
                  f"[{k}][{b}]overlay={x}:{y}:enable='between(t,{fa - a},{fb - a})'[{o}]"]
        last = o
    return chain, last


def build(story, root, take, standin, model):
    inputs, parts, chain, caps = [], [], [], []
    voices = story.get("voices", {})
    room_db = story.get("room_db", ROOM_DB)
    t0, n = 0.0, 0
    first = root / story["chapters"][0]["takes"][take]
    frame = size(first)  # every clip is fitted to the first chapter's frame
    for c, ch in enumerate(story["chapters"]):
        src = root / ch["takes"][take]
        if not src.exists():
            if not standin:
                sys.exit(f"missing {src.name} (use --standin to preview with chapter 1 in its place)")
            src = root / story["chapters"][0]["takes"][take]
        a, b = ch.get("trim", [0, None])
        b = dur(src) if b is None else min(b, dur(src))
        L = b - a
        vlab, slab, ci, n = add_clip(inputs, chain, src, a, b, n, frame)
        blur, vlast = blur_chain(vlab, ch.get("blur", {}).get(take, []), frame, a, ci)
        chain += blur + [f"[{vlast}]null[v{ci}]"]
        chain.append(f"[{slab}]volume={room_db}dB,afade=t=in:d={EDGE},afade=t=out:st={L - EDGE}:d={EDGE}[r{ci}]")
        mix = [f"[r{ci}]"]
        for piece in ch.get("voice", []):
            v = voices[piece["from"]]
            vsrc = root / v["file"]
            s = piece.get("start", 0.0)
            e = piece.get("end") or dur(vsrc)
            at = piece["at"]
            if at + e - s > L + 0.01:
                print(f"warning: chapter {c + 1} ({take}): narration runs {at + e - s - L:.2f} s past the chapter "
                      f"and is cut; lower 'at', trim the piece, or lengthen 'trim'")
            inputs += ["-i", str(vsrc)]
            vi = n
            n += 1
            chain.append(f"[{vi}:a]atrim={s}:{e},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                         f"afade=t=in:d=0.05,afade=t=out:st={e - s - 0.08}:d=0.08,adelay={int(at * 1000)}:all=1[n{vi}]")
            mix.append(f"[n{vi}]")
            for ca, cb, text in voice_captions(root, piece["from"], v, model):
                if ca < e and cb > s and not (ca >= s - 0.05 and cb <= e + 0.05):
                    print(f"warning: caption straddles a narration piece edge and is left out: {text!r}; "
                          f"move the piece's start or end to the pause around it")
                if ca >= s - 0.05 and cb <= e + 0.05:
                    caps.append([text, round(t0 + at + ca - s, 2), round(min(t0 + at + cb - s + HOLD, t0 + L), 2)])
        chain.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0:duration=first,"
                     f"apad=whole_dur={L},atrim=0:{L}[a{ci}]")
        parts.append(f"[v{ci}][a{ci}]")
        t0 += L
    closer = story.get("closer")
    if closer:
        src = root / closer["takes"][take]
        a, b = closer.get("trim", [0, None])
        b = dur(src) if b is None else min(b, dur(src))
        vlab, slab, pi, n = add_clip(inputs, chain, src, a, b, n, frame)
        parts.append(f"[{vlab}][{slab}]")
        if closer.get("line"):
            caps.append([closer["line"], round(t0 + closer.get("line_at", 0.15), 2), round(t0 + b - a, 2)])
        t0 += b - a
    caps.sort(key=lambda c: c[1])
    for c, nxt in zip(caps, caps[1:]):  # a caption's hold never runs into the next one
        c[2] = round(min(c[2], nxt[1] - 0.02), 2)
    chain.append(f"{''.join(parts)}concat=n={len(parts)}:v=1:a=1[vout][aout]")
    work = root / story.get("work_dir", "build")
    work.mkdir(parents=True, exist_ok=True)
    out = work / f"master-{take}.mov"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chain),
                    "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                    "-c:a", "pcm_s16le", str(out)], check=True)
    print(f"{out.relative_to(root)}  {t0:.2f} s  {len(caps)} captions")
    return out, t0, caps


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    model = args[args.index("--model") + 1] if "--model" in args else "small.en"
    standin = "--standin" in args
    pos = [x for x in args if not x.startswith("--") and x != model]
    path = Path(pos[0]).resolve()
    root = path.parent
    story = json.loads(path.read_text())
    takes = pos[1:] or sorted({k for ch in story["chapters"] for k in ch["takes"]})
    ad_path = root / story.get("ad", "ad.json")
    ad = json.loads(ad_path.read_text()) if ad_path.exists() else {}
    ad.setdefault("takes", {})
    seen = None
    for take in takes:
        out, total, caps = build(story, root, take, standin, model)
        lines = [c[0] for c in caps]
        if seen is not None and seen != lines:
            print(f"warning: captions for {take} differ from the other takes; build_ad.py needs the same lines in each")
        seen = lines
        ad["lines"] = lines
        ad["takes"][take] = {**ad["takes"].get(take, {}), "file": str(out.relative_to(ad_path.parent)),
                             "times": [[c[1], c[2]] for c in caps], "cut": round(total, 3)}
    ad_path.write_text(json.dumps(ad, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {ad_path.name}; next: python3 build_ad.py {ad_path.name}")


if __name__ == "__main__":
    main()
