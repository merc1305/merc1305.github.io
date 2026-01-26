#!/usr/bin/env python3
"""Render report.md into index.html using a simple HTML template."""

from __future__ import annotations

import argparse
import html
import json
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
WEBSITE_RE = re.compile(r"^\s*-\s*Website:\s*(.+?)\s*$", re.IGNORECASE)
DOMAIN_RE = re.compile(r"^\s*-\s*Domain:\s*(.+?)\s*$", re.IGNORECASE)
GENERATED_RE = re.compile(
    r"^\s*-\s*Generated At \(UTC\):\s*(.+?)\s*$", re.IGNORECASE
)
MARKER_RE = re.compile(r"\[(evidence|inference):\s*([^\]]+)\]", re.IGNORECASE)


class EvidenceRegistry:
    def __init__(self) -> None:
        self._sources: list[str] = []
        self._index: dict[str, int] = {}

    def register(self, source: str) -> int:
        source = source.strip()
        if source not in self._index:
            self._sources.append(source)
            self._index[source] = len(self._sources)
        return self._index[source]

    @property
    def sources(self) -> list[str]:
        return list(self._sources)


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


def _extract_metadata(lines: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    in_metadata = False
    for line in lines:
        if line.strip() == "## 1) Report Metadata":
            in_metadata = True
            continue
        if in_metadata and line.startswith("## "):
            break
        if in_metadata:
            if match := WEBSITE_RE.match(line):
                metadata["website"] = match.group(1).strip()
            if match := DOMAIN_RE.match(line):
                metadata["domain"] = match.group(1).strip()
            if match := GENERATED_RE.match(line):
                metadata["generated_at"] = match.group(1).strip()
    return metadata


def _extract_summary(lines: list[str]) -> str:
    in_summary = False
    summary_lines: list[str] = []
    for line in lines:
        if line.strip() == "## 2) Executive Summary":
            in_summary = True
            continue
        if in_summary and line.startswith("## "):
            break
        if in_summary and line.strip():
            summary_lines.append(line.strip())
    return _strip_markers(" ".join(summary_lines))


def _strip_markers(text: str) -> str:
    cleaned = MARKER_RE.sub("", text)
    return " ".join(cleaned.split())


def _build_json_ld(
    *, title: str, metadata: dict[str, str], summary: str
) -> str:
    payload: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "Report",
        "name": title,
        "url": "index.html",
        "mainEntityOfPage": "report.md",
    }

    generated = metadata.get("generated_at")
    if generated:
        payload["datePublished"] = generated

    domain = metadata.get("domain")
    if domain:
        payload["identifier"] = domain

    website = metadata.get("website")
    if website:
        payload["about"] = {"@type": "WebSite", "url": website, "name": domain or website}

    if summary:
        payload["abstract"] = summary

    json_ld = json.dumps(payload, ensure_ascii=True, indent=2)
    return f"<script type=\"application/ld+json\">{json_ld}</script>"


def _render_inline(text: str, registry: EvidenceRegistry) -> str:
    parts: list[str] = []
    cursor = 0
    for match in MARKER_RE.finditer(text):
        parts.append(_escape(text[cursor:match.start()]))
        kind = match.group(1).lower()
        content = match.group(2).strip()
        if kind == "evidence":
            index = registry.register(content)
            parts.append(
                f"<sup class=\"evidence-ref\" title=\"{_escape(content)}\">[{index}]</sup>"
            )
        else:
            parts.append(
                f"<span class=\"inference\">[inference: {_escape(content)}]</span>"
            )
        cursor = match.end()
    parts.append(_escape(text[cursor:]))
    return "".join(parts)


def _render_evidence_list(registry: EvidenceRegistry) -> str:
    if not registry.sources:
        return ""
    items = "\n".join(
        f"<li><a href=\"{_escape(source)}\">{_escape(source)}</a></li>"
        for source in registry.sources
    )
    return (
        "<section class=\"evidence-section\">"
        "<h2>Evidence Sources</h2>"
        f"<ol class=\"evidence-list\">{items}</ol>"
        "</section>"
    )


def _close_paragraph(output: list[str], in_paragraph: bool) -> bool:
    if in_paragraph:
        output.append("</p>")
        return False
    return in_paragraph


def _markdown_to_html(lines: list[str], registry: EvidenceRegistry) -> str:
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
            text = _render_inline(heading_match.group(2), registry)
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
            output.append(f"<li>{_render_inline(ordered_match.group(1), registry)}")
            continue

        unordered_match = UNORDERED_ITEM_RE.match(line)
        if unordered_match:
            in_paragraph = _close_paragraph(output, in_paragraph)
            item_text = _render_inline(unordered_match.group(1), registry)
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
        output.append(f"<p>{_render_inline(line, registry)}</p>")

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
    metadata = _extract_metadata(lines)
    summary = _extract_summary(lines)
    registry = EvidenceRegistry()
    html_body = _markdown_to_html(lines, registry)
    evidence_section = _render_evidence_list(registry)
    if evidence_section:
        html_body = f"{html_body}\n{evidence_section}"
    json_ld = _build_json_ld(title=title, metadata=metadata, summary=summary)

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
        .replace("{{JSON_LD}}", json_ld)
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
