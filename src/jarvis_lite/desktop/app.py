from __future__ import annotations

import argparse
import os
import sys
from typing import Any

from .bridge import DesktopBridge
from .tray import DesktopTrayController
from .widgets import AssistantPanel, DesktopPetWindow


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


def create_desktop_app(bridge: DesktopBridge | None = None) -> tuple[Any, Any]:
    from PySide6.QtGui import QFont
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(sys.argv[:1])
    app.setFont(QFont("Microsoft YaHei UI", 10))
    desktop_bridge = bridge or DesktopBridge()
    panel = AssistantPanel(desktop_bridge)
    pet_window = DesktopPetWindow(panel, desktop_bridge.paths)
    return app, pet_window


if __name__ == "__main__":
    raise SystemExit(main())
