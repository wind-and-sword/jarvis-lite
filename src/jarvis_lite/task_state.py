from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from .config import ProjectPaths
from .runtime_context import (
    RuntimeContext,
    RuntimeTaskContext,
    RuntimeTaskFailureContext,
    load_runtime_context,
    save_runtime_context,
)


TASK_BOUNDARY_TEXT = "不自动截图、不自动 OCR、不自动重新执行外部动作"
DEFAULT_SCREEN_CONTEXT = "未采集（第一阶段不自动截图、不自动 OCR）。"
DEFAULT_FAILURE_NEXT_STEP = "/task-resume 继续，/task-cancel 取消，或 /task-start 任务名称 重新开始。"


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
        failure_reason=reason_text,
        created_at=task.created_at,
        updated_at=now,
    )
    failure = RuntimeTaskFailureContext(
        title=task.title,
        failed_step=failed_step,
        reason=reason_text,
        origin_prompt=task.origin_prompt,
        route_summary=route_summary,
        authorization_summary=authorization_summary,
        completed_steps=task.completed_steps,
        screen_context=screen_context,
        next_step=DEFAULT_FAILURE_NEXT_STEP,
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
    lines.extend(
        [
            f"屏幕/OCR：{screen_context}",
            f"下一步建议：{DEFAULT_FAILURE_NEXT_STEP}",
            "人工固化入口：可把失败原话整理为 /inner-brain-eval-add 或 /inner-brain-eval-label 样本。",
        ]
    )
    return "\n".join(lines)


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
        if failure.next_step:
            lines.append(f"   下一步：{failure.next_step}")


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


def _status_label(status: str) -> str:
    if status == "failed":
        return "失败"
    return "进行中"


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
