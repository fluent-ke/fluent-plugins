# Edits

The edit kit in `template/edits.js`: the cuts, camera moves and effects that make a film feel edited rather than animated. Every helper is pure in time, so it re-times with the film and renders the same in parallel.

Frame counts below are at 30 fps. A beat at 120 BPM is 15 frames.

## How to use it

`edits.js` loads before comp.html's script (`new_film.sh` copies it in), so `montage()` can be called at the comp's top level. Three kinds of helper:

- **Wrapper:** `camera(keys, draw)` takes a function that draws the scene and films it.
- **Post edits** act on the frame drawn so far, so call them at the end of a scene's block, before `return`: `punch`, `shake`, `flash`, `leak`, `grade`, `letterbox`, `glitch`, `tilt3d`.
- **Transitions** are listed once in `TRANS` in comp.html: `[[cutBeat, kind, {opts}], …]`. `render()` applies them around each cut. List every cut in `TRANS` (`'cut'` for a plain one). `CUTS` drives only the old band `swipe()`; leave it empty unless the look wants band wipes.

Pick 3–5 **families** per film; record the transition **kinds** you use (whip, flood, punch…) in `FILM.transitions`:

| Family | Helpers |
|---|---|
| Camera | `camera`, `punch`, `shake`, `whip`, `zoom` |
| Speed | `SHOTS.X.ramp` |
| Light | `flash`, `leak`, `grade` |
| Graphic | `flood`, `iris`, `slice`, `split`, `grid`, `parallax`, `letterbox` |
| Time | `SHOTS.X.freeze` + `freezeCard`, holds |
| Glitch | `glitch` |

Two to four families is a style; six is noise. Never the same transition twice running, and no more than three of a kind in 30 s (the comp prints a ⚠ when `TRANS` breaks either). Glitch and flash appear in at most one film in three for a brand: the film log shows which.

## Camera

**Shot sizes and a moving camera.** `camera([[beat, size, focusX, focusY, rot], …], () => { …draw… }, {float})`. Sizes: `wide` 1, `medium` 1.35, `close` 1.8, `insert` 2.6, or any number. Each key starts its own spring at its beat, so a new key bends the move already under way; `w` sets the speed (9 snaps in about half a beat, 3–4 is a slow push). The focus point is kept inside the frame, so no edge ever shows. `float: 1` adds a hand-held drift; use it on reading holds so they stay alive.

- Lead the subject: key the camera about 0.1 s before what it follows moves.
- At least four different camera moves in a film: push, pull, a reframe, a snap to a close-up.
- Snapshot effects (`zoomBlur`, `warp`, `masked`, the post edits) work in frame space: call them outside `camera()`.

**Punch-in.** `punch(a, z, {to: 1.15, x, y})`: a hard cut to a tighter frame between beats a and z, on a key word or a hit. 110–120 % reads as a reframe; more reads as a zoom. Alternate in and out; punching on every sentence goes numb.

**Shake.** `shake(beat, {amp: .03, len: 10, rot: 1.5})`: an instant offset that decays over 8–12 frames. Impacts only: a slam, a drop, a stamp. Pair with `impact()`.

**Whip.** `TRANS: [c, 'whip', {dir: 1}]`: 10 frames across the cut, the blur peaking at the cut. Both shots should move the same way at a similar speed. Pair with `whoosh()` peaking on the cut.

**Zoom-through.** `TRANS: [c, 'zoom', {at: [x, y]}]`: the outgoing shot dives into a point (1 → 2.5×, radial blur), the incoming one settles out of it (2.5 → 1×). Aim at something dark or at the subject's centre. Pair with `whoosh()` and a `riser()` ending on the cut.

## Speed

**Speed ramp.** On the shot: `SHOTS.RUN = {at: 8, n: 240, ramp: [[9, 3], [10, .25], [11.5, 1]]}`. From each beat the footage plays at that speed (1 = real time), eased over 0.2 s. The pattern: normal → fast → slow on the key action → normal. Fast parts lose their natural blur, so render with `--blur 8`.

- Slow motion needs spare frames. Prep the shot with `prep_footage.sh … <slow>` (`slow` 4 interpolates 4× the frames) and treat speed 1 as 4× slow; or keep slow parts at 50 % or more on plain 30 fps footage.
- Pair: `whoosh()` into the fast part, `impact()` where it lands slow.
- Don't ramp footage with no motion in it (a talking head, a still product).

## Light

