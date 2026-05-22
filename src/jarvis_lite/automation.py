from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from .config import ProjectPaths
from .knowledge import build_knowledge_index
from .memory import list_recent_experiences, read_profile, summarize_profile
from .runtime_context import RuntimeContext, load_runtime_context


DIRECTORIES_FILENAME = "directories.json"


@dataclass(frozen=True)
class CommonDirectory:
    alias: str
    path: Path


@dataclass(frozen=True)
class DailyReport:
    path: Path
    relative_path: str


@dataclass(frozen=True)
class DirectoryOpenRecord:
    path: Path
    relative_path: str


@dataclass(frozen=True)
class FileOrganizationGroup:
    extension_label: str
    target_folder: str
    files: tuple[str, ...]


@dataclass(frozen=True)
class FileOrganizationPreview:
    directory: Path
    groups: tuple[FileOrganizationGroup, ...]
    skipped_directory_count: int

    @property
    def file_count(self) -> int:
        return sum(len(group.files) for group in self.groups)


@dataclass(frozen=True)
class RecentFile:
    alias: str
    path: Path
    modified_at: datetime


def describe_automation(paths: ProjectPaths) -> str:
    """输出阶段 4 工作台自动化状态。"""

    directories = list_common_directories(paths)
    lines = [
        "阶段 4 自动化状态：",
        f"- 常用目录：{len(directories)} 个",
        "- 日报目录：word",
        "- 当前能力：/dir-add、/dirs、/recent-files、/daily-report、/organize-preview、/dir-open",
        "- 硬件入口：摄像头、麦克风暂缓",
    ]
    if directories:
        lines.append("- 常用目录列表：")
        for directory in directories:
            lines.append(f"  - {directory.alias}：{directory.path}")
    return "\n".join(lines)


def add_common_directory(paths: ProjectPaths, alias: str, directory: str | Path) -> CommonDirectory:
    """登记常用目录，供后续桌面自动化复用。"""

    normalized_alias = _normalize_alias(alias)
    target = Path(directory).expanduser().resolve()
    if not target.is_dir():
        raise FileNotFoundError(f"目录不存在：{directory}")

    registry = _read_directories(paths)
    registry[normalized_alias] = str(target)
    _write_directories(paths, registry)
    return CommonDirectory(normalized_alias, target)


def list_common_directories(paths: ProjectPaths) -> tuple[CommonDirectory, ...]:
    """读取已登记的常用目录。"""

    registry = _read_directories(paths)
    directories = [
        CommonDirectory(alias=alias, path=Path(directory_path))
        for alias, directory_path in sorted(registry.items(), key=lambda item: item[0].lower())
    ]
    return tuple(directories)


def write_daily_report(paths: ProjectPaths, filename: str | None = None) -> DailyReport:
    """生成工作日报到 word 目录。"""

    target = paths.word_dir / _report_filename(filename)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_daily_report_content(paths), encoding="utf-8")
    return DailyReport(target, target.relative_to(paths.root).as_posix())


def record_directory_open_request(paths: ProjectPaths, alias: str, directory: str | Path) -> DirectoryOpenRecord:
    """记录打开常用目录的请求，当前不启动外部应用。"""

    target = Path(directory).expanduser().resolve()
    if not target.is_dir():
        raise FileNotFoundError(f"目录不存在：{directory}")

    transcript_path = paths.logs_dir / "desktop-actions.txt"
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')}\topen_directory\t{alias}\t{target}\n"
    with transcript_path.open("a", encoding="utf-8") as file:
        file.write(line)
    return DirectoryOpenRecord(transcript_path, transcript_path.relative_to(paths.root).as_posix())


def preview_file_organization(directory: str | Path) -> FileOrganizationPreview:
    """按扩展名生成文件整理预览，不移动或删除文件。"""

    target = Path(directory).expanduser().resolve()
    if not target.is_dir():
        raise FileNotFoundError(f"目录不存在：{directory}")

    grouped_files: dict[tuple[str, str], list[str]] = {}
    skipped_directory_count = 0
    for item in sorted(target.iterdir(), key=lambda path: path.name.lower()):
        if item.is_dir():
            skipped_directory_count += 1
            continue
        if not item.is_file():
            continue
        extension_label, target_folder = _organization_bucket(item)
        grouped_files.setdefault((extension_label, target_folder), []).append(item.name)

    groups = tuple(
        FileOrganizationGroup(extension_label=label, target_folder=folder, files=tuple(files))
        for (label, folder), files in sorted(grouped_files.items(), key=lambda item: item[0][1])
    )
    return FileOrganizationPreview(target, groups, skipped_directory_count)


def list_recent_files(directories: tuple[CommonDirectory, ...], limit: int = 5) -> tuple[RecentFile, ...]:
    """列出一组目录顶层最近修改的普通文件。"""

    if limit <= 0:
        return ()

    recent_files: list[tuple[float, RecentFile]] = []
    seen_paths: set[str] = set()
    for directory in directories:
        target = Path(directory.path).expanduser().resolve()
        if not target.is_dir():
            continue
        for item in target.iterdir():
            try:
                if item.name.startswith(".") or not item.is_file():
                    continue
                resolved = item.resolve()
                path_key = str(resolved).casefold()
                if path_key in seen_paths:
                    continue
                stat = resolved.stat()
            except OSError:
                continue
            seen_paths.add(path_key)
            recent_files.append(
                (
                    stat.st_mtime,
                    RecentFile(
                        alias=directory.alias,
                        path=resolved,
                        modified_at=datetime.fromtimestamp(stat.st_mtime),
                    ),
                )
            )

    return tuple(
        recent_file
        for _, recent_file in sorted(
            recent_files,
            key=lambda item: (
                -item[0],
                item[1].alias.lower(),
                item[1].path.name.lower(),
            ),
        )[:limit]
    )


