# One-part press moulds (e.g. clay)

*Contributed by Samwel Tinega from his project work.*

For pressing a small part's shape into a soft material (clay, etc.):

1. Create a solid block larger than the part with a margin (a few mm of
   wall all round).
2. Place the part so its **flat back** is on the open face of the cavity
   (the clay is pressed into the cavity, the flat back becomes the open
   side).
3. Boolean-difference the part from the block to get the **cavity
   (negative)**.
4. Add draft/taper or a slight rounding so the pressed material releases;
   avoid undercuts (thin protruding features like a trunk or ears must not
   trap material).
5. A pin feature in the cavity makes a hole (e.g. a hanging hole) directly
   when pressed — no separate drilling step.
6. Export the mould as STL (to print) and, if asked, a STEP of the cavity.
7. Allow for shrinkage of the material as it dries/cures **(general
   practice — confirm the material's actual shrinkage before relying on
   this)**: scale the cavity up a few percent if final size matters.

## Printing the mould

- Print with a smooth bed face for the pressing surface; sand or seal if the
  pressed material sticks.
- The `printing-3d-models` skill covers orientation, supports and first-layer
  checks for any print, mould included.
