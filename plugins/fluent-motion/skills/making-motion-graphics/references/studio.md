# Talking-head studio

Seventeen effects for a person talking to camera, in `template/studio.js`. Almost all of them rest on one structure, the **sandwich**: the room, then a graphic, then the person cut out on top, so the graphic sits behind the speaker. Use them on the big lines of a [talking-head film](talking-head.md): one or two in a 15 s reel, two or three in 30 s or more; between them, plain cuts and punch-ins carry the voice.

## Setup (once per shot)

1. **Frames:** `cut_interview.py` or `prep_footage.sh` (shots/NAME/0001.jpg …).
2. **Mattes:** `swift $K/scripts/segment.swift person shots/NAME masks/NAME` (macOS, Apple Vision; on Linux or Windows make the same per-frame alpha PNGs with rembg or Robust Video Matting). Set `mask: true` on the shot in `SHOTS`.
3. **Measure it:** `python3 $K/scripts/shot_check.py shots/NAME masks/NAME`, run from the film folder, writes `shots/NAME.info.js` (head top, head centre, neck, shoulder line, the room's drift) and prints which effects the shot supports: **OK**, **CHECK** (works, read the note) or **SKIP** (it would look fake; pick another effect). Add `--clean` for vertigo: it also writes `assets/NAME_clean.png`, the room with the person removed; list it in `SRC` as `NAME_clean`.
4. **Load it:** in comp.html, after `<script src="studio.js"></script>`, add `<script src="shots/NAME.info.js"></script>` (the template has a comment where it goes).
5. **Reuse a shot** in several scenes with an alias: `TALK2: {at: 24, n: 150, mask: true, dir: 'TALK'}` reads TALK's frames, mattes, measurements and clean plate.

Needs numpy and Pillow (`pip install numpy pillow`).

The foundation every effect uses, also yours to build with:

| Helper | Does |
|---|---|
| `head(k)` | the speaker on this frame: `top`, `cx`, `neck`, `sh` (shoulder line), `x0`/`x1`, `hh` (head height), `cy`, `chest` [x, y], and the room's drift `dx`/`dy` |
| `sandwich(k, behind, {s, x, y, front})` | room → `behind()` → person → `front()`; `s/x/y` move room and person together |
| `pinned(k, draw)` | draws on the wall: follows the room's drift when the camera moves |
| `cleanRoom(k, s, x, y)` | the room with the person removed (from `--clean`) |
| `glass(x, y, w, h, {r, blur, tint})` | a frosted card over whatever is drawn so far |

## The seventeen

| # | Effect | Call | Kind | Details |
|---|---|---|---|---|
| 01 | Orbit: cards circling the speaker, behind and in front | `orbit` | wall | [studio-walls.md](studio-walls.md#orbit-cards-circling-the-speaker) |
| 02 | Couch wall: the wall becomes a feed of cards rising from behind | `couchWall` | wall | [studio-walls.md](studio-walls.md) |
| 03 | UI world: an app screen over the top, the speaker in front of it | `uiWorld`, `uiType`, `uiBubble` | screen | [studio-screens.md](studio-screens.md) |
| 04 | Frame break: the film shrinks to a post card, the head breaks out of it | `frameBreak` | screen | [studio-screens.md](studio-screens.md) |
| 05 | Digital zoom: word-timed creeps, snaps and whips on the face | `faceZoom` | camera | [studio-looks.md](studio-looks.md#facezoom-the-digital-zoom) |
| 06 | Phone mockup: a drawn phone in perspective with taps | `phoneMockup` | screen | [studio-screens.md](studio-screens.md) |
| 07 | Checklist: a glass card behind the speaker ticks off | `checklist` | wall | [studio-walls.md](studio-walls.md) |
| 08 | Headline wall: cards saying one thing, a highlighter on the key word | `headlineWall` | wall | [studio-walls.md](studio-walls.md) |
| 09 | Zoom-through cut: a dive into the speaker that becomes the next shot | `zoomThroughCut` | camera | [studio-looks.md](studio-looks.md#zoomthroughcut-the-zoom-through-cut) |
| 10 | Chart grow: a line chart on the wall kicks up on a word | `chartGrow` | wall | [studio-walls.md](studio-walls.md) |
| 11 | Pull-back reveal: the film becomes a card in an app window with its steps | `pullBack` | screen | [studio-screens.md](studio-screens.md) |
| 12 | Green screen: the speaker small at the bottom, your media behind | `greenScreen` | screen | [studio-screens.md](studio-screens.md) |
| 13 | Paper cut: the room tears into paper, the speaker a cut-out, ransom-note words | `paperCut` | look | [studio-looks.md](studio-looks.md#papercut-the-paper-cut-out-collage) |
| 14 | Doodle boil: a boiling chalk outline and doodles | `doodleBoil` | look | [studio-looks.md](studio-looks.md#doodleboil-chalk-outline-and-doodles) |
| 15 | Vertigo: the room stretches away, the speaker stays put | `vertigo` | camera | [studio-looks.md](studio-looks.md#vertigo-the-dolly-zoom) |
| 16 | Cover story: the shot becomes a magazine cover, masthead behind the head | `coverStory` | screen | [studio-screens.md](studio-screens.md) |
| 17 | Glass type: one word in clear glass on the wall, bending the room | `glassType` | wall | [studio-walls.md](studio-walls.md) |

Each effect draws the whole frame for its beats, so call it in place of `plate(k)` in that scene.

## Rules

- **Only what the speaker gave you.** Covers, headlines, charts and screens show the user's own media, words and numbers; never invented views, sources, handles or figures.
- **Respect the refusals.** When `shot_check.py` says SKIP, or an effect returns `false`, pick another effect rather than forcing it: `force: true` exists for testing.
- **One or two in a 15 s reel, two or three in a longer film**, each on a line that earns it, and each from a different kind (wall, screen, camera, look). Log them in `FILM.transitions` as `studio:orbit`, `studio:paperCut` …, so the brand's next film reaches for others.
- **Every effect takes `(k, a, z, opts)`** and draws the plain shot outside a…z. `z` may run past the scene's end beat when the next scene should cut in while the graphic is still up.
- **Only the words you pass.** Labels that would add words (`handle`, `issue`, `listLabel`, `timeLabel`, the pull-back counter `label`, the checklist `footer`) are off or nullable: set them to `null`/`false` when the copy is fixed.
- **Safe area** still applies: the graphics sit in the top third and around the head; captions stay inside the safe area ([SKILL.md](../SKILL.md#safe-area)).
