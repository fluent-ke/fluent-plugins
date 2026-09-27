# Motion recipes

`comp.html` draws every frame from scratch with `render(t)`. `b` is the comp beat, `m` the music beat, `t` seconds. A scene is an `if(b<end){…;return}` block; helpers take progress values in 0–1 that you derive with `PB(a,z)` (linear) or `IN(a,dur,ease)` (eased entrance).

## Helper library

| Helper | Does |
|---|---|
| `word(str,x,y,weight,size,fill,{stroke,lw,alpha,sc,rot,track,align,blur,glow})` | one line of text; `sc` and `rot` pivot on (x,y), so a left-aligned word scales from its left edge |
| `fit(str,weight,maxW,maxSize)` | largest size that fits a width |
| `echo(str,x,y,w,s,fill,stroke,spread,alpha=1)` | slam: outline copies collapse into the word as `spread`→0 |
| `rise(str,x,y,w,s,fill,k)` | line slides up out of a masked slot |
| `wrap(str,w,s,maxW)` | lines for a paragraph; `rise` each with a small stagger |
| `pill(txt,x,y,s,bg,fg,{sc,alpha,stroke,w8})` | rounded tag (`w8` = font weight); pop it in with `sc:IN(b0,.45,E.outBack)` |
| `img(IMG.key,x,y,width,{alpha,sc,r,rot})` | an asset from `SRC`, at its own aspect ratio; `r` rounds the corners |
| `count(n,a,z)` | number counting up between two beats, formatted |
| `bgGlow(col,x,y)`, `bgFlat(col)` | backgrounds; `grainPass()` adds film grain over everything |
| `swipe()` + `CUTS` | band wipes across; the scene changes under it |
| `plate(SHOT)`, `subject(SHOT)` | footage frame; the matted person drawn on top of it |

## Recipes

**Kinetic words, one per beat.** `const i=Math.floor(b),k=b-i;` pick word i, flip background and fill each beat, scale from 1.3 to 1 with `E.outExpo(k/.35)`, `echo` with spread from `s*.9` to 0.

**Title slam.** `echo(title,…,lerp(s*.9,0,E.outQuint(PB(a,a+.6))))`, then the second word one beat later in the accent colour. Pair with an impact in the score.

**Reading card.** Header label small and tracked, big number or icon, then the text `rise`s line by line with a 0.08-beat stagger, then a pill. Exit by sliding left with `E.inExpo` in the last quarter-beat.

**Counter.** A centred number whose width changes wobbles as it counts: measure the final string once, then draw left-aligned from `x - finalWidth/2`, and wrap any scale in your own translate about the centre. `word('$'+count(1000,a,z),…,{sc:1+.12*Math.exp(-(b-z)*6),glow:b>z?C.accent:null})` and a burst of seeded particles on landing: positions from `rng(seed)`, moved by elapsed time with gravity, faded out.

**Map or network.** Nodes at fixed points, quadratic arcs between them drawn progressively (`k` of the path), dots travelling along each arc with `((b-start)*.55+j/3)%1`, labels and pills popping in per node. Flags and logos cropped from the supplied artwork.

**Text behind a person.** Footage frames via `prep_footage.sh`, mattes via `swift segment.swift person shots/NAME masks/NAME`, `mask:true` in `SHOTS`. Draw `plate`, then the text, then `subject` with the same transform.

**Product sticker.** `swift segment.swift cutout photo.jpg assets/cutout.png`, then draw it with a white outline (the silhouette drawn 24 times offset in a circle) and a soft shadow; bounce it in with `E.outBack`.

**Camera moves.** Wrap a scene in `ctx.translate/scale` driven by `PB`: slow push-in (scale 1→1.06 over the scene), whip (big `x` offset with `E.inExpo` at the scene end, blur up to 12 px), shake on impacts (`Math.sin(k*200)*10` for 0.15 beat).

## Rules of the craft

- One motion idea per scene; everything else holds still so the eye knows where to go.
- Entrances are fast (0.3–0.5 beat, ease-out); exits faster (0.25 beat, ease-in). Holds are long.
- Every hit on screen has a sound, and every big sound has something on screen.
- Two typefaces at most, usually one family in two weights; colours from the brand palette plus one accent.
