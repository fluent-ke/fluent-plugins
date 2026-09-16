---
name: designing-visual-assets
description: Use when creating, reviewing or critiquing any visual asset — a poster, social post, carousel, thumbnail, slide, flyer, banner or ad — or when a design has the right colours and still reads flat, cluttered, generic, or like nobody decided what it was for. Works with any brand, any editor, or none.
license: MIT
metadata:
  author: fluent
  version: "0.2"
---

# Designing Visual Assets

## The idea everything here follows from

**A viewer does not read elements. They read a handful of blocks.**

- **Segment** — a block the viewer perceives as one thing.
- **Element** — a part inside a segment: a word, a price, a logo, a rule.

Almost every failed asset is a segmentation failure wearing a different costume. Too many blocks, or blocks that dissolve into each other, or a block that leads which shouldn't.

This skill is the craft. **It names no colour, typeface, canvas size or application on purpose.** Three references make it concrete, and the first two are plug-ins you swap:

- `references/brand-layer.md` — the slots a brand document must fill. **Load the brand's own document before designing.** Without it the craft still runs and produces competent, faceless work. That is the intended failure, not a bug.
- `references/tool-layer.md` — what the craft assumes of any editor, what to do when a capability is missing, and print.
- `references/content-specs.md` — what each format must communicate.

## Before you design

**Design is the third step, not the first.** Do not open a canvas until:

1. **The brief exists** — audience, angle, the one message, the channel, the action.
2. **Copy exists and is signed off.**

Nothing in this skill audits *meaning*. Every check here can pass on a design whose words are wrong. If the brand has a voice document or a review step, the copy goes through it before it reaches you.

**If the approver is unreachable, there is a third state — use it instead of stopping or pretending.** Draft the copy to every rule you have, mark it `DRAFTED — NOT APPROVED`, name who must sign it off, and design against it. Carry anything you could not verify as a named blocker. Never invent a person's name, a URL, a price or a legal fact to fill a gap; leave a placeholder that cannot be mistaken for real.

## Step 1 — Decide

**Your first output is the decision block. Not a preamble, not a layout description, not an artefact — the block itself, printed in full, before anything is composed.**

This is the deliverable of step 1 and it is what the person reads first. A design that arrives without it has skipped the only step where the thinking is visible and checkable, and neither you nor they can tell afterwards whether the ranking was decided or inherited.

If you are also composing in the same turn, the block still comes first, in the reply, above the work.

```
MESSAGE   one or two sentences: what must this asset communicate?

RANKING   from the format's content spec
  1 …  2 …  3 …
  Overflow: where the ranks that don't fit are going — a caption, a page,
            a second asset. If the format has no overflow channel, write
            "none — the asset carries everything" and lengthen the ranking.

SEGMENTS  the blocks. Three to five suits most assets; a no-overflow format
          may need more, and one carrying a single idea may need fewer.
          Ranks may merge — say which and why.
  S1 [name]  ranks: …  elements: …
  S2 [name]  ranks: …  elements: …

LEADS     which rank leads, and why

IMAGE     what it must communicate, and its rank.
          If the brand permits no imagery, name what occupies that rank
          instead and what it must communicate.

BLOCKERS  anything you could not resolve, and who must resolve it
```

**Which ranks merge and which split is the design decision, not a lookup.** Three thin blocks at the base of a poster is usually one footer segment.

**A different event, audience or price is a new decision block, not a derivation from the last one.** Reusing the previous asset's ranking because the brand and format match is the most expensive shortcut available here — it silently inherits which rank leads, and that is the decision the whole composition hangs on. A name that stops the scroll for one audience means nothing to another. Re-run the block even when the layout will end up similar.

## Step 2 — Compose

- **Choose or compose the image for this segmentation.** Never generate an image into a layout already fixed — that makes the picture serve the leftover space.
- **Space encodes relatedness.** Set one gap between peer segments and hold it. Use a larger gap where the asset should breathe or where two segments are not peers. Equal throughout is the default, not a law; a quiet or luxury design is built on unequal macro-space. Deviate deliberately and say why.
- **Resolve each segment into one optical block.** Size or centre its elements to a common height. A tall thing beside a short thing is two things.
- **Commit to one alignment system and hold it.** Every element anchors to a real edge — a margin, another element's measure, a canvas corner. One element on a foreign axis with nothing else on it fails, and fails worse than if it had stayed on the default.
- **Separate by space first.** A device — rule, bar, panel, chip — only where space alone leaves the grouping ambiguous.

