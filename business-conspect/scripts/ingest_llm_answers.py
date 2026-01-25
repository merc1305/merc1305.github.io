#!/usr/bin/env python3
"""Ingest manual LLM answers into canonical report.md.

Supports Markdown or JSON inputs and normalizes them into a validator-friendly
report.md before running validation.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "business-conspect/scripts/validate_report.py"
TITLE_PREFIX = "# Business Conspect — "


CODE_FENCE_RE = re.compile(r"^```")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_validator_module() -> Any:
    if not VALIDATOR_PATH.is_file():
        raise FileNotFoundError(f"Missing validator: {VALIDATOR_PATH}")
    spec = importlib.util.spec_from_file_location("validate_report", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise ImportError("Could not load validate_report module.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[call-arg]
    return module


def _unwrap_code_fences(lines: list[str]) -> list[str]:
    non_empty = [idx for idx, line in enumerate(lines) if line.strip()]
    if not non_empty:
        return lines
    first = non_empty[0]
    last = non_empty[-1]
    if CODE_FENCE_RE.match(lines[first].strip()) and CODE_FENCE_RE.match(
        lines[last].strip()
    ):
        return lines[first + 1 : last]
    return lines


def _trim_to_title(lines: list[str]) -> list[str]:
    for idx, line in enumerate(lines):
        if line.strip().startswith(TITLE_PREFIX):
            return lines[idx:]
    return lines


def _normalize_markdown(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").splitlines()

    if lines and lines[0].startswith("\ufeff"):
        lines[0] = lines[0].lstrip("\ufeff")

    lines = _unwrap_code_fences(lines)
    lines = _trim_to_title(lines)

    normalized = [line.rstrip() for line in lines]

    while normalized and not normalized[0].strip():
        normalized.pop(0)
    while normalized and not normalized[-1].strip():
        normalized.pop()

    content = "\n".join(normalized)
    if content and not content.endswith("\n"):
        content += "\n"
    return content


def _get_path(payload: Any, path: Iterable[Any]) -> Any:
    current = payload
    for key in path:
        if isinstance(key, int):
            if not isinstance(current, list) or key >= len(current):
                return None
            current = current[key]
        else:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]
    return current


def _extract_markdown_from_json(payload: Any) -> str:
    candidate_paths: list[tuple[Any, ...]] = [
        ("report_md",),
        ("markdown",),
        ("content",),
        ("report", "markdown"),
        ("report", "content"),
        ("report", "report_md"),
        ("data", "markdown"),
        ("data", "content"),
        ("message", "content"),
        ("choices", 0, "message", "content"),
        ("choices", 0, "text"),
        ("output",),
        ("text",),
    ]

    for path in candidate_paths:
        value = _get_path(payload, path)
        if isinstance(value, str) and value.strip():
            return value

    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, str) and item.strip():
                return item
            if isinstance(item, dict):
                for path in candidate_paths:
                    value = _get_path(item, path)
                    if isinstance(value, str) and value.strip():
                        return value

    raise ValueError(
        "Could not find Markdown content in JSON. "
        "Provide a top-level 'report_md' or 'markdown' string."
    )


def _read_answer(answer_path: Path) -> str:
    if answer_path.suffix.lower() == ".json":
        payload = json.loads(answer_path.read_text(encoding="utf-8"))
        return _extract_markdown_from_json(payload)
    return _read_text(answer_path)


def _infer_report_dir(answer_path: Path) -> Path:
    if answer_path.parent.name == "raw":
        return answer_path.parent.parent
    return answer_path.parent


def ingest_answer(answer_path: Path, *, report_dir: Path, out_path: Path) -> Path:
    raw_text = _read_answer(answer_path)
    normalized = _normalize_markdown(raw_text)

    if not normalized.strip():
        raise ValueError("Normalized content is empty. Check the input answer.")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(normalized, encoding="utf-8")
    return out_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest a manual LLM answer into canonical report.md."
    )
    parser.add_argument(
        "answer_path",
        help="Path to the manual LLM answer (Markdown or JSON).",
    )
    parser.add_argument(
        "--report-dir",
        default="",
        help=(
            "Target report directory. Defaults to the parent directory "
            "(or parent of /raw) for the answer file."
        ),
    )
    parser.add_argument(
        "--out",
        default="",
        help="Optional custom output path. Defaults to <report-dir>/report.md.",
    )
    parser.add_argument(
        "--no-suggest-fixes",
        action="store_true",
        help="Disable repair suggestions when validation fails.",
    )
    return parser


def main(argv: list[str]) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    answer_path = Path(args.answer_path).resolve()
    if not answer_path.is_file():
        print(f"Answer file not found: {answer_path}", file=sys.stderr)
        return 2

    report_dir = Path(args.report_dir).resolve() if args.report_dir else _infer_report_dir(answer_path)
    out_path = Path(args.out).resolve() if args.out else report_dir / "report.md"

    try:
        written = ingest_answer(answer_path, report_dir=report_dir, out_path=out_path)
    except Exception as exc:
        print(f"Failed to ingest answer: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote report: {written}")
    try:
        validator = _load_validator_module()
    except Exception as exc:
        print(f"Validation failed to run: {exc}", file=sys.stderr)
        return 1

    result = validator.validate_report(written)
    validator._print_result(written, result)

    if not result.ok and not args.no_suggest_fixes:
        _suggest_fixes(result.errors)

    return 0 if result.ok else 1


def _suggest_fixes(errors: list[str]) -> None:
    suggestions: list[str] = []
    for error in errors:
        if "Missing required heading" in error:
            suggestions.append(
                "Use the canonical template in business-conspect/README.md (Section 4.6)."
            )
        if "Missing metadata field" in error or "Generated At (UTC)" in error:
            suggestions.append(
                "Ensure all metadata fields are present; consider running init_answer_template.py."
            )
        if "Services section must include at least one ordered list item" in error:
            suggestions.append("Add numbered services under the Services section.")
        if "must include a '- Who it is for:'" in error:
            suggestions.append("Add '- Who it is for:' to each service block.")
        if "must include a '- Expected outcome:'" in error:
            suggestions.append("Add '- Expected outcome:' to each service block.")
        if "must contain at least one '[evidence:" in error:
            suggestions.append("Add evidence markers with source URLs.")
        if "ICP section must include a '- Situation trigger:'" in error:
            suggestions.append("Add '- Situation trigger:' to the ICP section.")
        if "Dialogue must cover search intent" in error:
            suggestions.append(
                "Add Client questions for missing intents (outcome, selection, pricing, constraints, non-fit)."
            )
        if "Dialogue section must contain at least one 'Client:'" in error:
            suggestions.append("Add at least one 'Client:' line.")
        if "Dialogue section must contain at least one 'Expert:'" in error:
            suggestions.append("Add at least one 'Expert:' line.")

    if suggestions:
        print("\nSuggestions:")
        for suggestion in sorted(set(suggestions)):
            print(f"- {suggestion}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
