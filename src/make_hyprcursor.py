#!/usr/bin/env python3
"""Add native Hyprland hyprcursor data to the X-Vector XCursor themes.

Every theme keeps its XCursor ``cursors/`` tree for GTK, Qt and XWayland,
and gains a ``manifest.hl`` + ``hyprcursors/*.hlc`` tree for Hyprland.
The SVG is generated from the same 28 px pixel map, so the native cursor
is the same crisp pixel art rather than a resampled bitmap.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from make_x_vector import (
    ALIASES,
    BLACK,
    VARIANTS,
    WHITE,
    not_allowed_image,
    star_image,
    text_image,
)

CURSOR_OUTPUT = Path(os.environ.get(
    "CURSOR_OUTPUT", str(Path.home() / ".local/share/icons")))
SIZE = 28


def svg_from_pixels(pixels: bytearray, size: int = SIZE) -> str:
    rects: list[str] = []
    for y in range(size):
        for x in range(size):
            i = (y * size + x) * 4
            if not pixels[i + 3]:
                continue
            color = "#%02x%02x%02x" % (
                pixels[i], pixels[i + 1], pixels[i + 2])
            rects.append(
                f'  <rect x="{x}" y="{y}" width="1" height="1" '
                f'fill="{color}"/>')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
        'shape-rendering="crispEdges">\n'
        + "\n".join(rects)
        + "\n</svg>\n"
    )


def write_shape(work: Path, name: str, pixels: bytearray,
                overrides: list[str]) -> None:
    shape_dir = work / "hyprcursors" / name
    shape_dir.mkdir(parents=True)
    (shape_dir / "image.svg").write_text(svg_from_pixels(pixels))
    (shape_dir / "meta.hl").write_text(
        "resize_algorithm = nearest\n"
        "hotspot_x = 0.5\n"
        "hotspot_y = 0.5\n"
        "nominal_size = 1.0\n"
        "define_size = 0, image.svg\n"
        "define_override = " + ";".join(overrides) + "\n"
    )


def overrides_for(target: str) -> list[str]:
    return [
        alias for alias, dest in ALIASES.items()
        if dest == target
    ]


def normalize_hlc(path: Path) -> None:
    """Rewrite a .hlc zip with fixed timestamps for reproducible builds."""
    with zipfile.ZipFile(path) as source:
        entries = [
            (info.filename, source.read(info.filename))
            for info in source.infolist()
        ]
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as out:
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            out.writestr(info, data)


def build_theme(theme_name: str) -> None:
    variant = VARIANTS[theme_name]
    target = CURSOR_OUTPUT / theme_name
    if not target.exists():
        raise SystemExit(f"{target} does not exist; run make_x_vector.py first")

    default_overrides = overrides_for("default") + overrides_for("pointer")
    default_overrides.append("pointer")
    text_overrides = overrides_for("text")
    blocked_overrides = overrides_for("not-allowed")

    with tempfile.TemporaryDirectory(prefix="x-vector-hypr-") as tmp:
        tmp_path = Path(tmp)
        work = tmp_path / "work"
        compiled = tmp_path / "compiled"
        work.mkdir()
        compiled.mkdir()

        (work / "manifest.hl").write_text(
            "cursors_directory = hyprcursors\n"
            f"name = {theme_name}\n"
            "version = 1.0\n"
            f"description = {variant.comment}\n"
            "author = X-Vector\n"
        )

        write_shape(
            work, "default",
            star_image(SIZE, variant.core, variant.outline, variant.geometry),
            default_overrides,
        )
        write_shape(
            work, "text", text_image(variant.text, SIZE), text_overrides)
        write_shape(
            work, "not-allowed",
            not_allowed_image(SIZE, variant.core), blocked_overrides)

        subprocess.run(
            ["hyprcursor-util", "-c", str(work), "-o", str(compiled)],
            check=True,
        )
        produced = compiled / f"theme_{theme_name}"
        if not produced.is_dir():
            raise SystemExit(f"hyprcursor-util did not create {produced}")

        for old in (target / "manifest.hl", target / "hyprcursors"):
            if old.is_dir():
                shutil.rmtree(old)
            elif old.exists():
                old.unlink()
        shutil.copy2(produced / "manifest.hl", target / "manifest.hl")
        shutil.copytree(produced / "hyprcursors", target / "hyprcursors")
        for hlc in (target / "hyprcursors").glob("*.hlc"):
            normalize_hlc(hlc)

    print(f"added native hyprcursor data to {target}")


def main() -> int:
    if shutil.which("hyprcursor-util") is None:
        raise SystemExit("hyprcursor-util is required to build native cursors")

    parser = argparse.ArgumentParser()
    parser.add_argument("themes", nargs="*", choices=list(VARIANTS))
    args = parser.parse_args()
    themes = args.themes or list(VARIANTS)
    for theme in themes:
        build_theme(theme)
    return 0


if __name__ == "__main__":
    sys.exit(main())
