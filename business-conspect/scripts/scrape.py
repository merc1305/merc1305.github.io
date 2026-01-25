#!/usr/bin/env python3
"""Offline-friendly website scraper for Business Conspect.

This script turns one or more URLs (or local HTML files) into a reusable
`raw/pages.json` artifact under a target report directory.

It intentionally uses only the Python standard library so it can run in
restricted environments (e.g., GitHub Pages workflows without extra deps).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import argparse
import hashlib
import json
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from typing import Iterable, List
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


SKIP_TAGS = {"script", "style", "noscript", "template"}
HEADING_TAGS = {"h1", "h2", "h3"}
TITLE_TAG = "title"

WHITESPACE_RE = re.compile(r"\s+")


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _normalize_space(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _is_probably_local(path_or_url: str) -> bool:
    parsed = urlparse(path_or_url)
    if parsed.scheme == "file":
        return True
    if parsed.scheme in {"http", "https"}:
        return False
    return Path(path_or_url).exists()


def _read_local(path_or_url: str) -> tuple[str, str]:
    parsed = urlparse(path_or_url)
    if parsed.scheme == "file":
        path = Path(parsed.path)
        source_url = path_or_url
    else:
        path = Path(path_or_url)
        source_url = str(path.resolve())

    html = path.read_text(encoding="utf-8")
    return source_url, html


def _fetch_remote(url: str, *, timeout: float, user_agent: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        charset = "utf-8"
        if "charset=" in content_type:
            charset = content_type.split("charset=", 1)[1].split(";", 1)[0].strip()
        raw = response.read()
        return raw.decode(charset, errors="replace")


@dataclass
class ExtractedPage:
    url: str
    fetched_at: str
    title: str
    description: str
    headings: list[str]
    content: str
    content_chars: int
    content_words: int
    content_sha256: str
    content_source: str


class _HTMLTextExtractor(HTMLParser):
    """A lightweight HTML extractor focused on text and key metadata."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self._in_title = False
        self._current_heading: str | None = None
        self._main_depth = 0

        self._title_chunks: list[str] = []
        self._text_chunks: list[str] = []
        self._main_text_chunks: list[str] = []
        self._headings: list[str] = []
        self._description: str = ""
        self._links: list[str] = []

    @property
    def title(self) -> str:
        return _normalize_space(unescape(" ".join(self._title_chunks)))

    @property
    def description(self) -> str:
        return _normalize_space(unescape(self._description))

    @property
    def headings(self) -> list[str]:
        return [h for h in (h.strip() for h in self._headings) if h]

    @property
    def content(self) -> str:
        if self._main_text_chunks:
            return _normalize_space(unescape(" ".join(self._main_text_chunks)))
        return _normalize_space(unescape(" ".join(self._text_chunks)))

    @property
    def content_source(self) -> str:
        return "main" if self._main_text_chunks else "full"

    @property
    def links(self) -> list[str]:
        return [link.strip() for link in self._links if link.strip()]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self._skip_depth += 1
            return

        if tag == TITLE_TAG:
            self._in_title = True
            return

        if tag == "main":
            self._main_depth += 1

        if tag in HEADING_TAGS:
            self._current_heading = tag
            return

        if tag == "a":
            for key, value in attrs:
                if key and key.lower() == "href" and value:
                    self._links.append(value)

        if tag == "meta" and not self._description:
            attrs_dict = {k.lower(): (v or "") for k, v in attrs}
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            if name == "description" or prop in {"og:description", "twitter:description"}:
                self._description = attrs_dict.get("content", "")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
            return

        if tag == TITLE_TAG:
            self._in_title = False
            return

        if tag == "main" and self._main_depth > 0:
            self._main_depth -= 1

        if tag in HEADING_TAGS:
            self._current_heading = None

    def handle_data(self, data: str) -> None:
        if not data or self._skip_depth > 0:
            return

        if self._in_title:
            self._title_chunks.append(data)
            return

        if self._current_heading:
            heading = _normalize_space(data)
            if heading:
                self._headings.append(heading)

        self._text_chunks.append(data)
        if self._main_depth > 0:
            self._main_text_chunks.append(data)


def _count_words(text: str) -> int:
    if not text:
        return 0
    return len(re.findall(r"\b\w+\b", text))


def _extract_page(
    *, source_url: str, html: str, fetched_at: str, max_chars: int
) -> ExtractedPage:
    parser = _HTMLTextExtractor()
    parser.feed(html)
    parser.close()

    content = parser.content
    if max_chars > 0 and len(content) > max_chars:
        content = content[:max_chars].rstrip() + " …[truncated]"

    return ExtractedPage(
        url=source_url,
        fetched_at=fetched_at,
        title=parser.title,
        description=parser.description,
        headings=parser.headings,
        content=content,
        content_chars=len(content),
        content_words=_count_words(content),
        content_sha256=_sha256(content),
        content_source=parser.content_source,
    )


