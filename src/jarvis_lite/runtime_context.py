from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .config import ProjectPaths


RUNTIME_DIRNAME = "jarvis-lite-runtime"
CONTEXT_FILENAME = "agent-context.json"


@dataclass(frozen=True)
class RuntimeDirectoryContext:
    """保存最近目录的可序列化运行态信息。"""

    alias: str
    path: str


@dataclass(frozen=True)
class RuntimeContext:
    """保存可跨 Agent 实例恢复的轻量运行态上下文。"""

    recent_document_path: str | None = None
    recent_directory: RuntimeDirectoryContext | None = None
    recent_search_result_paths: tuple[str, ...] = ()
    recent_advice_suggestions: tuple[str, ...] = ()


def runtime_context_path(paths: ProjectPaths) -> Path:
    """返回项目外的 Agent 运行态上下文文件路径。"""

    return paths.root.parent / RUNTIME_DIRNAME / CONTEXT_FILENAME


def load_runtime_context(paths: ProjectPaths) -> RuntimeContext:
    """读取 Agent 运行态上下文；损坏或缺失时回退为空上下文。"""

    context_path = runtime_context_path(paths)
    if not context_path.exists():
        return RuntimeContext()

    try:
        raw = json.loads(context_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return RuntimeContext()

    if not isinstance(raw, dict):
        return RuntimeContext()
    return RuntimeContext(
        recent_document_path=_read_optional_str(raw.get("recent_document_path")),
        recent_directory=_read_directory_context(raw.get("recent_directory")),
        recent_search_result_paths=_read_str_tuple(raw.get("recent_search_result_paths")),
        recent_advice_suggestions=_read_str_tuple(raw.get("recent_advice_suggestions")),
    )


def save_runtime_context(paths: ProjectPaths, context: RuntimeContext) -> RuntimeContext:
    """写入 Agent 运行态上下文。"""

    context_path = runtime_context_path(paths)
    context_path.parent.mkdir(parents=True, exist_ok=True)
    context_path.write_text(
        json.dumps(
            {
                "recent_document_path": context.recent_document_path,
                "recent_directory": _directory_context_to_json(context.recent_directory),
                "recent_search_result_paths": list(context.recent_search_result_paths),
                "recent_advice_suggestions": list(context.recent_advice_suggestions),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return context


def _read_str_tuple(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item.strip())


def _read_optional_str(value: object) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def _read_directory_context(value: object) -> RuntimeDirectoryContext | None:
    if not isinstance(value, dict):
        return None
    alias = _read_optional_str(value.get("alias"))
    path = _read_optional_str(value.get("path"))
    if alias is None or path is None:
        return None
    return RuntimeDirectoryContext(alias=alias, path=path)


def _directory_context_to_json(context: RuntimeDirectoryContext | None) -> dict[str, str] | None:
    if context is None:
        return None
    return {"alias": context.alias, "path": context.path}
