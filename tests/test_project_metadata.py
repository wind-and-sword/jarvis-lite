import sys
import tomllib
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RELEASE_VERSION = "0.96.0"

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from jarvis_lite import __version__


class ProjectMetadataTests(unittest.TestCase):
    def test_pyproject_requires_python_313_series(self):
        pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

        self.assertEqual(pyproject["project"]["requires-python"], ">=3.13,<3.14")

    def test_python_version_file_pins_313_series(self):
        self.assertEqual((PROJECT_ROOT / ".python-version").read_text(encoding="utf-8").strip(), "3.13")

    def test_current_test_runner_uses_python_313(self):
        self.assertEqual(sys.version_info[:2], (3, 13))

    def test_project_version_matches_release_package_version(self):
        pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

        self.assertEqual(pyproject["project"]["version"], RELEASE_VERSION)
        self.assertEqual(__version__, RELEASE_VERSION)


if __name__ == "__main__":
    unittest.main()
