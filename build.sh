#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export CURSOR_OUTPUT="$ROOT/themes"

python3 "$ROOT/src/make_x_vector_star.py"
python3 "$ROOT/src/make_x_vector_crosshair.py"

echo "Built themes in $ROOT/themes"
