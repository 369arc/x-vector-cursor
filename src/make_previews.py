#!/usr/bin/env python3
"""Render the README preview tiles from the committed XCursor themes.

Each tile is a 36x36 canvas: the 28 px cursor plus 4 px breathing room on
every side, upscaled 12x to 432x432 with nearest-neighbour so the pixel art
stays sharp.

Usage:
  python3 src/make_previews.py
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

from PIL import Image

from make_x_vector import VARIANTS

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"
PREVIEWS = ROOT / "previews"

NOMINAL = 28
CANVAS = 36
PADDING = 4
SCALE = 12

BACKGROUNDS = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "gray": (128, 128, 128, 255),
}


def decode_xcursor(path: Path, nominal: int) -> Image.Image:
    data = path.read_bytes()
    count = struct.unpack_from("<I", data, 12)[0]
    for index in range(count):
        _, size, offset = struct.unpack_from("<III", data, 16 + index * 12)
        if size != nominal:
            continue
        header = struct.unpack_from("<IIIIIIIII", data, offset)
        width, height = header[4], header[5]
        pixels = data[offset + 36:offset + 36 + width * height * 4]
        return Image.frombytes("RGBA", (width, height), pixels, "raw", "BGRA")
    raise SystemExit(f"{path}: no {nominal}px image")


def render(theme: str) -> None:
    slug = theme.lower()
    star = decode_xcursor(THEMES / theme / "cursors" / "default", NOMINAL)
    for name, background in BACKGROUNDS.items():
        tile = Image.new("RGBA", (CANVAS, CANVAS), background)
        tile.alpha_composite(star, (PADDING, PADDING))
        tile = tile.resize((CANVAS * SCALE, CANVAS * SCALE),
                           Image.Resampling.NEAREST)
        tile.save(PREVIEWS / f"{slug}-{name}.png")


def main() -> int:
    PREVIEWS.mkdir(exist_ok=True)
    for theme in VARIANTS:
        render(theme)
        print(f"rendered previews for {theme}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
