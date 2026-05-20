from __future__ import annotations

from pathlib import Path

from .state import DesktopState


ASSETS_DIR = Path(__file__).resolve().parent / "assets"
APP_ICON_FILENAME = "app-icon.svg"

ASSET_FILENAMES = {
    DesktopState.IDLE: "idle.svg",
    DesktopState.THINKING: "thinking.svg",
    DesktopState.WORKING: "working.svg",
    DesktopState.SUCCESS: "success.svg",
    DesktopState.ERROR: "error.svg",
}


def desktop_asset_path(state: DesktopState) -> Path:
    """返回桌面小助手指定状态的项目内素材路径。"""

    return ASSETS_DIR / ASSET_FILENAMES[state]


def all_desktop_asset_paths() -> dict[DesktopState, Path]:
    """返回所有桌面小助手状态素材，供启动检查和测试使用。"""

    return {state: desktop_asset_path(state) for state in DesktopState}


def desktop_app_icon_path() -> Path:
    """返回桌面应用图标路径。"""

    return ASSETS_DIR / APP_ICON_FILENAME
