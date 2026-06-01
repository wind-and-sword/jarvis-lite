from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Mapping

from .config import ProjectPaths
from .intent import NaturalLanguageIntent, parse_natural_language_intent


HIGH_CONFIDENCE = 0.78
MEDIUM_CONFIDENCE = 0.58


class InnerBrainPolicy(str, Enum):
    """内脑对当前输入的下一步处理策略。"""

    EXECUTE = "execute"
    CLARIFY = "clarify"
    FALLBACK_TO_LLM = "fallback_to_llm"


@dataclass(frozen=True)
class InnerBrainTrainingSample:
    """一条可标注、可扩展的本地自然语言训练样本。"""

    text: str
    intent: str
    slots: Mapping[str, Any] = field(default_factory=dict)
    missing: tuple[str, ...] = ()
    source: str = "seed_sample"


@dataclass(frozen=True)
class InnerBrainTrainingSaveResult:
    """运行态样本写入结果，供 Agent 返回可审计反馈。"""

    sample: InnerBrainTrainingSample
    path: Path
    relative_path: str
    created: bool
    duplicate: bool


@dataclass(frozen=True)
class InnerBrainResult:
    """InnerBrain 对一次用户输入的结构化理解结果。"""

    intent: str
    slots: Mapping[str, Any]
    confidence: float
    missing: tuple[str, ...]
    source: str
    reason: str
    policy: InnerBrainPolicy
    natural_language_intent: NaturalLanguageIntent | None = None


@dataclass(frozen=True)
class InnerBrainEvaluationCase:
    """一条固定评估样本，用于衡量内脑分类器质量。"""

    text: str
    expected_intent: str
    expected_policy: InnerBrainPolicy = InnerBrainPolicy.EXECUTE
    expected_command: str | None = None
    source: str = "seed_evaluation"


@dataclass(frozen=True)
class InnerBrainEvaluationSaveResult:
    """本机评估样本写入结果，供 Agent 返回可审计反馈。"""

    case: InnerBrainEvaluationCase
    path: Path
    relative_path: str
    created: bool
    duplicate: bool


@dataclass(frozen=True)
class InnerBrainEvaluationCaseResult:
    """单条评估样本的实际识别结果。"""

    case: InnerBrainEvaluationCase
    result: InnerBrainResult
    passed: bool
    reason: str


@dataclass(frozen=True)
class InnerBrainEvaluationReport:
    """固定评估集的汇总结果。"""

    name: str
    case_results: tuple[InnerBrainEvaluationCaseResult, ...]

    @property
    def total_count(self) -> int:
        return len(self.case_results)

    @property
    def passed_count(self) -> int:
        return sum(1 for result in self.case_results if result.passed)

    @property
    def failed_count(self) -> int:
        return self.total_count - self.passed_count

    @property
    def accuracy(self) -> float:
        if self.total_count == 0:
            return 0.0
        return self.passed_count / self.total_count

    @property
    def source_counts(self) -> Mapping[str, int]:
        counts: dict[str, int] = {}
        for case_result in self.case_results:
            counts[case_result.case.source] = counts.get(case_result.case.source, 0) + 1
        return counts

    @property
    def failed_case_results(self) -> tuple[InnerBrainEvaluationCaseResult, ...]:
        return tuple(case_result for case_result in self.case_results if not case_result.passed)


class InnerBrain:
    """本地轻量内脑，负责把自然语言转成可审计的结构化意图。"""

    def __init__(self, paths: ProjectPaths | None = None, samples: tuple[InnerBrainTrainingSample, ...] | None = None):
        self.paths = paths
        self.samples = samples or (*seed_training_samples(), *load_training_samples(paths))

    def understand(self, text: str) -> InnerBrainResult:
        prompt = text.strip()
        if not prompt:
            return _no_match("输入为空")

        sample, confidence = self._best_sample(prompt)
        if sample is not None and confidence >= HIGH_CONFIDENCE:
            return self._sample_result(prompt, sample, confidence)

        legacy_intent = parse_natural_language_intent(prompt)
        if legacy_intent is not None:
            return self._legacy_fallback_result(legacy_intent)

        if sample is not None and confidence >= MEDIUM_CONFIDENCE:
            return self._sample_result(prompt, sample, confidence)

        reason = "没有命中样本分类器或 legacy fallback"
        if sample is not None:
            reason = f"最高相似样本 {sample.intent} 置信度 {confidence:.2f} 低于阈值"
        return _no_match(reason, confidence)

    def describe_status(self) -> str:
        source_counts: dict[str, int] = {}
        for sample in self.samples:
            source_counts[sample.source] = source_counts.get(sample.source, 0) + 1
        training_dir = self._training_dir_label()
        return "\n".join(
            [
                "InnerBrain 状态：",
                "- 样本分类器：启用（优先）",
                "- legacy_fallback：启用（仅迁移期兼容）",
                f"- seed_sample：{source_counts.get('seed_sample', 0)} 条",
                f"- runtime_sample：{source_counts.get('runtime_sample', 0)} 条",
                f"- 高置信阈值：{HIGH_CONFIDENCE:.2f}",
                f"- 中置信阈值：{MEDIUM_CONFIDENCE:.2f}",
                f"- 训练目录：{training_dir}",
            ]
        )

    def _training_dir_label(self) -> str:
        if self.paths is None:
            return "未绑定项目路径"
        training_dir = self.paths.data_dir / "inner-brain" / "training"
        try:
            return training_dir.relative_to(self.paths.root).as_posix()
        except ValueError:
            return training_dir.as_posix()

    def _legacy_fallback_result(self, intent: NaturalLanguageIntent) -> InnerBrainResult:
        slots = _slots_from_natural_language_intent(intent)
        return InnerBrainResult(
            intent=_legacy_intent_label(intent),
            slots=slots,
            confidence=1.0,
            missing=(),
            source="legacy_fallback",
            reason=f"迁移期兼容 fallback 命中：{intent.name}",
            policy=InnerBrainPolicy.EXECUTE,
            natural_language_intent=intent,
        )

    def _best_sample(self, prompt: str) -> tuple[InnerBrainTrainingSample | None, float]:
        best_sample: InnerBrainTrainingSample | None = None
        best_score = 0.0
        for sample in self.samples:
            score = _sample_similarity(prompt, sample)
            if score > best_score:
                best_sample = sample
                best_score = score
        return best_sample, best_score

    def _sample_result(self, prompt: str, sample: InnerBrainTrainingSample, confidence: float) -> InnerBrainResult:
        slots = _sample_slots(prompt, sample)
        missing = sample.missing
        natural_language_intent = _sample_to_natural_language_intent(prompt, sample, slots)
        if sample.intent == "desktop.delete_shortcut" and natural_language_intent is None:
            missing = ("items",)

        policy = InnerBrainPolicy.EXECUTE
        if missing or confidence < HIGH_CONFIDENCE:
            policy = InnerBrainPolicy.CLARIFY
            natural_language_intent = None

        return InnerBrainResult(
            intent=sample.intent,
            slots=slots,
            confidence=confidence,
            missing=missing,
            source=sample.source,
            reason=f"最相似样本：{sample.text}",
            policy=policy,
            natural_language_intent=natural_language_intent,
        )


