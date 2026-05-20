import sys
import tomllib
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.desktop.packaging import DESKTOP_EXE_NAME, default_desktop_build_paths, pyinstaller_desktop_args


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


if __name__ == "__main__":
    unittest.main()
