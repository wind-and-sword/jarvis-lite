from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .config import ProjectPaths


SUPPORTED_TEXT_SUFFIXES = {".md", ".txt"}
TAG_METADATA_FILENAME = ".knowledge-tags.json"


@dataclass(frozen=True)
class DataMatch:
    relative_path: str
    line_number: int
    text: str
    score: int


@dataclass(frozen=True)
class KnowledgeDocument:
    relative_path: str
    searchable_line_count: int
    tags: tuple[str, ...] = ()


@dataclass(frozen=True)
class KnowledgeIndex:
    documents: tuple[KnowledgeDocument, ...]

    @property
    def document_count(self) -> int:
        return len(self.documents)

    @property
    def searchable_line_count(self) -> int:
        return sum(document.searchable_line_count for document in self.documents)


@dataclass(frozen=True)
class KnowledgeImportSummary:
    documents: tuple[KnowledgeDocument, ...]
    skipped_count: int = 0

    @property
    def imported_count(self) -> int:
        return len(self.documents)

    @property
    def searchable_line_count(self) -> int:
        return sum(document.searchable_line_count for document in self.documents)

    @property
    def scanned_count(self) -> int:
        return self.imported_count + self.skipped_count


def search_data(paths: ProjectPaths, query: str, limit: int = 3) -> list[DataMatch]:
    """在 data 目录中查找和问题相关的文本行。"""

    terms = _query_terms(query)
    if not terms:
        return []

    metadata = _read_tag_metadata(paths)
    matches: list[DataMatch] = []
    for file_path in _iter_text_files(paths.data_dir):
        relative_path = file_path.relative_to(paths.data_dir).as_posix()
        tags = _document_tags(relative_path, metadata)
        for line_number, raw_line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
            text = raw_line.strip()
            if not text:
                continue
            if text.startswith("#"):
                continue
            score = _score(text, terms) + _score(" ".join(tags), terms)
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

    lines = [f"我在 data 目录找到 {len(matches)} 条相关资料："]
    for index, match in enumerate(matches, start=1):
        lines.append(f"{index}. 根据 data/{match.relative_path}:{match.line_number}，{match.text}")
    return "\n".join(lines)


def build_knowledge_index(paths: ProjectPaths) -> KnowledgeIndex:
    """构建本地个人知识库索引，用于查看 data 目录当前可检索状态。"""

    metadata = _read_tag_metadata(paths)
    documents = []
    for file_path in _iter_text_files(paths.data_dir):
        relative_path = file_path.relative_to(paths.data_dir).as_posix()
        documents.append(
            KnowledgeDocument(
                relative_path=relative_path,
                searchable_line_count=len(_searchable_lines(file_path)),
                tags=_document_tags(relative_path, metadata),
            )
        )
    return KnowledgeIndex(tuple(documents))


def describe_knowledge_base(paths: ProjectPaths) -> str:
    """输出给用户阅读的个人知识库状态摘要。"""

    index = build_knowledge_index(paths)
    lines = [
        "个人知识库状态：",
        "- 根目录：data",
        f"- 支持格式：{'、'.join(sorted(SUPPORTED_TEXT_SUFFIXES))}",
        f"- 资料文件：{index.document_count} 个",
        f"- 可检索文本行：{index.searchable_line_count} 行",
    ]

    if not index.documents:
        lines.append("- 资料列表：还没有可检索资料。")
        return "\n".join(lines)

    tags = sorted({tag for document in index.documents for tag in document.tags})
    if tags:
        lines.append(f"- 标签列表：{'、'.join(tags)}")
    else:
        lines.append("- 标签列表：还没有标签。")

    lines.append("- 资料列表：")
    for document in index.documents:
        tag_text = f"，标签：{'、'.join(document.tags)}" if document.tags else ""
        lines.append(f"  - data/{document.relative_path}（{document.searchable_line_count} 行{tag_text}）")
    return "\n".join(lines)


def import_knowledge_file(paths: ProjectPaths, source_path: str | Path, target_name: str | None = None) -> KnowledgeDocument:
    """把外部 Markdown 或 txt 文件导入 data 目录，供知识库检索。"""

    source = Path(source_path).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"源文件不存在：{source_path}")
    if source.suffix.lower() not in SUPPORTED_TEXT_SUFFIXES:
        raise ValueError(f"仅支持导入这些格式：{', '.join(sorted(SUPPORTED_TEXT_SUFFIXES))}")

    name = _target_filename(source, target_name)
    if Path(name).suffix.lower() not in SUPPORTED_TEXT_SUFFIXES:
        raise ValueError(f"目标文件必须是这些格式：{', '.join(sorted(SUPPORTED_TEXT_SUFFIXES))}")

    target = paths.data_dir / name
    if target.exists():
        raise FileExistsError(f"目标文件已存在：data/{name}")

    content = source.read_text(encoding="utf-8")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return KnowledgeDocument(
        relative_path=target.relative_to(paths.data_dir).as_posix(),
        searchable_line_count=len(_searchable_lines(target)),
    )


