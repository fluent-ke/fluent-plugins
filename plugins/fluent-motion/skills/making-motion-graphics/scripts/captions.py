#!/usr/bin/env python3
"""captions.py <pages.txt> [words.json] [captions.js] [--join name=part+part …] [--snap onsets.txt]

Builds captions.js (globalThis.CAPS) for caps() in comp.html from a page list you write by hand:

    # start-seconds | the words on the page, *key phrase* in the accent
    0.04 | most founders
    0.58 | don't *quit*
    26.75 | That's why we built a *Acme.*

- Each page starts at the time you give it: take it from onsets.txt (measured speech onsets), not from whisper,
  whose word times drift by up to 0.6 s.
- The words after the first pop on whisper's times (words.json, edited time from cut_interview.py), kept in order.
- Pages must use the speaker's words verbatim. A brand name whisper splits or mishears is matched with --join,
  e.g. --join acme=ack+me matches the whisper words "ack" "me." to the page word "Acme.".
- --snap onsets.txt moves every later word onto the nearest measured onset within 0.2 s, so words pop when they are said.
"""
import json, re, sys

a = sys.argv[1:]
if not a: sys.exit(__doc__)
joins = {}
while '--join' in a:
    i = a.index('--join'); name, parts = a[i + 1].split('='); joins[name.lower()] = parts.lower().split('+'); del a[i:i + 2]
snap = []
if '--snap' in a:
    i = a.index('--snap'); snap = [float(x) for x in open(a[i + 1]) if x.strip()]; del a[i:i + 2]
PAGES_F, WORDS_F, OUT = a[0], a[1] if len(a) > 1 else 'words.json', a[2] if len(a) > 2 else 'captions.js'
W = json.load(open(WORDS_F))
norm = lambda s: re.sub(r"[^a-z0-9']", '', s.lower())
pages = []
for line in open(PAGES_F):
    line = line.strip()
    if not line or line.startswith('#'): continue
    t, txt = line.split('|', 1); pages.append([float(t), txt.strip()])
wi, out = 0, []
for k, (t0, txt) in enumerate(pages):
    acc, words = False, []
    for i, tk in enumerate(txt.split()):
        if tk.startswith('*'): acc = True
        clean = tk.strip('*'); parts = joins.get(norm(clean), [norm(clean)])
        cand = [j for j in range(wi, min(len(W), wi + 14)) if [norm(w[0]) for w in W[j:j + len(parts)]] == parts]
        if not cand: sys.exit(f'"{clean}" (page at {t0}: {txt}) is not in words.json near here: the page must match what is said; use --join for a split brand name')
        j = min(cand, key=lambda j: abs(W[j][1] - t0)) if i == 0 else cand[0]   # first word: the occurrence nearest the page time
        ts = t0 if i == 0 else W[j][1]
        if i and snap:                                                         # nearest measured onset within 0.2 s
            near = min(snap, key=lambda o: abs(o - ts)); ts = near if abs(near - ts) <= .2 else ts
        if i: ts = max(ts, words[-1][1] + .06)
        words.append([clean, round(ts, 2), acc]); wi = j + len(parts)
        if tk.endswith('*'): acc = False
    end = pages[k + 1][0] if k + 1 < len(pages) else words[-1][1] + 1.0
    out.append({'t': t0, 'end': round(min(end, words[-1][1] + 1.4), 2), 'w': words})
open(OUT, 'w').write('globalThis.CAPS=' + json.dumps(out) + ';\n')
for p in out: print(f"{p['t']:6.2f}–{p['end']:6.2f}  " + ' '.join(('*' + w + '*' if a else w) + f'@{s}' for w, s, a in p['w']))
print(f'{OUT}: {len(out)} pages, {sum(len(p["w"]) for p in out)} words')
