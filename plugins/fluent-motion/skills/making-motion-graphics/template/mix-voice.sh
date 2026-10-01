#!/usr/bin/env bash
# ./mix-voice.sh [name] [voice] [score] [video]   for films that carry a voice (an interview, a voiceover)
#   → out/<name>-master.mp4, out/<name>.mp4 (posting), out/<name>-whatsapp.mp4 (≤16 MB)
# The voice gets a high-pass, gentle compression and a presence lift; the score is ducked under it by a sidechain;
# then two-pass loudnorm to -14 LUFS / -1 dBTP. Prints how far the voice sits above the music: keep it 10 dB or more.
set -euo pipefail; cd "$(dirname "$0")"
NAME=${1:-film}; VOICE=${2:-src/voice-edit.wav}; SCORE=${3:-score.wav}; VIDEO=${4:-out/video-only.mp4}
MUSIC=${MUSIC:-0.22}                         # score level before ducking; lower it if the report shows under 10 dB
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
STEMS="[0:a]aresample=48000,highpass=f=75,acompressor=threshold=0.09:ratio=3:attack=8:release=160:makeup=2,equalizer=f=3200:t=q:w=1.2:g=2.5,apad,asplit=2[v][vk];\
[1:a]aresample=48000,volume=$MUSIC[m];[m][vk]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=450[md]"
FC="$STEMS;[v][md]amix=inputs=2:duration=longest:normalize=0,atrim=0:$DUR,afade=t=out:st=$(awk "BEGIN{print $DUR-1.3}"):d=1.3"
M=$(ffmpeg -hide_banner -nostats -i "$VOICE" -i "$SCORE" -filter_complex "$FC,loudnorm=I=-14:TP=-1:LRA=11:print_format=json" -f null - 2>&1 | awk '/^\{/,/^\}/')
g(){ printf '%s' "$M" | python3 -c "import sys,json;print(json.load(sys.stdin)['$1'])"; }
LN="loudnorm=I=-14:TP=-1:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true"
mkdir -p out
ffmpeg -y -loglevel error -i "$VOICE" -i "$SCORE" -i "$VIDEO" -filter_complex "$FC,$LN,aresample=48000[a]" \
  -map 2:v -map "[a]" -c:v copy -c:a aac -b:a 256k -ar 48000 -t "$DUR" -movflags +faststart "out/$NAME-master.mp4"
TAGS=(-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv)
ffmpeg -y -loglevel error -i "out/$NAME-master.mp4" -c:v libx264 -preset slow -b:v 12M -maxrate 16M -bufsize 24M -profile:v high -pix_fmt yuv420p "${TAGS[@]}" -c:a aac -b:a 192k -movflags +faststart "out/$NAME.mp4"
VB=$(awk "BEGIN{v=int((15.2*8*1024/$DUR)-160); print (v>6000)?6000:v}")
ffmpeg -y -loglevel error -i "out/$NAME-master.mp4" -c:v libx264 -preset slow -b:v ${VB}k -maxrate ${VB}k -bufsize $((VB*2))k -profile:v high -pix_fmt yuv420p "${TAGS[@]}" -c:a aac -b:a 128k -movflags +faststart "out/$NAME-whatsapp.mp4"
# Voice over music, per 4 s window where the voice is talking
T=$(mktemp -d); ffmpeg -y -loglevel error -i "$VOICE" -i "$SCORE" -filter_complex "$STEMS" -map "[v]" -t "$DUR" "$T/v.wav" -map "[md]" -t "$DUR" "$T/m.wav"
python3 - "$T" <<'PY'
import sys,subprocess,math,array
def ld(f):return array.array('h',subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-f','s16le','-'],capture_output=True).stdout)
v,m=ld(sys.argv[1]+'/v.wav'),ld(sys.argv[1]+'/m.wav');sr=48000;win=4*sr;low=[]
rms=lambda a:math.sqrt(sum(x*x for x in a[::7])/max(1,len(a[::7])))+1e-6
for i in range(0,min(len(v),len(m))-win//2,win):
  rv,rm=rms(v[i:i+win]),rms(m[i:i+win])
  if 20*math.log10(rv/32768)<-40:continue            # no voice in this window
  d=20*math.log10(rv/rm);low+=[(i/sr,d)] if d<10 else []
  print(f"  {i/sr:5.1f}s voice above music {d:5.1f} dB")
print('voice/music: OK' if not low else f"voice/music: under 10 dB at {', '.join(f'{t:.0f}s' for t,_ in low)}: re-run with MUSIC=0.2 or thin the score there")
PY
rm -rf "$T"
echo "→ out/$NAME.mp4, out/$NAME-master.mp4, out/$NAME-whatsapp.mp4 ($(printf '%.1f' "$DUR") s, $(du -h "out/$NAME-whatsapp.mp4" | cut -f1) WhatsApp)"
