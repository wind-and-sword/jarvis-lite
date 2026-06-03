from __future__ import annotations

import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .app_registry import AppLaunchExecutor, AppLaunchResult, launch_registered_app, match_registered_app
from .config import ProjectPaths
from .window_state import WindowFocusExecutor, WindowSnapshot, describe_window_focus


IDEA_APP_QUERY = "idea"
IdeaProjectOpenExecutor = Callable[[Path, Path], None]
PROJECT_MARKERS = (
    "pyproject.toml",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "package.json",
    "Cargo.toml",
    "go.mod",
)


@dataclass(frozen=True)
class IdeaProjectOpenResult:
    app: object
    alias: str
    idea_path: Path
    project_path: Path
    executed_at: datetime


def describe_idea_workflow_status(paths: ProjectPaths) -> str:
    """输出 IDEA 工作流第一阶段边界。"""

    match = match_registered_app(paths, IDEA_APP_QUERY)
    launch_path = match.app.launch_path if match is not None else None
    path_status = str(launch_path) if launch_path is not None else "未找到，可在 config/apps.local.json 配置 idea.path"
    return "\n".join(
        [
            "IDEA 工作流状态：第一阶段",
            "- 当前能力：/idea-open、/idea-focus、/idea-open-project 项目路径、/idea-project-status [项目路径]",
            f"- IntelliJ IDEA 路径：{path_status}",
            "- 执行动作：只显式打开 IDEA、聚焦已有 IDEA 窗口，或用 IDEA 打开已存在的本地项目目录。",
            "- 项目状态：只读检查目录、.idea、.git 和常见构建文件。",
            "- 边界：不运行测试、不打开终端、不点击、不输入、不编辑项目文件。",
        ]
    )


def open_idea_app(
    paths: ProjectPaths,
    *,
    executor: AppLaunchExecutor | None = None,
) -> AppLaunchResult:
    """使用 AppRegistry 中的 IDEA 路径打开应用。"""

    try:
        return launch_registered_app(paths, IDEA_APP_QUERY, executor=executor)
    except FileNotFoundError as exc:
        raise FileNotFoundError("IDEA 启动路径未找到。可在 config/apps.local.json 配置 idea.path。") from exc


def describe_idea_open(
    paths: ProjectPaths,
    *,
    executor: AppLaunchExecutor | None = None,
) -> str:
    result = open_idea_app(paths, executor=executor)
    return "\n".join(
        [
            f"IDEA 打开执行：{result.app.display_name} ({result.app.app_id})",
            f"命中别名：{result.alias}",
            f"路径：{result.path}",
            f"时间：{result.executed_at.isoformat(timespec='seconds')}",
            "说明：当前阶段只打开 IDEA，不打开项目、不运行测试、不打开终端、不点击、不输入。",
        ]
    )


def describe_idea_focus(
    paths: ProjectPaths,
    *,
    snapshot: WindowSnapshot | None = None,
    executor: WindowFocusExecutor | None = None,
) -> str:
    try:
        focus_description = describe_window_focus(paths, IDEA_APP_QUERY, snapshot=snapshot, executor=executor)
    except ValueError as exc:
        raise ValueError(f"{exc} 可先执行 /idea-open 打开 IDEA。") from exc

    return "\n".join(
        [
            "IDEA 聚焦执行：",
            focus_description,
            "说明：当前阶段只聚焦已有 IDEA 窗口，不点击、不输入、不运行测试、不打开终端。",
        ]
    )


def open_idea_project(
    paths: ProjectPaths,
    raw_project_path: str,
    *,
    executor: IdeaProjectOpenExecutor | None = None,
) -> IdeaProjectOpenResult:
    """用 IDEA 打开一个显式本地项目目录。"""

    project_path = _resolve_project_path(paths, raw_project_path)
    if not project_path.exists():
        raise ValueError(f"项目目录不存在：{project_path}")
    if not project_path.is_dir():
        raise ValueError(f"项目路径不是目录：{project_path}")

    match = match_registered_app(paths, IDEA_APP_QUERY)
    idea_path = match.app.launch_path if match is not None else None
    if idea_path is None:
        raise FileNotFoundError("IDEA 启动路径未找到。可在 config/apps.local.json 配置 idea.path。")

    launcher = executor or _open_idea_project_with_subprocess
    launcher(idea_path, project_path)
    return IdeaProjectOpenResult(
        app=match.app,
        alias=match.alias,
        idea_path=idea_path,
        project_path=project_path,
        executed_at=datetime.now(),
    )


def describe_idea_open_project(
    paths: ProjectPaths,
    raw_project_path: str,
    *,
    executor: IdeaProjectOpenExecutor | None = None,
) -> str:
    result = open_idea_project(paths, raw_project_path, executor=executor)
    return "\n".join(
        [
            f"IDEA 打开项目执行：{result.app.display_name} ({result.app.app_id})",
            f"命中别名：{result.alias}",
            f"IDEA 路径：{result.idea_path}",
            f"项目路径：{result.project_path}",
            f"时间：{result.executed_at.isoformat(timespec='seconds')}",
            "说明：当前阶段只用 IDEA 打开显式项目目录，不运行测试、不打开终端、不点击、不输入、不编辑项目文件。",
        ]
    )


def describe_idea_project_status(paths: ProjectPaths, raw_project_path: str = "") -> str:
    """只读检查本地项目目录状态，不读取 IDE 内部内容。"""

    project_path = _resolve_project_path(paths, raw_project_path, default_to_root=True)
    lines = [
        "IDEA 项目状态：",
        f"项目路径：{project_path}",
    ]
    if not project_path.exists():
        lines.extend(
            [
                "目录：不存在",
                "说明：当前阶段只读检查本地项目目录，不运行测试、不打开终端、不读取 IDE 内容、不写项目文件。",
            ]
        )
        return "\n".join(lines)
    if not project_path.is_dir():
        lines.extend(
            [
                "目录：不是目录",
                "说明：当前阶段只读检查本地项目目录，不运行测试、不打开终端、不读取 IDE 内容、不写项目文件。",
            ]
        )
        return "\n".join(lines)

    marker_names = tuple(marker for marker in PROJECT_MARKERS if (project_path / marker).exists())
    lines.extend(
        [
            "目录：存在",
            f".idea：{'存在' if (project_path / '.idea').is_dir() else '未发现'}",
            f"Git：{'存在' if (project_path / '.git').exists() else '未发现'}",
            f"项目标记：{'、'.join(marker_names) if marker_names else '未发现'}",
            "说明：当前阶段只读检查本地项目目录，不运行测试、不打开终端、不读取 IDE 内容、不写项目文件。",
        ]
    )
    return "\n".join(lines)


def _resolve_project_path(paths: ProjectPaths, raw_project_path: str, *, default_to_root: bool = False) -> Path:
    stripped = raw_project_path.strip().strip('"').strip("'")
    if not stripped:
        if default_to_root:
            return paths.root.resolve()
        raise ValueError("项目路径不能为空。")

    project_path = Path(stripped).expanduser()
    if not project_path.is_absolute():
        project_path = paths.root / project_path
    return project_path.resolve()


def _open_idea_project_with_subprocess(idea_path: Path, project_path: Path) -> None:
    try:
        subprocess.Popen([str(idea_path), str(project_path)], cwd=str(idea_path.parent))
    except OSError as exc:
        raise RuntimeError(f"IDEA 打开项目失败：{project_path}：{exc}") from exc
