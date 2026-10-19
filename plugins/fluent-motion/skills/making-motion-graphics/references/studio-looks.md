# Studio: camera and stylised looks

Five talking-head effects in `studio.js` ([studio.md](studio.md) has the setup). Each call draws the whole frame for its moment, so it takes the place of `plate(k)` in the scene. All five are pure in time: the same beat always gives the same pixels. Beats are comp beats (`b`). Head positions come from `shots/NAME.info.js`. The effects use the shot's median head height and average the other measurements over a few frames, so they hold steady while the head moves.

---

## faceZoom: the digital zoom

**What the viewer sees.** The frame pushes in on the speaker's face in time with the words. It can creep in slowly, snap in hard with a short burst of radial blur, or whip back out with a motion smear. The face stays a little above centre, and the edge of the frame never shows.

**Use it** to land a key word with a snap, to build tension under a sentence with a creep, or to reset with an out after a punchline. It works on any talking shot that has measurements.

**Don't use it** on soft or low-resolution footage, where 1.6× shows the softness. Avoid more than one snap every couple of seconds, because it stops reading as emphasis. Don't stack it with `camera()` or `punch()` on the same beats.

**Call**
```js
faceZoom('TALK',[[1,'creep',1.18],[4,'snap',1.5],[6,'out'],[7,'snap',1.3],[8.5,'out']]);   // in place of plate('TALK')
```
- `keys`: `[[beat,'creep'|'snap'|'out',scale],…]` in beat order. `scale` is the absolute zoom. If you leave it out, creep adds 0.12, snap goes to 1.35 and out returns to 1.
  - `creep` eases to its scale until the next key, over 4 s at most.
  - `snap` lands in 5 frames.
  - `out` whips back in 7 frames.
- `{max=1.6}`: the cap. Every scale is clamped to the range 1 to max.
- `{draw}`: what gets zoomed. The default is `()=>plate(k)`. Pass a sandwich or a scene with text to zoom the whole picture.
- `{blur=1}`: multiplies the blur. The blur follows the speed of the zoom, so snaps and outs smear while creeps stay sharp.
- Returns the current scale.

**Shot needs.** Mattes are not required. It needs measurements (`SHOTINFO`) so it can find the face, and footage sharp enough to take a 1.6× crop.

**Sound.** Pair a snap with an **impact** or a **zap**, an out with a **whoosh** that peaks on the key beat, and a creep with a low **riser** under it.

---

## zoomThroughCut: the zoom-through cut

**What the viewer sees.** The camera seems to dive into the speaker's shirt. Over 9 frames the picture rushes in, the radial blur builds and a dark portal swells until the screen goes black. The next shot then opens out of that same point: a soft-edged hole grows from it while the new picture zooms down from 3.2× to 1× and its blur clears. Two shots become one move.

**Use it** for a hard cut between two takes, a jump in topic, or a "let's go deeper" moment. It suits shots where the speaker wears a dark top.

**Don't use it** more than once or twice a film. Avoid it when the chosen point is bright (a white shirt with no dark area): pass `into` to aim at something dark, or use a flood transition instead. Don't use it together with a TRANS entry on the same cut.

**Call.** It is a post edit, so call it after drawing, in both scenes around the cut. Always pass the *outgoing* shot:
```js
if(b<10){faceZoom('TALK',keys);zoomThroughCut('TALK',10);return}
if(b<20){plate('TALK2');zoomThroughCut('TALK',10);return}      // still 'TALK': the point is measured on the outgoing shot at the cut
```
- `{into}`: `[x,y]`, the point to dive through. The default is `head(k).chest` at the cut: the middle of the chest, about 0.6 of a head height below the shoulder line.
- `{len=9}`: frames on each side of the cut.
- `{depth=3.2}`: how far the dive zooms.
- `{col='#07070a'}`: the portal's colour.
- Returns true while it is active.

**Shot needs.** Measurements on the outgoing shot, unless you pass `into`. No mattes. The incoming scene can be anything, including graphics.

**Sound.** A **whoosh** that peaks on the cut, with an **impact** or a sub drop on the cut beat itself. A short **riser** over the 9 frames before the cut helps.

---

## paperCut: the paper cut-out collage

**What the viewer sees.** Torn sheets of coloured paper slide in over the room one after another, until the room is gone. The sheets have jagged white torn edges, a faint fibre texture and drop shadows. The speaker becomes a cut-out with a thick white edge and a shadow. The cut-out jitters at 12 fps like stop-motion. The author's words then slam down one letter at a time as a ransom note, with each letter on its own scrap of paper in its own font, colour, case and tilt. At `z` the paper backdrop rips down the middle, the rip opening from the top. The halves swing off to the sides, and the speaker turns back into normal footage in front of the real room.

**Use it** for a playful or punk aside, a "here's the headline" moment, or a list of rules. Brand colours can go in `palette`.

**Don't use it** for serious or sensitive content, or for long sentences: keep to 1 to 4 short words of about 14 letters. Avoid it on shots where the matte is ragged (hair, motion blur), because the white edge outlines every flaw.

**About the 12 fps step.** The footage itself still plays at 30 fps. The effect can't hold an earlier frame: only the current frame is loaded, and SHOTS can't take a step option. Instead, each 1/12 s step gives the cut-out a new seeded nudge (up to ±3.5 px) and tilt (up to ±0.6°). That reads as stop-motion.

