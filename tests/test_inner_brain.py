import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.inner_brain import InnerBrain, InnerBrainPolicy, describe_inner_brain_result


class InnerBrainTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.paths = build_project_paths(Path(self.temp_dir.name) / "jarvis-lite")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_legacy_rule_returns_structured_execute_result(self):
        result = InnerBrain(self.paths).understand("早上好")

        self.assertEqual(result.intent, "assistant.greeting")
        self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
        self.assertEqual(result.source, "legacy_rule")
        self.assertEqual(result.confidence, 1.0)
        self.assertEqual(result.missing, ())
        self.assertIsNotNone(result.natural_language_intent)
        self.assertEqual(result.natural_language_intent.name, "greeting")

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
        self.assertIn("legacy_rule：启用", description)
        self.assertIn("seed_sample：9 条", description)
        self.assertIn("runtime_sample：1 条", description)
        self.assertIn("高置信阈值：0.78", description)
        self.assertIn("中置信阈值：0.58", description)
        self.assertIn("data/inner-brain/training", description)


if __name__ == "__main__":
    unittest.main()
