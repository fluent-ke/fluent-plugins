# Studio: graphics on the wall behind the speaker

Six talking-head effects in `studio.js` ([studio.md](studio.md) has the setup). Each one draws a whole frame: the room, then the graphic, then the speaker on top, so the graphic sits on the wall behind them. Everything stuck to the wall goes through `pinned()`, so it stays put in a handheld shot.

What every effect needs from the shot:

- person mattes (`masks/NAME/`, with `mask:true` in SHOTS)
- measurements (`shots/NAME.info.js`, read through `head(k)`)
- some open wall above or beside the head. All six place their graphics in the top third of a 9:16 frame and around the head, because a seated speaker covers most of the lower frame.

Beats `a` and `z` are comp beats. Sounds come from the soundtrack kit: whoosh, riser, impact, shutter, zap and tick.

A note on the chin line. `head(k).neck` is the head top plus the shot's median head height, so it holds steady, but on a seated, bearded speaker it can still sit near the mouth. Anything drawn in front of the person stays below `SA.chin(k)`, the lower of `neck` and a margin under the shoulder line.

---

## orbit: cards circling the speaker

**What the viewer sees.** Four to eight cards swoop in one after another and circle the speaker on a tilted ring around the chest. On the far side of the ring the cards pass behind the head and shoulders, smaller and slightly darker. On the near side they pass in front of the lap, larger. Where a card crosses the side of the ring, over an arm, it dissolves from behind to in front instead of popping. At the end the cards spin outward and leave.

**When to use it.** For "all of these at once": the tools someone uses, the brands they've worked with, the places they've been. It also works as a high-energy beat between two quieter sections.

**When not to.** When the speaker gestures a lot at chest height, because the near cards cover the hands. Avoid it under captions that sit low in the frame. Don't use it for content the viewer must read: the cards are always moving.

**The call.**
```js
orbit('TALK', a, z, {items:['logo1','logo2','logo3','logo4','logo5','logo6'],
  tilt:.85,      // ring height / width: lower is flatter. .85 lets the far side pass beside the head
  roll:-.12,     // in-plane tilt of the ring, radians
  period:7,      // seconds per revolution (real time, so stretched segments don't change the speed)
  rx:470, w:220, // ring radius and card width in px
  stagger:.12, fly:.9, phase:-.4})
```
`items` are IMG keys, drawn with rounded corners and a small shadow. Leave at least 3 beats between `a` and `z`.

**Shot requirements.** Mattes, plus `head(k)` for the chest centre and the chin line. Use a medium shot with the chest in frame. Cards near the frame edges are partly cut off at the sides of the ring; this is intended.

**Sound.** A whoosh per card on the way in, or one long whoosh for the group, and a whoosh at the exit. A riser under the orbit suits a build.

---

## couchWall: the wall becomes a feed

**What the viewer sees.** The wall dims and fills with a three-column grid of cards that rise from behind the speaker, centre column first. The grid drifts slowly upward like a scrolling feed; each column moves at a slightly different speed and the columns are offset like masonry. At the end, the columns sink back down behind the speaker.

**When to use it.** For "everyone is posting about this", "my feed is full of…", or a portfolio wall behind someone talking about their work.

**When not to.** On a shot with little wall showing. The grid only shows above the shoulders and beside the head, so a tight close-up hides it. Skip it when a single image needs attention, because a feed is wallpaper, not a hero.

**The call.**
```js
couchWall('TALK', a, z, {items:['p1','p2','p3', …],   // 9–15 IMG keys read best; columns take every 3rd item and repeat to fill
  cols:3, gap:24, speed:34 /* px per second */, stagger:.22, rise:1.1, dim:.38, r:20})
```
Cards keep their image's aspect ratio, so mixed heights give a natural feed. Leave at least 3 beats between `a` and `z`.

**Shot requirements.** Mattes. Works with any amount of open wall above the shoulders. In a handheld shot, `pinned()` keeps the grid on the wall.

**Sound.** A riser into the rise, then a shutter per column landing (or one tick each). A soft whoosh down on the sink.

---

## headlineWall: one claim, everywhere

**What the viewer sees.** Cards pop onto the wall one after another: a news headline, a social post, a search result, each drawn as a clean vector card and each saying a version of the same claim. On `keyBeat` a yellow highlighter swipes across the key word on every card in a fast cascade, including where the key wraps onto a second line. Later, one card at a time lifts to the front of the wall, larger and straight, while the rest of the wall darkens. The lifted card stays behind the speaker.

**When to use it.** To show that a claim is everywhere, to set up a myth you are about to bust, or to give social proof for a trend.

**When not to.** Never with invented outlets, quotes or figures. The cards show only the text you pass in, and the function adds no sources or numbers of its own. Don't use it with more than about 7 cards: the layout has 8 slots around the head, and a ninth card would land on top of an earlier one.