**Call**
```js
paperCut('TALK2',11,17,{words:'say it LOUD'});    // in place of plate('TALK2'), from a to z+tear
```
- `a`: the beat the sheets start. The letters start at a+0.75, one every 0.075 beat.
- `z`: the beat the tear starts. The effect runs until `z+tear`, and outside a…z+tear it draws `plate(k)`.
- `{words}`: the text. Each letter's case is random (75% upper case).
- `{palette}`: sheet colours, used in order.
- `{seed=4}`: changes every tear, tilt and letter.
- `{sheets=4}`: 3 to 5 sheets.
- `{y=H*.7}`: the centre of the text block (kept above the caption zone).
- `{letterCase='mixed'}`: ransom-note mixed case; `'upper'`, `'lower'` or `'as-is'` to keep the copy as written.
- `{size=150}`: letter size, shrunk to fit 88% of the width.
- `{tear=1}`: how long the rip takes, in beats.

**Shot needs.** Person mattes (the cut-out uses `sticker()`) and measurements. A plain room is fine, since the paper covers it.

**Sound.** A paper **whoosh** for each sheet, a **tick** or **shutter** for each letter (or every second letter), and a ripping **whoosh** into an **impact** on `z`.

---

## doodleBoil: chalk outline and doodles

**What the viewer sees.** A chalk line traces around the speaker's body and head, sweeping round in 0.8 beat. The line hugs the body with a small gap and is redrawn every 2 frames with a new jitter, the hand-drawn "boil" of the line and its grain. Chalk doodles draw themselves on along their paths at the given beats and boil too: stars, arrows, underlines, circles, rays, sparkles, spirals and hearts. At `z` an eraser rubs everything out in zig-zags, leaving a brief haze of chalk dust.

**Use it** for teaching, explainers, a "big idea" moment, or a playful or kids' register. Rays and a circle around the head make a good "lightbulb" beat.

**Don't use it** over a very bright, plain background (white walls, sky behind the head). The pale chalk gets lost there even with its soft shadow, so pass a darker `col` or don't use it. Avoid it on a shot with fast movement, because the outline follows the matte and smears.

**Call**
```js
doodleBoil('TALK3',20.5,28,{doodles:[['star',22,-1.15,-.55,.5],['rays',22.6,0,-.05,1.6],['circle',26.8,0,.15,1.9]]});
```
- `doodles`: `[[kind,beat,dx,dy,scale],…]`.
  - `dx`, `dy` are in head heights from the head centre (`dy` < 0 is above). The position is fixed where the head was at that beat.
  - `scale` is in head heights (1 = one head tall).
  - Kinds: `star arrow underline circle rays sparkle spiral heart`. Rays fan over the top of the head; at a scale of about 1.6 they clear it.
  - Each doodle draws on in 0.6 beat.
- `{col='#F4F1EA'}`: chalk colour.
- `{width=14}`, `{gap=12}`: the outline's thickness and its distance from the body, in px.
- `{seed=7}`: changes the boil.
- `{out=.7}`: how long the rub-out takes, in beats.
- Draws the plain plate outside a…z+out.

**Shot needs.** Person mattes and measurements. It reads best over a mid-toned or textured background.

**Sound.** A **tick** or a scratchy **zap** as each doodle starts and a soft **riser** under the outline sweep. A short **whoosh** works for the rub-out. Chalk squeaks are optional.

---

## vertigo: the dolly zoom

**What the viewer sees.** The speaker stays perfectly still, the same size and in the same place, while the room behind them stretches away (it grows to `amt` around the head). The room softens and darkens a little as it goes. It holds there, then springs back to normal at `z`. This is the "Vertigo" unease shot.

**Use it** for a realisation, a shock, or "and then it hit me". Use it once a film.

**Don't use it** on a shot whose clean plate is mostly guesswork. Stretching the room also stretches the filled-in hole where the person was, so the fake area spreads out around their shoulders. That is why it refuses unless the room is well covered.

**It refuses by default.** It draws the plain shot and returns `false` when `SHOTINFO[k].bg.plain` is true (there is nothing to see stretch), when `coverage` is below 0.8, or when there is no clean plate. `force:true` overrides the coverage and plain checks; it can't make up a missing clean plate. Check the return value if you want a fallback:
```js
if(!vertigo('TALK4',31,37))punch(31,37,{to:1.12});
```

**Call**
```js
vertigo('TALK4',31,37,{force:true});
```
- `{amt=1.33}`: how far the room stretches.
- `{ramp}`: how long the stretch takes. The default is 40% of a…z, at most 2 beats.
- `{blur=2.5}`: px of background blur at full stretch.
- `{dim=.22}`: how much the room darkens at full stretch.
- `{force=false}`.
- It springs back from `z` in about 1 beat.

**Shot needs.** Person mattes, measurements, and a clean plate (`assets/NAME_clean.png` in `SRC` as `NAME_clean`). The background must be textured and should have coverage of at least 0.8. A locked-off camera works best.

**Tested on TALK** (coverage 0.62, so with `force:true`). The trees and sky above the shoulders stretch convincingly. The lower third is the problem: the plate's filled-in body area turns into pale, streaky mush on both sides of the arms, and the orange chair arms disappear. The blur and dimming make it read as soft bokeh at phone size for a 1 to 2 s hit at 1.33, and 1.2 hides it better. On a still frame or a big screen it looks fake. The refusal rule is correct for this shot.

**Sound.** A long **riser** over the stretch (pitch rising), cut dead at the hold, then an **impact** or a reversed **whoosh** on the spring back.
