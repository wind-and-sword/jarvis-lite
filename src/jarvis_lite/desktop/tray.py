from __future__ import annotations

import os
from typing import Any

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from .assets import desktop_app_icon_path
from .bridge import direct_quick_commands
from .widgets import DesktopPetWindow


RECENT_RESULT_EMPTY_TEXT = "最近结果（暂无）"


class DesktopTrayController:
    """管理桌面助手的系统托盘和应用生命周期。"""

    def __init__(self, app: QApplication, pet_window: DesktopPetWindow):
        self.app = app
        self.pet_window = pet_window
        self.panel = pet_window.panel
        self._quit_requested = False
        self._recent_result_text = ""

        self.app.setQuitOnLastWindowClosed(False)
        self.pet_window.set_close_to_tray_enabled(True)

        self.menu = QMenu()
        self.show_action = QAction("显示助手", self.menu)
        self.hide_action = QAction("隐藏助手", self.menu)
        self.recent_result_action = QAction(RECENT_RESULT_EMPTY_TEXT, self.menu)
        self.quit_action = QAction("退出", self.menu)
        self._quick_command_actions: dict[str, QAction] = {}

        self.show_action.triggered.connect(self.show_assistant)
        self.hide_action.triggered.connect(self.hide_assistant)
        self.recent_result_action.triggered.connect(self._show_recent_result)
        self.quit_action.triggered.connect(self.quit_application)
        self.recent_result_action.setEnabled(False)

        self.menu.addAction(self.show_action)
        self.menu.addAction(self.hide_action)
        self.menu.addSeparator()
        self._add_quick_command_actions()
        self.menu.addSeparator()
        self.menu.addAction(self.recent_result_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        icon = QIcon(str(desktop_app_icon_path()))
        self.tray_icon = QSystemTrayIcon(icon, self.app)
        self.tray_icon.setToolTip("Jarvis Lite")
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self._handle_activation)

    def show(self) -> None:
        self.tray_icon.show()

    def action_texts(self) -> tuple[str, ...]:
        return (self.show_action.text(), self.hide_action.text(), self.quit_action.text())

    def quick_command_texts(self) -> tuple[str, ...]:
        return tuple(self._quick_command_actions)

    def quick_command_action(self, label: str) -> QAction:
        return self._quick_command_actions[label]

    def recent_result_text(self) -> str:
        return self._recent_result_text

    def show_assistant(self, checked: bool = False) -> None:
        self.pet_window.show()
        if os.environ.get("QT_QPA_PLATFORM") not in {"minimal", "offscreen"}:
            self.pet_window.raise_()
            self.pet_window.activateWindow()

    def hide_assistant(self, checked: bool = False) -> None:
        self.panel.hide()
        self.pet_window.hide()

    def quit_application(self, checked: bool = False) -> None:
        self._quit_requested = True
        self.pet_window.allow_application_close()
        self.panel.close()
        self.pet_window.close()
        self.tray_icon.hide()
        self.app.quit()

    def is_quit_requested(self) -> bool:
        return self._quit_requested

    def _handle_activation(self, reason: Any) -> None:
        if reason != QSystemTrayIcon.ActivationReason.Trigger:
            return
        if self.pet_window.isVisible():
            self.hide_assistant()
            return
        self.show_assistant()

    def _add_quick_command_actions(self) -> None:
        for command in direct_quick_commands():
            action = QAction(command.label, self.menu)
            action.triggered.connect(
                lambda checked=False, label=command.label, prompt=command.prompt: self._run_quick_command(label, prompt)
            )
            self._quick_command_actions[command.label] = action
            self.menu.addAction(action)

    def _run_quick_command(self, label: str, prompt: str) -> None:
        self._show_panel()
        response = self.panel.submit_text(prompt)
        if response is not None:
            self._update_recent_result(label)

    def _show_panel(self) -> None:
        self.show_assistant()
        self.panel.show()
        if os.environ.get("QT_QPA_PLATFORM") not in {"minimal", "offscreen"}:
            self.panel.raise_()

    def _show_recent_result(self, checked: bool = False) -> None:
        if not self._recent_result_text:
            return
        self._show_panel()

    def _update_recent_result(self, label: str) -> None:
        self._recent_result_text = f"{label}\n{self.panel.last_result_text()}"
        self.recent_result_action.setText(f"最近结果：{label}")
        self.recent_result_action.setEnabled(True)
        self.tray_icon.setToolTip(f"Jarvis Lite - 最近：{label}")