def _directories_path(paths: ProjectPaths) -> Path:
    return paths.memory_dir / DIRECTORIES_FILENAME


def _read_directories(paths: ProjectPaths) -> dict[str, str]:
    registry_path = _directories_path(paths)
    if not registry_path.exists():
        return {}

    raw = json.loads(registry_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}

    registry: dict[str, str] = {}
    for alias, directory_path in raw.items():
        if isinstance(alias, str) and isinstance(directory_path, str):
            registry[alias] = directory_path
    return registry


def _write_directories(paths: ProjectPaths, registry: dict[str, str]) -> None:
    registry_path = _directories_path(paths)
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _normalize_alias(alias: str) -> str:
    normalized = alias.strip()
    if not normalized:
        raise ValueError("目录别名不能为空。")
    return normalized


def _report_filename(filename: str | None) -> str:
    if not filename:
        return f"{date.today().isoformat()}-daily-report.md"
    name = Path(filename.strip()).name
    if not name:
        raise ValueError("日报文件名不能为空。")
    return name if name.endswith(".md") else f"{name}.md"


def _daily_report_content(paths: ProjectPaths) -> str:
    profile_summary = summarize_profile(read_profile(paths))
    index = build_knowledge_index(paths)
    directories = list_common_directories(paths)
    lines = [
        "# Jarvis Lite 日报",
        "",
        f"> 日期：{date.today().isoformat()}",
        "> 执行者：Codex",
        "",
        "## 长期记忆摘要",
        "",
        f"- {profile_summary}",
        "",
        "## 知识库状态",
        "",
        f"- 知识库资料：{index.document_count} 个",
        f"- 可检索文本行：{index.searchable_line_count} 行",
        "",
        "## 常用目录",
        "",
    ]
    if directories:
        for directory in directories:
            lines.append(f"- {directory.alias}：{directory.path}")
    else:
        lines.append("- 还没有登记常用目录。")

    runtime_context = load_runtime_context(paths)
    lines.extend(["", "## 最近上下文", ""])
    _append_recent_context_lines(lines, runtime_context)

    lines.extend(["", "## 经验记忆", ""])
    recent_experiences = list_recent_experiences(paths)
    if recent_experiences:
        for experience in recent_experiences:
            lines.append(f"- {experience}")
    else:
        lines.append("- 暂无经验记忆。")

    lines.extend(["", "## 最近工具日志", ""])
    recent_logs = _recent_log_lines(paths)
    if recent_logs:
        for line in recent_logs:
            lines.append(f"- {line}")
    else:
        lines.append("- 暂无工具日志。")

    lines.extend(["", "## 下一步建议", ""])
    _append_next_action_lines(lines, runtime_context, recent_experiences, recent_logs)

    return "\n".join(lines).rstrip() + "\n"


def _append_recent_context_lines(lines: list[str], context: RuntimeContext) -> None:
    has_context = any(
        (
            context.recent_document_path,
            context.recent_document_paths,
            context.recent_directory,
            context.recent_search_result_paths,
            context.recent_advice_suggestions,
        )
    )
    if not has_context:
        lines.append("- 暂无最近上下文。")
        return

    if context.recent_document_path:
        lines.append(f"- 最近资料：data/{context.recent_document_path}")
    if context.recent_document_paths:
        lines.append(f"- 最近资料列表：{len(context.recent_document_paths)} 条")
        for index, path in enumerate(context.recent_document_paths, start=1):
            lines.append(f"  {index}. data/{path}")
    if context.recent_directory is not None:
        lines.append(f"- 最近目录：{context.recent_directory.alias} -> {context.recent_directory.path}")
    if context.recent_search_result_paths:
        lines.append(f"- 最近搜索结果：{len(context.recent_search_result_paths)} 条")
        for index, path in enumerate(context.recent_search_result_paths, start=1):
            lines.append(f"  {index}. data/{path}")
    if context.recent_advice_suggestions:
        lines.append(f"- 最近建议：{len(context.recent_advice_suggestions)} 条")
        for index, suggestion in enumerate(context.recent_advice_suggestions, start=1):
            lines.append(f"  {index}. {suggestion}")


def _append_next_action_lines(
    lines: list[str],
    context: RuntimeContext,
    recent_experiences: tuple[str, ...],
    recent_logs: list[str],
) -> None:
    suggestions: list[str] = []
    if context.recent_document_path:
        suggestions.append(
            f"继续处理最近资料：/read {context.recent_document_path}；/tag {context.recent_document_path} 标签..."
        )
    if context.recent_directory is not None:
        suggestions.append(
            f"继续处理最近目录：/organize-preview {context.recent_directory.alias}；/dir-open {context.recent_directory.alias}"
        )
    if context.recent_advice_suggestions:
        suggestions.append("继续最近建议：查看第一条建议；执行第一条建议")
    if recent_experiences:
        suggestions.append("复用经验记忆：/experience-advice 关键词")
    if recent_logs:
        suggestions.append("沉淀工具流程：/experience 经验内容")
    if not suggestions:
        suggestions.extend(
            [
                "导入资料：/import 源文件或目录路径 [目标文件名]",
                "登记常用目录：/dir-add 别名 目录路径",
                "记录经验：/experience 经验内容",
            ]
        )

    for suggestion in suggestions:
        lines.append(f"- {suggestion}")


def _recent_log_lines(paths: ProjectPaths, limit: int = 5) -> list[str]:
    if not paths.log_path.exists():
        return []
    lines = [line.strip() for line in paths.log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return lines[-limit:]


def _organization_bucket(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if not suffix:
        return "无后缀", "no-extension"
    return suffix, suffix.removeprefix(".")
