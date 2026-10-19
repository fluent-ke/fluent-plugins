#!/usr/bin/env python3
"""cut_interview.py <src-video> [options]   (run from the film project folder)

Cuts a talking-head take into a tight edit for a voice-led film (references/talking-head.md):
  1. finds the pauses (ffmpeg silencedetect) and shortens every pause longer than --gap to --keep seconds,
     unless edl.json already exists (edit it by hand, then re-run to rebuild from it);
  2. writes graded frames to shots/TALK/0001.jpg … and the cut voice to src/voice-edit.wav, picture and sound
     cut on the same frame boundaries so lip-sync holds;
  3. with --whisper MODEL, transcribes the source with word timestamps and writes words.json in EDITED time;
  4. writes onsets.txt: every word onset it can measure (energy rises), in edited time. Anchor caption pages and cues on these,
     not on whisper's word times (they drift by up to 0.6 s);
  5. writes cuts.txt: every jump cut in edited time, so each one gets a framing change.

Finding the hook: run it once with --whisper and no --from; src/words-source.json lists every word in SOURCE time. Pick the
first word of the hook, read the energy just before it if needed, then re-run with --from (whisper is cached).

Options:  --from S --to S   the part of the take to use (start on the hook, not on a breath)
          --gap 0.55        pauses longer than this are shortened      --keep 0.3   to this length
          --fps 25          pick one that divides the source rate (100/50 → 25, 120/60 → 30), so frames decimate evenly
          --size 1080x1920  cover-cropped from the centre (ffmpeg auto-rotates phone/camera footage first)
          --shot TALK       frame folder name          --whisper small|medium   transcribe (needs the whisper CLI)
"""
import json, os, re, shutil, subprocess, sys

a = sys.argv[1:]
if not a or a[0].startswith('-'): sys.exit(__doc__)
SRC = a[0]
opt = lambda k, d: a[a.index(k) + 1] if k in a else d
FROM, TO = float(opt('--from', 0)), opt('--to', None)
GAP, KEEP, FPS, SHOT = float(opt('--gap', .55)), float(opt('--keep', .3)), int(opt('--fps', 25)), opt('--shot', 'TALK')
W, H = map(int, opt('--size', '1080x1920').split('x')); MODEL = opt('--whisper', None)
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', SRC], capture_output=True, text=True).stdout)
TO = float(TO) if TO else dur
os.makedirs('src', exist_ok=True)
if MODEL and not os.path.exists('src/voice16k.json'):          # transcribe the whole take once, cached for re-runs
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', SRC, '-vn', '-ac', '1', '-ar', '16000', 'src/voice16k.wav'], check=True)
    subprocess.run(['whisper', 'src/voice16k.wav', '--model', MODEL, '--language', 'en', '--word_timestamps', 'True',
                    '--output_format', 'json', '--output_dir', 'src'], check=True, capture_output=True)
if MODEL:
    SW = [[w['word'].strip(), round(w['start'], 2), round(w['end'], 2)] for seg in json.load(open('src/voice16k.json'))['segments'] for w in seg['words']]
    json.dump(SW, open('src/words-source.json', 'w'))
snap = lambda x: round(round(x * FPS) / FPS, 4)          # every cut on a frame boundary of the film

def silences(path):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'silencedetect=n=-38dB:d=0.12', '-f', 'null', '-'], capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', err)]; e = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    return list(zip(s, e + [None] * (len(s) - len(e))))

if os.path.exists('edl.json'):
    EDL = json.load(open('edl.json')); print('using edl.json (delete it to re-detect pauses)')
else:
    EDL, cur = [], snap(FROM)
    for s, e in silences(SRC):
        if e is None or e <= FROM or s >= TO or e - s <= GAP: continue
        cut_a, cut_z = snap(s + KEEP / 2), snap(e - KEEP / 2)
        if cut_a > cur and cut_z > cut_a: EDL.append([cur, cut_a]); cur = cut_z
    EDL.append([cur, snap(TO)]); json.dump(EDL, open('edl.json', 'w'))

GRADE = "curves=all='0/0.015 0.5/0.5 1/0.93',eq=contrast=1.06:saturation=1.06,unsharp=5:5:0.3"   # highlights down, a little contrast
CROP = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}"
v = ';'.join(f"[0:v]trim={x}:{z},setpts=PTS-STARTPTS,fps={FPS}[v{i}]" for i, (x, z) in enumerate(EDL))
au = ';'.join(f"[0:a]atrim={x}:{z},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={z - x - 0.012:.3f}:d=0.012[a{i}]" for i, (x, z) in enumerate(EDL))
n = len(EDL); fc = (f"{v};{au};{''.join(f'[v{i}]' for i in range(n))}concat=n={n}:v=1:a=0,{CROP},{GRADE}[vo];"
                    f"{''.join(f'[a{i}]' for i in range(n))}concat=n={n}:v=0:a=1,aresample=48000[ao]")
shutil.rmtree(f'shots/{SHOT}', ignore_errors=True); os.makedirs(f'shots/{SHOT}')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', SRC, '-filter_complex', fc, '-map', '[vo]', '-q:v', '2', f'shots/{SHOT}/%04d.jpg',
                '-map', '[ao]', '-c:a', 'pcm_s16le', 'src/voice-edit.wav'], check=True)
frames = len(os.listdir(f'shots/{SHOT}')); length = sum(z - x for x, z in EDL)

def edited(t):                                             # source time → edited time (None inside a removed pause)
    acc = 0
    for x, z in EDL:
        if x <= t <= z: return round(acc + t - x, 2)
        acc += z - x
def onsets(path):                                         # word starts: the level jumps 12 dB above where it was 60 ms earlier
    import array, math
    a = array.array('h', subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout)
    e = [20 * math.log10(math.sqrt(sum(x * x for x in a[i:i + 160]) / 160) / 32768 + 1e-9) for i in range(0, len(a) - 160, 160)]
    out = []
    for i in range(6, len(e)):
        if e[i] > -38 and e[i] - min(e[i - 6:i]) > 12 and (not out or i / 100 - out[-1] > .15): out.append(i / 100)
    return out
on = [x for x in onsets('src/voice-edit.wav') if x < length - .05]
open('onsets.txt', 'w').write('\n'.join(f'{x:.2f}' for x in on) + '\n')
cuts = [round(sum(z - x for x, z in EDL[:i]), 2) for i in range(1, len(EDL))]
open('cuts.txt', 'w').write('\n'.join(f'{x:.2f}' for x in cuts) + '\n')
if MODEL:
    words = []
    for seg in json.load(open('src/voice16k.json'))['segments']:
        for w in seg['words']:
            m = edited((w['start'] + w['end']) / 2)          # a word belongs to the edit if its middle survives the cut
            if m is None: continue
            words.append([w['word'].strip(), edited(w['start']) if edited(w['start']) is not None else m, edited(w['end']) or m + .1])
    json.dump(words, open('words.json', 'w'))
    print(f"words.json: {len(words)} words in edited time:\n  " + ' '.join(w for w, _, _ in words))
print(f"{len(EDL)} segments, {length:.2f} s → shots/{SHOT}/ ({frames} frames at {FPS} fps; SHOTS {SHOT}:{{at:0,n:{frames},mask:true}}), "
      f"src/voice-edit.wav, edl.json, onsets.txt ({len(on)} word onsets)\njump cuts at (edited s): {' '.join(f'{x:.2f}' for x in cuts) or 'none'} (cuts.txt): give each a framing change")
if MODEL and FROM == 0: print('source words (pick the hook, then re-run with --from):\n  ' + ' '.join(f'{w}@{a}' for w, a, _ in SW[:40]))
