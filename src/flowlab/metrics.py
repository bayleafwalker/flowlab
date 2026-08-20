from __future__ import annotations

from collections import Counter, defaultdict, deque
from datetime import datetime
from typing import Any

from .util import distribution, parse_timestamp


def _seconds(start: datetime, end: datetime) -> float:
    return max(0.0, (end - start).total_seconds())


def compute_metrics(events: list[dict[str, Any]], gates: dict[str, Any] | None = None) -> dict[str, Any]:
    gates = gates or {}
    ordered = sorted(events, key=lambda event: (event["timestamp"], event.get("raw_index", 0)))

    sessions: dict[str, dict[str, Any]] = {}
    missing_session_id = 0

    def session_for(event: dict[str, Any]) -> dict[str, Any] | None:
        nonlocal missing_session_id
        session_id = event.get("session_id")
        if not session_id:
            missing_session_id += 1
            return None
        return sessions.setdefault(session_id, {
            "start": None,
            "end": None,
            "first": None,
            "last": None,
            "first_edit": None,
            "first_verification_pass": None,
            "work_ids": set(),
        })

    open_blockers: dict[str, deque[dict[str, Any]]] = defaultdict(deque)
    blockers: list[dict[str, Any]] = []
    blocker_events_missing_id = 0
    orphan_blocker_resolutions = 0
    oracle_counts: Counter[tuple[str, str, str]] = Counter()
    event_counts: Counter[str] = Counter()

    for event in ordered:
        event_counts[event["event"]] += 1
        timestamp = parse_timestamp(event["timestamp"])
        state = session_for(event)
        if state is not None:
            state["first"] = state["first"] or timestamp
            state["last"] = timestamp
            if event.get("work_id"):
                state["work_ids"].add(event["work_id"])
            if event["event"] == "session.started":
                state["start"] = state["start"] or timestamp
            elif event["event"] == "session.ended":
                state["end"] = timestamp
            elif event["event"] == "edit.meaningful":
                state["first_edit"] = state["first_edit"] or timestamp
            elif event["event"] == "verification.finished":
                result = (event.get("oracle_result") or "unknown").lower()
                if result in {"pass", "passed", "success", "succeeded", "ok"}:
                    state["first_verification_pass"] = state["first_verification_pass"] or timestamp

        if event["event"] == "blocker.opened":
            blocker_id = event.get("blocker_id")
            if not blocker_id:
                blocker_events_missing_id += 1
            else:
                open_blockers[blocker_id].append({"timestamp": timestamp, "event": event})
        elif event["event"] == "blocker.resolved":
            blocker_id = event.get("blocker_id")
            if not blocker_id:
                blocker_events_missing_id += 1
            elif open_blockers[blocker_id]:
                opened = open_blockers[blocker_id].popleft()
                source = opened["event"]
                blockers.append({
                    "blocker_id": blocker_id,
                    "duration_seconds": _seconds(opened["timestamp"], timestamp),
                    "blocker_class": source.get("blocker_class") or event.get("blocker_class") or "unknown",
                    "control": source.get("control") or event.get("control") or "unknown",
                    "session_id": source.get("session_id") or event.get("session_id"),
                    "work_id": source.get("work_id") or event.get("work_id"),
                })
            else:
                orphan_blocker_resolutions += 1

        if event["event"] == "verification.finished":
            oracle_counts[(
                event.get("oracle_kind") or "unknown",
                event.get("oracle_strength") or "unknown",
                (event.get("oracle_result") or "unknown").lower(),
            )] += 1

    orientation_fractions: list[float] = []
    orientation_seconds: list[float] = []
    time_to_verified_seconds: list[float] = []
    session_rows: list[dict[str, Any]] = []
    truncated_sessions = 0

    for session_id, state in sorted(sessions.items()):
        start = state["start"] or state["first"]
        end = state["end"] or state["last"]
        if state["end"] is None:
            truncated_sessions += 1
        duration = _seconds(start, end) if start and end else 0.0
        orientation = None
        fraction = None
        if start and state["first_edit"] and duration > 0:
            orientation = _seconds(start, state["first_edit"])
            fraction = orientation / duration
            orientation_seconds.append(orientation)
            orientation_fractions.append(fraction)
        verified = None
        if start and state["first_verification_pass"]:
            verified = _seconds(start, state["first_verification_pass"])
            time_to_verified_seconds.append(verified)
        session_rows.append({
            "session_id": session_id,
            "duration_seconds": duration,
            "orientation_seconds": orientation,
            "orientation_fraction": fraction,
            "time_to_first_verified_seconds": verified,
            "work_ids": sorted(state["work_ids"]),
            "truncated": state["end"] is None,
        })

    by_class_values: dict[str, list[float]] = defaultdict(list)
    by_control_values: dict[str, list[float]] = defaultdict(list)
    for blocker in blockers:
        by_class_values[blocker["blocker_class"]].append(blocker["duration_seconds"])
        by_control_values[blocker["control"]].append(blocker["duration_seconds"])

    by_class = {name: distribution(values) for name, values in sorted(by_class_values.items())}
    by_control = {name: distribution(values) for name, values in sorted(by_control_values.items())}
    classified_total = sum(sum(values) for name, values in by_control_values.items() if name in {"endogenous", "exogenous"})
    exogenous_total = sum(by_control_values.get("exogenous", []))
    endogenous_total = sum(by_control_values.get("endogenous", []))
    unknown_total = sum(by_control_values.get("unknown", []))
    exogenous_share = (exogenous_total / classified_total) if classified_total else None

    report: dict[str, Any] = {
        "summary": {
            "events": len(ordered),
            "sessions": len(sessions),
            "resolved_blockers": len(blockers),
            "verification_events": sum(oracle_counts.values()),
        },
        "orientation": {
            "fraction": distribution(orientation_fractions),
            "seconds": distribution(orientation_seconds),
            "measurable_sessions": len(orientation_fractions),
            "missing_sessions": len(sessions) - len(orientation_fractions),
        },
        "time_to_first_verified_seconds": distribution(time_to_verified_seconds),
        "blockers": {
            "by_class": by_class,
            "by_control": by_control,
            "records": blockers,
            "classified_seconds": {
                "endogenous": endogenous_total,
                "exogenous": exogenous_total,
                "unknown": unknown_total,
                "exogenous_share_of_classified": exogenous_share,
            },
        },
        "oracles": {
            "counts": [
                {"kind": key[0], "strength": key[1], "result": key[2], "count": count}
                for key, count in sorted(oracle_counts.items())
            ]
        },
        "data_quality": {
            "missing_session_id_events": missing_session_id,
            "blocker_events_missing_id": blocker_events_missing_id,
            "orphan_blocker_resolutions": orphan_blocker_resolutions,
            "unresolved_open_blockers": sum(len(queue) for queue in open_blockers.values()),
            "truncated_sessions": truncated_sessions,
            "event_counts": dict(sorted(event_counts.items())),
        },
        "sessions": session_rows,
    }
    report["decision_signals"] = evaluate_gates(report, gates)
    return report


