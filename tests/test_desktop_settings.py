import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.desktop.settings import (
    DesktopSettings,
    desktop_settings_path,
    load_desktop_settings,
    runtime_dir,
    save_desktop_panel_size,
    save_desktop_preferences,
    save_desktop_position,
    save_desktop_settings,
)


class DesktopSettingsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name) / "jarvis-lite"
        self.paths = build_project_paths(self.project_root)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_runtime_dir_lives_next_to_project_root(self):
        self.assertEqual(runtime_dir(self.paths), self.project_root.parent / "jarvis-lite-runtime")
        self.assertEqual(desktop_settings_path(self.paths), self.project_root.parent / "jarvis-lite-runtime" / "desktop-settings.json")

    def test_save_and_load_desktop_position(self):
        saved = save_desktop_position(self.paths, 320, 180)
        loaded = load_desktop_settings(self.paths)

        self.assertEqual(saved.position_x, 320)
        self.assertEqual(saved.position_y, 180)
        self.assertEqual(loaded.position_x, 320)
        self.assertEqual(loaded.position_y, 180)
        self.assertTrue(desktop_settings_path(self.paths).is_file())

    def test_default_desktop_preferences_are_restored_when_missing(self):
        loaded = load_desktop_settings(self.paths)

        self.assertTrue(loaded.always_on_top)
        self.assertEqual(loaded.opacity_percent, 100)
        self.assertEqual(loaded.pet_size, 148)
        self.assertFalse(loaded.launch_at_login)

    def test_save_and_load_desktop_preferences(self):
        saved = save_desktop_preferences(
            self.paths,
            always_on_top=False,
            opacity_percent=82,
            pet_size=184,
            launch_at_login=True,
        )
        loaded = load_desktop_settings(self.paths)

        self.assertFalse(saved.always_on_top)
        self.assertEqual(saved.opacity_percent, 82)
        self.assertEqual(saved.pet_size, 184)
        self.assertTrue(saved.launch_at_login)
        self.assertFalse(loaded.always_on_top)
        self.assertEqual(loaded.opacity_percent, 82)
        self.assertEqual(loaded.pet_size, 184)
        self.assertTrue(loaded.launch_at_login)

    def test_save_and_load_desktop_panel_size(self):
        saved = save_desktop_panel_size(self.paths, 560, 700)
        loaded = load_desktop_settings(self.paths)

        self.assertEqual(saved.panel_width, 560)
        self.assertEqual(saved.panel_height, 700)
        self.assertEqual(loaded.panel_width, 560)
        self.assertEqual(loaded.panel_height, 700)

    def test_save_position_preserves_existing_desktop_preferences(self):
        save_desktop_settings(
            self.paths,
            DesktopSettings(
                position_x=10,
                position_y=20,
                always_on_top=False,
                opacity_percent=76,
                pet_size=172,
                launch_at_login=True,
                panel_width=560,
                panel_height=700,
            ),
        )

        loaded = save_desktop_position(self.paths, 320, 180)

        self.assertEqual(loaded.position_x, 320)
        self.assertEqual(loaded.position_y, 180)
        self.assertFalse(loaded.always_on_top)
        self.assertEqual(loaded.opacity_percent, 76)
        self.assertEqual(loaded.pet_size, 172)
        self.assertTrue(loaded.launch_at_login)
        self.assertEqual(loaded.panel_width, 560)
        self.assertEqual(loaded.panel_height, 700)

    def test_save_panel_size_preserves_position_and_preferences(self):
        save_desktop_settings(
            self.paths,
            DesktopSettings(
                position_x=10,
                position_y=20,
                always_on_top=False,
                opacity_percent=76,
                pet_size=172,
                launch_at_login=True,
            ),
        )

        loaded = save_desktop_panel_size(self.paths, 580, 720)

        self.assertEqual(loaded.position_x, 10)
        self.assertEqual(loaded.position_y, 20)
        self.assertFalse(loaded.always_on_top)
        self.assertEqual(loaded.opacity_percent, 76)
        self.assertEqual(loaded.pet_size, 172)
        self.assertTrue(loaded.launch_at_login)
        self.assertEqual(loaded.panel_width, 580)
        self.assertEqual(loaded.panel_height, 720)

    def test_load_settings_falls_back_to_defaults_when_runtime_file_is_invalid(self):
        settings_path = desktop_settings_path(self.paths)
        settings_path.parent.mkdir(parents=True)
        settings_path.write_text("not-json", encoding="utf-8")

        loaded = load_desktop_settings(self.paths)

        self.assertEqual(loaded.position_x, 80)
        self.assertEqual(loaded.position_y, 80)


if __name__ == "__main__":
    unittest.main()
