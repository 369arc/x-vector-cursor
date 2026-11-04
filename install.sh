#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
THEME="${1:-X-Vector}"

case "$THEME" in
  X-Vector|X-Vector-Inverse|X-Vector-Meta|X-Vector-Meta-Inverse|X-Vector-Link|X-Vector-Link-Inverse) ;;
  *)
    echo "Unknown theme: $THEME" >&2
    echo "Use X-Vector, X-Vector-Inverse, X-Vector-Meta, X-Vector-Meta-Inverse, X-Vector-Link or X-Vector-Link-Inverse." >&2
    exit 1
    ;;
esac

install -d "$DEST"
for variant in X-Vector X-Vector-Inverse X-Vector-Meta X-Vector-Meta-Inverse X-Vector-Link X-Vector-Link-Inverse; do
  rm -rf "$DEST/$variant"
  cp -a "$ROOT/themes/$variant" "$DEST/$variant"
  echo "Installed $DEST/$variant"
done

if command -v hyprctl >/dev/null 2>&1 && hyprctl version >/dev/null 2>&1; then
  hyprctl setcursor "$THEME" 28 >/dev/null 2>&1 || true
  echo "Applied $THEME at 28 px for the current Hyprland session."
fi

cat <<EOT

For Hyprland, keep this in your environment:

  env = XCURSOR_THEME,$THEME
  env = XCURSOR_SIZE,28
  env = HYPRCURSOR_THEME,$THEME
  env = HYPRCURSOR_SIZE,28

For GTK:

  gsettings set org.gnome.desktop.interface cursor-theme '$THEME'
  gsettings set org.gnome.desktop.interface cursor-size 28
EOT
