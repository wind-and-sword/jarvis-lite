from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from .config import ProjectPaths
from .ocr import ImageRecognizer, describe_image_ocr
from .runtime_context import (
    RuntimeContext,
    RuntimeRouteDecisionContext,
    RuntimeTaskContext,
    RuntimeTaskEventContext,
    RuntimeTaskFailureContext,
    load_runtime_context,
    save_runtime_context,
)
from .screen_capture import ScreenCapturer, save_screen_capture


TASK_BOUNDARY_TEXT = "不自动截图、不自动 OCR、不自动重新执行外部动作"
DEFAULT_SCREEN_CONTEXT = "未采集（第一阶段不自动截图、不自动 OCR）。"
DEFAULT_FAILURE_NEXT_STEP = "/task-resume 继续，/task-cancel 取消，或 /task-start 任务名称 重新开始。"
TASK_FAILURE_CAPTURE_BOUNDARY = "当前阶段只记录失败上下文，不自动重新执行外部动作、不点击、不输入。"


def describe_task_status(paths: ProjectPaths) -> str:
    """输出当前任务和最近失败复盘，只读查看运行态上下文。"""

    context = load_runtime_context(paths)
    task = context.current_task
    lines = ["任务状态："]
    if task is None:
        lines[0] = "任务状态：还没有当前任务。"
        lines.append("- 可用 /task-start 任务名称 开始记录一个多步骤任务。")
    else:
        lines.append(f"当前任务：{task.title}（{_status_label(task.status)}）")
        if task.origin_prompt:
            lines.append(f"用户原话：{task.origin_prompt}")
        if task.current_step:
            lines.append(f"当前步骤：{task.current_step}")
        else:
            lines.append("当前步骤：未记录")
        lines.append(f"已完成步骤：{_completed_steps_text(task.completed_steps)}")
        if task.failure_reason:
            lines.append(f"失败原因：{task.failure_reason}")
        if task.updated_at:
            lines.append(f"更新时间：{task.updated_at}")
        _append_task_events(lines, task.recent_events)
        lines.append("下一步建议：/task-step 步骤说明、/task-fail 失败原因、/task-complete、/task-cancel")

    _append_recent_failures(lines, context.recent_task_failures)
    lines.append(f"边界：{TASK_BOUNDARY_TEXT}。")
    return "\n".join(lines)


def start_task(paths: ProjectPaths, title: str, *, origin_prompt: str = "") -> str:
    """开始记录一个显式任务，覆盖旧的当前任务。"""

    task_title = title.strip()
    if not task_title:
        return "任务名称不能为空。用法：/task-start 任务名称"
    now = _now_iso()
    context = load_runtime_context(paths)
    task = RuntimeTaskContext(
        title=task_title,
        status="running",
        origin_prompt=origin_prompt.strip() or task_title,
        created_at=now,
        updated_at=now,
    )
    _save_context(paths, context, current_task=task)
    return "\n".join(
        [
            f"已开始任务：{task.title}",
            "当前步骤：未记录",
            "可继续：/task-step 步骤说明；/task-fail 失败原因；/task-complete；/task-cancel",
        ]
    )


def record_task_step(paths: ProjectPaths, step: str) -> str:
    """记录当前任务步骤；已有当前步骤会转为已完成步骤。"""

    step_text = step.strip()
    if not step_text:
        return "步骤说明不能为空。用法：/task-step 步骤说明"
    context = load_runtime_context(paths)
    task = context.current_task
    if task is None:
        return "还没有当前任务。请先使用 /task-start 任务名称。"

    completed_steps = task.completed_steps
    completed_line = "已完成上一步：无"
    if task.current_step:
        completed_steps = (*completed_steps, task.current_step)
        completed_line = f"已完成上一步：{task.current_step}"
    updated_task = RuntimeTaskContext(
        title=task.title,
        status="running",
        origin_prompt=task.origin_prompt,
        current_step=step_text,
        completed_steps=completed_steps,
        recent_events=task.recent_events,
        failure_reason="",
        created_at=task.created_at,
        updated_at=_now_iso(),
    )
    _save_context(paths, context, current_task=updated_task)
    return "\n".join(
        [
            f"任务步骤已记录：{task.title}",
            completed_line,
            f"当前步骤：{step_text}",
        ]
    )


