from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .config import ProjectPaths
from .knowledge import build_knowledge_index
from .memory import read_profile, summarize_profile


DIRECTORIES_FILENAME = "directories.json"


@dataclass(frozen=True)
class CommonDirectory:
    alias: str
    path: Path


@dataclass(frozen=True)
class DailyReport:
    path: Path
    relative_path: str


def describe_automation(paths: ProjectPaths) -> str:
    """输出阶段 4 工作台自动化状态。"""

    directories = list_common_directories(paths)
    lines = [
        "阶段 4 自动化状态：",
        f"- 常用目录：{len(directories)} 个",
        "- 日报目录：word",
        "- 当前能力：/dir-add、/dirs、/daily-report",
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

    lines.extend(["", "## 最近工具日志", ""])
    recent_logs = _recent_log_lines(paths)
    if recent_logs:
        for line in recent_logs:
            lines.append(f"- {line}")
    else:
        lines.append("- 暂无工具日志。")

    return "\n".join(lines).rstrip() + "\n"


def _recent_log_lines(paths: ProjectPaths, limit: int = 5) -> list[str]:
    if not paths.log_path.exists():
        return []
    lines = [line.strip() for line in paths.log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return lines[-limit:]
