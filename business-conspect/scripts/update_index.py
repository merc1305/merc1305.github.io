#!/usr/bin/env python3
"""Regenerate the Business Conspect report index.

This script scans the /business-conspect/reports/ directory for reports laid out as:

  /business-conspect/reports/YYYY-MM-DD/domain.tld/index.html

It then:
1) Replaces the HTML block between REPORTS_LIST markers in business-conspect/index.html
2) Writes a machine-readable index to business-conspect/index.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, List


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MARKER_START = "<!-- REPORTS_LIST_START -->"
MARKER_END = "<!-- REPORTS_LIST_END -->"


@dataclass(frozen=True)
class ReportEntry:
    report_date: date
    date_str: str
    domain: str
    index_rel_path: str
    report_md_rel_path: str | None


def _parse_date(value: str) -> date | None:
    if not DATE_RE.match(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def discover_reports(
    reports_root: Path,
    root: Path,
    *,
    include_missing_report_md: bool,
) -> List[ReportEntry]:
    """Discover reports under the business-conspect/reports directory."""
    entries: List[ReportEntry] = []

    if not reports_root.is_dir():
        return entries

    for date_dir in sorted(reports_root.iterdir()):
        if not date_dir.is_dir():
            continue

        parsed_date = _parse_date(date_dir.name)
        if parsed_date is None:
            continue

        for domain_dir in sorted(date_dir.iterdir()):
            if not domain_dir.is_dir():
                continue

            index_file = domain_dir / "index.html"
            if not index_file.is_file():
                continue

            report_md = domain_dir / "report.md"
            report_md_exists = report_md.is_file()
            report_md_rel_path = (
                str(report_md.relative_to(root)) if report_md_exists else None
            )

            if not report_md_exists and not include_missing_report_md:
                continue

            entry = ReportEntry(
                report_date=parsed_date,
                date_str=date_dir.name,
                domain=domain_dir.name,
                index_rel_path=str(index_file.relative_to(root)),
                report_md_rel_path=report_md_rel_path,
            )
            entries.append(entry)

    # Newest first, then domain for stable ordering.
    entries.sort(key=lambda e: (e.report_date, e.domain), reverse=True)
    return entries


def _render_empty_state() -> str:
    return f"""{MARKER_START}
        <div class="glass-card" style="text-align: left;">
          <h3 style="margin-bottom: 0.75rem;">Generated Reports</h3>
          <p style="margin: 0;">
            No reports yet. Add one under <code>business-conspect/reports/YYYY-MM-DD/domain.tld/</code>
            and run <code>python3 business-conspect/scripts/update_index.py</code>.
          </p>
        </div>
        {MARKER_END}"""


def _render_reports_list(entries: Iterable[ReportEntry]) -> str:
    entries = list(entries)
    if not entries:
        return _render_empty_state()

    item_lines: list[str] = []
    for entry in entries:
        report_md_link = ""
        if entry.report_md_rel_path:
            report_md_link = (
                f' · <a href="{entry.report_md_rel_path}">report.md</a>'
            )

        item_lines.append(
            (
                "            <li style=\"margin: 0.35rem 0;\">"
                f"<a href=\"{entry.index_rel_path}\"><strong>{entry.domain}</strong></a> "
                f"<span style=\"color: var(--text-secondary);\">({entry.date_str})</span>"
                f"{report_md_link}"
                "</li>"
            )
        )

    items_html = "\n".join(item_lines)

    return f"""{MARKER_START}
        <div class="glass-card" style="text-align: left; margin-bottom: 2rem;">
          <h3 style="margin-bottom: 0.5rem;">Generated Reports</h3>
          <p style="margin: 0 0 1rem 0; color: var(--text-secondary);">
            Total reports: {len(entries)}
          </p>
          <ul style="margin: 0; padding-left: 1.25rem; line-height: 1.5;">
{items_html}
          </ul>
        </div>
        {MARKER_END}"""


def update_index_html(root: Path, entries: List[ReportEntry]) -> None:
    index_path = root / "index.html"
    original = index_path.read_text(encoding="utf-8")

    start_idx = original.find(MARKER_START)
    end_idx = original.find(MARKER_END)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        raise RuntimeError(
            "Could not find REPORTS_LIST markers in business-conspect/index.html"
        )

    end_idx += len(MARKER_END)
    replacement = _render_reports_list(entries)
    updated = original[:start_idx] + replacement + original[end_idx:]

    index_path.write_text(updated, encoding="utf-8")


def write_index_json(root: Path, entries: Iterable[ReportEntry]) -> None:
    index_json_path = root / "index.json"
    payload = [
        {
            "date": entry.date_str,
            "domain": entry.domain,
            "indexPath": entry.index_rel_path,
            "reportMdPath": entry.report_md_rel_path,
        }
        for entry in entries
    ]
    index_json_path.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Regenerate the Business Conspect report index."
    )
    parser.add_argument(
        "--skip-missing-report-md",
        action="store_true",
        help="Skip report entries that do not have report.md.",
    )
    parser.add_argument(
        "--no-warn-missing-report-md",
        action="store_true",
        help="Do not warn about entries missing report.md.",
    )
    return parser


def main(argv: list[str]) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    script_path = Path(__file__).resolve()
    root = script_path.parents[1]
    reports_root = root / "reports"

    entries = discover_reports(
        reports_root,
        root,
        include_missing_report_md=not args.skip_missing_report_md,
    )
    if not args.no_warn_missing_report_md:
        for entry in entries:
            if entry.report_md_rel_path is None:
                print(
                    f"[warn] Missing report.md for {entry.domain} ({entry.date_str}).",
                    file=sys.stderr,
                )
    update_index_html(root, entries)
    write_index_json(root, entries)

    print(f"Discovered reports: {len(entries)}")
    print(f"Updated: {root / 'index.html'}")
    print(f"Updated: {root / 'index.json'}")


if __name__ == "__main__":
    main(sys.argv[1:])
