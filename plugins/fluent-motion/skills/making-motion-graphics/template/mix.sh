#!/usr/bin/env bash
# ./mix.sh [name] [audio] [video] [offset-seconds]
#   name   output name (default: film) → out/<name>-master.mp4 (archive) and out/<name>.mp4 (for posting)
#   audio  score.wav from soundtrack.mjs, or a licensed track (mp3/wav/m4a)
#   offset seconds to skip into the track so its downbeat lands on frame 0 (default 0)
set -euo pipefail
cd "$(dirname "$0")"
NAME=${1:-film}; AUDIO=${2:-score.wav}; VIDEO=${3:-out/video-only.mp4}; OFF=${4:-0}
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
FADE=$(awk "BEGIN{print ($DUR>1.5)?$DUR-1.2:0}")
ffmpeg -y -loglevel error -i "$VIDEO" -ss "$OFF" -i "$AUDIO" -filter_complex \
  "[1:a]atrim=0:$DUR,asetpts=PTS-STARTPTS,afade=t=out:st=$FADE:d=1.2,loudnorm=I=-14:TP=-1.2:LRA=9,aresample=48000[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -t "$DUR" -movflags +faststart "out/$NAME-master.mp4"
# Posting copy: capped bitrate so Instagram, TikTok and WhatsApp accept it without re-compressing badly
ffmpeg -y -loglevel error -i "out/$NAME-master.mp4" -c:v libx264 -preset slow -b:v 12M -maxrate 16M -bufsize 24M \
  -profile:v high -pix_fmt yuv420p -c:a copy -movflags +faststart "out/$NAME.mp4"
echo "→ out/$NAME.mp4 and out/$NAME-master.mp4 ($(printf '%.1f' "$DUR") s)"
