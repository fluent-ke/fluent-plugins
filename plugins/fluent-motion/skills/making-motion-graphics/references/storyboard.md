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

## Beat sheet

Write it before any code. One line per scene: comp beats, on-screen words, motion, music cue.

```
b0–4    MONEY / STILL / STOPS AT / THE BORDER.   one word per beat, slam into a line   stab + kick per word, impact on 3
b4–12   corridor map, then BORDERLESS KENYA.     arcs draw one per beat, title slams    groove in, impacts on title words
b12–23  5 PROBLEMS. then one card per problem    card slides in, text rises line by line   breath on header, arp under cards
…
```

Author every scene at its natural kinetic speed (about 1 comp beat per action), then give reading scenes their time in `timeline.js`.

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
- In 9:16, keep text inside the middle 1080×1420: the top 250 px and bottom 250 px sit under platform UI.
- Content fills the frame: a scene with its content packed into one half gets re-centred or scaled.
- Text over footage has a scrim, shadow or matte so it reads on every frame.
- Brand marks are sharp, in proportion, and on a background the brand allows.
- The settled state of each text is on screen long enough (stills at the start and end of the hold).
