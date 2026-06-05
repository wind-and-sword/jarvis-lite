import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.preferences import (
    PREFERENCES_FILENAME,
    describe_preference_preview,
    describe_preferences,
    parse_preference_candidate,
    preference_count,
    read_preferences,
    remove_preference,
    save_preference,
    set_preference_enabled,
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
            self.assertRegex(saved.preference_id, r"^pref-[0-9a-f]{10}$")
            self.assertFalse(saved.enabled)
            self.assertEqual(count_after_save, 1)
            self.assertEqual(preferences_after_save[0].preference, "回答尽量简洁")
            self.assertEqual(preferences_after_save[0].preference_id, saved.preference_id)
            self.assertFalse(preferences_after_save[0].enabled)
            self.assertTrue((paths.config_dir / PREFERENCES_FILENAME).exists())
            self.assertIn("本地偏好：1 条", description_after_save)
            self.assertIn("已启用：0 条", description_after_save)
            self.assertIn("未启用：1 条", description_after_save)
            self.assertIn(f"1. 未启用 [{saved.preference_id}] 回答尽量简洁", description_after_save)
            self.assertIn("不自动改变回复风格、LLM prompt、路由或执行决策", description_after_save)
            self.assertTrue(removed)
            self.assertEqual(preferences_after_remove, ())
            self.assertEqual(preference_count(paths), 0)
            self.assertNotIn(
                "回答尽量简洁",
                (paths.config_dir / PREFERENCES_FILENAME).read_text(encoding="utf-8"),
            )

    def test_preference_store_derives_stable_ids_for_legacy_records(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            preferences_path = paths.config_dir / PREFERENCES_FILENAME
            preferences_path.parent.mkdir(parents=True, exist_ok=True)
            preferences_path.write_text(
                json.dumps(
                    {
                        "preferences": [
                            {
                                "preference": "优先使用中文",
                                "enabled": True,
                                "source": "legacy",
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            first_read = read_preferences(paths)
            second_read = read_preferences(paths)
            status = describe_preferences(paths)

            self.assertEqual(first_read[0].preference, "优先使用中文")
            self.assertRegex(first_read[0].preference_id, r"^pref-[0-9a-f]{10}$")
            self.assertEqual(first_read[0].preference_id, second_read[0].preference_id)
            self.assertIn(f"1. 已启用 [{first_read[0].preference_id}] 优先使用中文", status)

    def test_preference_candidate_rejects_empty_content(self):
        with self.assertRaises(ValueError) as context:
            parse_preference_candidate("   ")

        self.assertIn("偏好候选格式：偏好内容不能为空。", str(context.exception))

    def test_preference_store_enables_and_disables_preferences_by_index(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            save_preference(paths, "回答尽量简洁", source="test")

            enabled = set_preference_enabled(paths, 1, True)
            preferences_after_enable = read_preferences(paths)
            status_after_enable = describe_preferences(paths)
            disabled = set_preference_enabled(paths, enabled.preference_id, False)
            preferences_after_disable = read_preferences(paths)
            status_after_disable = describe_preferences(paths)

            self.assertTrue(enabled.enabled)
            self.assertEqual(enabled.preference, "回答尽量简洁")
            self.assertTrue(preferences_after_enable[0].enabled)
            self.assertIn("已启用：1 条", status_after_enable)
            self.assertIn("未启用：0 条", status_after_enable)
            self.assertIn(f"1. 已启用 [{enabled.preference_id}] 回答尽量简洁", status_after_enable)
            self.assertFalse(disabled.enabled)
            self.assertFalse(preferences_after_disable[0].enabled)
            self.assertIn("已启用：0 条", status_after_disable)
            self.assertIn("未启用：1 条", status_after_disable)
            self.assertIn(f"1. 未启用 [{enabled.preference_id}] 回答尽量简洁", status_after_disable)

    def test_preference_enable_rejects_invalid_index_without_writing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            save_preference(paths, "回答尽量简洁", source="test")

            with self.assertRaises(ValueError) as context:
                set_preference_enabled(paths, 2, True)

            self.assertIn("偏好引用不存在", str(context.exception))
            self.assertFalse(read_preferences(paths)[0].enabled)

    def test_preference_preview_lists_only_enabled_preferences_for_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            save_preference(paths, "回答尽量简洁", source="test")
            save_preference(paths, "优先使用中文", source="test")
            set_preference_enabled(paths, 2, True)

            preview = describe_preference_preview(paths, "帮我总结知识库")
            enabled_id = read_preferences(paths)[1].preference_id

            self.assertIn("偏好应用预览", preview)
            self.assertIn("预览输入：帮我总结知识库", preview)
            self.assertIn("已启用偏好：1 条", preview)
            self.assertIn(f"1. [{enabled_id}] 优先使用中文", preview)
            self.assertNotIn("回答尽量简洁", preview)
            self.assertIn("不自动改变回复风格、LLM prompt、路由或执行决策", preview)

    def test_preference_preview_reports_empty_enabled_preferences(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            save_preference(paths, "回答尽量简洁", source="test")

            preview = describe_preference_preview(paths)

            self.assertIn("偏好应用预览", preview)
            self.assertIn("已启用偏好：0 条", preview)
            self.assertIn("暂无已启用偏好", preview)
            self.assertIn("可用 /preference-enable 编号或ID 启用", preview)

    def test_preference_status_and_preview_report_enabled_conflicts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            concise = save_preference(paths, "回答尽量简洁", source="test")
            detailed = save_preference(paths, "回答尽量详细", source="test")
            set_preference_enabled(paths, concise.preference_id, True)
            set_preference_enabled(paths, detailed.preference_id, True)

            status = describe_preferences(paths)
            preview = describe_preference_preview(paths, "解释这个项目")

            self.assertIn("偏好冲突提示", status)
            self.assertIn(f"{concise.preference_id} 回答尽量简洁", status)
            self.assertIn(f"{detailed.preference_id} 回答尽量详细", status)
            self.assertIn("只提示冲突，不自动裁决优先级", status)
            self.assertIn("偏好冲突提示", preview)
            self.assertIn(f"{concise.preference_id} 回答尽量简洁", preview)
            self.assertIn(f"{detailed.preference_id} 回答尽量详细", preview)
            self.assertIn("当前不自动改变回复风格、LLM prompt、路由或执行决策", preview)


if __name__ == "__main__":
    unittest.main()
