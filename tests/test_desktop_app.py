import io
import os
import sys
import tempfile
import tomllib
import unittest
from contextlib import redirect_stdout
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "minimal")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite import __version__
from jarvis_lite.config import build_project_paths
from jarvis_lite.desktop.app import apply_panel_settings, build_window_title, create_desktop_app, main
from jarvis_lite.desktop.settings import DesktopSettings


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

    def test_apply_panel_settings_updates_window_preferences_and_autostart(self):
        class FakeWindow:
            def __init__(self, paths):
                self.paths = paths
                self.values = None

            def apply_preferences(self, *, always_on_top, opacity_percent, pet_size, launch_at_login):
                self.values = (always_on_top, opacity_percent, pet_size, launch_at_login)

        calls = []
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "jarvis-lite"
            paths = build_project_paths(project_root)
            window = FakeWindow(paths)

            apply_panel_settings(
                DesktopSettings(always_on_top=False, opacity_percent=76, pet_size=172, launch_at_login=True),
                window,
                project_root,
                syncer=lambda enabled, shortcut: calls.append((enabled, shortcut)),
            )

        self.assertEqual(window.values, (False, 76, 172, True))
        self.assertEqual(calls[0][0], True)
        self.assertEqual(calls[0][1].arguments, "-m jarvis_lite.desktop.app")

    def test_apply_panel_settings_skips_autostart_sync_when_value_is_unchanged(self):
        class FakeWindow:
            def __init__(self, paths):
                self.paths = paths
                self.values = None

            def apply_preferences(self, *, always_on_top, opacity_percent, pet_size, launch_at_login):
                self.values = (always_on_top, opacity_percent, pet_size, launch_at_login)

        calls = []
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "jarvis-lite"
            paths = build_project_paths(project_root)
            window = FakeWindow(paths)

            apply_panel_settings(
                DesktopSettings(always_on_top=False, opacity_percent=76, pet_size=172, launch_at_login=False),
                window,
                project_root,
                syncer=lambda enabled, shortcut: calls.append((enabled, shortcut)),
            )

        self.assertEqual(window.values, (False, 76, 172, False))
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
