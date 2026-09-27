#!/usr/bin/env bash
# prep_footage.sh <src-video> <SHOT> <start-s> <end-s> [slow] [WxH] [fps]
# Cuts one shot out of a source video into shots/<SHOT>/0001.jpg … for comp.html's SHOTS table.
#   slow  playback stretch: 1 = real time, 2 = half speed (frames are motion-interpolated, not duplicated)
#   WxH   output frame, cover-cropped from the centre (default 1080x1920)
# Run it from the film project folder. Prints the frame count to put in SHOTS as n.
set -euo pipefail
SRC=${1:?src}; SHOT=${2:?shot name}; A=${3:?start}; Z=${4:?end}; SLOW=${5:-1}; SIZE=${6:-1080x1920}; FPS=${7:-30}
W=${SIZE%x*}; H=${SIZE#*x}
GRADE="scale=$W:$H:force_original_aspect_ratio=increase:flags=lanczos,crop=$W:$H,unsharp=5:5:0.4,eq=contrast=1.06:saturation=1.08"
MI="minterpolate=fps=$FPS:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
rm -rf "shots/$SHOT"; mkdir -p "shots/$SHOT"
ffmpeg -y -loglevel error -i "$SRC" -vf "trim=$A:$Z,setpts=(PTS-STARTPTS)*$SLOW,$MI,$GRADE" -q:v 2 "shots/$SHOT/%04d.jpg"
echo "$SHOT: $(ls "shots/$SHOT" | wc -l | tr -d ' ') frames"
