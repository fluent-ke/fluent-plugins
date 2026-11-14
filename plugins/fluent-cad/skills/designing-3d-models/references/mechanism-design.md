# Mechanism design for printed parts

*Contributed by Samwel Tinega from his project work.*

Notes from real mechanism projects, kept as patterns rather than fixed specs
— every dimension below needs re-deriving for the user's own motor, spring,
and load.

## Lever + spring-return mechanism (e.g. a bionic-arm finger)

- A small stepper (e.g. NEMA 17, small driver, 12 V) drives a lever that
  pulls the mechanism closed. A limit switch defines zero; on release the
  stepper returns to zero and a **torsional spring** opens the mechanism
  back up.
- Design for: lever arm length vs. motor torque, spring preload that is
  small enough for the motor to overcome, hard stops, and a home position
  set by the limit switch.
- Print hinges/pins as separate parts, or print-in-place with 0.3 mm or
  larger clearance **(general practice — tune per printer/tolerance)**; use
  metal pins for load-bearing joints rather than printed pins.
- Control side: simulate the microcontroller logic (e.g. in Wokwi for an
  ESP32) before wiring the real hardware.

## Suspended (gimbal-style) holder (e.g. a car cup holder)

- Concept: a holder that stays level, hung from pivots inside a recess
  (reference pattern: a "gimbal" cup holder video/design).
- Start from measurements of the recess (a top-down photo plus tape
  measurements), then design: the outer frame to fit the recess, an inner
  ring on a pivot axis, and a cradle hung below the pivot so gravity keeps
  it upright.
- Add damping or friction at the pivots so it does not swing excessively;
  check clearance for the range of object sizes it needs to hold and for
  the pivot's swing range.

## Printing mechanism parts

- Orient to keep layers across the load direction, not just for a flat
  first layer — see `printing-3d-models`, step 3, Orient.
- Hole tolerance: print holes that must accept a pin or cord 0.1–0.3 mm
  oversize.
- Fit test before committing to a batch: print one copy, check fit, then
  feed any measured error back into the model's parameters (not into a
  scaled mesh) — see `printing-3d-models`, step 8, Log it.
