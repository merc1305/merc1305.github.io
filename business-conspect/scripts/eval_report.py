#!/usr/bin/env python3
"""Offline evaluation runner for recommendation-quality report dialogues."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVAL_SPEC = ROOT / "business-conspect/spec/eval_queries.json"


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
DOMAIN_RE = re.compile(r"^\s*-\s*Domain:\s*(.+?)\s*$", re.IGNORECASE)
EVIDENCE_RE = re.compile(r"\[evidence:\s*([^\]]+)\]", re.IGNORECASE)
INFERENCE_RE = re.compile(r"\[inference:\s*([^\]]+)\]", re.IGNORECASE)

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


STOPWORDS = {
    "a",
    "an",
    "and",
    "or",
    "the",
    "for",
    "with",
    "without",
    "to",
    "of",
    "in",
    "on",
    "is",
    "are",
    "was",
    "were",
    "my",
    "your",
    "this",
    "that",
    "when",
    "what",
    "how",
    "much",
    "does",
    "do",
    "should",
    "which",
    "best",
    "good",
    "vs",
    "versus",
    "a",
    "an",
    "i",
    "me",
}


class Heading:
    def __init__(self, line_index: int, level: int, text: str) -> None:
        self.line_index = line_index
        self.level = level
        self.text = text


def _parse_headings(lines: Sequence[str]) -> list[Heading]:
    headings: list[Heading] = []
    for idx, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        hashes, text = match.groups()
        headings.append(Heading(line_index=idx, level=len(hashes), text=text))
    return headings


def _section_slice(
    lines: Sequence[str], headings: Sequence[Heading], target: Heading
) -> slice:
    start = target.line_index + 1
    end = len(lines)
    for heading in headings:
        if heading.line_index <= target.line_index:
            continue
        if heading.level <= target.level:
            end = heading.line_index
            break
    return slice(start, end)


def _extract_section_text(
    lines: Sequence[str], headings: Sequence[Heading], heading_text: str
) -> str:
    for heading in headings:
        if heading.text == heading_text:
            sec = _section_slice(lines, headings, heading)
            return "\n".join(lines[sec]).strip()
    return ""


def _extract_domain(lines: Sequence[str]) -> str:
    for line in lines:
        match = DOMAIN_RE.match(line)
        if match:
            return match.group(1).strip().lower()
    return ""


def _extract_dialogue(lines: Sequence[str]) -> str:
    headings = _parse_headings(lines)
    return _extract_section_text(
        lines, headings, "5) Client ↔ Service Expert Dialogue (Deep Discovery)"
    )


def _client_lines(dialogue_text: str) -> list[str]:
    return [
        line.strip()[len("Client:") :].strip()
        for line in dialogue_text.splitlines()
        if line.strip().startswith("Client:")
    ]


def _covers(pattern: re.Pattern[str], queries: Iterable[str]) -> bool:
    return any(pattern.search(query) for query in queries)


def _keyword_coverage(dialogue_text: str, query: str) -> tuple[int, int, list[str]]:
    tokens = re.findall(r"[a-zA-Z0-9]+", query.lower())
    keywords = [t for t in tokens if len(t) >= 4 and t not in STOPWORDS]
    dialogue_lower = dialogue_text.lower()

    hits = [kw for kw in keywords if kw in dialogue_lower]
    required = min(3, len(keywords)) if keywords else 0
    return len(hits), required, keywords


def _evaluate_query(dialogue_text: str, query: dict[str, object]) -> tuple[bool, list[str]]:
    must_cover = [str(item) for item in query.get("mustCover", [])]
    client_queries = _client_lines(dialogue_text)

    coverage = {
        "value_outcome": _covers(OUTCOME_INTENT_RE, client_queries),
        "fit_constraints": _covers(CONSTRAINT_INTENT_RE, client_queries),
        "selection_logic_or_alternative": _covers(SELECTION_LOGIC_RE, client_queries),
        "pricing_cost": _covers(PRICING_INTENT_RE, client_queries),
        "non_fit_or_risk": any(
            NON_FIT_RE.search(q) or RISK_INTENT_RE.search(q) for q in client_queries
        ),
        "evidence_or_inference": bool(
            EVIDENCE_RE.search(dialogue_text) or INFERENCE_RE.search(dialogue_text)
        ),
    }

    missing = [key for key in must_cover if not coverage.get(key, False)]

    query_text = str(query.get("query", ""))
    keyword_hits, required_hits, keywords = _keyword_coverage(dialogue_text, query_text)
    if required_hits and keyword_hits < required_hits:
        missing.append(
            f"key_phrases({keyword_hits}/{required_hits})"
        )

    return len(missing) == 0, missing


def evaluate_report(report_path: Path, *, eval_spec_path: Path) -> int:
    if not report_path.is_file():
        print(f"Report not found: {report_path}", file=sys.stderr)
        return 2
    if not eval_spec_path.is_file():
        print(f"Eval spec not found: {eval_spec_path}", file=sys.stderr)
        return 2

    lines = report_path.read_text(encoding="utf-8").splitlines()
    domain = _extract_domain(lines)
    dialogue_text = _extract_dialogue(lines)

    if not domain:
        print("Could not determine report domain from metadata.", file=sys.stderr)
        return 2
    if not dialogue_text:
        print("Dialogue section not found or empty.", file=sys.stderr)
        return 2

    spec = json.loads(eval_spec_path.read_text(encoding="utf-8"))
    domain_entries = spec.get("domains", [])
    domain_entry = next(
        (entry for entry in domain_entries if entry.get("domain") == domain), None
    )
    if not domain_entry:
        print(f"No eval queries found for domain '{domain}'.", file=sys.stderr)
        return 2

    failures = 0
    queries = domain_entry.get("queries", [])
    print(f"Evaluation for {domain}: {len(queries)} queries")
    for query in queries:
        query_id = query.get("id", "unknown-id")
        passed, missing = _evaluate_query(dialogue_text, query)
        if passed:
            print(f"[PASS] {query_id}")
        else:
            failures += 1
            missing_str = ", ".join(missing)
            print(f"[FAIL] {query_id} missing: {missing_str}")

    if failures:
        print(f"Summary: {failures} failing queries.")
        return 1
    print("Summary: all queries passed.")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate a report dialogue against eval_queries.json."
    )
    parser.add_argument(
        "report_path",
        help="Path to report.md or report directory.",
    )
    parser.add_argument(
        "--eval-spec",
        default=str(DEFAULT_EVAL_SPEC),
        help="Path to eval_queries.json.",
    )
    return parser


def main(argv: list[str]) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    report_path = Path(args.report_path).resolve()
    if report_path.is_dir():
        report_path = report_path / "report.md"

    return evaluate_report(report_path, eval_spec_path=Path(args.eval_spec))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

