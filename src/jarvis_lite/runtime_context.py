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
class RuntimeRecentFileContext:
    """保存最近文件的可序列化运行态信息。"""

    alias: str
    path: str


@dataclass(frozen=True)
class RuntimeTaggedDocumentsOperationContext:
    """保存最近一次批量标签操作的可序列化运行态信息。"""

    tag: str
    tags: tuple[str, ...]
    updated_count: int
    restore_commands: tuple[str, ...] = ()
    document_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeContext:
    """保存可跨 Agent 实例恢复的轻量运行态上下文。"""

    recent_document_path: str | None = None
    recent_document_paths: tuple[str, ...] = ()
    recent_directory: RuntimeDirectoryContext | None = None
    recent_search_result_paths: tuple[str, ...] = ()
    recent_advice_suggestions: tuple[str, ...] = ()
    recent_files: tuple[RuntimeRecentFileContext, ...] = ()
    recent_tagged_documents_operation: RuntimeTaggedDocumentsOperationContext | None = None
    recent_tagged_documents_operations: tuple[RuntimeTaggedDocumentsOperationContext, ...] = ()


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
    recent_document_path = _read_optional_str(raw.get("recent_document_path"))
    recent_tagged_documents_operation = _read_tagged_documents_operation_context(
        raw.get("recent_tagged_documents_operation")
    )
    recent_tagged_documents_operations = _read_tagged_documents_operation_contexts(
        raw.get("recent_tagged_documents_operations")
    )
    recent_tagged_documents_operations = _tagged_documents_operation_history_with_latest(
        recent_tagged_documents_operation,
        recent_tagged_documents_operations,
    )
    if recent_tagged_documents_operation is None and recent_tagged_documents_operations:
        recent_tagged_documents_operation = recent_tagged_documents_operations[0]
    return RuntimeContext(
        recent_document_path=recent_document_path,
        recent_document_paths=_read_recent_document_paths(raw.get("recent_document_paths"), recent_document_path),
        recent_directory=_read_directory_context(raw.get("recent_directory")),
        recent_search_result_paths=_read_str_tuple(raw.get("recent_search_result_paths")),
        recent_advice_suggestions=_read_str_tuple(raw.get("recent_advice_suggestions")),
        recent_files=_read_recent_file_contexts(raw.get("recent_files")),
        recent_tagged_documents_operation=recent_tagged_documents_operation,
        recent_tagged_documents_operations=recent_tagged_documents_operations,
    )


