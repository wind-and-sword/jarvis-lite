from __future__ import annotations

import ctypes
import platform
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .app_registry import RegisteredApp, list_registered_apps, match_registered_app
from .config import ProjectPaths


WindowFocusExecutor = Callable[[int], None]


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


@dataclass(frozen=True)
class WindowFocusSelection:
    window: WindowInfo
    match_reason: str


@dataclass(frozen=True)
class WindowFocusResult:
    selection: WindowFocusSelection
    executed_at: datetime


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


def describe_task_window_context(paths: ProjectPaths, *, snapshot: WindowSnapshot | None = None) -> str:
    """返回任务失败复盘使用的紧凑前台窗口摘要。"""

    current_snapshot = snapshot or capture_window_snapshot(paths)
    if not current_snapshot.supported:
        reason = current_snapshot.message or "窗口枚举不可用。"
        return f"当前窗口：不可用（{reason}）"
    if current_snapshot.foreground_window is None:
        return f"当前窗口：未获取（平台：{current_snapshot.platform}，可见窗口：{len(current_snapshot.windows)} 个）"
    window = current_snapshot.foreground_window
    return f"当前窗口：{window.title} | 进程：{_process_label(window)} | 应用：{_app_label(window)}"


def select_window_focus_target(
    paths: ProjectPaths,
    snapshot: WindowSnapshot,
    target: str,
) -> WindowFocusSelection:
    """从窗口快照中选择一个显式窗口切换目标。"""

    query = target.strip()
    if not query:
        raise ValueError("窗口切换目标不能为空。")
    if not snapshot.supported:
        raise RuntimeError(snapshot.message or "当前平台不支持窗口切换。")
    if not snapshot.windows:
        raise ValueError("没有可切换窗口。请先用 /windows 查看当前窗口状态。")

    if query.isdecimal():
        index = int(query)
        if 1 <= index <= len(snapshot.windows):
            return WindowFocusSelection(snapshot.windows[index - 1], f"窗口编号：{index}")
        raise ValueError(f"窗口编号超出范围：{index}。请先用 /windows 查看当前窗口编号。")

    app_match = match_registered_app(paths, query)
    if app_match is not None:
        app_candidates = [
            WindowFocusSelection(window, f"应用：{app_match.app.display_name} ({app_match.app.app_id})")
            for window in snapshot.windows
            if window.app_id == app_match.app.app_id
        ]
        if app_candidates:
            return _single_window_focus_selection(snapshot, tuple(app_candidates))

    normalized_query = _normalize_text(query)
    title_candidates = tuple(
        WindowFocusSelection(window, f"标题包含：{query}")
        for window in snapshot.windows
        if normalized_query and normalized_query in _normalize_text(window.title)
    )
    if title_candidates:
        return _single_window_focus_selection(snapshot, title_candidates)

    process_candidates = tuple(
        WindowFocusSelection(window, f"进程包含：{query}")
        for window in snapshot.windows
        if window.process_name and normalized_query in _normalize_text(window.process_name)
    )
    if process_candidates:
        return _single_window_focus_selection(snapshot, process_candidates)

    raise ValueError(f"没有找到可切换窗口：{query}。请先用 /windows 查看当前窗口。")


def describe_window_focus(
    paths: ProjectPaths,
    target: str,
    *,
    snapshot: WindowSnapshot | None = None,
    executor: WindowFocusExecutor | None = None,
) -> str:
    """切换到显式指定窗口，并返回可复盘结果。"""

    current_snapshot = snapshot or capture_window_snapshot(paths)
    selection = select_window_focus_target(paths, current_snapshot, target)
    focus_executor = executor or _focus_window_with_user32
    focus_executor(selection.window.handle)
    result = WindowFocusResult(selection=selection, executed_at=datetime.now())
    window = result.selection.window
    return "\n".join(
        [
            f"窗口切换执行：{window.title}",
            f"匹配：{result.selection.match_reason}",
            f"进程：{_process_label(window)}",
            f"应用：{_app_label(window)}",
            f"时间：{result.executed_at.isoformat(timespec='seconds')}",
            "说明：当前阶段只切换显式窗口，不点击、不输入、不启动应用。",
        ]
    )


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


def _focus_window_with_user32(handle: int) -> None:
    if platform.system().lower() != "windows":
        raise RuntimeError("当前仅支持 Windows 窗口切换。")
    if handle <= 0:
        raise ValueError("窗口句柄无效。")

    from ctypes import wintypes

    user32 = ctypes.windll.user32
    hwnd = wintypes.HWND(handle)
    sw_restore = 9
    user32.ShowWindow(hwnd, sw_restore)
    if not user32.SetForegroundWindow(hwnd):
        raise RuntimeError("Windows 拒绝将目标窗口切到前台。")


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


def _single_window_focus_selection(
    snapshot: WindowSnapshot,
    selections: tuple[WindowFocusSelection, ...],
) -> WindowFocusSelection:
    if len(selections) == 1:
        return selections[0]

    lines = ["匹配到多个窗口，请使用 /window-focus 编号 或更具体标题："]
    for selection in selections:
        lines.append(f"  {_window_focus_candidate_line(snapshot, selection.window)}")
    raise ValueError("\n".join(lines))


def _window_focus_candidate_line(snapshot: WindowSnapshot, window: WindowInfo) -> str:
    index = next(
        (candidate_index for candidate_index, candidate in enumerate(snapshot.windows, start=1) if candidate == window),
        0,
    )
    return f"{index}. {_window_line(window)}"