def evaluate_gates(report: dict[str, Any], gates: dict[str, Any]) -> dict[str, Any]:
    warming = gates.get("warming", {})
    fraction = report["orientation"]["fraction"]
    measurable = report["orientation"]["measurable_sessions"]
    minimum = int(warming.get("minimum_sessions", 10))
    warming_outcome = "PILOT"
    rationale = "signal is between the pre-registered adopt and reject gates"
    if measurable < minimum:
        warming_outcome = "UNMEASURABLE"
        rationale = f"only {measurable} measurable sessions; gate requires {minimum}"
    elif (
        (fraction.get("median") or 0) >= float(warming.get("adopt_median_fraction", 0.15))
        or (fraction.get("p75") or 0) >= float(warming.get("adopt_p75_fraction", 0.25))
    ):
        warming_outcome = "ADOPT_CANDIDATE"
        rationale = "orientation distribution crosses the pre-registered adopt gate"
    elif (
        (fraction.get("median") or 0) < float(warming.get("reject_median_fraction", 0.10))
        and (fraction.get("p75") or 0) < float(warming.get("reject_p75_fraction", 0.15))
    ):
        warming_outcome = "REJECT_CANDIDATE"
        rationale = "orientation distribution remains below the pre-registered reject gate"

    duplication = gates.get("duplication", {})
    duplicate_candidates: list[dict[str, Any]] = []
    for blocker_class, stats in report["blockers"]["by_class"].items():
        median_value = stats.get("median")
        ratio = (stats.get("p90") / median_value) if median_value else None
        eligible_variance = (
            stats.get("count", 0) >= int(duplication.get("minimum_blockers", 8))
            and (stats.get("cv") or 0) >= float(duplication.get("minimum_cv", 0.75))
            and (ratio or 0) >= float(duplication.get("minimum_p90_median_ratio", 2.0))
        )
        duplicate_candidates.append({
            "blocker_class": blocker_class,
            "variance_gate": eligible_variance,
            "p90_median_ratio": ratio,
            "requires_oracle_and_reconciliation_check": True,
        })

    speculation = gates.get("speculation", {})
    share = report["blockers"]["classified_seconds"]["exogenous_share_of_classified"]
    if share is None:
        speculation_outcome = "UNMEASURABLE"
    elif share >= float(speculation.get("addressable_exogenous_share", 0.20)):
        speculation_outcome = "ADDRESSABLE_CANDIDATE"
    elif share < float(speculation.get("low_exogenous_share", 0.10)):
        speculation_outcome = "LOW_ADDRESSABLE_MARKET"
    else:
        speculation_outcome = "PILOT"

    return {
        "context_warming": {"outcome": warming_outcome, "rationale": rationale},
        "competitive_duplication": {"classes": duplicate_candidates},
        "exogenous_speculation": {"outcome": speculation_outcome, "exogenous_share": share},
    }