def seed_training_samples() -> tuple[InnerBrainTrainingSample, ...]:
    """内置第一批高频任务样本，运行态 JSONL 后续可继续扩展。"""

    return (
        InnerBrainTrainingSample("早上好", "assistant.greeting", {}),
        InnerBrainTrainingSample("早", "assistant.greeting", {}),
        InnerBrainTrainingSample("早安", "assistant.greeting", {}),
        InnerBrainTrainingSample("上午好", "assistant.greeting", {}),
        InnerBrainTrainingSample("中午好", "assistant.greeting", {}),
        InnerBrainTrainingSample("下午好", "assistant.greeting", {}),
        InnerBrainTrainingSample("你好", "assistant.greeting", {}),
        InnerBrainTrainingSample("您好", "assistant.greeting", {}),
        InnerBrainTrainingSample("晚上好", "assistant.greeting", {}),
        InnerBrainTrainingSample("哈喽", "assistant.greeting", {}),
        InnerBrainTrainingSample("hello", "assistant.greeting", {}),
        InnerBrainTrainingSample("hi", "assistant.greeting", {}),
        InnerBrainTrainingSample("你叫什么名字", "assistant.identity", {}),
        InnerBrainTrainingSample("你叫啥", "assistant.identity", {}),
        InnerBrainTrainingSample("你的名字是什么", "assistant.identity", {}),
        InnerBrainTrainingSample("你的名称是什么", "assistant.identity", {}),
        InnerBrainTrainingSample("你是谁", "assistant.identity", {}),
        InnerBrainTrainingSample("怎么称呼你", "assistant.identity", {}),
        InnerBrainTrainingSample("你能做什么", "assistant.capabilities", {}),
        InnerBrainTrainingSample("你现在能做什么事", "assistant.capabilities", {}),
        InnerBrainTrainingSample("你可以做什么", "assistant.capabilities", {}),
        InnerBrainTrainingSample("会做什么", "assistant.capabilities", {}),
        InnerBrainTrainingSample("能干什么", "assistant.capabilities", {}),
        InnerBrainTrainingSample("有什么功能", "assistant.capabilities", {}),
        InnerBrainTrainingSample("能帮我做什么", "assistant.capabilities", {}),
        InnerBrainTrainingSample("查看最近上下文", "context.recent_status", {}),
        InnerBrainTrainingSample("查看上下文", "context.recent_status", {}),
        InnerBrainTrainingSample("看看上下文", "context.recent_status", {}),
        InnerBrainTrainingSample("最近上下文状态", "context.recent_status", {}),
        InnerBrainTrainingSample("你还记得刚才什么", "context.recent_status", {}),
        InnerBrainTrainingSample("你还记得上次什么", "context.recent_status", {}),
        InnerBrainTrainingSample("查看最近文件", "context.recent_files", {}),
        InnerBrainTrainingSample("最近文件", "context.recent_files", {}),
        InnerBrainTrainingSample("最近文件列表", "context.recent_files", {}),
        InnerBrainTrainingSample("查看系统最近文件", "context.recent_files", {}),
        InnerBrainTrainingSample("读取这个资料", "document.read_recent", {}),
        InnerBrainTrainingSample("查看这份资料", "document.read_recent", {}),
        InnerBrainTrainingSample("看看当前文档", "document.read_recent", {}),
        InnerBrainTrainingSample("读取第{index}份资料", "document.read_numbered_recent", {}),
        InnerBrainTrainingSample("查看第{index}份资料", "document.read_numbered_recent", {}),
        InnerBrainTrainingSample("查看第{index}份最近文件", "recent_file.read_numbered", {}),
        InnerBrainTrainingSample("读取第{index}份最近文件", "recent_file.read_numbered", {}),
        InnerBrainTrainingSample("导入第{index}份最近文件到知识库", "recent_file.import_numbered", {}),
        InnerBrainTrainingSample("把第{index}份最近文件导入知识库", "recent_file.import_numbered", {}),
        InnerBrainTrainingSample("查看第{index}条结果", "search_result.read_numbered", {}),
        InnerBrainTrainingSample("读取第{index}条结果", "search_result.read_numbered", {}),
        InnerBrainTrainingSample("查看第{index}条建议", "advice.read_numbered", {}),
        InnerBrainTrainingSample("读取第{index}条建议", "advice.read_numbered", {}),
        InnerBrainTrainingSample("执行第{index}条建议", "advice.execute_numbered", {}),
        InnerBrainTrainingSample("运行第{index}条建议", "advice.execute_numbered", {}),
        InnerBrainTrainingSample("读取{path}", "document.read_path", {}),
        InnerBrainTrainingSample("查看{path}", "document.read_path", {}),
        InnerBrainTrainingSample("导入{source}到知识库", "knowledge.import", {}),
        InnerBrainTrainingSample("把{source}导入知识库", "knowledge.import", {}),
        InnerBrainTrainingSample("给这个资料打标签{tags}", "document.tag_recent", {}),
        InnerBrainTrainingSample("给这个结果打标签{tags}", "document.tag_recent", {}),
        InnerBrainTrainingSample("给{path}打标签{tags}", "document.tag_path", {}),
        InnerBrainTrainingSample("把{path}标记为{tags}", "document.tag_path", {}),
        InnerBrainTrainingSample("给第{index}份资料打标签{tags}", "document.tag_numbered_recent", {}),
        InnerBrainTrainingSample("给第{index}条结果打标签{tags}", "search_result.tag_numbered", {}),
        InnerBrainTrainingSample("给{tag}标签资料都打标签{tags}", "tag_group.preview_tagging", {}),
        InnerBrainTrainingSample("读取{tag}标签资料", "tag_group.read", {}),
        InnerBrainTrainingSample("查看{tag}标签资料", "tag_group.read", {}),
        InnerBrainTrainingSample("读取第{index}条标签历史资料", "tag_history.read_numbered", {}),
        InnerBrainTrainingSample("查看第{index}条批量标签历史影响资料", "tag_history.read_numbered", {}),
        InnerBrainTrainingSample("查看批量标签历史", "tag.history", {"command": "/tag-history"}),
        InnerBrainTrainingSample("批量标签历史", "tag.history", {"command": "/tag-history"}),
        InnerBrainTrainingSample("总结知识库", "knowledge.summary", {"command": "/kb-summary"}),
        InnerBrainTrainingSample("总结资料库", "knowledge.summary", {"command": "/kb-summary"}),
        InnerBrainTrainingSample("麻烦看一下知识库摘要", "knowledge.summary", {"command": "/kb-summary"}),
        InnerBrainTrainingSample("知识库摘要", "knowledge.summary", {"command": "/kb-summary"}),
        InnerBrainTrainingSample("资料库摘要", "knowledge.summary", {"command": "/kb-summary"}),
        InnerBrainTrainingSample("查看知识库", "knowledge.status", {"command": "/kb"}),
        InnerBrainTrainingSample("看看知识库", "knowledge.status", {"command": "/kb"}),
        InnerBrainTrainingSample("知识库状态", "knowledge.status", {"command": "/kb"}),
        InnerBrainTrainingSample("我的知识库", "knowledge.status", {"command": "/kb"}),
        InnerBrainTrainingSample("请看看资料库状态", "knowledge.status", {"command": "/kb"}),
        InnerBrainTrainingSample("查看常用目录", "directory.list", {"command": "/dirs"}),
        InnerBrainTrainingSample("常用目录", "directory.list", {"command": "/dirs"}),
        InnerBrainTrainingSample("目录列表", "directory.list", {"command": "/dirs"}),
        InnerBrainTrainingSample("打开{drive}盘", "directory.open_drive", {}),
        InnerBrainTrainingSample("打开{alias}目录", "directory.open_alias", {}),
        InnerBrainTrainingSample("整理{alias}目录", "directory.organize_alias", {}),
        InnerBrainTrainingSample("打开这个目录", "directory.open_recent", {}),
        InnerBrainTrainingSample("整理这个目录", "directory.organize_recent", {}),
        InnerBrainTrainingSample("生成日报", "report.daily", {"command": "/daily-report"}),
        InnerBrainTrainingSample("写日报", "report.daily", {"command": "/daily-report"}),
        InnerBrainTrainingSample("创建日报", "report.daily", {"command": "/daily-report"}),
        InnerBrainTrainingSample("今天日报", "report.daily", {"command": "/daily-report"}),
        InnerBrainTrainingSample("生成今天日报", "report.daily", {"command": "/daily-report"}),
        InnerBrainTrainingSample("帮我生成日报", "report.daily", {"command": "/daily-report"}),
        InnerBrainTrainingSample("检查更新", "update.status", {"command": "/update-status"}),
        InnerBrainTrainingSample("查看更新", "update.status", {"command": "/update-status"}),
        InnerBrainTrainingSample("有没有更新", "update.status", {"command": "/update-status"}),
        InnerBrainTrainingSample("看看更新", "update.status", {"command": "/update-status"}),
        InnerBrainTrainingSample("下载更新", "update.download", {"command": "/update-download"}),
        InnerBrainTrainingSample("下载新版本", "update.download", {"command": "/update-download"}),
        InnerBrainTrainingSample("下载最新版", "update.download", {"command": "/update-download"}),
        InnerBrainTrainingSample("下载更新安装包", "update.download", {"command": "/update-download"}),
        InnerBrainTrainingSample("查看经验记忆", "experience.status", {"command": "/experiences"}),
        InnerBrainTrainingSample("看看经验记忆", "experience.status", {"command": "/experiences"}),
        InnerBrainTrainingSample("查看经验", "experience.status", {"command": "/experiences"}),
        InnerBrainTrainingSample("看看经验", "experience.status", {"command": "/experiences"}),
        InnerBrainTrainingSample("记录经验{experience}", "experience.record", {}),
        InnerBrainTrainingSample("记住这个经验{experience}", "experience.record", {}),
        InnerBrainTrainingSample("搜索经验{query}", "experience.search", {}),
        InnerBrainTrainingSample("经验查询{query}", "experience.search", {}),
        InnerBrainTrainingSample("我该怎么{query}", "experience.advice", {}),
        InnerBrainTrainingSample("{query}有什么建议", "experience.advice", {}),
        InnerBrainTrainingSample("确认执行", "advice.confirm_execution", {}),
        InnerBrainTrainingSample("确认运行", "advice.confirm_execution", {}),
        InnerBrainTrainingSample("取消执行", "advice.cancel_execution", {}),
        InnerBrainTrainingSample("取消运行", "advice.cancel_execution", {}),
        InnerBrainTrainingSample("不执行了", "advice.cancel_execution", {}),
        InnerBrainTrainingSample("开启外脑", "llm.enable", {"command": "/llm-enable"}),
        InnerBrainTrainingSample("连接外脑", "llm.enable", {"command": "/llm-enable"}),
        InnerBrainTrainingSample("生成外脑配置", "llm.config_init", {"command": "/llm-config-init"}),
        InnerBrainTrainingSample("创建外脑配置文件", "llm.config_init", {"command": "/llm-config-init"}),
        InnerBrainTrainingSample("检查外脑配置", "llm.config_check", {"command": "/llm-config-check"}),
        InnerBrainTrainingSample("看看外脑配置有没有问题", "llm.config_check", {"command": "/llm-config-check"}),
        InnerBrainTrainingSample("设置外脑配置", "llm.config_set", {"command": "/llm-config-set"}),
        InnerBrainTrainingSample("修改外脑配置", "llm.config_set", {"command": "/llm-config-set"}),
        InnerBrainTrainingSample("测试外脑连接", "llm.smoke", {"command": "/llm-smoke"}),
        InnerBrainTrainingSample("检查外脑连接", "llm.smoke", {"command": "/llm-smoke"}),
        InnerBrainTrainingSample("生成联网搜索配置", "web.search.config_init", {"command": "/search-config-init"}),
        InnerBrainTrainingSample("创建搜索配置文件", "web.search.config_init", {"command": "/search-config-init"}),
        InnerBrainTrainingSample("检查联网搜索配置", "web.search.config_check", {"command": "/search-config-check"}),
        InnerBrainTrainingSample("看看搜索配置有没有问题", "web.search.config_check", {"command": "/search-config-check"}),
        InnerBrainTrainingSample("设置联网搜索配置", "web.search.config_set", {"command": "/search-config-set"}),
        InnerBrainTrainingSample("修改搜索配置", "web.search.config_set", {"command": "/search-config-set"}),
        InnerBrainTrainingSample("测试联网搜索连接", "web.search.smoke", {"command": "/search-smoke"}),
        InnerBrainTrainingSample("检查搜索连接", "web.search.smoke", {"command": "/search-smoke"}),
        InnerBrainTrainingSample("联网查一下{query}并总结", "web.search_summarize", {}),
        InnerBrainTrainingSample("搜索一下{query}并总结", "web.search_summarize", {}),
        InnerBrainTrainingSample("联网查一下{query}", "web.search", {}),
        InnerBrainTrainingSample("搜索一下{query}", "web.search", {}),
        InnerBrainTrainingSample("帮我看看网上{query}", "web.search", {}),
        InnerBrainTrainingSample("打开第{index}条联网搜索结果", "web_search.open_numbered", {}),
        InnerBrainTrainingSample("查看第{index}条联网来源", "web_search.open_numbered", {}),
        InnerBrainTrainingSample("比较这些联网来源", "web_search.compare_recent", {"command": "/search-compare"}),
        InnerBrainTrainingSample("保存这个搜索摘要", "web_search.save_summary", {"command": "/search-save-summary"}),
        InnerBrainTrainingSample("导入这个搜索摘要到知识库", "web_search.import_summary", {"command": "/search-import-summary"}),
        InnerBrainTrainingSample("把桌面{item}快捷方式删除", "desktop.delete_shortcut", {}),
        InnerBrainTrainingSample("删除桌面{item}快捷方式", "desktop.delete_shortcut", {}),
        InnerBrainTrainingSample("桌面快捷方式{item}删除", "desktop.delete_shortcut", {}),
    )


