from __future__ import annotations

import shlex
from pathlib import Path

from .config import ProjectPaths, build_project_paths
from .knowledge import answer_from_data, describe_knowledge_base, import_knowledge_path, set_document_tags
from .memory import append_memory, find_identity, is_identity_question, parse_identity_fact, read_profile, summarize_profile
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
        if prompt in {"/status", "status"}:
            return self._status()
        if prompt in {"/kb", "kb", "/knowledge", "knowledge"}:
            self.tools.run("record_log", message="查看个人知识库状态")
            return describe_knowledge_base(self.paths)

        if is_identity_question(prompt):
            identity = find_identity(read_profile(self.paths))
            if identity:
                return identity
            return "我还不知道你是谁。你可以说“我叫张三”或使用 /remember 用户姓名：张三。"

        if prompt.startswith("/"):
            return self._handle_command(prompt)

        fact = parse_identity_fact(prompt)
        if fact:
            return self._remember(fact)

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

        if command == "/remember":
            if not args:
                return "用法：/remember 记忆内容"
            return self._remember(" ".join(args))

        if command == "/ask":
            if not args:
                return "用法：/ask 问题"
            question = " ".join(args)
            answer = answer_from_data(self.paths, question)
            if not answer:
                return f"没有在 data 目录找到和“{question}”相关的资料。"
            self.tools.run("record_log", message=f"基于 data 目录回答显式问题：{question}")
            return answer

        if command == "/tag":
            if len(args) < 2:
                return "用法：/tag 文件名 标签..."
            try:
                document = set_document_tags(self.paths, self._strip_quotes(args[0]), args[1:])
            except (FileNotFoundError, ValueError) as exc:
                return f"标签更新失败：{exc}"
            tags = "、".join(document.tags)
            self.tools.run("record_log", message=f"更新知识库标签：data/{document.relative_path} -> {tags}")
            return f"已更新标签：data/{document.relative_path}（{tags}）"

        if command == "/import":
            if not args:
                return "用法：/import 源文件或目录路径 [目标文件名]"
            try:
                summary = import_knowledge_path(
                    self.paths,
                    self._strip_quotes(args[0]),
                    self._strip_quotes(args[1]) if len(args) > 1 else None,
                )
            except (FileExistsError, FileNotFoundError, RuntimeError, UnicodeDecodeError, ValueError) as exc:
                return f"导入失败：{exc}"
            imported_paths = "、".join(f"data/{document.relative_path}" for document in summary.documents)
            self.tools.run("record_log", message=f"导入知识库资料：{imported_paths}")
            if summary.scanned_count == 1 and summary.documents:
                document = summary.documents[0]
                return f"已导入知识库：data/{document.relative_path}（{document.searchable_line_count} 行）"
            return (
                f"已导入知识库：{summary.scanned_count} 个文件，"
                f"成功 {summary.imported_count} 个，跳过 {summary.skipped_count} 个，"
                f"可检索文本行 {summary.searchable_line_count} 行。"
            )

        return f"未知命令：{command}。输入 /help 查看可用命令。"

    def _help(self) -> str:
        return "\n".join(
            [
                "Jarvis Lite 可用命令：",
                "/memory：查看长期记忆",
                "/status：查看阶段 1 当前状态",
                "/kb：查看个人知识库状态",
                "/import 源文件或目录路径 [目标文件名]：导入 Markdown、txt、PDF 或 JSON 聊天记录到 data/",
                "/tag 文件名 标签...：给 data 资料设置标签",
                "/list [目录]：列出 data 目录内容",
                "/read 文件名：读取 data 目录中的文本文件",
                "/ask 问题：基于 data 目录中的文本资料回答",
                "/remember 记忆内容：写入长期记忆",
                "/note 标题 内容：写入 memory/notes/ 下的笔记",
                "/summary 文件名 内容：写入 word/ 下的总结",
                "/tools：查看第一阶段工具白名单",
                "/history：查看当前命令行会话历史",
                "/save-summary 文件名：保存当前命令行会话总结到 word/",
                "/clear：清空当前命令行会话历史",
                "/exit：退出命令行助手",
            ]
        )

    def _sentence(self, text: str) -> str:
        return text if text.endswith(("。", "！", "？", ".", "!", "?")) else f"{text}。"

    def _remember(self, fact: str) -> str:
        remembered = append_memory(self.paths, fact)
        self.tools.run("record_log", message=f"写入长期记忆：{remembered}")
        return f"已记住：{remembered}"

    def _project_path(self, path: Path) -> str:
        return path.relative_to(self.paths.root).as_posix()

    def _strip_quotes(self, value: str) -> str:
        return value.strip().strip('"').strip("'")

    def _status(self) -> str:
        return "\n".join(
            [
                "阶段 1 状态：命令行助手基础闭环已具备。",
                f"- 长期记忆：{self._project_path(self.paths.profile_path)}",
                f"- data 文本问答：{self._project_path(self.paths.data_dir)}",
                f"- 工具日志：{self._project_path(self.paths.log_path)}",
                "- 会话能力：/history、/save-summary、/clear",
                "- 记忆写入：/remember、我叫...、我是...",
                "- 本地验证：python -m unittest discover -s tests -v",
            ]
        )
