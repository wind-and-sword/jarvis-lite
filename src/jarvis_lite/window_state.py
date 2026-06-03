from __future__ import annotations

import ctypes
import platform
from dataclasses import dataclass
from pathlib import Path

from .app_registry import RegisteredApp, list_registered_apps
from .config import ProjectPaths


@dataclass(frozen=True)
class NativeWindow:
    handle: int
    title: str
    process_id: int
    process_name: str | None = None


@dataclass(frozen=True)
class WindowInfo:
    handle: int
    title: str
    process_id: int
    process_name: str | None
    is_foreground: bool
    app_id: str | None = None
    app_display_name: str | None = None


@dataclass(frozen=True)
class WindowSnapshot:
    platform: str
    supported: bool
    foreground_window: WindowInfo | None
    windows: tuple[WindowInfo, ...]
    message: str = ""


def describe_current_windows(paths: ProjectPaths, limit: int = 10) -> str:
    """读取当前窗口快照并输出只读状态说明。"""

    return describe_window_snapshot(capture_window_snapshot(paths), limit=limit)


def capture_window_snapshot(paths: ProjectPaths) -> WindowSnapshot:
    """通过 Windows 原生 API 获取可见顶层窗口；非 Windows 返回不可用快照。"""

    platform_name = platform.system() or "unknown"
    if platform_name.lower() != "windows":
        return build_unsupported_window_snapshot(platform_name, "当前仅支持 Windows 窗口枚举。")

    try:
        windows = _enumerate_windows()
        foreground_handle = _foreground_handle()
    except OSError as exc:
        return build_unsupported_window_snapshot(platform_name, f"窗口枚举失败：{exc}")

    return build_window_snapshot(paths, windows, foreground_handle, platform_name)


def build_window_snapshot(
    paths: ProjectPaths,
    windows: tuple[NativeWindow, ...],
    foreground_handle: int | None,
    platform_name: str,
) -> WindowSnapshot:
    registered_apps = list_registered_apps(paths)
    enriched_windows = tuple(
        _enrich_window(native_window, foreground_handle, registered_apps) for native_window in windows
    )
    foreground_window = next((window for window in enriched_windows if window.is_foreground), None)
    return WindowSnapshot(
        platform=platform_name,
        supported=True,
        foreground_window=foreground_window,
        windows=enriched_windows,
    )


def build_unsupported_window_snapshot(platform_name: str, reason: str) -> WindowSnapshot:
    return WindowSnapshot(
        platform=platform_name,
        supported=False,
        foreground_window=None,
        windows=(),
        message=reason,
    )


def describe_window_snapshot(snapshot: WindowSnapshot, limit: int = 10) -> str:
    action_boundary = "说明：当前阶段只做只读观察，不切换窗口、不点击、不输入。"
    if not snapshot.supported:
        return "\n".join(
            [
                "窗口感知：不可用",
                action_boundary,
                f"- 平台：{snapshot.platform}",
                f"- 原因：{snapshot.message or '窗口枚举不可用。'}",
            ]
        )

    lines = [
        "窗口感知：",
        action_boundary,
        f"- 平台：{snapshot.platform}",
        f"- 可见窗口：{len(snapshot.windows)} 个",
    ]
    if snapshot.foreground_window is None:
        lines.append("- 前台窗口：未获取")
    else:
        lines.extend(_describe_foreground_window(snapshot.foreground_window))

    if snapshot.windows:
        lines.append("- 窗口列表：")
        for index, window in enumerate(snapshot.windows[:limit], start=1):
            lines.append(f"  {index}. {_window_line(window)}")
        if len(snapshot.windows) > limit:
            lines.append(f"  ... 还有 {len(snapshot.windows) - limit} 个窗口")
    return "\n".join(lines)


def _enrich_window(
    window: NativeWindow,
    foreground_handle: int | None,
    registered_apps: tuple[RegisteredApp, ...],
) -> WindowInfo:
    app = _match_registered_app(window, registered_apps)
    return WindowInfo(
        handle=window.handle,
        title=window.title,
        process_id=window.process_id,
        process_name=window.process_name,
        is_foreground=foreground_handle is not None and window.handle == foreground_handle,
        app_id=app.app_id if app is not None else None,
        app_display_name=app.display_name if app is not None else None,
    )


def _match_registered_app(window: NativeWindow, registered_apps: tuple[RegisteredApp, ...]) -> RegisteredApp | None:
    process_name = _normalize_executable_name(window.process_name)
    if process_name:
        for app in registered_apps:
            executable_names = _registered_executable_names(app)
            if process_name in executable_names:
                return app

    normalized_title = _normalize_text(window.title)
    for app in registered_apps:
        for alias in (app.display_name, *app.aliases):
            normalized_alias = _normalize_text(alias)
            if normalized_alias and normalized_alias in normalized_title:
                return app
    return None


def _registered_executable_names(app: RegisteredApp) -> set[str]:
    paths = [*app.executable_candidates]
    if app.configured_path is not None:
        paths.insert(0, app.configured_path)
    return {_normalize_executable_name(path.name) for path in paths if path.name}


def _describe_foreground_window(window: WindowInfo) -> list[str]:
    lines = [
        f"- 前台窗口：{window.title}",
        f"  进程：{_process_label(window)}",
    ]
    lines.append(f"  已识别应用：{_app_label(window)}")
    return lines


def _window_line(window: WindowInfo) -> str:
    return f"{window.title} | 进程：{_process_label(window)} | 应用：{_app_label(window)}"


def _process_label(window: WindowInfo) -> str:
    name = window.process_name or "未知进程"
    return f"{name} (PID {window.process_id})"


def _app_label(window: WindowInfo) -> str:
    if window.app_id is None or window.app_display_name is None:
        return "未匹配"
    return f"{window.app_display_name} ({window.app_id})"


def _enumerate_windows() -> tuple[NativeWindow, ...]:
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    windows: list[NativeWindow] = []

    enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    def callback(hwnd, _lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        length = user32.GetWindowTextLengthW(hwnd)
        if length <= 0:
            return True
        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        title = buffer.value.strip()
        if not title:
            return True
        process_id = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
        windows.append(
            NativeWindow(
                handle=int(hwnd),
                title=title,
                process_id=int(process_id.value),
                process_name=_process_name(int(process_id.value)),
            )
        )
        return True

    if not user32.EnumWindows(enum_windows_proc(callback), 0):
        raise OSError("EnumWindows 返回失败。")
    return tuple(windows)


def _foreground_handle() -> int | None:
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    return int(hwnd) if hwnd else None


def _process_name(process_id: int) -> str | None:
    from ctypes import wintypes

    if process_id <= 0:
        return None
    kernel32 = ctypes.windll.kernel32
    process_query_limited_information = 0x1000
    handle = kernel32.OpenProcess(process_query_limited_information, False, process_id)
    if not handle:
        return None
    try:
        size = wintypes.DWORD(32768)
        buffer = ctypes.create_unicode_buffer(size.value)
        if kernel32.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size)):
            return Path(buffer.value).name
    finally:
        kernel32.CloseHandle(handle)
    return None


def _normalize_executable_name(value: str | None) -> str:
    if not value:
        return ""
    return Path(value).name.strip().casefold()


def _normalize_text(value: str) -> str:
    return "".join(value.strip().casefold().split())