def import_knowledge_path(paths: ProjectPaths, source_path: str | Path, target_name: str | None = None) -> KnowledgeImportSummary:
    """导入单个资料文件，或递归导入目录中的 Markdown/txt 资料。"""

    source = Path(source_path).expanduser().resolve()
    if source.is_file():
        return KnowledgeImportSummary((import_knowledge_file(paths, source, target_name),))
    if not source.is_dir():
        raise FileNotFoundError(f"源路径不存在：{source_path}")
    if target_name:
        raise ValueError("导入目录时不能指定目标文件名。")

    imported: list[KnowledgeDocument] = []
    skipped_count = 0
    for file_path in _iter_import_source_files(source):
        relative_path = file_path.relative_to(source).as_posix()
        if _has_hidden_part(file_path, source) or file_path.suffix.lower() not in SUPPORTED_TEXT_SUFFIXES:
            skipped_count += 1
            continue
        imported.append(import_knowledge_file(paths, file_path, relative_path))

    return KnowledgeImportSummary(tuple(imported), skipped_count)


def set_document_tags(paths: ProjectPaths, relative_path: str, tags: list[str] | tuple[str, ...]) -> KnowledgeDocument:
    """为 data 目录中的资料设置标签，供知识库展示和检索使用。"""

    document_path = _resolve_data_document(paths, relative_path)
    normalized_tags = _normalize_tags(tags)
    if not normalized_tags:
        raise ValueError("标签不能为空。")

    metadata = _read_tag_metadata(paths)
    document_key = document_path.relative_to(paths.data_dir).as_posix()
    metadata[document_key] = list(normalized_tags)
    _write_tag_metadata(paths, metadata)

    return KnowledgeDocument(
        relative_path=document_key,
        searchable_line_count=len(_searchable_lines(document_path)),
        tags=normalized_tags,
    )


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


def _iter_import_source_files(source_dir: Path) -> list[Path]:
    files: list[Path] = []
    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue
        files.append(file_path)
    return sorted(files, key=lambda item: item.relative_to(source_dir).as_posix().lower())


def _target_filename(source: Path, target_name: str | None) -> str:
    if target_name is None:
        return source.name

    name = target_name.strip().replace("\\", "/").lstrip("/")
    if not name:
        raise ValueError("目标文件名不能为空。")
    if ".." in Path(name).parts:
        raise ValueError("目标文件名不能包含上级目录。")
    if not Path(name).suffix:
        return f"{name}{source.suffix.lower()}"
    return name


def _resolve_data_document(paths: ProjectPaths, relative_path: str) -> Path:
    name = relative_path.strip().replace("\\", "/").lstrip("/")
    if not name:
        raise ValueError("资料文件名不能为空。")
    if ".." in Path(name).parts:
        raise ValueError("资料文件名不能包含上级目录。")
    if any(part.startswith(".") for part in Path(name).parts):
        raise ValueError("不能给隐藏资料设置标签。")
    if Path(name).suffix.lower() not in SUPPORTED_TEXT_SUFFIXES:
        raise ValueError(f"仅支持这些资料格式：{', '.join(sorted(SUPPORTED_TEXT_SUFFIXES))}")

    target = (paths.data_dir / name).resolve()
    if not target.is_file():
        raise FileNotFoundError(f"资料不存在：data/{name}")
    return target


def _has_hidden_part(file_path: Path, base_dir: Path) -> bool:
    return any(part.startswith(".") for part in file_path.relative_to(base_dir).parts)


def _searchable_lines(file_path: Path) -> list[str]:
    lines = []
    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        text = raw_line.strip()
        if not text:
            continue
        if text.startswith("#"):
            continue
        lines.append(text)
    return lines


def _tag_metadata_path(paths: ProjectPaths) -> Path:
    return paths.data_dir / TAG_METADATA_FILENAME


def _read_tag_metadata(paths: ProjectPaths) -> dict[str, list[str]]:
    metadata_path = _tag_metadata_path(paths)
    if not metadata_path.exists():
        return {}

    raw = json.loads(metadata_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}

    metadata: dict[str, list[str]] = {}
    for relative_path, tags in raw.items():
        if isinstance(relative_path, str) and isinstance(tags, list):
            metadata[relative_path] = [tag for tag in tags if isinstance(tag, str)]
    return metadata


def _write_tag_metadata(paths: ProjectPaths, metadata: dict[str, list[str]]) -> None:
    metadata_path = _tag_metadata_path(paths)
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _document_tags(relative_path: str, metadata: dict[str, list[str]]) -> tuple[str, ...]:
    return tuple(metadata.get(relative_path, ()))


def _normalize_tags(tags: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    normalized: list[str] = []
    for raw_tag in tags:
        for part in re.split(r"[,，]", raw_tag):
            tag = part.strip().lstrip("#").strip()
            if not tag:
                continue
            if tag not in normalized:
                normalized.append(tag)
    return tuple(normalized)


def _query_terms(query: str) -> set[str]:
    normalized = query.lower()
    terms = {match.group(0) for match in re.finditer(r"[a-z0-9][a-z0-9._-]*", normalized)}

    cjk_chars = re.findall(r"[\u4e00-\u9fff]", normalized)
    for index in range(len(cjk_chars) - 1):
        terms.add("".join(cjk_chars[index : index + 2]))

    return {term for term in terms if len(term) >= 2}


def _score(text: str, terms: set[str]) -> int:
    normalized = text.lower()
    return sum(_term_weight(term) for term in terms if term in normalized)


def _term_weight(term: str) -> int:
    if any(char.isdigit() for char in term):
        return 3
    return 1


def _filter_weak_matches(matches: list[DataMatch]) -> list[DataMatch]:
    if not matches:
        return []

    best_score = matches[0].score
    minimum_score = max(1, best_score - 1)
    return [match for match in matches if match.score >= minimum_score]
