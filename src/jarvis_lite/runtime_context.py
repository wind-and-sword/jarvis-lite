from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .config import ProjectPaths


RUNTIME_DIRNAME = "jarvis-lite-runtime"
CONTEXT_FILENAME = "agent-context.json"
ROUTE_DECISION_HISTORY_LIMIT = 5
INNER_BRAIN_CANDIDATE_LIMIT = 20
TASK_FAILURE_HISTORY_LIMIT = 5
MEMORY_CONFIG_CANDIDATE_LIMIT = 20


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
class RuntimeWebSearchResultContext:
    """保存联网搜索结果的可序列化运行态信息。"""

    title: str
    url: str
    snippet: str = ""
    source: str = ""


@dataclass(frozen=True)
class RuntimeWebSearchContext:
    """保存最近一次联网搜索的可序列化上下文。"""

    query: str
    results: tuple[RuntimeWebSearchResultContext, ...] = ()


@dataclass(frozen=True)
class RuntimeTaggedDocumentsOperationContext:
    """保存最近一次批量标签操作的可序列化运行态信息。"""

    tag: str
    tags: tuple[str, ...]
    updated_count: int
    restore_commands: tuple[str, ...] = ()
    document_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeLLMClarificationContext:
    """保存 LLM 外脑待澄清问题的可序列化运行态信息。"""

    original_prompt: str
    clarification: str
    context: tuple[str, ...] = ()
    clarification_count: int = 1
    created_at: str = ""


@dataclass(frozen=True)
class RuntimeLLMCallContext:
    """保存最近一次 LLM 外脑调用的可序列化运行态信息。"""

    source: str
    prompt: str
    intent_type: str
    summary: str = ""
    reason: str = ""
    provider: str = ""
    model: str = ""
    created_at: str = ""


@dataclass(frozen=True)
class RuntimeRouteDecisionContext:
    """保存最近一次输入路由决策的可序列化运行态信息。"""

    route: str
    detail: str
    prompt: str
    summary: str = ""
    explanation: str = ""
    created_at: str = ""


@dataclass(frozen=True)
class RuntimeInnerBrainCandidateContext:
    """保存 InnerBrain 训练候选的可序列化观察统计。"""

    prompt: str
    route: str
    detail: str
    summary: str = ""
    explanation: str = ""
    count: int = 1
    first_seen_at: str = ""
    last_seen_at: str = ""


@dataclass(frozen=True)
class RuntimeTaskContext:
    """保存当前任务的可序列化运行态信息。"""

    title: str
    status: str = "running"
    origin_prompt: str = ""
    current_step: str = ""
    completed_steps: tuple[str, ...] = ()
    failure_reason: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class RuntimeTaskFailureContext:
    """保存最近任务失败复盘的可序列化运行态信息。"""

    title: str
    failed_step: str
    reason: str
    origin_prompt: str = ""
    route_summary: str = ""
    authorization_summary: str = ""
    completed_steps: tuple[str, ...] = ()
    screen_context: str = ""
    next_step: str = ""
    created_at: str = ""


@dataclass(frozen=True)
class RuntimeMemoryConfigCandidateContext:
    """保存记忆与配置候选的可序列化运行态信息。"""

    candidate_type: str
    content: str
    status: str = "active"
    count: int = 1
    first_seen_at: str = ""
    last_seen_at: str = ""


