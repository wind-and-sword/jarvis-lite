from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QCloseEvent, QMouseEvent, QPixmap, QResizeEvent
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..config import ProjectPaths
from ..llm import LLMSettings
from ..search import SearchSettings
from .app_style import (
    DEFAULT_THEME_NAME,
    desktop_theme_label,
    desktop_theme_names,
    normalize_theme_name,
    panel_style,
    pet_style,
)
from .assets import desktop_asset_path
from .bridge import DesktopBridge, DesktopResponse, direct_quick_commands
from .settings import (
    DesktopSettings,
    load_desktop_settings,
    save_desktop_panel_size,
    save_desktop_position,
    save_desktop_settings,
)
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

DEFAULT_PET_SIZE = 148
DEFAULT_AVATAR_SIZE = 112
MIN_PANEL_WIDTH = 420
MIN_PANEL_HEIGHT = 520
MAX_PANEL_WIDTH = 980
MAX_PANEL_HEIGHT = 900
MIN_OPACITY_PERCENT = 50
MAX_OPACITY_PERCENT = 100
MIN_PET_SIZE = 120
MAX_PET_SIZE = 220
LLM_PROVIDER_OPTIONS = ("off", "fake", "openai", "openai-compatible", "qwen", "gemini")
SEARCH_PROVIDER_OPTIONS = ("off", "fake", "tavily")
DEFAULT_DESKTOP_LLM_PROVIDER = "openai-compatible"
DEFAULT_DESKTOP_SEARCH_PROVIDER = "tavily"
MAX_SEARCH_RESULTS = 50


