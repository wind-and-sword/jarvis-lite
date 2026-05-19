from __future__ import annotations

import shlex
from pathlib import Path

from .automation import (
    CommonDirectory,
    add_common_directory,
    describe_automation,
    list_common_directories,
    preview_file_organization,
    write_daily_report,
)
from .config import ProjectPaths, build_project_paths
from .knowledge import answer_from_data, describe_knowledge_base, import_knowledge_path, set_document_tags
from .memory import append_memory, find_identity, is_identity_question, parse_identity_fact, read_profile, summarize_profile
from .tools import ToolRegistry
from .voice import describe_voice, speak_text


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
        if prompt in {"/voice-status", "voice-status"}:
            self.tools.run("record_log", message="查看语音入口状态")
            return describe_voice(self.paths)
        if prompt in {"/automation-status", "automation-status"}:
            self.tools.run("record_log", message="查看阶段 4 自动化状态")
            return describe_automation(self.paths)
        if prompt in {"/dirs", "dirs"}:
            self.tools.run("record_log", message="查看常用目录")
            return self._directories()

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

        if command == "/speak":
            if not args:
                return "用法：/speak 文本"
            try:
                result = speak_text(self.paths, " ".join(args))
            except (RuntimeError, ValueError) as exc:
                return f"语音播报失败：{exc}"
            self.tools.run("record_log", message=f"语音播报：{' '.join(args)}")
            return result.message

        if command == "/voice":
            if not args:
                return "用法：/voice 已识别的语音文本"
            spoken_text = " ".join(args)
            answer = self.handle(spoken_text)
            try:
                speak_text(self.paths, answer)
            except (RuntimeError, ValueError) as exc:
                return f"识别文本：{spoken_text}\n助手：{answer}\n语音播报失败：{exc}"
            self.tools.run("record_log", message=f"处理语音文本：{spoken_text}")
            return f"识别文本：{spoken_text}\n助手：{answer}"

        if command == "/dir-add":
            if len(args) < 2:
                return "用法：/dir-add 别名 目录路径"
            try:
                directory = add_common_directory(self.paths, args[0], self._strip_quotes(args[1]))
            except (FileNotFoundError, ValueError) as exc:
                return f"常用目录登记失败：{exc}"
            self.tools.run("record_log", message=f"登记常用目录：{directory.alias} -> {directory.path}")
            return f"已登记常用目录：{directory.alias} -> {directory.path}"

        if command == "/daily-report":
            try:
                report = write_daily_report(self.paths, self._strip_quotes(args[0]) if args else None)
            except ValueError as exc:
                return f"日报生成失败：{exc}"
            self.tools.run("record_log", message=f"生成日报：{report.relative_path}")
            return f"已生成日报：{report.relative_path}"

        if command == "/organize-preview":
            if not args:
                return "用法：/organize-preview 常用目录别名"
            return self._organize_preview(args[0])

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
                "/voice-status：查看阶段 3 语音入口状态",
                "/speak 文本：播报一段文本",
                "/voice 已识别的语音文本：按语音入口处理文本并播报回答",
                "/automation-status：查看阶段 4 自动化状态",
                "/dir-add 别名 目录路径：登记常用目录",
                "/dirs：查看常用目录",
                "/daily-report [文件名]：生成工作日报到 word/",
                "/organize-preview 常用目录别名：按扩展名生成文件整理预览",
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

    def _directories(self) -> str:
        directories = list_common_directories(self.paths)
        if not directories:
            return "常用目录：还没有登记。"
        lines = ["常用目录："]
        for directory in directories:
            lines.append(f"- {directory.alias}：{directory.path}")
        return "\n".join(lines)

    def _organize_preview(self, alias: str) -> str:
        directory = self._find_common_directory(alias)
        if directory is None:
            return f"没有找到常用目录：{alias}。可用 /dirs 查看。"

        try:
            preview = preview_file_organization(directory.path)
        except FileNotFoundError as exc:
            return f"文件整理预览失败：{exc}"

        self.tools.run("record_log", message=f"生成文件整理预览：{directory.alias} -> {directory.path}")
        lines = [
            f"文件整理预览：{directory.alias}",
            f"- 目录：{preview.directory}",
            f"- 文件数量：{preview.file_count} 个",
            f"- 跳过子目录：{preview.skipped_directory_count} 个",
            "- 说明：只生成预览，不会移动或删除文件。",
        ]
        if not preview.groups:
            lines.append("- 没有可整理的文件。")
            return "\n".join(lines)

        lines.append("整理建议：")
        for group in preview.groups:
            files = "、".join(group.files)
            lines.append(f"- {group.target_folder}/：{files}")
        return "\n".join(lines)

    def _find_common_directory(self, alias: str) -> CommonDirectory | None:
        normalized_alias = alias.strip()
        for directory in list_common_directories(self.paths):
            if directory.alias == normalized_alias:
                return directory
        return None

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
