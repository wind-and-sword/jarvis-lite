from __future__ import annotations

from dataclasses import dataclass

from .app_registry import AppLaunchExecutor, AppLaunchResult, launch_registered_app, match_registered_app
from .config import ProjectPaths
from .window_state import WindowFocusExecutor, WindowSnapshot, describe_window_focus


@dataclass(frozen=True)
class MessagingAppProfile:
    app_id: str
    display_name: str
    open_command: str
    focus_command: str
    prepare_command: str


@dataclass(frozen=True)
class MessageDraft:
    contact: str
    message: str


MESSAGING_APP_PROFILES = {
    "qq": MessagingAppProfile(
        app_id="qq",
        display_name="QQ",
        open_command="/qq-open",
        focus_command="/qq-focus",
        prepare_command="/qq-prepare-message",
    ),
    "wechat": MessagingAppProfile(
        app_id="wechat",
        display_name="微信",
        open_command="/wechat-open",
        focus_command="/wechat-focus",
        prepare_command="/wechat-prepare-message",
    ),
}


def describe_messaging_workflow_status(paths: ProjectPaths) -> str:
    """输出 QQ/微信准备式工作流第一阶段边界。"""

    lines = [
        "QQ/微信准备式工作流状态：第一阶段",
        "- 当前能力：/qq-open、/qq-focus、/qq-prepare-message 联系人 => 消息、/wechat-open、/wechat-focus、/wechat-prepare-message 联系人 => 消息",
    ]
    for profile in MESSAGING_APP_PROFILES.values():
        match = match_registered_app(paths, profile.app_id)
        launch_path = match.app.launch_path if match is not None else None
        path_status = (
            str(launch_path)
            if launch_path is not None
            else f"未找到，可在 config/apps.local.json 配置 {profile.app_id}.path"
        )
        lines.append(f"- {profile.display_name} 路径：{path_status}")
    lines.extend(
        [
            "- 执行动作：只显式打开应用、聚焦已有窗口，或生成未发送消息准备单。",
            "- 边界：不查找真实联系人、不点击、不输入、不发送消息、不读取聊天内容。",
        ]
    )
    return "\n".join(lines)


def open_messaging_app(
    paths: ProjectPaths,
    app_id: str,
    *,
    executor: AppLaunchExecutor | None = None,
) -> AppLaunchResult:
    """使用 AppRegistry 中的 QQ/微信路径打开应用。"""

    profile = _profile(app_id)
    try:
        return launch_registered_app(paths, profile.app_id, executor=executor)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"{profile.display_name}启动路径未找到。可在 config/apps.local.json 配置 {profile.app_id}.path。"
        ) from exc


def describe_messaging_open(
    paths: ProjectPaths,
    app_id: str,
    *,
    executor: AppLaunchExecutor | None = None,
) -> str:
    profile = _profile(app_id)
    result = open_messaging_app(paths, profile.app_id, executor=executor)
    return "\n".join(
        [
            f"{profile.display_name}打开执行：{result.app.display_name} ({result.app.app_id})",
            f"命中别名：{result.alias}",
            f"路径：{result.path}",
            f"时间：{result.executed_at.isoformat(timespec='seconds')}",
            "说明：当前阶段只打开应用，不查找联系人、不点击、不输入、不发送消息。",
        ]
    )


def describe_messaging_focus(
    paths: ProjectPaths,
    app_id: str,
    *,
    snapshot: WindowSnapshot | None = None,
    executor: WindowFocusExecutor | None = None,
) -> str:
    profile = _profile(app_id)
    try:
        focus_description = describe_window_focus(paths, profile.app_id, snapshot=snapshot, executor=executor)
    except ValueError as exc:
        raise ValueError(f"{exc} 可先执行 {profile.open_command} 打开应用。") from exc

    return "\n".join(
        [
            f"{profile.display_name}聚焦执行：",
            focus_description,
            "说明：当前阶段只聚焦已有窗口，不点击、不输入、不发送消息。",
        ]
    )


def parse_message_prepare_request(raw_request: str) -> MessageDraft:
    """解析显式消息准备单：联系人 => 消息。"""

    request = raw_request.strip()
    if "=>" not in request:
        raise ValueError("用法：联系人 => 消息")
    raw_contact, raw_message = request.split("=>", 1)
    contact = raw_contact.strip()
    message = raw_message.strip()
    if not contact:
        raise ValueError("联系人不能为空。")
    if not message:
        raise ValueError("消息内容不能为空。")
    return MessageDraft(contact=contact, message=message)


def describe_message_prepare(app_id: str, raw_request: str) -> str:
    profile = _profile(app_id)
    draft = parse_message_prepare_request(raw_request)
    return "\n".join(
        [
            f"{profile.display_name} 消息准备单：",
            f"联系人：{draft.contact}",
            f"消息：{draft.message}",
            "状态：未发送",
            "说明：当前阶段只生成准备单，不查找真实联系人、不点击、不输入、不发送消息。",
        ]
    )


def _profile(app_id: str) -> MessagingAppProfile:
    normalized_app_id = app_id.strip().casefold()
    if normalized_app_id not in MESSAGING_APP_PROFILES:
        supported = "、".join(sorted(MESSAGING_APP_PROFILES))
        raise ValueError(f"不支持的通讯应用：{app_id}。支持：{supported}")
    return MESSAGING_APP_PROFILES[normalized_app_id]
