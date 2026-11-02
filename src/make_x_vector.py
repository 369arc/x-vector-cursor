#!/usr/bin/env python3
"""Generate the X-Vector XCursor theme.

Eight-point star:
  - main vertical/horizontal axes: size - 2 px;
  - diagonals: half the cursor size;
  - white 1 px core + black 1 px outline;
  - text cursor: black/white/black vertical sandwich, 8 px shorter.
No motion trail or click animation: XCursor cannot do that.
"""

from __future__ import annotations

import shutil
import struct
import sys
import os
from pathlib import Path

CURSOR_OUTPUT = Path(os.environ.get("CURSOR_OUTPUT", str(Path.home() / ".local/share/icons")))
THEME = CURSOR_OUTPUT / "X-Vector"
CURSORS = THEME / "cursors"
SIZES = (24, 28, 32, 48, 64)

MAGIC = 0x72756358
IMAGE_TYPE = 0xFFFD0002
WHITE = b"\xff\xff\xff\xff"
BLACK = b"\x00\x00\x00\xff"


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


def star_image(size: int) -> bytearray:
    buf = blank(size)
    c = size // 2
    main = size - 2
    diag = max(8, size // 2)
    mh = main // 2
    dh = diag // 2

    arms = [
        ((c, c - mh), (c, c + mh)),       # vertical
        ((c - mh, c), (c + mh, c)),       # horizontal
        ((c - dh, c - dh), (c + dh, c + dh)),  # diagonal
        ((c - dh, c + dh), (c + dh, c - dh)),  # diagonal
    ]

    # black outline first, then white core
    for a, b in arms:
        line(buf, size, a[0], a[1], b[0], b[1], BLACK, thickness=3)
    for a, b in arms:
        line(buf, size, a[0], a[1], b[0], b[1], WHITE, thickness=1)
    return buf


def text_image(canvas: int = 28) -> bytearray:
    buf = blank(canvas)
    c = canvas // 2
    top = 4
    bottom = canvas - 5
    for y in range(top, bottom + 1):
        put(buf, canvas, c - 1, y, BLACK)
        put(buf, canvas, c, y, WHITE)
        put(buf, canvas, c + 1, y, BLACK)
    return buf


def not_allowed_image(size: int) -> bytearray:
    buf = blank(size)
    c = size / 2.0
    r = size * 0.30
    for y in range(size):
        for x in range(size):
            dx, dy = x - c + 0.5, y - c + 0.5
            d = (dx * dx + dy * dy) ** 0.5
            if abs(d - r) < 0.7:
                put(buf, size, x, y, WHITE)
    for i in range(size):
        x = round(c - r / 2**0.5 + i * (r * 2**0.5) / size)
        y = round(c - r / 2**0.5 + i * (r * 2**0.5) / size)
        put(buf, size, x, y, WHITE)
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


def write_cursor(name: str, factory, special: bool = False) -> None:
    if special:
        pixels = factory(28)
        images = [(s, 28, 28, pixels) for s in SIZES]
    else:
        images = [(s, s, s, factory(s)) for s in SIZES]
    (CURSORS / name).write_bytes(xcursor(images))


def main() -> int:
    if THEME.exists():
        shutil.rmtree(THEME)
    CURSORS.mkdir(parents=True)
    (THEME / "index.theme").write_text(
        "[Icon Theme]\nName=X-Vector\n"
        "Comment=Eight-point star cursor for a black desktop\n"
        "Inherits=hicolor\n"
    )
    (THEME / "cursor.theme").write_text(
        "[Icon Theme]\nName=X-Vector\nInherits=hicolor\n"
    )

    write_cursor("default", star_image)
    write_cursor("pointer", star_image)
    write_cursor("text", text_image, special=True)
    write_cursor("not-allowed", not_allowed_image)

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
        link = CURSORS / alias
        try:
            link.symlink_to(target)
        except FileExistsError:
            link.unlink()
            link.symlink_to(target)

    print(f"created {THEME} with {len(list(CURSORS.iterdir()))} cursors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
