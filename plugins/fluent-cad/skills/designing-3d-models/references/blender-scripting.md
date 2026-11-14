# Blender via Python scripts

*Contributed by Samwel Tinega from his project work.*

For organic/sculpted shapes (the "Organic shape" row in the skill's routing table), do the modelling through complete, runnable Python
(`bpy`) scripts rather than manual clicking — especially when the user is
newer to Blender than to CAD. Explain how to run the script in a sentence or
two (Scripting workspace -> New -> paste -> Run Script), not a tutorial.

Compiled from real project work: an elephant clay charm/cutter, a
bionic-arm finger mechanism, and a suspended car cup holder.

## Working style

- Always work in **millimetres**. Set the scene unit scale so 1 Blender unit
  = 1 mm (or state clearly if 1 BU = 1 m and scale on export).
- Treat reference images and spec sheets as the source of truth for
  dimensions (e.g. "16 mm wide, 18 mm tall, 3 mm thick, 4 mm hole"). Re-state
  the extracted dimensions before modelling so the user can correct them.
- Offer **numbered versions** (v1, v2) when the shape is subjective; the
  user picks one and iterates on it.
- Deliver output files (STL/STEP/.blend/.py) every time, not just the
  script.

## Build pattern (worked example: a 3 mm clay charm)

1. Clear the scene and set units/scale.
2. Build the silhouette from primitives (ellipsoids/cylinders for body,
   head, ears, legs, trunk, tail, etc.) or from a traced 2D outline, then
   join/boolean-union them.
3. Extrude/solidify to the spec thickness (about 3 mm for a small charm).
4. **Flat back**: keep one face planar (cut with a boolean, or scale the
   back vertices to a single Z plane) so it prints flat and presses cleanly.
5. Add any hole (e.g. a hanging hole) with a cylinder boolean (difference)
   at the specified diameter.
6. Smooth the front (subdivision or bevel) without changing the overall
   bounding box; verify dimensions after modifiers are applied.
7. Check: manifold (no holes/non-manifold edges), normals outward, bounding
   box equals the spec, no loose parts.
8. Export STL (and keep the `.blend` for later edits).

Script tips:

- Apply modifiers (`bpy.ops.object.modifier_apply`) before export.
- Use `bmesh` or the Boolean modifier with the exact solver for clean
  booleans.
- Name objects and parameters at the top of the script (`WIDTH`, `HEIGHT`,
  `THICKNESS`, `HOLE_D`) so the user can tweak and re-run.

## Editing a user-supplied STL

Example: filling a hanging hole and thickening the flat back by 2 mm on an
existing STL.

- Import the STL, inspect its bounding box and which axis is the "back".
- **Fill a hole**: add a cylinder slightly larger than the hole through the
  same axis and boolean-union, then clean up.
- **Thicken the back**: extrude the back-face vertices outward by the
  requested amount (or union a slab matching the outline), keeping the face
  flat.
- Re-check manifoldness (`admesh`, step 5 of the skill), re-export STL,
  and report the new overall dimensions.

## Moving to CAD (Onshape / STEP)

- Users adding further parametric features often want **STEP**, not a mesh.
- Blender exports meshes (STL/OBJ), not true STEP solids. A STEP made from
  an STL is a faceted mesh-to-solid conversion — say so plainly, and choose
  the conversion route (e.g. FreeCAD mesh-to-shape-to-solid, or importing the
  STL into Onshape directly) based on what the user needs to edit
  afterwards. If clean parametric features are needed, rebuild the part in
  CAD using the mesh as a reference, rather than relying on the converted
  solid.
- Keep consistent mm units across tools when a part moves between Blender
  and CAD (e.g. block STLs for simulation work coming from Onshape).

## Deliverables convention

For each part, provide: the generating script (`.py`), the `.blend`, the
STL, and the STEP (with the mesh-to-solid caveat above if it is
mesh-derived), plus a short note listing final dimensions — this is the
Blender-specific version of the `README.md` convention in the main
SKILL.md's design "Record" step.