## Step 3 — Verify

Both passes. See **Verification** below.

---

## The rules that bite

Ordered by how reliably they get missed. Ordinary design advice is left out — you already have it.

### Segments

- **Proximity beats alignment for grouping.** Two elements close together read as one group even on different axes; two far apart read as two even when perfectly aligned. Spreading a segment across the full measure separates what you meant to bind.
- **Judge a segment's height in place, at size** — never on its own board. Its height is spent from the same budget as the image.
- **A secondary segment must not approach the leading one in size.** The brand layer sets the ratio. If it doesn't, pick one, write it down, and hold it.
- **Three segments in one even stack read as one segment**, whatever the gaps between them. Evenly spaced peers are a single object to the eye. Separate them by *region* — one at the top margin, the group in the middle — or by a step change in gap. Another twenty pixels will not do it.
- **A hard edge may cross an element; it must never cross a segment's internal gap.** A ground split running through a word is a depth move and reads as deliberate. The same split running between a title and its subtitle cuts one segment into two, and no amount of correct spacing recovers it.

### Alignment

- **Anchored, always** — to a margin, an edge, another element's measure, or a canvas corner.
- **Pinning an element to a canvas corner is a legitimate move**, often better than forcing it into the stack.
- **Align optically, not to the box.** A rule beside text matches the text's cap height and centres on its optical middle, not its line box — which carries ascender and descender space the text does not fill. Box alignment is arithmetically right and visibly wrong.
- **A text box is wider than its letters.** Letter-spacing is applied after the final character too, so a tracked line's box carries one extra space its last glyph does not fill. Matching two lines by box width leaves the tracked one visibly short. **Two lines bind into one lockup when their visible measures match and the gap between them is tight** — matching heights is not enough, and matching boxes is wrong.
- **When edges must align exactly, measure them; do not calculate them.** Read the actual ink extents. Arithmetic from reported widths is how you get three confident wrong answers in a row.

### Devices and colour

- **A separating device used more than once stops separating.** Repeat it and it becomes texture.
- **Never do one job with two devices.** If a rule already separates two blocks, do not also change their colour.
- **Pick one channel to carry hierarchy** — size, weight, space, or colour — and lead with it. Doing hierarchy in two channels *by accident* is the failure. Where a brand deliberately welds two channels to one element, that is the brand's call and it wins; declare the exception rather than flagging a false failure.
- **A translucent device needs contrast behind it to exist.** Glass on a dark ground is invisible. Put it where the ground is light, or drop it.
- **A panel is an accent for one element, not a container for the copy.** One panel holding title, promise, facts and action merges every rank into a single object and destroys the segmentation.

### Type

- **Delete redundant hierarchy.** An eyebrow repeating the title is noise; one carrying category or series information the title does not is a legitimate device. Cut the redundancy, not the device.
- **Never fabricate a lockup.** Do not set another organisation's name in your own type beside its mark as though the two were one supplied unit — a partner's wordmark has its own typeface, so a hand-set version is wrong on sight. Use the supplied lockup whole wherever you use it at all.
- **Run a small fixed set of type sizes.** Two items of identical importance take identical size. Differentiate only where reading order demands it.
- **Build recurring lockups as components with one master.** Rebuilt by hand they drift on every asset.

### Image