@dataclass(frozen=True)
class RuntimeContext:
    """保存可跨 Agent 实例恢复的轻量运行态上下文。"""

    recent_document_path: str | None = None
    recent_document_paths: tuple[str, ...] = ()
    recent_directory: RuntimeDirectoryContext | None = None
    recent_search_result_paths: tuple[str, ...] = ()
    recent_web_search: RuntimeWebSearchContext | None = None
    recent_advice_suggestions: tuple[str, ...] = ()
    recent_files: tuple[RuntimeRecentFileContext, ...] = ()
    recent_tagged_documents_operation: RuntimeTaggedDocumentsOperationContext | None = None
    recent_tagged_documents_operations: tuple[RuntimeTaggedDocumentsOperationContext, ...] = ()
    pending_llm_clarification: RuntimeLLMClarificationContext | None = None
    recent_llm_call: RuntimeLLMCallContext | None = None
    recent_route_decision: RuntimeRouteDecisionContext | None = None
    recent_route_decisions: tuple[RuntimeRouteDecisionContext, ...] = ()
    inner_brain_candidates: tuple[RuntimeInnerBrainCandidateContext, ...] | None = None
    current_task: RuntimeTaskContext | None = None
    recent_task_failures: tuple[RuntimeTaskFailureContext, ...] = ()
    memory_config_candidates: tuple[RuntimeMemoryConfigCandidateContext, ...] = ()


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
    recent_route_decision = _read_route_decision_context(raw.get("recent_route_decision"))
    recent_route_decisions = _route_decision_history_with_latest(
        recent_route_decision,
        _read_route_decision_contexts(raw.get("recent_route_decisions")),
    )
    if recent_route_decision is None and recent_route_decisions:
        recent_route_decision = recent_route_decisions[0]
    return RuntimeContext(
        recent_document_path=recent_document_path,
        recent_document_paths=_read_recent_document_paths(raw.get("recent_document_paths"), recent_document_path),
        recent_directory=_read_directory_context(raw.get("recent_directory")),
        recent_search_result_paths=_read_str_tuple(raw.get("recent_search_result_paths")),
        recent_web_search=_read_web_search_context(raw.get("recent_web_search")),
        recent_advice_suggestions=_read_str_tuple(raw.get("recent_advice_suggestions")),
        recent_files=_read_recent_file_contexts(raw.get("recent_files")),
        recent_tagged_documents_operation=recent_tagged_documents_operation,
        recent_tagged_documents_operations=recent_tagged_documents_operations,
        pending_llm_clarification=_read_llm_clarification_context(raw.get("pending_llm_clarification")),
        recent_llm_call=_read_llm_call_context(raw.get("recent_llm_call")),
        recent_route_decision=recent_route_decision,
        recent_route_decisions=recent_route_decisions,
        inner_brain_candidates=_read_inner_brain_candidate_contexts(raw.get("inner_brain_candidates")),
        current_task=_read_task_context(raw.get("current_task")),
        recent_task_failures=_read_task_failure_contexts(raw.get("recent_task_failures")),
        memory_config_candidates=_read_memory_config_candidate_contexts(raw.get("memory_config_candidates")),
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
    recent_route_decisions = _route_decision_history_with_latest(
        context.recent_route_decision,
        context.recent_route_decisions,
    )
    recent_route_decision = (
        context.recent_route_decision
        if context.recent_route_decision is not None
        else recent_route_decisions[0]
        if recent_route_decisions
        else None
    )
    context_path.write_text(
        json.dumps(
            {
                "recent_document_path": context.recent_document_path,
                "recent_document_paths": list(context.recent_document_paths),
                "recent_directory": _directory_context_to_json(context.recent_directory),
                "recent_search_result_paths": list(context.recent_search_result_paths),
                "recent_web_search": _web_search_context_to_json(context.recent_web_search),
                "recent_advice_suggestions": list(context.recent_advice_suggestions),
                "recent_files": [_recent_file_context_to_json(recent_file) for recent_file in context.recent_files],
                "recent_tagged_documents_operation": _tagged_documents_operation_context_to_json(
                    recent_tagged_documents_operation
                ),
                "recent_tagged_documents_operations": [
                    _tagged_documents_operation_context_to_json(operation)
                    for operation in recent_tagged_documents_operations
                ],
                "pending_llm_clarification": _llm_clarification_context_to_json(
                    context.pending_llm_clarification
                ),
                "recent_llm_call": _llm_call_context_to_json(context.recent_llm_call),
                "recent_route_decision": _route_decision_context_to_json(recent_route_decision),
                "recent_route_decisions": [
                    _route_decision_context_to_json(decision) for decision in recent_route_decisions
                ],
                "inner_brain_candidates": _inner_brain_candidate_contexts_to_json(
                    context.inner_brain_candidates
                ),
                "current_task": _task_context_to_json(context.current_task),
                "recent_task_failures": [
                    _task_failure_context_to_json(failure)
                    for failure in context.recent_task_failures[:TASK_FAILURE_HISTORY_LIMIT]
                ],
                "memory_config_candidates": [
                    _memory_config_candidate_context_to_json(candidate)
                    for candidate in context.memory_config_candidates[:MEMORY_CONFIG_CANDIDATE_LIMIT]
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


def _read_positive_int(value: object, default: int) -> int:
    if isinstance(value, int) and value > 0:
        return value
    return default


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


def _read_web_search_context(value: object) -> RuntimeWebSearchContext | None:
    if not isinstance(value, dict):
        return None
    query = _read_optional_str(value.get("query"))
    if query is None:
        return None
    results = _read_web_search_result_contexts(value.get("results"))
    return RuntimeWebSearchContext(query=query, results=results)


def _read_web_search_result_contexts(value: object) -> tuple[RuntimeWebSearchResultContext, ...]:
    if not isinstance(value, list):
        return ()
    results: list[RuntimeWebSearchResultContext] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        title = _read_optional_str(item.get("title"))
        url = _read_optional_str(item.get("url"))
        if title is None or url is None:
            continue
        results.append(
            RuntimeWebSearchResultContext(
                title=title,
                url=url,
                snippet=_read_optional_str(item.get("snippet")) or "",
                source=_read_optional_str(item.get("source")) or "",
            )
        )
        if len(results) >= 5:
            break
    return tuple(results)


def _read_llm_clarification_context(value: object) -> RuntimeLLMClarificationContext | None:
    if not isinstance(value, dict):
        return None
    original_prompt = _read_optional_str(value.get("original_prompt"))
    clarification = _read_optional_str(value.get("clarification"))
    if original_prompt is None or clarification is None:
        return None
    return RuntimeLLMClarificationContext(
        original_prompt=original_prompt,
        clarification=clarification,
        context=_read_str_tuple(value.get("context")),
        clarification_count=_read_positive_int(value.get("clarification_count"), 1),
        created_at=_read_optional_str(value.get("created_at")) or "",
    )


def _read_llm_call_context(value: object) -> RuntimeLLMCallContext | None:
    if not isinstance(value, dict):
        return None
    source = _read_optional_str(value.get("source"))
    prompt = _read_optional_str(value.get("prompt"))
    intent_type = _read_optional_str(value.get("intent_type"))
    if source is None or prompt is None or intent_type is None:
        return None
    return RuntimeLLMCallContext(
        source=source,
        prompt=prompt,
        intent_type=intent_type,
        summary=_read_optional_str(value.get("summary")) or "",
        reason=_read_optional_str(value.get("reason")) or "",
        provider=_read_optional_str(value.get("provider")) or "",
        model=_read_optional_str(value.get("model")) or "",
        created_at=_read_optional_str(value.get("created_at")) or "",
    )


def _read_route_decision_context(value: object) -> RuntimeRouteDecisionContext | None:
    if not isinstance(value, dict):
        return None
    route = _read_optional_str(value.get("route"))
    detail = _read_optional_str(value.get("detail"))
    prompt = _read_optional_str(value.get("prompt"))
    if route is None or detail is None or prompt is None:
        return None
    return RuntimeRouteDecisionContext(
        route=route,
        detail=detail,
        prompt=prompt,
        summary=_read_optional_str(value.get("summary")) or "",
        explanation=_read_optional_str(value.get("explanation")) or "",
        created_at=_read_optional_str(value.get("created_at")) or "",
    )


def _read_route_decision_contexts(value: object) -> tuple[RuntimeRouteDecisionContext, ...]:
    if not isinstance(value, list):
        return ()
    decisions: list[RuntimeRouteDecisionContext] = []
    for item in value:
        decision = _read_route_decision_context(item)
        if decision is not None:
            decisions.append(decision)
        if len(decisions) >= ROUTE_DECISION_HISTORY_LIMIT:
            break
    return tuple(decisions)


def _read_inner_brain_candidate_contexts(value: object) -> tuple[RuntimeInnerBrainCandidateContext, ...] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        return ()
    candidates: list[RuntimeInnerBrainCandidateContext] = []
    seen_prompts: set[str] = set()
    for item in value:
        if not isinstance(item, dict):
            continue
        prompt = _read_optional_str(item.get("prompt"))
        route = _read_optional_str(item.get("route"))
        detail = _read_optional_str(item.get("detail"))
        if prompt is None or route is None or detail is None:
            continue
        prompt_key = prompt.strip()
        if prompt_key in seen_prompts:
            continue
        seen_prompts.add(prompt_key)
        candidates.append(
            RuntimeInnerBrainCandidateContext(
                prompt=prompt,
                route=route,
                detail=detail,
                summary=_read_optional_str(item.get("summary")) or "",
                explanation=_read_optional_str(item.get("explanation")) or "",
                count=_read_positive_int(item.get("count"), 1),
                first_seen_at=_read_optional_str(item.get("first_seen_at")) or "",
                last_seen_at=_read_optional_str(item.get("last_seen_at")) or "",
            )
        )
        if len(candidates) >= INNER_BRAIN_CANDIDATE_LIMIT:
            break
    return tuple(candidates)


def _read_task_context(value: object) -> RuntimeTaskContext | None:
    if not isinstance(value, dict):
        return None
    title = _read_optional_str(value.get("title"))
    if title is None:
        return None
    status = _read_optional_str(value.get("status")) or "running"
    if status not in {"running", "failed"}:
        status = "running"
    return RuntimeTaskContext(
        title=title,
        status=status,
        origin_prompt=_read_optional_str(value.get("origin_prompt")) or "",
        current_step=_read_optional_str(value.get("current_step")) or "",
        completed_steps=_read_str_tuple(value.get("completed_steps")),
        failure_reason=_read_optional_str(value.get("failure_reason")) or "",
        created_at=_read_optional_str(value.get("created_at")) or "",
        updated_at=_read_optional_str(value.get("updated_at")) or "",
    )


def _read_task_failure_context(value: object) -> RuntimeTaskFailureContext | None:
    if not isinstance(value, dict):
        return None
    title = _read_optional_str(value.get("title"))
    failed_step = _read_optional_str(value.get("failed_step"))
    reason = _read_optional_str(value.get("reason"))
    if title is None or failed_step is None or reason is None:
        return None
    return RuntimeTaskFailureContext(
        title=title,
        failed_step=failed_step,
        reason=reason,
        origin_prompt=_read_optional_str(value.get("origin_prompt")) or "",
        route_summary=_read_optional_str(value.get("route_summary")) or "",
        authorization_summary=_read_optional_str(value.get("authorization_summary")) or "",
        completed_steps=_read_str_tuple(value.get("completed_steps")),
        screen_context=_read_optional_str(value.get("screen_context")) or "",
        next_step=_read_optional_str(value.get("next_step")) or "",
        created_at=_read_optional_str(value.get("created_at")) or "",
    )


def _read_task_failure_contexts(value: object) -> tuple[RuntimeTaskFailureContext, ...]:
    if not isinstance(value, list):
        return ()
    failures: list[RuntimeTaskFailureContext] = []
    for item in value:
        failure = _read_task_failure_context(item)
        if failure is not None:
            failures.append(failure)
        if len(failures) >= TASK_FAILURE_HISTORY_LIMIT:
            break
    return tuple(failures)


def _read_memory_config_candidate_context(value: object) -> RuntimeMemoryConfigCandidateContext | None:
    if not isinstance(value, dict):
        return None
    candidate_type = _read_optional_str(value.get("candidate_type"))
    content = _read_optional_str(value.get("content"))
    if candidate_type is None or content is None:
        return None
    status = _read_optional_str(value.get("status")) or "active"
    if status not in {"active", "dismissed"}:
        status = "active"
    return RuntimeMemoryConfigCandidateContext(
        candidate_type=candidate_type,
        content=content,
        status=status,
        count=_read_positive_int(value.get("count"), 1),
        first_seen_at=_read_optional_str(value.get("first_seen_at")) or "",
        last_seen_at=_read_optional_str(value.get("last_seen_at")) or "",
    )


def _read_memory_config_candidate_contexts(value: object) -> tuple[RuntimeMemoryConfigCandidateContext, ...]:
    if not isinstance(value, list):
        return ()
    candidates: list[RuntimeMemoryConfigCandidateContext] = []
    seen: set[tuple[str, str, str]] = set()
    for item in value:
        candidate = _read_memory_config_candidate_context(item)
        if candidate is None:
            continue
        key = (candidate.candidate_type, candidate.content.strip(), candidate.status)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(candidate)
        if len(candidates) >= MEMORY_CONFIG_CANDIDATE_LIMIT:
            break
    return tuple(candidates)


def _route_decision_history_with_latest(
    latest: RuntimeRouteDecisionContext | None,
    history: tuple[RuntimeRouteDecisionContext, ...],
) -> tuple[RuntimeRouteDecisionContext, ...]:
    decisions: list[RuntimeRouteDecisionContext] = []
    if latest is not None:
        decisions.append(latest)
    for decision in history:
        if latest is not None and _same_route_decision(decision, latest) and decisions:
            continue
        decisions.append(decision)
        if len(decisions) >= ROUTE_DECISION_HISTORY_LIMIT:
            break
    return tuple(decisions[:ROUTE_DECISION_HISTORY_LIMIT])


def _same_route_decision(left: RuntimeRouteDecisionContext, right: RuntimeRouteDecisionContext) -> bool:
    return (
        left.route == right.route
        and left.detail == right.detail
        and left.prompt == right.prompt
        and left.summary == right.summary
        and left.explanation == right.explanation
        and left.created_at == right.created_at
    )


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


def _web_search_context_to_json(context: RuntimeWebSearchContext | None) -> dict[str, object] | None:
    if context is None:
        return None
    return {
        "query": context.query,
        "results": [_web_search_result_context_to_json(result) for result in context.results],
    }


def _web_search_result_context_to_json(context: RuntimeWebSearchResultContext) -> dict[str, str]:
    return {
        "title": context.title,
        "url": context.url,
        "snippet": context.snippet,
        "source": context.source,
    }


def _llm_clarification_context_to_json(
    context: RuntimeLLMClarificationContext | None,
) -> dict[str, object] | None:
    if context is None:
        return None
    return {
        "original_prompt": context.original_prompt,
        "clarification": context.clarification,
        "context": list(context.context),
        "clarification_count": context.clarification_count,
        "created_at": context.created_at,
    }


def _llm_call_context_to_json(context: RuntimeLLMCallContext | None) -> dict[str, str] | None:
    if context is None:
        return None
    return {
        "source": context.source,
        "prompt": context.prompt,
        "intent_type": context.intent_type,
        "summary": context.summary,
        "reason": context.reason,
        "provider": context.provider,
        "model": context.model,
        "created_at": context.created_at,
    }


def _route_decision_context_to_json(context: RuntimeRouteDecisionContext | None) -> dict[str, str] | None:
    if context is None:
        return None
    return {
        "route": context.route,
        "detail": context.detail,
        "prompt": context.prompt,
        "summary": context.summary,
        "explanation": context.explanation,
        "created_at": context.created_at,
    }


def _inner_brain_candidate_contexts_to_json(
    contexts: tuple[RuntimeInnerBrainCandidateContext, ...] | None,
) -> list[dict[str, object]] | None:
    if contexts is None:
        return None
    return [_inner_brain_candidate_context_to_json(context) for context in contexts[:INNER_BRAIN_CANDIDATE_LIMIT]]


def _inner_brain_candidate_context_to_json(context: RuntimeInnerBrainCandidateContext) -> dict[str, object]:
    return {
        "prompt": context.prompt,
        "route": context.route,
        "detail": context.detail,
        "summary": context.summary,
        "explanation": context.explanation,
        "count": context.count,
        "first_seen_at": context.first_seen_at,
        "last_seen_at": context.last_seen_at,
    }


def _task_context_to_json(context: RuntimeTaskContext | None) -> dict[str, object] | None:
    if context is None:
        return None
    return {
        "title": context.title,
        "status": context.status,
        "origin_prompt": context.origin_prompt,
        "current_step": context.current_step,
        "completed_steps": list(context.completed_steps),
        "failure_reason": context.failure_reason,
        "created_at": context.created_at,
        "updated_at": context.updated_at,
    }


def _task_failure_context_to_json(context: RuntimeTaskFailureContext) -> dict[str, object]:
    return {
        "title": context.title,
        "failed_step": context.failed_step,
        "reason": context.reason,
        "origin_prompt": context.origin_prompt,
        "route_summary": context.route_summary,
        "authorization_summary": context.authorization_summary,
        "completed_steps": list(context.completed_steps),
        "screen_context": context.screen_context,
        "next_step": context.next_step,
        "created_at": context.created_at,
    }


def _memory_config_candidate_context_to_json(
    context: RuntimeMemoryConfigCandidateContext,
) -> dict[str, object]:
    return {
        "candidate_type": context.candidate_type,
        "content": context.content,
        "status": context.status,
        "count": context.count,
        "first_seen_at": context.first_seen_at,
        "last_seen_at": context.last_seen_at,
    }


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