**Flash frame.** `flash(beat, {col, up: 2, down: 10})`: 2 frames up to near-white (#ebebeb, not pure white), 4–20 frames down. Or as a transition: `[c, 'flash']`. Never more than 3 flashes a second (photosensitivity).

**Light leak.** `leak(beat, {len: 24})`: warm light drifting across in screen blend for 15–30 frames. Once a film, on a warm or nostalgic moment.

**Grade.** `grade('teal-orange' | 'warm-film' | 'cool-night' | 'bleach' | 'mono' | 'punchy', {amt})`, or your own `{con, sat, bri, hi, lo, amt}`. Put it in `look()` in comp.html (it runs after every scene, so the whole film sits in one look); switch on `b` there to change the grade between sections and mark a turn (mono flashback, colour present).

## Graphic

**Flood.** `[c, 'flood', {col, from: [x, y], to: [x, y]}]`: a colour from the scene grows from `from` to fill the frame, the cut happens under it, and it recedes into `to` on the next scene's subject. Pick `from` on an element of the outgoing scene (a button, a dot, a letter's counter).

**Iris.** `[c, 'iris', {at: [x, y]}]`: the incoming scene opens in a circle from a point; the outgoing scene's last frame stays around it.

**Slice.** `[c, 'slice', {n: 5}]`: the incoming scene slides in as alternating bands.

**Split screen.** `split([() => plate('A'), () => plate('B')], beat, {dir: 'v'})`: panels slide in one after another. Two panels for before/after, three for options, four for a montage moment.

**Grid.** `grid(['p1', 'p2', …], beat, {cols: 3})`: a wall of photos or frames popping in per beat. Good for "all of these" moments and for a burst.

**Letterbox.** `letterbox(a, z)`: bars in for a cinematic stretch; take them out for the drop.

**Parallax photo.** `parallax('team', a, z, {push, lift})`: a still becomes a shot with depth. Needs `IMG.team` and its matte `IMG.team_m` (`swift $K/scripts/segment.swift cutout photo.jpg assets/team_m.png`, or `person` for people). Keep the move small (push .05–.1): a big move tears the edge of the cut-out.

## Time

**Freeze frame.** On the shot: `freeze: [[beat, 1.5]]` holds its frame for 1.5 beats. Then `freezeCard('RUN', beat, 1.5, {label: 'THE MOMENT', stroke: 14, col: '#fff'})` dims the room, pops the subject as an outlined sticker and lands a label (sized to fit). `sticker(k, {stroke, col, sc, x, y})` is the outlined cut-out on its own. Needs the shot's mattes (`mask: true`). Pair with `shutter()` and a dip in the score.

**The hold.** The strongest edit is often none: one shot, held, with a slow push. Every film has at least one (the rhythm gate checks for it).

## Glitch

`glitch(beat, {len: 3})` or `[c, 'glitch']`: 2–4 frames of displaced slices and a colour split. Tech and nightlife films only, at most twice. Pair with `zap()`. Not for calm or premium brands.

## Montage

```js
const MT = montage(['A', 'B:40', 'photo1', 'C', 'photo2'], 16, '2 1 1 .5 .5 .5 .5 2', {edits: ['cut', 'punch', 'zoom']});
// in scene(): if (b < MT.end) { MT.draw(); return }
```

The pattern is beats per cut: start slower, compress into a burst, land on a long one. `'B:40'` starts shot B at its frame 40 (an in-point). Each cut gets its own copy of the shot starting on that cut, so the list can repeat and a shot can still be used elsewhere. Edits: `cut`; `punch`, a 1.14× reframe halfway through the shot; `zoom`, a fast radial-blur settle into it; `flash` and `shake` too, but they count toward the flash and shake budget. Never the same edit twice running. Past its last frame any shot holds that frame. `MT.cuts` lists the cut beats; soundtrack.mjs cannot read them, so copy the ones that get a hit (the first and last of the burst, not every one) into the cue sheet. Don't name it `M`: the score uses `M()`.

## Sound for edits

In `soundtrack.mjs`, each at the cut's time `T(M(c))`:

| Edit | Sound |
|---|---|
| whip, zoom, slide | `whoosh(T(M(c)))`: peaks on the cut, starts 0.3 s before |
| ramp into slow, drop | `riser(T(M(c)) - len, len)` then `impact(T(M(c)))` |
| freeze | `shutter(T(M(c)))` and pull the groove out for the hold |
| glitch | `zap(T(M(c)))` |
| the breath before the drop | `tapeStop(T(M(c)) - .6, .6)`: the whole mix slows to a stop |

Fewer sounds than cuts: an effect on every cut becomes noise. Sound may lead a cut (a riser, a reversed crash) or run over it into the next scene.
