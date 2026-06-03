from __future__ import annotations

from .app_registry import AppLaunchExecutor, AppLaunchResult, launch_registered_app, match_registered_app
from .config import ProjectPaths
from .window_state import WindowFocusExecutor, WindowSnapshot, describe_window_focus


CLASH_APP_QUERY = "clash_verge"


def describe_clash_workflow_status(paths: ProjectPaths) -> str:
    """输出 Clash Verge 工作流第一阶段边界。"""

    match = match_registered_app(paths, CLASH_APP_QUERY)
    launch_path = match.app.launch_path if match is not None else None
    path_status = (
        str(launch_path)
        if launch_path is not None
        else "未找到，可在 config/apps.local.json 配置 clash_verge.path"
    )
    return "\n".join(
        [
            "Clash Verge 工作流状态：第一阶段",
            "- 当前能力：/clash-open、/clash-focus",
            f"- Clash Verge 路径：{path_status}",
            "- 执行动作：只启动代理面板，或聚焦已经存在的代理面板窗口。",
            "- 边界：不切换节点、不开关系统代理、不修改配置、不点击、不输入。",
        ]
    )


def open_clash_verge(
    paths: ProjectPaths,
    *,
    executor: AppLaunchExecutor | None = None,
) -> AppLaunchResult:
    """使用 AppRegistry 中的 Clash Verge 路径打开代理面板。"""

    try:
        return launch_registered_app(paths, CLASH_APP_QUERY, executor=executor)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            "Clash Verge 启动路径未找到。可在 config/apps.local.json 配置 clash_verge.path。"
        ) from exc


def describe_clash_open(
    paths: ProjectPaths,
    *,
    executor: AppLaunchExecutor | None = None,
) -> str:
    result = open_clash_verge(paths, executor=executor)
    return "\n".join(
        [
            f"Clash Verge 打开代理面板执行：{result.app.display_name} ({result.app.app_id})",
            f"命中别名：{result.alias}",
            f"路径：{result.path}",
            f"时间：{result.executed_at.isoformat(timespec='seconds')}",
            "说明：当前阶段只打开代理面板，不切换节点、不开关系统代理、不修改配置。",
        ]
    )


def describe_clash_focus(
    paths: ProjectPaths,
    *,
    snapshot: WindowSnapshot | None = None,
    executor: WindowFocusExecutor | None = None,
) -> str:
    try:
        focus_description = describe_window_focus(paths, CLASH_APP_QUERY, snapshot=snapshot, executor=executor)
    except ValueError as exc:
        raise ValueError(f"{exc} 可先执行 /clash-open 启动代理面板。") from exc

    return "\n".join(
        [
            "Clash Verge 聚焦执行：",
            focus_description,
            "说明：当前阶段只聚焦已有代理面板，不点击、不输入、不切换节点、不修改系统代理。",
        ]
    )
