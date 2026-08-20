#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

INPUT=evidence/campaign-2026-08-20/sanitized-auditctl.ndjson
OUT=${1:-reports/baseline}

python -m flowlab run "$INPUT" \
  --mapping config/auditctl-map.json \
  --gates config/gates.default.json \
  --out-dir "$OUT" \
  --fail-on-error
