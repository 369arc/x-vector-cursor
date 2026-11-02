#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${XDG_DATA_HOME:-$HOME/.local/share}/icons"

install -d "$DEST"
rm -rf "$DEST/X-Vector-Star"
cp -a "$ROOT/themes/X-Vector-Star" "$DEST/X-Vector-Star"
echo "Installed $DEST/X-Vector-Star"

if command -v hyprctl >/dev/null 2>&1 && hyprctl version >/dev/null 2>&1; then
  hyprctl setcursor X-Vector-Star 28 >/dev/null 2>&1 || true
  echo "Applied X-Vector-Star at 28 px for the current Hyprland session."
fi

cat <<'EOT'

For Hyprland, keep this in your environment:

  env = XCURSOR_THEME,X-Vector-Star
  env = XCURSOR_SIZE,28
  env = HYPRCURSOR_THEME,X-Vector-Star
  env = HYPRCURSOR_SIZE,28

For GTK:

  gsettings set org.gnome.desktop.interface cursor-theme 'X-Vector-Star'
  gsettings set org.gnome.desktop.interface cursor-size 28
EOT
