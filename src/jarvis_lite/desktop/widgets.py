from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QCloseEvent, QMouseEvent, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..config import ProjectPaths
from .app_style import PANEL_STYLE, PET_STYLE
from .assets import desktop_asset_path
from .bridge import DesktopBridge, quick_commands
from .settings import load_desktop_settings, save_desktop_position
from .state import DesktopState


STATE_CAPTIONS = {
    DesktopState.IDLE: "待命",
    DesktopState.THINKING: "思考",
    DesktopState.WORKING: "工作",
    DesktopState.SUCCESS: "完成",
    DesktopState.ERROR: "错误",
}


@dataclass(frozen=True)
class StateAnimationProfile:
    name: str
    interval_ms: int
    frame_sizes: tuple[int, ...]


STATE_ANIMATION_PROFILES = {
    DesktopState.IDLE: StateAnimationProfile("idle-breathing", 1200, (86, 88, 90, 88)),
    DesktopState.THINKING: StateAnimationProfile("thinking-pulse", 360, (86, 91, 88, 92)),
    DesktopState.WORKING: StateAnimationProfile("working-pulse", 280, (88, 94, 90, 94)),
    DesktopState.SUCCESS: StateAnimationProfile("success-bounce", 620, (88, 96, 90, 88)),
    DesktopState.ERROR: StateAnimationProfile("error-shake", 420, (88, 84, 92, 86)),
}


class AssistantPanel(QWidget):
    """桌面助手展开后的对话面板。"""

    def __init__(self, bridge: DesktopBridge):
        super().__init__()
        self.bridge = bridge
        self._state_listener: Callable[[DesktopState], None] | None = None
        self.setObjectName("assistantPanel")
        self.setWindowTitle("Jarvis Lite 助手面板")
        self.setMinimumSize(420, 620)
        self.setStyleSheet(PANEL_STYLE)

        self._status_label = QLabel("状态：idle")
        self._status_label.setObjectName("statusLabel")
        self._output = QTextEdit()
        self._output.setObjectName("conversationOutput")
        self._output.setReadOnly(True)
        self._input = QLineEdit()
        self._input.setObjectName("conversationInput")
        self._input.setPlaceholderText("输入问题或命令")

        send_button = QPushButton("发送")
        send_button.setObjectName("sendButton")
        send_button.clicked.connect(self._submit_input)
        self._input.returnPressed.connect(self._submit_input)

        input_row = QHBoxLayout()
        input_row.addWidget(self._input)
        input_row.addWidget(send_button)

        command_row = QHBoxLayout()
        for command in quick_commands():
            button = QPushButton(command.label)
            button.setObjectName(f"quickCommand_{command.prompt.strip('/').replace('-', '_')}")
            button.clicked.connect(lambda checked=False, prompt=command.prompt: self.submit_text(prompt))
            command_row.addWidget(button)

        layout = QVBoxLayout()
        title = QLabel("Jarvis Lite")
        title.setObjectName("panelTitle")
        layout.addWidget(title)
        layout.addWidget(self._status_label)
        layout.addWidget(self._output)
        layout.addLayout(input_row)
        layout.addLayout(command_row)
        self.setLayout(layout)

    def submit_text(self, text: str) -> None:
        prompt = text.strip()
        if not prompt:
            return
        self._set_state(DesktopState.WORKING if prompt.startswith("/") else DesktopState.THINKING)
        response = self.bridge.send(prompt)
        self._output.append(f"用户：{response.user_input}")
        self._output.append(f"Jarvis：{response.assistant_text}")
        self._set_state(response.state)

    def transcript_text(self) -> str:
        return self._output.toPlainText()

    def status_text(self) -> str:
        return self._status_label.text()

    def set_state_listener(self, listener: Callable[[DesktopState], None]) -> None:
        self._state_listener = listener

    def _submit_input(self) -> None:
        text = self._input.text().strip()
        if not text:
            return
        self._input.clear()
        self.submit_text(text)

    def _set_state(self, state: DesktopState) -> None:
        self._status_label.setText(f"状态：{state.value}")
        if self._state_listener is not None:
            self._state_listener(state)


