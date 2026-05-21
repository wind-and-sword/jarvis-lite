from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class NaturalLanguageIntent:
    """表示本地大脑识别出的自然语言意图。"""

    name: str
    command: str = ""
    alias: str = ""
    path: Path | None = None


def parse_natural_language_intent(text: str) -> NaturalLanguageIntent | None:
    """把常见中文表达映射为可测试的本地动作。"""

    prompt = _normalize_text(text)
    if not prompt:
        return None

    if _is_capability_question(prompt):
        return NaturalLanguageIntent("capabilities")
    if _matches_any(prompt, ("查看知识库", "看看知识库", "知识库状态", "我的知识库", "资料库状态")):
        return NaturalLanguageIntent("command", command="/kb")
    if _matches_any(prompt, ("查看常用目录", "看看常用目录", "常用目录", "目录列表")):
        return NaturalLanguageIntent("command", command="/dirs")
    if _matches_any(prompt, ("生成日报", "写日报", "创建日报", "今天日报", "生成今天日报", "帮我生成日报")):
        return NaturalLanguageIntent("command", command="/daily-report")
    if _matches_any(prompt, ("检查更新", "查看更新", "有没有更新", "看看更新")):
        return NaturalLanguageIntent("command", command="/update-status")
    if _matches_any(prompt, ("下载更新", "下载新版本", "下载最新版", "下载更新安装包")):
        return NaturalLanguageIntent("command", command="/update-download")

    drive_intent = _parse_open_drive(prompt)
    if drive_intent is not None:
        return drive_intent

    alias_intent = _parse_directory_alias_intent(prompt)
    if alias_intent is not None:
        return alias_intent

    return None


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text.strip().strip("。！？!?."))


def _is_capability_question(prompt: str) -> bool:
    capability_words = ("能做什么", "可以做什么", "会做什么", "能干什么", "有什么功能", "能帮我做什么")
    return any(word in prompt for word in capability_words)


def _matches_any(prompt: str, candidates: tuple[str, ...]) -> bool:
    return prompt in candidates


def _parse_open_drive(prompt: str) -> NaturalLanguageIntent | None:
    match = re.fullmatch(r"(?:帮我)?打开([a-zA-Z])(?:盘|:|：)?", prompt)
    if not match:
        return None
    drive_letter = match.group(1).upper()
    return NaturalLanguageIntent(
        "open_directory_path",
        alias=f"{drive_letter}盘",
        path=Path(f"{drive_letter}:/"),
    )


def _parse_directory_alias_intent(prompt: str) -> NaturalLanguageIntent | None:
    open_match = re.fullmatch(r"(?:帮我)?打开(.+?)(?:目录|文件夹)?", prompt)
    if open_match:
        alias = _normalize_directory_alias(open_match.group(1))
        if alias:
            return NaturalLanguageIntent("open_directory_alias", alias=alias)

    organize_match = re.fullmatch(r"(?:帮我)?(?:整理|整理预览|预览整理)(.+?)(?:目录|文件夹)?", prompt)
    if organize_match:
        alias = _normalize_directory_alias(organize_match.group(1))
        if alias:
            return NaturalLanguageIntent("organize_directory_alias", alias=alias)

    return None


def _normalize_directory_alias(alias: str) -> str:
    return alias.strip().removesuffix("目录").removesuffix("文件夹").strip()