- **The subject is the segment; the photograph is its container.** The subject must be whole, recognisable at a glance, and surrounded by enough bleed that it sits *in* a space rather than filling the frame.
- **A crop belongs to one photograph.** Replace the image and the crop resets to zero. Inherited framing becomes a zoom.
- **An image that communicates nothing is a failed segment, not a neutral background.**
- **Where the subject looks, the reader looks.** A face turned away from the copy sends attention off the canvas.
- **Generated screens and props:** show real work, softly rendered, too small and too soft for any letter to be legible. Blank screens say nothing; fabricated legible interface text is a credibility risk and the most reliable failure in generated imagery.
- **A generated image drifts on every axis you did not name.** Age, dress, setting, who is in the room and what they are doing all get decided by whatever the words most commonly co-occur with. Name the axes that matter, explicitly. The ones that fail silently and most need naming:

  | Axis | What to state |
  |---|---|
  | **Cast, including everyone in the background** | Naming the subject sets the subject only. Background figures default to whatever the model averages to, so a correctly-cast foreground arrives in front of a miscast room. Name every person in frame, not just the one in focus. |
  | **Object anatomy, for any device in shot** | Laptops are the repeat offender: the screen renders *outside*, *above*, or *through* the lid, or the lid goes transparent. State that the lid is a single opaque panel and the screen sits entirely inside its bezel. Phones and monitors fail the same way. |
  | **The negative space the layout needs** | Name the region that must stay empty **and what it is for** ("the lower third is empty unlit desk, clear of any object, so text can sit over it"). Name only the subject and you get a well-composed photograph with nowhere to put the copy. |
- **Words with two meanings steer by the wrong one.** "Senior" meaning seniority returns people in their sixties; "executive" returns boardrooms. Describe the trait — the role, the age range, the activity — not the word that implies it.
- **Correcting one axis moves another.** Tighten on age and the cast changes; tighten on setting and the activity does. Re-check the axes you had already got right, every regeneration.
- **Check what the image says the event is.** People watching a presenter sells a lecture. If the brief says workshop, the room must be working.

### A row of portraits — speaker bills, line-ups, panels

Different photographs of different people have to read as one row, and they will not do it on their own.

- **Match on shared landmarks, not head height.** Pick two — the hair line and the shoulder line — and land them on the same y in every cell. Matching head heights alone leaves a waist-up shot beside a head-and-shoulders one, and the waist-up face reads smaller in the same frame even though the measurement says they match.
- **Never land a landmark on a clipping edge.** Place the hair line 30–40px inside the frame, not at zero. The landmark is a measurement made by eye, and one placed exactly on a crop boundary turns any error into a flat-topped head. The headroom absorbs the error.
- **The widest subject sets the ceiling for everyone.** Long hair can measure nearly twice the head height; once it exceeds the column it gets sliced with no container to justify the cut. Size the row to the widest photograph, and say so rather than quietly shrinking one face. **Fixing this is a photography request, not a layout move.**
- **A bust cannot fill a circle.** The lower arcs stay empty however you scale it, because shoulders end where a circle is still wide. Give the disc its own ground so the gap reads as a medallion, or use a rectangle.
- **A container wider than it is tall stops reading as a portrait frame.** Check the *ratio* — widening a column while holding the head fixed makes the face look smaller even though nothing shrank.
- **When someone hand-edits one cell to show you what they want, read the numbers off it and reduce them to ratios** of the column width before propagating. Ratios port to other sizes; pixel values do not, and re-eyeballing their intent wastes the edit they just made.

---

## Output: three to five variations

**One or two is not a choice.** Present three to five, differing on **two structural axes**: composition, plus one other the brand permits — the image, the ground treatment, where the accent is spent, the grid's orientation. A recolour or a recrop is not an axis.

**Composition means the grammar, not the ground.** Two variations differ in composition when you can point at a change in at least two of:

- which rank leads, and at what size
- the reading axis — left, centred, right, or a column
- where each segment sits on the canvas, not merely how far apart
- which devices are present at all
- the order segments are read in

**Swapping the photograph and moving the fade is one design in different clothes.** Say, for each variation, which two of the above changed. If you cannot name them, you have made one composition several times, and the set will read as one design to everyone but you.

---

## Working in different environments

Branch on what your environment can actually do, not on what product you are running in.

**No editor at all** (a chat window with no design tool). You cannot compose, and that does not make this skill useless — two of its three steps still run, and they are the two that decide whether the asset works.

- **Do run:** the decision block, the ranking, the segmentation, the image brief, and the critique of a design someone shows you. Reviewing an uploaded asset against the rules above is a complete and useful job.
- **Do not:** describe a layout in prose and present it as a design. A specification is not an artefact. Say plainly that you have produced a plan for someone to execute.
- **If the environment can render markup** — an inline document, HTML, SVG — that is a real canvas and you may compose in it. The computed checks below still do not run unless you can measure what rendered.

