from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from ..config import ProjectPaths


RUNTIME_DIRNAME = "jarvis-lite-runtime"
SETTINGS_FILENAME = "desktop-settings.json"


@dataclass(frozen=True)
class DesktopSettings:
    position_x: int = 80
    position_y: int = 80
    always_on_top: bool = True
    opacity_percent: int = 100
    pet_size: int = 148
    panel_width: int = 420
    panel_height: int = 620


def runtime_dir(paths: ProjectPaths) -> Path:
    """返回项目外的运行时目录，避免把用户窗口位置写进 Git。"""

    return paths.root.parent / RUNTIME_DIRNAME


def desktop_settings_path(paths: ProjectPaths) -> Path:
    return runtime_dir(paths) / SETTINGS_FILENAME


def load_desktop_settings(paths: ProjectPaths) -> DesktopSettings:
    settings_path = desktop_settings_path(paths)
    if not settings_path.exists():
        return DesktopSettings()

    defaults = DesktopSettings()
    try:
        raw = json.loads(settings_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return defaults

    if not isinstance(raw, dict):
        return defaults
    return DesktopSettings(
        position_x=_read_int(raw.get("position_x"), defaults.position_x),
        position_y=_read_int(raw.get("position_y"), defaults.position_y),
        always_on_top=_read_bool(raw.get("always_on_top"), defaults.always_on_top),
        opacity_percent=_read_int(raw.get("opacity_percent"), defaults.opacity_percent),
        pet_size=_read_int(raw.get("pet_size"), defaults.pet_size),
        panel_width=_read_int(raw.get("panel_width"), defaults.panel_width),
        panel_height=_read_int(raw.get("panel_height"), defaults.panel_height),
    )


def save_desktop_settings(paths: ProjectPaths, settings: DesktopSettings) -> DesktopSettings:
    settings_path = desktop_settings_path(paths)
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(
        json.dumps(
            {
                "position_x": settings.position_x,
                "position_y": settings.position_y,
                "always_on_top": settings.always_on_top,
                "opacity_percent": settings.opacity_percent,
                "pet_size": settings.pet_size,
                "panel_width": settings.panel_width,
                "panel_height": settings.panel_height,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return settings


def save_desktop_position(paths: ProjectPaths, x: int, y: int) -> DesktopSettings:
    current = load_desktop_settings(paths)
    return save_desktop_settings(
        paths,
        DesktopSettings(
            position_x=int(x),
            position_y=int(y),
            always_on_top=current.always_on_top,
            opacity_percent=current.opacity_percent,
            pet_size=current.pet_size,
            panel_width=current.panel_width,
            panel_height=current.panel_height,
        ),
    )


def save_desktop_preferences(
    paths: ProjectPaths,
    *,
    always_on_top: bool,
    opacity_percent: int,
    pet_size: int,
) -> DesktopSettings:
    current = load_desktop_settings(paths)
    return save_desktop_settings(
        paths,
        DesktopSettings(
            position_x=current.position_x,
            position_y=current.position_y,
            always_on_top=bool(always_on_top),
            opacity_percent=int(opacity_percent),
            pet_size=int(pet_size),
            panel_width=current.panel_width,
            panel_height=current.panel_height,
        ),
    )


def save_desktop_panel_size(paths: ProjectPaths, panel_width: int, panel_height: int) -> DesktopSettings:
    current = load_desktop_settings(paths)
    return save_desktop_settings(
        paths,
        DesktopSettings(
            position_x=current.position_x,
            position_y=current.position_y,
            always_on_top=current.always_on_top,
            opacity_percent=current.opacity_percent,
            pet_size=current.pet_size,
            panel_width=int(panel_width),
            panel_height=int(panel_height),
        ),
    )


def _read_int(value: object, default: int) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else default


def _read_bool(value: object, default: bool) -> bool:
    return value if isinstance(value, bool) else default
