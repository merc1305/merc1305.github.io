#!/usr/bin/env python3
"""Validate a canonical Business Conspect report.md.

This validator enforces the contract defined in:
  business-conspect/spec/REPORT_CONTRACT.md

It focuses on strict, testable checks that can run on GitHub Pages-friendly
artifacts without network access or third-party dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import re
import sys
from pathlib import Path
from typing import Iterable, List, Sequence
from urllib.parse import urlparse


TITLE_PREFIX = "# Business Conspect — "

REQUIRED_HEADINGS: Sequence[tuple[int, str]] = (
    (1, "Business Conspect — <domain.tld>"),
    (2, "1) Report Metadata"),
    (2, "2) Executive Summary"),
    (2, "3) Services and Offers (What This Site Provides)"),
    (2, "4) Ideal Customer Profile (ICP)"),
    (2, "5) Client ↔ Service Expert Dialogue (Deep Discovery)"),
)

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
ORDERED_ITEM_RE = re.compile(r"^\s*\d+\.\s+")
EVIDENCE_RE = re.compile(r"\[evidence:\s*([^\]]+)\]", re.IGNORECASE)
INFERENCE_RE = re.compile(r"\[inference:\s*([^\]]+)\]", re.IGNORECASE)
METADATA_FIELD_RE = re.compile(r"^\s*-\s*([^:]+):\s*(.+?)\s*$")
WHO_FOR_RE = re.compile(r"^\s*-\s*Who it is for:\s+", re.IGNORECASE)
EXPECTED_OUTCOME_RE = re.compile(r"^\s*-\s*Expected outcome:\s+", re.IGNORECASE)
SITUATION_TRIGGER_RE = re.compile(r"^\s*-\s*Situation trigger:\s+", re.IGNORECASE)
SELECTION_LOGIC_RE = re.compile(
    r"\b(choose|vs|versus|alternative|which service|when should i|best option)\b",
    re.IGNORECASE,
)
NON_FIT_RE = re.compile(
    r"\b(non[- ]?fit|not (a )?fit|not suitable|not for|should not|shouldn't|avoid)\b",
    re.IGNORECASE,
)
OUTCOME_INTENT_RE = re.compile(
    r"\b(need|want|goal|result|results|outcome|outcomes|achieve|improve|increase|reduce|solve|fix|help me|how do i|how can i|how to)\b",
    re.IGNORECASE,
)
PRICING_INTENT_RE = re.compile(
    r"\b(price|pricing|cost|costs|budget|rate|rates|fee|fees|how much|quote|estimate|expensive|cheap)\b",
    re.IGNORECASE,
)
CONSTRAINT_INTENT_RE = re.compile(
    r"\b(fit|suitable|budget|deadline|timeline|by when|geo|region|country|language|team size|team|stack|tech stack|framework|platform|industry|company size|small business|enterprise|jurisdiction|compliance|regulation|limited)\b",
    re.IGNORECASE,
)
RISK_INTENT_RE = re.compile(
    r"\b(risk|risks|mistake|mistakes|failure|fail|go wrong|limitation|limitations|pitfall|pitfalls|avoid)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Heading:
    line_index: int
    level: int
    text: str


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def _normalize_host(host: str) -> str:
    host = (host or "").strip().lower()
    if host.startswith("www."):
        return host[4:]
    return host


def _parse_headings(lines: Sequence[str]) -> list[Heading]:
    headings: list[Heading] = []
    for idx, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        hashes, text = match.groups()
        headings.append(Heading(line_index=idx, level=len(hashes), text=text))
    return headings


def _find_headings(
    headings: Iterable[Heading], *, level: int, text: str
) -> list[Heading]:
    return [h for h in headings if h.level == level and h.text == text]


def _section_slice(
    lines: Sequence[str], headings: Sequence[Heading], target: Heading
) -> slice:
    """Return a slice covering the target section content (excluding heading)."""
    start = target.line_index + 1
    end = len(lines)

    for heading in headings:
        if heading.line_index <= target.line_index:
            continue
        # A heading at the same or higher level closes the section.
        if heading.level <= target.level:
            end = heading.line_index
            break

    return slice(start, end)


def _extract_section_text(
    lines: Sequence[str], headings: Sequence[Heading], target: Heading
) -> str:
    sec = _section_slice(lines, headings, target)
    return "\n".join(lines[sec]).strip()


def _extract_metadata_fields(section_text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in section_text.splitlines():
        match = METADATA_FIELD_RE.match(line)
        if not match:
            continue
        key, value = match.groups()
        fields[key.strip()] = value.strip()
    return fields


def _validate_metadata(fields: dict[str, str], result: ValidationResult) -> None:
    required_keys = (
        "Website",
        "Domain",
        "Generated At (UTC)",
        "Report Version",
    )

    for key in required_keys:
        if key not in fields:
            result.error(f"Missing metadata field: '{key}'.")

    website = fields.get("Website", "")
    domain = fields.get("Domain", "")
    generated_at = fields.get("Generated At (UTC)", "")

    if website:
        parsed = urlparse(website)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            result.error("Website must be an absolute http(s) URL.")

        if domain and parsed.netloc:
            website_host = _normalize_host(parsed.netloc.split("@")[-1])
            domain_host = _normalize_host(domain)
            if website_host != domain_host:
                result.error(
                    "Domain must match the host portion of Website "
                    f"(got Website host '{website_host}' vs Domain '{domain_host}')."
                )

    if generated_at:
        if not generated_at.endswith("Z"):
            result.error("Generated At (UTC) must end with 'Z'.")
        else:
            # Replace Z with +00:00 for fromisoformat compatibility.
            try:
                datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
            except ValueError:
                result.error("Generated At (UTC) must be a valid ISO-8601 timestamp.")


def _validate_required_headings(
    lines: Sequence[str], headings: Sequence[Heading], result: ValidationResult
) -> dict[str, Heading]:
    """Validate required headings and return a mapping for downstream checks."""
    mapping: dict[str, Heading] = {}

    for level, heading_text in REQUIRED_HEADINGS:
        if level == 1:
            # Title is special: we accept any domain suffix but enforce the prefix.
            title_candidates = [h for h in headings if h.level == 1]
            if len(title_candidates) != 1:
                result.error("Report must contain exactly one level-1 title.")
                continue

            title = title_candidates[0]
            if not lines[title.line_index].startswith(TITLE_PREFIX):
                result.error(
                    "Level-1 title must start with '# Business Conspect — '."
                )
            mapping["__title__"] = title
            continue

        matches = _find_headings(headings, level=level, text=heading_text)
        if not matches:
            result.error(f"Missing required heading: '## {heading_text}'.")
            continue
        if len(matches) > 1:
            result.error(f"Heading appears more than once: '## {heading_text}'.")
            continue
        mapping[heading_text] = matches[0]

    return mapping


def _validate_services_section(
    section_text: str, result: ValidationResult
) -> None:
    if not section_text:
        result.error("Services section is empty.")
        return

    section_lines = section_text.splitlines()
    has_ordered_item = any(ORDERED_ITEM_RE.match(line) for line in section_lines)
    if not has_ordered_item:
        result.error("Services section must include at least one ordered list item (e.g., '1. Service').")

    blocks: list[list[str]] = []
    current_block: list[str] = []
    for line in section_lines:
        if ORDERED_ITEM_RE.match(line):
            if current_block:
                blocks.append(current_block)
            current_block = [line]
            continue
        if current_block:
            current_block.append(line)
    if current_block:
        blocks.append(current_block)

    if not blocks:
        return

    for idx, block_lines in enumerate(blocks, start=1):
        block_text = "\n".join(block_lines)

        has_evidence = bool(EVIDENCE_RE.search(block_text))
        if not has_evidence:
            result.error(
                f"Service #{idx} must contain at least one '[evidence: ...]' marker."
            )

        has_who_for = any(WHO_FOR_RE.match(line) for line in block_lines)
        if not has_who_for:
            result.error(f"Service #{idx} must include a '- Who it is for:' line.")

        has_expected_outcome = any(
            EXPECTED_OUTCOME_RE.match(line) for line in block_lines
        )
        if not has_expected_outcome:
            result.error(
                f"Service #{idx} must include a '- Expected outcome:' line."
            )


def _validate_icp_section(section_text: str, result: ValidationResult) -> None:
    if not section_text:
        result.error("Section is empty: '4) Ideal Customer Profile (ICP)'.")
        return

    has_situation_trigger = any(
        SITUATION_TRIGGER_RE.match(line) for line in section_text.splitlines()
    )
    if not has_situation_trigger:
        result.error("ICP section must include a '- Situation trigger:' line.")


def _validate_dialogue_section(
    section_text: str, result: ValidationResult
) -> None:
    if not section_text:
        result.error("Dialogue section is empty.")
        return

    section_lines = section_text.splitlines()
    has_client = any(line.strip().startswith("Client:") for line in section_lines)
    has_expert = any(line.strip().startswith("Expert:") for line in section_lines)

    if not has_client:
        result.error("Dialogue section must contain at least one 'Client:' line.")
    if not has_expert:
        result.error("Dialogue section must contain at least one 'Expert:' line.")

    client_queries = [
        line.strip()[len("Client:") :].strip()
        for line in section_lines
        if line.strip().startswith("Client:")
    ]

    def _covers(pattern: re.Pattern[str]) -> bool:
        return any(pattern.search(query) for query in client_queries)

    outcome_ok = _covers(OUTCOME_INTENT_RE)
    selection_ok = _covers(SELECTION_LOGIC_RE)
    pricing_ok = _covers(PRICING_INTENT_RE)
    constraint_ok = _covers(CONSTRAINT_INTENT_RE)
    non_fit_risk_ok = any(
        NON_FIT_RE.search(query) or RISK_INTENT_RE.search(query)
        for query in client_queries
    )

    if not outcome_ok:
        result.error(
            "Dialogue must cover search intent: Outcome / JTBD "
            "(e.g., need, want, results, outcome)."
        )
    if not selection_ok:
        result.error(
            "Dialogue must cover search intent: Selection / Comparison "
            "(e.g., choose, vs, alternative)."
        )
    if not pricing_ok:
        result.error(
            "Dialogue must cover search intent: Pricing / Cost "
            "(e.g., pricing, cost, budget, how much)."
        )
    if not constraint_ok:
        result.error(
            "Dialogue must cover search intent: Constraints / Fit "
            "(e.g., fit, team size, stack, geo, deadline)."
        )
    if not non_fit_risk_ok:
        result.error(
            "Dialogue must cover search intent: Non-Fit / Risk "
            "(e.g., not a fit, risks, mistakes, avoid)."
        )

    if not (EVIDENCE_RE.search(section_text) or INFERENCE_RE.search(section_text)):
        result.warn(
            "Dialogue section contains neither evidence nor inference markers; "
            "consider grounding key answers."
        )


def _warn_evidence_diversity(lines: Sequence[str], result: ValidationResult) -> None:
    sources = {
        match.group(1).strip().lower()
        for line in lines
        for match in EVIDENCE_RE.finditer(line)
    }
    if not sources:
        return
    if len(sources) < 2:
        result.warn(
            "Evidence sources are not diverse; consider citing multiple specific URLs."
        )


def _validate_non_empty(section_name: str, section_text: str, result: ValidationResult) -> None:
    if not section_text:
        result.error(f"Section is empty: '{section_name}'.")


def validate_report(report_path: Path) -> ValidationResult:
    result = ValidationResult()

    if report_path.is_dir():
        report_path = report_path / "report.md"

    if not report_path.is_file():
        result.error(f"Report not found: {report_path}")
        return result

    lines = report_path.read_text(encoding="utf-8").splitlines()
    headings = _parse_headings(lines)

    heading_map = _validate_required_headings(lines, headings, result)

    metadata_heading = heading_map.get("1) Report Metadata")
    summary_heading = heading_map.get("2) Executive Summary")
    services_heading = heading_map.get("3) Services and Offers (What This Site Provides)")
    icp_heading = heading_map.get("4) Ideal Customer Profile (ICP)")
    dialogue_heading = heading_map.get("5) Client ↔ Service Expert Dialogue (Deep Discovery)")

    if metadata_heading:
        metadata_text = _extract_section_text(lines, headings, metadata_heading)
        fields = _extract_metadata_fields(metadata_text)
        _validate_metadata(fields, result)

    if summary_heading:
        summary_text = _extract_section_text(lines, headings, summary_heading)
        _validate_non_empty("2) Executive Summary", summary_text, result)

    if services_heading:
        services_text = _extract_section_text(lines, headings, services_heading)
        _validate_services_section(services_text, result)

    if icp_heading:
        icp_text = _extract_section_text(lines, headings, icp_heading)
        _validate_icp_section(icp_text, result)

    if dialogue_heading:
        dialogue_text = _extract_section_text(lines, headings, dialogue_heading)
        _validate_dialogue_section(dialogue_text, result)

    _warn_evidence_diversity(lines, result)

    return result


def _print_result(report_path: Path, result: ValidationResult) -> None:
    status = "PASS" if result.ok else "FAIL"
    print(f"[{status}] {report_path}")

    if result.errors:
        print("\nErrors:")
        for err in result.errors:
            print(f"- {err}")

    if result.warnings:
        print("\nWarnings:")
        for warn in result.warnings:
            print(f"- {warn}")


def main(argv: Sequence[str]) -> int:
    if len(argv) < 2:
        print("Usage: python3 business-conspect/scripts/validate_report.py <path-to-report-or-dir>")
        return 2

    report_path = Path(argv[1])
    result = validate_report(report_path)
    _print_result(report_path, result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
