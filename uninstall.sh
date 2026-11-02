#!/usr/bin/env bash
set -euo pipefail

DEST="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
rm -rf "$DEST/X-Vector-Star"
echo "Removed $DEST/X-Vector-Star"
