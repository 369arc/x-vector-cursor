#!/usr/bin/env bash
set -euo pipefail

DEST="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
for theme in X-Vector X-Vector-Inverse; do
  rm -rf "$DEST/$theme"
  if [ -L "$HOME/.icons/$theme" ]; then
    rm -f "$HOME/.icons/$theme"
  fi
  echo "Removed $DEST/$theme"
done
