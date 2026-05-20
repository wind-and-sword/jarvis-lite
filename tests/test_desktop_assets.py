import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.desktop.assets import all_desktop_asset_paths, desktop_app_icon_path, desktop_asset_path
from jarvis_lite.desktop.state import DesktopState


class DesktopAssetTests(unittest.TestCase):
    def test_all_desktop_state_assets_exist_in_project(self):
        paths = all_desktop_asset_paths()

        self.assertEqual(set(paths), set(DesktopState))
        for state, path in paths.items():
            self.assertTrue(path.is_file(), f"{state} asset is missing")
            self.assertEqual(path.suffix, ".svg")
            self.assertIn("src", path.parts)
            self.assertIn("assets", path.parts)

    def test_desktop_asset_path_returns_state_specific_svg(self):
        self.assertEqual(desktop_asset_path(DesktopState.SUCCESS).name, "success.svg")
        self.assertEqual(desktop_asset_path(DesktopState.ERROR).name, "error.svg")

    def test_desktop_app_icon_exists_in_project_assets(self):
        path = desktop_app_icon_path()

        self.assertTrue(path.is_file())
        self.assertEqual(path.name, "app-icon.svg")
        self.assertIn("src", path.parts)
        self.assertIn("assets", path.parts)


if __name__ == "__main__":
    unittest.main()
