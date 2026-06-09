import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.preferences import (
    PREFERENCES_FILENAME,
    describe_confirmed_preference_application,
    describe_preference_application_history,
    describe_preference_application_draft,
    describe_preference_reply_context,
    describe_preference_preview,
    describe_preferences,
    parse_preference_candidate,
    preference_count,
    read_preferences,
    remove_preference,
    save_preference,
    set_preference_enabled,
    undo_preference_application,
)
from jarvis_lite.runtime_context import load_runtime_context


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

    def test_preference_application_draft_reports_empty_enabled_preferences(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            save_preference(paths, "回答尽量简洁", source="test")

            draft = describe_preference_application_draft(paths, "帮我总结知识库")

            self.assertIn("待确认偏好应用草稿", draft)
            self.assertIn("预览输入：帮我总结知识库", draft)
            self.assertIn("已启用偏好：0 条", draft)
            self.assertIn("暂无已启用偏好", draft)
            self.assertIn("可用 /preference-enable 编号或ID 启用", draft)
            self.assertIn("当前阶段不真正应用偏好", draft)

    def test_preference_application_draft_lists_enabled_preferences_and_conflicts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            concise = save_preference(paths, "回答尽量简洁", source="test")
            detailed = save_preference(paths, "回答尽量详细", source="test")
            set_preference_enabled(paths, concise.preference_id, True)
            set_preference_enabled(paths, detailed.preference_id, True)

            draft = describe_preference_application_draft(paths, "解释这个项目")

            self.assertIn("待确认偏好应用草稿", draft)
            self.assertIn("确认状态：待用户显式确认", draft)
            self.assertIn("预览输入：解释这个项目", draft)
            self.assertIn("已启用偏好：2 条", draft)
            self.assertIn(f"1. [{concise.preference_id}] 回答尽量简洁", draft)
            self.assertIn(f"2. [{detailed.preference_id}] 回答尽量详细", draft)
            self.assertIn("偏好冲突提示", draft)
            self.assertIn("只提示冲突，不自动裁决优先级", draft)
            self.assertIn("当前阶段不自动改变回复风格、LLM prompt、路由或执行决策", draft)
            self.assertIn("当前阶段不真正应用偏好", draft)

    def test_confirmed_preference_application_requires_enabled_preferences(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            save_preference(paths, "回答尽量简洁", source="test")

            confirmation = describe_confirmed_preference_application(paths, "帮我总结知识库")

            self.assertIn("无法确认偏好应用：暂无已启用偏好", confirmation)
            self.assertIn("可用 /preference-enable 编号或ID 启用", confirmation)
            self.assertIn("未确认应用偏好", confirmation)

    def test_confirmed_preference_application_reports_one_shot_scope(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            concise = save_preference(paths, "回答尽量简洁", source="test")
            chinese = save_preference(paths, "优先使用中文", source="test")
            set_preference_enabled(paths, concise.preference_id, True)
            set_preference_enabled(paths, chinese.preference_id, True)

            confirmation = describe_confirmed_preference_application(paths, "帮我总结知识库")

            self.assertIn("已确认本次偏好应用", confirmation)
            self.assertIn("应用输入：帮我总结知识库", confirmation)
            self.assertIn("已确认偏好：2 条", confirmation)
            self.assertIn(f"1. [{concise.preference_id}] 回答尽量简洁", confirmation)
            self.assertIn(f"2. [{chinese.preference_id}] 优先使用中文", confirmation)
            self.assertIn("应用范围：仅限本次 /preference-apply-confirm 命令输出", confirmation)
            self.assertIn("不写入 LLM prompt", confirmation)
            self.assertIn("不影响普通聊天、路由或执行决策", confirmation)

    def test_confirmed_preference_application_records_auditable_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            preference = save_preference(paths, "回答尽量简洁", source="test")
            set_preference_enabled(paths, preference.preference_id, True)

            confirmation = describe_confirmed_preference_application(paths, "帮我总结知识库")
            history = describe_preference_application_history(paths)

            self.assertRegex(confirmation, r"确认ID：prefapp-[0-9a-f]{10}")
            self.assertIn("偏好应用确认历史", history)
            self.assertIn("1. 已确认 [prefapp-", history)
            self.assertIn("应用输入：帮我总结知识库", history)
            self.assertIn(f"- [{preference.preference_id}] 回答尽量简洁", history)
            self.assertIn("撤销确认：/preference-apply-undo 编号或ID", history)

    def test_confirmed_preference_application_keeps_same_second_duplicate_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            preference = save_preference(paths, "回答尽量简洁", source="test")
            set_preference_enabled(paths, preference.preference_id, True)

            with patch("jarvis_lite.preferences._now_iso", return_value="2026-06-09T15:23:28"):
                describe_confirmed_preference_application(paths, "帮我总结知识库")
                describe_confirmed_preference_application(paths, "帮我总结知识库")

            applications = load_runtime_context(paths).recent_preference_applications
            history = describe_preference_application_history(paths)

            self.assertEqual(len(applications), 2)
            self.assertNotEqual(applications[0].application_id, applications[1].application_id)
            self.assertIn("1. 已确认 [prefapp-", history)
            self.assertIn("2. 已确认 [prefapp-", history)

    def test_failed_preference_application_confirmation_does_not_record_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            concise = save_preference(paths, "回答尽量简洁", source="test")
            detailed = save_preference(paths, "回答尽量详细", source="test")

            no_enabled = describe_confirmed_preference_application(paths, "帮我总结知识库")
            set_preference_enabled(paths, concise.preference_id, True)
            set_preference_enabled(paths, detailed.preference_id, True)
            conflicted = describe_confirmed_preference_application(paths, "帮我总结知识库")
            history = describe_preference_application_history(paths)

            self.assertIn("无法确认偏好应用：暂无已启用偏好", no_enabled)
            self.assertIn("无法确认偏好应用：存在偏好冲突", conflicted)
            self.assertIn("偏好应用确认历史：暂无", history)

    def test_preference_application_undo_marks_history_without_disabling_preferences(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            preference = save_preference(paths, "回答尽量简洁", source="test")
            set_preference_enabled(paths, preference.preference_id, True)
            describe_confirmed_preference_application(paths, "帮我总结知识库")

            undo = undo_preference_application(paths, 1)
            history = describe_preference_application_history(paths)
            preferences = read_preferences(paths)

            self.assertIn("已撤销偏好应用确认", undo)
            self.assertIn("只撤销确认记录", undo)
            self.assertIn("不删除或停用偏好", undo)
            self.assertIn("不回滚已经展示的输出", undo)
            self.assertIn("1. 已撤销 [prefapp-", history)
            self.assertTrue(preferences[0].enabled)

    def test_preference_reply_context_uses_latest_confirmed_application_until_undone(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            preference = save_preference(paths, "回答尽量简洁", source="test")
            set_preference_enabled(paths, preference.preference_id, True)
            confirmation = describe_confirmed_preference_application(paths, "帮我总结知识库")

            reply_context = describe_preference_reply_context(paths)
            undo_preference_application(paths, 1)
            context_after_undo = describe_preference_reply_context(paths)

            self.assertIn("确认ID：prefapp-", confirmation)
            self.assertIn("已确认偏好应用：prefapp-", reply_context)
            self.assertIn(f"- [{preference.preference_id}] 回答尽量简洁", reply_context)
            self.assertIn("应用边界：仅作为普通 LLM fallback 上下文", reply_context)
            self.assertEqual(context_after_undo, "")

    def test_preference_reply_context_requires_enabled_preferences_to_match_confirmation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            concise = save_preference(paths, "回答尽量简洁", source="test")
            chinese = save_preference(paths, "优先使用中文", source="test")
            set_preference_enabled(paths, concise.preference_id, True)
            describe_confirmed_preference_application(paths, "帮我总结知识库")

            context_before_change = describe_preference_reply_context(paths)
            set_preference_enabled(paths, chinese.preference_id, True)
            context_after_change = describe_preference_reply_context(paths)

            self.assertIn(f"- [{concise.preference_id}] 回答尽量简洁", context_before_change)
            self.assertEqual(context_after_change, "")

    def test_confirmed_preference_application_rejects_enabled_conflicts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            concise = save_preference(paths, "回答尽量简洁", source="test")
            detailed = save_preference(paths, "回答尽量详细", source="test")
            set_preference_enabled(paths, concise.preference_id, True)
            set_preference_enabled(paths, detailed.preference_id, True)

            confirmation = describe_confirmed_preference_application(paths, "解释这个项目")

            self.assertIn("无法确认偏好应用：存在偏好冲突", confirmation)
            self.assertIn("偏好冲突提示", confirmation)
            self.assertIn(f"{concise.preference_id} 回答尽量简洁", confirmation)
            self.assertIn(f"{detailed.preference_id} 回答尽量详细", confirmation)
            self.assertIn("只提示冲突，不自动裁决优先级", confirmation)
            self.assertIn("未确认应用偏好", confirmation)
            self.assertIn("可用 /preference-disable 编号或ID 停用冲突偏好", confirmation)

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