def describe_inner_brain_result(result: InnerBrainResult) -> str:
    """格式化内脑识别结果，供预览命令使用，不能触发执行。"""

    lines = [
        "InnerBrain 预览：",
        f"- 策略：{result.policy.value}",
        f"- 意图：{result.intent}",
        f"- 来源：{result.source}",
        f"- 置信度：{result.confidence:.2f}",
    ]
    if result.missing:
        lines.append(f"- 缺失：{'、'.join(result.missing)}")
    slot_lines = _inner_brain_result_slot_lines(result)
    if slot_lines:
        lines.extend(slot_lines)
    lines.append(f"- 原因：{result.reason}")
    lines.append("说明：这里只预览识别结果，不执行命令。")
    return "\n".join(lines)


def seed_evaluation_cases() -> tuple[InnerBrainEvaluationCase, ...]:
    """返回可重复执行的内脑基线评估集。"""

    return (
        InnerBrainEvaluationCase("早上好", "assistant.greeting"),
        InnerBrainEvaluationCase("帮我看一下知识库状态", "knowledge.status", expected_command="/kb"),
        InnerBrainEvaluationCase("麻烦看一下知识库摘要", "knowledge.summary", expected_command="/kb-summary"),
        InnerBrainEvaluationCase("帮我联网查一下 Python 版本", "web.search", expected_command="/search Python 版本"),
        InnerBrainEvaluationCase("联网查一下 Python 版本并总结", "web.search_summarize", expected_command="/search-summary Python 版本"),
        InnerBrainEvaluationCase("读取第二份资料", "document.read_numbered_recent"),
        InnerBrainEvaluationCase("给第二份资料打标签 项目 Python", "document.tag_numbered_recent"),
        InnerBrainEvaluationCase("导入 note.txt 到知识库", "knowledge.import", expected_command='/import "note.txt"'),
        InnerBrainEvaluationCase("删除桌面快捷方式", "desktop.delete_shortcut", expected_policy=InnerBrainPolicy.CLARIFY),
        InnerBrainEvaluationCase("这句话需要外脑理解", "unknown", expected_policy=InnerBrainPolicy.FALLBACK_TO_LLM),
    )


def evaluate_inner_brain(
    inner_brain: InnerBrain,
    cases: tuple[InnerBrainEvaluationCase, ...] | None = None,
    name: str | None = None,
    source_filter: str | None = None,
) -> InnerBrainEvaluationReport:
    """执行固定评估集，不写入训练样本或运行态上下文。"""

    if cases is None:
        local_cases = load_evaluation_cases(inner_brain.paths)
        cases = (*seed_evaluation_cases(), *local_cases)
        if source_filter is not None:
            cases = tuple(case for case in cases if case.source == source_filter)
            report_name = name or source_filter
        else:
            report_name = name or ("seed_evaluation+local_evaluation" if local_cases else "seed_evaluation")
    else:
        if source_filter is not None:
            cases = tuple(case for case in cases if case.source == source_filter)
        report_name = name or "custom_evaluation"
    case_results = tuple(_evaluate_inner_brain_case(inner_brain, case) for case in cases)
    return InnerBrainEvaluationReport(name=report_name, case_results=case_results)


def load_evaluation_cases(paths: ProjectPaths | None) -> tuple[InnerBrainEvaluationCase, ...]:
    """读取本机评估 JSONL，只用于评估，不作为训练样本。"""

    if paths is None:
        return ()
    evaluation_dir = paths.data_dir / "inner-brain" / "evaluation"
    if not evaluation_dir.is_dir():
        return ()

    cases: list[InnerBrainEvaluationCase] = []
    for case_file in sorted(evaluation_dir.glob("*.jsonl")):
        cases.extend(_load_evaluation_case_file(case_file))
    return tuple(cases)


def save_local_evaluation_case(
    paths: ProjectPaths,
    case: InnerBrainEvaluationCase,
) -> InnerBrainEvaluationSaveResult:
    """保存本机评估样本，只用于评估，不写入训练样本。"""

    normalized_case = _normalized_local_evaluation_case(case)
    case_file = _runtime_evaluation_case_file(paths)
    relative_path = _relative_evaluation_case_path(paths, case_file)
    if _local_evaluation_case_exists(paths, normalized_case):
        return InnerBrainEvaluationSaveResult(
            case=normalized_case,
            path=case_file,
            relative_path=relative_path,
            created=False,
            duplicate=True,
        )

    case_file.parent.mkdir(parents=True, exist_ok=True)
    with case_file.open("a", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(_evaluation_case_payload(normalized_case), ensure_ascii=False, sort_keys=True) + "\n")
    return InnerBrainEvaluationSaveResult(
        case=normalized_case,
        path=case_file,
        relative_path=relative_path,
        created=True,
        duplicate=False,
    )


def describe_inner_brain_evaluation(report: InnerBrainEvaluationReport, failures_only: bool = False) -> str:
    """格式化内脑评估结果，供命令行和桌面转录查看。"""

    lines = [
        "InnerBrain 评估：",
        f"- 评估集：{report.name}",
        f"- 通过：{report.passed_count}/{report.total_count}",
        f"- 失败：{report.failed_count}",
        f"- 准确率：{report.accuracy * 100:.1f}%",
    ]
    for source, count in report.source_counts.items():
        lines.append(f"- {source}：{count} 条")
    case_results = report.failed_case_results if failures_only else report.case_results
    lines.append("失败样例：" if failures_only else "样例：")
    if failures_only and not case_results:
        lines.append("- 无")
    for case_result in case_results:
        mark = "PASS" if case_result.passed else "FAIL"
        lines.append(
            f"- {mark} {case_result.case.text} -> {case_result.result.intent} "
            f"({case_result.result.policy.value}, {case_result.result.confidence:.2f})"
        )
        if not case_result.passed:
            lines.append(f"  原因：{case_result.reason}")
    if report.failed_case_results:
        lines.append("失败修复建议：")
        for case_result in report.failed_case_results:
            lines.append(f"- {_inner_brain_evaluation_fix_suggestion(case_result)}")
        lines.append("说明：这里只生成显式训练提示，不自动写入 runtime 样本。")
    return "\n".join(lines)


def _evaluate_inner_brain_case(
    inner_brain: InnerBrain,
    case: InnerBrainEvaluationCase,
) -> InnerBrainEvaluationCaseResult:
    result = inner_brain.understand(case.text)
    failures: list[str] = []
    if result.intent != case.expected_intent:
        failures.append(f"意图期望 {case.expected_intent}，实际 {result.intent}")
    if result.policy != case.expected_policy:
        failures.append(f"策略期望 {case.expected_policy.value}，实际 {result.policy.value}")
    if case.expected_command is not None:
        command = result.natural_language_intent.command if result.natural_language_intent is not None else ""
        if command != case.expected_command:
            failures.append(f"命令期望 {case.expected_command}，实际 {command or '无'}")
    reason = "通过" if not failures else "；".join(failures)
    return InnerBrainEvaluationCaseResult(case=case, result=result, passed=not failures, reason=reason)


def _inner_brain_evaluation_fix_suggestion(case_result: InnerBrainEvaluationCaseResult) -> str:
    case = case_result.case
    text = " ".join(case.text.split())
    if case.expected_command:
        return f"{text}：/inner-brain-teach {text} => {case.expected_command}"
    if case.expected_policy == InnerBrainPolicy.EXECUTE:
        return f"{text}：/inner-brain-label {text} => {case.expected_intent}"
    return f"{text}：先确认 expected_policy={case.expected_policy.value} 是否符合预期，再决定是否补样本"


def _load_evaluation_case_file(case_file: Path) -> tuple[InnerBrainEvaluationCase, ...]:
    cases: list[InnerBrainEvaluationCase] = []
    for line in case_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            raw_case = json.loads(line)
        except json.JSONDecodeError:
            continue
        case = _evaluation_case_from_json(raw_case)
        if case is not None:
            cases.append(case)
    return tuple(cases)


def _evaluation_case_from_json(raw_case: object) -> InnerBrainEvaluationCase | None:
    if not isinstance(raw_case, dict):
        return None
    text = raw_case.get("text")
    expected_intent = raw_case.get("expected_intent")
    if not isinstance(text, str) or not text.strip():
        return None
    if not isinstance(expected_intent, str) or not expected_intent.strip():
        return None
    expected_policy = _evaluation_policy(raw_case.get("expected_policy", InnerBrainPolicy.EXECUTE.value))
    if expected_policy is None:
        return None
    expected_command = raw_case.get("expected_command")
    if expected_command is not None and not isinstance(expected_command, str):
        return None
    return InnerBrainEvaluationCase(
        text=text.strip(),
        expected_intent=expected_intent.strip(),
        expected_policy=expected_policy,
        expected_command=expected_command.strip() if isinstance(expected_command, str) and expected_command.strip() else None,
        source="local_evaluation",
    )


def _evaluation_policy(raw_policy: object) -> InnerBrainPolicy | None:
    if isinstance(raw_policy, InnerBrainPolicy):
        return raw_policy
    if not isinstance(raw_policy, str):
        return None
    try:
        return InnerBrainPolicy(raw_policy.strip())
    except ValueError:
        return None


def _normalized_local_evaluation_case(case: InnerBrainEvaluationCase) -> InnerBrainEvaluationCase:
    text = case.text.strip()
    expected_intent = case.expected_intent.strip()
    if not text:
        raise ValueError("评估样本文本不能为空")
    if not expected_intent or re.search(r"\s", expected_intent):
        raise ValueError("expected_intent 不能为空且不能包含空白")
    expected_command = case.expected_command.strip() if isinstance(case.expected_command, str) else None
    return InnerBrainEvaluationCase(
        text=text,
        expected_intent=expected_intent,
        expected_policy=case.expected_policy,
        expected_command=expected_command or None,
        source="local_evaluation",
    )


def _runtime_evaluation_case_file(paths: ProjectPaths) -> Path:
    return paths.data_dir / "inner-brain" / "evaluation" / "runtime.jsonl"


def _relative_evaluation_case_path(paths: ProjectPaths, case_file: Path) -> str:
    try:
        return case_file.relative_to(paths.root).as_posix()
    except ValueError:
        return case_file.as_posix()


def _local_evaluation_case_exists(paths: ProjectPaths, case: InnerBrainEvaluationCase) -> bool:
    case_key = _evaluation_case_key(case)
    return any(_evaluation_case_key(existing_case) == case_key for existing_case in load_evaluation_cases(paths))


def _evaluation_case_key(case: InnerBrainEvaluationCase) -> str:
    return json.dumps(_evaluation_case_payload(case), ensure_ascii=False, sort_keys=True)


def _evaluation_case_payload(case: InnerBrainEvaluationCase) -> dict[str, str]:
    payload = {
        "expected_intent": case.expected_intent,
        "expected_policy": case.expected_policy.value,
        "text": case.text,
    }
    if case.expected_command:
        payload["expected_command"] = case.expected_command
    return payload


