# Score and sync

## The synthesised score

`soundtrack.mjs` writes `score.wav`: an original track built from oscillators and noise, so there is nothing to license. It reads the tempo and scene timing from `timeline.js`.

- `STYLE`: `afrohouse` (kick, clap, congas, offbeat sub bass, filtered pads; 118–124 BPM), `amapiano` (log drum lead, shakers; set `BPM` to 108–114), `ambient` (no drums: pads, bass, marimba arp; for corporate or calm films).
- `CH`: four chords, one per bar, as MIDI notes. The default is A minor (Am9, Fmaj9, Dm9, Em7). Transpose every number by the same amount to change key; swap in major chords for a brighter film.
- `groove(from,to,opts)`: the beat between two music beats. Thin it for quiet scenes (`k:false` drops the kick, `bs:false` the bass), open the filter with `cut` (700 muffled, 1300 warm, 3000 bright), `arp:true` for the marimba line under reading scenes.
- FX: `revCrash(T(M(c)))` + `impact` or `crash` on every cut, `riser` into every reveal, `stab`, `mar`, `tick` for small hits, `kick` alone for punctuation.

Arc that works: sparse intro hits on each word, groove in as the title lands, a breath (drums out) before the big number with a riser into it, full groove to the end card, one final hit and a tail.

## Sync

Write every cue as `M(comp beat)`, never raw seconds, so re-timing a scene in `timeline.js` moves its sounds with it. Keep segment boundaries on whole music beats (`toMusic(c)` prints them); a hit that lands between beats sounds late.

## Checking what you cannot hear

Run `audio_check.py` on `score.wav` and on the final mp4 (1-second windows by default; a one-beat breath needs them):

- Sections meant to be quiet read quieter. A **FLAT** warning means something dominates: usually the kick (lower its gain or shorten its decay) or a voice with a runaway length.
- No **SILENT** windows except the fade-out; no **CLIPPING**.
- The final file is near -14 LUFS. `score.wav` is written hotter (around -10) on purpose; `mix.sh` normalises it.

Then tell the user the numbers and ask them to listen: taste is theirs.

## Using a licensed or supplied track

1. Find its tempo and the time of its first downbeat (ask, read it from the track's page, or tap it out with the user).
2. Set `BPM` in `timeline.js` to the track's tempo and shape the segments so the scene changes land on its bar lines.
3. `./mix.sh <name> track.mp3 out/video-only.mp4 <seconds-to-first-downbeat>`. Skip `soundtrack.mjs`.

Only use music the user has the rights to post; trending sounds are added in the platform's own app instead.
