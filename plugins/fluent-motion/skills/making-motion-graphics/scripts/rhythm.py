#!/usr/bin/env python3
"""rhythm.py <film.mp4> [--shape S]: is the cutting varied enough to stay interesting?
Measures, from the picture itself (so it works on any film, and catches wipes and graphic changes as well as hard cuts):
change events (peaks of ffmpeg's scdet score on a blurred thumbnail), the variation of the gaps between them (CV = sd/mean),
the longest rest (a stretch whose downscaled, blurred frame difference stays tiny: grain does not count as motion),
and the fastest burst (consecutive gaps of one beat or less: the BPM comes from ../timeline.js, else 120). Prints one line per check, ✓ or ✗; exits 1 on any ✗.
The film's shape comes from --shape, else from FILM in ../timeline.js next to an out/ folder; talking-head skips the burst rule,
continuous skips variation and burst."""
import os, re, statistics, subprocess, sys

a = sys.argv[1:]
if not a: sys.exit(__doc__)
src = a[0]; shape = a[a.index('--shape') + 1] if '--shape' in a else None
if shape is None:
    tl = os.path.join(os.path.dirname(os.path.abspath(src)), '..', 'timeline.js')
    m = re.search(r"shape:\s*'([\w-]+)'", open(tl).read()) if os.path.exists(tl) else None
    shape = m.group(1) if m else 'promo'
tl = os.path.join(os.path.dirname(os.path.abspath(src)), '..', 'timeline.js')
bm = re.search(r"globalThis\.BPM\s*=\s*([\d.]+)", open(tl).read()) if os.path.exists(tl) else None
beat = 60 / float(bm.group(1)) if bm else 0.5
quick = max(0.6, beat * 1.15)                 # one beat, with a little slack for detection
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src],
                           capture_output=True, text=True).stdout)
log = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', src, '-vf',
                      'scale=96:-2,gblur=sigma=1.5,scdet=t=0,signalstats,metadata=print', '-an', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
t, frames, score = 0.0, [], []
for line in log.splitlines():
    if 'pts_time:' in line: t = float(line.split('pts_time:')[1].split()[0])
    elif 'lavfi.scd.score=' in line: score.append((t, float(line.split('=')[1])))
    elif 'lavfi.signalstats.YDIF=' in line: frames.append((t, float(line.split('=')[1])))
cuts = []                                     # a change event: a local peak of 2.0 or more, at least 0.2 s after the last one
for i in range(1, len(score) - 1):
    ts, s = score[i]
    if s >= 2.0 and s >= score[i - 1][1] and s >= score[i + 1][1] and (not cuts or ts - cuts[-1] >= 0.2): cuts.append(ts)
edges = [0.0] + cuts + [dur]
shots = [z - a for a, z in zip(edges, edges[1:]) if z - a > 0.05]
cv = statistics.pstdev(shots) / statistics.mean(shots) if len(shots) > 1 else 0.0
rest, start = 0.0, None
for ft, ydif in frames:                       # still: the blurred thumbnail barely changes from the frame before
    if ydif < 0.6:
        start = ft if start is None else start
        rest = max(rest, ft - start)
    else: start = None
burst = cur = 0
for s in shots:
    cur = cur + 1 if s <= quick else 0; burst = max(burst, cur)
fail = False
def check(ok, good, bad):
    global fail
    print(('  ✓ ' + good) if ok else ('  ✗ ' + bad)); fail |= not ok
print(f'  · rhythm ({shape}): {len(shots)} shots between {len(cuts)} changes, mean {statistics.mean(shots):.2f} s, CV {cv:.2f} (target 0.4–0.7), '
      f'longest rest {rest:.1f} s, fastest burst {burst} shots of ≤ {quick:.2f} s')
if shape != 'continuous' and len(shots) >= 4:
    check(cv >= 0.30, f'shot lengths vary (CV {cv:.2f})', f'shots too even (CV {cv:.2f} < 0.30): mix long holds with bursts')
check(rest >= 1.0, f'a rest of {rest:.1f} s', 'no rest: hold something still for 1 s or more, usually before the biggest moment')
if shape not in ('talking-head', 'continuous') and dur >= 12:
    check(burst >= 3, f'a burst of {burst} quick shots', 'no burst: give the film one run of 3 or more one-beat shots')
sys.exit(1 if fail else 0)
