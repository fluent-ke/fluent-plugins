#!/usr/bin/env python3
"""shot_check.py <shots/NAME> <masks/NAME> [--clean]: measure a talking-head shot for the studio effects (references/studio.md).
Reads the frames and the person mattes from segment.swift and writes shots/NAME.info.js (load it in comp.html after studio.js):
  per frame: head top, head centre x, neck (narrowest row under the head), shoulder line, subject left/right, and the background's
  drift dx,dy from frame 1 (phase correlation on the room, the person masked out), all in frame pixels;
  per shot: whether the camera moves, how textured the room is, and how much of the room is ever seen behind the person.
--clean also writes assets/NAME_clean.png in the film folder: the room with the person removed (averaged from frames where that pixel is uncovered,
holes filled from their surroundings), for vertigo. Then prints which studio effects the shot supports: OK, CHECK or SKIP, with why.
Needs numpy and Pillow."""
import glob, json, os, sys
import numpy as np
from PIL import Image

a = sys.argv[1:]
if len(a) < 2: sys.exit(__doc__)
sdir, mdir, clean = a[0].rstrip('/'), a[1].rstrip('/'), '--clean' in a
name = os.path.basename(sdir)
frames = sorted(glob.glob(os.path.join(sdir, '*.jpg')) + glob.glob(os.path.join(sdir, '*.png')))
if not frames: sys.exit(f'no frames in {sdir}')
W0, H0 = Image.open(frames[0]).size
S = 4                                                           # analyse at 1/4 size
rows, prev, cum, seen = [], None, np.zeros(2), None
acc = cnt = None
def gray(im): return np.asarray(im.convert('L').resize((W0 // S, H0 // S)), np.float32)
for i, f in enumerate(frames):
    mp = os.path.join(mdir, os.path.splitext(os.path.basename(f))[0] + '.png')
    m = np.asarray(Image.open(mp).convert('L').resize((W0 // S, H0 // S)), np.float32) / 255 if os.path.exists(mp) else np.zeros((H0 // S, W0 // S), np.float32)
    on = m > .5; h, w = on.shape
    wid = on.sum(1)
    mid = on[:, w // 4: 3 * w // 4].sum(1)
    top = next((y for y in range(h) if mid[y] > 3), None)
    if top is None:
        rows.append(rows[-1][:6] + [float(cum[0]) * S, float(cum[1]) * S] if rows else [H0 // 3, W0 // 2, H0 // 2, H0 // 2 + 60, W0 // 3, 2 * W0 // 3, 0, 0])
    else:
        band = [x for y in range(top, min(h, top + 12)) for x in np.nonzero(on[y])[0]]
        cx = int(np.mean(band)) if band else w // 2
        lo, hi = top + int(.04 * h), min(h - 1, top + int(.3 * h))     # the neck: narrowest row a little under the head top
        neck = lo + int(np.argmin(wid[lo:hi] + (wid[lo:hi] == 0) * 9999)) if hi > lo else top + h // 10
        nw = max(1, wid[neck])
        sh = next((y for y in range(neck, h) if wid[y] > 1.8 * nw), min(h - 1, neck + h // 12))
        xs = np.nonzero(on.any(0))[0]
        x0, x1 = (int(xs[0]), int(xs[-1])) if len(xs) else (w // 3, 2 * w // 3)
        g = gray(Image.open(f))
        if prev is not None:                                    # room drift: phase correlation with the person filled with the mean
            ga, gb = prev[0].copy(), g.copy(); keep = ~(prev[1] | on)
            ga[~keep] = ga[keep].mean() if keep.any() else 0; gb[~keep] = gb[keep].mean() if keep.any() else 0
            F = np.fft.fft2(ga - ga.mean()) * np.conj(np.fft.fft2(gb - gb.mean())); r = np.fft.ifft2(F / (np.abs(F) + 1e-6)).real
            py, px = np.unravel_index(np.argmax(r), r.shape)
            dy, dx = (py if py < h // 2 else py - h), (px if px < w // 2 else px - w)
            if abs(dx) < w // 8 and abs(dy) < h // 8: cum -= (dx, dy)
        prev = (g, on)
        rows.append([top * S, cx * S, int(neck) * S, int(sh) * S, x0 * S, x1 * S, round(float(cum[0]) * S, 1), round(float(cum[1]) * S, 1)])
    seen = ~on if seen is None else seen | ~on
    if clean and i % 3 == 0:                                    # every third frame is plenty for a static room
        full = np.asarray(Image.open(f).convert('RGB'), np.float32)
        mf = np.asarray(Image.open(mp).convert('L'), np.float32) / 255 if os.path.exists(mp) else np.zeros(full.shape[:2], np.float32)
        wgt = (mf < .1).astype(np.float32)[..., None]
        acc = full * wgt if acc is None else acc + full * wgt; cnt = wgt if cnt is None else cnt + wgt
hh = float(np.median([r[2] - r[0] for r in rows]))              # head height is steady; the narrowest row is not (hands, collars)
for r in rows: r[2] = r[0] + hh                                 # so the neck is the head top plus the shot's median head height
k = 5                                                           # smooth the per-frame numbers a little
sm = [[round(float(np.mean([r[j] for r in rows[max(0, i - k):i + k + 1]])), 1) for j in range(8)] for i in range(len(rows))]
g0 = gray(Image.open(frames[0])); m0 = ~np.asarray(Image.open(os.path.join(mdir, os.path.splitext(os.path.basename(frames[0]))[0] + '.png')).convert('L').resize((W0 // S, H0 // S))).astype(bool) if os.path.exists(os.path.join(mdir, os.path.splitext(os.path.basename(frames[0]))[0] + '.png')) else np.ones_like(g0, bool)
gy, gx = np.abs(np.diff(g0, axis=0))[:, :-1], np.abs(np.diff(g0, axis=1))[:-1, :]
texture = float(((gy + gx)[m0[:-1, :-1]]).mean()) if m0[:-1, :-1].any() else 0.0
drift = float(max(np.hypot(r[6], r[7]) for r in rows))
coverage = float(seen.mean())
info = {'n': len(rows), 'W': W0, 'H': H0, 'cam': {'drift': round(drift, 1), 'moving': drift > 12},
        'bg': {'texture': round(texture, 2), 'plain': texture < 2.5, 'coverage': round(coverage, 3)}, 'f': sm}
out = os.path.join(os.path.dirname(sdir), name + '.info.js')
open(out, 'w').write(f'(globalThis.SHOTINFO??={{}}).{name}=' + json.dumps(info, separators=(',', ':')) + ';\n')
print(f'{out}: {len(rows)} frames, camera drift {drift:.0f} px ({"moving" if drift > 12 else "locked off"}), room texture {texture:.1f} ({"plain" if texture < 2.5 else "textured"}), room seen {coverage:.0%}')
if clean and acc is not None:
    c = cnt[..., 0]; img = acc / np.maximum(cnt, 1e-6); hole = c < .5
    if hole.any():                                              # fill what was never seen from a blurred pyramid of what was
        fill, wsum = np.zeros_like(img), np.zeros(c.shape, np.float32)
        for lv in (8, 16, 32, 64, 128, 256, 512, 2048):
            sm_img = np.asarray(Image.fromarray(np.clip(img * (~hole)[..., None], 0, 255).astype(np.uint8)).resize((max(1, W0 // lv), max(1, H0 // lv)), Image.BOX).resize((W0, H0), Image.BILINEAR), np.float32)
            sm_w = np.asarray(Image.fromarray(((~hole) * 255).astype(np.uint8)).resize((max(1, W0 // lv), max(1, H0 // lv)), Image.BOX).resize((W0, H0), Image.BILINEAR), np.float32) / 255
            take = (wsum < .5) & (sm_w > .05); fill[take] = sm_img[take] / sm_w[take][..., None]; wsum[take] = 1
        img[hole] = fill[hole]
    ad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(sdir))), 'assets'); os.makedirs(ad, exist_ok=True); cp = os.path.join(ad, name + '_clean.png')
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(cp); print(f'{cp}: clean room plate ({hole.mean():.0%} of it filled in, never seen)')
heads_ok = sum(1 for r in rows if r[0] < H0 * .45) / len(rows) > .9
def say(effects, ok, why): print(f"  {'OK   ' if ok == 1 else 'CHECK' if ok == 0 else 'SKIP '} {effects}: {why}")
say('orbit, frame break, cover story, doodle boil, paper cut, green screen, UI world', 1 if heads_ok else -1,
    'head and shoulders in frame' if heads_ok else 'the head is low or missing in more than a tenth of the frames')
say('couch wall, headline wall, chart grow, checklist, glass type', 0 if drift > 12 else 1,
    f'camera drifts {drift:.0f} px: pin with pinned() (tracked)' if drift > 12 else 'locked-off room: graphics sit still on the wall')
say('vertigo', -1 if texture < 2.5 or coverage < .8 else 1,
    'the room is too plain to show the stretch' if texture < 2.5 else f'only {coverage:.0%} of the room is ever seen: too much to invent' if coverage < .8 else
    f'room textured and {coverage:.0%} seen: run with --clean')
say('digital zoom, zoom-through cut, phone mockup, pull-back reveal', 1, 'any shot')
