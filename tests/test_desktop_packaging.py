import sys
import tomllib
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite import __version__
from jarvis_lite.desktop.packaging import (
    DESKTOP_EXE_NAME,
    default_desktop_build_paths,
    pyinstaller_desktop_args,
    render_windows_version_info,
    windows_version_tuple,
    write_windows_version_file,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DesktopPackagingTests(unittest.TestCase):
    def test_pyproject_declares_desktop_build_optional_dependency(self):
        pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

        self.assertIn("desktop-build", pyproject["project"]["optional-dependencies"])
        self.assertIn("pyinstaller>=6,<7", pyproject["project"]["optional-dependencies"]["desktop-build"])

    def test_default_desktop_build_paths_live_outside_project(self):
        paths = default_desktop_build_paths(PROJECT_ROOT)

        self.assertEqual(paths.output_root, PROJECT_ROOT.parent / "jarvis-lite-dist")
        self.assertEqual(paths.dist_dir, paths.output_root / "desktop-exe")
        self.assertEqual(paths.build_dir, paths.output_root / "pyinstaller-build")
        self.assertEqual(paths.spec_dir, paths.output_root / "pyinstaller-spec")
        self.assertEqual(paths.launcher_path, PROJECT_ROOT / "packaging" / "windows" / "desktop_launcher.py")
        self.assertEqual(paths.assets_dir, PROJECT_ROOT / "src" / "jarvis_lite" / "desktop" / "assets")
        self.assertEqual(paths.icon_path, PROJECT_ROOT / "packaging" / "windows" / "JarvisLite.ico")
        self.assertEqual(paths.version_file_path, paths.output_root / "JarvisLite.version.txt")

    def test_windows_icon_asset_is_available_for_packaging(self):
        icon_path = PROJECT_ROOT / "packaging" / "windows" / "JarvisLite.ico"

        icon_header = icon_path.read_bytes()[:6]

        self.assertEqual(icon_header[:4], b"\x00\x00\x01\x00")
        self.assertGreater(int.from_bytes(icon_header[4:6], "little"), 0)

    def test_pyinstaller_desktop_args_are_deterministic(self):
        paths = default_desktop_build_paths(PROJECT_ROOT)

        args = pyinstaller_desktop_args(paths)

        self.assertEqual(args[0:3], ["--noconfirm", "--clean", "--windowed"])
        self.assertIn(DESKTOP_EXE_NAME, args)
        self.assertIn(str(paths.dist_dir), args)
        self.assertIn(str(paths.build_dir), args)
        self.assertIn(str(paths.spec_dir), args)
        self.assertIn(str(paths.launcher_path), args)
        self.assertIn(f"{paths.assets_dir};jarvis_lite/desktop/assets", args)
        self.assertIn("--icon", args)
        self.assertIn(str(paths.icon_path), args)
        self.assertIn("--version-file", args)
        self.assertIn(str(paths.version_file_path), args)

    def test_windows_version_tuple_pads_to_four_segments(self):
        self.assertEqual(windows_version_tuple("1.2.3"), (1, 2, 3, 0))
        self.assertEqual(windows_version_tuple("10.20.30.40"), (10, 20, 30, 40))
        self.assertEqual(windows_version_tuple("2.5.0-dev"), (2, 5, 0, 0))

    def test_windows_version_info_contains_project_metadata(self):
        version_info = render_windows_version_info("1.2.3")

        self.assertIn("FileDescription", version_info)
        self.assertIn("Jarvis Lite desktop assistant", version_info)
        self.assertIn("ProductName", version_info)
        self.assertIn("Jarvis Lite", version_info)
        self.assertIn("FileVersion", version_info)
        self.assertIn("1.2.3", version_info)

    def test_write_windows_version_file_uses_current_project_version(self):
        paths = default_desktop_build_paths(PROJECT_ROOT)

        written_path = write_windows_version_file(paths)

        self.assertEqual(written_path, paths.version_file_path)
        self.assertIn(__version__, written_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
