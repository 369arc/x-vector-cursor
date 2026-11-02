#!/usr/bin/env bash
set -euo pipefail

DEST="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
for theme in X-Vector X-Vector-Inverse; do
  rm -rf "$DEST/$theme"
  echo "Removed $DEST/$theme"
done
