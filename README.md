# X-Vector Star Cursor

A minimal eight-point star cursor for a pure-black desktop, with enough
two-tone contrast to stay readable on white pages.

<p align="center">
  <img src="previews/x-vector-star-black.png" width="160" alt="X-Vector Star on black">
  <img src="previews/x-vector-star-white.png" width="160" alt="X-Vector Star on white">
  <img src="previews/x-vector-star-gray.png" width="160" alt="X-Vector Star on gray">
</p>

## Design

- **28 px** nominal size.
- Four main axes: **26 px** (1 px margin for the outline).
- Four diagonals: **14 px**.
- White **1 px** core; black **1 px** outline.
- No centre dot.
- Static XCursor; no motion trail and no per-click animation (XCursor cannot
  receive global mouse-button events).

The black outline disappears on a black background, leaving a white star.
On white it makes the star visible as a black outline. On mid-gray both
layers are visible — the unavoidable compromise of a two-tone cursor.

`X-Vector-Crosshair` is included as a lighter fallback: four white axes with
a 14 px black X.

<p align="center">
  <img src="previews/x-vector-crosshair-black.png" width="160" alt="X-Vector Crosshair on black">
  <img src="previews/x-vector-crosshair-white.png" width="160" alt="X-Vector Crosshair on white">
  <img src="previews/x-vector-crosshair-gray.png" width="160" alt="X-Vector Crosshair on gray">
</p>

The text cursor is a black-white-black vertical sandwich, 8 px shorter than
the nominal cursor, so it survives both dark and light input fields.

## Install

The generated XCursor themes are committed, so Python is only needed when
rebuilding.

```bash
git clone https://github.com/369arc/x-vector-star-cursor.git
cd x-vector-star-cursor
./install.sh
```

The script copies both themes to `${XDG_DATA_HOME:-$HOME/.local/share}/icons`
and applies `X-Vector-Star` for the current Hyprland session when `hyprctl`
is available.

### Hyprland

```ini
env = XCURSOR_THEME,X-Vector-Star
env = XCURSOR_SIZE,28
env = HYPRCURSOR_THEME,X-Vector-Star
env = HYPRCURSOR_SIZE,28
```

Or apply immediately:

```bash
hyprctl setcursor X-Vector-Star 28
```

### GTK

```bash
gsettings set org.gnome.desktop.interface cursor-theme 'X-Vector-Star'
gsettings set org.gnome.desktop.interface cursor-size 28
```

## Build

Requires Python 3 (no external Python packages).

```bash
./build.sh
```

This regenerates `themes/X-Vector-Star` and `themes/X-Vector-Crosshair`
from the scripts in `src/`.

## Uninstall

```bash
./uninstall.sh
```

Then switch to another theme with `hyprctl setcursor` / your environment.

## License

MIT. X-Vector is an original cursor design.
