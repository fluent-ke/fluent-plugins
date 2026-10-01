# Footage effects

Edit tricks on supplied footage, in the style of sports and event hype reels: reveals, match cuts, frame-rate flicker, logo swaps and warps. Each is built in `comp.html` from the footage helpers, so it re-times and renders in parallel like any other scene.

## Before you pick one

- **Footage decides.** Each effect lists the footage it needs. Check it against the intake asset list; when a shot is missing, use the effect the footage supports, or a generated plate ([3d.md](3d.md#generated-plates)).
- **Seasoning.** One or two effects per film, on its biggest beats (the drop, the reveal, the logo). Every effect pairs with a sound in the score on the same beat.
- **Live shots.** A shot's frames load only while it plays, from its `at` beat for `n` frames. Every shot an effect reads in a frame must be playing then: give each shot in a pool the scene's start beat as its `at`.
- **Frame-rate effects** (match cut, colour flip, frame build) count film frames with `fi()` from `fAt(beat)`. They keep their speed when `timeline.js` stretches a scene; only their start moves.
- **Points from the footage.** Vanishing points, logo corners, crowd sections and player positions are frame pixels read off the source frame: `python3 $K/scripts/asset_tools.py grid shots/NAME/0001.jpg out/grid.png [x0 y0 x1 y1]` labels the grid in source pixels. Check each shape on a stills sheet before building on it.

## Helpers

| Helper | Does |
|---|---|
| `masked(draw,shape,{feather,alpha})` | runs `draw()` (any helpers: `plate`, `subject`, `word`…) and shows it only inside `shape`: a point list `[[x,y],…]` or `c=>{…a path on c…}`. `feather` softens the edge in px. The building block of every reveal below |
| `ctx.filter='brightness(g)'` before `plate`/`subject` | exposure: `g` .3 is a darkened base, 1.5–2 a flash. Reset to `'none'` after |
| `about(x,y,s,f)` | `f()` scaled by `s` about a point (a vanishing point, a portal) |
| `zoomBlur(cx,cy,amt)` | radial zoom blur of everything drawn so far: .1 subtle, .45 a punch |
| `warp(cx,cy,R,amt)` | per-pixel lens bulge (WebGL) inside radius `R`: .5 doubles the centre, negative pinches |
| `quad(img,[TL,TR,BR,BL])` | an image pinned to four corners in perspective |
| `grow(P,d)` | a convex shape with every edge pushed `d` px outward |
| `track(SHOT,[[frame,points],…])` | any point list (four corners, a section) keyed on a few source frames, interpolated for the frame playing now |
| `fi()`, `fAt(beat)` | the film frame now; the frame a comp beat starts on |

## Hyperlapse merge

Two hyperlapses joined into one forward rush. **Needs** two forward-moving hyperlapses with a clear vanishing point (stabilise first: `ffmpeg -i in.mp4 -vf deshake out.mp4`; speed one up with `prep_footage.sh … 0.125` for 8×). Read each shot's vanishing point; draw B shifted so its vanishing point lands on A's. A accelerates into the point and B grows out of it, with the zoom blur peaking on the cut:

```js
const vp=[540,820],c=1;                         // vanishing point, cut beat
if(b<c)about(...vp,lerp(1,1.9,E.inExpo(PB(c-.5,c))),()=>plate('A'));
else   about(...vp,lerp(.75,1,E.outExpo(PB(c,c+.5))),()=>plate('B',1,0,-120));   // B's offset aligns the two points
zoomBlur(...vp,.45*Math.exp(-(((b-c)/.18)**2)));
```
Sound: a riser into a sub hit on the cut.

## Stadium reveal

An empty venue wiped to the same view full. **Needs** two shots with the same camera move (direction and speed) from about the same position, such as rehearsal and match night; match their speeds with `prep_footage.sh`'s `slow` and their framing with `plate` offsets until a still at 50 % opacity shows the stands lining up. Draw the full shot, then the empty one masked to the side of a moving feathered edge:

```js
plate('FULL');const x=lerp(-500,W+500,E.inOutCubic(PB(a,a+1)));
masked(()=>plate('EMPTY'),[[x,0],[W+600,0],[W+600,H],[x-500,H]],{feather:40});
```
The edge sells it when it follows something in the shot (a pillar, a stairway, a floodlight beam); key the edge's points to that feature. Sound: a crowd roar swelling under the wipe.

## Masked frame build

A steady subject while the world behind them flickers through shots. **Needs** a subject shot with a matte (`swift $K/scripts/segment.swift person …`, `mask:true`) and a pool of three or more shots, all live. Three masks (panels, circles, the letters of a word) open one per beat behind the subject, each cycling the pool every 2 frames on its own offset; on the last beat they lock to one shot:

```js
const pool=['A','B','C','D'],f=fi()-fAt(a);
[[0,W/3],[W/3,2*W/3],[2*W/3,W]].forEach(([x0,x1],j)=>{if(b<a+.2+j*.3)return;
  const k=b>a+1.3?0:Math.floor(f/2+j);masked(()=>plate(pool[k%pool.length]),[[x0,0],[x1,0],[x1,H],[x0,H]])});
subject('HERO');
```
Sound: a stuttering hi-hat or glitch tick on the flicker, a hit on the lock.

## Crowd masking

Sections of a crowd lit up one by one. **Needs** a locked-off shot (or one held frame) so the sections stay put; on a moving camera key each section's points like a logo's: `masked(…,track('CROWD',[[1,P],[60,P2]]))`. Darken the whole shot, then expose each section with an overshoot that settles above the base:

```js
ctx.filter='brightness(.3) saturate(.7)';plate('CROWD');ctx.filter='none';     // a = the scene's start beat
SECTIONS.forEach((P,j)=>{const s=a+1+j,g=b<s?0:1+.6*Math.exp(-(b-s)*6);
  if(g)masked(()=>{ctx.filter=`brightness(${g})`;plate('CROWD');ctx.filter='none'},P,{feather:24})});
```
One section per beat, landing on the kick. Sound: a crowd-shout sample or a stab per section.

## Court reveal

A darkened arena where the court lights, then each player, then the whole venue in rings. **Needs** a wide shot of the court with players, mattes for the players, and a locked or tracked camera. Build it from the crowd-masking pattern: the court polygon exposed first; each player via `subject()` under a brightness flash (to isolate one person from a matte of many, wrap `subject` in `masked` with a polygon around them); then three circles from the court centre on staggered springs, so their edges ripple out out of step:

```js
[[a,1.1],[a+.12,1.4],[a+.3,1]].forEach(([s,g])=>{const r=1300*spring(s,{z:.7,w:10});
  if(r>1)masked(()=>{ctx.filter=`brightness(${g})`;plate('COURT');ctx.filter='none'},c=>{c.beginPath();c.arc(540,900,r,0,TAU)},{feather:50})});
```
Sound: a hit per stage, the rings on a rising sweep.

## Logo match cut

The same logo on many surfaces, 1–3 frames each, never moving on screen. **Needs** five or more stills or shots showing the logo (shirts, signs, screens, merch); read each logo's centre and width off its frame. Scale each shot so its logo lands at frame centre at the same width; choose the target width as the largest logo in the set so no shot is drawn below full size, and fill behind for a logo near a frame edge:

```js
const L=[['A',540,1150,260],['B',300,620,200],['C',540,1000,300]],   // [shot, logo x, logo y, logo width]
  [k,lx,ly,lw]=L[Math.floor((fi()-fAt(a))/2)%L.length],s=300/lw;
bgFlat(C.bg);ctx.save();ctx.translate(W/2,H/2);ctx.scale(s,s);ctx.translate(-lx,-ly);ctx.drawImage(FR['f'+k],0,0,W,H);ctx.restore();
```
Accelerate it: 3 frames per shot, then 2, then 1, landing on the clean brand mark on a hit. Sound: a tick per cut over a riser.

## Colour flip

A burst of frame-by-frame brand colour across a cut. **Needs** nothing beyond the two shots. A grid of cells (halves, thirds, a 2×3) each flips between the two brand colours and the footage every frame on its own phase; the footage underneath switches to the incoming shot halfway:

```js
const f=fi()-fAt(cut);plate(f>=0?'IN':'OUT');
if(Math.abs(f)<=5)for(let r=0;r<3;r++)for(let c=0;c<2;c++){const s=(f+r+c*2+99)%3;if(s===2)continue;
  ctx.fillStyle=s?C.brand:'#FFFFFF';ctx.fillRect(c*W/2,r*H/3,W/2,H/3)}
```
Keep each burst to about 10 frames with the cells out of phase, so the whole frame never flashes white at once (photosensitive viewers, and platform flash checks). Sound: a burst of noise or a glitch stab.

## Logo replace

The original mark removed and a new one placed in the same orientation and size. **Needs** a shot where the old mark is visible and the user's right to alter it (see Rights below). Key the mark's four corners every 10–15 source frames with `asset_tools.py grid` (more often where the camera eases or turns), across only the frames that play: beats on screen × 60/BPM × FPS. A corner that leaves the frame in a push-in is extrapolated from the mark's aspect ratio; negative x is fine. Then fill over the old mark and pin the new one:

```js
plate('SHOT');const P=track('SHOT',[[1,[[172,532],[654,540],[654,625],[172,620]]],[20,[…]],[48,[…]],[96,[…]]]);
masked(()=>bgFlat('#0e0e0e'),grow(P,12),{feather:6});    // fill 12 px past the old mark, in the surface colour from asset_tools.py sample
quad(IMG.newlogo,P);
```
On a flat surface (screen, wall, a plain shirt) fill with the sampled colour; on texture, clone it from beside the mark: `masked(()=>{ctx.filter='blur(4px)';plate('SHOT',1,dx,dy);ctx.filter='none'},…)` with `(dx,dy)` the offset to a clean patch. A static mark on a locked shot can be removed at prep instead: `ffmpeg -i in.mp4 -vf delogo=x=…:y=…:w=…:h=… out.mp4`. The new logo matches the old one's proportions; a different shape needs a larger fill. Give it contrast with the surface: a dark mark on a dark screen is recoloured on a canvas first (draw it, then `source-in` a fill in the brand colour). Check it on stills at each key and midway between keys: where the outline drifts, add a key.

## Warp reveal

The player is pulled into a portal that opens on the next shot. **Needs** a player shot with a matte, and the next shot. Shake on the impact, the bulge swells over the player, the portal (the next shot in a growing circle) opens at their centre while their matte shrinks into it; the portal covers the player's own spot in the plate before they vanish, so no clean plate is needed:

```js
const p=[540,950],sh=b>a&&b<a+.6?Math.sin(b*90)*16*(1-PB(a,a+.6)):0;ctx.translate(sh,sh*.6);
plate('PLAYER');const r=1400*E.inExpo(PB(a+.3,a+1.1));
if(r>1)masked(()=>plate('NEXT'),c=>{c.beginPath();c.arc(...p,r,0,TAU)});
if(b<a+.9)about(...p,1-E.inExpo(PB(a+.2,a+.9)),()=>subject('PLAYER'));
ctx.setTransform(1,0,0,1,0,0);warp(...p,700,.6*Math.sin(Math.PI*PB(a,a+1.2)));
```
Sound: a whoosh reversed into an impact as the portal fills the frame.

## Rights

A logo replace on someone else's mark, or footage of a real event, needs the owner's permission or a licence the user holds. Ask where the footage and marks come from when it is unclear, and say so when delivering.
