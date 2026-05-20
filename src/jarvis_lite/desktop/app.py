from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

from .. import __version__
from .autostart import default_autostart_shortcut, sync_windows_autostart
from .bridge import DesktopBridge
from .assets import desktop_app_icon_path
from .settings import DesktopSettings, load_desktop_settings
from .tray import DesktopTrayController
from .widgets import AssistantPanel, DesktopPetWindow


APP_NAME = "Jarvis Lite"
APP_TITLE = "Jarvis Lite 桌面助手"


def build_window_title() -> str:
    return APP_TITLE


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=APP_TITLE)
    parser.add_argument("--smoke", action="store_true", help="加载桌面依赖后立即退出，用于本地自动化验证。")
    args = parser.parse_args(argv)

    if args.smoke:
        os.environ.setdefault("QT_QPA_PLATFORM", "minimal")
        app, window = create_desktop_app()
        print(APP_TITLE)
        print(window.objectName())
        window.close()
        app.quit()
        return 0

    app, window = create_desktop_app()
    tray = DesktopTrayController(app, window)
    tray.show()
    window.show()
    return app.exec()


def ensure_qt_available() -> None:
    from PySide6 import QtWidgets  # noqa: F401


def apply_panel_settings(
    values: DesktopSettings,
    pet_window: DesktopPetWindow,
    project_root: Path,
    *,
    syncer=sync_windows_autostart,
) -> None:
    """应用面板设置，并同步当前用户级开机启动。"""

    previous_launch_at_login = load_desktop_settings(pet_window.paths).launch_at_login
    pet_window.apply_preferences(
        always_on_top=values.always_on_top,
        opacity_percent=values.opacity_percent,
        pet_size=values.pet_size,
        launch_at_login=values.launch_at_login,
        theme_name=values.theme_name,
    )
    if values.launch_at_login != previous_launch_at_login:
        syncer(values.launch_at_login, default_autostart_shortcut(project_root=project_root))


def create_desktop_app(bridge: DesktopBridge | None = None) -> tuple[Any, Any]:
    from PySide6.QtGui import QFont, QIcon
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(sys.argv[:1])
    app_icon = QIcon(str(desktop_app_icon_path()))
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(__version__)
    app.setOrganizationName(APP_NAME)
    app.setFont(QFont("Microsoft YaHei UI", 10))
    app.setWindowIcon(app_icon)
    desktop_bridge = bridge or DesktopBridge()
    settings = load_desktop_settings(desktop_bridge.paths)
    panel = AssistantPanel(desktop_bridge, settings)
    pet_window = DesktopPetWindow(panel, desktop_bridge.paths)
    panel.setWindowIcon(app_icon)
    pet_window.setWindowIcon(app_icon)
    panel.set_settings_listener(lambda values: apply_panel_settings(values, pet_window, desktop_bridge.paths.root))
    return app, pet_window


if __name__ == "__main__":
    raise SystemExit(main())
