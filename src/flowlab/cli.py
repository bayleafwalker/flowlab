from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .discovery import discover
from .metrics import compute_metrics
from .normalize import normalize
from .report import render_markdown
from .util import read_ndjson, write_json


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def _write_ndjson(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def command_discover(args: argparse.Namespace) -> int:
    result = discover(args.input, include_samples=args.include_samples)
    if args.output:
        write_json(args.output, result)
    else:
        json.dump(result, sys.stdout, indent=2, sort_keys=True)
        print()
    return 0


def command_normalize(args: argparse.Namespace) -> int:
    mapping = _load_json(args.mapping)
    records, errors = normalize(args.input, mapping)
    _write_ndjson(args.output, records)
    if args.errors:
        write_json(args.errors, errors)
    if errors and args.fail_on_error:
        print(f"normalization produced {len(errors)} error(s)", file=sys.stderr)
        return 2
    return 0


def command_measure(args: argparse.Namespace) -> int:
    records, errors = read_ndjson(args.input)
    if errors:
        print(f"normalized input contains {len(errors)} invalid record(s)", file=sys.stderr)
        return 2
    gates = _load_json(args.gates) if args.gates else {}
    report = compute_metrics(records, gates)
    if args.output:
        write_json(args.output, report)
    else:
        json.dump(report, sys.stdout, indent=2, sort_keys=True)
        print()
    return 0


def command_report(args: argparse.Namespace) -> int:
    report = _load_json(args.input)
    text = render_markdown(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


def command_run(args: argparse.Namespace) -> int:
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.out_dir / "profile.json", discover(args.input))

    mapping = _load_json(args.mapping)
    normalized, errors = normalize(args.input, mapping)
    _write_ndjson(args.out_dir / "normalized.ndjson", normalized)
    write_json(args.out_dir / "normalization-errors.json", errors)
    if errors and args.fail_on_error:
        print(f"normalization produced {len(errors)} error(s)", file=sys.stderr)
        return 2

    gates = _load_json(args.gates) if args.gates else {}
    report = compute_metrics(normalized, gates)
    write_json(args.out_dir / "report.json", report)
    (args.out_dir / "report.md").write_text(render_markdown(report), encoding="utf-8")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="flowlab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p = subparsers.add_parser("discover", help="profile an NDJSON event stream")
    p.add_argument("input", type=Path)
    p.add_argument("--output", "-o", type=Path)
    p.add_argument("--include-samples", action="store_true", help="include raw field samples; keep output local and uncommitted")
    p.set_defaults(handler=command_discover)

    p = subparsers.add_parser("normalize", help="normalize events using a mapping")
    p.add_argument("input", type=Path)
    p.add_argument("--mapping", required=True, type=Path)
    p.add_argument("--output", "-o", required=True, type=Path)
    p.add_argument("--errors", type=Path)
    p.add_argument("--fail-on-error", action="store_true")
    p.set_defaults(handler=command_normalize)

    p = subparsers.add_parser("measure", help="compute metrics from normalized NDJSON")
    p.add_argument("input", type=Path)
    p.add_argument("--gates", type=Path)
    p.add_argument("--output", "-o", type=Path)
    p.set_defaults(handler=command_measure)

    p = subparsers.add_parser("report", help="render a JSON metric report as Markdown")
    p.add_argument("input", type=Path)
    p.add_argument("--output", "-o", type=Path)
    p.set_defaults(handler=command_report)

    p = subparsers.add_parser("run", help="discover, normalize, measure, and render")
    p.add_argument("input", type=Path)
    p.add_argument("--mapping", required=True, type=Path)
    p.add_argument("--gates", type=Path)
    p.add_argument("--out-dir", required=True, type=Path)
    p.add_argument("--fail-on-error", action="store_true")
    p.set_defaults(handler=command_run)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"flowlab: {exc}", file=sys.stderr)
        return 1