**An editor, but no way to measure geometry.** Every anchored alignment becomes an estimate. Export and look far more often, and prefer aligning to margins over aligning to other elements. Report which computed checks you could not run rather than implying they passed.

**Sub-agents available.** Give each variation its own agent — same brief, a different composition assignment. A single author produces variations that all share their first instinct.

Each child brief must carry, **in full**: the brand layer's contents, the approved or drafted copy verbatim, the decision block, its one composition assignment, and an instruction to read this skill first. A child with no brand layer produces competent, faceless work; it cannot fetch what you did not send.

**You own the synthesis. Dispatching is not delivering.** Launch them, wait, read what came back, and write the comparison yourself. Never end your turn on "the agents are working" — that reads as finished, and the person gets a status line instead of a design.

**No sub-agents.** Fix the composition assignments as structurally disjoint *before* composing anything, then do the work yourself against them. **Say plainly that this is single-author work.** Never present it as if it had been fanned out.

---

## Verification

### Pass 1 — computed

**Only where the tool exposes geometry.** Where it does not, these move to pass 2 and you look harder — and you say which you could not run.

Checks marked **[B]** may be overridden by an explicit brand rule. An override is declared in your output, never silent.

1. Gaps match the intended spacing, and any deviation was declared.
2. Every element anchors to another edge, a margin, or a canvas corner.
3. One margin value, held on all sides.
4. Rules and bars match the cap height of adjacent text.
5. **[B]** Each separating device appears once.
6. **[B]** Hierarchy is carried in one channel, not two.
7. No bounding-box collisions, no overflow.
8. Text and ground clear the contrast floor at the size used. **Not overridable.** A colour with no published value cannot be checked — escalate rather than invent one. **If the brand mandates a failing combination, break the rule loudly:** state the measured ratio, state the minimum change that fixes it, mark it as needing the brand owner's sign-off, and never ship illegible type or a silent deviation.
9. Values are tokens where tokens exist.
10. No fabricated lockup.
11. **At 20% scale, the leading rank is still legible.** Every format, not just thumbnails.

### Pass 2 — looked at, full resolution, on the export

12. Subject whole, legible, with air around it, facing into the asset.
13. The image communicates the message rather than decorating it.
14. No garbled text on generated props.
15. Segments read as separate at a glance, in the intended order.
16. Rags, widows and line breaks read as chosen rather than as wrapping.

**Pass 2 is not optional and it cannot be satisfied from a specification.** If you have produced a spec rather than an artefact, report 12–16 as unverified rather than inferred.

---

## Worked example — where the decision block does the work

A four-hour paid webinar poster. Ranking: identity, promise, when, cost, entry.

The naive reading gives five segments, and the base of the poster becomes three thin blocks — date, price, action — none of which leads and all of which are the same kind of thing. **Merging ranks 3–5 into one footer segment** takes the asset to four, gives the eye somewhere to stop, and lets identical importance take identical size. Nothing in the spec says to do it. The spec gives the ranks; the merge is the design.

Then the image: not a person at a laptop, which depicts *using a computer*, but the audience's own marketing laid out on a counter — which depicts the thing being taught. That decision sets the crop, which sets where the footer can start, which sets the rhythm. Image first, layout second.

---

## Common mistakes

| Mistake | Fix |
|---|---|
| Straight to layout | Message and ranking first, in the decision block |
| Designing before copy is signed off | Get it, or mark it drafted-not-approved and carry the blocker |
| Image generated into a fixed layout | Compose the image for the segmentation, or move the layout |
| Checklist run once, then the image changed | Changing the image resets every image-dependent check |
| Variations differing by a parameter | Two structural axes, or it is one design |
| A panel to make text legible | Space, ground, or a fade. A panel is for one element |
| Equal spacing enforced everywhere | Equal is the default between peers, not a law |
| Filling a gap the brand left | Layout gaps you may fill and record; identity gaps you escalate |
| Presenting a spec as if it were verified | 12–16 need eyes on an export |

---

Stuck, or want to send feedback on this skill? Read the `about-fluent` skill.