def record_task_failure(
    paths: ProjectPaths,
    reason: str,
    *,
    route_summary: str = "",
    authorization_summary: str = "",
    window_context: str = "",
    screen_context: str = DEFAULT_SCREEN_CONTEXT,
) -> str:
    """将当前任务标记为失败，并写入最近失败复盘。"""

    reason_text = reason.strip()
    if not reason_text:
        return "失败原因不能为空。用法：/task-fail 失败原因"
    context = load_runtime_context(paths)
    task = context.current_task
    if task is None:
        return "还没有当前任务。请先使用 /task-start 任务名称。"

    failed_step = task.current_step or "未记录"
    now = _now_iso()
    updated_task = RuntimeTaskContext(
        title=task.title,
        status="failed",
        origin_prompt=task.origin_prompt,
        current_step=task.current_step,
        completed_steps=task.completed_steps,
        recent_events=task.recent_events,
        failure_reason=reason_text,
        created_at=task.created_at,
        updated_at=now,
    )
    next_step = _failure_next_step(reason_text, screen_context)
    failure = RuntimeTaskFailureContext(
        title=task.title,
        failed_step=failed_step,
        reason=reason_text,
        origin_prompt=task.origin_prompt,
        route_summary=route_summary,
        authorization_summary=authorization_summary,
        window_context=window_context,
        completed_steps=task.completed_steps,
        recent_events=task.recent_events,
        screen_context=screen_context,
        next_step=next_step,
        created_at=now,
    )
    _save_context(
        paths,
        context,
        current_task=updated_task,
        recent_task_failures=(failure, *context.recent_task_failures)[:5],
    )
    lines = [
        f"任务失败复盘：{task.title}",
        f"失败步骤：{failed_step}",
        f"已完成步骤：{_completed_steps_text(task.completed_steps)}",
        f"失败原因：{reason_text}",
    ]
    if task.origin_prompt:
        lines.append(f"用户原话：{task.origin_prompt}")
    if route_summary:
        lines.append(f"路由摘要：{route_summary}")
    if authorization_summary:
        lines.append(f"授权摘要：{authorization_summary}")
    if window_context:
        lines.append(f"窗口上下文：{window_context}")
    _append_task_events(lines, task.recent_events, header="自动采集上下文：")
    lines.extend(
        [
            f"屏幕/OCR：{screen_context}",
            f"下一步建议：{next_step}",
            "人工固化入口：可把失败原话整理为 /inner-brain-eval-add 或 /inner-brain-eval-label 样本。",
        ]
    )
    lines.extend(_task_event_eval_suggestion_lines(task.recent_events))
    return "\n".join(lines)


def record_task_failure_with_screen_ocr(
    paths: ProjectPaths,
    reason: str,
    *,
    language: str | None = None,
    route_summary: str = "",
    authorization_summary: str = "",
    window_context: str = "",
    capturer: ScreenCapturer | None = None,
    recognizer: ImageRecognizer | None = None,
) -> str:
    """显式采集截图和 OCR 结果后记录任务失败复盘。"""

    reason_text = reason.strip()
    if not reason_text:
        return "失败原因不能为空。用法：/task-fail-capture 失败原因 [lang=chi_sim+eng]"
    context = load_runtime_context(paths)
    if context.current_task is None:
        return "还没有当前任务。请先使用 /task-start 任务名称。"

    try:
        capture = save_screen_capture(
            paths,
            filename=f"task-failure-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            capturer=capturer,
        )
    except (RuntimeError, ValueError) as exc:
        screen_context = f"截图失败：{exc}"
    else:
        ocr_description = describe_image_ocr(
            paths,
            capture.relative_path,
            language=language,
            recognizer=recognizer,
        )
        screen_context = "\n".join(
            [
                f"截图：{capture.relative_path}",
                f"尺寸：{capture.width}x{capture.height}",
                ocr_description,
            ]
        )

    failure_response = record_task_failure(
        paths,
        reason_text,
        route_summary=route_summary,
        authorization_summary=authorization_summary,
        window_context=window_context,
        screen_context=screen_context,
    )
    return f"{failure_response}\n边界：{TASK_FAILURE_CAPTURE_BOUNDARY}"


