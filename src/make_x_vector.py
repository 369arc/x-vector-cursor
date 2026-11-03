#!/usr/bin/env python3
"""Generate the X-Vector XCursor themes.

Eight-point star:
  - main vertical/horizontal axes: size - 4 px;
  - diagonals: half the cursor size;
  - 1 px core + 1 px outline in opposite tones;
  - Meta variants use rhombic axial beads; Link also bridges the four
    axial separators so the arms meet the centre;
  - text cursor: a three-stripe vertical sandwich, 8 px shorter.
No motion trail or click animation: XCursor cannot do that.

Usage:
  python3 make_x_vector.py X-Vector
  python3 make_x_vector.py X-Vector-Inverse
  python3 make_x_vector.py X-Vector-Meta
  python3 make_x_vector.py X-Vector-Meta-Inverse
  python3 make_x_vector.py X-Vector-Meta-Link
  python3 make_x_vector.py X-Vector-Meta-Link-Inverse
"""

from __future__ import annotations

import argparse
import os
import shutil
import struct
import sys
from dataclasses import dataclass
from pathlib import Path

CURSOR_OUTPUT = Path(os.environ.get("CURSOR_OUTPUT", str(Path.home() / ".local/share/icons")))
SIZES = (24, 28, 32, 48, 64)

MAGIC = 0x72756358
IMAGE_TYPE = 0xFFFD0002
WHITE = b"\xff\xff\xff\xff"
BLACK = b"\x00\x00\x00\xff"


@dataclass(frozen=True)
class Variant:
    core: bytes
    outline: bytes
    text: tuple[bytes, bytes, bytes]
    comment: str
    geometry: str = "classic"


VARIANTS = {
    "X-Vector": Variant(
        core=WHITE,
        outline=BLACK,
        text=(BLACK, WHITE, BLACK),
        comment="White eight-point star with black outline",
    ),
    "X-Vector-Inverse": Variant(
        core=BLACK,
        outline=WHITE,
        text=(WHITE, BLACK, WHITE),
        comment="Black eight-point star with white outline",
    ),
    "X-Vector-Meta": Variant(
        core=WHITE,
        outline=BLACK,
        text=(BLACK, WHITE, BLACK),
        comment="White eight-point star with rhombic axes and black outline",
        geometry="meta",
    ),
    "X-Vector-Meta-Inverse": Variant(
        core=BLACK,
        outline=WHITE,
        text=(WHITE, BLACK, WHITE),
        comment="Black eight-point star with rhombic axes and white outline",
        geometry="meta",
    ),
    "X-Vector-Meta-Link": Variant(
        core=WHITE,
        outline=BLACK,
        text=(BLACK, WHITE, BLACK),
        comment="White eight-point star with linked rhombic axes and black outline",
        geometry="meta-link",
    ),
    "X-Vector-Meta-Link-Inverse": Variant(
        core=BLACK,
        outline=WHITE,
        text=(WHITE, BLACK, WHITE),
        comment="Black eight-point star with linked rhombic axes and white outline",
        geometry="meta-link",
    ),
}


def blank(size: int) -> bytearray:
    return bytearray(size * size * 4)


def put(buf: bytearray, size: int, x: int, y: int, color: bytes) -> None:
    if 0 <= x < size and 0 <= y < size:
        i = (y * size + x) * 4
        buf[i:i + 4] = color


