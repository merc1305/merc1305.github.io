import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


def _load_module(module_path: Path):
    spec = importlib.util.spec_from_file_location(
        f"update_index_{module_path.stat().st_mtime_ns}", module_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load update_index module.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[call-arg]
    return module


def _write_minimal_index(root: Path, marker_start: str, marker_end: str) -> None:
    content = f"""<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>Index</title></head>
  <body>
    <h1>Reports</h1>
    {marker_start}
    <div>Placeholder</div>
    {marker_end}
  </body>
</html>
"""
    (root / "index.html").write_text(content, encoding="utf-8")


class TestUpdateIndex(unittest.TestCase):
    def setUp(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        self.module = _load_module(repo_root / "business-conspect/scripts/update_index.py")

    def test_discover_reports_includes_report_md_link(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            reports_root = tmp_root / "reports"
            report_dir = reports_root / "2026-01-25" / "example.com"
            report_dir.mkdir(parents=True)
            (report_dir / "index.html").write_text("<html></html>", encoding="utf-8")
            (report_dir / "report.md").write_text(
                "# Business Conspect — example.com", encoding="utf-8"
            )

            _write_minimal_index(tmp_root, self.module.MARKER_START, self.module.MARKER_END)

            entries = self.module.discover_reports(
                reports_root, tmp_root, include_missing_report_md=True
            )
            self.assertEqual(len(entries), 1)
            self.assertIsNotNone(entries[0].report_md_rel_path)

            self.module.update_index_html(tmp_root, entries)
            self.module.write_index_json(tmp_root, entries)

            payload = json.loads((tmp_root / "index.json").read_text(encoding="utf-8"))
            self.assertIsNotNone(payload[0]["reportMdPath"])

    def test_discover_reports_skip_missing_report_md(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            reports_root = tmp_root / "reports"
            report_dir = reports_root / "2026-01-25" / "example.com"
            report_dir.mkdir(parents=True)
            (report_dir / "index.html").write_text("<html></html>", encoding="utf-8")

            entries_included = self.module.discover_reports(
                reports_root, tmp_root, include_missing_report_md=True
            )
            self.assertEqual(len(entries_included), 1)
            self.assertIsNone(entries_included[0].report_md_rel_path)

            entries_skipped = self.module.discover_reports(
                reports_root, tmp_root, include_missing_report_md=False
            )
            self.assertEqual(entries_skipped, [])