def complete_inner_brain_clarification(result: InnerBrainResult, reply: str) -> InnerBrainResult:
    """用用户下一句回复补齐缺失槽位，并复用既有意图映射。"""

    if result.policy != InnerBrainPolicy.CLARIFY or not result.missing:
        return result

    slots = _normalized_slots(result.slots)
    slots.update(_clarification_slots_from_reply(reply, result.intent, result.missing))
    missing = tuple(slot for slot in result.missing if not _slot_is_present(slot, slots))

    natural_language_intent = None
    if not missing:
        sample = InnerBrainTrainingSample("", result.intent, {})
        natural_language_intent = _sample_to_natural_language_intent(reply, sample, slots)

    if missing or natural_language_intent is None:
        return InnerBrainResult(
            intent=result.intent,
            slots=slots,
            confidence=result.confidence,
            missing=missing or result.missing,
            source=result.source,
            reason="已接收补充信息，但槽位仍未完整",
            policy=InnerBrainPolicy.CLARIFY,
            natural_language_intent=None,
        )

    return InnerBrainResult(
        intent=result.intent,
        slots=slots,
        confidence=result.confidence,
        missing=(),
        source=result.source,
        reason="已根据用户补充信息补齐槽位",
        policy=InnerBrainPolicy.EXECUTE,
        natural_language_intent=natural_language_intent,
    )


def load_training_samples(paths: ProjectPaths | None) -> tuple[InnerBrainTrainingSample, ...]:
    """读取运行态 JSONL 样本，格式为 text -> intent -> slots。"""

    if paths is None:
        return ()
    training_dir = paths.data_dir / "inner-brain" / "training"
    if not training_dir.is_dir():
        return ()

    samples: list[InnerBrainTrainingSample] = []
    for sample_file in sorted(training_dir.glob("*.jsonl")):
        samples.extend(_load_training_sample_file(sample_file))
    return tuple(samples)


def save_runtime_training_sample(
    paths: ProjectPaths,
    text: str,
    result: InnerBrainResult,
) -> InnerBrainTrainingSaveResult:
    """把一次 InnerBrain 识别结果保存为运行态 JSONL 样本。"""

    prompt = text.strip()
    if not prompt:
        raise ValueError("输入为空")
    if result.intent == "unknown" or result.policy == InnerBrainPolicy.FALLBACK_TO_LLM:
        raise ValueError(f"当前识别结果为 {result.intent}，不能保存为训练样本")

    sample = InnerBrainTrainingSample(
        text=prompt,
        intent=result.intent,
        slots=_training_slots_from_result(result),
        missing=result.missing,
        source="runtime_sample",
    )
    return _save_runtime_training_sample(paths, sample)


def save_labeled_runtime_training_sample(
    paths: ProjectPaths,
    text: str,
    intent: str,
    slots: Mapping[str, Any],
    missing: tuple[str, ...] = (),
) -> InnerBrainTrainingSaveResult:
    """保存人工标注的运行态样本，用于纠正 unknown 或误识别输入。"""

    prompt = text.strip()
    intent_label = intent.strip()
    if not prompt:
        raise ValueError("输入为空")
    if not intent_label or re.search(r"\s", intent_label):
        raise ValueError("intent 不能为空且不能包含空白")

    sample = InnerBrainTrainingSample(
        text=prompt,
        intent=intent_label,
        slots=_json_ready_mapping(slots),
        missing=tuple(str(item).strip() for item in missing if str(item).strip()),
        source="runtime_sample",
    )
    return _save_runtime_training_sample(paths, sample)


def _save_runtime_training_sample(
    paths: ProjectPaths,
    sample: InnerBrainTrainingSample,
) -> InnerBrainTrainingSaveResult:
    sample_file = _runtime_training_sample_file(paths)
    relative_path = _relative_training_sample_path(paths, sample_file)
    if _runtime_training_sample_exists(paths, sample):
        return InnerBrainTrainingSaveResult(
            sample=sample,
            path=sample_file,
            relative_path=relative_path,
            created=False,
            duplicate=True,
        )

    sample_file.parent.mkdir(parents=True, exist_ok=True)
    with sample_file.open("a", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(_training_sample_payload(sample), ensure_ascii=False, sort_keys=True) + "\n")
    return InnerBrainTrainingSaveResult(
        sample=sample,
        path=sample_file,
        relative_path=relative_path,
        created=True,
        duplicate=False,
    )


def _load_training_sample_file(sample_file: Path) -> tuple[InnerBrainTrainingSample, ...]:
    samples: list[InnerBrainTrainingSample] = []
    for line in sample_file.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            raw_sample = json.loads(line)
        except json.JSONDecodeError:
            continue
        sample = _training_sample_from_json(raw_sample)
        if sample is not None:
            samples.append(sample)
    return tuple(samples)


def _runtime_training_sample_file(paths: ProjectPaths) -> Path:
    return paths.data_dir / "inner-brain" / "training" / "runtime.jsonl"


def _relative_training_sample_path(paths: ProjectPaths, sample_file: Path) -> str:
    try:
        return sample_file.relative_to(paths.root).as_posix()
    except ValueError:
        return sample_file.as_posix()


def _runtime_training_sample_exists(paths: ProjectPaths, sample: InnerBrainTrainingSample) -> bool:
    sample_key = _training_sample_key(sample)
    return any(_training_sample_key(existing_sample) == sample_key for existing_sample in load_training_samples(paths))


def _training_sample_key(sample: InnerBrainTrainingSample) -> str:
    return json.dumps(_training_sample_payload(sample), ensure_ascii=False, sort_keys=True)


def _training_sample_payload(sample: InnerBrainTrainingSample) -> dict[str, Any]:
    return {
        "intent": sample.intent,
        "missing": list(sample.missing),
        "slots": _json_ready_mapping(sample.slots),
        "text": sample.text,
    }


def _training_slots_from_result(result: InnerBrainResult) -> dict[str, Any]:
    slots = dict(result.slots)
    if result.natural_language_intent is not None:
        slots.update(_slots_from_natural_language_intent(result.natural_language_intent))
    return _json_ready_mapping(slots)


def _json_ready_mapping(values: Mapping[str, Any]) -> dict[str, Any]:
    return {key: _json_ready_value(value) for key, value in values.items()}


def _json_ready_value(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, tuple | list):
        return [_json_ready_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_ready_value(item) for key, item in value.items()}
    return value


def _training_sample_from_json(raw_sample: object) -> InnerBrainTrainingSample | None:
    if not isinstance(raw_sample, dict):
        return None
    text = raw_sample.get("text")
    intent = raw_sample.get("intent")
    slots = raw_sample.get("slots")
    if not isinstance(text, str) or not text.strip():
        return None
    if not isinstance(intent, str) or not intent.strip():
        return None
    if not isinstance(slots, dict):
        return None
    missing = raw_sample.get("missing", ())
    if not isinstance(missing, list):
        missing = ()
    return InnerBrainTrainingSample(
        text=text.strip(),
        intent=intent.strip(),
        slots=slots,
        missing=tuple(str(item).strip() for item in missing if str(item).strip()),
        source="runtime_sample",
    )


def _sample_similarity(prompt: str, sample: InnerBrainTrainingSample) -> float:
    prompt_text = _similarity_text(prompt, sample.intent)
    sample_text = _similarity_text(sample.text, sample.intent)
    if prompt_text == sample_text:
        return 1.0
    score = _dice_similarity(_features(prompt_text), _features(sample_text))
    return max(score, _contained_sample_signature_similarity(prompt_text, sample_text))


def _similarity_text(text: str, intent: str) -> str:
    normalized = _normalize_text(text)
    if intent == "document.read_recent":
        return _recent_document_signature(normalized)
    if intent == "document.read_numbered_recent":
        return _numbered_recent_document_signature(normalized)
    if intent == "recent_file.read_numbered":
        return _numbered_recent_file_signature(normalized)
    if intent == "recent_file.import_numbered":
        return _import_numbered_recent_file_signature(normalized)
    if intent == "search_result.read_numbered":
        return _numbered_search_result_signature(normalized)
    if intent == "advice.read_numbered":
        return _numbered_advice_signature(normalized)
    if intent == "advice.execute_numbered":
        return _execute_numbered_advice_signature(normalized)
    if intent == "document.read_path":
        return _read_document_path_signature(normalized)
    if intent == "knowledge.import":
        return _import_source_signature(normalized)
    if intent == "directory.open_drive":
        return _open_drive_signature(normalized)
    if intent == "directory.open_alias":
        return _open_directory_alias_signature(normalized)
    if intent == "directory.organize_alias":
        return _organize_directory_alias_signature(normalized)
    if intent == "directory.open_recent":
        return _open_recent_directory_signature(normalized)
    if intent == "directory.organize_recent":
        return _organize_recent_directory_signature(normalized)
    if intent == "experience.record":
        return _experience_record_signature(normalized)
    if intent == "experience.search":
        return _experience_search_signature(normalized)
    if intent == "experience.advice":
        return _experience_advice_signature(normalized)
    if intent == "document.tag_path":
        return _tag_path_signature(normalized)
    if intent == "document.tag_recent":
        return _tag_recent_document_signature(normalized)
    if intent == "document.tag_numbered_recent":
        return _tag_numbered_recent_document_signature(normalized)
    if intent == "search_result.tag_numbered":
        return _tag_numbered_search_result_signature(normalized)
    if intent == "tag_group.preview_tagging":
        return _tag_group_preview_tagging_signature(normalized)
    if intent == "tag_group.read":
        return _tag_group_read_signature(normalized)
    if intent == "tag_history.read_numbered":
        return _tag_history_read_numbered_signature(normalized)
    if intent == "desktop.delete_shortcut":
        return _desktop_shortcut_signature(normalized)
    if intent == "web.search_summarize":
        return _web_search_summary_signature(normalized)
    if intent == "web.search":
        return _web_search_signature(normalized)
    if intent == "web_search.open_numbered":
        return _numbered_web_search_source_signature(normalized)
    if intent == "web_search.compare_recent":
        return _web_search_compare_recent_signature(normalized)
    if intent == "web_search.save_summary":
        return _web_search_save_summary_signature(normalized)
    if intent == "web_search.import_summary":
        return _web_search_import_summary_signature(normalized)
    return normalized


def _normalize_text(text: str) -> str:
    return re.sub(r"[\s。！？!?.,，、：:；;“”\"'（）()]+", "", text.strip().lower())


_NUMBER_SLOT_PATTERN = r"[0-9一二两三四五六七八九十]+|\{index\}"


def _recent_document_signature(text: str) -> str:
    if re.fullmatch(r"(?:读取|查看|看看)(?:这个|这份|刚才的|最近的|当前)(?:资料|文档|文件)", text):
        return "读取这个资料"
    return text


