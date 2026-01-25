#!/usr/bin/env python3
"""Publish a Business Conspect report using the hardened pipeline.

Steps:
1) Validate report.md
2) Run the offline evaluation runner
3) Render index.html from report.md
4) Update the global index (index.html + index.json)
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "business-conspect/scripts/validate_report.py"
EVAL_RUNNER_PATH = ROOT / "business-conspect/scripts/eval_report.py"
RENDER_REPORT_PATH = ROOT / "business-conspect/scripts/render_report.py"
INDEX_UPDATER_PATH = ROOT / "business-conspect/scripts/update_index.py"


STEP_ORDER = ("validate", "evaluate", "render", "update-index")


def _run(cmd: list[str], *, label: str) -> int:
    print(f"[run] {label}: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    return result.returncode


def _summarize(results: dict[str, str]) -> None:
    print("\nSummary:")
    for step in STEP_ORDER:
        status = results.get(step, "SKIP")
        print(f"- {step}: {status}")


def publish(report_dir: Path) -> int:
    report_dir = report_dir.resolve()
    report_path = report_dir / "report.md"
    results: dict[str, str] = {}

    if not VALIDATOR_PATH.is_file():
        print(f"Missing validator: {VALIDATOR_PATH}", file=sys.stderr)
        return 1
    if not EVAL_RUNNER_PATH.is_file():
        print(f"Missing eval runner: {EVAL_RUNNER_PATH}", file=sys.stderr)
        return 1
    if not RENDER_REPORT_PATH.is_file():
        print(f"Missing renderer: {RENDER_REPORT_PATH}", file=sys.stderr)
        return 1
    if not INDEX_UPDATER_PATH.is_file():
        print(f"Missing index updater: {INDEX_UPDATER_PATH}", file=sys.stderr)
        return 1

    code = _run([sys.executable, str(VALIDATOR_PATH), str(report_path)], label="validate")
    if code != 0:
        results["validate"] = "FAIL"
        results["evaluate"] = "SKIP"
        results["render"] = "SKIP"
        results["update-index"] = "SKIP"
        print("Validation failed; aborting publish.", file=sys.stderr)
        _summarize(results)
        return code
    results["validate"] = "PASS"

    code = _run([sys.executable, str(EVAL_RUNNER_PATH), str(report_dir)], label="evaluate")
    if code != 0:
        results["evaluate"] = "FAIL"
        results["render"] = "SKIP"
        results["update-index"] = "SKIP"
        print("Evaluation failed; aborting publish.", file=sys.stderr)
        _summarize(results)
        return code
    results["evaluate"] = "PASS"

    code = _run([sys.executable, str(RENDER_REPORT_PATH), str(report_path)], label="render")
    if code != 0:
        results["render"] = "FAIL"
        results["update-index"] = "SKIP"
        print("Rendering failed; aborting publish.", file=sys.stderr)
        _summarize(results)
        return code
    results["render"] = "PASS"

    code = _run([sys.executable, str(INDEX_UPDATER_PATH)], label="update index")
    if code != 0:
        results["update-index"] = "FAIL"
        print("Index update failed.", file=sys.stderr)
        _summarize(results)
        return code
    results["update-index"] = "PASS"

    print("[ok] Publish completed.")
    _summarize(results)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Publish a report: validate, ensure index.html, update index."
    )
    parser.add_argument(
        "report_dir",
        help="Path to a report directory containing report.md.",
    )
    return parser


def main(argv: list[str]) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return publish(Path(args.report_dir))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
