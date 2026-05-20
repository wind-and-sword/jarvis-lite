import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.desktop.app_style import (
    DEFAULT_THEME_NAME,
    THEME_PRESETS,
    desktop_theme_names,
    normalize_theme_name,
    panel_style,
    pet_style,
)


class DesktopStyleTests(unittest.TestCase):
    def test_theme_presets_include_midnight_and_daylight(self):
        self.assertEqual(DEFAULT_THEME_NAME, "midnight")
        self.assertIn("midnight", desktop_theme_names())
        self.assertIn("daylight", desktop_theme_names())
        self.assertIn("midnight", THEME_PRESETS)
        self.assertIn("daylight", THEME_PRESETS)

    def test_invalid_theme_name_falls_back_to_default(self):
        self.assertEqual(normalize_theme_name("missing"), DEFAULT_THEME_NAME)
        self.assertEqual(normalize_theme_name("daylight"), "daylight")

    def test_panel_and_pet_styles_use_theme_colors(self):
        panel = panel_style("daylight")
        pet = pet_style("daylight")

        self.assertIn("#f8fafc", panel)
        self.assertIn("#0f766e", panel)
        self.assertIn("#ecfeff", pet)
        self.assertIn("#0f766e", pet)


if __name__ == "__main__":
    unittest.main()
