import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.inner_brain import (
    InnerBrain,
    InnerBrainPolicy,
    describe_inner_brain_result,
    save_labeled_runtime_training_sample,
    save_runtime_training_sample,
)


class InnerBrainTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_greeting_uses_sample_classifier_before_legacy_fallback(self):
        result = InnerBrain(self.paths).understand("早上好")

        self.assertEqual(result.intent, "assistant.greeting")
        self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
        self.assertEqual(result.source, "seed_sample")
        self.assertEqual(result.confidence, 1.0)
        self.assertEqual(result.missing, ())
        self.assertIsNotNone(result.natural_language_intent)
        self.assertEqual(result.natural_language_intent.name, "greeting")

    def test_high_frequency_intents_use_sample_classifier(self):
        cases = (
            ("总结知识库", "knowledge.summary", "command", "/kb-summary"),
            ("查看最近上下文", "context.recent_status", "recent_context_status", ""),
            ("查看最近文件", "context.recent_files", "recent_files_status", ""),
            ("有什么功能", "assistant.capabilities", "capabilities", ""),
            ("查看常用目录", "directory.list", "command", "/dirs"),
            ("目录列表", "directory.list", "command", "/dirs"),
            ("检查更新", "update.status", "command", "/update-status"),
            ("下载最新版", "update.download", "command", "/update-download"),
            ("查看经验记忆", "experience.status", "command", "/experiences"),
            ("确认执行", "advice.confirm_execution", "confirm_pending_advice_suggestion_execution", ""),
            ("执行确认", "advice.confirm_execution", "confirm_pending_advice_suggestion_execution", ""),
            ("取消执行", "advice.cancel_execution", "cancel_pending_advice_suggestion_execution", ""),
            ("取消运行", "advice.cancel_execution", "cancel_pending_advice_suggestion_execution", ""),
        )

        for prompt, expected_intent, expected_natural_name, expected_command in cases:
            with self.subTest(prompt=prompt):
                result = InnerBrain(self.paths).understand(prompt)

                self.assertEqual(result.intent, expected_intent)
                self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
                self.assertEqual(result.source, "seed_sample")
                self.assertGreaterEqual(result.confidence, 0.78)
                self.assertIsNotNone(result.natural_language_intent)
                self.assertEqual(result.natural_language_intent.name, expected_natural_name)
                if expected_command:
                    self.assertEqual(result.natural_language_intent.command, expected_command)

    def test_explicit_file_tag_intents_use_sample_classifier_slots(self):
        cases = (
            ("给 note.txt 打标签 项目", {"path": "note.txt", "tags": ("项目",)}, '/tag "note.txt" 项目'),
            (
                "把 data/note.txt 标记为 项目 Python",
                {"path": "note.txt", "tags": ("项目", "Python")},
                '/tag "note.txt" 项目 Python',
            ),
        )

        for prompt, expected_slots, expected_command in cases:
            with self.subTest(prompt=prompt):
                result = InnerBrain(self.paths).understand(prompt)

                self.assertEqual(result.intent, "document.tag_path")
                self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
                self.assertEqual(result.source, "seed_sample")
                self.assertGreaterEqual(result.confidence, 0.78)
                self.assertIsNotNone(result.natural_language_intent)
                self.assertEqual(result.natural_language_intent.name, "command")
                self.assertEqual(result.natural_language_intent.command, expected_command)
                self.assertEqual(result.slots["path"], expected_slots["path"])
                self.assertEqual(result.slots["tags"], expected_slots["tags"])

    def test_numbered_object_intents_use_sample_classifier_slots(self):
        cases = (
            ("读取这个资料", "document.read_recent", "read_recent_document", 0),
            ("读取第二份资料", "document.read_numbered_recent", "read_numbered_recent_document", 2),
            ("查看第一份最近文件", "recent_file.read_numbered", "read_numbered_recent_file", 1),
            ("导入第一份最近文件到知识库", "recent_file.import_numbered", "import_numbered_recent_file", 1),
            ("把第2份最近文件导入知识库", "recent_file.import_numbered", "import_numbered_recent_file", 2),
            ("查看第二条结果", "search_result.read_numbered", "read_numbered_search_result", 2),
            ("查看第一条建议", "advice.read_numbered", "read_numbered_advice_suggestion", 1),
            ("执行第二条建议", "advice.execute_numbered", "prepare_numbered_advice_suggestion_execution", 2),
        )

        for prompt, expected_intent, expected_natural_name, expected_index in cases:
            with self.subTest(prompt=prompt):
                result = InnerBrain(self.paths).understand(prompt)

                self.assertEqual(result.intent, expected_intent)
                self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
                self.assertEqual(result.source, "seed_sample")
                self.assertGreaterEqual(result.confidence, 0.78)
                self.assertIsNotNone(result.natural_language_intent)
                self.assertEqual(result.natural_language_intent.name, expected_natural_name)
                if expected_index:
                    self.assertEqual(result.slots["result_index"], expected_index)
                    self.assertEqual(result.natural_language_intent.result_index, expected_index)

    def test_tag_intents_use_sample_classifier_slots(self):
        cases = (
            (
                "给这个资料打标签 项目 Python",
                "document.tag_recent",
                "tag_recent_document",
                {"tags": ("项目", "Python")},
            ),
            (
                "给这个结果打标签 运行环境",
                "document.tag_recent",
                "tag_recent_document",
                {"tags": ("运行环境",)},
            ),
            (
                "给第二份资料打标签 项目 Python",
                "document.tag_numbered_recent",
                "tag_numbered_recent_document",
                {"tags": ("项目", "Python"), "result_index": 2},
            ),
            (
                "给第二条结果打标签 运行环境",
                "search_result.tag_numbered",
                "tag_numbered_search_result",
                {"tags": ("运行环境",), "result_index": 2},
            ),
            (
                "给项目标签资料都打标签 归档",
                "tag_group.preview_tagging",
                "preview_tagged_documents_tagging",
                {"alias": "项目", "tags": ("归档",)},
            ),
            (
                "读取项目标签资料",
                "tag_group.read",
                "read_tagged_documents",
                {"alias": "项目"},
            ),
            (
                "读取第一条标签历史资料",
                "tag_history.read_numbered",
                "read_tagged_documents_history_documents",
                {"result_index": 1},
            ),
        )

        for prompt, expected_intent, expected_natural_name, expected_slots in cases:
            with self.subTest(prompt=prompt):
                result = InnerBrain(self.paths).understand(prompt)

                self.assertEqual(result.intent, expected_intent)
                self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
                self.assertEqual(result.source, "seed_sample")
                self.assertGreaterEqual(result.confidence, 0.78)
                self.assertIsNotNone(result.natural_language_intent)
                self.assertEqual(result.natural_language_intent.name, expected_natural_name)
                for slot_name, expected_value in expected_slots.items():
                    self.assertEqual(result.slots[slot_name], expected_value)
                if "tags" in expected_slots:
                    self.assertEqual(result.natural_language_intent.tags, expected_slots["tags"])
                if "alias" in expected_slots:
                    self.assertEqual(result.natural_language_intent.alias, expected_slots["alias"])
                if "result_index" in expected_slots:
                    self.assertEqual(result.natural_language_intent.result_index, expected_slots["result_index"])

    def test_file_path_intents_use_sample_classifier_slots(self):
        cases = (
            (
                "读取 manual.md",
                "document.read_path",
                "command",
                {"path": "manual.md"},
                '/read "manual.md"',
            ),
            (
                "查看 data/manual.txt",
                "document.read_path",
                "command",
                {"path": "manual.txt"},
                '/read "manual.txt"',
            ),
            (
                '把 "C:/work/outside natural.md" 导入知识库',
                "knowledge.import",
                "command",
                {"source": "C:/work/outside natural.md"},
                '/import "C:/work/outside natural.md"',
            ),
            (
                "导入 E:/docs/manual.pdf 到资料库",
                "knowledge.import",
                "command",
                {"source": "E:/docs/manual.pdf"},
                '/import "E:/docs/manual.pdf"',
            ),
        )

        for prompt, expected_intent, expected_natural_name, expected_slots, expected_command in cases:
            with self.subTest(prompt=prompt):
                result = InnerBrain(self.paths).understand(prompt)

                self.assertEqual(result.intent, expected_intent)
                self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
                self.assertEqual(result.source, "seed_sample")
                self.assertGreaterEqual(result.confidence, 0.78)
                self.assertIsNotNone(result.natural_language_intent)
                self.assertEqual(result.natural_language_intent.name, expected_natural_name)
                self.assertEqual(result.natural_language_intent.command, expected_command)
                for slot_name, expected_value in expected_slots.items():
                    self.assertEqual(result.slots[slot_name], expected_value)

    def test_directory_intents_use_sample_classifier_slots(self):
        cases = (
            (
                "打开D盘",
                "directory.open_drive",
                "open_directory_path",
                {"alias": "D盘", "path": "D:/"},
            ),
            (
                "打开项目目录",
                "directory.open_alias",
                "open_directory_alias",
                {"alias": "项目"},
            ),
            (
                "整理项目目录",
                "directory.organize_alias",
                "organize_directory_alias",
                {"alias": "项目"},
            ),
            (
                "打开这个目录",
                "directory.open_recent",
                "open_recent_directory",
                {},
            ),
            (
                "整理这个目录",
                "directory.organize_recent",
                "organize_recent_directory",
                {},
            ),
        )

        for prompt, expected_intent, expected_natural_name, expected_slots in cases:
            with self.subTest(prompt=prompt):
                result = InnerBrain(self.paths).understand(prompt)

                self.assertEqual(result.intent, expected_intent)
                self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
                self.assertEqual(result.source, "seed_sample")
                self.assertGreaterEqual(result.confidence, 0.78)
                self.assertIsNotNone(result.natural_language_intent)
                self.assertEqual(result.natural_language_intent.name, expected_natural_name)
                for slot_name, expected_value in expected_slots.items():
                    self.assertEqual(result.slots[slot_name], expected_value)
                if "alias" in expected_slots:
                    self.assertEqual(result.natural_language_intent.alias, expected_slots["alias"])
                if "path" in expected_slots:
                    self.assertEqual(result.natural_language_intent.path.as_posix(), expected_slots["path"])

    def test_experience_intents_use_sample_classifier_slots(self):
        cases = (
            (
                "记住这个经验：导入资料后先打标签",
                "experience.record",
                {"experience": "导入资料后先打标签"},
                "/experience 导入资料后先打标签",
            ),
            (
                "搜索经验 导入",
                "experience.search",
                {"query": "导入"},
                "/experience-search 导入",
            ),
            (
                "经验查询 日报",
                "experience.search",
                {"query": "日报"},
                "/experience-search 日报",
            ),
            (
                "我该怎么导入资料",
                "experience.advice",
                {"query": "导入资料"},
                "/experience-advice 导入资料",
            ),
            (
                "导入资料有什么建议",
                "experience.advice",
                {"query": "导入资料"},
                "/experience-advice 导入资料",
            ),
        )

        for prompt, expected_intent, expected_slots, expected_command in cases:
            with self.subTest(prompt=prompt):
                result = InnerBrain(self.paths).understand(prompt)

                self.assertEqual(result.intent, expected_intent)
                self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
                self.assertEqual(result.source, "seed_sample")
                self.assertGreaterEqual(result.confidence, 0.78)
                self.assertIsNotNone(result.natural_language_intent)
                self.assertEqual(result.natural_language_intent.name, "command")
                self.assertEqual(result.natural_language_intent.command, expected_command)
                for slot_name, expected_value in expected_slots.items():
                    self.assertEqual(result.slots[slot_name], expected_value)

    def test_web_search_summary_uses_sample_classifier_slot(self):
        result = InnerBrain(self.paths).understand("联网查一下 Python 版本并总结")

        self.assertEqual(result.intent, "web.search_summarize")
        self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
        self.assertEqual(result.source, "seed_sample")
        self.assertGreaterEqual(result.confidence, 0.78)
        self.assertIsNotNone(result.natural_language_intent)
        self.assertEqual(result.natural_language_intent.name, "command")
        self.assertEqual(result.natural_language_intent.command, "/search-summary Python 版本")
        self.assertEqual(result.slots["query"], "Python 版本")

    def test_web_search_followup_intents_use_sample_classifier_slots(self):
        cases = (
            ("打开第一条联网搜索结果", "web_search.open_numbered", "/search-open 1", {"result_index": 1}),
            ("查看第二条联网来源", "web_search.open_numbered", "/search-open 2", {"result_index": 2}),
            ("比较一下这些联网来源", "web_search.compare_recent", "/search-compare", {}),
            ("保存这个搜索摘要", "web_search.save_summary", "/search-save-summary", {}),
            ("导入这个搜索摘要到知识库", "web_search.import_summary", "/search-import-summary", {}),
        )

        for prompt, expected_intent, expected_command, expected_slots in cases:
            with self.subTest(prompt=prompt):
                result = InnerBrain(self.paths).understand(prompt)

                self.assertEqual(result.intent, expected_intent)
                self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
                self.assertEqual(result.source, "seed_sample")
                self.assertGreaterEqual(result.confidence, 0.78)
                self.assertIsNotNone(result.natural_language_intent)
                self.assertEqual(result.natural_language_intent.name, "command")
                self.assertEqual(result.natural_language_intent.command, expected_command)
                for slot_name, expected_value in expected_slots.items():
                    self.assertEqual(result.slots[slot_name], expected_value)

    def test_seed_variant_maps_to_knowledge_summary_command(self):
        result = InnerBrain(self.paths).understand("麻烦看一下知识库摘要")

        self.assertEqual(result.intent, "knowledge.summary")
        self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
        self.assertEqual(result.source, "seed_sample")
        self.assertGreaterEqual(result.confidence, 0.78)
        self.assertIsNotNone(result.natural_language_intent)
        self.assertEqual(result.natural_language_intent.command, "/kb-summary")

    def test_seed_variant_extracts_desktop_shortcut_item(self):
        result = InnerBrain(self.paths).understand("把桌面比特浏览器快捷方式删除")

        self.assertEqual(result.intent, "desktop.delete_shortcut")
        self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
        self.assertEqual(result.source, "seed_sample")
        self.assertGreaterEqual(result.confidence, 0.78)
        self.assertIsNotNone(result.natural_language_intent)
        self.assertEqual(result.natural_language_intent.name, "delete_desktop_shortcuts")
        self.assertEqual(result.natural_language_intent.items, ("比特浏览器",))

    def test_desktop_shortcut_object_first_variants_use_sample_classifier_slots(self):
        cases = (
            ("把桌面快捷方式比特浏览器删掉", ("比特浏览器",)),
            ("桌面快捷方式比特云手机和比特浏览器删除", ("比特云手机", "比特浏览器")),
        )

        for prompt, expected_items in cases:
            with self.subTest(prompt=prompt):
                result = InnerBrain(self.paths).understand(prompt)

                self.assertEqual(result.intent, "desktop.delete_shortcut")
                self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
                self.assertEqual(result.source, "seed_sample")
                self.assertGreaterEqual(result.confidence, 0.78)
                self.assertIsNotNone(result.natural_language_intent)
                self.assertEqual(result.natural_language_intent.name, "delete_desktop_shortcuts")
                self.assertEqual(result.natural_language_intent.items, expected_items)

    def test_low_confidence_prompt_falls_back_to_llm_policy(self):
        result = InnerBrain(self.paths).understand("火星基地预算需要外部判断")

        self.assertEqual(result.intent, "unknown")
        self.assertEqual(result.policy, InnerBrainPolicy.FALLBACK_TO_LLM)
        self.assertEqual(result.source, "no_match")
        self.assertLess(result.confidence, 0.58)
        self.assertIsNone(result.natural_language_intent)

    def test_runtime_jsonl_samples_extend_seed_samples(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "请打开我的资料库",
                    "intent": "knowledge.status",
                    "slots": {"command": "/kb"},
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        result = InnerBrain(self.paths).understand("请打开我的资料库")

        self.assertEqual(result.intent, "knowledge.status")
        self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
        self.assertEqual(result.source, "runtime_sample")
        self.assertIsNotNone(result.natural_language_intent)
        self.assertEqual(result.natural_language_intent.command, "/kb")

    def test_save_runtime_training_sample_writes_reloadable_jsonl(self):
        prompt = "帮我看看资料库状态"
        result = InnerBrain(self.paths).understand(prompt)

        save_result = save_runtime_training_sample(self.paths, prompt, result)
        reloaded_result = InnerBrain(self.paths).understand(prompt)

        self.assertTrue(save_result.created)
        self.assertFalse(save_result.duplicate)
        self.assertEqual(save_result.relative_path, "data/inner-brain/training/runtime.jsonl")
        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())
        self.assertEqual(saved_sample["text"], prompt)
        self.assertEqual(saved_sample["intent"], "knowledge.status")
        self.assertEqual(saved_sample["slots"], {"command": "/kb"})
        self.assertEqual(saved_sample["missing"], [])
        self.assertEqual(reloaded_result.intent, "knowledge.status")
        self.assertEqual(reloaded_result.source, "runtime_sample")
        self.assertEqual(reloaded_result.policy, InnerBrainPolicy.EXECUTE)

    def test_save_runtime_training_sample_skips_duplicate(self):
        prompt = "帮我看看资料库状态"
        result = InnerBrain(self.paths).understand(prompt)

        first_result = save_runtime_training_sample(self.paths, prompt, result)
        second_result = save_runtime_training_sample(self.paths, prompt, result)

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        lines = sample_file.read_text(encoding="utf-8").splitlines()
        self.assertTrue(first_result.created)
        self.assertFalse(second_result.created)
        self.assertTrue(second_result.duplicate)
        self.assertEqual(len(lines), 1)

    def test_save_runtime_training_sample_rejects_unknown_result(self):
        prompt = "火星基地预算需要外部判断"
        result = InnerBrain(self.paths).understand(prompt)

        with self.assertRaises(ValueError):
            save_runtime_training_sample(self.paths, prompt, result)

        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        self.assertFalse(sample_file.exists())

    def test_save_labeled_runtime_training_sample_writes_unknown_prompt_mapping(self):
        prompt = "可以看看资料库吗"

        save_result = save_labeled_runtime_training_sample(
            self.paths,
            prompt,
            "knowledge.status",
            {"command": "/kb"},
        )
        result = InnerBrain(self.paths).understand(prompt)

        self.assertTrue(save_result.created)
        self.assertEqual(save_result.sample.intent, "knowledge.status")
        self.assertEqual(save_result.sample.slots, {"command": "/kb"})
        self.assertEqual(result.intent, "knowledge.status")
        self.assertEqual(result.source, "runtime_sample")
        self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
        self.assertIsNotNone(result.natural_language_intent)
        self.assertEqual(result.natural_language_intent.command, "/kb")

    def test_save_labeled_runtime_training_sample_preserves_list_slots(self):
        prompt = "随手删掉这个快捷方式"

        save_labeled_runtime_training_sample(
            self.paths,
            prompt,
            "desktop.delete_shortcut",
            {"items": ["比特浏览器"]},
        )
        result = InnerBrain(self.paths).understand(prompt)
        sample_file = self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"
        saved_sample = json.loads(sample_file.read_text(encoding="utf-8").strip())

        self.assertEqual(saved_sample["slots"], {"items": ["比特浏览器"]})
        self.assertEqual(result.intent, "desktop.delete_shortcut")
        self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
        self.assertIsNotNone(result.natural_language_intent)
        self.assertEqual(result.natural_language_intent.items, ("比特浏览器",))

    def test_missing_required_slot_returns_clarify_policy(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "帮我导入这份资料",
                    "intent": "knowledge.import",
                    "slots": {},
                    "missing": ["source"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        result = InnerBrain(self.paths).understand("帮我导入这份资料")

        self.assertEqual(result.intent, "knowledge.import")
        self.assertEqual(result.policy, InnerBrainPolicy.CLARIFY)
        self.assertEqual(result.missing, ("source",))
        self.assertIsNone(result.natural_language_intent)

    def test_describe_inner_brain_result_formats_non_executing_preview(self):
        result = InnerBrain(self.paths).understand("麻烦看一下知识库摘要")

        description = describe_inner_brain_result(result)

        self.assertIn("InnerBrain 预览", description)
        self.assertIn("策略：execute", description)
        self.assertIn("意图：knowledge.summary", description)
        self.assertIn("来源：seed_sample", description)
        self.assertIn("置信度：1.00", description)
        self.assertIn("命令：/kb-summary", description)
        self.assertIn("说明：这里只预览识别结果，不执行命令。", description)

    def test_describe_status_reports_sample_counts_and_thresholds(self):
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        training_dir.mkdir(parents=True)
        (training_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "请打开我的资料库",
                    "intent": "knowledge.status",
                    "slots": {"command": "/kb"},
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        description = InnerBrain(self.paths).describe_status()

        self.assertIn("InnerBrain 状态", description)
        self.assertIn("样本分类器：启用（优先）", description)
        self.assertIn("legacy_fallback：启用（仅迁移期兼容）", description)
        self.assertNotIn("legacy_rule：启用", description)
        self.assertRegex(description, r"seed_sample：\d+ 条")
        self.assertIn("runtime_sample：1 条", description)
        self.assertIn("高置信阈值：0.78", description)
        self.assertIn("中置信阈值：0.58", description)
        self.assertIn("data/inner-brain/training", description)


if __name__ == "__main__":
    unittest.main()
