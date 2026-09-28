#!/usr/bin/env bash
# ./mix.sh [name] [audio] [video] [offset-seconds]
#   name   output name (default: film) → out/<name>-master.mp4 (archive), out/<name>.mp4 (posting), out/<name>-whatsapp.mp4 (≤16 MB)
#   audio  score.wav from soundtrack.mjs, or a licensed track (mp3/wav/m4a)
#   offset seconds to skip into the track so its downbeat lands on frame 0 (default 0)
# Loudness is two-pass: measure, then normalise to -14 LUFS with a -1 dBTP ceiling (single-pass loudnorm drifts on short films).
set -euo pipefail
cd "$(dirname "$0")"
NAME=${1:-film}; AUDIO=${2:-score.wav}; VIDEO=${3:-out/video-only.mp4}; OFF=${4:-0}
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
FADE=$(awk "BEGIN{print ($DUR>1.5)?$DUR-1.2:0}")
PRE="atrim=0:$DUR,asetpts=PTS-STARTPTS,afade=t=out:st=$FADE:d=1.2"
M=$(ffmpeg -hide_banner -nostats -ss "$OFF" -i "$AUDIO" -af "$PRE,loudnorm=I=-14:TP=-1:LRA=11:print_format=json" -f null - 2>&1 | awk '/^\{/,/^\}/')
g(){ printf '%s' "$M" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
LN="loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true"
ffmpeg -y -loglevel error -i "$VIDEO" -ss "$OFF" -i "$AUDIO" -filter_complex "[1:a]$PRE,$LN,aresample=48000[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -ar 48000 -t "$DUR" -movflags +faststart "out/$NAME-master.mp4"
TAGS=(-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv)
# Posting copy: capped bitrate so Instagram, TikTok and Reels recompress it cleanly
ffmpeg -y -loglevel error -i "out/$NAME-master.mp4" -c:v libx264 -preset slow -b:v 12M -maxrate 16M -bufsize 24M \
  -profile:v high -pix_fmt yuv420p "${TAGS[@]}" -c:a aac -b:a 192k -movflags +faststart "out/$NAME.mp4"
# WhatsApp Status / DM copy: WhatsApp caps video at 16 MB, so size the bitrate to the length
VB=$(awk "BEGIN{v=int((15.2*8*1024/$DUR)-160); print (v>6000)?6000:v}")
ffmpeg -y -loglevel error -i "out/$NAME-master.mp4" -c:v libx264 -preset slow -b:v ${VB}k -maxrate ${VB}k -bufsize $((VB*2))k \
  -profile:v high -pix_fmt yuv420p "${TAGS[@]}" -c:a aac -b:a 128k -movflags +faststart "out/$NAME-whatsapp.mp4"
echo "→ out/$NAME.mp4, out/$NAME-master.mp4, out/$NAME-whatsapp.mp4 ($(printf '%.1f' "$DUR") s, $(du -h "out/$NAME-whatsapp.mp4" | cut -f1) for WhatsApp)"
