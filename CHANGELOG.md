# Changelog

## 1.3.0 — 2026-11-02

- Added a Linux setup guide for Hyprland, GNOME, Cinnamon, MATE, XFCE,
  KDE Plasma, generic X11, GTK and Flatpak.
- Added a Windows `.cur` package with a PowerShell installer.
- Added macOS Mousecape `.cape` packages for all variants.
- Added **X-Vector-Meta** and **X-Vector-Meta-Inverse**: rhombic horizontal
  and vertical axes, an eight-point centre, and the classic X diagonals. The
  Meta geometry snaps to whole pixels and uses no anti-aliasing.
- Added **X-Vector-Meta-Link** and **X-Vector-Meta-Link-Inverse**: the same
  geometry with the four axial separators bridged, so the arms meet the
  centre.
- `build.sh` now regenerates the Linux, Windows and macOS assets.

## 1.2.0 — 2026-11-02

- Added **X-Vector-Inverse**: a black 1 px core with a white 1 px outline for
  light desktops.
- `install.sh` now installs both variants and accepts `X-Vector` or
  `X-Vector-Inverse` as an argument.

## 1.1.0 — 2026-11-02

- Fixed the missing black outline on the south and east edges.
- Main axes are now 24 px at the 28 px cursor size, leaving a 2 px margin for
  the outline on every side.
- Preview tiles are now 36×36: the 28 px cursor plus 4 px breathing room.
- Renamed the theme and repository to **X-Vector**.
- Removed the old crosshair fallback theme.

## 1.0.0 — 2026-11-02

- Initial X-Vector eight-point star cursor.
