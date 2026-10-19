# Studio: screens and layouts around the speaker

Six effects in `studio.js` ([studio.md](studio.md) has the setup). Each effect draws the **whole frame** for its moment. Before beat `a` it shows the plain shot. It eases in from `a`, holds, and is back to the plain shot by beat `z`. Call one effect per scene block, with nothing else under it. Entrances and exits are timed in seconds, so a stretched timeline segment does not slow them. Pops inside an effect (bubbles, ticks, labels) are timed in beats.

All six effects need the shot's mattes (`masks/NAME`) and measurements (`shots/NAME.info.js` from `shot_check.py`). Layouts are anchored to the shot's **average** head top, shoulder line and head height (neck minus top), so they hold still while the head moves. They are tuned for a seated or standing medium shot with head and shoulders in frame and the head near the vertical middle. Everything is pure in time: the cold and warm renders of each test beat were byte-identical.

---

## uiWorld: the speaker in front of an app screen

**What the viewer sees.** A rounded app window (title bar, three dots, optional title) drops in over the top ~55% of the frame. At the same time the shot pushes down and scales up about 1.25×, so the head sits on the window's lower edge and the person stands in front of the screen. A band of the real room shows below. The window's content is yours. At `z` the window lifts away and the shot settles back.

**Use it** when the speaker is talking about something that happens on a screen: a chat, a prompt, a form, a dashboard.
**Don't use it** on a wide shot where the head is small, or when the content needs the whole window. The head covers the lower-middle of the window.

