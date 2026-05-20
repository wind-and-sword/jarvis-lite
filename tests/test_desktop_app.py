import io
import os
import sys
import tomllib
import unittest
from contextlib import redirect_stdout
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "minimal")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite import __version__
from jarvis_lite.desktop.app import build_window_title, create_desktop_app, main


class DesktopAppTests(unittest.TestCase):
    def test_desktop_window_title_names_jarvis_lite(self):
        self.assertEqual(build_window_title(), "Jarvis Lite 桌面助手")

    def test_pyproject_declares_desktop_script_and_pyside_dependency(self):
        pyproject = tomllib.loads((Path(__file__).resolve().parents[1] / "pyproject.toml").read_text(encoding="utf-8"))

        self.assertEqual(pyproject["project"]["scripts"]["jarvis-lite-desktop"], "jarvis_lite.desktop.app:main")
        self.assertIn("PySide6>=6,<7", pyproject["project"]["dependencies"])

    def test_smoke_mode_creates_desktop_pet_window(self):
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["--smoke"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Jarvis Lite 桌面助手", output.getvalue())
        self.assertIn("desktopPetWindow", output.getvalue())

    def test_desktop_app_applies_application_identity_and_icons(self):
        app, window = create_desktop_app()
        self.addCleanup(window.close)
        self.addCleanup(app.quit)

        self.assertEqual(app.applicationName(), "Jarvis Lite")
        self.assertEqual(app.applicationVersion(), __version__)
        self.assertFalse(app.windowIcon().isNull())
        self.assertFalse(window.windowIcon().isNull())
        self.assertFalse(window.panel.windowIcon().isNull())


if __name__ == "__main__":
    unittest.main()
