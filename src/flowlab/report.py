from __future__ import annotations

from typing import Any


def _fmt_number(value: Any, digits: int = 2) -> str:
    return "n/a" if value is None else f"{float(value):.{digits}f}"


def _fmt_percent(value: Any) -> str:
    return "n/a" if value is None else f"{float(value) * 100:.1f}%"


def _fmt_duration(value: Any) -> str:
    if value is None:
        return "n/a"
    seconds = float(value)
    if seconds < 120:
        return f"{seconds:.1f} s"
    if seconds < 7200:
        return f"{seconds / 60:.1f} min"
    return f"{seconds / 3600:.2f} h"


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    fraction = report["orientation"]["fraction"]
    seconds = report["orientation"]["seconds"]
    signals = report["decision_signals"]
    blocked = report["blockers"]["classified_seconds"]

    lines = [
        "# FlowLab report", "", "## Coverage", "",
        f"- Events: **{summary['events']}**",
        f"- Sessions: **{summary['sessions']}**",
        f"- Resolved blockers: **{summary['resolved_blockers']}**",
        f"- Verification events: **{summary['verification_events']}**",
        "", "## Orientation", "",
        f"- Measurable sessions: **{report['orientation']['measurable_sessions']}**",
        f"- Median fraction: **{_fmt_percent(fraction.get('median'))}**",
        f"- p75 fraction: **{_fmt_percent(fraction.get('p75'))}**",
        f"- p90 fraction: **{_fmt_percent(fraction.get('p90'))}**",
        f"- Median absolute time: **{_fmt_duration(seconds.get('median'))}**",
        f"- Gate signal: **{signals['context_warming']['outcome']}** — {signals['context_warming']['rationale']}",
        "", "## Blockers by class", "",
        "| Class | n | Median | p90 | CV | p90/median | Variance gate |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]

    candidate_map = {item["blocker_class"]: item for item in signals["competitive_duplication"]["classes"]}
    for blocker_class, stats in report["blockers"]["by_class"].items():
        candidate = candidate_map.get(blocker_class, {})
        lines.append(
            "| {name} | {count} | {median} | {p90} | {cv} | {ratio} | {gate} |".format(
                name=blocker_class,
                count=stats.get("count", 0),
                median=_fmt_duration(stats.get("median")),
                p90=_fmt_duration(stats.get("p90")),
                cv=_fmt_number(stats.get("cv")),
                ratio=_fmt_number(candidate.get("p90_median_ratio")),
                gate="yes; oracle still required" if candidate.get("variance_gate") else "no",
            )
        )

    lines.extend([
        "", "## Control split", "",
        f"- Endogenous blocked time: **{_fmt_duration(blocked.get('endogenous'))}**",
        f"- Exogenous blocked time: **{_fmt_duration(blocked.get('exogenous'))}**",
        f"- Unknown blocked time: **{_fmt_duration(blocked.get('unknown'))}**",
        f"- Exogenous share of classified time: **{_fmt_percent(blocked.get('exogenous_share_of_classified'))}**",
        f"- Gate signal: **{signals['exogenous_speculation']['outcome']}**",
        "", "## Oracle observations", "",
        "| Kind | Strength | Result | Count |",
        "|---|---|---|---:|",
    ])
    for item in report["oracles"]["counts"]:
        lines.append(f"| {item['kind']} | {item['strength']} | {item['result']} | {item['count']} |")
    if not report["oracles"]["counts"]:
        lines.append("| unknown | unknown | unknown | 0 |")

    quality = report["data_quality"]
    lines.extend([
        "", "## Data quality", "",
        f"- Events missing session ID: **{quality['missing_session_id_events']}**",
        f"- Blocker events missing blocker ID: **{quality['blocker_events_missing_id']}**",
        f"- Orphan blocker resolutions: **{quality['orphan_blocker_resolutions']}**",
        f"- Unresolved open blockers: **{quality['unresolved_open_blockers']}**",
        f"- Truncated sessions: **{quality['truncated_sessions']}**",
        "", "## Interpretation boundary", "",
        "Gate signals are not final decisions. Competitive duplication still requires a suitable oracle and bounded discard/reconciliation cost. Missing blocker events are reported as missing data rather than inferred from silence.",
        "",
    ])
    return "\n".join(lines)
