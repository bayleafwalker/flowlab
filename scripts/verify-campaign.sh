#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

rm -rf .test-campaign
./scripts/run-campaign.sh .test-campaign
for name in profile.json normalized.ndjson normalization-errors.json report.json report.md; do
  diff -u "reports/baseline/$name" ".test-campaign/$name"
done

python - <<'PY'
import hashlib
import json
from pathlib import Path

root = Path.cwd()
provenance = json.loads((root / "evidence/campaign-2026-08-20/provenance.json").read_text())
source = root / provenance["input"]["path"]
actual = hashlib.sha256(source.read_bytes()).hexdigest()
assert actual == provenance["input"]["sha256"], (actual, provenance["input"]["sha256"])
assert sum(1 for line in source.read_text().splitlines() if line.strip()) == provenance["input"]["records"]
PY

rm -rf .test-campaign
