from __future__ import annotations

from dataclasses import dataclass

from ..config import ProjectPaths, build_project_paths
from ..conversation import ConversationSession
from .state import DesktopState


@dataclass(frozen=True)
class DesktopResponse:
    user_input: str
    assistant_text: str
    state: DesktopState
    turn_count: int


@dataclass(frozen=True)
class QuickCommand:
    label: str
    prompt: str


DIRECT_QUICK_COMMAND_PROMPTS = ("/status", "/kb", "/dirs", "/daily-report", "/update-status")


class DesktopBridge:
    """为桌面 UI 封装现有会话核心。"""

    def __init__(self, paths: ProjectPaths | None = None):
        self.paths = paths or build_project_paths()
        self.session = ConversationSession(self.paths)
        self.state = DesktopState.IDLE

    def send(self, user_input: str) -> DesktopResponse:
        prompt = user_input.strip()
        assistant_text = self.session.handle(prompt)
        self.state = _classify_response_state(assistant_text)
        return DesktopResponse(prompt, assistant_text, self.state, len(self.session.turns))


def quick_commands() -> tuple[QuickCommand, ...]:
    """返回桌面面板第一版要展示的快捷命令。"""

    return (
        QuickCommand("状态", "/status"),
        QuickCommand("知识库", "/kb"),
        QuickCommand("常用目录", "/dirs"),
        QuickCommand("生成日报", "/daily-report"),
        QuickCommand("检查更新", "/update-status"),
        QuickCommand("整理预览", "/organize-preview"),
    )


def direct_quick_commands() -> tuple[QuickCommand, ...]:
    """返回不需要额外参数、可以直接点击执行的桌面快捷命令。"""

    return tuple(command for command in quick_commands() if command.prompt in DIRECT_QUICK_COMMAND_PROMPTS)


def _classify_response_state(assistant_text: str) -> DesktopState:
    error_prefixes = (
        "未知命令：",
        "用法：",
        "命令解析失败：",
        "导入失败：",
        "标签更新失败：",
        "语音播报失败：",
        "常用目录登记失败：",
        "日报生成失败：",
        "文件整理预览失败：",
        "打开目录请求记录失败：",
        "更新检查失败：",
        "没有找到常用目录：",
    )
    return DesktopState.ERROR if assistant_text.startswith(error_prefixes) else DesktopState.SUCCESS
