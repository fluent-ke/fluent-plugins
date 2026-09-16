# Slide decks in Pencil

Read after `SKILL.md`. This is the mechanics of building and presenting a deck. Visual taste — palette, type, imagery — belongs to whatever design-preferences doc your team keeps; where that disagrees with anything here or with Pencil's own Slides guide, **the team's rules win**.

## Get the Slides guide first

```
read_skill({path: "guide/slides.md"})
```

It returns 20 numbered layout contracts (L01–L20) plus hard floors: 16:9 at 1920×1080, body ≥24px (prefer 28–32), titles ≥40px, content ≥100px from every edge, max two font families, line-height 1.1–1.2.

Contracts by job: **L02** bold cover · **L04** key statement · **L07/L16** pillars and icon rows · **L08/L18** compare and before/after · **L09–L11** hero numbers · **L13** process steps · **L19** lists · **L20** closing.

## Frame layout that presents correctly

Pencil presents off **top-level frames in layer order**. Not canvas position — layer order. A deck can look perfect on canvas and present shuffled.

- One frame per slide, `1920×1080`, `layout: "none"`, `clip: true`, at the document root.
- Lay them down the canvas at `y = index * 1280` so the canvas reads in running order too. That spacing is convention (it just adds a gutter below a 1080-tall frame), not function.
- **Park every `reusable` component at the end of the layer list** or it presents as slide one.
- Name frames `01 · Title`, `02 · Title` … so running order is legible in the layer panel.

Reorder and rename in one pass:

```js
const deck = [["S01","01 · Cover"], ["X21WOj","02 · Inside the black box"]]
deck.forEach(([id,nm],i) => { Update(id,{name:nm,x:0,y:i*1280}); Move(id, document, i) })
Move(markComponentId, document, deck.length)
```

## Build a new deck from an existing one

The fastest reliable route, and it preserves component wiring:

1. Read the source `.pen` **on disk** (it's JSON) and copy the slide nodes you want **verbatim**, along with `variables` and the component node.
2. Write the new `.pen` to a path the app has never opened.
3. Copy the referenced images into the new folder's `images/` — image `url`s are relative to the `.pen` file's own directory, so a deck without its images renders empty rectangles.
4. `open` it, re-run the guard, then work through the MCP.

Copying verbatim keeps node IDs, so every `ref` → component link survives the transplant. Six slides have been moved between decks this way with their component instances intact.

For a deck with no ancestor, use the scaffolder — see `SKILL.md`.

## Presented-only vs authoring pairs

Slides authored as pairs (a projected version beside a detailed twin) are excellent for review and useless for presenting. Flattening later means: move every presented slide to `document`, reposition (coordinates arrive parent-relative and therefore wrong), delete wrappers, twins and variant columns, then reorder.

**Decide up front.** If the deck is for presenting, build presented-only from the start.

## Sweeping the whole deck

Deck-wide edits are one visitor pass, not one call per slide:

```js
const turns = Get(n => (n.type === "text" && n.name === "Turn") ? n.id : undefined)
turns.forEach(id => Delete(id))
```

This depends entirely on **consistent node names across slides**. Name every node you insert (`Panel`, `Title`, `List`, `Row`, `Num`, `Label`, `Pointer`, `Turn`) and a later sweep is trivial. Skip naming and every change becomes manual.

## Timing

Roughly **90 seconds** per content slide when the room already half-knows the material, **2–3 minutes** when it's new. Budget backwards from the slot and cut slides, never font sizes. A 15–20 minute slot is 7–9 slides, not 12.

## Verify before it's presented

1. Structural pass for clipping.
2. **Screenshot every slide carrying a photo.** Composition — text over a face, a panel over the logo, a subject cropped out — is invisible to a layout check.
3. Confirm layer order matches running order.
4. Confirm the component is parked last.
