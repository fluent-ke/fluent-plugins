#!/usr/bin/env bash
# qc.sh <film.mp4> [WxH] [fps]
# Automatic checks on a finished film, so "done" rests on evidence rather than a render log:
#   spec (size, fps, codec, BT.709 tags) · dead holds (nothing changes for >5 s) · cut rhythm
#   black frames · loudness (-14 LUFS ±1.5, true peak ≤ -1 dBTP) · a contact sheet (2 frames a second) to read with your own eyes
set -uo pipefail
F=${1:?usage: qc.sh <film.mp4> [WxH] [fps]}; RES=${2:-}; FPS=${3:-}
fail=0; bad(){ echo "  ✗ $*"; fail=1; }; ok(){ echo "  ✓ $*"; }
q(){ ffprobe -v error -select_streams v:0 -show_entries "stream=$1" -of default=nw=1:nk=1 "$F" | head -1; }
W=$(q width); H=$(q height); C=$(q codec_name); R=$(q r_frame_rate); CS=$(q color_space); D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$F")
echo "$(basename "$F"): ${W}x${H} $C $R fps ${D}s colour=$CS"
[ -n "$RES" ] && { [ "${W}x${H}" = "$RES" ] && ok "size $RES" || bad "size ${W}x${H} ≠ $RES"; }
[ -n "$FPS" ] && { awk -v r="$R" -v f="$FPS" 'BEGIN{split(r,a,"/");d=a[1]/a[2]-f;exit !(d<.5&&d>-.5)}' && ok "fps $FPS" || bad "fps $R ≠ $FPS"; }
[ "$C" = h264 ] && ok "h264" || bad "codec $C (platforms expect h264)"
[ "$CS" = bt709 ] && ok "tagged BT.709" || bad "colour not tagged bt709 (hues can shift after upload)"
LOG=$(ffmpeg -nostdin -hide_banner -nostats -i "$F" -vf "freezedetect=n=-50dB:d=5,blackdetect=d=0.1:pix_th=0.05,scdet=t=8" -af ebur128=peak=true -f null - 2>&1 || true)
if grep -q "freeze_start" <<<"$LOG"; then bad "dead hold: $(grep -o 'freeze_start: [0-9.]*' <<<"$LOG" | head -3 | tr '\n' ' ')"; else ok "no hold longer than 5 s"; fi
B=$(grep -o 'black_start:[0-9.]*' <<<"$LOG" | grep -v 'black_start:0$' | head -3 | tr '\n' ' ' || true); [ -z "$B" ] && ok "no black frames" || echo "  ⚠ black frames at $B (fine if it is the final fade)"
CUTS=$(grep -c 'lavfi.scd.time' <<<"$LOG" || true)
EVERY=$(awk -v d="$D" -v c="$CUTS" 'BEGIN{printf "%.1f", d/(c+1)}' </dev/null)
echo "  · $CUTS scene changes, about one every $EVERY s"
I=$(grep -A1 'Integrated loudness' <<<"$LOG" | grep -o '\-\?[0-9.]* LUFS' | head -1 | awk '{print $1}' || true)
P=$(grep -A1 'True peak' <<<"$LOG" | grep -o '\-\?[0-9.]* dBFS' | head -1 | awk '{print $1}' || true)
[ -n "$I" ] && { awk -v i="$I" 'BEGIN{exit !(i>-15.5&&i<-12.5)}' && ok "loudness $I LUFS" || bad "loudness $I LUFS (aim for -14)"; }
[ -n "$P" ] && { awk -v p="$P" 'BEGIN{exit !(p<=-0.9)}' && ok "true peak $P dBTP" || bad "true peak $P dBTP (ceiling -1)"; }
SHEET="${F%.*}-sheet.jpg"
ROWS=$(awk -v d="$D" 'BEGIN{n=int(d*2);print int((n+5)/6)}' </dev/null)
ffmpeg -nostdin -y -loglevel error -i "$F" -vf "fps=2,scale=270:-1,tile=6x$ROWS" -frames:v 1 "$SHEET"
echo "  · contact sheet → $SHEET (read it: hook in the first 2 s, text legible, nothing under platform UI)"
[ "$fail" -eq 0 ] && echo "QC passed" || { echo "QC failed"; exit 1; }