def record_task_route_event(paths: ProjectPaths, decision: RuntimeRouteDecisionContext) -> None:
    """把当前任务期间的路由决策自动追加到任务上下文。"""

    context = load_runtime_context(paths)
    task = context.current_task
    if task is None or task.status != "running":
        return
    event = RuntimeTaskEventContext(
        route=decision.route,
        detail=decision.detail,
        prompt=decision.prompt,
        summary=decision.summary,
        explanation=decision.explanation,
        created_at=decision.created_at,
    )
    updated_task = replace(
        task,
        recent_events=(event, *task.recent_events)[:5],
        updated_at=_now_iso(),
    )
    _save_context(paths, context, current_task=updated_task)


def record_task_event_result(paths: ProjectPaths, prompt: str, result: str) -> None:
    """把显式命令返回摘要写回最近匹配的任务事件。"""

    prompt_text = prompt.strip()
    result_text = _compact_event_result(result)
    if not prompt_text or not result_text:
        return
    context = load_runtime_context(paths)
    task = context.current_task
    if task is None or task.status != "running" or not task.recent_events:
        return

    updated_events: list[RuntimeTaskEventContext] = []
    changed = False
    for event in task.recent_events:
        if not changed and event.prompt == prompt_text:
            updated_events.append(replace(event, summary=result_text))
            changed = True
        else:
            updated_events.append(event)
    if not changed:
        return
    _save_context(
        paths,
        context,
        current_task=replace(task, recent_events=tuple(updated_events), updated_at=_now_iso()),
    )


def resume_task(paths: ProjectPaths) -> str:
    """恢复失败中的当前任务，但不自动执行任何外部动作。"""

    context = load_runtime_context(paths)
    task = context.current_task
    if task is None or task.status != "failed":
        return "还没有可恢复的失败任务。"
    updated_task = RuntimeTaskContext(
        title=task.title,
        status="running",
        origin_prompt=task.origin_prompt,
        current_step=task.current_step,
        completed_steps=task.completed_steps,
        recent_events=task.recent_events,
        failure_reason="",
        created_at=task.created_at,
        updated_at=_now_iso(),
    )
    _save_context(paths, context, current_task=updated_task)
    current_step = task.current_step or "未记录"
    return "\n".join(
        [
            f"已恢复任务：{task.title}",
            f"当前步骤：{current_step}",
            f"边界：{TASK_BOUNDARY_TEXT}。",
        ]
    )


def complete_task(paths: ProjectPaths) -> str:
    """结束当前任务并清空当前任务状态。"""

    context = load_runtime_context(paths)
    task = context.current_task
    if task is None:
        return "还没有当前任务。"
    _save_context(paths, context, current_task=None)
    return f"已完成任务：{task.title}"


def cancel_task(paths: ProjectPaths) -> str:
    """取消当前任务并清空当前任务状态。"""

    context = load_runtime_context(paths)
    task = context.current_task
    if task is None:
        return "还没有当前任务。"
    _save_context(paths, context, current_task=None)
    return f"已取消任务：{task.title}"


def _append_recent_failures(lines: list[str], failures: tuple[RuntimeTaskFailureContext, ...]) -> None:
    if not failures:
        lines.append("最近失败记录：无")
        return
    lines.append("最近失败记录：")
    for index, failure in enumerate(failures[:5], start=1):
        parts = [
            f"{index}. {failure.title}",
            f"失败步骤：{failure.failed_step}",
            f"原因：{failure.reason}",
        ]
        if failure.created_at:
            parts.append(f"时间：{failure.created_at}")
        lines.append(" | ".join(parts))
        if failure.route_summary:
            lines.append(f"   路由：{failure.route_summary}")
        if failure.authorization_summary:
            lines.append(f"   授权：{failure.authorization_summary}")
        if failure.window_context:
            lines.append(f"   窗口：{_compact_context(failure.window_context)}")
        if failure.next_step:
            lines.append(f"   下一步：{failure.next_step}")
        if failure.screen_context:
            lines.append(f"   屏幕/OCR：{_compact_context(failure.screen_context)}")
        if failure.recent_events:
            lines.append(f"   自动采集：{_compact_context(_task_events_text(failure.recent_events))}")
            for suggestion_line in _task_event_eval_suggestion_lines(failure.recent_events):
                lines.append(f"   {suggestion_line}")