class DesktopPetWindow(QWidget):
    """桌面角落常驻的小助手窗口。"""

    def __init__(self, panel: AssistantPanel, paths: ProjectPaths):
        super().__init__()
        self.panel = panel
        self.paths = paths
        self.panel.set_state_listener(self.set_state)
        self._drag_start: QPoint | None = None
        self._current_asset_path = desktop_asset_path(DesktopState.IDLE)
        self._asset_pixmap = QPixmap()
        self._animation_frame = 0
        self._current_animation_profile = STATE_ANIMATION_PROFILES[DesktopState.IDLE]
        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(self.advance_animation_frame)
        self._close_to_tray_enabled = False
        self.setObjectName("desktopPetWindow")
        self.setWindowTitle("Jarvis Lite")
        self.setFixedSize(148, 148)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self._avatar = QFrame()
        self._avatar.setObjectName("petAvatar")
        self._avatar.setFixedSize(112, 112)
        self._avatar_label = QLabel()
        self._avatar_label.setObjectName("petAvatarLabel")
        self._avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_layout = QVBoxLayout()
        avatar_layout.addWidget(self._avatar_label)
        self._avatar.setLayout(avatar_layout)

        self._caption = QLabel(STATE_CAPTIONS[DesktopState.IDLE])
        self._caption.setObjectName("petCaption")
        self._caption.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._avatar, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._caption)
        self.setLayout(layout)
        self.setStyleSheet(PET_STYLE)
        self.set_state(DesktopState.IDLE)
        settings = load_desktop_settings(self.paths)
        self.move(settings.position_x, settings.position_y)

    def set_state(self, state: DesktopState) -> None:
        self._caption.setText(STATE_CAPTIONS[state])
        self._set_asset(state)

    def caption_text(self) -> str:
        return self._caption.text()

    def current_asset_name(self) -> str:
        return self._current_asset_path.name

    def current_animation_name(self) -> str:
        return self._current_animation_profile.name

    def animation_interval_ms(self) -> int:
        return self._current_animation_profile.interval_ms

    def animation_frame(self) -> int:
        return self._animation_frame

    def advance_animation_frame(self) -> None:
        frame_count = len(self._current_animation_profile.frame_sizes)
        self._animation_frame = (self._animation_frame + 1) % frame_count
        self._render_asset()

    def persist_position(self) -> None:
        save_desktop_position(self.paths, self.x(), self.y())

    def set_close_to_tray_enabled(self, enabled: bool) -> None:
        self._close_to_tray_enabled = enabled

    def is_close_to_tray_enabled(self) -> bool:
        return self._close_to_tray_enabled

    def allow_application_close(self) -> None:
        self._close_to_tray_enabled = False

    def toggle_panel(self) -> None:
        if self.panel.isVisible():
            self.panel.hide()
            return
        self._position_panel()
        self.panel.show()
        if os.environ.get("QT_QPA_PLATFORM") not in {"minimal", "offscreen"}:
            self.panel.raise_()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._drag_start is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_start)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = None
            self.persist_position()
            self.toggle_panel()
        super().mouseReleaseEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._close_to_tray_enabled:
            self.persist_position()
            self.panel.hide()
            self.hide()
            event.ignore()
            return
        self._animation_timer.stop()
        self.persist_position()
        super().closeEvent(event)

    def _position_panel(self) -> None:
        self.panel.move(self.x() - self.panel.width() - 12, self.y())

    def _set_asset(self, state: DesktopState) -> None:
        self._current_asset_path = desktop_asset_path(state)
        self._asset_pixmap = QPixmap(str(self._current_asset_path))
        self._set_animation_profile(state)

    def _set_animation_profile(self, state: DesktopState) -> None:
        self._current_animation_profile = STATE_ANIMATION_PROFILES[state]
        self._animation_frame = 0
        self._animation_timer.start(self._current_animation_profile.interval_ms)
        self._render_asset()

    def _render_asset(self) -> None:
        if not self._asset_pixmap.isNull():
            size = self._current_animation_profile.frame_sizes[self._animation_frame]
            self._avatar_label.setPixmap(
                self._asset_pixmap.scaled(
                    size,
                    size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            self._avatar_label.setText("")
            return
        self._avatar_label.clear()
        self._avatar_label.setText("J")
