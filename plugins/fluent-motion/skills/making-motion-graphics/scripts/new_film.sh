#!/usr/bin/env bash
# new_film.sh <project-dir> [font-url]
# Scaffolds a film project from the skill's template, installs Playwright + Chromium locally, and fetches a brand font.
# font-url: a .ttf/.otf to use as the Brand face (default: Plus Jakarta Sans, a variable geometric sans from Google Fonts).
set -euo pipefail
K="$(cd "$(dirname "$0")/.." && pwd)"
DIR=${1:?usage: new_film.sh <project-dir> [font-url]}
FONT=${2:-https://github.com/google/fonts/raw/main/ofl/plusjakartasans/PlusJakartaSans%5Bwght%5D.ttf}
if [ -e "$DIR/comp.html" ]; then echo "$DIR already has a comp.html; not overwriting"; exit 1; fi
mkdir -p "$DIR"/{assets,fonts,stills,out,src,shots,masks}
cp "$K"/template/{comp.html,timeline.js,render.mjs,soundtrack.mjs,mix.sh} "$DIR"/
chmod +x "$DIR/mix.sh"
cd "$DIR"
[ -f package.json ] || printf '{\n  "name": "film",\n  "private": true,\n  "type": "module",\n  "dependencies": {}\n}\n' > package.json
npm install --silent playwright >/dev/null
npx --yes playwright install chromium >/dev/null 2>&1 || npx playwright install chromium
if [ -f "$FONT" ]; then cp "$FONT" fonts/Brand.ttf; else curl -sfL -o fonts/Brand.ttf "$FONT" || echo "font download failed: put a .ttf at fonts/Brand.ttf"; fi
echo "Film project ready at $(pwd)"
if [ -f ../score-log.tsv ]; then echo "Scores this brand's films already use (pick a different STYLE in soundtrack.mjs):"; tail -n +2 ../score-log.tsv | tail -5 | awk -F'\t' '{printf "  %-24s %-10s key %s  %s BPM\n",$1,$2,$3,$4}'; fi
echo "Next: edit comp.html (scenes), timeline.js (pacing), soundtrack.mjs (cues), then:"
echo "  node soundtrack.mjs && node render.mjs stills 1 3 6 && node render.mjs beats && node render.mjs --draft"
echo "  then the blind critic, then: node render.mjs --blur 8 && ./mix.sh film && $K/scripts/qc.sh out/film.mp4 1080x1920 30"
