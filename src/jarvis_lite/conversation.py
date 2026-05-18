from __future__ import annotations

import shlex
from dataclasses import dataclass

from .agent import JarvisAgent
from .config import ProjectPaths
from .tools import ToolRegistry


@dataclass(frozen=True)
class ConversationTurn:
    user: str
    assistant: str


class ConversationSession:
    """管理一次命令行会话中的多轮对话和会话总结。"""

    def __init__(self, paths: ProjectPaths):
        self.paths = paths
        self.agent = JarvisAgent(paths)
        self.tools = ToolRegistry(paths)
        self.turns: list[ConversationTurn] = []

    def handle(self, user_input: str) -> str:
        prompt = user_input.strip()
        if not prompt:
            return self.agent.handle(prompt)

        if prompt == "/history":
            return self._history()
        if prompt == "/clear":
            self.turns.clear()
            return "已清空当前会话。"
        if prompt.startswith("/save-summary"):
            return self._save_summary(prompt)

        response = self.agent.handle(prompt)
        self.turns.append(ConversationTurn(user=prompt, assistant=response))
        return response

    def _history(self) -> str:
        if not self.turns:
            return "当前会话还没有历史记录。"

        lines = ["当前会话历史："]
        for index, turn in enumerate(self.turns, start=1):
            lines.append(f"{index}. 用户：{turn.user}")
            lines.append(f"   助手：{turn.assistant}")
        return "\n".join(lines)

    def _save_summary(self, prompt: str) -> str:
        if not self.turns:
            return "当前会话还没有可总结的内容。"

        try:
            parts = shlex.split(prompt, posix=False)
        except ValueError as exc:
            return f"命令解析失败：{exc}"

        if len(parts) < 2:
            return "用法：/save-summary 文件名"

        filename = parts[1]
        content = self._summary_markdown()
        result = self.tools.run("write_summary", filename=filename, content=content)
        return result.message.replace("总结", "会话总结")

    def _summary_markdown(self) -> str:
        lines = ["## 对话记录"]
        for index, turn in enumerate(self.turns, start=1):
            lines.append("")
            lines.append(f"### 第 {index} 轮")
            lines.append("")
            lines.append(f"- 用户：{turn.user}")
            lines.append(f"- 助手：{turn.assistant}")
        return "\n".join(lines)
