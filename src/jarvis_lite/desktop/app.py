from __future__ import annotations

import argparse
import sys
from typing import Any

from .bridge import DesktopBridge, quick_commands


APP_TITLE = "Jarvis Lite 桌面助手"


def build_window_title() -> str:
    return APP_TITLE


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=APP_TITLE)
    parser.add_argument("--smoke", action="store_true", help="加载桌面依赖后立即退出，用于本地自动化验证。")
    args = parser.parse_args(argv)

    if args.smoke:
        ensure_qt_available()
        print(APP_TITLE)
        return 0

    app, window = create_desktop_app()
    window.show()
    return app.exec()


def ensure_qt_available() -> None:
    from PySide6 import QtWidgets  # noqa: F401


def create_desktop_app(bridge: DesktopBridge | None = None) -> tuple[Any, Any]:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QApplication,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QPushButton,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

    class DesktopAssistantWindow(QWidget):
        """第一版桌面助手面板，后续再拆成独立 widget 模块。"""

        def __init__(self, desktop_bridge: DesktopBridge):
            super().__init__()
            self.bridge = desktop_bridge
            self.setWindowTitle(APP_TITLE)
            self.setMinimumSize(420, 620)
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

            self.status_label = QLabel("状态：idle")
            self.output = QTextEdit()
            self.output.setReadOnly(True)
            self.input = QLineEdit()
            self.input.setPlaceholderText("输入问题或命令")

            send_button = QPushButton("发送")
            send_button.clicked.connect(self._send_input)
            self.input.returnPressed.connect(self._send_input)

            input_row = QHBoxLayout()
            input_row.addWidget(self.input)
            input_row.addWidget(send_button)

            command_row = QHBoxLayout()
            for command in quick_commands():
                button = QPushButton(command.label)
                button.clicked.connect(lambda checked=False, prompt=command.prompt: self._send(prompt))
                command_row.addWidget(button)

            layout = QVBoxLayout()
            layout.addWidget(QLabel("Jarvis Lite"))
            layout.addWidget(self.status_label)
            layout.addWidget(self.output)
            layout.addLayout(input_row)
            layout.addLayout(command_row)
            self.setLayout(layout)

        def _send_input(self) -> None:
            text = self.input.text().strip()
            if not text:
                return
            self.input.clear()
            self._send(text)

        def _send(self, text: str) -> None:
            self.status_label.setText("状态：working" if text.startswith("/") else "状态：thinking")
            response = self.bridge.send(text)
            self.output.append(f"用户：{response.user_input}")
            self.output.append(f"Jarvis：{response.assistant_text}")
            self.status_label.setText(f"状态：{response.state.value}")

    app = QApplication.instance() or QApplication(sys.argv[:1])
    window = DesktopAssistantWindow(bridge or DesktopBridge())
    return app, window


if __name__ == "__main__":
    raise SystemExit(main())