def _numbered_recent_document_signature(text: str) -> str:
    match = re.fullmatch(
        rf"(?P<verb>读取|查看|看看)第(?:{_NUMBER_SLOT_PATTERN})(?:条|个|份)?(?:资料|文档|文件)",
        text,
    )
    if not match:
        return text
    verb = "读取" if match.group("verb") == "读取" else "查看"
    return f"{verb}第{{index}}份资料"


def _numbered_recent_file_signature(text: str) -> str:
    match = re.fullmatch(
        rf"(?P<verb>读取|查看|看看)第(?:{_NUMBER_SLOT_PATTERN})(?:条|个|份)?(?:最近文件|系统最近文件)",
        text,
    )
    if not match:
        return text
    verb = "读取" if match.group("verb") == "读取" else "查看"
    return f"{verb}第{{index}}份最近文件"


def _import_numbered_recent_file_signature(text: str) -> str:
    import_match = re.fullmatch(
        rf"(?:请帮我|请|帮我)?导入第(?:{_NUMBER_SLOT_PATTERN})(?:条|个|份)?(?:最近文件|系统最近文件)(?:(?:到|进|加入|放进)?(?:知识库|资料库))?",
        text,
    )
    if import_match:
        return "导入第{index}份最近文件到知识库"

    object_first_match = re.fullmatch(
        rf"(?:请帮我|请|帮我)?把第(?:{_NUMBER_SLOT_PATTERN})(?:条|个|份)?(?:最近文件|系统最近文件)(?:导入|加入|放进)(?:(?:到|进|加入|放进)?(?:知识库|资料库))?",
        text,
    )
    if object_first_match:
        return "把第{index}份最近文件导入知识库"
    return text


def _numbered_search_result_signature(text: str) -> str:
    match = re.fullmatch(rf"(?P<verb>查看|看看|读取|打开)第(?:{_NUMBER_SLOT_PATTERN})(?:条|个)?结果", text)
    if not match:
        return text
    verb = "读取" if match.group("verb") == "读取" else "查看"
    return f"{verb}第{{index}}条结果"


def _numbered_web_search_source_signature(text: str) -> str:
    match = re.fullmatch(
        rf"(?P<verb>查看|看看|读取|打开)第(?:{_NUMBER_SLOT_PATTERN})(?:条|个)?(?:联网搜索结果|联网来源|搜索来源|来源)",
        text,
    )
    if not match:
        return text
    if match.group("verb") == "打开":
        return "打开第{index}条联网搜索结果"
    return "查看第{index}条联网来源"


def _numbered_advice_signature(text: str) -> str:
    match = re.fullmatch(rf"(?P<verb>查看|看看|读取)第(?:{_NUMBER_SLOT_PATTERN})(?:条|个)?建议", text)
    if not match:
        return text
    verb = "读取" if match.group("verb") == "读取" else "查看"
    return f"{verb}第{{index}}条建议"


def _execute_numbered_advice_signature(text: str) -> str:
    match = re.fullmatch(rf"(?P<verb>执行|运行)第(?:{_NUMBER_SLOT_PATTERN})(?:条|个)?建议", text)
    if not match:
        return text
    return f"{match.group('verb')}第{{index}}条建议"


def _read_document_path_signature(text: str) -> str:
    if re.fullmatch(r"(?:请|帮我)?(?P<verb>读取|查看|看看)(?:\{path\}|.+(?:md|txt))", text):
        verb = "读取" if text.startswith(("读取", "请读取", "帮我读取")) else "查看"
        return f"{verb}{{path}}"
    return text


def _import_source_signature(text: str) -> str:
    if "最近文件" in text or "系统最近文件" in text:
        return text
    source_pattern = r"(?:\{source\}|.+(?:md|txt|pdf|json)|.+[/\\].+)"
    if re.fullmatch(rf"(?:请|帮我)?导入{source_pattern}(?:(?:到|进|加入)?(?:知识库|资料库))", text):
        return "导入{source}到知识库"
    if re.fullmatch(rf"(?:请|帮我)?把{source_pattern}(?:导入|加入|放进)(?:(?:到|进|加入|放进)?(?:知识库|资料库))", text):
        return "把{source}导入知识库"
    return text


def _open_drive_signature(text: str) -> str:
    if re.fullmatch(r"(?:帮我)?打开(?:\{drive\}|[a-z])(?:盘)?", text):
        return "打开{drive}盘"
    return text


def _open_directory_alias_signature(text: str) -> str:
    match = re.fullmatch(r"(?:帮我)?打开(?P<alias>.+?)(?:目录|文件夹)", text)
    if not match:
        return text
    if _is_recent_directory_reference(match.group("alias")):
        return text
    return "打开{alias}目录"


def _organize_directory_alias_signature(text: str) -> str:
    match = re.fullmatch(r"(?:帮我)?(?:整理|整理预览|预览整理)(?P<alias>.+?)(?:目录|文件夹)", text)
    if not match:
        return text
    if _is_recent_directory_reference(match.group("alias")):
        return text
    return "整理{alias}目录"


def _open_recent_directory_signature(text: str) -> str:
    if re.fullmatch(r"(?:帮我)?打开(?:这个|刚才的|最近的|当前)(?:目录|文件夹)", text):
        return "打开这个目录"
    return text


def _organize_recent_directory_signature(text: str) -> str:
    if re.fullmatch(r"(?:帮我)?(?:整理|整理预览|预览整理)(?:这个|刚才的|最近的|当前)(?:目录|文件夹)", text):
        return "整理这个目录"
    return text


def _experience_record_signature(text: str) -> str:
    if re.fullmatch(r"(?:请|帮我)?(?:记录|保存|沉淀)(?:一条)?经验.+", text):
        return "记录经验{experience}"
    if re.fullmatch(r"(?:请|帮我)?记住(?:这个|这条)?经验.+", text):
        return "记住这个经验{experience}"
    return text


def _experience_search_signature(text: str) -> str:
    if re.fullmatch(r"(?:请|帮我)?(?:搜索|查找|查询)经验.+", text):
        return "搜索经验{query}"
    if re.fullmatch(r"(?:请|帮我)?经验(?:搜索|查找|查询).+", text):
        return "经验查询{query}"
    return text


def _experience_advice_signature(text: str) -> str:
    if re.fullmatch(r"(?:我该怎么|我应该怎么|该怎么|如何|怎样).+", text):
        return "我该怎么{query}"
    if re.fullmatch(r".+(?:有什么|有哪些|有啥)(?:经验|建议)", text):
        return "{query}有什么建议"
    if re.fullmatch(r"(?:给我|请给我|帮我给).+?(?:的)?(?:经验建议|建议)", text):
        return "{query}有什么建议"
    return text


def _tag_recent_document_signature(text: str) -> str:
    match = re.fullmatch(r"(?:给|把)(?P<target>这个|这份|刚才的|最近的|当前)(?P<kind>资料|文档|文件|结果)(?:打标签|标记为).+", text)
    if not match:
        return text
    if match.group("kind") == "结果":
        return "给这个结果打标签{tags}"
    return "给这个资料打标签{tags}"


def _tag_path_signature(text: str) -> str:
    path_pattern = r"(?:\{path\}|.+(?:md|txt))"
    if re.fullmatch(rf"(?:给){path_pattern}(?:打标签|标记为).+", text):
        return "给{path}打标签{tags}"
    if re.fullmatch(rf"(?:把){path_pattern}(?:打标签|标记为).+", text):
        return "把{path}标记为{tags}"
    return text


def _tag_numbered_recent_document_signature(text: str) -> str:
    if re.fullmatch(rf"(?:给|把)第(?:{_NUMBER_SLOT_PATTERN})(?:条|个|份)?(?:资料|文档|文件)(?:打标签|标记为).+", text):
        return "给第{index}份资料打标签{tags}"
    return text


def _tag_numbered_search_result_signature(text: str) -> str:
    if re.fullmatch(rf"(?:给|把)第(?:{_NUMBER_SLOT_PATTERN})(?:条|个)?结果(?:打标签|标记为).+", text):
        return "给第{index}条结果打标签{tags}"
    return text


def _tag_group_preview_tagging_signature(text: str) -> str:
    if re.fullmatch(r"(?:请|帮我)?(?:给|把).+?标签(?:资料|文档)(?:都|全部)?(?:打标签|标记为).+", text):
        return "给{tag}标签资料都打标签{tags}"
    return text


def _tag_group_read_signature(text: str) -> str:
    match = re.fullmatch(r"(?P<verb>请?帮?我?)?(?P<action>读取|查看|看看).+?标签(?:资料|文档)", text)
    if not match:
        return text
    action = "读取" if match.group("action") == "读取" else "查看"
    return f"{action}{{tag}}标签资料"


def _tag_history_read_numbered_signature(text: str) -> str:
    match = re.fullmatch(
        rf"(?P<verb>读取|查看|看看)第(?:{_NUMBER_SLOT_PATTERN})(?:条|个)?(?:批量标签历史|批量打标签历史|标签历史)(?:影响)?(?:资料|文档)",
        text,
    )
    if not match:
        return text
    if match.group("verb") == "查看" and "批量标签历史" in text:
        return "查看第{index}条批量标签历史影响资料"
    return "读取第{index}条标签历史资料"


def _desktop_shortcut_signature(text: str) -> str:
    patterns = (
        r"(?:请|帮我|麻烦)?(?:把)?桌面(?:上|上的)?(?P<item>.+?)快捷方式(?:删除|删掉|移除)",
        r"(?:请|帮我|麻烦)?(?:删除|删掉|移除)桌面(?:上|上的)?(?P<item>.+?)快捷方式",
        r"(?:请|帮我|麻烦)?(?:把)?桌面(?:上|上的)?快捷方式(?P<item>.+?)(?:删除|删掉|移除)",
    )
    for pattern in patterns:
        if re.fullmatch(pattern, text):
            if text.startswith(("删除", "删掉", "移除")):
                return "删除桌面{item}快捷方式"
            if "桌面快捷方式" in text or "桌面上快捷方式" in text or "桌面上的快捷方式" in text:
                return "桌面快捷方式{item}删除"
            return "把桌面{item}快捷方式删除"
    return text


def _web_search_signature(text: str) -> str:
    patterns = (
        r"(?:请|帮我|麻烦)?(?:联网|上网|网上)?(?:查一下|查查|搜索一下|搜一下)(?P<query>.+)",
        r"(?:请|帮我|麻烦)?(?:帮我)?看看网上(?P<query>.+)",
    )
    for pattern in patterns:
        if not re.fullmatch(pattern, text):
            continue
        if "搜索一下" in text or "搜一下" in text:
            return "搜索一下{query}"
        if "网上" in text and "看看" in text:
            return "帮我看看网上{query}"
        return "联网查一下{query}"
    return text