**The call.**
```js
headlineWall('TALK', a, {
  cards:[{kind:'headline', text:'…', src:'Outlet'},              // src: outlet line, optional
         {kind:'post',     text:'…', src:'Name', handle:'@x'},   // name and handle optional; no counts are drawn
         {kind:'search',   text:'…', src:'site.com › path'}],    // src: the URL line, optional
  key:'four-day week', keyBeat:a+3,
  heroBeats:[[a+4.6,0],[a+6.2,2]],   // [beat, card index]: each lifts until the next one replaces it
  stagger:.28, z:Infinity})          // z (optional) fades the wall out over the half beat before it
```
Keep the key word short (one to three words) and make sure it appears in each card's text, because the match is case-insensitive but exact.

**Shot requirements.** Mattes and `head(k)`: the cards are placed around the head top. Leave open wall above the head; the lifted card fits between y≈190 and the head top.

**Sound.** A tick or shutter as each card lands, a zap on the highlighter swipe, and a whoosh (or an impact for a big reveal) when a card lifts.

---

## chartGrow: the line that kicks up

**What the viewer sees.** A frosted panel appears on the wall with your label. A line chart draws itself left to right, mostly flat with small wobbles, with a dot at the pen tip. At `kickAt` the last stretch shoots up in the accent colour with a glow and a gradient fill. At the same moment the room behind the speaker dims (the speaker does not), so the kick pops.

**When to use it.** For "then everything changed": a growth moment, a before-and-after in one line, a hockey stick.

**When not to.** When the numbers don't kick. The shape comes only from your numbers, so if the data is flat, show it flat or use another effect. Don't use it for precise reading of values: by default there are no axis numbers.

**The call.**
```js
chartGrow('TALK', a, {points:[3,3.4,3.1,3.6,3.3,3.5,3.4,9.5],   // your numbers only, evenly spaced in x
  kickAt:a+4.8,                 // the accent segment starts drawing here
  kickFrom:points.length-2,     // index of the point where the accent starts
  label:'Weekly sign-ups',      // optional title
  tag:null,                     // optional pill near the peak: text you supply, e.g. a verified figure
  axis:null,                    // optional labels under each point, e.g. ['Jan','Feb',…]
  x:60, y:280, w:W-120, h:360, dim:.32, panel:true, z:Infinity})
```
The pre-kick line draws from `a+.35` to `kickAt`, so give it 3 or more beats.

**Shot requirements.** Mattes and open wall above the head (the default box is y 170–530 px).

**Sound.** A soft tick at `a`, a riser from about two beats before `kickAt`, and an impact on `kickAt`.

---

## checklist: the ticks land

**What the viewer sees.** A frosted glass card behind the speaker grows one row at a time. Each row slides in at its own beat with an empty circle, and at its tick beat the circle fills with the accent and a tick draws on. When every row is ticked, a footer springs open with an "n of n" pill and a full progress bar, and a soft accent glow spreads around the card.

**When to use it.** For steps, requirements, "three things you need", or a plan being completed as the speaker names each part.

**When not to.** With more than about 5 rows: the card grows down toward the head and the last rows end up behind it. Don't use it for long sentences; rows shrink to fit, so keep each under about 30 characters.

**The call.**
```js
checklist('TALK', a, {items:[['Record the talk',a+.4,a+1.6],
                             ['Cut it to 60 seconds',a+1.2,a+2.8],
                             ['Post it everywhere',a+2,a+4]],   // [text, inBeat, tickBeat]
  title:'LAUNCH CHECKLIST',   // optional
  x:80, y:280, w:W-160, row:92, size:48, footer:true, z:Infinity})   // footer: the 'n of n' pill; false keeps the words to your rows (the progress bar stays)
```
Time each tick to the moment the speaker says that item.

**Shot requirements.** Mattes and open wall above the head. With three rows and a title, the finished card is about 500 px tall, so from its default y (280) it ends near the head top: keep rows to three or four.

**Sound.** A tick on each row landing and a zap or brighter tick on each check. A small impact or a chord stab when the pill and glow complete it.

---

## glassType: the word in glass

**What the viewer sees.** One word stands on the wall as thick, clear glass letters. You can see the room through them, bent by the bevels, with a little rainbow fringing at the edges, a dark rim, a bright rim light that moves slowly across the edges, and a soft shadow on the wall behind. The word fades and rises into place, holds for about 1.3 seconds while drifting slightly, then fades out. The speaker stays in front of it.

**When to use it.** For a single premium keyword ("CLEAR", "FOCUS", a product name), a title moment, or an elegant alternative to a flat title.

**When not to.** Over a flat, very bright wall such as blown-out sky or a white studio: glass needs texture behind it to show, so it reads weakly there. It also suits only one short word; for a phrase, use type.

**The call.**
```js
glassType('TALK', a, z, {word:'CLEAR',
  x:W/2, y:330, size:250,   // centre of the word and its font size
  ref:1,                    // refraction strength
  disp:.18,                 // dispersion: the spread between the red, green and blue offsets
  drift:28, w8:800})        // drift in px over a→z; font weight
```
`a` to `z` of about 3.6 beats at 120 BPM gives the 1.3 s hold plus a half-beat in and a half-beat out.

**Shot requirements.** Mattes, and textured wall (foliage, brick, a room) behind the word. It needs WebGL: the shader context is built once on first use and reused. The height map is cached by word, size and weight.

**Sound.** A shutter or glassy tick on the entrance, or an impact if the word is the punchline. Fade out under a whoosh.
