# Score and sync

## The synthesised score

`soundtrack.mjs` writes `score.wav`: an original track built from oscillators and noise, so there is nothing to license. It reads the tempo and scene timing from `timeline.js`.

- `STYLE`: `afrohouse` (kick, clap, congas, offbeat sub bass, filtered pads; 118–124 BPM), `amapiano` (log drum lead, shakers; set `BPM` to 108–114), `benga` (Kenyan benga over a house kick: a muted 16th-note guitar arpeggio on the left, a chattering lead guitar on the right when `arp:true`, a walking eighth-note bass, D major; 118–128 BPM), `drill` (Nairobi drill: half-time drums, triplet hat rolls, sliding 808s, a buzzy nyatiti-like lyre riff, brass stabs; minor key, 118–144 BPM), `ambient` (no drums: pads, bass, marimba arp; for corporate or calm films; 80–100 BPM).
- A style the last few films used sounds generic to the client even when it is good. Rotate styles across a brand's films, and when one is asked for "not generic", reach for a local form (benga, or build one on `pluck()`: a kora-like harp line, a nyatiti-like lyre ostinato) before a global one.
- `CH`: four chords, one per bar, as MIDI notes. The default is A minor (Am9, Fmaj9, Dm9, Em7). Transpose every number by the same amount to change key; swap in major chords for a brighter film.
- `drill` voices: `e808(t,note,len,gain,fromNote)` (sliding 808), `dkick`, `dsnare`, `dhat`, `lyre(t,note,gain,pan,len)` (buzzy nyatiti-like pluck), `brass(t,notes,gain,len)` (stab for big hits). In `groove()`, `cg`/`arp` turn the lyre riff on for drill.
- `pluck(t,note,gain,pan,{bright,mute,len})`: a plucked string (Karplus-Strong). Muted and dark for rhythm parts, bright and longer for leads.
- `groove(from,to,opts)`: the beat between two music beats. Thin it for quiet scenes (`k:false` drops the kick, `bs:false` the bass), open the filter with `cut` (700 muffled, 1300 warm, 3000 bright), `arp:true` for the marimba line under reading scenes.
- FX: `revCrash(T(M(c)))` + `impact` or `crash` on every cut, `riser` into every reveal, `stab`, `mar`, `tick` for small hits, `kick` alone for punctuation.

Arc that works: sparse intro hits on each word, groove in as the title lands, a breath (drums out) before the big number with a riser into it, full groove to the end card, one final hit and a tail.

## Every film gets its own music

A score heard on the last film makes the new one feel like a rerun, even when the score is good. So each film gets a different track:

1. **Before writing cues, read the log.** `new_film.sh` prints the last scores from `score-log.tsv` in the folder that holds the brand's films (keep each brand's films as sibling folders under one brand folder, so a brand's first film starts its log there); `soundtrack.mjs` updates it on every run and prints a ⚠ when this film's `STYLE` matches either of the brand's last two films.
2. **Change the style first.** Rotate through `afrohouse`, `amapiano`, `benga`, `drill`, `ambient`, and prefer the one that fits the film's story (chaos into order suits drill's breakdown and drop; warm lifestyle suits amapiano or benga; a calm explainer suits ambient).
3. **Change the key and feel too.** `KEY` transposes everything (-5…+6); a different tempo range, a new chord progression in `CH`, or new riff notes make even a returning style a new track.
4. **When all five are spent, make a new one** from the voices on hand (`pluck()`, `lyre()`, `e808()`, `logdrum()`, `brass()`, `pad()`): a kora-like harp line, an ohangla-style drum pattern, a taarab-flavoured string pad. Add it as a new `STYLE` so the next film can use it too.
5. When delivering, name the track's style and key, and say it differs from the brand's last film.

## Sync

Write every cue as `M(comp beat)`, never raw seconds, so re-timing a scene in `timeline.js` moves its sounds with it. Keep segment boundaries on whole music beats (`toMusic(c)` prints them); a hit that lands between beats sounds late.

## Checking what you cannot hear

Run `audio_check.py` on `score.wav` and on the final mp4 (1-second windows by default; a one-beat breath needs them):

- Sections meant to be quiet read quieter. A **FLAT** warning means something dominates: usually the kick (lower its gain or shorten its decay) or a voice with a runaway length.
- No **SILENT** windows except the fade-out; no **CLIPPING**.
- The final file is near -14 LUFS. `score.wav` is written hotter (around -10) on purpose; `mix.sh` normalises it.

A spectrogram shows what the numbers cannot: `ffmpeg -i score.wav -lavfi showspectrumpic=s=1400x500:legend=0:fscale=log:stop=6000 spec.png`, then read the image. Pitched parts show as horizontal harmonic lines; a solid block across the low end means the bass is too loud or too long.

Then tell the user the numbers and ask them to listen: taste is theirs.

Stacked hits on one beat (impact + kick + crash + stab on the drop) are the usual cause of **CLIPPING**: lower the impact first.

## Using a licensed or supplied track

1. Find its tempo and the time of its first downbeat (ask, read it from the track's page, or tap it out with the user).
2. Set `BPM` in `timeline.js` to the track's tempo and shape the segments so the scene changes land on its bar lines.
3. `./mix.sh <name> track.mp3 out/video-only.mp4 <seconds-to-first-downbeat>`. Skip `soundtrack.mjs`.

Only use music the user has the rights to post; trending sounds are added in the platform's own app instead.

## Other sources of music

| Source | Use | Terms (check on the day) |
|---|---|---|
| ElevenLabs Music (API, paid plans) | A generated bed cleared for ads | Paid plan; check the plan's exclusions |
| Google Lyria (Vertex AI / Gemini API) | Generated bed, watermarked with SynthID | Paid access |
| Magenta RealTime 2 (local, CC-BY) · ACE-Step 1.5 (local, MIT) | Textures and stems to layer under the synthesised score | Credit Magenta; check ACE-Step's weight licence |
| Stable Audio Open | Textures | Free commercial use only under USD 1M revenue, registration required |
| Freesound (CC0 filter), Kenney (CC0), Sonniss GDC bundles | One-shot hits, risers, foley | Keep a list of every sample's URL and licence beside the film |

Avoid for client work: MusicGen/AudioCraft weights (non-commercial), Udio (downloads disabled), Mubert's Creator plan (excludes ads). Suno's paid plans grant use but no longer say you own the song. Pixabay tracks may trigger Content ID claims.
