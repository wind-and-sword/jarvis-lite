import sys
import tomllib
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.desktop.app import build_window_title


class DesktopAppTests(unittest.TestCase):
    def test_desktop_window_title_names_jarvis_lite(self):
        self.assertEqual(build_window_title(), "Jarvis Lite 桌面助手")

    def test_pyproject_declares_desktop_script_and_pyside_dependency(self):
        pyproject = tomllib.loads((Path(__file__).resolve().parents[1] / "pyproject.toml").read_text(encoding="utf-8"))

        self.assertEqual(pyproject["project"]["scripts"]["jarvis-lite-desktop"], "jarvis_lite.desktop.app:main")
        self.assertIn("PySide6>=6,<7", pyproject["project"]["dependencies"])


if __name__ == "__main__":
    unittest.main()