class AssistantPanel(QWidget):
    """桌面助手展开后的对话面板。"""

    def __init__(self, bridge: DesktopBridge, settings: DesktopSettings | None = None):
        super().__init__()
        initial_settings = settings or DesktopSettings()
        self.bridge = bridge
        self._state_listener: Callable[[DesktopState], None] | None = None
        self._settings_listener: Callable[[DesktopSettings], None] | None = None
        self._settings_position_x = initial_settings.position_x
        self._settings_position_y = initial_settings.position_y
        self._theme_name = normalize_theme_name(initial_settings.theme_name)
        self._last_result_text = ""
        self._persist_panel_size_enabled = False
        self.setObjectName("assistantPanel")
        self.setWindowTitle("Jarvis Lite 助手面板")
        self.setMinimumSize(MIN_PANEL_WIDTH, MIN_PANEL_HEIGHT)
        self.setMaximumSize(MAX_PANEL_WIDTH, MAX_PANEL_HEIGHT)
        self.setStyleSheet(panel_style(self._theme_name))

        self._status_label = QLabel("状态：idle")
        self._status_label.setObjectName("statusLabel")
        self._llm_pending_status_label = QLabel(self.bridge.llm_pending_status_text())
        self._llm_pending_status_label.setObjectName("llmPendingStatusLabel")
        self._llm_pending_status_label.setWordWrap(True)
        self._llm_activity_status_label = QLabel(self.bridge.llm_activity_status_text())
        self._llm_activity_status_label.setObjectName("llmActivityStatusLabel")
        self._llm_activity_status_label.setWordWrap(True)
        self._route_status_label = QLabel(self.bridge.route_status_text())
        self._route_status_label.setObjectName("routeStatusLabel")
        self._route_status_label.setWordWrap(True)
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
        self._quick_command_buttons: dict[str, QPushButton] = {}
        for command in direct_quick_commands():
            button = QPushButton(command.label)
            button.setObjectName(f"quickCommand_{command.prompt.strip('/').replace('-', '_')}")
            button.clicked.connect(lambda checked=False, prompt=command.prompt: self.submit_text(prompt))
            self._quick_command_buttons[command.label] = button
            command_row.addWidget(button)

        provider_config_area = self._build_provider_config_area()
        settings_row = self._build_settings_row(initial_settings)

        layout = QVBoxLayout()
        title = QLabel("Jarvis Lite")
        title.setObjectName("panelTitle")
        layout.addWidget(title)
        layout.addWidget(self._status_label)
        layout.addWidget(self._llm_pending_status_label)
        layout.addWidget(self._llm_activity_status_label)
        layout.addWidget(self._route_status_label)
        layout.addWidget(self._output)
        layout.addLayout(input_row)
        layout.addLayout(command_row)
        layout.addWidget(provider_config_area)
        layout.addLayout(settings_row)
        self.setLayout(layout)
        self.resize(
            _clamp_int(initial_settings.panel_width, MIN_PANEL_WIDTH, MAX_PANEL_WIDTH),
            _clamp_int(initial_settings.panel_height, MIN_PANEL_HEIGHT, MAX_PANEL_HEIGHT),
        )
        self._persist_panel_size_enabled = True

    def submit_text(self, text: str) -> DesktopResponse | None:
        prompt = text.strip()
        if not prompt:
            return None
        self._set_state(DesktopState.WORKING if prompt.startswith("/") else DesktopState.THINKING)
        response = self.bridge.send(prompt)
        self._append_response(response)
        return response

    def submit_sensitive_text(self, command: str, display_text: str) -> DesktopResponse | None:
        prompt = command.strip()
        if not prompt:
            return None
        self._set_state(DesktopState.WORKING)
        response = self.bridge.send_sensitive(prompt, display_text)
        self._append_response(response)
        return response

    def _append_response(self, response: DesktopResponse) -> None:
        user_line = f"用户：{response.user_input}"
        assistant_line = f"Jarvis：{response.assistant_text}"
        self._output.append(user_line)
        self._output.append(assistant_line)
        self._last_result_text = f"{user_line}\n{assistant_line}"
        self._llm_pending_status_label.setText(response.llm_pending_status_text)
        self._llm_activity_status_label.setText(response.llm_activity_status_text)
        self._route_status_label.setText(response.route_status_text)
        self._set_state(response.state)

    def transcript_text(self) -> str:
        return self._output.toPlainText()

    def last_result_text(self) -> str:
        return self._last_result_text

    def quick_command_texts(self) -> tuple[str, ...]:
        return tuple(self._quick_command_buttons)

    def quick_command_button(self, label: str) -> QPushButton:
        return self._quick_command_buttons[label]

    def status_text(self) -> str:
        return self._status_label.text()

    def llm_pending_status_text(self) -> str:
        return self._llm_pending_status_label.text()

    def llm_activity_status_text(self) -> str:
        return self._llm_activity_status_label.text()

    def route_status_text(self) -> str:
        return self._route_status_label.text()

    def set_state_listener(self, listener: Callable[[DesktopState], None]) -> None:
        self._state_listener = listener

    def set_settings_listener(self, listener: Callable[[DesktopSettings], None]) -> None:
        self._settings_listener = listener

    def settings_values(self) -> DesktopSettings:
        return DesktopSettings(
            position_x=self._settings_position_x,
            position_y=self._settings_position_y,
            always_on_top=self._always_on_top_checkbox.isChecked(),
            opacity_percent=self._opacity_slider.value(),
            pet_size=self._pet_size_slider.value(),
            launch_at_login=self._launch_at_login_checkbox.isChecked(),
            theme_name=normalize_theme_name(self._theme_select.currentData()),
            panel_width=_clamp_int(self.width(), MIN_PANEL_WIDTH, MAX_PANEL_WIDTH),
            panel_height=_clamp_int(self.height(), MIN_PANEL_HEIGHT, MAX_PANEL_HEIGHT),
        )

    def provider_config_values(self) -> dict[str, dict[str, object]]:
        return {
            "llm": {
                "provider": str(self._llm_provider_select.currentData()),
                "model": self._llm_model_input.text().strip(),
                "base_url": self._llm_base_url_input.text().strip(),
                "api_key": self._llm_api_key_input.text().strip(),
            },
            "search": {
                "provider": str(self._search_provider_select.currentData()),
                "api_key": self._search_api_key_input.text().strip(),
                "base_url": self._search_base_url_input.text().strip(),
                "max_results": self._search_max_results_input.value(),
            },
        }

    def change_llm_provider_config(self, *, provider: str, model: str, base_url: str, api_key: str) -> None:
        self._set_combo_data(self._llm_provider_select, provider)
        self._llm_model_input.setText(model)
        self._llm_base_url_input.setText(base_url)
        self._llm_api_key_input.setText(api_key)

    def change_search_provider_config(self, *, provider: str, api_key: str, base_url: str, max_results: int) -> None:
        self._set_combo_data(self._search_provider_select, provider)
        self._search_api_key_input.setText(api_key)
        self._search_base_url_input.setText(base_url)
        self._search_max_results_input.setValue(_clamp_int(max_results, 1, MAX_SEARCH_RESULTS))

    def write_llm_provider_config(self) -> DesktopResponse | None:
        return self.submit_sensitive_text(self._llm_config_set_command(), "写入外脑配置（api_key 已隐藏）")

    def write_search_provider_config(self) -> DesktopResponse | None:
        return self.submit_sensitive_text(self._search_config_set_command(), "写入联网搜索配置（api_key 已隐藏）")

    def check_llm_provider_config(self) -> DesktopResponse | None:
        return self.submit_text("/llm-config-check")

    def smoke_llm_provider(self) -> DesktopResponse | None:
        return self.submit_text("/llm-smoke 请用一句话确认连接可用")

    def check_search_provider_config(self) -> DesktopResponse | None:
        return self.submit_text("/search-config-check")

    def smoke_search_provider(self) -> DesktopResponse | None:
        return self.submit_text("/search-smoke Python 版本")

    def change_settings(
        self,
        *,
        always_on_top: bool,
        opacity_percent: int,
        pet_size: int,
        launch_at_login: bool | None = None,
        theme_name: str | None = None,
    ) -> None:
        self._set_settings_controls(always_on_top, opacity_percent, pet_size, theme_name or self._theme_name)
        if launch_at_login is not None:
            self._launch_at_login_checkbox.blockSignals(True)
            self._launch_at_login_checkbox.setChecked(launch_at_login)
            self._launch_at_login_checkbox.blockSignals(False)
        self._emit_settings_changed()

    def persist_size(self) -> DesktopSettings:
        return save_desktop_panel_size(
            self.bridge.paths,
            _clamp_int(self.width(), MIN_PANEL_WIDTH, MAX_PANEL_WIDTH),
            _clamp_int(self.height(), MIN_PANEL_HEIGHT, MAX_PANEL_HEIGHT),
        )

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        if self._persist_panel_size_enabled:
            self.persist_size()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._persist_panel_size_enabled:
            self.persist_size()
        super().closeEvent(event)

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

    def _build_settings_row(self, settings: DesktopSettings) -> QHBoxLayout:
        self._always_on_top_checkbox = QCheckBox("置顶")
        self._always_on_top_checkbox.setObjectName("alwaysOnTopToggle")
        self._launch_at_login_checkbox = QCheckBox("开机启动")
        self._launch_at_login_checkbox.setObjectName("launchAtLoginToggle")
        self._theme_select = QComboBox()
        self._theme_select.setObjectName("themePresetSelect")
        for theme_name in desktop_theme_names():
            self._theme_select.addItem(desktop_theme_label(theme_name), theme_name)
        self._opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self._opacity_slider.setObjectName("opacitySlider")
        self._opacity_slider.setRange(MIN_OPACITY_PERCENT, MAX_OPACITY_PERCENT)
        self._pet_size_slider = QSlider(Qt.Orientation.Horizontal)
        self._pet_size_slider.setObjectName("petSizeSlider")
        self._pet_size_slider.setRange(MIN_PET_SIZE, MAX_PET_SIZE)
        self._set_settings_controls(settings.always_on_top, settings.opacity_percent, settings.pet_size, settings.theme_name)
        self._launch_at_login_checkbox.setChecked(settings.launch_at_login)
        self._always_on_top_checkbox.stateChanged.connect(lambda value: self._emit_settings_changed())
        self._launch_at_login_checkbox.stateChanged.connect(lambda value: self._emit_settings_changed())
        self._theme_select.currentIndexChanged.connect(lambda value: self._emit_settings_changed())
        self._opacity_slider.valueChanged.connect(lambda value: self._emit_settings_changed())
        self._pet_size_slider.valueChanged.connect(lambda value: self._emit_settings_changed())

        settings_row = QHBoxLayout()
        settings_row.addWidget(QLabel("设置"))
        settings_row.addWidget(self._always_on_top_checkbox)
        settings_row.addWidget(self._launch_at_login_checkbox)
        settings_row.addWidget(QLabel("主题"))
        settings_row.addWidget(self._theme_select)
        settings_row.addWidget(QLabel("透明度"))
        settings_row.addWidget(self._opacity_slider)
        settings_row.addWidget(QLabel("尺寸"))
        settings_row.addWidget(self._pet_size_slider)
        return settings_row

    def _build_provider_config_area(self) -> QWidget:
        llm_settings = LLMSettings.from_sources(self.bridge.paths)
        search_settings = SearchSettings.from_sources(self.bridge.paths)

        self._llm_provider_select = QComboBox()
        self._llm_provider_select.setObjectName("llmProviderSelect")
        for provider in LLM_PROVIDER_OPTIONS:
            self._llm_provider_select.addItem(provider, provider)
        self._set_combo_data(
            self._llm_provider_select,
            llm_settings.provider if llm_settings.config_source or llm_settings.enabled else DEFAULT_DESKTOP_LLM_PROVIDER,
        )
        self._llm_model_input = QLineEdit(llm_settings.model)
        self._llm_model_input.setObjectName("llmModelInput")
        self._llm_model_input.setPlaceholderText("model")
        self._llm_base_url_input = QLineEdit(llm_settings.base_url)
        self._llm_base_url_input.setObjectName("llmBaseUrlInput")
        self._llm_base_url_input.setPlaceholderText("base_url 或完整 /v1/responses URL")
        self._llm_api_key_input = QLineEdit()
        self._llm_api_key_input.setObjectName("llmApiKeyInput")
        self._llm_api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._llm_api_key_input.setPlaceholderText("api_key（留空保留已有值）")

        llm_write_button = QPushButton("写入外脑")
        llm_write_button.setObjectName("llmConfigWriteButton")
        llm_write_button.clicked.connect(lambda checked=False: self.write_llm_provider_config())
        llm_check_button = QPushButton("检查")
        llm_check_button.setObjectName("llmConfigCheckButton")
        llm_check_button.clicked.connect(lambda checked=False: self.check_llm_provider_config())
        llm_smoke_button = QPushButton("测试")
        llm_smoke_button.setObjectName("llmSmokeButton")
        llm_smoke_button.clicked.connect(lambda checked=False: self.smoke_llm_provider())

        llm_group = QGroupBox("外脑")
        llm_group.setObjectName("llmConfigGroup")
        llm_layout = QVBoxLayout()
        llm_provider_row = QHBoxLayout()
        llm_provider_row.addWidget(QLabel("Provider"))
        llm_provider_row.addWidget(self._llm_provider_select)
        llm_provider_row.addWidget(QLabel("Model"))
        llm_provider_row.addWidget(self._llm_model_input)
        llm_layout.addLayout(llm_provider_row)
        llm_layout.addWidget(self._llm_base_url_input)
        llm_layout.addWidget(self._llm_api_key_input)
        llm_button_row = QHBoxLayout()
        llm_button_row.addWidget(llm_write_button)
        llm_button_row.addWidget(llm_check_button)
        llm_button_row.addWidget(llm_smoke_button)
        llm_layout.addLayout(llm_button_row)
        llm_group.setLayout(llm_layout)

        self._search_provider_select = QComboBox()
        self._search_provider_select.setObjectName("searchProviderSelect")
        for provider in SEARCH_PROVIDER_OPTIONS:
            self._search_provider_select.addItem(provider, provider)
        self._set_combo_data(
            self._search_provider_select,
            search_settings.provider if search_settings.config_source or search_settings.enabled else DEFAULT_DESKTOP_SEARCH_PROVIDER,
        )
        self._search_api_key_input = QLineEdit()
        self._search_api_key_input.setObjectName("searchApiKeyInput")
        self._search_api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._search_api_key_input.setPlaceholderText("api_key（留空保留已有值）")
        self._search_base_url_input = QLineEdit(search_settings.base_url)
        self._search_base_url_input.setObjectName("searchBaseUrlInput")
        self._search_base_url_input.setPlaceholderText("base_url（通常留空）")
        self._search_max_results_input = QSpinBox()
        self._search_max_results_input.setObjectName("searchMaxResultsInput")
        self._search_max_results_input.setRange(1, MAX_SEARCH_RESULTS)
        self._search_max_results_input.setValue(_clamp_int(search_settings.max_results, 1, MAX_SEARCH_RESULTS))

        search_write_button = QPushButton("写入搜索")
        search_write_button.setObjectName("searchConfigWriteButton")
        search_write_button.clicked.connect(lambda checked=False: self.write_search_provider_config())
        search_check_button = QPushButton("检查")
        search_check_button.setObjectName("searchConfigCheckButton")
        search_check_button.clicked.connect(lambda checked=False: self.check_search_provider_config())
        search_smoke_button = QPushButton("测试")
        search_smoke_button.setObjectName("searchSmokeButton")
        search_smoke_button.clicked.connect(lambda checked=False: self.smoke_search_provider())

        search_group = QGroupBox("联网搜索")
        search_group.setObjectName("searchConfigGroup")
        search_layout = QVBoxLayout()
        search_provider_row = QHBoxLayout()
        search_provider_row.addWidget(QLabel("Provider"))
        search_provider_row.addWidget(self._search_provider_select)
        search_provider_row.addWidget(QLabel("Max"))
        search_provider_row.addWidget(self._search_max_results_input)
        search_layout.addLayout(search_provider_row)
        search_layout.addWidget(self._search_base_url_input)
        search_layout.addWidget(self._search_api_key_input)
        search_button_row = QHBoxLayout()
        search_button_row.addWidget(search_write_button)
        search_button_row.addWidget(search_check_button)
        search_button_row.addWidget(search_smoke_button)
        search_layout.addLayout(search_button_row)
        search_group.setLayout(search_layout)

        area = QWidget()
        area.setObjectName("providerConfigArea")
        area_layout = QHBoxLayout()
        area_layout.addWidget(llm_group)
        area_layout.addWidget(search_group)
        area.setLayout(area_layout)
        return area

    def _llm_config_set_command(self) -> str:
        values = self.provider_config_values()["llm"]
        parts = [
            f"provider={values['provider']}",
            f"model={values['model']}",
            f"base_url={values['base_url']}",
        ]
        api_key = str(values["api_key"])
        if api_key:
            parts.append(f"api_key={api_key}")
        return "/llm-config-set " + " ".join(parts)

    def _search_config_set_command(self) -> str:
        values = self.provider_config_values()["search"]
        parts = [
            f"provider={values['provider']}",
            f"base_url={values['base_url']}",
            f"max_results={values['max_results']}",
        ]
        api_key = str(values["api_key"])
        if api_key:
            parts.append(f"api_key={api_key}")
        return "/search-config-set " + " ".join(parts)

    def _set_settings_controls(self, always_on_top: bool, opacity_percent: int, pet_size: int, theme_name: str | None = None) -> None:
        controls = (
            self._always_on_top_checkbox,
            self._launch_at_login_checkbox,
            self._theme_select,
            self._opacity_slider,
            self._pet_size_slider,
        )
        for control in controls:
            control.blockSignals(True)
        self._always_on_top_checkbox.setChecked(always_on_top)
        self._set_theme_selection(theme_name or DEFAULT_THEME_NAME)
        self._opacity_slider.setValue(_clamp_int(opacity_percent, MIN_OPACITY_PERCENT, MAX_OPACITY_PERCENT))
        self._pet_size_slider.setValue(_clamp_int(pet_size, MIN_PET_SIZE, MAX_PET_SIZE))
        for control in controls:
            control.blockSignals(False)

    def _emit_settings_changed(self) -> None:
        self.apply_theme(self.settings_values().theme_name)
        if self._settings_listener is not None:
            self._settings_listener(self.settings_values())

    def apply_theme(self, theme_name: str) -> None:
        self._theme_name = normalize_theme_name(theme_name)
        self.setStyleSheet(panel_style(self._theme_name))

    def _set_theme_selection(self, theme_name: str) -> None:
        normalized_theme = normalize_theme_name(theme_name)
        for index in range(self._theme_select.count()):
            if self._theme_select.itemData(index) == normalized_theme:
                self._theme_select.setCurrentIndex(index)
                return
        self._theme_select.setCurrentIndex(0)

    def _set_combo_data(self, combo: QComboBox, value: str) -> None:
        for index in range(combo.count()):
            if combo.itemData(index) == value:
                combo.setCurrentIndex(index)
                return
        combo.setCurrentIndex(0)


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
        self._always_on_top = True
        self._opacity_percent = 100
        self._pet_size = DEFAULT_PET_SIZE
        self._theme_name = DEFAULT_THEME_NAME
        self.setObjectName("desktopPetWindow")
        self.setWindowTitle("Jarvis Lite")
        self.setFixedSize(DEFAULT_PET_SIZE, DEFAULT_PET_SIZE)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self._avatar = QFrame()
        self._avatar.setObjectName("petAvatar")
        self._avatar.setFixedSize(DEFAULT_AVATAR_SIZE, DEFAULT_AVATAR_SIZE)
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
        self.setStyleSheet(pet_style(self._theme_name))
        self.set_state(DesktopState.IDLE)
        settings = load_desktop_settings(self.paths)
        self.move(settings.position_x, settings.position_y)
        self.apply_settings(settings)

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

    def apply_settings(self, settings: DesktopSettings) -> None:
        self._always_on_top = settings.always_on_top
        self._opacity_percent = _clamp_int(settings.opacity_percent, MIN_OPACITY_PERCENT, MAX_OPACITY_PERCENT)
        self._pet_size = _clamp_int(settings.pet_size, MIN_PET_SIZE, MAX_PET_SIZE)
        self._theme_name = normalize_theme_name(settings.theme_name)
        self._apply_window_preferences()

    def apply_preferences(
        self,
        *,
        always_on_top: bool,
        opacity_percent: int,
        pet_size: int,
        launch_at_login: bool | None = None,
        theme_name: str | None = None,
    ) -> None:
        current = load_desktop_settings(self.paths)
        settings = save_desktop_settings(
            self.paths,
            DesktopSettings(
                position_x=self.x(),
                position_y=self.y(),
                always_on_top=always_on_top,
                opacity_percent=opacity_percent,
                pet_size=pet_size,
                launch_at_login=current.launch_at_login if launch_at_login is None else bool(launch_at_login),
                theme_name=current.theme_name if theme_name is None else normalize_theme_name(theme_name),
                panel_width=current.panel_width,
                panel_height=current.panel_height,
            ),
        )
        self.apply_settings(settings)

    def current_opacity_percent(self) -> int:
        return self._opacity_percent

    def current_pet_size(self) -> int:
        return self._pet_size

    def current_theme_name(self) -> str:
        return self._theme_name

    def is_always_on_top(self) -> bool:
        return self._always_on_top

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

    def _apply_window_preferences(self) -> None:
        was_visible = self.isVisible()
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
        if self._always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setWindowOpacity(self._opacity_percent / 100)
        self.setFixedSize(self._pet_size, self._pet_size)
        self.setStyleSheet(pet_style(self._theme_name))
        avatar_size = round(DEFAULT_AVATAR_SIZE * self._pet_size / DEFAULT_PET_SIZE)
        self._avatar.setFixedSize(avatar_size, avatar_size)
        self._render_asset()
        if was_visible:
            self.show()

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
            base_size = self._current_animation_profile.frame_sizes[self._animation_frame]
            size = round(base_size * self._pet_size / DEFAULT_PET_SIZE)
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


def _clamp_int(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(value)))
