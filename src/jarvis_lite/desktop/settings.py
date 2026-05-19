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
    )


def save_desktop_position(paths: ProjectPaths, x: int, y: int) -> DesktopSettings:
    settings = DesktopSettings(int(x), int(y))
    settings_path = desktop_settings_path(paths)
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(
        json.dumps(
            {
                "position_x": settings.position_x,
                "position_y": settings.position_y,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return settings


def _read_int(value: object, default: int) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) else default