def _web_search_summary_signature(text: str) -> str:
    patterns = (
        r"(?:请|帮我|麻烦)?(?:联网|上网|网上)?(?:查一下|查查)(?P<query>.+?)(?:并|然后)?(?:总结|总结一下)",
        r"(?:请|帮我|麻烦)?(?:搜索一下|搜一下)(?P<query>.+?)(?:并|然后)?(?:总结|总结一下)",
    )
    for pattern in patterns:
        if not re.fullmatch(pattern, text):
            continue
        if "搜索一下" in text or "搜一下" in text:
            return "搜索一下{query}并总结"
        return "联网查一下{query}并总结"
    return text


def _web_search_compare_recent_signature(text: str) -> str:
    if re.fullmatch(r"(?:请|帮我|麻烦)?(?:比较|对比)(?:一下)?(?:这些|这几个|当前|最近)?(?:联网)?(?:搜索)?(?:来源|结果)", text):
        return "比较这些联网来源"
    return text


def _web_search_save_summary_signature(text: str) -> str:
    if re.fullmatch(r"(?:请|帮我|麻烦)?(?:保存|写入)(?:这个|当前|最近)?(?:联网)?搜索摘要", text):
        return "保存这个搜索摘要"
    return text


def _web_search_import_summary_signature(text: str) -> str:
    if re.fullmatch(
        r"(?:请|帮我|麻烦)?(?:导入|加入|保存)(?:这个|当前|最近)?(?:联网)?搜索摘要(?:到|进|加入)?(?:知识库|资料库)",
        text,
    ):
        return "导入这个搜索摘要到知识库"
    return text


def _features(text: str) -> set[str]:
    if not text:
        return set()
    features = set(text)
    features.update(text[index : index + 2] for index in range(len(text) - 1))
    return features


def _dice_similarity(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return (2 * len(left & right)) / (len(left) + len(right))


def _contained_sample_signature_similarity(prompt_text: str, sample_text: str) -> float:
    if len(sample_text) < 4 or sample_text not in prompt_text:
        return 0.0
    coverage = len(sample_text) / max(len(prompt_text), 1)
    return min(0.94, HIGH_CONFIDENCE + coverage * 0.18)


def _sample_to_natural_language_intent(
    prompt: str,
    sample: InnerBrainTrainingSample,
    slots: Mapping[str, Any],
) -> NaturalLanguageIntent | None:
    command = slots.get("command")
    if isinstance(command, str) and command.strip().startswith("/"):
        return NaturalLanguageIntent("command", command=command.strip())
    if sample.intent == "knowledge.summary":
        return NaturalLanguageIntent("command", command="/kb-summary")
    if sample.intent == "knowledge.status":
        return NaturalLanguageIntent("command", command="/kb")
    if sample.intent == "assistant.identity":
        return NaturalLanguageIntent("assistant_identity")
    if sample.intent == "assistant.greeting":
        return NaturalLanguageIntent("greeting", alias=prompt.strip())
    if sample.intent == "assistant.capabilities":
        return NaturalLanguageIntent("capabilities")
    if sample.intent == "context.recent_status":
        return NaturalLanguageIntent("recent_context_status")
    if sample.intent == "context.recent_files":
        return NaturalLanguageIntent("recent_files_status")
    if sample.intent == "document.read_recent":
        return NaturalLanguageIntent("read_recent_document")
    if sample.intent == "document.read_numbered_recent":
        result_index = _slot_result_index(slots)
        if result_index > 0:
            return NaturalLanguageIntent("read_numbered_recent_document", result_index=result_index)
        return None
    if sample.intent == "recent_file.read_numbered":
        result_index = _slot_result_index(slots)
        if result_index > 0:
            return NaturalLanguageIntent("read_numbered_recent_file", result_index=result_index)
        return None
    if sample.intent == "recent_file.import_numbered":
        result_index = _slot_result_index(slots)
        if result_index > 0:
            return NaturalLanguageIntent("import_numbered_recent_file", result_index=result_index)
        return None
    if sample.intent == "search_result.read_numbered":
        result_index = _slot_result_index(slots)
        if result_index > 0:
            return NaturalLanguageIntent("read_numbered_search_result", result_index=result_index)
        return None
    if sample.intent == "advice.read_numbered":
        result_index = _slot_result_index(slots)
        if result_index > 0:
            return NaturalLanguageIntent("read_numbered_advice_suggestion", result_index=result_index)
        return None
    if sample.intent == "advice.execute_numbered":
        result_index = _slot_result_index(slots)
        if result_index > 0:
            return NaturalLanguageIntent("prepare_numbered_advice_suggestion_execution", result_index=result_index)
        return None
    if sample.intent == "document.read_path":
        path = _slot_path(slots)
        if path:
            return NaturalLanguageIntent("command", command=f'/read "{path}"')
        return None
    if sample.intent == "directory.open_drive":
        alias = _slot_alias(slots)
        path = _slot_path(slots)
        if alias and path:
            return NaturalLanguageIntent("open_directory_path", alias=alias, path=Path(path))
        return None
    if sample.intent == "directory.open_alias":
        alias = _slot_alias(slots)
        if alias:
            return NaturalLanguageIntent("open_directory_alias", alias=alias)
        return None
    if sample.intent == "directory.organize_alias":
        alias = _slot_alias(slots)
        if alias:
            return NaturalLanguageIntent("organize_directory_alias", alias=alias)
        return None
    if sample.intent == "directory.open_recent":
        return NaturalLanguageIntent("open_recent_directory")
    if sample.intent == "directory.organize_recent":
        return NaturalLanguageIntent("organize_recent_directory")
    if sample.intent == "experience.record":
        experience = _slot_text(slots, "experience")
        if experience:
            return NaturalLanguageIntent("command", command=f"/experience {experience}")
        return None
    if sample.intent == "experience.search":
        query = _slot_text(slots, "query")
        if query:
            return NaturalLanguageIntent("command", command=f"/experience-search {query}")
        return None
    if sample.intent == "experience.advice":
        query = _slot_text(slots, "query")
        if query:
            return NaturalLanguageIntent("command", command=f"/experience-advice {query}")
        return None
    if sample.intent == "document.tag_path":
        path = _slot_path(slots)
        tags = _slot_tags(slots)
        if path and tags:
            return NaturalLanguageIntent("command", command=f'/tag "{path}" {" ".join(tags)}')
        return None
    if sample.intent == "document.tag_recent":
        tags = _slot_tags(slots)
        if tags:
            return NaturalLanguageIntent("tag_recent_document", tags=tags)
        return None
    if sample.intent == "document.tag_numbered_recent":
        result_index = _slot_result_index(slots)
        tags = _slot_tags(slots)
        if result_index > 0 and tags:
            return NaturalLanguageIntent("tag_numbered_recent_document", tags=tags, result_index=result_index)
        return None
    if sample.intent == "search_result.tag_numbered":
        result_index = _slot_result_index(slots)
        tags = _slot_tags(slots)
        if result_index > 0 and tags:
            return NaturalLanguageIntent("tag_numbered_search_result", tags=tags, result_index=result_index)
        return None
    if sample.intent == "tag_group.preview_tagging":
        alias = _slot_alias(slots)
        tags = _slot_tags(slots)
        if alias and tags:
            return NaturalLanguageIntent("preview_tagged_documents_tagging", alias=alias, tags=tags)
        return None
    if sample.intent == "tag_group.read":
        alias = _slot_alias(slots)
        if alias:
            return NaturalLanguageIntent("read_tagged_documents", alias=alias)
        return None
    if sample.intent == "tag_history.read_numbered":
        result_index = _slot_result_index(slots)
        if result_index > 0:
            return NaturalLanguageIntent("read_tagged_documents_history_documents", result_index=result_index)
        return None
    if sample.intent == "advice.confirm_execution":
        return NaturalLanguageIntent("confirm_pending_advice_suggestion_execution")
    if sample.intent == "advice.cancel_execution":
        return NaturalLanguageIntent("cancel_pending_advice_suggestion_execution")
    if sample.intent == "web.search":
        query = _slot_text(slots, "query") or _extract_web_search_query(prompt)
        if query:
            return NaturalLanguageIntent("command", command=f"/search {query}")
        return None
    if sample.intent == "web.search_summarize":
        query = _slot_text(slots, "query") or _extract_web_search_summary_query(prompt)
        if query:
            return NaturalLanguageIntent("command", command=f"/search-summary {query}")
        return None
    if sample.intent == "web_search.open_numbered":
        result_index = _slot_result_index(slots)
        if result_index > 0:
            return NaturalLanguageIntent("command", command=f"/search-open {result_index}")
        return None
    if sample.intent == "web_search.compare_recent":
        return NaturalLanguageIntent("command", command="/search-compare")
    if sample.intent == "web_search.save_summary":
        return NaturalLanguageIntent("command", command="/search-save-summary")
    if sample.intent == "web_search.import_summary":
        return NaturalLanguageIntent("command", command="/search-import-summary")
    if sample.intent == "desktop.delete_shortcut":
        items = _extract_desktop_shortcut_items(prompt)
        if not items:
            raw_items = slots.get("items", ())
            if isinstance(raw_items, str):
                items = (raw_items,)
            elif isinstance(raw_items, list | tuple):
                items = tuple(str(item).strip() for item in raw_items if str(item).strip())
        if not items:
            return None
        return NaturalLanguageIntent("delete_desktop_shortcuts", items=items)
    if sample.intent == "knowledge.import" and "source" in slots:
        source = str(slots["source"]).strip()
        if source:
            return NaturalLanguageIntent("command", command=f'/import "{source}"')
    return None


def _extract_desktop_shortcut_items(text: str) -> tuple[str, ...]:
    normalized = text.strip().strip("。！？!?.")
    patterns = (
        r"(?:请|帮我|麻烦)?(?:把)?桌面(?:上|上的)?(?P<items>.+?)快捷方式(?:删除|删掉|移除)",
        r"(?:请|帮我|麻烦)?(?:删除|删掉|移除)桌面(?:上|上的)?(?P<items>.+?)快捷方式",
        r"(?:请|帮我|麻烦)?(?:把)?桌面(?:上|上的)?快捷方式(?P<items>.+?)(?:删除|删掉|移除)",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, normalized)
        if not match:
            continue
        return _split_shortcut_items(match.group("items"))
    return ()


def _extract_web_search_query(text: str) -> str:
    normalized = text.strip().strip("。！？!?.")
    patterns = (
        r"(?:请|帮我|麻烦)?(?:联网|上网|网上)?(?:查一下|查查|搜索一下|搜一下)\s*(?P<query>.+)",
        r"(?:请|帮我|麻烦)?(?:帮我)?看看网上\s*(?P<query>.+)",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, normalized)
        if not match:
            continue
        query = match.group("query").strip()
        if query:
            return query
    return ""


def _extract_web_search_summary_query(text: str) -> str:
    normalized = text.strip().strip("。！？!?.")
    patterns = (
        r"(?:请|帮我|麻烦)?(?:联网|上网|网上)?(?:查一下|查查)\s*(?P<query>.+?)\s*(?:并|然后)?(?:总结|总结一下)",
        r"(?:请|帮我|麻烦)?(?:搜索一下|搜一下)\s*(?P<query>.+?)\s*(?:并|然后)?(?:总结|总结一下)",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, normalized)
        if not match:
            continue
        query = match.group("query").strip()
        if query:
            return query
    return ""


def _split_shortcut_items(text: str) -> tuple[str, ...]:
    items: list[str] = []
    for raw_item in re.split(r"\s*(?:和|及|与|、|，|,)\s*", text.strip()):
        item = raw_item.strip().strip("“”\"'").strip()
        item = item.removeprefix("的").removesuffix("的").removesuffix("快捷方式").strip()
        if item.lower().endswith(".lnk"):
            item = item[:-4].strip()
        if item and item != "{item}":
            items.append(item)
    return tuple(items)


def _sample_slots(prompt: str, sample: InnerBrainTrainingSample) -> dict[str, Any]:
    slots = _normalized_slots(sample.slots)
    result_index = _extract_numbered_result_index(prompt, sample.intent)
    if result_index > 0:
        slots["result_index"] = result_index
    file_path_slots = _extract_file_path_slots(prompt, sample.intent)
    slots.update(file_path_slots)
    directory_slots = _extract_directory_slots(prompt, sample.intent)
    slots.update(directory_slots)
    experience_slots = _extract_experience_slots(prompt, sample.intent)
    slots.update(experience_slots)
    web_search_slots = _extract_web_search_slots(prompt, sample.intent)
    slots.update(web_search_slots)
    tag_slots = _extract_tag_slots(prompt, sample.intent)
    slots.update(tag_slots)
    return slots


def _clarification_slots_from_reply(reply: str, intent: str, missing: tuple[str, ...]) -> dict[str, Any]:
    slots: dict[str, Any] = {}
    value = _normalize_clarification_value(reply)
    if intent == "tag_group.preview_tagging" and {"alias", "tags"}.issubset(set(missing)):
        slots.update(_clarification_tag_group_slots(value))
        if "alias" in slots and "tags" in slots:
            return slots
    for slot in missing:
        if slot == "source":
            source = _extract_import_source(reply) or value
            if _looks_like_path_or_file(source):
                slots["source"] = source
        elif slot == "path":
            path = _extract_read_document_path(reply) or value
            if _looks_like_path_or_file(path):
                slots["path"] = _normalize_read_document_path(path)
        elif slot == "items":
            items = _split_shortcut_items(value)
            if items:
                slots["items"] = items
        elif slot == "tags":
            tags = _split_tag_text(_clarification_tag_text(value, missing))
            if tags:
                slots["tags"] = tags
        elif slot == "result_index":
            result_index = _extract_clarification_number(value)
            if result_index > 0:
                slots["result_index"] = result_index
        elif slot in {"query", "experience", "alias"} and value:
            slots[slot] = value
    return slots


def _clarification_tag_group_slots(value: str) -> dict[str, Any]:
    """解析标签组补槽，避免把标签组名当成新增标签。"""

    normalized = value.strip()
    if not normalized:
        return {}
    normalized = re.sub(r"^(?:标签组|目录别名|别名|目录)\s*(?:是|为)?\s*[:：]?\s*", "", normalized)
    normalized = re.sub(r"\s*(?:新标签|追加标签|标签)\s*(?:是|为)?\s*[:：]\s*", " ", normalized, count=1)
    parts = [part.strip() for part in re.split(r"\s+|[，,、;；]+", normalized) if part.strip()]
    if len(parts) < 2:
        return {}
    alias = _normalize_directory_alias(_strip_wrapping_quotes(parts[0]))
    tags = tuple(tag for tag in _split_tag_text(" ".join(parts[1:])) if tag != alias)
    if not alias or not tags:
        return {}
    return {"alias": alias, "tags": tags}


def _normalize_clarification_value(reply: str) -> str:
    value = reply.strip().strip("。！？!?.")
    patterns = (
        r"^(?:就是|是|用|补充|路径是|文件是|来源是|名称是|名字是|对象是|目录是|目录别名是|别名是|经验是|经验内容是|关键词是|查询是)\s*[:：]?\s*(?P<value>.+)$",
        r"^(?:请用|帮我用)\s*(?P<value>.+)$",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, value)
        if match:
            value = match.group("value").strip()
            break
    return _strip_wrapping_quotes(value)


def _clarification_tag_text(value: str, missing: tuple[str, ...]) -> str:
    tag_text = value.strip()
    if "result_index" in missing:
        tag_text = re.sub(
            r"^\s*(?:第)?[0-9一二两三四五六七八九十]+(?:条|个|份)?(?:资料|文档|文件|结果)?\s*[:：,，、]?\s*",
            "",
            tag_text,
        )
    tag_text = re.sub(r"^(?:标签是|标签为|打标签|标记为)\s*[:：]?\s*", "", tag_text)
    return tag_text.strip()


def _looks_like_path_or_file(value: str) -> bool:
    if not value:
        return False
    if re.match(r"^[a-zA-Z]:[/\\]", value):
        return True
    if value.startswith(("~/", "~\\", "./", ".\\", "../", "..\\")):
        return True
    if "/" in value or "\\" in value:
        return True
    return bool(re.search(r"\.(?:md|txt|pdf|json)$", value, flags=re.IGNORECASE))


def _extract_clarification_number(value: str) -> int:
    normalized = _normalize_text(value)
    return _extract_number(normalized, r"(?:第)?(?P<number>[0-9一二两三四五六七八九十]+)(?:条|个|份)?")


def _slot_is_present(slot: str, slots: Mapping[str, Any]) -> bool:
    if slot == "result_index":
        return _slot_result_index(slots) > 0
    if slot in {"items", "tags"}:
        value = slots.get(slot, ())
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, list | tuple):
            return any(str(item).strip() for item in value)
        return False
    value = slots.get(slot)
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list | tuple):
        return any(str(item).strip() for item in value)
    return bool(value)


