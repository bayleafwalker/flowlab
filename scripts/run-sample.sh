#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
rm -rf reports/sample
python -m flowlab run tests/fixtures/sample-auditctl.ndjson \
  --mapping config/auditctl-map.example.json \
  --gates config/gates.default.json \
  --out-dir reports/sample \
  --fail-on-error
printf 'Wrote %s\n' "$ROOT/reports/sample/report.md"
