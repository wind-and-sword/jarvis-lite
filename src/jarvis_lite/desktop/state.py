from __future__ import annotations

from enum import StrEnum


class DesktopState(StrEnum):
    """桌面助手对 UI 暴露的稳定状态。"""

    IDLE = "idle"
    THINKING = "thinking"
    WORKING = "working"
    SUCCESS = "success"
    ERROR = "error"