```js
uiWorld('TALK', a, z, {draw:(p, r)=>{…}, dark:false, title:'Assistant', s:1.25, top:250, h:830, overlap:.42})
```
- `draw(p, r)`: paints the content. `p` runs 0→1 across a…z. `r = {x, y, w, h}` is the content rect below the title bar. Keep content out of its lower-middle third, where the head sits.
- `dark`: dark window. `s`: push scale. `top` / `h`: window position and height. `overlap`: the share of head height that overlaps the window's bottom edge.
- Helpers to use inside `draw` (they follow the window's light/dark theme):
  - `uiType(text, x, y, a, cps=16, {size, col, w8, caret})` types `text` from beat `a` at `cps` characters a second, with an accent caret. The caret is solid while typing and blinks after. Text is left-aligned at x and centred on y. Returns the typed width.
  - `uiBubble(text, x, y, a, {me, size, maxW, bg, fg})` pops a chat bubble from its tail corner at beat `a`. With `me:true` it sits on the right in the accent colour (x = its right edge); otherwise it is grey on the left (x = its left edge). y = its top. Returns its height for stacking.

**Shot:** head and shoulders in frame, head top around 25–35% down.
**Sound:** whoosh as the window drops, a soft tick per bubble, and keyboard ticks under `uiType`.

---

## frameBreak: out of the post

**What the viewer sees.** The video shrinks over about 0.7 s into a floating card styled like a social post. The card has rounded corners, a white edge and a deep shadow. A handle row sits above it (avatar, handle, more-dots) and an action row below it (like, comment, share, save). Behind the card is a blurred, darkened copy of the room. The person is drawn with the same transform but is not clipped above the card or past its sides, so the head and shoulders rise over the top edge and the arms reach past the side. The person casts a soft shadow where they leave the card. At `z` the card grows back to full frame.

**Use it** for a "this is the post / this went viral / here's the clip" moment, or to make the speaker literally step out of the feed.
**Don't use it** when the person is small in frame or off to one side. Don't use it when their arms are tight to the body, because then nothing breaks the sides.

```js
frameBreak('TALK', a, z, {s:.68, x:50, y:-10, cw:null, bottom:1480, cut:.12, handle:null, dim:.55, r:34})   // handle: the account name shown above the card, only if you pass one
```
- `s`: picture scale inside the card. `x`/`y`: picture shift (the default x:50 moves the person right to free room for the handle; the right arm breaks out more).
- `cw`: card width (default 72% of the scaled frame width). `bottom`: card bottom edge. `cut`: where the card's top crosses the body, as a share of head height below the shoulder line.
- `handle`: keep it short (about 8 characters). The collar starts about 120 px right of the avatar. `dim`: backdrop darkness.

**Shot:** a medium shot, centred, head and shoulders in frame, arms away from the body.
**Sound:** whoosh on the shrink, a light impact as the card lands, and a reverse whoosh on the grow-back.

---

## phoneMockup: the app beside the speaker

**What the viewer sees.** A drawn phone flies in from the side, swings in perspective (a damped rotateY with a little overshoot) and then floats gently. It has a polished metal frame with real thickness (the side edge is visible), a highlight on the rim, a black bezel, a dynamic-island notch and a glass sheen that slides with the angle. Its screen shows your drawing, rendered offscreen at screen size and mapped in perspective. Taps show a grey press dot and then an accent ripple. A soft shadow falls on the room. At `z` it swings back out.

**Use it** to show a mobile app, a message or a step the speaker refers to.
**Don't use it** when the speaker fills the frame edge to edge at head height: there is no room beside the head. Don't use it when the screen needs to hold a lot of text. The screen is 320×720 px at most and seen at an angle.

```js
phoneMockup('TALK', a, z, {screen:(p, w, h)=>{…}, side:'right', taps:[[beat, .5, .86]], behind:false, w:360, h:760, x:null, y:null, tilt:16})
```
- `screen(p, w, h)`: draws the screen at (0,0)–(w,h). All comp helpers work inside it (`word`, `pill`, `uiType`, `uiBubble`…). The screen is pre-filled off-white.
- `taps`: `[beat, x, y]` with x and y as 0–1 of the screen.
- `behind:true` puts the phone between the room and the person (the sandwich), so the head or shoulder overlaps it.
- `side`: `'left'` or `'right'`. `x`/`y`: rest centre. `w`/`h`: phone size. `tilt`: rest angle in degrees, turned toward the speaker.

**Shot:** any shot with some room beside the head. Use `behind:true` when the phone has to overlap the person.
**Sound:** whoosh on the fly-in, a tick or zap on each tap, and a reverse whoosh out.

---

## pullBack: the edit behind the talk

**What the viewer sees.** The video shrinks into a 9:16 card inside a light app window. The window has a title bar, a sidebar with icon slots, and four more parts:
- a **checklist** whose items tick one by one: the box fills with a spring, a checkmark draws, and the text dims and is struck through;
- a **counter** tile that rolls up odometer-style to 100%, with a progress bar;
- a **timeline** of five "clips" (the current frame cropped and tinted five ways, popping in) with a ruler;
- an **audio waveform**, with an accent playhead moving across both.

At `z` the card grows back to full frame.

**Use it** for process, plan or "how I made this" lines, and for listing steps while the speaker keeps talking.
**Don't use it** for more than six steps, for long step text (about 18 characters fits), or under a fast cut rhythm. It needs about 6 beats to read.

```js
pullBack('TALK', a, z, {steps:['Write the plan','Step 1','Step 2','Step 3'], title:'Project', label:'Done'})
```
- Steps tick evenly between a+1.4 and z−1.4 beats. The counter rolls to round(100·i/n) at each tick.

**Shot:** any shot.
**Sound:** whoosh on the pull-back, a tick per checked step, a soft riser under the counter and a whoosh back.

---

## greenScreen: the speaker in front of the source

**What the viewer sees.** The room blurs and fades to a plain wallpaper colour. The speaker, cut out by the matte, shrinks to about 55% and stays anchored to the bottom of the frame, with the head well inside the safe area. Your media rises in behind them as a big rounded card with a shadow, and the head overlaps its bottom edge. An optional credit pill names the source. It eases back to the plain shot by `z`.

**Use it** for reacting to or explaining an article, a chart, a screenshot or a photo.
**Don't use it** for media that needs the full frame or has key detail at the bottom centre (the head covers it). Don't use it on shots without a clean matte, because hair edges show against the flat wallpaper.

```js
greenScreen('TALK', a, z, {media:'ARTICLE', wallpaper:'#ECE8E1', credit:'Source: example.com', s:.55, clean:null})
```
- `media`: an IMG key, an image or canvas, or `(w, h)=>{…}` drawing a vector slide. It is cover-cropped into the card, which is about 920 px wide and runs from y 268 to just behind the head.
- `clean`: the IMG key of the empty room for the fade-out (defaults to `NAME_clean`). Without one, the shot itself is blurred instead.

**Shot:** a head-and-shoulders or seated shot with a good matte.
**Sound:** whoosh as the room drops away, a shutter as the media card lands, and a reverse whoosh back.

---

## coverStory: the speaker as a magazine cover

**What the viewer sees.** A hairline border draws around the frame and the picture pushes in 3%. A tall, condensed, wide-tracked masthead (Brand 800, accent colour) rises letter by letter **behind** the head. The head overlaps the masthead's lower part and the word stays readable. A small issue line appears top-left, and cover labels (an accent kicker plus a bold line) pop in at the sides. On `punchBeat` a big slanted cover line slams in near the bottom with an accent underline sweeping under it. Everything folds away by `z`.

**Use it** for a title moment: an intro, a big claim, or "the one thing to remember".
**Don't use it** on shots with the head high in frame (it needs at least about 250 px between the safe top and the head for the masthead), or on a busy bright background behind the side labels without testing.

```js
coverStory('TALK', a, z, {masthead:'STUDIO', lines:[['Step 1','Write the plan'], 'Pick one goal'], coverLine:'Write the plan first', punchBeat:a+4, col:C.accent, ink:'#FFFFFF', issue:'No. 01'})
```
- `masthead`: one short word (4–8 letters reads best). It is sized to about 880 px wide and capped so it never rises above y 300.
- `lines`: up to four labels, alternating left/right beside the head. Each is `'text'` or `['KICKER','text']`, wrapped at 230 px. Keep each to two or three short words.
- `coverLine`: fitted to 840 px at up to 104 px tall, placed at y 1440. `punchBeat` defaults to 55% of the way through.

**Shot:** a centred head-and-shoulders shot with the head top around 28–32% down.
**Sound:** a shutter as the border draws, a riser into `punchBeat`, and an impact on the cover line.

---

### Notes for all six
- `render()` starts every frame from a clean canvas; still, fill the frame opaquely before drawing anything translucent. Blurred backdrops go through `sbBlur()`, which blurs an offscreen copy and overscales it so its edges never show.
- A shape function passed to comp's `masked()` must call `beginPath()` itself. Otherwise its path accumulates across frames.
- To reuse one shot in several scenes, add an alias with `dir`: `TALK2: {at: 24, n: 150, mask: true, dir: 'TALK'}` (it reads TALK's frames, mattes, measurements and clean plate).
