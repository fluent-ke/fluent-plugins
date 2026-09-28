# Fluent Motion

Give your agent a poster, a logo, some footage, a video you like the look of, or just a brief, and it makes a motion-graphics film from it: kinetic type, animated logos and maps, counters, footage with text behind the subject, and an original soundtrack cut to the same beat. You get an MP4 ready for Reels, TikTok, WhatsApp Status, the feed or LinkedIn.

One skill, **making-motion-graphics**. The film is built in code (an HTML canvas rendered frame by frame in headless Chromium, then ffmpeg), so it is exact, repeatable and easy to change: "slow down the part with the dates" or "use a calmer sound" is one edit and a re-render.

## What it does

- Reads everything you supply and checks each fact it will put on screen against its source, on the day.
- Agrees the goal, format and length with you, then writes a beat sheet before any animation.
- Crops your logos and partner marks from the artwork you gave it rather than redrawing them.
- Composes an original score (afro-house, amapiano, Kenyan benga or ambient) to the film's timeline, or syncs to a track you have the rights to.
- Adds 3D shots from Blender when a logo, product or swarm needs real light and depth: rendered headless as transparent plates the film can move and write over.
- Ends on a call to action that reads as one: a button that pops in, gets tapped and holds.
- Renders across your CPU cores (about 2× faster), with a half-size draft for checking timing, and delivers a posting copy, a master and a WhatsApp copy under 16 MB, colour-tagged so hues hold after upload.
- Checks its own work: stills of every scene read before the full render, audio measured for level, silence and clipping, and a QC pass on the finished file (size, colour tags, dead holds, loudness, true peak, contact sheet).
- Renders variants from one source, such as a "TOMORROW" cut and a "TODAY" cut.

## Where it works

| App | What works |
|---|---|
| Claude Code: terminal, desktop app, IDE extensions | Everything |
| Codex: CLI, desktop app, IDE extension | Everything |
| Claude chat (web or desktop) and Cowork | Storyboards and the film's code; rendering needs a real computer |

It needs Node 18+, ffmpeg and Python 3 with Pillow. Subject cut-outs (text behind a person, product stickers) use Apple Vision and work on macOS only. 3D shots need Blender 4.2 or later (tested on 5.2).

## Install

Open Claude Code or Codex and paste:

> Install the Fluent Motion plugin by following https://github.com/fluent-ke/fluent-plugins/blob/main/plugins/fluent-motion/INSTALL.md

## Use

Start a new session in the folder with your material and say what the film is for:

> Make a 20-second vertical video for our event from the poster in this folder. People should want to come.

> Here is our product footage and logo. Make a 15-second launch ad in the style of reference.mp4.

## What's inside

```
skills/making-motion-graphics/
  SKILL.md                     the workflow: intake, decide, storyboard, build, look, render, deliver
  template/                    a working 12-second film to start from
    comp.html                  scenes and the helper library (kinetic type, key-phrase captions, reveals, pills, counters,
                               swipes, footage, shockwaves, sparks, the call-to-action button)
    timeline.js                pacing: stretches reading scenes while the music keeps its tempo
    soundtrack.mjs             the synthesised score, cued to the scenes
    render.mjs, mix.sh         frames to MP4 in parallel (or a quick draft), then audio in, loudness-normalised in two passes
  scripts/
    new_film.sh                start a film project from the template
    study_reference.sh         cuts, shot length and a contact sheet of any video
    prep_footage.sh            footage into frame sequences, with slow motion
    asset_tools.py             crop, key out backgrounds, brand palette, contact sheets
    audio_check.py             levels, loudness, silence and clipping, for an agent that cannot listen
    qc.sh                      checks the finished film: spec, colour tags, dead holds, loudness, true peak, contact sheet
    blender_plate.py           a 3D shot rendered headless to a transparent plate
    segment.swift              person mattes and subject cut-outs (macOS)
  references/                  storyboard and pacing, motion recipes, score and sync, 3D plates, voiceover and captions
```

## Licence

[MIT](../../LICENSE).
