from __future__ import annotations

import shlex
from pathlib import Path

from .automation import (
    CommonDirectory,
    add_common_directory,
    describe_automation,
    list_common_directories,
    preview_file_organization,
    record_directory_open_request,
    write_daily_report,
)
from .config import ProjectPaths, build_project_paths
from .knowledge import answer_from_matches, describe_knowledge_base, find_data_matches, import_knowledge_path, set_document_tags
from .intent import parse_natural_language_intent
from .memory import append_memory, find_identity, is_identity_question, parse_identity_fact, read_profile, summarize_profile
from .runtime_context import RuntimeContext, RuntimeDirectoryContext, load_runtime_context, save_runtime_context
from .tools import ToolRegistry
from .update import describe_update_download, describe_update_status, update_download_dir
from .voice import describe_voice, speak_text


class JarvisAgent:
    """负责解析命令并调度第一阶段本地能力。"""

    def __init__(self, paths: ProjectPaths | None = None):
        self.paths = paths or build_project_paths()
        self.tools = ToolRegistry(self.paths)
        runtime_context = load_runtime_context(self.paths)
        self._recent_document_path: str | None = runtime_context.recent_document_path
        self._recent_directory: CommonDirectory | None = self._restore_recent_directory(runtime_context.recent_directory)
        self._recent_search_result_paths: tuple[str, ...] = runtime_context.recent_search_result_paths
        if self._recent_document_path is None and self._recent_search_result_paths:
            self._recent_document_path = self._recent_search_result_paths[0]

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
        if prompt in {"/update-status", "update-status"}:
            self.tools.run("record_log", message="检查更新状态")
            return describe_update_status()
        if prompt in {"/update-download", "update-download"}:
            self.tools.run("record_log", message="下载更新安装包：默认更新源")
            return describe_update_download(downloads_dir=update_download_dir(self.paths.root))
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

        intent = parse_natural_language_intent(prompt)
        if intent is not None:
            return self._handle_natural_language_intent(intent)

        data_answer = self._answer_from_data(prompt)
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
            answer = self._answer_from_data(question)
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
            self._remember_recent_document(document.relative_path)
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

        if command == "/dir-open":
            if not args:
                return "用法：/dir-open 常用目录别名"
            return self._open_directory(args[0])

        if command == "/update-status":
            source = self._strip_quotes(args[0]) if args else None
            self.tools.run("record_log", message=f"检查更新状态：{source or '默认更新源'}")
            return describe_update_status(source)

        if command == "/update-download":
            source = self._strip_quotes(args[0]) if args else None
            self.tools.run("record_log", message=f"下载更新安装包：{source or '默认更新源'}")
            return describe_update_download(source, downloads_dir=update_download_dir(self.paths.root))

        if command == "/import":
            if not args:
                return "用法：/import 源文件或目录路径 [目标文件名]"
            source_arg = self._strip_quotes(args[0])
            try:
                summary = import_knowledge_path(
                    self.paths,
                    source_arg,
                    self._strip_quotes(args[1]) if len(args) > 1 else None,
                )
            except (FileExistsError, FileNotFoundError, RuntimeError, UnicodeDecodeError, ValueError) as exc:
                return f"导入失败：{exc}"
            imported_paths = "、".join(f"data/{document.relative_path}" for document in summary.documents)
            self.tools.run("record_log", message=f"导入知识库资料：{imported_paths}")
            if len(summary.documents) == 1 and Path(source_arg).expanduser().is_file():
                self._remember_recent_document(summary.documents[0].relative_path)
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
                "/update-status [清单路径或URL]：检查 Jarvis Lite 新版本",
                "/update-download [清单路径或URL]：下载新版本安装包到运行态目录",
                "/dir-add 别名 目录路径：登记常用目录",
                "/dirs：查看常用目录",
                "/daily-report [文件名]：生成工作日报到 word/",
                "/organize-preview 常用目录别名：按扩展名生成文件整理预览",
                "/dir-open 常用目录别名：记录打开目录请求，不启动外部应用",
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

    def _handle_natural_language_intent(self, intent) -> str:
        if intent.name == "capabilities":
            return self._capability_summary()
        if intent.name == "recent_context_status":
            return self._recent_context_status()
        if intent.name == "command":
            return self.handle(intent.command)
        if intent.name == "open_directory_path" and intent.path is not None:
            return self._open_directory_path(intent.alias, intent.path)
        if intent.name == "open_directory_alias":
            return self._open_directory(intent.alias)
        if intent.name == "organize_directory_alias":
            return self._organize_preview(intent.alias)
        if intent.name == "open_recent_directory":
            return self._open_recent_directory()
        if intent.name == "organize_recent_directory":
            return self._organize_recent_directory()
        if intent.name == "tag_recent_document":
            return self._tag_recent_document(intent.tags)
        if intent.name == "tag_numbered_search_result":
            return self._tag_numbered_search_result(intent.result_index, intent.tags)
        if intent.name == "read_numbered_search_result":
            return self._read_numbered_search_result(intent.result_index)
        return "我还不能理解这个自然语言请求。你可以换一种说法，或输入 /help 查看当前能力。"

    def _capability_summary(self) -> str:
        return "\n".join(
            [
                "我现在可以做这些事：",
                "- 记忆：记住你的姓名、身份和偏好，也能回答“我是谁”。",
                "- 知识库：导入 Markdown、txt、PDF、JSON 聊天记录，并基于资料回答。",
                "- 工作台：登记常用目录、查看目录、生成日报、做文件整理预览。",
                "- 桌面：通过小助手面板和托盘触发常用能力。",
                "- 更新：检查更新，也可以下载更新安装包到运行态目录。",
                "- 语音准备：/voice 会复用同一套文本理解流程。",
            ]
        )

    def _recent_context_status(self) -> str:
        self.tools.run("record_log", message="查看最近上下文状态")
        has_document = self._recent_document_path is not None
        has_directory = self._recent_directory is not None
        has_search_results = bool(self._recent_search_result_paths)
        if not has_document and not has_directory and not has_search_results:
            return "\n".join(
                [
                    "最近上下文：还没有记录。",
                    "- 你可以先提问、导入资料，或打开/整理目录。",
                ]
            )

        lines = ["最近上下文："]
        if has_document:
            lines.append(f"- 最近资料：data/{self._recent_document_path}")
        else:
            lines.append("- 最近资料：无")

        if has_directory and self._recent_directory is not None:
            lines.append(f"- 最近目录：{self._recent_directory.alias} -> {self._recent_directory.path}")
        else:
            lines.append("- 最近目录：无")

        if has_search_results:
            lines.append(f"- 最近搜索结果：{len(self._recent_search_result_paths)} 条")
            for index, relative_path in enumerate(self._recent_search_result_paths, start=1):
                lines.append(f"  {index}. data/{relative_path}")
        else:
            lines.append("- 最近搜索结果：无")
        return "\n".join(lines)

    def _sentence(self, text: str) -> str:
        return text if text.endswith(("。", "！", "？", ".", "!", "?")) else f"{text}。"

    def _remember(self, fact: str) -> str:
        remembered = append_memory(self.paths, fact)
        self.tools.run("record_log", message=f"写入长期记忆：{remembered}")
        return f"已记住：{remembered}"

    def _answer_from_data(self, question: str) -> str:
        matches = find_data_matches(self.paths, question)
        if not matches:
            return ""
        self._remember_recent_search_results(tuple(match.relative_path for match in matches))
        self._remember_recent_document(matches[0].relative_path)
        return answer_from_matches(matches)

    def _tag_recent_document(self, tags: tuple[str, ...]) -> str:
        if self._recent_document_path is None:
            return "还没有最近资料。你可以先导入资料，或说“给 note.txt 打标签 项目”。"
        return self.handle(f'/tag "{self._recent_document_path}" {" ".join(tags)}')

    def _tag_numbered_search_result(self, result_index: int, tags: tuple[str, ...]) -> str:
        relative_path, error = self._recent_search_result_path(result_index)
        if error:
            return error
        assert relative_path is not None
        return self.handle(f'/tag "{relative_path}" {" ".join(tags)}')

    def _read_numbered_search_result(self, result_index: int) -> str:
        relative_path, error = self._recent_search_result_path(result_index)
        if error:
            return error
        assert relative_path is not None
        result = self.tools.run("read_data_file", path=relative_path)
        if not result.success:
            return result.message
        self.tools.run("record_log", message=f"读取最近搜索结果：data/{relative_path}")
        return f"第 {result_index} 条结果：data/{relative_path}\n{result.output}"

    def _recent_search_result_path(self, result_index: int) -> tuple[str | None, str | None]:
        if not self._recent_search_result_paths:
            return None, "还没有最近搜索结果。你可以先提问，例如“Jarvis Lite 使用什么？”。"
        if result_index < 1 or result_index > len(self._recent_search_result_paths):
            return None, f"最近搜索结果只有 {len(self._recent_search_result_paths)} 条，不能选择第 {result_index} 条。"
        return self._recent_search_result_paths[result_index - 1], None

    def _remember_recent_document(self, relative_path: str) -> None:
        self._recent_document_path = relative_path
        self._save_runtime_context()

    def _remember_recent_search_results(self, relative_paths: tuple[str, ...]) -> None:
        self._recent_search_result_paths = relative_paths
        self._save_runtime_context()

    def _remember_recent_directory(self, alias: str, directory_path: Path) -> None:
        self._recent_directory = CommonDirectory(alias, directory_path)
        self._save_runtime_context()

    def _restore_recent_directory(self, context: RuntimeDirectoryContext | None) -> CommonDirectory | None:
        if context is None:
            return None
        return CommonDirectory(context.alias, Path(context.path))

    def _save_runtime_context(self) -> None:
        recent_directory = None
        if self._recent_directory is not None:
            recent_directory = RuntimeDirectoryContext(
                alias=self._recent_directory.alias,
                path=str(self._recent_directory.path),
            )
        save_runtime_context(
            self.paths,
            RuntimeContext(
                recent_document_path=self._recent_document_path,
                recent_directory=recent_directory,
                recent_search_result_paths=self._recent_search_result_paths,
            ),
        )

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

        return self._organize_directory(directory)

    def _organize_recent_directory(self) -> str:
        if self._recent_directory is None:
            return "还没有最近目录。你可以先打开或整理一个目录，或说“整理桌面”。"
        return self._organize_directory(self._recent_directory)

    def _organize_directory(self, directory: CommonDirectory) -> str:
        try:
            preview = preview_file_organization(directory.path)
        except FileNotFoundError as exc:
            return f"文件整理预览失败：{exc}"

        self._remember_recent_directory(directory.alias, directory.path)
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

    def _open_directory(self, alias: str) -> str:
        directory = self._find_common_directory(alias)
        if directory is None:
            return f"没有找到常用目录：{alias}。可用 /dirs 查看。"

        return self._open_directory_path(directory.alias, directory.path)

    def _open_recent_directory(self) -> str:
        if self._recent_directory is None:
            return "还没有最近目录。你可以先打开或整理一个目录，或说“打开桌面”。"
        return self._open_directory_path(self._recent_directory.alias, self._recent_directory.path)

    def _open_directory_path(self, alias: str, directory_path: Path) -> str:
        try:
            record = record_directory_open_request(self.paths, alias, directory_path)
        except FileNotFoundError as exc:
            return f"打开目录请求记录失败：{exc}"

        self._remember_recent_directory(alias, directory_path.resolve())
        self.tools.run("record_log", message=f"记录打开目录请求：{alias} -> {directory_path}")
        return "\n".join(
            [
                f"已记录打开目录请求：{alias} -> {directory_path.resolve()}",
                f"- 记录文件：{record.relative_path}",
                "- 当前不会启动外部应用。",
            ]
        )

    def _find_common_directory(self, alias: str) -> CommonDirectory | None:
        normalized_alias = alias.strip()
        for directory in list_common_directories(self.paths):
            if directory.alias == normalized_alias:
                return directory
        return self._known_directory(normalized_alias)

    def _known_directory(self, alias: str) -> CommonDirectory | None:
        for directory_name in self._known_directory_candidates(alias):
            directory = Path.home() / directory_name
            if directory.is_dir():
                return CommonDirectory(alias, directory.resolve())
        return None

    def _known_directory_candidates(self, alias: str) -> tuple[str, ...]:
        if alias.strip().lower() in {"桌面", "desktop"}:
            return ("Desktop", "桌面")
        return ()

    def _project_path(self, path: Path) -> str:
        return path.relative_to(self.paths.root).as_posix()

    def _strip_quotes(self, value: str) -> str:
        return value.strip().strip('"').strip("'")

    def _status(self) -> str:
        return "\n".join(
            [
                "Jarvis Lite 当前状态：本地助手基础闭环已具备。",
                "- 入口：命令行、桌面小助手、助手面板和系统托盘",
                f"- 长期记忆：{self._project_path(self.paths.profile_path)}",
                f"- 个人知识库：{self._project_path(self.paths.data_dir)}",
                f"- 工具日志：{self._project_path(self.paths.log_path)}",
                "- 自然语言：已支持能力询问、身份询问、日报、知识库、更新和打开磁盘等第一批意图",
                "- 语音入口：/voice、/speak、/voice-status",
                "- 工作台自动化：常用目录、日报、整理预览和目录打开记录",
                "- 桌面能力：小助手窗口、面板、托盘、主题、开机启动、安装包、更新检查和下载",
                "- 会话能力：/history、/save-summary、/clear",
                "- 记忆写入：/remember、我叫...、我是...",
                "- 本地验证：python -m unittest discover -s tests -v",
            ]
        )