def _extract_numbered_result_index(text: str, intent: str) -> int:
    normalized = _normalize_text(text)
    if intent in {"document.read_numbered_recent", "document.tag_numbered_recent"}:
        return _extract_number(normalized, r"第(?P<number>[0-9一二两三四五六七八九十]+)(?:条|个|份)?(?:资料|文档|文件)")
    if intent in {"recent_file.read_numbered", "recent_file.import_numbered"}:
        return _extract_number(normalized, r"第(?P<number>[0-9一二两三四五六七八九十]+)(?:条|个|份)?(?:最近文件|系统最近文件)")
    if intent in {"search_result.read_numbered", "search_result.tag_numbered"}:
        return _extract_number(normalized, r"第(?P<number>[0-9一二三四五六七八九十]+)(?:条|个)?结果")
    if intent == "web_search.open_numbered":
        return _extract_number(
            normalized,
            r"第(?P<number>[0-9一二两三四五六七八九十]+)(?:条|个)?(?:联网搜索结果|联网来源|搜索来源|来源)",
        )
    if intent in {"advice.read_numbered", "advice.execute_numbered"}:
        return _extract_number(normalized, r"第(?P<number>[0-9一二三四五六七八九十]+)(?:条|个)?建议")
    if intent == "tag_history.read_numbered":
        return _extract_number(normalized, r"第(?P<number>[0-9一二两三四五六七八九十]+)(?:条|个)?(?:批量标签历史|批量打标签历史|标签历史)(?:影响)?(?:资料|文档)")
    return 0


def _extract_number(text: str, pattern: str) -> int:
    match = re.search(pattern, text)
    if not match:
        return 0
    return _parse_positive_number(match.group("number"))


def _parse_positive_number(text: str) -> int:
    if text.isdigit():
        return int(text)
    mapping = {
        "一": 1,
        "二": 2,
        "两": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "十": 10,
    }
    return mapping.get(text, 0)


def _slot_result_index(slots: Mapping[str, Any]) -> int:
    raw_result_index = slots.get("result_index", 0)
    if isinstance(raw_result_index, int):
        return raw_result_index
    if isinstance(raw_result_index, str) and raw_result_index.isdigit():
        return int(raw_result_index)
    return 0


def _extract_file_path_slots(text: str, intent: str) -> dict[str, Any]:
    if intent == "document.read_path":
        path = _extract_read_document_path(text)
        if path:
            return {"path": path}
        return {}
    if intent == "knowledge.import":
        source = _extract_import_source(text)
        if source:
            return {"source": source}
        return {}
    return {}


def _extract_read_document_path(text: str) -> str:
    normalized = text.strip().strip("。！？!?.")
    match = re.fullmatch(r"(?:请)?(?:帮我)?(?:读取|查看|看看)\s*(?P<path>.+\.(?:md|txt))", normalized, flags=re.IGNORECASE)
    if not match:
        return ""
    return _normalize_read_document_path(match.group("path"))


def _normalize_read_document_path(path_text: str) -> str:
    path = _strip_wrapping_quotes(path_text.strip())
    path = path.replace("\\", "/").removeprefix("data/").lstrip("/")
    return path.strip()


def _extract_import_source(text: str) -> str:
    normalized = text.strip().strip("。！？!?.")
    patterns = (
        r"(?:请)?(?:帮我)?导入\s*(?P<source>.+?)\s*(?:到|进|加入)?\s*(?:知识库|资料库)",
        r"(?:请)?(?:帮我)?把\s*(?P<source>.+?)\s*(?:导入|加入|放进)\s*(?:到|进|加入|放进)?\s*(?:知识库|资料库)",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, normalized, flags=re.IGNORECASE)
        if not match:
            continue
        source = _strip_wrapping_quotes(match.group("source").strip())
        if source:
            return source
    return ""


def _extract_directory_slots(text: str, intent: str) -> dict[str, Any]:
    normalized = _normalize_text(text)
    if intent == "directory.open_drive":
        match = re.fullmatch(r"(?:帮我)?打开(?P<drive>[a-z])(?:盘)?", normalized)
        if not match:
            return {}
        drive = match.group("drive").upper()
        return {"alias": f"{drive}盘", "path": f"{drive}:/"}
    if intent in {"directory.open_alias", "directory.organize_alias"}:
        alias = _extract_directory_alias(text)
        if alias and not _is_recent_directory_reference(alias):
            return {"alias": alias}
        return {}
    return {}


