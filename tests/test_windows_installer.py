import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.desktop.windows_installer import (
    INSTALLER_EXE_NAME,
    render_iexpress_sed,
    render_install_script,
    render_uninstall_script,
    windows_installer_paths,
)


class WindowsInstallerTests(unittest.TestCase):
    def test_install_script_copies_exe_and_registers_uninstall(self):
        script = render_install_script("JarvisLite.exe")

        self.assertIn(r"%LOCALAPPDATA%\Programs\Jarvis Lite", script)
        self.assertIn("JarvisLite.exe", script)
        self.assertIn("Jarvis Lite.lnk", script)
        self.assertIn("Uninstall Jarvis Lite.lnk", script)
        self.assertIn(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\JarvisLite", script)

    def test_install_script_uses_supplied_project_version(self):
        script = render_install_script("JarvisLite.exe", version="9.8.7")

        self.assertIn('DisplayVersion /d "9.8.7"', script)

    def test_install_script_prepares_for_cover_install_and_complete_uninstall_metadata(self):
        script = render_install_script("JarvisLite.exe", version="9.8.7")

        self.assertIn("taskkill /IM JarvisLite.exe /F", script)
        self.assertIn('DisplayIcon /d "%INSTALL_DIR%\\JarvisLite.exe"', script)
        self.assertIn('QuietUninstallString /d "\\"%INSTALL_DIR%\\uninstall.cmd\\""', script)

    def test_uninstall_script_removes_shortcuts_install_dir_and_registry(self):
        script = render_uninstall_script()

        self.assertIn("Jarvis Lite.lnk", script)
        self.assertIn("Uninstall Jarvis Lite.lnk", script)
        self.assertIn(r"%LOCALAPPDATA%\Programs\Jarvis Lite", script)
        self.assertIn(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\JarvisLite", script)

    def test_uninstall_script_removes_startup_shortcut_and_stops_running_app(self):
        script = render_uninstall_script()

        self.assertIn(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup", script)
        self.assertIn("taskkill /IM JarvisLite.exe /F", script)
        self.assertIn('del "%STARTUP_DIR%\\Jarvis Lite.lnk"', script)

    def test_uninstall_script_preserves_user_data_directory(self):
        script = render_uninstall_script()

        self.assertIn(r"%LOCALAPPDATA%\Jarvis Lite", script)
        self.assertIn("User data kept", script)
        self.assertNotIn(r'rmdir /S /Q "%LOCALAPPDATA%\Jarvis Lite"', script)

    def test_iexpress_sed_points_to_external_installer_output_and_packaged_exe(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "jarvis-lite"
            project_root.mkdir()
            paths = windows_installer_paths(project_root=project_root)
            sed = render_iexpress_sed(paths)

        self.assertEqual(paths.output_root, project_root.parent / "jarvis-lite-dist")
        self.assertEqual(paths.installer_path.name, INSTALLER_EXE_NAME)
        self.assertIn(f"TargetName={paths.installer_path}", sed)
        self.assertIn("AppLaunched=install.cmd", sed)
        self.assertIn("JarvisLite.exe=", sed)
        self.assertIn("install.cmd=", sed)
        self.assertIn("uninstall.cmd=", sed)


if __name__ == "__main__":
    unittest.main()
