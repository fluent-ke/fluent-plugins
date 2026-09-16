#!/usr/bin/env python3
"""Create a new Pencil `.pen` file on disk, optionally seeded from a brand `.pen`.

Why this exists: the Pencil MCP can only act on the document the app already has
open, so an agent with no open file is stuck — it cannot create one. But `.pen`
is plain JSON, so a new file can be authored directly. Writing a file the app has
*never opened* is the one safe direct-to-disk write; the app then opens it and
the MCP takes over. Operating rules live in SKILL.md beside this script.

Usage
-----
    python3 new_pen.py "path/to/My Campaign - design.pen" \
        --artboard "POSTER Portrait:1080x1350" \
        --artboard "POSTER Square:1080x1080" \
        --brand "path/to/brand.pen"

    # no artboards, neutral tokens
    python3 new_pen.py "path/to/scratch.pen"

Options
-------
    --artboard NAME:WxH   Repeatable. Top-level frame, laid out left to right.
    --brand PATH          A brand `.pen` whose variables and reusable components are copied in.
    --no-components       Skip copying the brand's reusable components.
    --no-vars             Skip seeding brand variables (bare document).
    --force               Overwrite an existing file. Off by default, on purpose.

Cross-OS: Python 3 standard library only, no hardcoded paths. `python` on Windows.
"""

import argparse
import json
import os
import random
import string
import sys
import uuid

PEN_VERSION = "2.14"

# Neutral fallback, used when no brand file is given. Replace with the brand's own
# tokens by passing --brand.
FALLBACK_VARS = {
    "canvas": "#f7f7f5", "surface": "#ffffff", "surface-2": "#efefec",
    "ink": "#1c1c1a", "ink-2": "#4a4a46", "ink-3": "#76766f",
    "accent": "#2f5bea", "accent-ink": "#1f3fa8", "accent-tint": "#e3eafc",
    "border": "#e2e2dd", "success": "#3f7a52", "error": "#b3403a",
}
FALLBACK_FONTS = {
    "font-display": "Inter", "font-body": "Inter", "font-mono": "JetBrains Mono",
}

ID_ALPHABET = string.ascii_letters + string.digits


class IdFactory:
    """Pencil node ids: 5-6 chars, [A-Za-z0-9], unique within the document."""

    def __init__(self, taken=None):
        self.taken = set(taken or ())

    def new(self):
        while True:
            candidate = "".join(random.choice(ID_ALPHABET) for _ in range(5))
            if candidate not in self.taken:
                self.taken.add(candidate)
                return candidate

    def claim(self, node):
        """Register every id in an existing subtree so we never collide with it."""
        if isinstance(node, dict):
            if isinstance(node.get("id"), str):
                self.taken.add(node["id"])
            for child in node.get("children") or ():
                self.claim(child)


def load_brand(brand_path):
    """Return (variables, reusable_components) from a brand `.pen` file."""
    if not brand_path:
        return None, []
    if not os.path.isfile(brand_path):
        print("warn: brand file not found: %s; using fallback tokens" % brand_path,
              file=sys.stderr)
        return None, []
    try:
        with open(brand_path, encoding="utf-8") as handle:
            brand = json.load(handle)
    except (OSError, ValueError) as exc:
        print("warn: could not read brand file (%s); using fallback tokens" % exc,
              file=sys.stderr)
        return None, []
    components = [c for c in brand.get("children", []) if c.get("reusable")]
    return brand.get("variables"), components


def fallback_vars():
    variables = {name: {"type": "color", "value": value}
                 for name, value in FALLBACK_VARS.items()}
    variables.update({name: {"type": "string", "value": value}
                      for name, value in FALLBACK_FONTS.items()})
    return variables


