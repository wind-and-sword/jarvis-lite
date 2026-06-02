import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.inner_brain import (
    HIGH_CONFIDENCE,
    InnerBrain,
    InnerBrainEvaluationCase,
    InnerBrainPolicy,
    describe_inner_brain_evaluation,
    describe_inner_brain_resolved_evaluation,
    describe_inner_brain_result,
    evaluate_inner_brain,
    load_evaluation_cases,
    save_local_evaluation_case,
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

    def test_legacy_high_frequency_aliases_use_seed_samples(self):
        cases = (
            ("早", "assistant.greeting", "greeting", ""),
            ("早安", "assistant.greeting", "greeting", ""),
            ("上午好", "assistant.greeting", "greeting", ""),
            ("下午好", "assistant.greeting", "greeting", ""),
            ("中午好", "assistant.greeting", "greeting", ""),
            ("哈喽", "assistant.greeting", "greeting", ""),
            ("hello", "assistant.greeting", "greeting", ""),
            ("hi", "assistant.greeting", "greeting", ""),
            ("你叫啥", "assistant.identity", "assistant_identity", ""),
            ("你的名字是什么", "assistant.identity", "assistant_identity", ""),
            ("你的名称是什么", "assistant.identity", "assistant_identity", ""),
            ("怎么称呼你", "assistant.identity", "assistant_identity", ""),
            ("会做什么", "assistant.capabilities", "capabilities", ""),
            ("能干什么", "assistant.capabilities", "capabilities", ""),
            ("查看上下文", "context.recent_status", "recent_context_status", ""),
            ("看看上下文", "context.recent_status", "recent_context_status", ""),
            ("你还记得上次什么", "context.recent_status", "recent_context_status", ""),
            ("资料库摘要", "knowledge.summary", "command", "/kb-summary"),
            ("知识库状态", "knowledge.status", "command", "/kb"),
            ("最近文件", "context.recent_files", "recent_files_status", ""),
            ("创建日报", "report.daily", "command", "/daily-report"),
            ("今天日报", "report.daily", "command", "/daily-report"),
            ("生成今天日报", "report.daily", "command", "/daily-report"),
            ("帮我生成日报", "report.daily", "command", "/daily-report"),
            ("有没有更新", "update.status", "command", "/update-status"),
            ("看看更新", "update.status", "command", "/update-status"),
            ("下载更新安装包", "update.download", "command", "/update-download"),
            ("查看经验", "experience.status", "command", "/experiences"),
            ("看看经验", "experience.status", "command", "/experiences"),
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

    def test_sample_classifier_boosts_contained_sample_signature(self):
        result = InnerBrain(self.paths).understand("帮我看一下知识库状态")

        self.assertEqual(result.intent, "knowledge.status")
        self.assertEqual(result.policy, InnerBrainPolicy.EXECUTE)
        self.assertEqual(result.source, "seed_sample")
        self.assertGreaterEqual(result.confidence, HIGH_CONFIDENCE)
        self.assertIsNotNone(result.natural_language_intent)
        self.assertEqual(result.natural_language_intent.command, "/kb")

    def test_inner_brain_evaluation_reports_repeatable_seed_baseline(self):
        report = evaluate_inner_brain(InnerBrain(self.paths))

        self.assertGreaterEqual(report.total_count, 8)
        self.assertEqual(report.failed_count, 0)
        self.assertEqual(report.passed_count, report.total_count)
        description = describe_inner_brain_evaluation(report)
        self.assertIn("InnerBrain 评估", description)
        self.assertIn("评估集：seed_evaluation", description)
        self.assertIn(f"通过：{report.passed_count}/{report.total_count}", description)
        self.assertIn("失败：0", description)
        self.assertIn("帮我看一下知识库状态 -> knowledge.status", description)

    def test_inner_brain_evaluation_loads_local_jsonl_cases(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "custom.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.status",
                    "expected_command": "/kb",
                },
                ensure_ascii=False,
            )
            + "\n"
            + '{"text": ""}\n',
            encoding="utf-8",
        )

        local_cases = load_evaluation_cases(self.paths)
        report = evaluate_inner_brain(InnerBrain(self.paths))
        description = describe_inner_brain_evaluation(report)

        self.assertEqual(len(local_cases), 1)
        self.assertEqual(local_cases[0].source, "local_evaluation")
        self.assertIn("评估集：seed_evaluation+local_evaluation", description)
        self.assertIn("local_evaluation：1 条", description)
        self.assertIn("请看看资料库状态 -> knowledge.status", description)
        self.assertEqual(report.failed_count, 0)

    def test_inner_brain_evaluation_describes_failed_cases_with_training_suggestions(self):
        cases = (
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
            ),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="local_evaluation")
        description = describe_inner_brain_evaluation(report)

        self.assertEqual(report.failed_count, 1)
        self.assertIn("失败修复建议：", description)
        self.assertIn("请看看资料库状态：/inner-brain-teach 请看看资料库状态 => /kb-summary", description)
        self.assertIn("说明：这里只生成显式训练提示，不自动写入 runtime 样本。", description)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_evaluation_can_describe_failed_cases_only(self):
        cases = (
            InnerBrainEvaluationCase("早上好", "assistant.greeting"),
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
            ),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="mixed_evaluation")
        description = describe_inner_brain_evaluation(report, failures_only=True)

        self.assertIn("失败样例：", description)
        self.assertNotIn("PASS 早上好", description)
        self.assertNotIn("早上好 -> assistant.greeting", description)
        self.assertIn("FAIL 请看看资料库状态 -> knowledge.status", description)
        self.assertIn("失败修复建议：", description)
        self.assertIn("请看看资料库状态：/inner-brain-teach 请看看资料库状态 => /kb-summary", description)

    def test_inner_brain_evaluation_can_filter_local_evaluation_source(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "real-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.status",
                    "expected_command": "/kb",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), source_filter="local_evaluation")
        description = describe_inner_brain_evaluation(report)

        self.assertEqual(report.total_count, 1)
        self.assertEqual(report.name, "local_evaluation")
        self.assertIn("评估集：local_evaluation", description)
        self.assertIn("local_evaluation：1 条", description)
        self.assertIn("请看看资料库状态 -> knowledge.status", description)
        self.assertNotIn("seed_evaluation：", description)
        self.assertNotIn("早上好 -> assistant.greeting", description)

    def test_inner_brain_local_evaluation_empty_state_suggests_evaluation_sample_commands(self):
        report = evaluate_inner_brain(InnerBrain(self.paths), source_filter="local_evaluation")
        description = describe_inner_brain_evaluation(report, failures_only=True)

        self.assertEqual(report.total_count, 0)
        self.assertIn("本机评估样本：", description)
        self.assertIn("- 无", description)
        self.assertIn("添加本机评估样本：", description)
        self.assertIn("- /inner-brain-eval-add 文本 => /命令", description)
        self.assertIn("- /inner-brain-eval-label 文本 => intent [slot=value ...]", description)
        self.assertIn("- /inner-brain-eval-add-candidate 编号 => /命令", description)
        self.assertIn("- /inner-brain-eval-label-candidate 编号 => intent [slot=value ...]", description)
        self.assertIn("说明：这些命令只写入本机 evaluation 样本，不自动训练。", description)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_evaluation_can_filter_local_evaluation_file(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "real-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.status",
                    "expected_command": "/kb",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (evaluation_dir / "failed-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.summary",
                    "expected_command": "/kb-summary",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        local_cases = load_evaluation_cases(self.paths)
        report = evaluate_inner_brain(
            InnerBrain(self.paths),
            source_filter="local_evaluation",
            source_file_filter="real-log.jsonl",
        )
        description = describe_inner_brain_evaluation(report)

        self.assertEqual(sorted(case.source_file for case in local_cases), ["failed-log.jsonl", "real-log.jsonl"])
        self.assertEqual(report.total_count, 1)
        self.assertEqual(report.name, "local_evaluation:real-log.jsonl")
        self.assertIn("评估文件：real-log.jsonl", description)
        self.assertIn("请看看资料库状态 -> knowledge.status", description)
        self.assertNotIn("FAIL 请看看资料库状态", description)

    def test_inner_brain_failed_evaluation_groups_local_failures_by_file(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "real-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.status",
                    "expected_command": "/kb",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (evaluation_dir / "failed-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.summary",
                    "expected_command": "/kb-summary",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), source_filter="local_evaluation")
        description = describe_inner_brain_evaluation(report, failures_only=True)

        self.assertIn("失败文件：", description)
        self.assertIn(
            "- failed-log.jsonl：1 条：/inner-brain-eval-local-file-failed failed-log.jsonl；"
            "报告：/inner-brain-eval-local-report failed-log.jsonl",
            description,
        )
        self.assertNotIn("- real-log.jsonl：", description)

    def test_inner_brain_failed_evaluation_sorts_failure_files_by_failed_count(self):
        cases = (
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="aaa-one-failure.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="知识库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="zzz-two-failures.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="查看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="zzz-two-failures.jsonl",
            ),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="local_evaluation")
        description = describe_inner_brain_evaluation(report, failures_only=True)

        larger_file_line = (
            "- zzz-two-failures.jsonl：2 条：/inner-brain-eval-local-file-failed zzz-two-failures.jsonl；"
            "报告：/inner-brain-eval-local-report zzz-two-failures.jsonl"
        )
        smaller_file_line = (
            "- aaa-one-failure.jsonl：1 条：/inner-brain-eval-local-file-failed aaa-one-failure.jsonl；"
            "报告：/inner-brain-eval-local-report aaa-one-failure.jsonl"
        )
        self.assertIn("失败文件：", description)
        self.assertIn(larger_file_line, description)
        self.assertIn(smaller_file_line, description)
        self.assertLess(description.index(larger_file_line), description.index(smaller_file_line))

    def test_inner_brain_failed_evaluation_summarizes_failure_reasons(self):
        cases = (
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="知识库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase("早上好", "assistant.greeting", source="local_evaluation", source_file="runtime.jsonl"),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="local_evaluation")
        description = describe_inner_brain_evaluation(report, failures_only=True)

        expected_reason = "意图期望 knowledge.summary，实际 knowledge.status；命令期望 /kb-summary，实际 /kb"
        self.assertEqual(report.failed_reason_counts, {expected_reason: 2})
        self.assertIn("失败原因汇总：", description)
        self.assertIn(f"- {expected_reason}：2 条", description)
        self.assertIn("  典型样本：请看看资料库状态", description)

    def test_inner_brain_failed_evaluation_summarizes_failure_reason_categories(self):
        cases = (
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="删除桌面快捷方式",
                expected_intent="desktop.delete_shortcut",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase("早上好", "assistant.greeting", source="local_evaluation", source_file="runtime.jsonl"),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="local_evaluation")
        description = describe_inner_brain_evaluation(report, failures_only=True)

        self.assertEqual(
            report.failed_reason_category_counts,
            {
                "意图不匹配": 1,
                "命令不匹配": 1,
                "策略不匹配": 1,
            },
        )
        self.assertIn("失败类型汇总：", description)
        self.assertIn("- 命令不匹配：1 条", description)
        self.assertIn("- 意图不匹配：1 条", description)
        self.assertIn("- 策略不匹配：1 条", description)
        self.assertIn("  典型样本：请看看资料库状态", description)
        self.assertIn("  典型样本：删除桌面快捷方式", description)

    def test_inner_brain_failed_evaluation_summarizes_failed_expected_intents(self):
        cases = (
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="知识库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="删除桌面快捷方式",
                expected_intent="desktop.delete_shortcut",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase("早上好", "assistant.greeting", source="local_evaluation", source_file="runtime.jsonl"),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="local_evaluation")
        description = describe_inner_brain_evaluation(report, failures_only=True)

        self.assertEqual(
            report.failed_expected_intent_counts,
            {
                "knowledge.summary": 2,
                "desktop.delete_shortcut": 1,
            },
        )
        self.assertIn("失败期望意图汇总：", description)
        self.assertIn("- knowledge.summary：2 条", description)
        self.assertIn("- desktop.delete_shortcut：1 条", description)
        self.assertIn("  典型样本：请看看资料库状态", description)
        self.assertIn("  典型样本：删除桌面快捷方式", description)

    def test_inner_brain_failed_evaluation_summarizes_failed_intent_confusions(self):
        cases = (
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="知识库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="删除桌面快捷方式",
                expected_intent="desktop.delete_shortcut",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase("早上好", "assistant.greeting", source="local_evaluation", source_file="runtime.jsonl"),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="local_evaluation")
        description = describe_inner_brain_evaluation(report, failures_only=True)

        self.assertEqual(
            report.failed_intent_confusion_counts,
            {
                "knowledge.summary -> knowledge.status": 2,
            },
        )
        self.assertIn("失败意图混淆汇总：", description)
        self.assertIn("- knowledge.summary -> knowledge.status：2 条", description)
        self.assertIn("  典型样本：请看看资料库状态", description)
        self.assertNotIn("- desktop.delete_shortcut -> desktop.delete_shortcut：", description)

    def test_inner_brain_failed_evaluation_summarizes_failed_file_intent_confusions(self):
        cases = (
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="知识库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="查看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="failed-log.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="删除桌面快捷方式",
                expected_intent="desktop.delete_shortcut",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="seed_evaluation",
            ),
            InnerBrainEvaluationCase("早上好", "assistant.greeting", source="local_evaluation", source_file="runtime.jsonl"),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="local_evaluation")
        description = describe_inner_brain_evaluation(report, failures_only=True)

        self.assertEqual(
            report.failed_source_file_intent_confusion_counts,
            {
                ("runtime.jsonl", "knowledge.summary -> knowledge.status"): 2,
                ("failed-log.jsonl", "knowledge.summary -> knowledge.status"): 1,
            },
        )
        self.assertIn("失败文件意图混淆汇总：", description)
        self.assertIn("- runtime.jsonl：knowledge.summary -> knowledge.status：2 条", description)
        self.assertIn("- failed-log.jsonl：knowledge.summary -> knowledge.status：1 条", description)
        self.assertIn("  典型样本：请看看资料库状态", description)
        self.assertNotIn("- runtime.jsonl：desktop.delete_shortcut -> desktop.delete_shortcut：", description)

    def test_inner_brain_failed_evaluation_groups_fix_suggestions_by_intent_confusion(self):
        cases = (
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="知识库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="删除桌面快捷方式",
                expected_intent="desktop.delete_shortcut",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase("早上好", "assistant.greeting", source="local_evaluation", source_file="runtime.jsonl"),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="local_evaluation")
        description = describe_inner_brain_evaluation(report, failures_only=True)

        self.assertIn("失败意图混淆修复建议：", description)
        self.assertIn("- knowledge.summary -> knowledge.status：2 条", description)
        self.assertIn("  - 请看看资料库状态：/inner-brain-teach 请看看资料库状态 => /kb-summary", description)
        self.assertIn("  - 知识库状态：/inner-brain-teach 知识库状态 => /kb-summary", description)
        self.assertNotIn("- desktop.delete_shortcut -> desktop.delete_shortcut：", description)
        self.assertIn("失败修复建议：", description)
        self.assertIn("删除桌面快捷方式：/inner-brain-label 删除桌面快捷方式 => desktop.delete_shortcut", description)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_failed_evaluation_groups_fix_suggestions_by_file_intent_confusion(self):
        cases = (
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="知识库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="查看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="failed-log.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="seed_evaluation",
            ),
            InnerBrainEvaluationCase(
                text="删除桌面快捷方式",
                expected_intent="desktop.delete_shortcut",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase("早上好", "assistant.greeting", source="local_evaluation", source_file="runtime.jsonl"),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="local_evaluation")
        description = describe_inner_brain_evaluation(report, failures_only=True)

        self.assertIn("失败文件意图混淆修复建议：", description)
        self.assertIn("- runtime.jsonl：knowledge.summary -> knowledge.status：2 条", description)
        self.assertIn("  - 请看看资料库状态：/inner-brain-teach 请看看资料库状态 => /kb-summary", description)
        self.assertIn("  - 知识库状态：/inner-brain-teach 知识库状态 => /kb-summary", description)
        self.assertIn("- failed-log.jsonl：knowledge.summary -> knowledge.status：1 条", description)
        self.assertIn("  - 查看资料库状态：/inner-brain-teach 查看资料库状态 => /kb-summary", description)
        self.assertNotIn("- seed_evaluation：knowledge.summary -> knowledge.status：", description)
        self.assertNotIn("- runtime.jsonl：desktop.delete_shortcut -> desktop.delete_shortcut：", description)
        filtered_report = evaluate_inner_brain(
            InnerBrain(self.paths),
            cases=cases,
            name="local_evaluation:runtime.jsonl",
            source_file_filter="runtime.jsonl",
        )
        filtered_description = describe_inner_brain_evaluation(filtered_report, failures_only=True)
        self.assertNotIn("失败文件意图混淆修复建议：", filtered_description)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_resolved_evaluation_lists_only_passed_local_cases(self):
        cases = (
            InnerBrainEvaluationCase(
                text="早上好",
                expected_intent="assistant.greeting",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="local_evaluation")
        description = describe_inner_brain_resolved_evaluation(report)

        self.assertIn("已处理样例：", description)
        self.assertIn("PASS 早上好 -> assistant.greeting", description)
        self.assertNotIn("FAIL 请看看资料库状态", description)
        self.assertNotIn("失败修复建议：", description)
        self.assertIn("说明：这里只展示当前已通过的本机 evaluation 样本，不自动写入 runtime 样本。", description)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_inner_brain_resolved_evaluation_reports_empty_passed_list(self):
        cases = (
            InnerBrainEvaluationCase(
                text="请看看资料库状态",
                expected_intent="knowledge.summary",
                expected_command="/kb-summary",
                source="local_evaluation",
                source_file="runtime.jsonl",
            ),
        )

        report = evaluate_inner_brain(InnerBrain(self.paths), cases=cases, name="local_evaluation")
        description = describe_inner_brain_resolved_evaluation(report)

        self.assertIn("已处理样例：", description)
        self.assertIn("- 无", description)
        self.assertNotIn("FAIL 请看看资料库状态", description)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_export_inner_brain_evaluation_report_writes_failed_markdown_without_training(self):
        evaluation_dir = self.paths.data_dir / "inner-brain" / "evaluation"
        evaluation_dir.mkdir(parents=True)
        (evaluation_dir / "failed-log.jsonl").write_text(
            json.dumps(
                {
                    "text": "请看看资料库状态",
                    "expected_intent": "knowledge.summary",
                    "expected_command": "/kb-summary",
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        report = evaluate_inner_brain(InnerBrain(self.paths), source_filter="local_evaluation")
        from jarvis_lite import inner_brain as inner_brain_module

        export_report = getattr(inner_brain_module, "export_inner_brain_evaluation_report", None)

        self.assertIsNotNone(export_report)
        save_result = export_report(self.paths, report)
        content = save_result.path.read_text(encoding="utf-8")
        self.assertEqual(save_result.relative_path, "word/inner-brain-evaluation-report.md")
        self.assertEqual(save_result.failed_count, 1)
        self.assertIn("# InnerBrain 本机评估失败报告", content)
        self.assertIn("> 执行者：Codex", content)
        self.assertIn("失败文件：", content)
        self.assertIn("- failed-log.jsonl：1 条", content)
        self.assertIn("失败类型汇总：", content)
        self.assertIn("- 命令不匹配：1 条", content)
        self.assertIn("- 意图不匹配：1 条", content)
        self.assertIn("失败期望意图汇总：", content)
        self.assertIn("- knowledge.summary：1 条", content)
        self.assertIn("失败意图混淆汇总：", content)
        self.assertIn("- knowledge.summary -> knowledge.status：1 条", content)
        self.assertIn("失败文件意图混淆汇总：", content)
        self.assertIn("- failed-log.jsonl：knowledge.summary -> knowledge.status：1 条", content)
        self.assertIn("失败意图混淆修复建议：", content)
        self.assertIn("- knowledge.summary -> knowledge.status：1 条", content)
        self.assertIn("  - 请看看资料库状态：/inner-brain-teach 请看看资料库状态 => /kb-summary", content)
        self.assertIn("失败文件意图混淆修复建议：", content)
        self.assertIn("- failed-log.jsonl：knowledge.summary -> knowledge.status：1 条", content)
        self.assertIn("  - 请看看资料库状态：/inner-brain-teach 请看看资料库状态 => /kb-summary", content)
        self.assertIn("失败原因汇总：", content)
        self.assertIn("意图期望 knowledge.summary，实际 knowledge.status；命令期望 /kb-summary，实际 /kb：1 条", content)
        self.assertIn("FAIL 请看看资料库状态 -> knowledge.status", content)
        self.assertIn("失败修复建议：", content)
        self.assertIn("说明：报告只读导出，不自动训练。", content)
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

    def test_save_local_evaluation_case_writes_reloadable_jsonl_without_training(self):
        case = InnerBrainEvaluationCase(
            "请看看资料库状态",
            "knowledge.status",
            expected_command="/kb",
        )

        first_result = save_local_evaluation_case(self.paths, case)
        second_result = save_local_evaluation_case(self.paths, case)

        self.assertTrue(first_result.created)
        self.assertFalse(first_result.duplicate)
        self.assertFalse(second_result.created)
        self.assertTrue(second_result.duplicate)
        self.assertEqual(first_result.relative_path, "data/inner-brain/evaluation/runtime.jsonl")
        case_file = self.paths.data_dir / "inner-brain" / "evaluation" / "runtime.jsonl"
        lines = case_file.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        payload = json.loads(lines[0])
        self.assertEqual(payload["text"], "请看看资料库状态")
        self.assertEqual(payload["expected_intent"], "knowledge.status")
        self.assertEqual(payload["expected_command"], "/kb")
        local_cases = load_evaluation_cases(self.paths)
        self.assertEqual(len(local_cases), 1)
        self.assertEqual(local_cases[0].expected_command, "/kb")
        self.assertFalse((self.paths.data_dir / "inner-brain" / "training" / "runtime.jsonl").exists())

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
            ("请帮我导入第二份最近文件到资料库", "recent_file.import_numbered", "import_numbered_recent_file", 2),
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