def _unique_urls(urls: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for url in urls:
        key = url.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        ordered.append(key)
    return ordered


def _is_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"}


def _normalize_url(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme:
        return url
    normalized = parsed._replace(fragment="").geturl()
    return normalized.rstrip("/")


def _extract_links(html: str) -> list[str]:
    parser = _HTMLTextExtractor()
    parser.feed(html)
    parser.close()
    return parser.links


def scrape(
    urls: Iterable[str],
    *,
    out_dir: Path,
    max_chars: int,
    timeout: float,
    user_agent: str,
    crawl: bool,
    max_pages: int,
    same_domain_only: bool,
) -> tuple[Path, int, int]:
    """Scrape the provided URLs into raw/pages.json.

    Returns:
      (pages_json_path, page_count, error_count)
    """
    urls = _unique_urls(urls)
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    pages_json_path = raw_dir / "pages.json"

    pages: list[ExtractedPage] = []
    errors: list[dict[str, str]] = []

    queue = _unique_urls(urls)
    seen: set[str] = set()

    while queue:
        if crawl and max_pages > 0 and len(pages) >= max_pages:
            break

        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)

        fetched_at = _now_iso_utc()
        try:
            if _is_probably_local(url):
                source_url, html = _read_local(url)
            else:
                source_url = url
                html = _fetch_remote(url, timeout=timeout, user_agent=user_agent)

            page = _extract_page(
                source_url=source_url,
                html=html,
                fetched_at=fetched_at,
                max_chars=max_chars,
            )
            pages.append(page)
            print(f"[ok] scraped: {url}")

            if crawl and _is_http_url(source_url):
                links = _extract_links(html)
                for link in links:
                    if link.startswith(("mailto:", "tel:", "javascript:")):
                        continue
                    target = _normalize_url(urljoin(source_url, link))
                    if not _is_http_url(target):
                        continue
                    if same_domain_only:
                        source_host = urlparse(source_url).netloc.lower()
                        target_host = urlparse(target).netloc.lower()
                        if source_host and target_host and source_host != target_host:
                            continue
                    if target and target not in seen and target not in queue:
                        queue.append(target)
        except Exception as exc:  # pragma: no cover - defensive
            errors.append({"url": url, "error": f"{type(exc).__name__}: {exc}"})
            print(f"[error] failed to scrape {url}: {exc}", file=sys.stderr)

    payload = {
        "generated_at": _now_iso_utc(),
        "source_urls": urls,
        "pages": [page.__dict__ for page in pages],
        "errors": errors,
    }
    pages_json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return pages_json_path, len(pages), len(errors)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scrape URLs into business-conspect raw/pages.json."
    )
    parser.add_argument(
        "url",
        help="Primary URL or local HTML file path.",
    )
    parser.add_argument(
        "--also",
        dest="also_urls",
        action="append",
        default=[],
        help="Additional URL or local HTML file path. Can be provided multiple times.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Target report directory (raw/pages.json will be written under it).",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=20000,
        help="Maximum content length per page (0 disables truncation). Default: 20000.",
    )
    parser.add_argument(
        "--crawl",
        action="store_true",
        help="Crawl additional same-domain links starting from the provided URL.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=5,
        help="Maximum number of pages to scrape when --crawl is enabled. Default: 5.",
    )
    parser.add_argument(
        "--allow-external",
        action="store_true",
        help="Allow crawling links outside the starting domain when --crawl is enabled.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="HTTP timeout in seconds. Default: 20.",
    )
    parser.add_argument(
        "--user-agent",
        default=(
            "BusinessConspectBot/0.1 (+https://merc1305.github.io/business-conspect/)"
        ),
        help="User agent string for HTTP requests.",
    )
    return parser


def main(argv: list[str]) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    out_dir = Path(args.out)
    urls = [args.url, *args.also_urls]
    pages_json_path, page_count, error_count = scrape(
        urls,
        out_dir=out_dir,
        max_chars=args.max_chars,
        timeout=args.timeout,
        user_agent=args.user_agent,
        crawl=args.crawl,
        max_pages=args.max_pages,
        same_domain_only=not args.allow_external,
    )

    print(
        f"Wrote {page_count} page(s) to {pages_json_path} "
        f"(errors: {error_count})."
    )
    return 0 if page_count > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