def _extract_directory_alias(text: str) -> str:
    normalized = text.strip().strip("。！？!?.")
    patterns = (
        r"(?:帮我)?打开(?P<alias>.+?)(?:目录|文件夹)",
        r"(?:帮我)?(?:整理|整理预览|预览整理)(?P<alias>.+?)(?:目录|文件夹)",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, normalized)
        if not match:
            continue
        return _normalize_directory_alias(match.group("alias"))
    return ""


def _normalize_directory_alias(alias: str) -> str:
    return alias.strip().removesuffix("目录").removesuffix("文件夹").strip()


def _is_recent_directory_reference(alias: str) -> bool:
    return alias in {"这个", "刚才的", "最近的", "当前"}


def _extract_experience_slots(text: str, intent: str) -> dict[str, Any]:
    if intent == "experience.record":
        experience = _extract_experience_text(text)
        if experience:
            return {"experience": experience}
        return {}
    if intent == "experience.search":
        query = _extract_experience_search_query(text)
        if query:
            return {"query": query}
        return {}
    if intent == "experience.advice":
        query = _extract_experience_advice_query(text)
        if query:
            return {"query": query}
        return {}
    return {}


def _extract_experience_text(text: str) -> str:
    normalized = text.strip().strip("。！？!?.")
    patterns = (
        r"(?:请)?(?:帮我)?(?:记录|保存|沉淀)\s*(?:一条)?经验\s*[:：]?\s*(?P<experience>.+)",
        r"(?:请)?(?:帮我)?记住\s*(?:这个|这条)?经验\s*[:：]?\s*(?P<experience>.+)",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, normalized)
        if not match:
            continue
        experience = _strip_wrapping_quotes(match.group("experience").strip())
        if experience:
            return experience
    return ""


def _extract_experience_search_query(text: str) -> str:
    normalized = text.strip().strip("。！？!?.")
    patterns = (
        r"(?:请)?(?:帮我)?(?:搜索|查找|查询)\s*经验\s*[:：]?\s*(?P<query>.+)",
        r"(?:请)?(?:帮我)?经验\s*(?:搜索|查找|查询)\s*[:：]?\s*(?P<query>.+)",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, normalized)
        if not match:
            continue
        query = _strip_wrapping_quotes(match.group("query").strip())
        if query:
            return query
    return ""


def _extract_experience_advice_query(text: str) -> str:
    normalized = text.strip().strip("。！？!?.")
    patterns = (
        r"(?:我该怎么|我应该怎么|该怎么|如何|怎样)\s*(?P<query>.+)",
        r"(?P<query>.+?)\s*(?:有什么|有哪些|有啥)\s*(?:经验|建议)",
        r"(?:给我|请给我|帮我给)\s*(?P<query>.+?)\s*(?:的)?(?:经验建议|建议)",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, normalized)
        if not match:
            continue
        query = _strip_wrapping_quotes(match.group("query").strip())
        if query:
            return query
    return ""


def _extract_web_search_slots(text: str, intent: str) -> dict[str, Any]:
    if intent == "web.search":
        query = _extract_web_search_query(text)
        if query:
            return {"query": query}
        return {}
    if intent == "web.search_summarize":
        query = _extract_web_search_summary_query(text)
        if query:
            return {"query": query}
        return {}
    return {}


def _strip_wrapping_quotes(text: str) -> str:
    stripped = text.strip().strip("“”")
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {"'", '"'}:
        return stripped[1:-1].strip()
    return stripped


def _extract_tag_slots(text: str, intent: str) -> dict[str, Any]:
    normalized = text.strip().strip("。！？!?.")
    if intent == "document.tag_path":
        match = re.fullmatch(
            r"(?:给|把)\s*(?P<path>.+?\.(?:md|txt))\s*(?:打标签|标记为)\s*(?P<tags>.+)",
            normalized,
            flags=re.IGNORECASE,
        )
        if not match:
            return {}
        path = _normalize_read_document_path(match.group("path"))
        tags = _split_tag_text(match.group("tags"))
        if path and tags:
            return {"path": path, "tags": tags}
        return {}
    if intent == "document.tag_recent":
        match = re.fullmatch(
            r"(?:给|把)\s*(?:这个|这份|刚才的|最近的|当前)(?:资料|文档|文件|结果)\s*(?:打标签|标记为)\s*(?P<tags>.+)",
            normalized,
        )
        return _tag_slots_from_match(match)
    if intent == "document.tag_numbered_recent":
        match = re.fullmatch(
            r"(?:给|把)\s*第[0-9一二两三四五六七八九十]+(?:条|个|份)?(?:资料|文档|文件)\s*(?:打标签|标记为)\s*(?P<tags>.+)",
            normalized,
        )
        return _tag_slots_from_match(match)
    if intent == "search_result.tag_numbered":
        match = re.fullmatch(
            r"(?:给|把)\s*第[0-9一二三四五六七八九十]+(?:条|个)?结果\s*(?:打标签|标记为)\s*(?P<tags>.+)",
            normalized,
        )
        return _tag_slots_from_match(match)
    if intent == "tag_group.preview_tagging":
        match = re.fullmatch(
            r"(?:请)?(?:帮我)?(?:给|把)\s*(?P<alias>.+?)\s*标签(?:资料|文档)(?:都|全部)?\s*(?:打标签|标记为)\s*(?P<tags>.+)",
            normalized,
        )
        if not match:
            return {}
        tags = _split_tag_text(match.group("tags"))
        alias = match.group("alias").strip()
        if alias and tags:
            return {"alias": alias, "tags": tags}
        return {}
    if intent == "tag_group.read":
        match = re.fullmatch(r"(?:请)?(?:帮我)?(?:读取|查看|看看)\s*(?P<alias>.+?)\s*标签(?:资料|文档)", normalized)
        if not match:
            return {}
        alias = match.group("alias").strip()
        if alias:
            return {"alias": alias}
        return {}
    return {}


def _tag_slots_from_match(match: re.Match[str] | None) -> dict[str, Any]:
    if not match:
        return {}
    tags = _split_tag_text(match.group("tags"))
    if tags:
        return {"tags": tags}
    return {}


def _split_tag_text(text: str) -> tuple[str, ...]:
    tags: list[str] = []
    for raw_tag in re.split(r"[\s,，、]+", text.strip()):
        tag = raw_tag.strip().lstrip("#").strip()
        if tag:
            tags.append(tag)
    return tuple(tags)


def _slot_tags(slots: Mapping[str, Any]) -> tuple[str, ...]:
    raw_tags = slots.get("tags", ())
    if isinstance(raw_tags, str):
        return (raw_tags,) if raw_tags.strip() else ()
    if isinstance(raw_tags, list | tuple):
        return tuple(str(tag).strip() for tag in raw_tags if str(tag).strip())
    return ()


def _slot_alias(slots: Mapping[str, Any]) -> str:
    raw_alias = slots.get("alias", "")
    if isinstance(raw_alias, str):
        return raw_alias.strip()
    return ""


def _slot_path(slots: Mapping[str, Any]) -> str:
    raw_path = slots.get("path", "")
    if isinstance(raw_path, str):
        return raw_path.strip()
    return ""


def _slot_text(slots: Mapping[str, Any], key: str) -> str:
    raw_text = slots.get(key, "")
    if isinstance(raw_text, str):
        return raw_text.strip()
    return ""


def _normalized_slots(slots: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in slots.items():
        if isinstance(value, list):
            normalized[key] = tuple(value)
        else:
            normalized[key] = value
    return normalized


def _inner_brain_result_slot_lines(result: InnerBrainResult) -> list[str]:
    lines: list[str] = []
    command = result.slots.get("command")
    if not command and result.natural_language_intent is not None:
        command = result.natural_language_intent.command
    if command:
        lines.append(f"- 命令：{command}")

    items = result.slots.get("items", ())
    if not items and result.natural_language_intent is not None:
        items = result.natural_language_intent.items
    if isinstance(items, str):
        items = (items,)
    if isinstance(items, tuple):
        item_text = "、".join(str(item) for item in items if str(item).strip())
        if item_text:
            lines.append(f"- 对象：{item_text}")

    tags = result.slots.get("tags", ())
    if not tags and result.natural_language_intent is not None:
        tags = result.natural_language_intent.tags
    if isinstance(tags, str):
        tags = (tags,)
    if isinstance(tags, tuple):
        tag_text = "、".join(str(tag) for tag in tags if str(tag).strip())
        if tag_text:
            lines.append(f"- 标签：{tag_text}")

    alias = result.slots.get("alias")
    if alias:
        lines.append(f"- 别名：{alias}")
    path = result.slots.get("path")
    if path:
        lines.append(f"- 路径：{path}")
    result_index = result.slots.get("result_index")
    if result_index:
        lines.append(f"- 编号：{result_index}")
    return lines


def _slots_from_natural_language_intent(intent: NaturalLanguageIntent) -> dict[str, Any]:
    slots: dict[str, Any] = {}
    if intent.command:
        slots["command"] = intent.command
    if intent.alias:
        slots["alias"] = intent.alias
    if intent.path is not None:
        slots["path"] = str(intent.path)
    if intent.tags:
        slots["tags"] = intent.tags
    if intent.items:
        slots["items"] = intent.items
    if intent.result_index:
        slots["result_index"] = intent.result_index
    return slots


def _legacy_intent_label(intent: NaturalLanguageIntent) -> str:
    if intent.name == "greeting":
        return "assistant.greeting"
    if intent.name == "assistant_identity":
        return "assistant.identity"
    if intent.name == "capabilities":
        return "assistant.capabilities"
    if intent.name == "recent_context_status":
        return "context.recent_status"
    if intent.name == "recent_files_status":
        return "context.recent_files"
    if intent.name == "delete_desktop_shortcuts":
        return "desktop.delete_shortcut"
    if intent.name == "command":
        command_labels = {
            "/kb-summary": "knowledge.summary",
            "/kb": "knowledge.status",
            "/dirs": "directory.list",
            "/daily-report": "report.daily",
            "/update-status": "update.status",
            "/update-download": "update.download",
            "/experiences": "experience.status",
            "/tag-history": "tag.history",
        }
        return command_labels.get(intent.command, "command")
    return f"legacy.{intent.name}"


def _no_match(reason: str, confidence: float = 0.0) -> InnerBrainResult:
    return InnerBrainResult(
        intent="unknown",
        slots={},
        confidence=confidence,
        missing=(),
        source="no_match",
        reason=reason,
        policy=InnerBrainPolicy.FALLBACK_TO_LLM,
    )
