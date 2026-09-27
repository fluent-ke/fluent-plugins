#!/usr/bin/env bash
# study_reference.sh <video> [out-dir]
# Breaks down a reference or source video so you can see its pacing and look without watching it:
#   - duration, size, fps, audio yes/no
#   - every hard cut (scene change) with its time, and the average shot length
#   - sheet.png: one frame per shot, tiled, to read with an image viewer (needs Pillow)
set -euo pipefail
V=${1:?video}; OUT=${2:-study}; mkdir -p "$OUT"
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of compact "$V"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
ffmpeg -hide_banner -i "$V" -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 > "$OUT/cuts.txt" || true
NC=$(wc -l < "$OUT/cuts.txt" | tr -d ' ')
echo "cuts: $NC  → $OUT/cuts.txt"
awk -v d="$DUR" -v n="$NC" 'BEGIN{printf "average shot length: %.2f s\n", d/(n+1)}'
# One frame per shot, sampled 0.6 s after its cut so a transition isn't what you see (every 1 s when there are no cuts)
if [ "$NC" -gt 0 ]; then TIMES=$( (echo 0; cat "$OUT/cuts.txt") | head -24); else TIMES=$(seq 0 1 "${DUR%.*}" | head -24); fi
rm -f "$OUT"/f_*.png; i=0
for t in $TIMES; do s=$(awk -v t="$t" -v d="$DUR" 'BEGIN{x=t+0.6; if(x>d-0.1)x=d-0.1; print x}')
  ffmpeg -v error -y -ss "$s" -i "$V" -frames:v 1 -vf scale=240:-2 "$OUT/$(printf 'f_%02d' $i).png"; i=$((i+1)); done
python3 "$(dirname "$0")/asset_tools.py" sheet "$OUT/sheet.png" "$OUT"/f_*.png --cols 6 --w 240 >/dev/null
echo "contact sheet ($i frames, one per shot) → $OUT/sheet.png"
