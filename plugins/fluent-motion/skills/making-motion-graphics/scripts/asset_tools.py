#!/usr/bin/env python3
"""Asset helpers for a film project. Needs Pillow (pip install pillow).

  asset_tools.py info    <image>...                      size of each image
  asset_tools.py crop    <image> <x0> <y0> <x1> <y1> <out.png>   cut a logo or flag out of a poster, in source pixels
  asset_tools.py key     <image> <out.png> [tolerance]   make the background colour (sampled at the top-left corner) transparent
  asset_tools.py palette <image> [n]                     the n dominant colours as hex (a flat logo or brand sheet; on a photo poster it only finds the photo)
  asset_tools.py sample  <image> <x0> <y0> <x1> <y1>     average colour of a region: point it at a headline, button or logo to read a brand colour
  asset_tools.py sheet   <out.png> <image>... [--cols 4] [--w 360]   tile stills into one contact sheet to review at a glance
  asset_tools.py grid    <image> <out.png> [x0 y0 x1 y1] [step]   pixel grid labelled in source pixels, cropped to the region: read corners and points off a frame
"""
import sys
from PIL import Image

def info(paths):
    for p in paths:
        im = Image.open(p); print(f"{p}: {im.width}x{im.height} {im.mode}")

def crop(p, x0, y0, x1, y1, out):
    Image.open(p).crop((int(x0), int(y0), int(x1), int(y1))).save(out); print(out)

def key(p, out, tol=40):
    im = Image.open(p).convert('RGBA'); px = im.load(); bg = px[2, 2]; tol = float(tol)
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            d = ((r - bg[0])**2 + (g - bg[1])**2 + (b - bg[2])**2) ** .5
            px[x, y] = (r, g, b, int(a * max(0, min(1, (d - tol) / (tol * 2.25)))))
    im.save(out); print(f"{out} (keyed out {bg[:3]})")

def palette(p, n=6):
    im = Image.open(p).convert('RGB'); im.thumbnail((300, 300))
    q = im.quantize(colors=int(n), method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:int(n) * 3]; counts = sorted(q.getcolors(), reverse=True)
    for c, i in counts:
        r, g, b = pal[i*3:i*3+3]; print(f"#{r:02X}{g:02X}{b:02X}  {100*c/sum(x for x,_ in counts):.0f}%")

def sample(p, x0, y0, x1, y1):
    im = Image.open(p).convert('RGB').crop((int(x0), int(y0), int(x1), int(y1))); px = list(im.getdata())
    # the most common colour in the region, so anti-aliased edges and background don't pull the average
    from collections import Counter
    (r, g, b), n = Counter((r//4*4, g//4*4, b//4*4) for r, g, b in px).most_common(1)[0]
    print(f"#{r:02X}{g:02X}{b:02X}  ({100*n/len(px):.0f}% of the region)")

def sheet(out, paths, cols=4, w=360):
    ims = [Image.open(p).convert('RGB') for p in paths]
    h = int(w * ims[0].height / ims[0].width); rows = (len(ims) + cols - 1) // cols
    s = Image.new('RGB', (cols * w, rows * h), (20, 20, 20))
    for i, im in enumerate(ims): s.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    s.save(out); print(out)

def grid(p, out, *r):
    from PIL import ImageDraw
    im = Image.open(p).convert('RGB'); x0, y0, x1, y1 = map(int, r[:4]) if len(r) >= 4 else (0, 0, im.width, im.height)
    step = int(r[4]) if len(r) == 5 else 25; d = ImageDraw.Draw(im)
    for x in range(0, im.width, step): d.line([(x, 0), (x, im.height)], fill=(0, 255, 0) if x % 100 == 0 else (0, 80, 0))
    for y in range(0, im.height, step): d.line([(0, y), (im.width, y)], fill=(0, 255, 0) if y % 100 == 0 else (0, 80, 0))
    for x in range(0, im.width, 100):
        for y in range(0, im.height, 100): d.text((x + 3, y + 2), f"{x},{y}", fill=(255, 255, 0))
    im.crop((x0, y0, x1, y1)).save(out); print(out)

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    cmd, rest = a[0], a[1:]
    if cmd == 'sheet':
        cols = int(rest[rest.index('--cols') + 1]) if '--cols' in rest else 4
        w = int(rest[rest.index('--w') + 1]) if '--w' in rest else 360
        files, skip = [], False
        for x in rest[1:]:
            if skip: skip = False; continue
            if x in ('--cols', '--w'): skip = True; continue
            files.append(x)
        sheet(rest[0], files, cols, w)
    else:
        {'info': lambda r: info(r), 'crop': lambda r: crop(*r), 'key': lambda r: key(*r), 'palette': lambda r: palette(*r), 'sample': lambda r: sample(*r), 'grid': lambda r: grid(*r)}[cmd](rest)
