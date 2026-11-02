#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export CURSOR_OUTPUT="$ROOT/themes"

python3 "$ROOT/src/make_x_vector.py"

echo "Built theme in $ROOT/themes"
