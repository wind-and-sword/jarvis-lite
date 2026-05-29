from __future__ import annotations

from dataclasses import dataclass


DEFAULT_THEME_NAME = "midnight"


@dataclass(frozen=True)
class DesktopTheme:
    name: str
    label: str
    panel_background: str
    panel_text: str
    panel_surface: str
    panel_border: str
    status_text: str
    input_background: str
    input_text: str
    input_border: str
    button_background: str
    button_hover: str
    button_text: str
    pet_background: str
    pet_border: str
    pet_text: str
    caption_background: str
    caption_text: str


THEME_PRESETS = {
    "midnight": DesktopTheme(
        name="midnight",
        label="深色",
        panel_background="#111827",
        panel_text="#f9fafb",
        panel_surface="#0b1220",
        panel_border="#334155",
        status_text="#93c5fd",
        input_background="#f9fafb",
        input_text="#111827",
        input_border="#94a3b8",
        button_background="#2563eb",
        button_hover="#1d4ed8",
        button_text="#ffffff",
        pet_background="#1f2937",
        pet_border="#60a5fa",
        pet_text="#f9fafb",
        caption_background="#111827",
        caption_text="#f9fafb",
    ),
    "daylight": DesktopTheme(
        name="daylight",
        label="浅色",
        panel_background="#f8fafc",
        panel_text="#0f172a",
        panel_surface="#ffffff",
        panel_border="#cbd5e1",
        status_text="#0f766e",
        input_background="#ffffff",
        input_text="#0f172a",
        input_border="#64748b",
        button_background="#0f766e",
        button_hover="#0e7490",
        button_text="#ffffff",
        pet_background="#ecfeff",
        pet_border="#0f766e",
        pet_text="#0f172a",
        caption_background="#ffffff",
        caption_text="#0f172a",
    ),
}


def desktop_theme_names() -> tuple[str, ...]:
    """返回可用桌面主题名，供设置面板填充下拉选择。"""

    return tuple(THEME_PRESETS)


def desktop_theme_label(theme_name: str) -> str:
    """返回主题显示名。"""

    return THEME_PRESETS[normalize_theme_name(theme_name)].label


def normalize_theme_name(theme_name: str | None) -> str:
    """把未知主题名回退到默认主题。"""

    return theme_name if theme_name in THEME_PRESETS else DEFAULT_THEME_NAME


def panel_style(theme_name: str | None = None) -> str:
    """生成助手面板样式表。"""

    theme = THEME_PRESETS[normalize_theme_name(theme_name)]
    return f"""
QWidget#assistantPanel {{
    background: {theme.panel_background};
    color: {theme.panel_text};
}}
QLabel#panelTitle {{
    font-size: 22px;
    font-weight: 700;
}}
QLabel#statusLabel {{
    color: {theme.status_text};
}}
QTextEdit#conversationOutput {{
    background: {theme.panel_surface};
    border: 1px solid {theme.panel_border};
    border-radius: 6px;
    color: {theme.panel_text};
    padding: 8px;
}}
QLineEdit#conversationInput {{
    background: {theme.input_background};
    border: 1px solid {theme.input_border};
    border-radius: 6px;
    color: {theme.input_text};
    padding: 8px;
}}
QLineEdit {{
    background: {theme.input_background};
    border: 1px solid {theme.input_border};
    border-radius: 6px;
    color: {theme.input_text};
    padding: 6px 8px;
}}
QPushButton {{
    background: {theme.button_background};
    border: 0;
    border-radius: 6px;
    color: {theme.button_text};
    padding: 8px 10px;
}}
QPushButton:hover {{
    background: {theme.button_hover};
}}
QComboBox {{
    background: {theme.input_background};
    border: 1px solid {theme.input_border};
    border-radius: 6px;
    color: {theme.input_text};
    padding: 4px 8px;
}}
QSpinBox {{
    background: {theme.input_background};
    border: 1px solid {theme.input_border};
    border-radius: 6px;
    color: {theme.input_text};
    padding: 4px 8px;
}}
QGroupBox {{
    border: 1px solid {theme.panel_border};
    border-radius: 6px;
    margin-top: 8px;
    padding: 8px;
}}
QGroupBox::title {{
    color: {theme.panel_text};
    left: 8px;
    padding: 0 4px;
}}
QCheckBox {{
    color: {theme.panel_text};
}}
"""


def pet_style(theme_name: str | None = None) -> str:
    """生成桌面小助手样式表。"""

    theme = THEME_PRESETS[normalize_theme_name(theme_name)]
    return f"""
QFrame#petAvatar {{
    background: {theme.pet_background};
    border: 3px solid {theme.pet_border};
    border-radius: 56px;
}}
QLabel#petAvatarLabel {{
    color: {theme.pet_text};
    font-size: 48px;
    font-weight: 800;
}}
QLabel#petCaption {{
    background: {theme.caption_background};
    border-radius: 6px;
    color: {theme.caption_text};
    padding: 4px 8px;
}}
"""


PANEL_STYLE = panel_style(DEFAULT_THEME_NAME)
PET_STYLE = pet_style(DEFAULT_THEME_NAME)
