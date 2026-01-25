#!/usr/bin/env python3
"""Render report.md into index.html using a simple HTML template."""

from __future__ import annotations

import argparse
import html
import os
from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = ROOT / "business-conspect/scripts/templates/report.html"
ROOT_INDEX_PATH = ROOT / "business-conspect/index.html"
VALIDATOR_PATH = ROOT / "business-conspect/scripts/validate_report.py"


TITLE_PREFIX = "# Business Conspect — "
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
ORDERED_ITEM_RE = re.compile(r"^\s*\d+\.\s+(.*)$")
UNORDERED_ITEM_RE = re.compile(r"^\s*-\s+(.*)$")


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _escape(text: str) -> str:
    return html.escape(text, quote=True)


def _extract_title(lines: list[str]) -> str:
    for line in lines:
        if line.startswith(TITLE_PREFIX):
            return line.replace("# ", "").strip()
    return "Business Conspect Report"


def _close_paragraph(output: list[str], in_paragraph: bool) -> bool:
    if in_paragraph:
        output.append("</p>")
        return False
    return in_paragraph


def _markdown_to_html(lines: list[str]) -> str:
    output: list[str] = []
    in_paragraph = False
    in_ordered = False
    in_unordered = False
    in_nested_ul = False
    ordered_li_open = False

    def close_unordered() -> None:
        nonlocal in_unordered
        if in_unordered:
            output.append("</ul>")
            in_unordered = False

    def close_nested_ul() -> None:
        nonlocal in_nested_ul
        if in_nested_ul:
            output.append("</ul>")
            in_nested_ul = False

    def close_ordered_li() -> None:
        nonlocal ordered_li_open
        if ordered_li_open:
            close_nested_ul()
            output.append("</li>")
            ordered_li_open = False

    def close_ordered() -> None:
        nonlocal in_ordered
        if in_ordered:
            close_ordered_li()
            output.append("</ol>")
            in_ordered = False

    def close_lists() -> None:
        close_unordered()
        close_ordered()

    for raw_line in lines:
        line = raw_line.rstrip()

        heading_match = HEADING_RE.match(line)
        if heading_match:
            in_paragraph = _close_paragraph(output, in_paragraph)
            close_lists()
            level = len(heading_match.group(1))
            text = _escape(heading_match.group(2))
            output.append(f"<h{level}>{text}</h{level}>")
            continue

        ordered_match = ORDERED_ITEM_RE.match(line)
        if ordered_match:
            in_paragraph = _close_paragraph(output, in_paragraph)
            close_unordered()
            if in_ordered:
                close_ordered_li()
            else:
                output.append("<ol>")
                in_ordered = True
            ordered_li_open = True
            output.append(f"<li>{_escape(ordered_match.group(1))}")
            continue

        unordered_match = UNORDERED_ITEM_RE.match(line)
        if unordered_match:
            in_paragraph = _close_paragraph(output, in_paragraph)
            item_text = _escape(unordered_match.group(1))
            if in_ordered and ordered_li_open:
                if not in_nested_ul:
                    output.append("<ul>")
                    in_nested_ul = True
                output.append(f"<li>{item_text}</li>")
            else:
                if not in_unordered:
                    output.append("<ul>")
                    in_unordered = True
                output.append(f"<li>{item_text}</li>")
            continue

        if not line.strip():
            in_paragraph = _close_paragraph(output, in_paragraph)
            continue

        in_paragraph = _close_paragraph(output, in_paragraph)
        close_lists()
        output.append(f"<p>{_escape(line)}</p>")

    in_paragraph = _close_paragraph(output, in_paragraph)
    close_lists()

    return "\n".join(output)


def render_report(report_path: Path, *, out_path: Path) -> Path:
    if not report_path.is_file():
        raise FileNotFoundError(f"Report not found: {report_path}")
    if not TEMPLATE_PATH.is_file():
        raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")

    lines = report_path.read_text(encoding="utf-8").splitlines()
    title = _extract_title(lines)
    html_body = _markdown_to_html(lines)

    try:
        index_rel = os.path.relpath(ROOT_INDEX_PATH, report_path.parent)
    except ValueError:
        index_rel = "../../index.html"

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    rendered = (
        template.replace("{{TITLE}}", _escape(title))
        .replace("{{REPORT_MD_REL}}", "report.md")
        .replace("{{INDEX_REL}}", _escape(index_rel))
        .replace("{{GENERATED_AT}}", _now_iso_utc())
        .replace("{{CONTENT}}", html_body)
    )

    out_path.write_text(rendered, encoding="utf-8")
    return out_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render report.md into index.html."
    )
    parser.add_argument(
        "report_path",
        help="Path to report.md or report directory.",
    )
    parser.add_argument(
        "--out",
        default="",
        help="Optional custom output path (defaults to <report-dir>/index.html).",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip report validation before rendering.",
    )
    return parser


def main(argv: list[str]) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    report_path = Path(args.report_path).resolve()
    if report_path.is_dir():
        report_path = report_path / "report.md"

    out_path = Path(args.out).resolve() if args.out else report_path.parent / "index.html"

    if not args.skip_validation:
        if not VALIDATOR_PATH.is_file():
            print(f"Missing validator: {VALIDATOR_PATH}", file=sys.stderr)
            return 1
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), str(report_path)],
            check=False,
        )
        if result.returncode != 0:
            print("Validation failed; HTML rendering skipped.", file=sys.stderr)
            return result.returncode

    try:
        written = render_report(report_path, out_path=out_path)
    except Exception as exc:
        print(f"Failed to render report: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote HTML report: {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
