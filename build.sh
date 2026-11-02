#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export CURSOR_OUTPUT="$ROOT/themes"

for theme in X-Vector X-Vector-Inverse; do
  python3 "$ROOT/src/make_x_vector.py" "$theme"
done
python3 "$ROOT/src/make_platform_assets.py"

echo "Built themes in $ROOT/themes and platform assets in $ROOT/platforms"