def line(buf: bytearray, size: int, x0: int, y0: int, x1: int, y1: int,
         color: bytes, thickness: int = 1) -> None:
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    r = thickness // 2
    while True:
        for ox in range(-r, r + 1):
            for oy in range(-r, r + 1):
                put(buf, size, x0 + ox, y0 + oy, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def star_image(size: int, core: bytes, outline: bytes,
               geometry: str = "classic") -> bytearray:
    if geometry == "meta":
        return meta_image(size, core, outline)
    if geometry == "meta-link":
        return meta_link_image(size, core, outline)
    buf = blank(size)
    c = size // 2
    main = size - 4
    diag = max(8, size // 2)
    mh = main // 2
    dh = diag // 2

    arms = [
        ((c, c - mh), (c, c + mh)),       # vertical
        ((c - mh, c), (c + mh, c)),       # horizontal
        ((c - dh, c - dh), (c + dh, c + dh)),  # diagonal
        ((c - dh, c + dh), (c + dh, c - dh)),  # diagonal
    ]

    # Outline first, then the core on top.
    for a, b in arms:
        line(buf, size, a[0], a[1], b[0], b[1], outline, thickness=3)
    for a, b in arms:
        line(buf, size, a[0], a[1], b[0], b[1], core, thickness=1)
    return buf


def meta_image(size: int, core: bytes, outline: bytes) -> bytearray:
    """Eight-point star with rhombic horizontal and vertical axes.

    The diagonals are the classic X staircase. The axial cores are chains of
    whole-pixel rhombi: at 28 px a rotated 1x1 square is smaller than one
    pixel, so it would average to gray, while |dx| + |dy| <= 1 is the smallest
    rhombus that stays solid. The centre is the union of a square and a
    rhombus, an eight-point figure.
    """
    buf = blank(size)
    c = size // 2
    mh = (size - 4) // 2
    dh = max(8, size // 2) // 2
    scale = size / 28.0

    def scaled(value: int, minimum: int) -> int:
        return max(minimum, round(value * scale))

    center_sq = scaled(1, 1)
    center_dia = scaled(2, 2)
    bead_r = scaled(1, 1)
    step = scaled(3, 3)
    first = center_dia + bead_r + 2
    last = mh - bead_r

    def square(cx: int, cy: int, r: int, color: bytes) -> None:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                put(buf, size, x, y, color)

    def diamond(cx: int, cy: int, r: int, color: bytes) -> None:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if abs(x - cx) + abs(y - cy) <= r:
                    put(buf, size, x, y, color)

    # Outline first, then the core on top.
    line(buf, size, c - dh, c - dh, c + dh, c + dh, outline, thickness=3)
    line(buf, size, c - dh, c + dh, c + dh, c - dh, outline, thickness=3)
    square(c, c, center_sq + 1, outline)
    diamond(c, c, center_dia + 1, outline)
    for d in range(first, last + 1, step):
        for sx, sy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            diamond(c + sx * d, c + sy * d, bead_r + 1, outline)

    line(buf, size, c - dh, c - dh, c + dh, c + dh, core, thickness=1)
    line(buf, size, c - dh, c + dh, c + dh, c - dh, core, thickness=1)
    square(c, c, center_sq, core)
    diamond(c, c, center_dia, core)
    for d in range(first, last + 1, step):
        for sx, sy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            diamond(c + sx * d, c + sy * d, bead_r, core)
    return buf


def meta_link_image(size: int, core: bytes, outline: bytes) -> bytearray:
    """Meta with the four axial separators bridged by one core pixel.

    The bridge sits at the outer edge of the centre outline. It merges the
    four cardinal points of the centre with the axial rays, so the arms read
    as connected. The diagonal points and the outer contour are unchanged.
    """
    buf = meta_image(size, core, outline)
    scale = size / 28.0
    center_dia = max(2, round(2 * scale))
    c = size // 2
    bridge = center_dia + 1
    for x, y in (
        (c - bridge, c),
        (c + bridge, c),
        (c, c - bridge),
        (c, c + bridge),
    ):
        put(buf, size, x, y, core)
    return buf


def text_image(colors: tuple[bytes, bytes, bytes], canvas: int = 28) -> bytearray:
    left, middle, right = colors
    buf = blank(canvas)
    c = canvas // 2
    top = 4
    bottom = canvas - 5
    for y in range(top, bottom + 1):
        put(buf, canvas, c - 1, y, left)
        put(buf, canvas, c, y, middle)
        put(buf, canvas, c + 1, y, right)
    return buf


def not_allowed_image(size: int, color: bytes) -> bytearray:
    buf = blank(size)
    c = size / 2.0
    r = size * 0.30
    for y in range(size):
        for x in range(size):
            dx, dy = x - c + 0.5, y - c + 0.5
            d = (dx * dx + dy * dy) ** 0.5
            if abs(d - r) < 0.7:
                put(buf, size, x, y, color)
    for i in range(size):
        x = round(c - r / 2**0.5 + i * (r * 2**0.5) / size)
        y = round(c - r / 2**0.5 + i * (r * 2**0.5) / size)
        put(buf, size, x, y, color)
    return buf


def xcursor(images: list[tuple[int, int, int, bytearray]]) -> bytes:
    ntoc = len(images)
    offset = 16 + ntoc * 12
    toc = bytearray()
    chunks = bytearray()
    for nominal, width, height, pixels in images:
        toc += struct.pack("<III", IMAGE_TYPE, nominal, offset)
        chunk = struct.pack(
            "<IIIIIIIII",
            36, IMAGE_TYPE, nominal, 1, width, height,
            width // 2, height // 2, 0,
        )
        chunks += chunk + bytes(pixels)
        offset += len(chunk) + len(pixels)
    return struct.pack("<IIII", MAGIC, 16, 0x00010000, ntoc) + bytes(toc + chunks)


def write_cursor(cursors: Path, name: str, factory, special: bool = False) -> None:
    if special:
        pixels = factory(28)
        images = [(s, 28, 28, pixels) for s in SIZES]
    else:
        images = [(s, s, s, factory(s)) for s in SIZES]
    (cursors / name).write_bytes(xcursor(images))


def populate_aliases(cursors: Path) -> None:
    aliases = {
        "left_ptr": "default", "arrow": "default", "top_left_arrow": "default",
        "crosshair": "default", "cross": "default", "cell": "default",
        "move": "default", "all-scroll": "default",
        "col-resize": "default", "row-resize": "default",
        "n-resize": "default", "s-resize": "default",
        "e-resize": "default", "w-resize": "default",
        "ne-resize": "default", "nw-resize": "default",
        "se-resize": "default", "sw-resize": "default",
        "ew-resize": "default", "ns-resize": "default",
        "nesw-resize": "default", "nwse-resize": "default",
        "zoom-in": "default", "zoom-out": "default",
        "context-menu": "default", "help": "default",
        "wait": "default", "progress": "default",
        "hand1": "pointer", "hand2": "pointer", "link": "pointer", "alias": "pointer",
        "xterm": "text", "vertical-text": "text",
        "no-drop": "not-allowed", "forbidden": "not-allowed",
    }
    for alias, target in aliases.items():
        link = cursors / alias
        try:
            link.symlink_to(target)
        except FileExistsError:
            link.unlink()
            link.symlink_to(target)


def main(theme_name: str) -> int:
    variant = VARIANTS[theme_name]
    theme = CURSOR_OUTPUT / theme_name
    cursors = theme / "cursors"

    if theme.exists():
        shutil.rmtree(theme)
    cursors.mkdir(parents=True)

    (theme / "index.theme").write_text(
        f"[Icon Theme]\nName={theme_name}\n"
        f"Comment={variant.comment}\n"
        "Inherits=hicolor\n"
    )
    (theme / "cursor.theme").write_text(
        f"[Icon Theme]\nName={theme_name}\nInherits=hicolor\n"
    )

    write_cursor(cursors, "default",
                 lambda s: star_image(s, variant.core, variant.outline,
                                      variant.geometry))
    write_cursor(cursors, "pointer",
                 lambda s: star_image(s, variant.core, variant.outline,
                                      variant.geometry))
    write_cursor(cursors, "text", lambda s: text_image(variant.text, s), special=True)
    write_cursor(cursors, "not-allowed", lambda s: not_allowed_image(s, variant.core))

    populate_aliases(cursors)

    print(f"created {theme} with {len(list(cursors.iterdir()))} cursors")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate X-Vector XCursor themes.")
    parser.add_argument("theme", nargs="?", default="X-Vector", choices=VARIANTS)
    return parser.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main(parse_args(sys.argv[1:]).theme))
