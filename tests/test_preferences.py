import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.preferences import (
    PREFERENCES_FILENAME,
    describe_preferences,
    parse_preference_candidate,
    preference_count,
    read_preferences,
    remove_preference,
    save_preference,
)


class PreferenceTests(unittest.TestCase):
    def test_preference_store_writes_counts_describes_and_removes_preferences(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")

            parsed = parse_preference_candidate(" 回答尽量简洁 ")
            saved = save_preference(paths, parsed, source="test")
            preferences_after_save = read_preferences(paths)
            count_after_save = preference_count(paths)
            description_after_save = describe_preferences(paths)
            removed = remove_preference(paths, "回答尽量简洁")
            preferences_after_remove = read_preferences(paths)

            self.assertEqual(parsed, "回答尽量简洁")
            self.assertEqual(saved.preference, "回答尽量简洁")
            self.assertEqual(count_after_save, 1)
            self.assertEqual(preferences_after_save[0].preference, "回答尽量简洁")
            self.assertTrue((paths.config_dir / PREFERENCES_FILENAME).exists())
            self.assertIn("偏好：1 条", description_after_save)
            self.assertIn("- 回答尽量简洁", description_after_save)
            self.assertIn("不自动改变回复或执行决策", description_after_save)
            self.assertTrue(removed)
            self.assertEqual(preferences_after_remove, ())
            self.assertEqual(preference_count(paths), 0)
            self.assertNotIn(
                "回答尽量简洁",
                (paths.config_dir / PREFERENCES_FILENAME).read_text(encoding="utf-8"),
            )

    def test_preference_candidate_rejects_empty_content(self):
        with self.assertRaises(ValueError) as context:
            parse_preference_candidate("   ")

        self.assertIn("偏好候选格式：偏好内容不能为空。", str(context.exception))


if __name__ == "__main__":
    unittest.main()
