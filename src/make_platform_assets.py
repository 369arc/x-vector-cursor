#!/usr/bin/env python3
"""Generate Windows .cur files and macOS Mousecape .cape files.

The Linux XCursor themes are built by make_x_vector.py. Windows and macOS
use different cursor formats, so this script converts the same star geometry
to those formats.

Outputs:
  platforms/windows/<theme>/*.cur
  platforms/macos/<theme>.cape
"""

from __future__ import annotations

import copy
import plistlib
import struct
import sys
import zlib
from pathlib import Path

from make_x_vector import VARIANTS, not_allowed_image, star_image, text_image

ROOT = Path(__file__).resolve().parent.parent
WINDOWS = ROOT / "platforms" / "windows"
MACOS = ROOT / "platforms" / "macos"

WINDOWS_SIZES = (32, 48, 64)
MACOS_SCALES = (1, 2, 5, 10)
MACOS_POINTS = 28
MACOS_HOTSPOT = 14

# Common macOS cursor identifiers, from Mousecape's MCDefs.
MACOS_STAR_IDS = (
    "com.apple.coregraphics.Arrow",
    "com.apple.coregraphics.ArrowCtx",
    "com.apple.coregraphics.Alias",
    "com.apple.coregraphics.Copy",
    "com.apple.coregraphics.Move",
    "com.apple.coregraphics.Wait",
    "com.apple.cursor.2",   # Link
    "com.apple.cursor.7",   # Crosshair
    "com.apple.cursor.13",  # Pointing hand
    "com.apple.cursor.24",  # Context menu
    "com.apple.cursor.40",  # Help
    "com.apple.cursor.42",  # Zoom in
    "com.apple.cursor.43",  # Zoom out
)
MACOS_TEXT_IDS = (
    "com.apple.coregraphics.IBeam",
    "com.apple.coregraphics.IBeamXOR",
)
MACOS_BLOCKED_IDS = (
    "com.apple.cursor.3",   # Forbidden
)


def scale_to(pixels: bytearray, src_size: int, dst_size: int) -> bytearray:
    """Nearest-neighbour scaling that keeps the pixel-art edges crisp."""
    out = bytearray(dst_size * dst_size * 4)
    for y in range(dst_size):
        sy = y * src_size // dst_size
        src_row = sy * src_size * 4
        dst_row = y * dst_size * 4
        for x in range(dst_size):
            sx = x * src_size // dst_size
            src = src_row + sx * 4
            dst = dst_row + x * 4
            out[dst:dst + 4] = pixels[src:src + 4]
    return out


def png_bytes(width: int, height: int, pixels: bytearray) -> bytes:
    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    stride = width * 4
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filter: none
        raw.extend(pixels[y * stride:(y + 1) * stride])

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


def cur_dib(pixels: bytearray, size: int) -> bytes:
    mask_row = ((size + 31) // 32) * 4
    header = struct.pack(
        "<IiiHHIIiiII",
        40, size, size * 2, 1, 32, 0,
        size * size * 4 + mask_row * size, 0, 0, 0, 0,
    )
    xor = bytearray()
    mask = bytearray()
    for y in range(size - 1, -1, -1):
        row_mask = bytearray(mask_row)
        for x in range(size):
            i = (y * size + x) * 4
            r, g, b, a = pixels[i:i + 4]
            xor += bytes((b, g, r, a))
            if a == 0:
                row_mask[x // 8] |= 0x80 >> (x % 8)
        mask += row_mask
    return header + bytes(xor) + bytes(mask)


def write_cur(path: Path, images: list[tuple[int, bytearray]]) -> None:
    entries = bytearray()
    blobs = bytearray()
    offset = 6 + 16 * len(images)
    for size, pixels in images:
        blob = cur_dib(pixels, size)
        hotspot = size // 2
        entries += struct.pack(
            "<BBBBHHII",
            size, size, 0, 0, hotspot, hotspot, len(blob), offset,
        )
        blobs += blob
        offset += len(blob)
    path.write_bytes(struct.pack("<HHH", 0, 2, len(images)) + bytes(entries) + bytes(blobs))


def make_windows() -> None:
    for name, variant in VARIANTS.items():
        folder = WINDOWS / name
        folder.mkdir(parents=True, exist_ok=True)
        for old in folder.glob("*.cur"):
            old.unlink()

        star = [(size, star_image(size, variant.core, variant.outline,
                                  variant.geometry))
                for size in WINDOWS_SIZES]
        text_source = text_image(variant.text, 28)
        text = [(size, scale_to(text_source, 28, size)) for size in WINDOWS_SIZES]
        blocked = [(size, not_allowed_image(size, variant.core))
                   for size in WINDOWS_SIZES]

        write_cur(folder / "default.cur", star)
        write_cur(folder / "text.cur", text)
        write_cur(folder / "not-allowed.cur", blocked)
        print(f"created {folder}")


def macos_cursor(pixels: bytearray, points: int, hotspot: int) -> dict:
    representations = []
    for scale in MACOS_SCALES:
        size = points * scale
        representations.append(png_bytes(size, size, scale_to(pixels, points, size)))
    return {
        "FrameCount": 1,
        "FrameDuration": 1.0,
        "HotSpotX": float(hotspot),
        "HotSpotY": float(hotspot),
        "PointsHigh": float(points),
        "PointsWide": float(points),
        "Representations": representations,
    }


def make_macos() -> None:
    for name, variant in VARIANTS.items():
        star = macos_cursor(
            star_image(MACOS_POINTS, variant.core, variant.outline,
                       variant.geometry),
            MACOS_POINTS,
            MACOS_HOTSPOT,
        )
        text = macos_cursor(
            text_image(variant.text, MACOS_POINTS),
            MACOS_POINTS,
            MACOS_HOTSPOT,
        )
        blocked = macos_cursor(
            not_allowed_image(MACOS_POINTS, variant.core),
            MACOS_POINTS,
            MACOS_HOTSPOT,
        )

        cursors = {}
        for identifier in MACOS_STAR_IDS:
            cursors[identifier] = copy.deepcopy(star)
        for identifier in MACOS_TEXT_IDS:
            cursors[identifier] = copy.deepcopy(text)
        for identifier in MACOS_BLOCKED_IDS:
            cursors[identifier] = copy.deepcopy(blocked)

        cape = {
            "Author": "369arc",
            "CapeName": name,
            "CapeVersion": 1.0,
            "Cloud": False,
            "Cursors": cursors,
            "HiDPI": True,
            "Identifier": f"com.github.369arc.{name.lower().replace('-', '.')}",
            "MinimumVersion": 2.0,
            "Version": 2.0,
        }
        path = MACOS / f"{name}.cape"
        path.write_bytes(plistlib.dumps(cape, fmt=plistlib.FMT_BINARY, sort_keys=False))
        print(f"created {path}")


def main() -> int:
    WINDOWS.mkdir(parents=True, exist_ok=True)
    MACOS.mkdir(parents=True, exist_ok=True)
    make_windows()
    make_macos()
    return 0


if __name__ == "__main__":
    sys.exit(main())