def save_runtime_context(paths: ProjectPaths, context: RuntimeContext) -> RuntimeContext:
    """写入 Agent 运行态上下文。"""

    context_path = runtime_context_path(paths)
    context_path.parent.mkdir(parents=True, exist_ok=True)
    recent_tagged_documents_operations = _tagged_documents_operation_history_with_latest(
        context.recent_tagged_documents_operation,
        context.recent_tagged_documents_operations,
    )
    recent_tagged_documents_operation = (
        context.recent_tagged_documents_operation
        if context.recent_tagged_documents_operation is not None
        else recent_tagged_documents_operations[0]
        if recent_tagged_documents_operations
        else None
    )
    context_path.write_text(
        json.dumps(
            {
                "recent_document_path": context.recent_document_path,
                "recent_document_paths": list(context.recent_document_paths),
                "recent_directory": _directory_context_to_json(context.recent_directory),
                "recent_search_result_paths": list(context.recent_search_result_paths),
                "recent_advice_suggestions": list(context.recent_advice_suggestions),
                "recent_files": [_recent_file_context_to_json(recent_file) for recent_file in context.recent_files],
                "recent_tagged_documents_operation": _tagged_documents_operation_context_to_json(
                    recent_tagged_documents_operation
                ),
                "recent_tagged_documents_operations": [
                    _tagged_documents_operation_context_to_json(operation)
                    for operation in recent_tagged_documents_operations
                ],
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


def _read_recent_document_paths(value: object, current_path: str | None) -> tuple[str, ...]:
    paths = _read_str_tuple(value)
    if current_path is None or current_path in paths:
        return paths
    return (current_path, *paths)


def _read_directory_context(value: object) -> RuntimeDirectoryContext | None:
    if not isinstance(value, dict):
        return None
    alias = _read_optional_str(value.get("alias"))
    path = _read_optional_str(value.get("path"))
    if alias is None or path is None:
        return None
    return RuntimeDirectoryContext(alias=alias, path=path)


def _read_recent_file_contexts(value: object) -> tuple[RuntimeRecentFileContext, ...]:
    if not isinstance(value, list):
        return ()
    recent_files: list[RuntimeRecentFileContext] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        alias = _read_optional_str(item.get("alias"))
        path = _read_optional_str(item.get("path"))
        if alias is None or path is None:
            continue
        recent_files.append(RuntimeRecentFileContext(alias=alias, path=path))
    return tuple(recent_files)


def _read_tagged_documents_operation_context(value: object) -> RuntimeTaggedDocumentsOperationContext | None:
    if not isinstance(value, dict):
        return None
    tag = _read_optional_str(value.get("tag"))
    tags = _read_str_tuple(value.get("tags"))
    updated_count = value.get("updated_count")
    if tag is None or not tags or not isinstance(updated_count, int) or updated_count < 0:
        return None
    return RuntimeTaggedDocumentsOperationContext(
        tag=tag,
        tags=tags,
        updated_count=updated_count,
        restore_commands=_read_str_tuple(value.get("restore_commands")),
        document_paths=_read_str_tuple(value.get("document_paths")),
    )


def _read_tagged_documents_operation_contexts(value: object) -> tuple[RuntimeTaggedDocumentsOperationContext, ...]:
    if not isinstance(value, list):
        return ()
    operations: list[RuntimeTaggedDocumentsOperationContext] = []
    for item in value:
        operation = _read_tagged_documents_operation_context(item)
        if operation is not None:
            operations.append(operation)
        if len(operations) >= 5:
            break
    return tuple(operations)


def _tagged_documents_operation_history_with_latest(
    latest: RuntimeTaggedDocumentsOperationContext | None,
    history: tuple[RuntimeTaggedDocumentsOperationContext, ...],
) -> tuple[RuntimeTaggedDocumentsOperationContext, ...]:
    operations: list[RuntimeTaggedDocumentsOperationContext] = []
    if latest is not None:
        latest = _tagged_documents_operation_with_history_paths(latest, history)
        operations.append(latest)
    for operation in history:
        if latest is not None and _same_tagged_documents_operation(operation, latest) and operations:
            continue
        operations.append(operation)
        if len(operations) >= 5:
            break
    return tuple(operations[:5])


def _tagged_documents_operation_with_history_paths(
    latest: RuntimeTaggedDocumentsOperationContext,
    history: tuple[RuntimeTaggedDocumentsOperationContext, ...],
) -> RuntimeTaggedDocumentsOperationContext:
    if latest.document_paths:
        return latest
    for operation in history:
        if _same_tagged_documents_operation(operation, latest) and operation.document_paths:
            return RuntimeTaggedDocumentsOperationContext(
                tag=latest.tag,
                tags=latest.tags,
                updated_count=latest.updated_count,
                restore_commands=latest.restore_commands,
                document_paths=operation.document_paths,
            )
    return latest


def _same_tagged_documents_operation(
    left: RuntimeTaggedDocumentsOperationContext,
    right: RuntimeTaggedDocumentsOperationContext,
) -> bool:
    return (
        left.tag == right.tag
        and left.tags == right.tags
        and left.updated_count == right.updated_count
        and left.restore_commands == right.restore_commands
    )


def _directory_context_to_json(context: RuntimeDirectoryContext | None) -> dict[str, str] | None:
    if context is None:
        return None
    return {"alias": context.alias, "path": context.path}


def _recent_file_context_to_json(context: RuntimeRecentFileContext) -> dict[str, str]:
    return {"alias": context.alias, "path": context.path}


def _tagged_documents_operation_context_to_json(
    context: RuntimeTaggedDocumentsOperationContext | None,
) -> dict[str, object] | None:
    if context is None:
        return None
    return {
        "tag": context.tag,
        "tags": list(context.tags),
        "updated_count": context.updated_count,
        "restore_commands": list(context.restore_commands),
        "document_paths": list(context.document_paths),
    }
