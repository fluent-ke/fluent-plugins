# Storyboard and pacing

## Shape of a short film

A 15–40 s social film is a handful of scenes, each carrying one idea. The shape that has worked:

| Scene | Job | Typical length |
|---|---|---|
| Hook | Kinetic words, one per beat, colours flipping: the problem or the promise in 3–5 words | 2 s |
| Name | The product, event or brand lands (slam or reveal), with its one-line promise | 3–4 s |
| Proof | What it is: features, the problems it solves, footage of the product in use | 2–3 s per item |
| Stakes | The number: price, prize, date, stat, as a counter or a big slam | 3–4 s |
| When and where | Dates, place, how to get it | 3–4 s |
| End card | Name, partner logos as supplied, one call to action | 4–5 s |

That table runs 18–25 s before reading time. For 15 s or less keep four scenes: hook, name, stakes, and an end card that carries when and where. Cut scenes the material does not support; add a proof item only when it has a fact behind it.

## The look

Without a look to follow, a model falls back on the same film every time: centred text on a gradient, every element fading in, a logo at the end. Agree the look in step 2 and write it down before the beat sheet:

- **A reference.** A video the user likes: run `study_reference.sh`, read its sheet, and name what to take from it (cut rhythm, type treatment, colour moves, transitions). Stills from the user's inspiration folder work too.
- **A named style.** When there is no reference, pick one and write it out in four lines, from the brand: *palette* (ground, ink, one accent, and where the accent goes), *type* (family, weights, case, tracking), *motion signature* (the one move that recurs: slams with echoes, lines rising out of slots, one shape morphing between states, hard cuts on the beat), *texture* (grain, glow, flat, paper).

Every scene then answers to the look. Name it in the beat sheet's first line so the critic can judge against it.

## Beat sheet

Write it before any code. One line per scene: comp beats, on-screen words, motion, music cue.

```
b0–4    MONEY / STILL / STOPS AT / THE BORDER.   one word per beat, slam into a line   stab + kick per word, impact on 3
b4–12   corridor map, then BORDERLESS KENYA.     arcs draw one per beat, title slams    groove in, impacts on title words
b12–23  5 PROBLEMS. then one card per problem    card slides in, text rises line by line   breath on header, arp under cards
…
```

Author every scene at its natural kinetic speed (about 1 comp beat per action), then give reading scenes their time in `timeline.js`.

## Scene briefs

A film of more than about six scenes can be built in parallel: one worker agent per scene, each writing a function `S_name()` in `scenes/name.js`, loaded with a `<script src="scenes/name.js">` after the main script in comp.html (the helpers are globals, so a scene file uses them directly), and called from `scene()` inside its `if(b<end)` block. Write that skeleton (every call, `CUTS`, `timeline.js`) and a stub file per scene before dispatching, so each worker can render its scene from the start. Each worker gets this brief and nothing else, so everything it needs is in it:

```
<scene> S3 "Stakes", comp beats 12–16, 9:16. Look: <the four look lines>. Brand: C = {…}, font Brand 400/800.
<words> The on-screen words, exactly, with the key phrase marked. </words>
<rules> Pure render(t): seeded rng(), no Date, no state between frames. Helpers from comp.html only.
  Text and logos inside the safe area (SKILL.md): top 250 px, bottom 350 px, sides 60–100 px clear. Frame 0 of the scene carries content. </rules>
<structure> Beat by beat: b12 number counts up · b13.5 lands (shock + sparks) · b14 label rises · b15–16 hold. </structure>
<motion> The look's motion signature. Springs with a small overshoot; entrances 0.3–0.5 beat, exits faster. </motion>
<export> Render stills at each beat of the scene with `node render.mjs stills --into S3 b12.5 b13.5 …`, read them, fix, and return
  the function plus the stills paths. </export>
```

The main agent owns comp.html, `CUTS`, `timeline.js` and the score, merges the scene files, and runs the beat sheet and critic on the whole film.

## Reading time

Once a piece of text has finished animating in, it stays still and on screen for at least **0.3 s per word + 1 s** (a 6-word card: about 3 s). A dense card or a number with a label needs more. Kinetic single words are exempt: they are felt, not read.

`timeline.js` sets this per scene: a factor of 2 doubles the scene's length. A factor slows **everything** in its segment, entrances included, so a word pop inside a 2.5× segment plays in slow motion. Put the entrances in a factor-1 segment and follow it with a separate hold segment that carries the stretch. Tune factors so each segment ends on a whole music beat (`MUSIC_BEATS` is the total; `node -e "import('./timeline.js').then(()=>console.log([12,23].map(toMusic)))"` checks boundaries).

## Copy on screen

- Every fact on screen traces to a source in the fact list. A date word that expires (TOMORROW, TONIGHT, LAST DAY) becomes a variant: render one cut per day with `--query` and read it with `Q.get()` in comp.html.
- Short lines: 2–6 words for slams, up to about 9 per line for reading scenes. Sentence case for reading, capitals for slams.
- One call to action, and only one the viewer can act on today. When sign-ups have closed, the end card says what happens next instead.
- The user's own words (tagline, poster lines) beat invented ones. A line you wrote is a suggestion; say so when delivering.

## Still checks

Read the stills sheet for each scene and fix before the full render:

- Frame 0 carries content (a word already on screen, the plate, a shape): it is the thumbnail and the first thing a scrolling viewer sees. Start the first entrance at b0 with most of it already in, or put a still element under it.
- Nothing touches or crosses the frame edge unless it is meant to bleed; keep 60 px of margin on text.
- In 9:16, keep text and logos inside the safe area (SKILL.md): the top 250 px and bottom 350 px sit under platform UI, and sides need 60 px (100 px for logos and key words). Check with `--query safe=1` stills.
- Content fills the frame: a scene with its content packed into one half gets re-centred or scaled.
- Text over footage has a scrim, shadow or matte so it reads on every frame.
- Brand marks are sharp, in proportion, and on a background the brand allows.
- The settled state of each text is on screen long enough (stills at the start and end of the hold).
- On out/beats-sheet.png, every tile in a kinetic scene differs from the one before it. Identical neighbours belong only to reading holds, and a hold still has something alive in it (a slow push-in, a drifting field, the CTA arrow).
- The look is the agreed one: set a tile beside the reference sheet, or check it against the four look lines.
