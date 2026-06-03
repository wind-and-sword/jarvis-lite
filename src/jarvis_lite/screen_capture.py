from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .config import ProjectPaths


ScreenCapturer = Callable[[Path], tuple[int, int]]


@dataclass(frozen=True)
class ScreenCaptureResult:
    path: Path
    relative_path: str
    width: int
    height: int
    captured_at: datetime


def save_screen_capture(
    paths: ProjectPaths,
    filename: str | None = None,
    *,
    capturer: ScreenCapturer | None = None,
) -> ScreenCaptureResult:
    """保存当前主屏幕截图到 logs/screenshots。"""

    target_path = _screenshot_path(paths, filename)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    captured_at = datetime.now()
    width, height = (capturer or _capture_primary_screen)(target_path)
    if not target_path.is_file():
        raise RuntimeError(f"截图保存失败，未生成文件：{target_path}")
    return ScreenCaptureResult(
        path=target_path,
        relative_path=target_path.relative_to(paths.root).as_posix(),
        width=width,
        height=height,
        captured_at=captured_at,
    )


def describe_screen_capture(
    paths: ProjectPaths,
    filename: str | None = None,
    *,
    capturer: ScreenCapturer | None = None,
) -> str:
    result = save_screen_capture(paths, filename, capturer=capturer)
    return "\n".join(
        [
            f"已保存屏幕截图：{result.relative_path}",
            f"尺寸：{result.width}x{result.height}",
            "说明：当前阶段只截图保存，不 OCR、不点击、不切换窗口。",
        ]
    )


def _screenshot_path(paths: ProjectPaths, filename: str | None) -> Path:
    return paths.logs_dir / "screenshots" / _screenshot_filename(filename)


def _screenshot_filename(filename: str | None) -> str:
    if filename is None or not filename.strip():
        if filename is not None:
            raise ValueError("截图文件名不能为空。")
        return f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-screen.png"

    name = Path(filename.strip()).name
    if not name:
        raise ValueError("截图文件名不能为空。")
    return name if name.lower().endswith(".png") else f"{name}.png"


def _capture_primary_screen(target_path: Path) -> tuple[int, int]:
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication(sys.argv[:1])
    screen = app.primaryScreen()
    if screen is None:
        raise RuntimeError("截图失败：未找到主屏幕。")

    pixmap = screen.grabWindow(0)
    if pixmap.isNull():
        raise RuntimeError("截图失败：主屏幕返回空图像。")
    if not pixmap.save(str(target_path), "PNG"):
        raise RuntimeError(f"截图保存失败：{target_path}")
    return pixmap.width(), pixmap.height()
