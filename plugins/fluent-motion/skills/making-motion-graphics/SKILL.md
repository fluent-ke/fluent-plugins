---
name: making-motion-graphics
description: Use when making a motion-graphics video - an animated promo, launch film, event hype reel, social video ad or kinetic-type clip - from whatever the user supplies - posters, logos, photos, footage, a reference video to match, or just a brief. Also use to re-time, re-score or re-cut a film made this way.
license: MIT
metadata:
  author: fluent
  version: "0.2"
---

# Making motion graphics

Build the film in code: a canvas composition rendered frame by frame in headless Chromium (several pages in parallel), an original score synthesised to the same beat grid, optional 3D plates from Blender, and ffmpeg to put them together. Everything is timed in beats, so picture and sound stay locked and any scene can be slowed without re-animating it. The result looks like After Effects work and is fully reproducible.

`K` below is this skill's folder. Needs Node 18+, ffmpeg, Python 3 with Pillow; `new_film.sh` installs Playwright and Chromium into the project. On macOS, `swift` adds subject mattes.

## Tool routing

| Input or job | Tool | Details |
|---|---|---|
| New film | `$K/scripts/new_film.sh <dir> [font.ttf or url]` | scaffolds `comp.html`, `timeline.js`, `soundtrack.mjs`, `render.mjs`, `mix.sh` |
| Poster, flyer, brand sheet | `asset_tools.py crop / key / sample / palette` | cut logos out as supplied: `key` when the mark sits on a flat colour; on a photo or gradient, crop inside the card and draw with `img(…,{r})`. `sample` reads a brand colour from a headline or button |
| Reference video to match | `study_reference.sh <video>` | cut times, average shot length, one frame per shot |
| Footage to use in the film | `prep_footage.sh <src> <SHOT> <start> <end> [slow]` | frame sequence for `SHOTS` in comp.html |
| A 3D shot (logo that assembles, product turn, swarm) | `blender -b -P $K/scripts/blender_plate.py -- still\|anim …` | [3d.md](references/3d.md) |
| Text behind a person, product die-cut | `swift $K/scripts/segment.swift person\|cutout …` (macOS) | [motion.md](references/motion.md) |
| Scenes and effects | comp.html helper library | [motion.md](references/motion.md) |
| Story, pacing, copy | — | [storyboard.md](references/storyboard.md) |
| Music, sync, a licensed track | `soundtrack.mjs`, `mix.sh` | [score.md](references/score.md) |
| Checking the audio | `audio_check.py <file>` | levels, LUFS, silence, clipping, flat mix |
| Checking the finished film | `$K/scripts/qc.sh out/<name>.mp4 1080x1920 30` | spec, BT.709 tags, dead holds, loudness and true peak, contact sheet |
| Voiceover, captions | vendor TTS or `media-use`; `words()` in comp.html | [voice-captions.md](references/voice-captions.md) |

## Steps

1. **Intake.** Read everything supplied: every image, the brief, any linked page or folder of context. Study each reference video with `study_reference.sh` and read its sheet. Where the film states a fact (date, price, prize, venue, offer, deadline), find its source and check it is still true today; a closed registration or a passed date changes the film's goal and call to action. Where sources disagree (or a brief contradicts its own date), put only the consistent part on screen and carry the conflict to the user. Done when you hold a fact list with a source for each line, the brand colours and fonts, and the asset list.
2. **Decide.** Settle with the user what the film must make the viewer do, the format (9:16 for Reels/TikTok/Status, 4:5 feed, 16:9 LinkedIn/screens) and the length. Ask only what the material cannot answer; recommend a default for each. Done when goal, format and length are agreed.
3. **Storyboard.** Write the beat sheet per [storyboard.md](references/storyboard.md): scenes, the words on screen, beats per scene, where the music hits. Show it to the user in a few lines. Done when every on-screen word traces to the fact list or the user's own copy.
4. **Build.** `new_film.sh`, then write the scenes in `comp.html` (and set `CUTS` to their end beats), the pacing in `timeline.js`, and the cues in `soundtrack.mjs` (every cue as `M(comp beat)`). Brand marks go in as cropped image files, drawn at their own proportions.
5. **Look.** `node soundtrack.mjs && node render.mjs stills b2 b5.5 …` (`bN` is comp beat N; plain numbers are seconds) at one moment per scene plus each text's settled state (each run replaces `stills/`); tile them with `python3 $K/scripts/asset_tools.py sheet out/stills-sheet.png stills/*.png` and read the sheet. `node render.mjs --draft` renders the whole film at half size with the score muxed in (out/draft.mp4, well under a minute) to check timing against the music. Fix, re-render stills, read again. Done when every scene passes the checks in [storyboard.md](references/storyboard.md#still-checks).
6. **Render and mix.** `node render.mjs && ./mix.sh <name>` (render splits the film across the performance cores; `--workers N` to change, `--png` for lossless capture); variants with `--query` and `--out`. `mix.sh` writes the master, a posting copy and a WhatsApp copy under 16 MB. Run `$K/scripts/qc.sh out/<name>.mp4 1080x1920 30`, read its contact sheet, and grab frames around each cut. Done when QC passes and the cut frames look right.
7. **Deliver.** Open the posting copy in the user's default player (`open` on macOS, `xdg-open` on Linux, `start` on Windows). Say where both files are, what each variant is for, and anything unverified (facts, font substitutions, the score you could not hear). Put the files in the user's project folder when they have one.

## Related skills (use them if installed)

Reach for these for depth; this skill stays the pipeline. `kinetic-typography` and `motion-design` (timing and easing tables), `animation-principles`, `beat-sync-editing`, `shot-composition` (safe areas), `motion-art-direction`, `logo-animation`, `color-motion`, `ad-creative-video` (hook→CTA structure, variants), `anidoodle` (code-drawn illustration styles and composed scores), HyperFrames (`hyperframes`, `media-use` for TTS, music and SFX). If one is missing, carry on without it.

## Revisions

Slower or faster: change the factor for that scene's segment in `timeline.js`; the animation stretches and the score follows. Different music: see [score.md](references/score.md). Keep the film's folder as the source of truth and re-render; never patch the mp4.

## Common mistakes

| Mistake | Fix |
|---|---|
| Text leaves before it can be read | Hold rule in [storyboard.md](references/storyboard.md#reading-time); stretch the segment, keep the entrance snappy |
| Redrawing a logo in the film's font | Crop it from the supplied artwork (`asset_tools.py crop`, then `key` if it sits on a flat colour) |
| A fact from memory or an old brief | Re-check the live source on the day; film the answer, cite it when delivering |
| Calling the render done from the log | Read the stills sheet and the frames around each cut |
| "The music sounds good" | You cannot hear it: report `audio_check.py` numbers and invite a listen |
| Hits drifting off the beat after re-timing | Segment boundaries land on whole music beats; cues written as `M(c)`, never raw seconds |
| `Math.random()` or `Date` in comp.html | Seeded `rng()` and `t`: every frame must render the same twice |
| State carried between frames in comp.html | Parallel rendering gives each page a different range of frames, so anything not derived from `t` breaks between chunks |
| A CTA as a plain line of text | `cta(label,x,y,beat,tapBeat)`: a button with an arrow, a tap, and a hold of 3 s or more |
| Captions all one colour | The key phrase of each line in the accent, via `words()` |
