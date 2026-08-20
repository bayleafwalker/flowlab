#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python -m unittest discover -s tests -p 'test_*.py' -v
rm -rf .test-output
python -m flowlab run tests/fixtures/sample-auditctl.ndjson \
  --mapping config/auditctl-map.example.json \
  --gates config/gates.default.json \
  --out-dir .test-output \
  --fail-on-error
python -m flowlab report .test-output/report.json --output .test-output/report-rerendered.md
cmp .test-output/report.md .test-output/report-rerendered.md
printf '\nFlowLab verification passed.\n'
