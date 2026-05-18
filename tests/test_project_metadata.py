import sys
import tomllib
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ProjectMetadataTests(unittest.TestCase):
    def test_pyproject_requires_python_313_series(self):
        pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

        self.assertEqual(pyproject["project"]["requires-python"], ">=3.13,<3.14")

    def test_python_version_file_pins_313_series(self):
        self.assertEqual((PROJECT_ROOT / ".python-version").read_text(encoding="utf-8").strip(), "3.13")

    def test_current_test_runner_uses_python_313(self):
        self.assertEqual(sys.version_info[:2], (3, 13))


if __name__ == "__main__":
    unittest.main()