def parse_artboard(spec):
    """'POSTER Portrait:1080x1350' -> ('POSTER Portrait', 1080, 1350)"""
    if ":" not in spec:
        raise argparse.ArgumentTypeError(
            "artboard must be NAME:WxH, got %r" % spec)
    name, _, size = spec.rpartition(":")
    dims = size.lower().split("x")
    if len(dims) != 2:
        raise argparse.ArgumentTypeError(
            "artboard size must be WxH, got %r" % size)
    try:
        width, height = int(dims[0]), int(dims[1])
    except ValueError:
        raise argparse.ArgumentTypeError("artboard size must be integers: %r" % size)
    if not name.strip():
        raise argparse.ArgumentTypeError("artboard needs a name: %r" % spec)
    return name.strip(), width, height


def build_document(artboards, variables, components, ids):
    children = []

    # Components first, parked off to the left of the artboard row. Keeping them
    # at the head of the layer list matches the brand file; anything `reusable`
    # parked at the *end* is what the presenting flow wants, but a design file
    # reads better with its components up top.
    x = -1200
    for component in components:
        clone = json.loads(json.dumps(component))  # deep copy; ids already claimed
        clone["x"] = x
        clone["y"] = 0
        children.append(clone)
        x += 200

    # Artboards laid out left to right with a consistent gutter.
    x = 0
    for name, width, height in artboards:
        children.append({
            "type": "frame",
            "id": ids.new(),
            "x": x,
            "y": 0,
            "name": name,
            "width": width,
            "height": height,
            "layout": "none",
            "clip": True,
            "fill": "$canvas" if variables and "canvas" in variables else "#f7f7f5",
            "children": [],
        })
        x += width + 200

    document = {"version": PEN_VERSION, "children": children,
                "fileToken": str(uuid.uuid4())}
    if variables:
        document["variables"] = variables
    return document


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Create a new Pencil .pen file, optionally seeded from a brand .pen.")
    parser.add_argument("output", help="path to the .pen file to create")
    parser.add_argument("--artboard", action="append", default=[],
                        type=parse_artboard, metavar="NAME:WxH",
                        help="top-level frame; repeatable")
    parser.add_argument("--brand", default=None, metavar="PATH",
                        help="brand .pen to copy variables and reusable components from")
    parser.add_argument("--no-components", action="store_true",
                        help="do not copy the brand's reusable components")
    parser.add_argument("--no-vars", action="store_true",
                        help="do not seed brand variables")
    parser.add_argument("--force", action="store_true",
                        help="overwrite an existing file")
    args = parser.parse_args(argv)

    output = args.output
    if not output.endswith(".pen"):
        output += ".pen"

    if os.path.exists(output) and not args.force:
        print("refusing to overwrite existing file: %s" % output, file=sys.stderr)
        print("  (if Pencil has it open, writing here would be silently lost anyway)",
              file=sys.stderr)
        return 1

    brand_vars, components = load_brand(args.brand)

    variables = None if args.no_vars else (brand_vars or fallback_vars())
    if not args.no_vars and brand_vars is None:
        print("note: no brand file used; seeded neutral fallback tokens", file=sys.stderr)
    if args.no_components:
        components = []

    ids = IdFactory()
    for component in components:
        ids.claim(component)

    document = build_document(args.artboard, variables, components, ids)

    parent = os.path.dirname(os.path.abspath(output))
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output, "w", encoding="utf-8") as handle:
        json.dump(document, handle, ensure_ascii=False, indent=1)

    # Round-trip check: a file Pencil cannot parse is worse than no file.
    with open(output, encoding="utf-8") as handle:
        json.load(handle)

    print("created %s" % output)
    print("  version   %s" % PEN_VERSION)
    print("  variables %d" % (len(variables) if variables else 0))
    print("  components %d (%s)" % (
        len(components), ", ".join(c.get("name", "?") for c in components) or "none"))
    print("  artboards %d" % len(args.artboard))
    for name, width, height in args.artboard:
        print("    %-28s %dx%d" % (name, width, height))
    print("\nNext: open it in Pencil, then drive it through the MCP.")
    print("Images referenced by a fill use a path relative to this .pen file"
          " (e.g. images/foo.png).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
