# Posters, campaign and social creative in Pencil

Read after `SKILL.md`. This is the mechanics. Visual taste — palette, type, imagery — belongs to whatever design-preferences doc your team keeps.

## Where files live

- **The brand system file stays closed and read-only.** Work in the campaign's own file. Opening the brand file to "just check" is how it gets edited.
- **Campaign creative lives in that campaign's own working folder**, never back in the shared assets folder. This has already gone wrong once: a shared file was forked into a campaign, both copies were edited, and they diverged silently.
- An `images/` folder sits **beside the `.pen`**, because image `url`s resolve relative to the `.pen` file's own directory.
- Partner or client assets come from the shared reference location unchanged; copies that get edited stop being reference.

## Take geometry from the source, never from looking

Before rebuilding any brand element, open the canonical asset and read the numbers out of it. A logo eyeballed from a screenshot will be subtly wrong in a way nobody catches until it is printed: one mark built as a tidy 2×2 grid of circles should have been four *overlapping* circles at centre spacing = diameter × 0.833, and the wrong version is still baked into a deck component.

The scaffolder in `SKILL.md` avoids this entirely by copying components out of the brand file rather than recreating them.

## Canvas sizes come from the brief

Placement dimensions (feed square, story, landscape, each ad variant) change with the platforms and are **not** listed here — a stale hardcoded number is worse than none. Take them from the campaign brief, the previous campaign's `.pen`, or the current platform spec, and confirm before building. A whole matrix rebuilt at the wrong size is the expensive version of this mistake.

## Masters first, then derive

1. Build and approve **one master per composition** — not per output size. Square, story and landscape are genuinely different compositions; an ad variant is usually a derivation of one of them.
2. Only then copy into the size matrix.

Doing it the other way means every later change is edited N times. When a shared change is needed mid-matrix, fix the masters and re-derive rather than sweeping copies.

## Sizes are not scales

A story crop is not a square with different numbers — the composition changes. Re-place the panel and re-check the subject in each size. Reuse the *system* (type scale, panel treatment, mark placement), not the coordinates.

## Images

- Image fills have **no crop or offset**. To reframe a subject, oversize the image rect inside a `clip: true` parent and offset it. The structural check reports "partially clipped" — intended.
- `Generate` is asynchronous. Fire the generations for a batch, do other work, then screenshot.
- **The subject must stay visible.** Text and panels sit in the negative space. If the subject is cropped out or covered, fix the crop, not the copy.
- **Before writing any `Generate` prompt, fill the four required slots** in the designing-visual-assets skill's Image section: cast including background figures, object anatomy for any device in shot, screen content, and the negative space the layout needs. Leaving them unnamed is what puts a laptop screen outside or behind its own lid, and a miscast crowd behind a correctly-cast subject. Both have shipped more than once. That skill owns the list; this line exists so you meet it at the moment you call `Generate`.
- **`Generate` on a node that already has an image orphans the old file** in `images/` rather than replacing it, and a batch fired in one call **does not land in the order you fired it**. Read the fill `url` back off each node before mapping files to boards; newest-by-mtime is not a safe proxy.

## Text that must not wrap

A text node at fixed `x`/`y` with a fixed `width` wraps inside its own box and collides with whatever sits at the next fixed `y`. This is invisible to a structural check and has shipped twice. For fixed-position lines, width-check before placing — for a heavy grotesque at weight 700, advance is roughly **0.55 × font size per character**, about **0.62** in caps. Shrink until every line fits, or measure your own face rather than trusting those numbers.

## Logos

Prefer **SVG paths over bitmaps**. Single-path `currentColor` icons drop straight in as `{type:"path", geometry:d, viewBox:[0,0,24,24], fill:"$token", fillRule:"evenodd"}` and tint to a design token with no recolouring step. Recoloured PNGs are the fallback, not the default.

Never fabricate a logo. If an authentic mark isn't available, set the name as a wordmark in the display face and say so — a wrong logo in front of the brand's own audience is worse than no logo.

## Exporting

- `export_nodes` failed above **4 node IDs per call** when this was hit. Its successor, `Export([ids], format, dir)` inside `execute`, took five ids in one call on 2026-09-07 without complaint, so treat the ceiling as an `export_nodes`-era observation and test before assuming it. Argument shape: `SKILL.md`'s API table.
- It fails with a misleading *"probably referencing the wrong .pen file"* when the output directory doesn't exist. `mkdir -p` first.
- **Export filenames become downstream identifiers.** Keep them ASCII, lowercase, hyphenated and descriptive. Pencil's default frame names contain `·` and `×`, which mangle in URLs and analytics — and on one paid-ads set the export stems became the ad names verbatim. Export to your own stems (`brand-campaign-placement-variant.png`), never off frame names.
- If the desktop export path errors on a file, the CLI exports headlessly — see `SKILL.md`.

## Parallel subagents

A size matrix parallelises well: one agent per size or per composition, each given **exact node IDs** and a hard boundary. The two rules from `SKILL.md` apply hardest here — name the layer not the effect, and mark human-fixed nodes untouchable in every brief.
