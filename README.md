# X-Vector Cursor

A minimal eight-point star cursor for your desktop environment.<br>
B/W tone contrast to stay readable on black and white pages.

## Variants

**X-Vector** — white core, black outline. Built for dark desktops; the outline
keeps it readable on light pages.

<p align="center">
  <img src="previews/x-vector-black.png" width="160" alt="X-Vector on black">
  <img src="previews/x-vector-white.png" width="160" alt="X-Vector on white">
  <img src="previews/x-vector-gray.png" width="160" alt="X-Vector on gray">
</p>

**X-Vector-Inverse** — black core, white outline. Built for light desktops;
the outline keeps it readable on dark pages.

<p align="center">
  <img src="previews/x-vector-inverse-black.png" width="160" alt="X-Vector-Inverse on black">
  <img src="previews/x-vector-inverse-white.png" width="160" alt="X-Vector-Inverse on white">
  <img src="previews/x-vector-inverse-gray.png" width="160" alt="X-Vector-Inverse on gray">
</p>

Preview tiles use a 36×36 canvas: the 28 px cursor plus 4 px breathing room on every side.

## Design

- **28 px** nominal size.
- Four main axes: **24 px** at the 28 px size (2 px margin on every side for the outline).
- Four diagonals: **14 px**.
- `X-Vector`: white **1 px** core; black **1 px** outline.
- `X-Vector-Inverse`: black **1 px** core; white **1 px** outline.
- No centre dot.
- Static XCursor; no motion trail and no per-click animation (XCursor cannot
  receive global mouse-button events).

Each variant is a two-tone cursor. On a matching background one layer
disappears, while the other keeps the star visible. `X-Vector` favors dark
desktops; `X-Vector-Inverse` favors light ones. On mid-gray both layers are
visible — the unavoidable compromise of a two-tone cursor.

The text cursor is a three-stripe vertical sandwich, 8 px shorter than the
nominal cursor. `X-Vector` uses black-white-black; the inverse uses
white-black-white. Both survive dark and light input fields.

## Release

Current version: **1.2.0** — added the inverse variant.
See [CHANGELOG.md](CHANGELOG.md) for details.

## Install

The generated XCursor themes are committed, so Python is only needed when
rebuilding.

```bash
git clone https://github.com/369arc/x-vector-cursor.git
cd x-vector-cursor
./install.sh
```

The script copies both themes to `${XDG_DATA_HOME:-$HOME/.local/share}/icons`
and applies `X-Vector` for the current Hyprland session when `hyprctl` is
available. To apply the inverse instead:

```bash
./install.sh X-Vector-Inverse
```

### Hyprland

```ini
env = XCURSOR_THEME,X-Vector
env = XCURSOR_SIZE,28
env = HYPRCURSOR_THEME,X-Vector
env = HYPRCURSOR_SIZE,28
```

Or apply immediately:

```bash
hyprctl setcursor X-Vector 28
```

Use `X-Vector-Inverse` in place of `X-Vector` for the light-desktop variant.

### GTK

```bash
gsettings set org.gnome.desktop.interface cursor-theme 'X-Vector'
gsettings set org.gnome.desktop.interface cursor-size 28
```

## Build

Requires Python 3 (no external Python packages).

```bash
./build.sh
```

This regenerates `themes/X-Vector` and `themes/X-Vector-Inverse` from the
script in `src/`.

## Uninstall

```bash
./uninstall.sh
```

Then switch to another theme with `hyprctl setcursor` / your environment.

## License

MIT. X-Vector is an original cursor design.
