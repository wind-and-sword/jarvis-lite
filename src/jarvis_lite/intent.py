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
    tags: tuple[str, ...] = ()
    result_index: int = 0


def parse_natural_language_intent(text: str) -> NaturalLanguageIntent | None:
    """把常见中文表达映射为可测试的本地动作。"""

    readable_prompt = _normalize_text_preserving_spaces(text)
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

    import_intent = _parse_import_intent(readable_prompt)
    if import_intent is not None:
        return import_intent

    tag_intent = _parse_tag_intent(readable_prompt)
    if tag_intent is not None:
        return tag_intent

    drive_intent = _parse_open_drive(prompt)
    if drive_intent is not None:
        return drive_intent

    alias_intent = _parse_directory_alias_intent(prompt)
    if alias_intent is not None:
        return alias_intent

    return None


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text.strip().strip("。！？!?."))


def _normalize_text_preserving_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().strip("。！？!?."))


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


def _parse_tag_intent(prompt: str) -> NaturalLanguageIntent | None:
    match = re.fullmatch(r"(?:给|把)\s*(?P<filename>\S+)\s*(?:打标签|标记为)\s*(?P<tags>.+)", prompt)
    if not match:
        return None

    filename = match.group("filename").strip()
    tags = _split_tag_text(match.group("tags"))
    if not filename or not tags:
        return None
    result_index = _parse_result_index(filename)
    if result_index > 0:
        return NaturalLanguageIntent("tag_numbered_search_result", tags=tags, result_index=result_index)
    if filename in {"这个资料", "这份资料", "刚才的资料", "最近的资料", "这个结果", "这条结果", "刚才的结果", "最近的结果"}:
        return NaturalLanguageIntent("tag_recent_document", tags=tags)
    return NaturalLanguageIntent("command", command=f"/tag {filename} {' '.join(tags)}")


def _parse_import_intent(prompt: str) -> NaturalLanguageIntent | None:
    patterns = (
        r"(?:请)?(?:帮我)?导入\s*(?P<source>.+?)\s*(?:到|进|加入)?\s*(?:知识库|资料库)",
        r"(?:请)?(?:帮我)?把\s*(?P<source>.+?)\s*(?:导入|加入|放进)\s*(?:知识库|资料库)",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, prompt)
        if not match:
            continue
        source = _strip_wrapping_quotes(match.group("source").strip())
        if source:
            return NaturalLanguageIntent("command", command=f'/import "{source}"')
    return None


def _parse_directory_alias_intent(prompt: str) -> NaturalLanguageIntent | None:
    open_match = re.fullmatch(r"(?:帮我)?打开(.+?)(?:目录|文件夹)?", prompt)
    if open_match:
        alias = _normalize_directory_alias(open_match.group(1))
        if alias:
            if _is_recent_directory_reference(alias):
                return NaturalLanguageIntent("open_recent_directory")
            return NaturalLanguageIntent("open_directory_alias", alias=alias)

    organize_match = re.fullmatch(r"(?:帮我)?(?:整理|整理预览|预览整理)(.+?)(?:目录|文件夹)?", prompt)
    if organize_match:
        alias = _normalize_directory_alias(organize_match.group(1))
        if alias:
            if _is_recent_directory_reference(alias):
                return NaturalLanguageIntent("organize_recent_directory")
            return NaturalLanguageIntent("organize_directory_alias", alias=alias)

    return None


def _normalize_directory_alias(alias: str) -> str:
    return alias.strip().removesuffix("目录").removesuffix("文件夹").strip()


def _is_recent_directory_reference(alias: str) -> bool:
    return alias in {"这个", "刚才的", "最近的", "当前"}


def _split_tag_text(text: str) -> tuple[str, ...]:
    tags: list[str] = []
    for raw_tag in re.split(r"[\s,，、]+", text.strip()):
        tag = raw_tag.strip().lstrip("#").strip()
        if tag:
            tags.append(tag)
    return tuple(tags)


def _parse_result_index(text: str) -> int:
    match = re.fullmatch(r"第(?P<number>[0-9一二三四五六七八九十]+)(?:条|个)?结果", text)
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


def _strip_wrapping_quotes(text: str) -> str:
    stripped = text.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in {"'", '"'}:
        return stripped[1:-1].strip()
    return stripped
