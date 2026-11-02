#!/usr/bin/env python3
"""Generate the X-Vector-Crosshair XCursor theme.

White, 1px crosshair on a black desktop:
  - four thin lines, no centre dot by default;
  - pointer/links get a small 2px centre dot;
  - text cursors keep a minimal I-beam;
  - no motion trail / click animation: XCursor cannot do that.
"""

from __future__ import annotations

import os
import shutil
import struct
import sys
import os
from pathlib import Path

CURSOR_OUTPUT = Path(os.environ.get("CURSOR_OUTPUT", str(Path.home() / ".local/share/icons")))
THEME = CURSOR_OUTPUT / "X-Vector-Crosshair"
CURSORS = THEME / "cursors"
SIZES = (24, 28, 32, 48, 64)

MAGIC = 0x72756358  # "Xcur"
IMAGE_TYPE = 0xFFFD0002


def blank(size: int) -> bytearray:
    return bytearray(size * size * 4)


def put(buf: bytearray, size: int, x: int, y: int, color: bytes = b"\xff\xff\xff\xff") -> None:
    if 0 <= x < size and 0 <= y < size:
        i = (y * size + x) * 4
        buf[i:i + 4] = color  # ARGB


def draw_x(buf: bytearray, size: int, length: int = 14) -> None:
    c = size // 2
    start = c - length // 2
    black = b"\x00\x00\x00\xff"
    for i in range(length):
        x = start + i
        y = start + i
        y2 = size - 1 - x
        put(buf, size, x, y, black)
        put(buf, size, x, y2, black)


def crosshair(size: int, dot: bool = False) -> bytearray:
    buf = blank(size)
    c = size // 2
    draw_x(buf, size, 14)
    gap = max(4, round(size * 0.16))
    length = max(5, round(size * 0.22))

    # top / bottom
    for y in range(c - gap - length, c - gap):
        put(buf, size, c, y)
    for y in range(c + gap, c + gap + length):
        put(buf, size, c, y)

    # left / right
    for x in range(c - gap - length, c - gap):
        put(buf, size, x, c)
    for x in range(c + gap, c + gap + length):
        put(buf, size, x, c)

    if dot:
        for y in (c - 1, c):
            for x in (c - 1, c):
                put(buf, size, x, y)
    return buf


def text_cursor(canvas: int = 28) -> bytearray:
    """Black-white-black sandwich, 8 px shorter than the nominal cursor."""
    buf = blank(canvas)
    c = canvas // 2
    top = 4
    bottom = canvas - 5
    for y in range(top, bottom + 1):
        put(buf, canvas, c - 1, y, b"\x00\x00\x00\xff")
        put(buf, canvas, c, y, b"\xff\xff\xff\xff")
        put(buf, canvas, c + 1, y, b"\x00\x00\x00\xff")
    return buf


def not_allowed(size: int) -> bytearray:
    buf = blank(size)
    c = size / 2.0
    r = size * 0.30
    for y in range(size):
        for x in range(size):
            dx, dy = x - c + 0.5, y - c + 0.5
            d = (dx * dx + dy * dy) ** 0.5
            if abs(d - r) < 0.7:
                put(buf, size, x, y)
    for i in range(size):
        x = round(c - r / 2**0.5 + i * (r * 2**0.5) / size)
        y = round(c - r / 2**0.5 + i * (r * 2**0.5) / size)
        put(buf, size, x, y)
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
            36,          # image header length
            IMAGE_TYPE,
            nominal,     # nominal size
            1,           # image version
            width,
            height,
            width // 2,  # xhot
            height // 2, # yhot
            0,           # delay (static)
        )
        chunks += chunk + bytes(pixels)
        offset += len(chunk) + len(pixels)
    header = struct.pack("<IIII", MAGIC, 16, 0x00010000, ntoc)
    return bytes(header + toc + chunks)


def write_cursor(name: str, factory) -> None:
    path = CURSORS / name
    path.write_bytes(xcursor([(s, s, s, factory(s)) for s in SIZES]))


def write_text_cursor() -> None:
    write_cursor("text", text_cursor)


def main() -> int:
    if THEME.exists():
        shutil.rmtree(THEME)
    CURSORS.mkdir(parents=True)

    (THEME / "index.theme").write_text(
        "[Icon Theme]\n"
        "Name=X-Vector-Crosshair\n"
        "Comment=White crosshair cursor for a black desktop\n"
        "Inherits=hicolor\n"
    )
    (THEME / "cursor.theme").write_text(
        "[Icon Theme]\n"
        "Name=X-Vector-Crosshair\n"
        "Inherits=hicolor\n"
    )

    write_cursor("default", lambda s: crosshair(s, dot=False))
    write_cursor("pointer", lambda s: crosshair(s, dot=True))
    write_text_cursor()
    write_cursor("not-allowed", not_allowed)

    aliases = {
        # default / arrow
        "left_ptr": "default",
        "arrow": "default",
        "top_left_arrow": "default",
        "top_left_corner": "default",
        "crosshair": "default",
        "cross": "default",
        "cell": "default",
        "move": "default",
        "all-scroll": "default",
        "col-resize": "default",
        "row-resize": "default",
        "n-resize": "default",
        "s-resize": "default",
        "e-resize": "default",
        "w-resize": "default",
        "ne-resize": "default",
        "nw-resize": "default",
        "se-resize": "default",
        "sw-resize": "default",
        "ew-resize": "default",
        "ns-resize": "default",
        "nesw-resize": "default",
        "nwse-resize": "default",
        "zoom-in": "default",
        "zoom-out": "default",
        "context-menu": "default",
        "help": "default",
        "wait": "default",
        "progress": "default",
        # clickable / links
        "hand1": "pointer",
        "hand2": "pointer",
        "link": "pointer",
        "alias": "pointer",
        # text
        "xterm": "text",
        "vertical-text": "text",
        # forbidden
        "no-drop": "not-allowed",
        "forbidden": "not-allowed",
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
