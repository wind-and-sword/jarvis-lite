from __future__ import annotations

import shlex

from .config import ProjectPaths, build_project_paths
from .knowledge import answer_from_data
from .memory import read_profile, summarize_profile
from .tools import ToolRegistry


class JarvisAgent:
    """负责解析命令并调度第一阶段本地能力。"""

    def __init__(self, paths: ProjectPaths | None = None):
        self.paths = paths or build_project_paths()
        self.tools = ToolRegistry(self.paths)

    def handle(self, user_input: str) -> str:
        prompt = user_input.strip()
        if not prompt:
            return "请输入问题或命令。输入 /help 查看可用命令。"

        if prompt in {"/help", "help"}:
            return self._help()
        if prompt in {"/memory", "memory"}:
            return read_profile(self.paths)
        if prompt in {"/tools", "tools"}:
            return "\n".join(sorted(self.tools.allowed_tool_names))

        if prompt.startswith("/"):
            return self._handle_command(prompt)

        data_answer = answer_from_data(self.paths, prompt)
        if data_answer:
            self.tools.run("record_log", message=f"基于 data 目录回答普通问题：{prompt}")
            return data_answer

        profile = read_profile(self.paths)
        summary = summarize_profile(profile)
        return f"Jarvis Lite 已读取长期记忆。当前记忆摘要：{self._sentence(summary)}你可以输入 /help 查看我现在能做的事。"

    def _handle_command(self, prompt: str) -> str:
        try:
            parts = shlex.split(prompt, posix=False)
        except ValueError as exc:
            return f"命令解析失败：{exc}"

        command = parts[0]
        args = parts[1:]

        if command == "/list":
            result = self.tools.run("list_data", path=args[0] if args else ".")
            return result.output if result.success else result.message

        if command == "/read":
            if not args:
                return "用法：/read 文件名"
            result = self.tools.run("read_data_file", path=args[0])
            return result.output if result.success else result.message

        if command == "/note":
            if len(args) < 2:
                return "用法：/note 标题 内容"
            result = self.tools.run("write_note", title=args[0], content=" ".join(args[1:]))
            return result.message

        if command == "/summary":
            if len(args) < 2:
                return "用法：/summary 文件名 内容"
            result = self.tools.run("write_summary", filename=args[0], content=" ".join(args[1:]))
            return result.message

        if command == "/ask":
            if not args:
                return "用法：/ask 问题"
            question = " ".join(args)
            answer = answer_from_data(self.paths, question)
            if not answer:
                return f"没有在 data 目录找到和“{question}”相关的资料。"
            self.tools.run("record_log", message=f"基于 data 目录回答显式问题：{question}")
            return answer

        return f"未知命令：{command}。输入 /help 查看可用命令。"

    def _help(self) -> str:
        return "\n".join(
            [
                "Jarvis Lite 可用命令：",
                "/memory：查看长期记忆",
                "/list [目录]：列出 data 目录内容",
                "/read 文件名：读取 data 目录中的文本文件",
                "/ask 问题：基于 data 目录中的文本资料回答",
                "/note 标题 内容：写入 memory/notes/ 下的笔记",
                "/summary 文件名 内容：写入 word/ 下的总结",
                "/tools：查看第一阶段工具白名单",
                "/exit：退出命令行助手",
            ]
        )

    def _sentence(self, text: str) -> str:
        return text if text.endswith(("。", "！", "？", ".", "!", "?")) else f"{text}。"
