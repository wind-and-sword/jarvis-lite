from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .config import ProjectPaths


SUPPORTED_TEXT_SUFFIXES = {".md", ".txt"}


@dataclass(frozen=True)
class DataMatch:
    relative_path: str
    line_number: int
    text: str
    score: int


def search_data(paths: ProjectPaths, query: str, limit: int = 3) -> list[DataMatch]:
    """在 data 目录中查找和问题相关的文本行。"""

    terms = _query_terms(query)
    if not terms:
        return []

    matches: list[DataMatch] = []
    for file_path in _iter_text_files(paths.data_dir):
        relative_path = file_path.relative_to(paths.data_dir).as_posix()
        for line_number, raw_line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
            text = raw_line.strip()
            if not text:
                continue
            if text.startswith("#"):
                continue
            score = _score(text, terms)
            if score > 0:
                matches.append(
                    DataMatch(
                        relative_path=relative_path,
                        line_number=line_number,
                        text=text,
                        score=score,
                    )
                )

    return sorted(matches, key=lambda item: (-item.score, item.relative_path, item.line_number))[:limit]


def answer_from_data(paths: ProjectPaths, question: str) -> str:
    """基于 data 目录命中的片段生成规则式回答；无命中时返回空字符串。"""

    matches = _filter_weak_matches(search_data(paths, question))
    if not matches:
        return ""

    lines = []
    for match in matches:
        lines.append(f"根据 data/{match.relative_path}:{match.line_number}，{match.text}")
    return "\n".join(lines)


def _iter_text_files(data_dir: Path) -> list[Path]:
    files: list[Path] = []
    for file_path in data_dir.rglob("*"):
        if not file_path.is_file():
            continue
        if any(part.startswith(".") for part in file_path.relative_to(data_dir).parts):
            continue
        if file_path.suffix.lower() not in SUPPORTED_TEXT_SUFFIXES:
            continue
        files.append(file_path)
    return sorted(files, key=lambda item: item.relative_to(data_dir).as_posix().lower())


def _query_terms(query: str) -> set[str]:
    normalized = query.lower()
    terms = {match.group(0) for match in re.finditer(r"[a-z0-9][a-z0-9._-]*", normalized)}

    cjk_chars = re.findall(r"[\u4e00-\u9fff]", normalized)
    for index in range(len(cjk_chars) - 1):
        terms.add("".join(cjk_chars[index : index + 2]))

    return {term for term in terms if len(term) >= 2}


def _score(text: str, terms: set[str]) -> int:
    normalized = text.lower()
    return sum(1 for term in terms if term in normalized)


def _filter_weak_matches(matches: list[DataMatch]) -> list[DataMatch]:
    if not matches:
        return []

    best_score = matches[0].score
    minimum_score = max(1, best_score - 1)
    return [match for match in matches if match.score >= minimum_score]
