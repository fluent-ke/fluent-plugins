"""Finish generated takes into a posted-ready ad: upscale, captions, end card, music, every format.

Usage:  python3 build_ad.py ad.json [FORMAT ...] [--only with-music|no-music]

Reads ad.json (schema: references/edit-config.md; example: assets/ad.example.json). Paths in ad.json are
relative to the file. Writes <out_dir>/with-music/ and <out_dir>/no-music/ (only no-music when ad.json
has no music), one MP4 per format, so the version without music is always there to compare and to reuse.
Needs Python 3, Pillow (pip install pillow) and ffmpeg on PATH.
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FPS = 24
XFADE = 0.8  # fade through dark into the end card


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Ad:
    def __init__(self, path):
        self.path = Path(path).resolve()
        self.root = self.path.parent
        self.cfg = json.loads(self.path.read_text())
        c = self.cfg
        self.lines = c["lines"]
        col = c.get("colors", {})
        self.ground = hex_rgb(col.get("ground", "#141312"))
        self.text = hex_rgb(col.get("text", "#f5f4ee"))
        self.hairline = hex_rgb(col.get("line", "#b8b6af"))
        self.font_file = c.get("font")
        self.out = self.root / c.get("out_dir", "exports")
        self.work = self.root / c.get("work_dir", "build")

    def file(self, rel):
        return self.root / rel

    def font(self, px):
        if self.font_file:
            return ImageFont.truetype(str(self.file(self.font_file)), px)
        return ImageFont.load_default(px)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    if len(lines) == 2:  # balance two lines so the second is not a widow
        best = None
        for i in range(1, len(words)):
            a, b = " ".join(words[:i]), " ".join(words[i:])
            wa, wb = draw.textlength(a, font=fnt), draw.textlength(b, font=fnt)
            if max(wa, wb) <= width and (best is None or abs(wa - wb) < best[0]):
                best = (abs(wa - wb), [a, b])
        if best:
            lines = best[1]
    return lines


def layout(fmt):
    """Caption size and position per format; any value can be overridden in ad.json."""
    W, H = fmt["size"]
    landscape = W >= H
    tall = H / W > 1.5
    d = dict(cap_px=round(H * 0.046) if landscape else round(W * (0.052 if tall else 0.048)),
             cap_width=round(W * 0.78) if landscape else W - 160,
             cap_bottom=round(H * 0.10) if landscape else round(H * (0.27 if tall else 0.096)))
    d.update({k: fmt[k] for k in ("cap_px", "cap_width", "cap_bottom") if k in fmt})
    return d


def caption_png(ad, text, size, lay, out):
    W, H = size
    fnt = ad.font(lay["cap_px"])
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    lines = wrap(d, text, fnt, lay["cap_width"])
    lh = int(lay["cap_px"] * 1.25)
    y0 = H - lay["cap_bottom"] - lh * len(lines)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for i, line in enumerate(lines):
        sd.text(((W - d.textlength(line, font=fnt)) / 2, y0 + i * lh + 3), line, font=fnt, fill=(*ad.ground, 230))
    img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(lay["cap_px"] / 7)))
    d = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        d.text(((W - d.textlength(line, font=fnt)) / 2, y0 + i * lh), line, font=fnt, fill=(*ad.text, 255))
    img.save(out)


def fade_png(ad, size, lay, out):
    """A graded fade into the ground colour behind the captions, not a box."""
    W, H = size
    top = max(H - lay["cap_bottom"] - int(lay["cap_px"] * 1.25) * 2 - int(lay["cap_px"] * 2.5), 0)
    col = Image.new("L", (1, H), 0)
    for y in range(top, H):
        col.putpixel((0, y), int(150 * ((y - top) / (H - top)) ** 1.6))
    img = Image.new("RGBA", (W, H), (*ad.ground, 0))
    img.putalpha(col.resize((W, H)))
    img.save(out)


def card_png(ad, size, out):
    W, H = size
    card = ad.cfg["end_card"]
    img = Image.new("RGB", (W, H), ad.ground)
    d = ImageDraw.Draw(img)
    short = min(W, H)
    parts = []
    if card.get("logo"):
        logo = Image.open(ad.file(card["logo"])).convert("RGBA")
        lw = int(short * (0.42 if W >= H else 0.56))
        logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
        parts.append(("logo", logo, logo.height))
    head = ad.font(int(short * 0.058))
    if card.get("headline"):
        hl = wrap(d, card["headline"], head, int(W * (0.62 if W >= H else 0.80)))
        parts.append(("head", hl, int(head.size * 1.18) * len(hl)))
    cta_f = ad.font(int(short * 0.036))
    if card.get("cta"):
        pad_y = int(cta_f.size * 0.7)
        parts.append(("cta", card["cta"], cta_f.size + 2 * pad_y))
    gaps = {"head": int(short * 0.085), "cta": int(short * 0.06)}
    total = sum(h for _, _, h in parts) + sum(gaps.get(k, 0) for k, _, _ in parts[1:])
    y = (H - total) // 2
    for i, (kind, val, h) in enumerate(parts):
        if i:
            y += gaps.get(kind, 0)
        if kind == "logo":
            img.paste(val, ((W - val.width) // 2, y), val)
        elif kind == "head":
            for line in val:
                d.text(((W - d.textlength(line, font=head)) / 2, y), line, font=head, fill=ad.text)
                y += int(head.size * 1.18)
            continue
        else:  # a hairline pill: the logo carries the brand colour, the CTA stays quiet
            cw = d.textlength(val, font=cta_f)
            pad_x, pad_y = int(cta_f.size * 1.1), int(cta_f.size * 0.7)
            x0 = (W - cw) / 2 - pad_x
            d.rounded_rectangle([x0, y, x0 + cw + 2 * pad_x, y + h], radius=h / 2, outline=ad.hairline, width=2)
            d.text(((W - cw) / 2, y + pad_y - int(cta_f.size * 0.12)), val, font=cta_f, fill=ad.text)
        y += h
    img.save(out)


def build(ad, fmt, with_music):
    take = ad.cfg["takes"][fmt["take"]]
    W, H = fmt["size"]
    lay = layout(fmt)
    work = ad.work / fmt["name"]
    work.mkdir(parents=True, exist_ok=True)
    times = take["times"]
    if any(t is None for t in times) or len(times) != len(ad.lines):
        sys.exit(f"take {fmt['take']}: every line needs [start, end] in times (run caption_timings.py)")
    cut = take["cut"]
    card_s = ad.cfg["end_card"].get("seconds", 3.5)
    total = cut + card_s - XFADE

    caps = []
    for i, (text, (a, b)) in enumerate(zip(ad.lines, times)):
        p = work / f"cap{i}.png"
        caption_png(ad, text, (W, H), lay, p)
        caps.append((p, a, min(b, cut)))
    fade_png(ad, (W, H), lay, work / "fade.png")
    card_png(ad, (W, H), work / "card.png")

    crop = "crop={}:{}:{}:{},".format(*fmt["crop"]) if fmt.get("crop") else ""
    soften = "".join(f"gblur=sigma=4.5:enable='between(t,{a},{b})'," for a, b in take.get("soften", []))
    chain = [f"[0:v]trim=0:{cut},setpts=PTS-STARTPTS,{soften}{crop}hqdn3d=1.2:1.2:3:3,"
             f"scale={W}:{H}:flags=lanczos,cas=0.55,format=yuv420p,fps={FPS}[v0]",
             f"[v0][2:v]overlay=0:0:shortest=1:enable='between(t,0.8,{cut})'[v1]"]
    last = "v1"
    for i, (_, a, b) in enumerate(caps):
        chain.append(f"[{last}][{3 + i}:v]overlay=0:0:shortest=1:enable='between(t,{a},{b})'[c{i}]")
        last = f"c{i}"
    chain += [f"[1:v]fps={FPS},format=yuv420p,trim=0:{card_s},setpts=PTS-STARTPTS[card]",
              f"[{last}]format=yuv420p,setsar=1[film]",
              f"[film][card]xfade=transition=fadeblack:duration={XFADE}:offset={cut - XFADE}[vout]"]
    voice = (f"[0:a]atrim=0:{cut},asetpts=PTS-STARTPTS,afade=t=out:st={cut - XFADE - 0.1}:d={XFADE},"
             f"apad=whole_dur={total},aresample=48000,aformat=channel_layouts=stereo")
    loud = "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[aout]"
    inputs = ["-i", str(ad.file(take["file"])), "-loop", "1", "-t", str(card_s), "-i", str(work / "card.png"),
              "-loop", "1", "-i", str(work / "fade.png")]
    for p, _, _ in caps:
        inputs += ["-loop", "1", "-i", str(p)]

    if not with_music:
        chain.append(f"{voice},{loud}")
    else:
        m = ad.cfg["music"]
        inputs += ["-i", str(ad.file(m["file"]))]
        mi = 3 + len(caps)
        chain.append(f"{voice},asplit=2[voice][key]")
        chain.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,volume={m.get('level_db', -13)}dB,"
                     f"asplit=2[ma][mb]")
        a_end = (times[-1][0] - 0.05) if m.get("break_before_last_line") else total
        start = m.get("start_at", 0)
        chain.append(f"[ma]atrim={start}:{start + a_end},asetpts=PTS-STARTPTS,"
                     f"afade=t=out:st={a_end - 0.9}:d=0.85[mA]")
        if m.get("return_at") is not None:  # a phrase of the track comes back as the end card lands
            b_at = cut - 0.35
            b_len = total - b_at
            r = m["return_at"]
            chain.append(f"[mb]atrim={r}:{r + b_len},asetpts=PTS-STARTPTS,volume={m.get('return_boost_db', 3)}dB,"
                         f"afade=t=in:d=0.08,afade=t=out:st={b_len - 1.3}:d=1.3,adelay={int(b_at * 1000)}:all=1[mB]")
            chain.append(f"[mA][mB]amix=inputs=2:normalize=0:duration=longest,apad=whole_dur={total}[mus]")
        else:
            chain.append("[mb]anullsink")
            chain.append(f"[mA]apad=whole_dur={total}[mus]")
        chain.append("[mus][key]sidechaincompress=threshold=0.02:ratio=6:attack=25:release=500[ducked]")
        chain.append(f"[voice][ducked]amix=inputs=2:normalize=0:duration=first,{loud}")

    out_dir = ad.out / ("with-music" if with_music else "no-music")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{fmt['name']}.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chain),
           "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "slow",
           "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    print(f"{out.relative_to(ad.root)}  {W}x{H}  {total:.2f} s")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    only = args[args.index("--only") + 1] if "--only" in args else None
    names = [a for a in args[1:] if not a.startswith("--") and a != only]
    ad = Ad(args[0])
    versions = [False] + ([True] if ad.cfg.get("music") else [])
    if only:
        versions = [v for v in versions if (v and only == "with-music") or (not v and only == "no-music")]
    for fmt in ad.cfg["formats"]:
        if names and fmt["name"] not in names:
            continue
        for with_music in versions:
            build(ad, fmt, with_music)


if __name__ == "__main__":
    main()
