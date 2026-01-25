import importlib.util
import sys
import unittest
from pathlib import Path


def _load_module(module_path: Path):
    spec = importlib.util.spec_from_file_location(
        f"validate_report_{module_path.stat().st_mtime_ns}", module_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load validate_report module.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)  # type: ignore[call-arg]
    return module


class TestValidateReport(unittest.TestCase):
    def setUp(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        self.module = _load_module(repo_root / "business-conspect/scripts/validate_report.py")
        self.valid_path = repo_root / "business-conspect/reports/fixtures/valid/report.md"
        self.invalid_path = repo_root / "business-conspect/reports/fixtures/invalid/report.md"

    def test_validate_report_fixtures(self):
        valid_result = self.module.validate_report(self.valid_path)
        self.assertTrue(valid_result.ok)
        self.assertFalse(valid_result.errors)

        invalid_result = self.module.validate_report(self.invalid_path)
        self.assertFalse(invalid_result.ok)
        self.assertTrue(invalid_result.errors)
