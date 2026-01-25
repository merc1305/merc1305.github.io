#!/usr/bin/env python3
"""Initialize a validator-friendly LLM answer template for a report directory."""

from __future__ import annotations

from datetime import datetime, timezone
import argparse
import json
from pathlib import Path
import sys
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = ROOT / "business-conspect/spec/LLM_ANSWER_TEMPLATE.md"
PAGES_JSON_REL = Path("raw/pages.json")
DEFAULT_OUT_REL = Path("raw/llm_answer.md")


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _normalize_host(host: str) -> str:
    host = (host or "").strip().lower()
    return host[4:] if host.startswith("www.") else host


def _domain_from_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return _normalize_host(parsed.netloc)
    return ""


def _first_http_url(payload: dict[str, Any]) -> str:
    candidates: list[str] = []
    candidates.extend(payload.get("source_urls", []) or [])
    for page in payload.get("pages", []) or []:
        url = str(page.get("url", "")).strip()
        if url:
            candidates.append(url)

    for url in candidates:
        parsed = urlparse(url)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return url
    return ""


def _load_pages_payload(report_dir: Path) -> dict[str, Any]:
    pages_path = report_dir / PAGES_JSON_REL
    if not pages_path.is_file():
        return {}
    try:
        return json.loads(pages_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _derive_domain_and_website(
    report_dir: Path, domain_override: str, website_override: str
) -> tuple[str, str]:
    payload = _load_pages_payload(report_dir)
    detected_website = _first_http_url(payload)
    detected_domain = _domain_from_url(detected_website) if detected_website else ""

    domain = (domain_override or detected_domain or report_dir.name).strip().lower()
    website = (website_override or detected_website).strip()
    if not website and domain:
        website = f"https://{domain}/"

    # Keep the domain consistent with the website when possible.
    website_domain = _domain_from_url(website)
    if website_domain:
        domain = website_domain

    return domain, website


def init_template(report_dir: Path, *, domain: str, website: str, out_path: Path) -> Path:
    if not TEMPLATE_PATH.is_file():
        raise FileNotFoundError(f"Missing template: {TEMPLATE_PATH}")

    resolved_domain, resolved_website = _derive_domain_and_website(
        report_dir, domain_override=domain, website_override=website
    )
    if not resolved_domain:
        raise ValueError("Could not determine domain. Provide --domain explicitly.")
    if not resolved_website:
        raise ValueError("Could not determine website URL. Provide --website explicitly.")

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    rendered = (
        template.replace("{{DOMAIN}}", resolved_domain)
        .replace("{{WEBSITE}}", resolved_website)
        .replace("{{GENERATED_AT}}", _now_iso_utc())
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    return out_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create raw/llm_answer.md from the LLM answer template."
    )
    parser.add_argument("report_dir", help="Path to a report directory.")
    parser.add_argument("--domain", default="", help="Override the detected domain.")
    parser.add_argument("--website", default="", help="Override the detected website URL.")
    parser.add_argument(
        "--out",
        default="",
        help="Optional custom output path. Defaults to <report_dir>/raw/llm_answer.md.",
    )
    return parser


def main(argv: list[str]) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    report_dir = Path(args.report_dir).resolve()
    out_path = Path(args.out).resolve() if args.out else report_dir / DEFAULT_OUT_REL

    try:
        written = init_template(
            report_dir,
            domain=args.domain,
            website=args.website,
            out_path=out_path,
        )
    except Exception as exc:
        print(f"Failed to initialize answer template: {exc}", file=sys.stderr)
        return 1

    try:
        rel = written.relative_to(ROOT)
    except ValueError:
        rel = written

    print(f"Wrote LLM answer template: {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

