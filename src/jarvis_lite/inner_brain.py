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


class InnerBrain:
    """本地轻量内脑，负责把自然语言转成可审计的结构化意图。"""

    def __init__(self, paths: ProjectPaths | None = None, samples: tuple[InnerBrainTrainingSample, ...] | None = None):
        self.paths = paths
        self.samples = samples or (*seed_training_samples(), *load_training_samples(paths))

    def understand(self, text: str) -> InnerBrainResult:
        prompt = text.strip()
        if not prompt:
            return _no_match("输入为空")

        legacy_intent = parse_natural_language_intent(prompt)
        if legacy_intent is not None:
            return self._legacy_result(legacy_intent)

        sample, confidence = self._best_sample(prompt)
        if sample is None or confidence < MEDIUM_CONFIDENCE:
            reason = "没有命中 legacy 规则或训练样本"
            if sample is not None:
                reason = f"最高相似样本 {sample.intent} 置信度 {confidence:.2f} 低于阈值"
            return _no_match(reason, confidence)

        return self._sample_result(prompt, sample, confidence)

    def describe_status(self) -> str:
        source_counts: dict[str, int] = {}
        for sample in self.samples:
            source_counts[sample.source] = source_counts.get(sample.source, 0) + 1
        training_dir = self._training_dir_label()
        return "\n".join(
            [
                "InnerBrain 状态：",
                "- legacy_rule：启用",
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

    def _legacy_result(self, intent: NaturalLanguageIntent) -> InnerBrainResult:
        slots = _slots_from_natural_language_intent(intent)
        return InnerBrainResult(
            intent=_legacy_intent_label(intent),
            slots=slots,
            confidence=1.0,
            missing=(),
            source="legacy_rule",
            reason=f"现有自然语言规则命中：{intent.name}",
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
        slots = _normalized_slots(sample.slots)
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
        InnerBrainTrainingSample("麻烦看一下知识库摘要", "knowledge.summary", {"command": "/kb-summary"}),
        InnerBrainTrainingSample("知识库摘要", "knowledge.summary", {"command": "/kb-summary"}),
        InnerBrainTrainingSample("查看知识库", "knowledge.status", {"command": "/kb"}),
        InnerBrainTrainingSample("请看看资料库状态", "knowledge.status", {"command": "/kb"}),
        InnerBrainTrainingSample("你叫什么名字", "assistant.identity", {}),
        InnerBrainTrainingSample("早上好", "assistant.greeting", {}),
        InnerBrainTrainingSample("你好", "assistant.greeting", {}),
        InnerBrainTrainingSample("开启外脑", "llm.enable", {"command": "/llm-enable"}),
        InnerBrainTrainingSample("连接外脑", "llm.enable", {"command": "/llm-enable"}),
        InnerBrainTrainingSample("把桌面{item}快捷方式删除", "desktop.delete_shortcut", {}),
        InnerBrainTrainingSample("删除桌面{item}快捷方式", "desktop.delete_shortcut", {}),
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
    return _dice_similarity(_features(prompt_text), _features(sample_text))


def _similarity_text(text: str, intent: str) -> str:
    normalized = _normalize_text(text)
    if intent == "desktop.delete_shortcut":
        return _desktop_shortcut_signature(normalized)
    return normalized


def _normalize_text(text: str) -> str:
    return re.sub(r"[\s。！？!?.,，、：:；;“”\"'（）()]+", "", text.strip().lower())


def _desktop_shortcut_signature(text: str) -> str:
    patterns = (
        r"(?:请|帮我|麻烦)?(?:把)?桌面(?:上|上的)?(?P<item>.+?)快捷方式(?:删除|删掉|移除)",
        r"(?:请|帮我|麻烦)?(?:删除|删掉|移除)桌面(?:上|上的)?(?P<item>.+?)快捷方式",
    )
    for pattern in patterns:
        if re.fullmatch(pattern, text):
            if text.startswith(("删除", "删掉", "移除")):
                return "删除桌面{item}快捷方式"
            return "把桌面{item}快捷方式删除"
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


def _sample_to_natural_language_intent(
    prompt: str,
    sample: InnerBrainTrainingSample,
    slots: Mapping[str, Any],
) -> NaturalLanguageIntent | None:
    if sample.intent == "knowledge.summary":
        return NaturalLanguageIntent("command", command=str(slots.get("command") or "/kb-summary"))
    if sample.intent == "knowledge.status":
        return NaturalLanguageIntent("command", command=str(slots.get("command") or "/kb"))
    if sample.intent == "assistant.identity":
        return NaturalLanguageIntent("assistant_identity")
    if sample.intent == "assistant.greeting":
        return NaturalLanguageIntent("greeting", alias=prompt.strip())
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
    command = slots.get("command")
    if isinstance(command, str) and command.strip().startswith("/"):
        return NaturalLanguageIntent("command", command=command.strip())
    return None


def _extract_desktop_shortcut_items(text: str) -> tuple[str, ...]:
    normalized = text.strip().strip("。！？!?.")
    patterns = (
        r"(?:请|帮我|麻烦)?(?:把)?桌面(?:上|上的)?(?P<items>.+?)快捷方式(?:删除|删掉|移除)",
        r"(?:请|帮我|麻烦)?(?:删除|删掉|移除)桌面(?:上|上的)?(?P<items>.+?)快捷方式",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, normalized)
        if not match:
            continue
        return _split_shortcut_items(match.group("items"))
    return ()


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
