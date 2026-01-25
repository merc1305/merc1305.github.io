#!/usr/bin/env python3
"""Build a manual LLM prompt pack from raw/pages.json.

This script supports the no-API workflow (DEC-008):
1) scrape the site into raw/pages.json
2) build a high-quality prompt pack
3) run it manually in any LLM
4) paste the result back into the pipeline
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import argparse
import json
from pathlib import Path
import textwrap
import sys
from typing import Any, Iterable
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
REPORT_CONTRACT_PATH = ROOT / "business-conspect/spec/REPORT_CONTRACT.md"
SEARCH_INTENT_CONTRACT_PATH = ROOT / "business-conspect/spec/SEARCH_INTENT_CONTRACT.md"
PAGES_JSON_REL = Path("raw/pages.json")
PROMPT_PACK_REL = Path("raw/prompt_pack.md")


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _normalize_host(host: str) -> str:
    host = (host or "").strip().lower()
    return host[4:] if host.startswith("www.") else host


def _domain_from_url(url: str) -> str:
    parsed = urlparse(url)
    return _normalize_host(parsed.netloc) if parsed.scheme else ""


def _shorten(text: str, max_chars: int) -> str:
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + " ...[truncated]"


@dataclass(frozen=True)
class Page:
    url: str
    title: str
    description: str
    headings: list[str]
    content: str
    content_chars: int

    @staticmethod
    def from_json(data: dict[str, Any]) -> "Page":
        return Page(
            url=str(data.get("url", "")),
            title=str(data.get("title", "")),
            description=str(data.get("description", "")),
            headings=list(data.get("headings", []) or []),
            content=str(data.get("content", "")),
            content_chars=int(data.get("content_chars", 0) or 0),
        )


def _load_pages(report_dir: Path) -> tuple[dict[str, Any], list[Page]]:
    pages_path = report_dir / PAGES_JSON_REL
    if not pages_path.is_file():
        raise FileNotFoundError(f"Missing pages.json: {pages_path}")

    payload = json.loads(pages_path.read_text(encoding="utf-8"))
    pages = [Page.from_json(p) for p in payload.get("pages", [])]
    if not pages:
        raise ValueError("pages.json contains no pages. Run scrape.py first.")
    return payload, pages


def _contract_block(path: Path, *, label: str) -> str:
    if not path.is_file():
        return f"- {label}: MISSING at `{path}`"
    rel = path.relative_to(ROOT)
    return f"- {label}: `{rel}`"


def _render_contract_summary() -> str:
    # Keep this short and actionable. The canonical sources remain the spec docs.
    return textwrap.dedent(
        f"""
        ## Contract References (Read Before Generating)
        {_contract_block(REPORT_CONTRACT_PATH, label="Report contract")}
        {_contract_block(SEARCH_INTENT_CONTRACT_PATH, label="Search intent contract")}

        Minimum non-negotiables to follow:
        - Output MUST be a single canonical `report.md` in Markdown.
        - Use the exact required headings and metadata fields.
        - Ground non-trivial claims with `[evidence: <url>]`.
        - Any inferred claim MUST include `[inference: <reason>]` plus evidence.
        - Dialogue MUST cover: outcome, selection, pricing, constraints, non-fit/risk.
        - Every service MUST include `Who it is for` and `Expected outcome`.
        """
    ).strip()


def _render_generation_instructions(domain_hint: str) -> str:
    return textwrap.dedent(
        f"""
        ## Generation Goal (Recommendation and Traffic Oriented)
        Produce a report that helps LLMs:
        - understand the true value of the service
        - recommend it in the right situations
        - cite it with grounded, evidence-backed claims

        Focus on decision-stage usefulness. Do not write generic marketing copy.
        Where the site is silent, infer cautiously and label it clearly.

        Target domain hint: `{domain_hint or "<derive-from-sources>"}`.

        ## Output Requirements (Return Only Markdown)
        Return exactly one Markdown document that can be saved as `report.md`.
        Do not wrap it in JSON or extra commentary.

        Use this skeleton exactly (fill the placeholders with real content):

        ```md
        # Business Conspect — <domain.tld>

        ## 1) Report Metadata
        - Website: <https://domain.tld>
        - Domain: <domain.tld>
        - Generated At (UTC): <YYYY-MM-DDTHH:MM:SSZ>
        - Report Version: v1

        ## 2) Executive Summary
        <2-4 sentences. Include at least one evidence marker.>

        ## 3) Services and Offers (What This Site Provides)
        1. <Service / Offer Name>
        - What it is: <plain-language description> [evidence: <url>]
        - Who it is for: <segment / role / company type> [evidence: <url>]
        - Expected outcome: <result> [evidence: <url>]
        - Constraints: <geo, budget, prerequisites, timelines> [inference: <reason>] [evidence: <url>]
        - Evidence: <extra proof> [evidence: <url>]

        ## 4) Ideal Customer Profile (ICP)
        - Role or buyer type: <...> [evidence: <url>]
        - Company or context: <...> [evidence: <url>]
        - Situation trigger: <what makes them search now> [evidence: <url>]
        - Top goals: <3-5 goals> [evidence: <url>]
        - Top pains and risks: <3-5 risks> [evidence: <url>]
        - Decision criteria: <...> [evidence: <url>]
        - Common objections: <...> [evidence: <url>]

        ## 5) Client ↔ Service Expert Dialogue (Deep Discovery)
        Client: I need to achieve <outcome>. What should I choose here?
        Expert: <answer with selection logic> [evidence: <url>]

        Client: <Service A> vs <Service B> for <context> - when should I choose each?
        Expert: <answer> [evidence: <url>]

        Client: How much does this cost and what drives the price?
        Expert: <answer; infer carefully if needed> [inference: <reason>] [evidence: <url>]

        Client: Is this a fit for <team size/stack/geo/deadline>?
        Expert: <answer with constraints and prerequisites> [evidence: <url>]

        Client: When is this NOT a fit and what are the risks or common mistakes?
        Expert: <answer with non-fit boundaries> [evidence: <url>]
        ```
        """
    ).strip()


def _render_sources(pages: Iterable[Page], *, max_content_chars: int) -> str:
    blocks: list[str] = ["## Scraped Sources (Use These As Ground Truth)"]
    for idx, page in enumerate(pages, start=1):
        headings = ", ".join(page.headings[:12]) if page.headings else "(none found)"
        excerpt = _shorten(page.content, max_content_chars)
        blocks.append(
            textwrap.dedent(
                f"""
                ### Source {idx}
                - URL: {page.url}
                - Title: {page.title or "(no title found)"}
                - Description: {page.description or "(no meta description found)"}
                - Headings: {headings}
                - Content chars: {page.content_chars}

                Content excerpt:
                ```text
                {excerpt}
                ```
                """
            ).strip()
        )
    return "\n\n".join(blocks)


def build_prompt_pack(report_dir: Path, *, max_content_chars: int, out_path: Path) -> Path:
    payload, pages = _load_pages(report_dir)

    domain_hint = ""
    first_page_url = pages[0].url
    if first_page_url:
        domain_hint = _domain_from_url(first_page_url)

    generated_at = _now_iso_utc()
    sources_count = len(pages)
    source_urls = payload.get("source_urls", [])
    source_urls_block = "\n".join(f"- {url}" for url in source_urls) or "- (none)"

    header = textwrap.dedent(
        f"""
        # Business Conspect Prompt Pack — {domain_hint or "unknown-domain"}
        Generated at (UTC): {generated_at}
        Report directory: `{report_dir.relative_to(ROOT)}`
        Sources discovered: {sources_count}

        Source URLs:
        {source_urls_block}
        """
    ).strip()

    parts = [
        header,
        _render_contract_summary(),
        _render_generation_instructions(domain_hint),
        _render_sources(pages, max_content_chars=max_content_chars),
    ]
    content = "\n\n---\n\n".join(parts) + "\n"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    return out_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build raw/prompt_pack.md from raw/pages.json."
    )
    parser.add_argument(
        "report_dir",
        help="Path to the report directory containing raw/pages.json.",
    )
    parser.add_argument(
        "--max-content-chars",
        type=int,
        default=8000,
        help="Max characters per source content excerpt. Default: 8000.",
    )
    parser.add_argument(
        "--out",
        default="",
        help="Optional custom output path. Defaults to <report_dir>/raw/prompt_pack.md.",
    )
    return parser


def main(argv: list[str]) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    report_dir = Path(args.report_dir).resolve()
    out_path = Path(args.out).resolve() if args.out else report_dir / PROMPT_PACK_REL

    try:
        written = build_prompt_pack(
            report_dir,
            max_content_chars=args.max_content_chars,
            out_path=out_path,
        )
    except Exception as exc:
        print(f"Failed to build prompt pack: {exc}", file=sys.stderr)
        return 1

    try:
        rel = written.relative_to(ROOT)
    except ValueError:
        rel = written
    print(f"Wrote prompt pack: {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