def _save_context(
    paths: ProjectPaths,
    context: RuntimeContext,
    *,
    current_task: RuntimeTaskContext | None,
    recent_task_failures: tuple[RuntimeTaskFailureContext, ...] | None = None,
) -> RuntimeContext:
    return save_runtime_context(
        paths,
        replace(
            context,
            current_task=current_task,
            recent_task_failures=(
                recent_task_failures
                if recent_task_failures is not None
                else context.recent_task_failures
            ),
        ),
    )


def _completed_steps_text(steps: tuple[str, ...]) -> str:
    return "、".join(steps) if steps else "无"


def _append_task_events(
    lines: list[str],
    events: tuple[RuntimeTaskEventContext, ...],
    *,
    header: str = "最近任务事件：",
) -> None:
    if not events:
        lines.append(f"{header}无")
        return
    lines.append(header)
    lines.extend(_task_event_lines(events))


def _task_events_text(events: tuple[RuntimeTaskEventContext, ...]) -> str:
    return "\n".join(_task_event_lines(events))


def _task_event_lines(events: tuple[RuntimeTaskEventContext, ...]) -> list[str]:
    lines: list[str] = []
    for index, event in enumerate(events[:5], start=1):
        parts = [
            f"{index}. {event.route} / {event.detail}",
            f"输入：{event.prompt}",
        ]
        if event.summary:
            parts.append(f"结果：{event.summary}")
        if event.explanation:
            parts.append(f"依据：{event.explanation}")
        lines.append(" | ".join(parts))
    return lines


def _task_event_eval_suggestion_lines(events: tuple[RuntimeTaskEventContext, ...]) -> list[str]:
    suggestions = _task_event_eval_suggestions(events)
    if not suggestions:
        return []
    return [
        *(f"样本建议：{suggestion}" for suggestion in suggestions),
        "样本建议边界：只展示建议，不自动写入 evaluation、不训练、不自动重新执行外部动作。",
    ]


def _task_event_eval_suggestions(events: tuple[RuntimeTaskEventContext, ...]) -> list[str]:
    suggestions: list[str] = []
    seen: set[str] = set()
    for event in events[:5]:
        if event.route != "command":
            continue
        prompt = _compact_eval_token(event.prompt)
        command = _compact_eval_token(event.detail)
        if not prompt or not command.startswith("/"):
            continue
        suggestion = f"/inner-brain-eval-add {prompt} => {command}"
        if suggestion in seen:
            continue
        seen.add(suggestion)
        suggestions.append(suggestion)
    return suggestions


def _compact_eval_token(text: str) -> str:
    return " ".join(text.split())


def _status_label(status: str) -> str:
    if status == "failed":
        return "失败"
    return "进行中"


def _compact_context(text: str) -> str:
    parts = [line.strip() for line in text.splitlines() if line.strip()]
    return " | ".join(parts)


def _compact_event_result(text: str, max_length: int = 180) -> str:
    compacted = _compact_context(text)
    if len(compacted) <= max_length:
        return compacted
    return compacted[: max_length - 1].rstrip() + "…"


def _failure_next_step(reason: str, screen_context: str) -> str:
    if screen_context.strip() == DEFAULT_SCREEN_CONTEXT:
        return f"补充截图/OCR：/task-fail-capture {reason}；然后 {DEFAULT_FAILURE_NEXT_STEP}"
    return DEFAULT_FAILURE_NEXT_STEP


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
