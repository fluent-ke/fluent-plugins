#!/usr/bin/env python3
"""audio_check.py <file.wav|file.mp4> [window-seconds]

You cannot listen, so measure. Prints level per window as a bar chart, integrated loudness (LUFS),
and flags the faults that matter: silence, clipping, and a flat line (a stuck or runaway voice makes
every window read the same level, including sections that should be quiet).
"""
import array, math, subprocess, sys, wave, tempfile, os

src = sys.argv[1]; win = float(sys.argv[2]) if len(sys.argv) > 2 else 1
tmp = None
def pcm16(p):                                   # wave reads 16-bit PCM only: 24-bit, float and WAVE_FORMAT_EXTENSIBLE files are converted first
    try:
        with wave.open(p) as w: return w.getsampwidth() == 2
    except wave.Error: return False
if not src.lower().endswith('.wav') or not pcm16(src):
    tmp = tempfile.mktemp(suffix='.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-ac', '2', '-ar', '44100', tmp], check=True); src = tmp
w = wave.open(src); sr = w.getframerate(); ch = w.getnchannels()
a = array.array('h', w.readframes(w.getnframes()))
lv = []; total = len(a) / (sr * ch); t0 = 0.0
while t0 + win * .5 <= total:
    seg = a[int(t0 * sr) * ch:int((t0 + win) * sr) * ch]
    sub = seg[::5]; r = math.sqrt(sum(x * x for x in sub) / len(sub)) / 32768; p = max(abs(x) for x in seg) / 32768
    db = 20 * math.log10(r + 1e-9); lv.append(db)
    flag = ' SILENT' if db < -45 else ' CLIPPING' if p >= .999 else ''
    print(f"{t0:5.1f}s {db:6.1f} dB peak {p:.2f} " + '#' * int(max(0, 45 + db)) + flag)
    t0 += win
lufs = subprocess.run(['ffmpeg', '-hide_banner', '-i', src, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
i = [l for l in lufs.splitlines() if l.strip().startswith('I:')]
print('integrated loudness:', i[-1].split(':', 1)[1].strip() if i else '?', '(posting target is about -14 LUFS; mix.sh normalises to it)')
body = lv[:-max(1, int(2 / win))]          # the fade-out tail is always quiet; judge the rest
if len(body) > 2 and max(body) - min(body) < 4:
    print('FLAT: every window within 4 dB before the fade. Quiet sections are not quiet; check for a voice that never ends or a kick that dominates.')
if tmp: os.remove(tmp)
