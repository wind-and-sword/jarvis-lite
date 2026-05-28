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

    def test_unmigrated_slot_heavy_rule_is_marked_as_legacy_fallback(self):
        result = InnerBrain(self.paths).understand("给 note.txt 打标签 项目")

        self.assertEqual(result.intent, "command")
        self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
        self.assertEqual(result.source, "legacy_fallback")
        self.assertIsNotNone(result.natural_language_intent)
        self.assertEqual(result.natural_language_intent.command, "/tag note.txt 项目")

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
