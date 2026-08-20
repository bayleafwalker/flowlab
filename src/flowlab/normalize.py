from __future__ import annotations

from pathlib import Path
from typing import Any

from .util import first_present, isoformat_z, parse_timestamp, read_ndjson

CANONICAL_EVENTS = {
    "session.started", "session.ended", "edit.meaningful",
    "blocker.opened", "blocker.resolved",
    "verification.started", "verification.finished",
    "work.completed", "other",
}


def _text(value: Any) -> str | None:
    return None if value is None else str(value)


def _canonical_event(raw_event: str | None, tool_name: str | None, mapping: dict[str, Any]) -> str:
    for canonical, aliases in mapping.get("events", {}).items():
        if raw_event in {str(alias) for alias in aliases}:
            return canonical
    edit = mapping.get("meaningful_edit", {})
    if raw_event in {str(value) for value in edit.get("event_types", [])}:
        return "edit.meaningful"
    if tool_name in {str(value) for value in edit.get("tool_names", [])}:
        return "edit.meaningful"
    return "other"


def normalize(path: Path, mapping: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records, parse_errors = read_ndjson(path)
    fields = mapping.get("fields", {})
    normalized: list[dict[str, Any]] = []
    errors = list(parse_errors)

    for index, record in enumerate(records, start=1):
        try:
            timestamp = parse_timestamp(first_present(record, fields.get("timestamp", [])))
            raw_event = _text(first_present(record, fields.get("event_type", [])))
            tool_name = _text(first_present(record, fields.get("tool_name", [])))
            event = _canonical_event(raw_event, tool_name, mapping)
            if event not in CANONICAL_EVENTS:
                raise ValueError(f"mapping produced unknown canonical event {event!r}")

            blocker_class = _text(first_present(record, fields.get("blocker_class", [])))
            control = _text(first_present(record, fields.get("control", [])))
            if control not in {"endogenous", "exogenous", "unknown", None}:
                control = None
            if control is None and blocker_class is not None:
                control = mapping.get("control_by_blocker_class", {}).get(blocker_class, "unknown")

            normalized.append({
                "timestamp": isoformat_z(timestamp),
                "event": event,
                "session_id": _text(first_present(record, fields.get("session_id", []))),
                "work_id": _text(first_present(record, fields.get("work_id", []))),
                "blocker_id": _text(first_present(record, fields.get("blocker_id", []))),
                "blocker_class": blocker_class,
                "control": control,
                "oracle_kind": _text(first_present(record, fields.get("oracle_kind", []))),
                "oracle_strength": _text(first_present(record, fields.get("oracle_strength", []))),
                "oracle_result": _text(first_present(record, fields.get("oracle_result", []))),
                "raw_index": index,
                "source_event": raw_event,
                "source_tool": tool_name,
            })
        except (TypeError, ValueError) as exc:
            errors.append({"record": index, "error": str(exc)})

    normalized.sort(key=lambda item: (item["timestamp"], item["raw_index"]))
    return normalized, errors
