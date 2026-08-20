from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .util import flatten, read_ndjson, sha256_file


def _type_name(value: Any) -> str:
    return "null" if value is None else type(value).__name__


def discover(path: Path, max_samples: int = 12, include_samples: bool = False) -> dict[str, Any]:
    records, errors = read_ndjson(path)
    counts: Counter[str] = Counter()
    types: dict[str, Counter[str]] = defaultdict(Counter)
    samples: dict[str, list[Any]] = defaultdict(list)

    for record in records:
        for field, value in flatten(record).items():
            counts[field] += 1
            types[field][_type_name(value)] += 1
            if include_samples and len(samples[field]) < max_samples and value not in samples[field]:
                samples[field].append(value)

    fields: dict[str, Any] = {}
    for field in sorted(counts):
        fields[field] = {
            "count": counts[field],
            "coverage": (counts[field] / len(records)) if records else 0.0,
            "types": dict(types[field]),
            "samples": samples[field] if include_samples else [],
        }

    def candidates(words: tuple[str, ...]) -> list[str]:
        ranked = [name for name in fields if any(word in name.lower() for word in words)]
        return sorted(ranked, key=lambda name: (-fields[name]["coverage"], name))

    return {
        "profile_safety": {
            "includes_raw_value_samples": include_samples,
            "warning": (
                "Profiles with samples may contain sensitive values; keep them under evidence/raw and do not commit."
                if include_samples else None
            ),
        },
        "input": {
            "path_name": path.name,
            "sha256": sha256_file(path),
            "records": len(records),
            "invalid_records": len(errors),
        },
        "errors": errors[:100],
        "candidates": {
            "timestamp": candidates(("timestamp", "time", "created", "ts")),
            "event_type": candidates(("event", "type", "kind")),
            "session_id": candidates(("session",)),
            "work_id": candidates(("work", "task", "sprint")),
            "blocker": candidates(("block", "reason")),
            "oracle": candidates(("oracle", "verify", "test", "check")),
        },
        "fields": fields,
    }
