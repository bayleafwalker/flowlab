#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from flowlab.discovery import discover  # noqa: E402
from flowlab.util import write_json  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    profile = discover(args.input)
    write_json(args.output, {
        "input": profile["input"],
        "note": "Contains hashes and counts only; raw input is not copied.",
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
