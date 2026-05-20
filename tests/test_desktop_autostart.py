import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.desktop.autostart import (
    SHORTCUT_NAME,
    default_autostart_shortcut,
    disable_windows_autostart,
    enable_windows_autostart,
    is_windows_autostart_enabled,
    render_shortcut_powershell,
    sync_windows_autostart,
    windows_startup_dir,
)


class DesktopAutostartTests(unittest.TestCase):
    def test_windows_startup_dir_uses_current_user_appdata(self):
        startup_dir = windows_startup_dir(appdata=r"C:\Users\Tester\AppData\Roaming")

        self.assertEqual(
            startup_dir,
            Path(r"C:\Users\Tester\AppData\Roaming") / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup",
        )

    def test_default_source_shortcut_points_to_python_module_entry(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "jarvis-lite"
            startup_dir = Path(temp_dir) / "Startup"
            executable = Path(temp_dir) / "python.exe"

            shortcut = default_autostart_shortcut(
                project_root=root,
                startup_dir=startup_dir,
                executable=executable,
                frozen=False,
            )

        self.assertEqual(shortcut.shortcut_path, startup_dir / SHORTCUT_NAME)
        self.assertEqual(shortcut.target_path, executable)
        self.assertEqual(shortcut.working_directory, root)
        self.assertEqual(shortcut.arguments, "-m jarvis_lite.desktop.app")

    def test_default_frozen_shortcut_points_to_current_exe_without_arguments(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            startup_dir = Path(temp_dir) / "Startup"
            executable = Path(temp_dir) / "JarvisLite.exe"

            shortcut = default_autostart_shortcut(
                project_root=Path(temp_dir) / "jarvis-lite",
                startup_dir=startup_dir,
                executable=executable,
                frozen=True,
            )

        self.assertEqual(shortcut.shortcut_path, startup_dir / SHORTCUT_NAME)
        self.assertEqual(shortcut.target_path, executable)
        self.assertEqual(shortcut.working_directory, executable.parent)
        self.assertEqual(shortcut.arguments, "")

    def test_render_shortcut_powershell_sets_target_arguments_workdir_and_icon(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            shortcut = default_autostart_shortcut(
                project_root=Path(temp_dir) / "jarvis-lite",
                startup_dir=Path(temp_dir) / "Startup",
                executable=Path(temp_dir) / "python.exe",
                frozen=False,
            )

            script = render_shortcut_powershell(shortcut)

        self.assertIn("CreateShortcut", script)
        self.assertIn(str(shortcut.shortcut_path), script)
        self.assertIn(str(shortcut.target_path), script)
        self.assertIn("-m jarvis_lite.desktop.app", script)
        self.assertIn(str(shortcut.working_directory), script)

    def test_enable_windows_autostart_invokes_powershell_runner(self):
        calls = []

        def fake_runner(command, check):
            calls.append((command, check))

        with tempfile.TemporaryDirectory() as temp_dir:
            shortcut = default_autostart_shortcut(
                project_root=Path(temp_dir) / "jarvis-lite",
                startup_dir=Path(temp_dir) / "Startup",
                executable=Path(temp_dir) / "python.exe",
                frozen=False,
            )

            enable_windows_autostart(shortcut, runner=fake_runner)
            self.assertTrue(shortcut.shortcut_path.parent.is_dir())

        self.assertEqual(calls[0][0][0], "powershell")
        self.assertIn("-Command", calls[0][0])
        self.assertTrue(calls[0][1])

    def test_disable_windows_autostart_removes_existing_shortcut(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            shortcut = default_autostart_shortcut(
                project_root=Path(temp_dir) / "jarvis-lite",
                startup_dir=Path(temp_dir) / "Startup",
                executable=Path(temp_dir) / "python.exe",
                frozen=False,
            )
            shortcut.shortcut_path.parent.mkdir(parents=True)
            shortcut.shortcut_path.write_text("shortcut", encoding="utf-8")

            disable_windows_autostart(shortcut)
            self.assertFalse(shortcut.shortcut_path.exists())

    def test_sync_windows_autostart_enables_or_disables_shortcut(self):
        calls = []

        def fake_runner(command, check):
            calls.append((command, check))

        with tempfile.TemporaryDirectory() as temp_dir:
            shortcut = default_autostart_shortcut(
                project_root=Path(temp_dir) / "jarvis-lite",
                startup_dir=Path(temp_dir) / "Startup",
                executable=Path(temp_dir) / "python.exe",
                frozen=False,
            )
            sync_windows_autostart(True, shortcut, runner=fake_runner)
            shortcut.shortcut_path.write_text("shortcut", encoding="utf-8")
            self.assertTrue(is_windows_autostart_enabled(shortcut))

            sync_windows_autostart(False, shortcut, runner=fake_runner)
            self.assertFalse(shortcut.shortcut_path.exists())

        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
