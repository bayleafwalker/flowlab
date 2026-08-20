from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
from statistics import fmean, median, pstdev
from typing import Any, Iterable


def parse_timestamp(value: Any) -> datetime:
    if isinstance(value, (int, float)):
        seconds = float(value) / 1000.0 if float(value) > 10_000_000_000 else float(value)
        return datetime.fromtimestamp(seconds, tz=timezone.utc)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"unsupported timestamp: {value!r}")
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def isoformat_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def get_path(record: dict[str, Any], path: str) -> Any:
    current: Any = record
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def first_present(record: dict[str, Any], paths: Iterable[str]) -> Any:
    for path in paths:
        value = get_path(record, path)
        if value is not None:
            return value
    return None


def flatten(record: Any, prefix: str = "") -> dict[str, Any]:
    result: dict[str, Any] = {}
    if isinstance(record, dict):
        for key, value in record.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            result.update(flatten(value, path))
    elif isinstance(record, list):
        result[prefix] = f"<list:{len(record)}>"
    else:
        result[prefix] = record
    return result


def percentile(values: list[float], quantile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def distribution(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {
            "count": 0, "min": None, "median": None, "p75": None,
            "p90": None, "max": None, "mean": None, "stddev": None, "cv": None,
        }
    mean = fmean(values)
    stddev = pstdev(values) if len(values) > 1 else 0.0
    return {
        "count": len(values),
        "min": min(values),
        "median": median(values),
        "p75": percentile(values, 0.75),
        "p90": percentile(values, 0.90),
        "max": max(values),
        "mean": mean,
        "stddev": stddev,
        "cv": (stddev / mean) if mean else None,
    }


def read_ndjson(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                value = json.loads(text)
                if not isinstance(value, dict):
                    raise ValueError("NDJSON record is not an object")
                records.append(value)
            except (json.JSONDecodeError, ValueError) as exc:
                errors.append({"line": line_number, "error": str(exc)})
    return records, errors


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
