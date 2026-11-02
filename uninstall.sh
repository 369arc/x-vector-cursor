#!/usr/bin/env bash
set -euo pipefail

DEST="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
for theme in X-Vector-Star X-Vector-Crosshair; do
  rm -rf "$DEST/$theme"
  echo "Removed $DEST/$theme"
done
