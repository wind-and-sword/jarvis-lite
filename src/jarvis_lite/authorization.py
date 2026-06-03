from __future__ import annotations

import shlex
from dataclasses import dataclass
from typing import Iterable


DESKTOP_ACTION_COMMANDS = (
    "/app-launch",
    "/chrome-open",
    "/chrome-search",
    "/clash-open",
    "/clash-focus",
    "/qq-open",
    "/qq-focus",
    "/wechat-open",
    "/wechat-focus",
    "/window-focus",
    "/hotkey",
    "/mouse-click",
    "/type-text",
    "/screen-ocr",
    "/screenshot",
)
LOW_CONFIDENCE_THRESHOLD = 0.78


@dataclass(frozen=True)
class AuthorizationDecision:
    """意图授权层对一次命令执行请求的可审计决策。"""

    intent_name: str
    command: str
    source: str
    action: str
    reason: str
    next_step: str = ""
    requires_confirmation: bool = False
    requires_clarification: bool = False


def is_desktop_action_command(command: str) -> bool:
    """判断命令是否属于当前桌面动作集合。"""

    return _command_name(command) in DESKTOP_ACTION_COMMANDS


def authorize_intent_execution(
    *,
    intent_name: str,
    command: str,
    source: str,
    confirmed: bool = False,
    confidence: float | None = None,
    missing: Iterable[str] = (),
) -> AuthorizationDecision:
    """根据来源、槽位和动作类型决定本轮是否可执行。"""

    normalized_source = source.strip().casefold().replace("-", "_")
    missing_slots = tuple(slot for slot in missing if str(slot).strip())
    command_text = command.strip()
    is_desktop_action = is_desktop_action_command(command_text)

    if normalized_source == "explicit_command":
        return AuthorizationDecision(
            intent_name=intent_name,
            command=command_text,
            source=normalized_source,
            action="direct_execute",
            reason="显式命令由用户直接输入，可以直接执行。",
        )

    if missing_slots:
        missing_text = "、".join(missing_slots)
        return AuthorizationDecision(
            intent_name=intent_name,
            command=command_text,
            source=normalized_source,
            action="clarify",
            reason=f"缺少槽位：{missing_text}。",
            next_step=f"请先补充：{missing_text}",
            requires_clarification=True,
        )

    if confidence is not None and confidence < LOW_CONFIDENCE_THRESHOLD:
        return AuthorizationDecision(
            intent_name=intent_name,
            command=command_text,
            source=normalized_source,
            action="clarify",
            reason=f"识别置信度 {confidence:.2f} 低于 {LOW_CONFIDENCE_THRESHOLD:.2f}。",
            next_step="请换一种说法，或用显式 slash command。",
            requires_clarification=True,
        )

    if confirmed:
        return AuthorizationDecision(
            intent_name=intent_name,
            command=command_text,
            source=normalized_source,
            action="direct_execute",
            reason="已确认执行，可以直接执行。",
        )

    if normalized_source == "llm" and is_desktop_action:
        return AuthorizationDecision(
            intent_name=intent_name,
            command=command_text,
            source=normalized_source,
            action="downgrade",
            reason="LLM 外脑建议的是桌面动作命令，第一阶段不自动执行。",
            next_step="请显式输入该 slash command，或先生成建议并确认执行。",
        )

    if is_desktop_action:
        return AuthorizationDecision(
            intent_name=intent_name,
            command=command_text,
            source=normalized_source,
            action="prepare_confirmation",
            reason="桌面动作需要准备后确认，避免自然语言直接触发窗口、键鼠或应用动作。",
            next_step="确认执行请说“确认执行”，取消请说“取消执行”。",
            requires_confirmation=True,
        )

    return AuthorizationDecision(
        intent_name=intent_name,
        command=command_text,
        source=normalized_source,
        action="direct_execute",
        reason="低风险查询或本地状态命令可以直接执行。",
    )


def describe_authorization_status() -> str:
    """输出意图授权层第一阶段策略。"""

    command_list = "、".join(DESKTOP_ACTION_COMMANDS)
    return "\n".join(
        [
            "意图授权层状态：第一阶段已启用",
            "- 直接执行：显式 slash command，或高置信低风险查询/状态命令。",
            "- 准备后确认：自然语言或建议链路中的桌面动作命令。",
            "- 追问补充：缺少槽位或识别置信度不足的意图。",
            "- 降级：LLM 外脑桌面动作只返回说明，不自动执行。",
            f"- 桌面动作范围：{command_list}",
            "- 确认入口：确认执行 / 取消执行。",
        ]
    )


def _command_name(command: str) -> str:
    if not command.startswith("/"):
        return ""
    try:
        parts = shlex.split(command, posix=False)
    except ValueError:
        parts = command.split()
    return parts[0] if parts else ""
