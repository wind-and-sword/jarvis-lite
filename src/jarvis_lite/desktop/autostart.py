from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SHORTCUT_NAME = "Jarvis Lite.lnk"


@dataclass(frozen=True)
class AutostartShortcut:
    shortcut_path: Path
    target_path: Path
    working_directory: Path
    arguments: str = ""
    icon_location: Path | None = None


def windows_startup_dir(appdata: str | None = None) -> Path:
    """返回当前用户 Startup 目录，用于用户级开机启动。"""

    appdata_root = appdata or os.environ.get("APPDATA")
    if not appdata_root:
        raise RuntimeError("未找到 APPDATA，无法定位当前用户 Startup 目录。")
    return Path(appdata_root) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"


def default_autostart_shortcut(
    *,
    project_root: Path | None = None,
    startup_dir: Path | None = None,
    executable: Path | None = None,
    frozen: bool | None = None,
) -> AutostartShortcut:
    """构建默认开机启动快捷方式配置。"""

    is_frozen = bool(getattr(sys, "frozen", False)) if frozen is None else frozen
    target_path = Path(executable or sys.executable).resolve()
    root = Path(project_root or Path(__file__).resolve().parents[3]).resolve()
    shortcut_dir = Path(startup_dir or windows_startup_dir()).resolve()
    if is_frozen:
        return AutostartShortcut(
            shortcut_path=shortcut_dir / SHORTCUT_NAME,
            target_path=target_path,
            working_directory=target_path.parent,
            icon_location=target_path,
        )
    return AutostartShortcut(
        shortcut_path=shortcut_dir / SHORTCUT_NAME,
        target_path=target_path,
        working_directory=root,
        arguments="-m jarvis_lite.desktop.app",
        icon_location=target_path,
    )


def render_shortcut_powershell(shortcut: AutostartShortcut) -> str:
    """渲染创建 Windows 快捷方式的 PowerShell 脚本。"""

    icon_location = shortcut.icon_location or shortcut.target_path
    return "\n".join(
        [
            "$w = New-Object -ComObject WScript.Shell",
            f"$s = $w.CreateShortcut({_ps_quote(shortcut.shortcut_path)})",
            f"$s.TargetPath = {_ps_quote(shortcut.target_path)}",
            f"$s.WorkingDirectory = {_ps_quote(shortcut.working_directory)}",
            f"$s.Arguments = {_ps_quote(shortcut.arguments)}",
            f"$s.IconLocation = {_ps_quote(icon_location)}",
            "$s.Save()",
        ]
    )


def enable_windows_autostart(
    shortcut: AutostartShortcut | None = None,
    *,
    runner: Callable[..., Any] = subprocess.run,
) -> AutostartShortcut:
    """启用当前用户级开机启动。"""

    target = shortcut or default_autostart_shortcut()
    target.shortcut_path.parent.mkdir(parents=True, exist_ok=True)
    runner(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            render_shortcut_powershell(target),
        ],
        check=True,
    )
    return target


def disable_windows_autostart(shortcut: AutostartShortcut | None = None) -> AutostartShortcut:
    """关闭当前用户级开机启动。"""

    target = shortcut or default_autostart_shortcut()
    target.shortcut_path.unlink(missing_ok=True)
    return target


def sync_windows_autostart(
    enabled: bool,
    shortcut: AutostartShortcut | None = None,
    *,
    runner: Callable[..., Any] = subprocess.run,
) -> AutostartShortcut:
    """按设置值同步当前用户级开机启动状态。"""

    if enabled:
        return enable_windows_autostart(shortcut, runner=runner)
    return disable_windows_autostart(shortcut)


def is_windows_autostart_enabled(shortcut: AutostartShortcut | None = None) -> bool:
    """检查当前用户级开机启动快捷方式是否存在。"""

    target = shortcut or default_autostart_shortcut()
    return target.shortcut_path.exists()


def _ps_quote(value: object) -> str:
    return "'" + str(value).replace("'", "''") + "'"
