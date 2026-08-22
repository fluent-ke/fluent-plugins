# The tool layer

The parent skill names no application. It assumes an editor with the capabilities below and nothing more. **Load that editor's own skill for mechanics** — how to open a file, what its API is called, how it fails.

Swap the editor and the craft is unchanged. That is the point.

## Capabilities assumed

| Capability | Why the craft needs it |
|---|---|
| **Place** | Position an element at explicit coordinates, and nest one inside another. |
| **Measure** | Read back an element's resolved bounding box *after* layout. Required for anchoring, for equal rhythm, and for computing tracking to a target width. Guessed geometry is how misalignment ships. |
| **Group** | Bind elements into a segment that can be moved and reasoned about as one object. |
| **Component** | Define a master once and reference it, so a lockup used across a series stays identical and a correction propagates. |
| **Clip** | Constrain an image to a frame so the crop is a property of the layout rather than of the file. |
| **Export** | Render at full resolution for the eyes half of verification. Thumbnails hide text-over-subject and garbled props. |
| **Screenshot** | See the canvas without exporting, for cheap intermediate checks. |

## If a capability is missing

- **No measure** — every anchored alignment becomes an estimate. Compensate by exporting and checking visually far more often, and prefer alignments to margins over alignments to other elements.
- **No component** — a shared lockup will drift. Build it once, export it as an image, and place that image rather than rebuilding the construction each time.
- **No clip** — the crop lives in the image file. Re-crop the source when the layout changes rather than inheriting framing.

## Rules that hold in any editor

- **Read geometry back; do not trust what you set.** Layout engines override position inside automatic layouts, resolve text to different widths than estimated, and silently drop constructs they do not support. "I set it" and "it is there" are different claims.
- **Verify visually before presenting.** Structural checks pass on designs that are visibly broken — a panel across a subject's face is valid geometry.
- **Assume no undo history and no autosave** unless the editor's own skill says otherwise. Confirm work is saved before ending a session.
- **One editor session, one agent.** Where the editor exposes a single active document, a second agent's writes land in the first agent's file. Parallel *authoring* into separate files is safe; parallel *looking* is not.
- **Proportional scaling of a group may not exist.** Where it doesn't, derive every dimension in a construction from one parameter so the whole thing can be rebuilt at any size instead of dragged.

## Print

Screen assumptions break on paper, and a brand's full-width bands make this immediate.

- **Bleed.** Any element touching a sheet edge extends past the trim — 3mm is the common minimum. Without it, every trimmed copy shows a sliver of ground at the band's end.
- **Trim and safe area.** Content sits inside a margin measured from the *trim*, not the bleed edge. Trimming varies by a millimetre or two.
- **Minimum rule weight.** A hairline that survives print can vanish in a photograph of the sheet. Where a printed asset will also be photographed and forwarded — which in many markets is its main circulation — set rules at a weight that survives both, around 0.4mm rather than a true hairline.
- **Colour space.** Deliver in the printer's profile, and confirm any large flat field's build with them; a field converted naively from screen values bands on cheap stock.
- **Ink coverage.** A design that is mostly flat field costs more, dries slower and shows handling marks.

**Ask which media the asset lives in before composing.** An asset that is both handed out and photographed has two verification passes, not one, and the constraints conflict.
