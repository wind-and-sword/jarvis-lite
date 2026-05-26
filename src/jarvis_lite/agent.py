from __future__ import annotations

import shlex
from datetime import datetime
from pathlib import Path

from .automation import (
    CommonDirectory,
    add_common_directory,
    describe_automation,
    list_recent_files,
    list_common_directories,
    preview_file_organization,
    record_directory_open_request,
    suggest_next_actions_from_context,
    write_daily_report,
)
from .config import ProjectPaths, build_project_paths
from .knowledge import (
    KnowledgeIndex,
    answer_from_matches,
    build_knowledge_index,
    describe_knowledge_base,
    find_data_matches,
    import_knowledge_path,
    set_document_tags,
    summarize_knowledge_base,
)
from .intent import parse_natural_language_intent
from .memory import (
    append_experience,
    append_memory,
    find_identity,
    is_identity_question,
    list_recent_experiences,
    parse_identity_fact,
    read_experiences,
    read_profile,
    search_experiences,
    summarize_profile,
)
from .runtime_context import (
    RuntimeContext,
    RuntimeDirectoryContext,
    RuntimeRecentFileContext,
    RuntimeTaggedDocumentsOperationContext,
    load_runtime_context,
    save_runtime_context,
)
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
        self._recent_document_paths: tuple[str, ...] = runtime_context.recent_document_paths
        self._recent_directory: CommonDirectory | None = self._restore_recent_directory(runtime_context.recent_directory)
        self._recent_search_result_paths: tuple[str, ...] = runtime_context.recent_search_result_paths
        self._recent_advice_suggestions: tuple[str, ...] = runtime_context.recent_advice_suggestions
        self._recent_files: tuple[RuntimeRecentFileContext, ...] = runtime_context.recent_files
        self._pending_advice_command: str | None = None
        self._pending_advice_command_draft_command: str | None = None
        self._pending_tagged_documents_tag: str | None = None
        self._pending_tagged_documents_tags: tuple[str, ...] = ()
        self._pending_tagged_documents_paths: tuple[str, ...] = ()
        self._recent_tagged_documents_operation_tag: str | None = (
            runtime_context.recent_tagged_documents_operation.tag
            if runtime_context.recent_tagged_documents_operation is not None
            else None
        )
        self._recent_tagged_documents_operation_tags: tuple[str, ...] = (
            runtime_context.recent_tagged_documents_operation.tags
            if runtime_context.recent_tagged_documents_operation is not None
            else ()
        )
        self._recent_tagged_documents_operation_updated_count = (
            runtime_context.recent_tagged_documents_operation.updated_count
            if runtime_context.recent_tagged_documents_operation is not None
            else 0
        )
        self._recent_tagged_documents_operation_restore_commands: tuple[str, ...] = (
            runtime_context.recent_tagged_documents_operation.restore_commands
            if runtime_context.recent_tagged_documents_operation is not None
            else ()
        )
        if self._recent_document_path is None and self._recent_search_result_paths:
            self._recent_document_path = self._recent_search_result_paths[0]
        if self._recent_document_path is not None and self._recent_document_path not in self._recent_document_paths:
            self._recent_document_paths = (self._recent_document_path, *self._recent_document_paths)

    def handle(self, user_input: str) -> str:
        prompt = user_input.strip()
        if not prompt:
            return "请输入问题或命令。输入 /help 查看可用命令。"

        if prompt in {"/help", "help"}:
            return self._help()
        if prompt in {"/memory", "memory"}:
            return read_profile(self.paths)
        if prompt in {"/experiences", "experiences"}:
            self.tools.run("record_log", message="查看经验记忆")
            return read_experiences(self.paths)
        if prompt in {"/tools", "tools"}:
            return "\n".join(sorted(self.tools.allowed_tool_names))
        if prompt in {"/status", "status"}:
            return self._status()
        if prompt in {"/kb", "kb", "/knowledge", "knowledge"}:
            self.tools.run("record_log", message="查看个人知识库状态")
            return describe_knowledge_base(self.paths)
        if prompt in {"/kb-summary", "kb-summary", "/knowledge-summary", "knowledge-summary"}:
            self.tools.run("record_log", message="查看知识库摘要")
            return self._knowledge_summary()
        if prompt in {"/voice-status", "voice-status"}:
            self.tools.run("record_log", message="查看语音入口状态")
            return describe_voice(self.paths)
        if prompt in {"/automation-status", "automation-status"}:
            self.tools.run("record_log", message="查看阶段 4 自动化状态")
            return describe_automation(self.paths)
        if prompt in {"/recent-files", "recent-files"}:
            return self._recent_files_status()
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

        if self._pending_advice_command_draft_command == command:
            completed_command = self._executable_advice_command(prompt)
            if completed_command is not None:
                self._pending_advice_command = completed_command
                self._pending_advice_command_draft_command = None
                self.tools.run("record_log", message=f"补全最近建议命令草稿：{completed_command}")
                return "\n".join(
                    [
                        "已补全建议命令，等待确认执行。",
                        f"命令：{completed_command}",
                        "确认执行请说“确认执行”，取消请说“取消执行”。",
                    ]
                )

        if command == "/list":
            result = self.tools.run("list_data", path=args[0] if args else ".")
            return result.output if result.success else result.message

        if command == "/read":
            if not args:
                return "用法：/read 文件名"
            document_path = self._strip_quotes(args[0])
            result = self.tools.run("read_data_file", path=document_path)
            if not result.success:
                return result.message
            self._remember_recent_document(document_path)
            return result.output

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

        if command == "/experience":
            if not args:
                return "用法：/experience 经验内容"
            return self._remember_experience(self._strip_quotes(" ".join(args)))

        if command == "/experience-search":
            if not args:
                return "用法：/experience-search 关键词"
            return self._search_experiences(" ".join(args))

        if command == "/experience-advice":
            if not args:
                return "用法：/experience-advice 关键词"
            return self._experience_advice(" ".join(args))

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
                "/experiences：查看经验记忆",
                "/status：查看阶段 1 当前状态",
                "/kb：查看个人知识库状态",
                "/kb-summary：查看知识库资料摘要",
                "/voice-status：查看阶段 3 语音入口状态",
                "/speak 文本：播报一段文本",
                "/voice 已识别的语音文本：按语音入口处理文本并播报回答",
                "/automation-status：查看阶段 4 自动化状态",
                "/recent-files：查看常用目录、项目目录、桌面和下载目录中的最近文件",
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
                "/experience 经验内容：写入经验记忆",
                "/experience-search 关键词：搜索经验记忆",
                "/experience-advice 关键词：根据经验给出操作建议",
                "/note 标题 内容：写入 memory/notes/ 下的笔记",
                "/summary 文件名 内容：写入 word/ 下的总结",
                "/tools：查看第一阶段工具白名单",
                "/history：查看当前命令行会话历史",
                "/save-summary 文件名：保存当前命令行会话总结到 word/",
                "/clear：清空当前命令行会话历史",
                "/exit：退出命令行助手",
            ]
        )

    def _knowledge_summary(self) -> str:
        summary = summarize_knowledge_base(self.paths)
        index = build_knowledge_index(self.paths)
        document_paths = tuple(document.relative_path for document in index.documents)
        if not document_paths:
            return summary

        self._recent_document_path = document_paths[0]
        self._recent_document_paths = document_paths
        self._save_runtime_context()
        lines = [
            summary,
            "可继续操作：读取第一份资料；给第一份资料打标签 标签；/ask 关键词",
        ]
        tag_suggestions = self._knowledge_summary_tag_suggestions(index)
        if tag_suggestions:
            lines.append(f"按标签提问：{tag_suggestions}")
        tag_read_suggestions = self._knowledge_summary_tag_read_suggestions(index)
        if tag_read_suggestions:
            lines.append(f"按标签读取：{tag_read_suggestions}")
        return "\n".join(lines)

    def _knowledge_summary_tag_suggestions(self, index: KnowledgeIndex) -> str:
        return "；".join(f"/ask {tag}" for tag in self._knowledge_summary_tags(index))

    def _knowledge_summary_tag_read_suggestions(self, index: KnowledgeIndex) -> str:
        return "；".join(f"读取{tag}标签资料" for tag in self._knowledge_summary_tags(index))

    def _knowledge_summary_tags(self, index: KnowledgeIndex) -> tuple[str, ...]:
        return tuple(sorted({tag for document in index.documents for tag in document.tags})[:3])

    def _handle_natural_language_intent(self, intent) -> str:
        if intent.name == "capabilities":
            return self._capability_summary()
        if intent.name == "recent_context_status":
            return self._recent_context_status()
        if intent.name == "recent_files_status":
            return self._recent_files_status()
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
        if intent.name == "tag_numbered_recent_document":
            return self._tag_numbered_recent_document(intent.result_index, intent.tags)
        if intent.name == "tag_numbered_search_result":
            return self._tag_numbered_search_result(intent.result_index, intent.tags)
        if intent.name == "preview_tagged_documents_tagging":
            return self._preview_tagged_documents_tagging(intent.alias, intent.tags)
        if intent.name == "read_tagged_documents":
            return self._read_tagged_documents(intent.alias)
        if intent.name == "read_recent_document":
            return self._read_recent_document()
        if intent.name == "read_numbered_recent_document":
            return self._read_numbered_recent_document(intent.result_index)
        if intent.name == "read_numbered_recent_file":
            return self._read_numbered_recent_file(intent.result_index)
        if intent.name == "import_numbered_recent_file":
            return self._import_numbered_recent_file(intent.result_index)
        if intent.name == "read_numbered_search_result":
            return self._read_numbered_search_result(intent.result_index)
        if intent.name == "read_numbered_advice_suggestion":
            return self._read_numbered_advice_suggestion(intent.result_index)
        if intent.name == "prepare_numbered_advice_suggestion_execution":
            return self._prepare_numbered_advice_suggestion_execution(intent.result_index)
        if intent.name == "confirm_pending_advice_suggestion_execution":
            return self._confirm_pending_advice_suggestion_execution()
        if intent.name == "cancel_pending_advice_suggestion_execution":
            return self._cancel_pending_advice_suggestion_execution()
        return "我还不能理解这个自然语言请求。你可以换一种说法，或输入 /help 查看当前能力。"

    def _capability_summary(self) -> str:
        lines = [
            "我现在可以做这些事：",
            "- 记忆：记住你的姓名、身份和偏好，也能回答“我是谁”。",
            "- 经验：记录和查看可复用流程经验。",
            "- 知识库：导入 Markdown、txt、PDF、JSON 聊天记录，并基于资料回答。",
            "- 工作台：登记常用目录、查看目录、生成日报、做文件整理预览。",
            "- 桌面：通过小助手面板和托盘触发常用能力。",
            "- 更新：检查更新，也可以下载更新安装包到运行态目录。",
            "- 语音准备：/voice 会复用同一套文本理解流程。",
        ]
        recent_experiences = list_recent_experiences(self.paths)
        if recent_experiences:
            lines.append("最近经验：")
            for experience in recent_experiences:
                lines.append(f"- {experience}")
        return "\n".join(lines)

    def _recent_context_status(self) -> str:
        self.tools.run("record_log", message="查看最近上下文状态")
        has_document = self._recent_document_path is not None
        has_document_list = bool(self._recent_document_paths)
        has_directory = self._recent_directory is not None
        has_recent_files = bool(self._recent_files)
        has_search_results = bool(self._recent_search_result_paths)
        has_advice_suggestions = bool(self._recent_advice_suggestions)
        has_pending_advice_command = self._pending_advice_command is not None
        has_pending_tagged_documents_tagging = bool(self._pending_tagged_documents_paths)
        has_recent_tagged_documents_operation = self._recent_tagged_documents_operation_tag is not None
        if (
            not has_document
            and not has_document_list
            and not has_directory
            and not has_recent_files
            and not has_search_results
            and not has_advice_suggestions
            and not has_pending_advice_command
            and not has_pending_tagged_documents_tagging
            and not has_recent_tagged_documents_operation
        ):
            return "\n".join(
                [
                    "最近上下文：还没有记录。",
                    "- 你可以先提问、导入资料、查看最近文件、打开/整理目录，或生成经验建议。",
                ]
            )

        lines = ["最近上下文："]
        if has_document:
            lines.append(f"- 最近资料：data/{self._recent_document_path}")
        else:
            lines.append("- 最近资料：无")

        if has_document_list:
            lines.append(f"- 最近资料列表：{len(self._recent_document_paths)} 条")
            for index, relative_path in enumerate(self._recent_document_paths, start=1):
                lines.append(f"  {index}. data/{relative_path}")
        else:
            lines.append("- 最近资料列表：无")

        if has_directory and self._recent_directory is not None:
            lines.append(f"- 最近目录：{self._recent_directory.alias} -> {self._recent_directory.path}")
        else:
            lines.append("- 最近目录：无")

        if has_recent_files:
            lines.append(f"- 最近文件列表：{len(self._recent_files)} 条")
            for index, recent_file in enumerate(self._recent_files, start=1):
                lines.append(f"  {index}. {recent_file.alias} -> {recent_file.path}")
        else:
            lines.append("- 最近文件列表：无")

        if has_search_results:
            lines.append(f"- 最近搜索结果：{len(self._recent_search_result_paths)} 条")
            for index, relative_path in enumerate(self._recent_search_result_paths, start=1):
                lines.append(f"  {index}. data/{relative_path}")
        else:
            lines.append("- 最近搜索结果：无")

        if has_advice_suggestions:
            lines.append(f"- 最近建议：{len(self._recent_advice_suggestions)} 条")
            for index, suggestion in enumerate(self._recent_advice_suggestions, start=1):
                lines.append(f"  {index}. {suggestion}")
        else:
            lines.append("- 最近建议：无")

        if self._pending_advice_command is not None:
            lines.append(f"- 待确认建议命令：{self._pending_advice_command}")
        else:
            lines.append("- 待确认建议命令：无")
        if has_pending_tagged_documents_tagging:
            group_tag = self._pending_tagged_documents_tag or ""
            appended_tags = "、".join(self._pending_tagged_documents_tags)
            document_count = len(self._pending_tagged_documents_paths)
            lines.append(
                f"- 待确认批量打标签：{group_tag}标签资料 -> "
                f"追加标签：{appended_tags}，{document_count} 份"
            )
        else:
            lines.append("- 待确认批量打标签：无")
        if has_recent_tagged_documents_operation:
            group_tag = self._recent_tagged_documents_operation_tag or ""
            appended_tags = "、".join(self._recent_tagged_documents_operation_tags)
            lines.append(
                f"- 最近批量打标签：{group_tag}标签资料 -> "
                f"追加标签：{appended_tags}，已更新 {self._recent_tagged_documents_operation_updated_count} 份"
            )
            if self._recent_tagged_documents_operation_restore_commands:
                lines.append(
                    f"  恢复提示：{'；'.join(self._recent_tagged_documents_operation_restore_commands)}"
                )
        else:
            lines.append("- 最近批量打标签：无")
        lines.append("下一步建议：")
        for suggestion in suggest_next_actions_from_context(self._runtime_context(), list_recent_experiences(self.paths)):
            lines.append(f"- {suggestion}")
        return "\n".join(lines)

    def _recent_files_status(self) -> str:
        self.tools.run("record_log", message="查看最近文件")
        recent_files = list_recent_files(self._recent_file_directories(), limit=5)
        if not recent_files:
            self._remember_recent_files(())
            return "最近文件：没有找到最近文件。你可以先在项目目录、桌面或下载目录放入文件，或使用 /dir-add 登记常用目录。"

        self._remember_recent_files(
            tuple(RuntimeRecentFileContext(alias=recent_file.alias, path=str(recent_file.path)) for recent_file in recent_files)
        )
        lines = ["最近文件："]
        for index, recent_file in enumerate(recent_files, start=1):
            modified_at = recent_file.modified_at.strftime("%Y-%m-%d %H:%M:%S")
            lines.append(f"{index}. {recent_file.alias}：{recent_file.path.name}")
            lines.append(f"   路径：{recent_file.path}")
            lines.append(f"   修改时间：{modified_at}")
        return "\n".join(lines)

    def _sentence(self, text: str) -> str:
        return text if text.endswith(("。", "！", "？", ".", "!", "?")) else f"{text}。"

    def _remember(self, fact: str) -> str:
        remembered = append_memory(self.paths, fact)
        self.tools.run("record_log", message=f"写入长期记忆：{remembered}")
        return f"已记住：{remembered}"

    def _remember_experience(self, experience: str) -> str:
        try:
            remembered = append_experience(self.paths, experience)
        except ValueError as exc:
            return f"经验记录失败：{exc}"
        self.tools.run("record_log", message=f"写入经验记忆：{remembered}")
        return f"已记录经验：{remembered}"

    def _search_experiences(self, query: str) -> str:
        normalized_query = self._strip_quotes(query)
        if not normalized_query:
            return "用法：/experience-search 关键词"
        matches = search_experiences(self.paths, normalized_query)
        self.tools.run("record_log", message=f"搜索经验记忆：{normalized_query}")
        if not matches:
            return f"没有找到和“{normalized_query}”相关的经验。"
        lines = [f"经验搜索：{normalized_query}"]
        for index, experience in enumerate(matches, start=1):
            lines.append(f"{index}. {experience}")
        return "\n".join(lines)

    def _experience_advice(self, query: str) -> str:
        normalized_query = self._strip_quotes(query)
        if not normalized_query:
            return "用法：/experience-advice 关键词"
        search_query = self._experience_search_query(normalized_query)
        matches = search_experiences(self.paths, search_query)
        context_lines = self._experience_context_lines(normalized_query)
        command_suggestions = self._experience_command_suggestions(normalized_query)
        self.tools.run("record_log", message=f"生成经验操作建议：{normalized_query}")
        if not matches and not context_lines and not command_suggestions:
            return (
                f"还没有找到和“{normalized_query}”相关的经验建议。"
                "你可以先用 /experience 经验内容 记录可复用流程。"
            )
        lines = [f"操作建议：{normalized_query}"]
        lines.extend(context_lines)
        lines.append("相关经验：")
        if matches:
            for index, experience in enumerate(matches, start=1):
                lines.append(f"{index}. {experience}")
        else:
            lines.append(f"- 还没有找到和“{normalized_query}”相关的经验建议。")
            lines.append("- 可以先用 /experience 经验内容 记录可复用流程。")
        if command_suggestions:
            self._remember_recent_advice_suggestions(command_suggestions)
            lines.append("可执行命令：")
            lines.extend(f"- {suggestion}" for suggestion in command_suggestions)
        else:
            self._remember_recent_advice_suggestions(())
        lines.append(f"可继续使用：/experience-search {normalized_query}")
        return "\n".join(lines)

    def _experience_search_query(self, query: str) -> str:
        if self._is_recent_document_query(query):
            return "资料"
        if self._is_recent_directory_query(query):
            return "目录"
        return query

    def _experience_context_lines(self, query: str) -> tuple[str, ...]:
        if self._is_recent_document_query(query):
            if self._recent_document_path is None:
                return ("当前资料：还没有最近资料。",)
            return (f"当前资料：data/{self._recent_document_path}",)
        if self._is_recent_directory_query(query):
            if self._recent_directory is None:
                return ("当前目录：还没有最近目录。",)
            return (f"当前目录：{self._recent_directory.alias} -> {self._recent_directory.path}",)
        return ()

    def _experience_command_suggestions(self, query: str) -> tuple[str, ...]:
        prompt = query.lower()
        suggestions: list[str] = []

        def add(command: str) -> None:
            if command not in suggestions:
                suggestions.append(command)

        if self._is_recent_document_query(query):
            if self._recent_document_path is not None:
                add(f"/read {self._recent_document_path}：读取当前资料")
                add(f"/tag {self._recent_document_path} 标签...：给当前资料设置标签")
            else:
                add("/import 源文件或目录路径 [目标文件名]：先导入一份资料")
            add("/ask 问题：基于知识库提问")

        if self._is_recent_directory_query(query):
            if self._recent_directory is not None:
                add(f"/organize-preview {self._recent_directory.alias}：预览整理当前目录")
                add(f"/dir-open {self._recent_directory.alias}：记录打开当前目录")
            else:
                add("/dir-add 别名 目录路径：先登记常用目录")
                add("/dirs：查看常用目录")

        if any(word in prompt for word in ("导入", "资料", "知识库", "pdf", "聊天记录")):
            add("/import 源文件或目录路径 [目标文件名]：导入资料到知识库")
            add("/kb：查看知识库状态")
            add("/tag 文件名 标签...：给资料设置标签")
        if any(word in prompt for word in ("标签", "标记")):
            add("/tag 文件名 标签...：给资料设置标签")
            add("/kb：查看资料标签")
        if "日报" in prompt:
            add("/daily-report [文件名]：生成工作日报")
        if any(word in prompt for word in ("目录", "文件夹", "整理", "打开")):
            add("/dirs：查看常用目录")
            add("/dir-add 别名 目录路径：登记常用目录")
            add("/organize-preview 常用目录别名：预览文件整理")
            add("/dir-open 常用目录别名：记录打开目录请求")
        if "更新" in prompt:
            add("/update-status [清单路径或URL]：检查更新")
            add("/update-download [清单路径或URL]：下载更新安装包")
        if "语音" in prompt:
            add("/voice-status：查看语音入口状态")
            add("/speak 文本：播报文本")
            add("/voice 已识别的语音文本：处理语音文本")
        if "经验" in prompt:
            add("/experience 经验内容：记录经验")
            add("/experience-search 关键词：搜索经验")

        return tuple(suggestions)

    def _is_recent_document_query(self, query: str) -> bool:
        return query.strip() in {"这个资料", "这份资料", "刚才的资料", "最近的资料", "当前资料"}

    def _is_recent_directory_query(self, query: str) -> bool:
        return query.strip() in {"这个目录", "这个文件夹", "刚才的目录", "最近的目录", "当前目录"}

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

    def _tag_numbered_recent_document(self, document_index: int, tags: tuple[str, ...]) -> str:
        if not self._recent_document_paths:
            return "还没有最近资料列表。你可以先读取资料、导入资料，或说“读取 note.txt”。"
        if document_index < 1 or document_index > len(self._recent_document_paths):
            return f"最近资料列表只有 {len(self._recent_document_paths)} 条，不能选择第 {document_index} 份。"
        relative_path = self._recent_document_paths[document_index - 1]
        return self.handle(f'/tag "{relative_path}" {" ".join(tags)}')

    def _preview_tagged_documents_tagging(self, tag: str, tags: tuple[str, ...]) -> str:
        documents = self._tagged_documents(tag)
        if not documents:
            return f"没有找到标签为“{tag}”的资料。你可以先用 /kb-summary 查看标签分组，或给资料打标签。"

        document_paths = tuple(document.relative_path for document in documents)
        self._recent_document_path = document_paths[0]
        self._recent_document_paths = document_paths
        self._save_runtime_context()
        self._pending_tagged_documents_tag = tag
        self._pending_tagged_documents_tags = tags
        self._pending_tagged_documents_paths = document_paths
        self._pending_advice_command = None
        self._pending_advice_command_draft_command = None
        self.tools.run("record_log", message=f"预览标签组批量打标签：{tag} -> {len(documents)} 份")

        lines = [
            f"批量打标签预览：{tag}标签资料",
            f"拟追加标签：{'、'.join(tags)}",
        ]
        for document_index, document in enumerate(documents, start=1):
            current_tags = "、".join(document.tags) if document.tags else "无"
            preview_tags = "、".join(self._merged_tags(document.tags, tags))
            lines.append(
                f"{document_index}. data/{document.relative_path}"
                f"（当前标签：{current_tags}；预览标签：{preview_tags}）"
            )
        lines.append("说明：这里只生成预览，不会修改资料标签。")
        lines.append(f"可继续操作：{self._tagged_document_tagging_followups(documents, tags)}")
        return "\n".join(lines)

    def _read_tagged_documents(self, tag: str) -> str:
        documents = self._tagged_documents(tag)
        if not documents:
            return f"没有找到标签为“{tag}”的资料。你可以先用 /kb-summary 查看标签分组，或给资料打标签。"

        document_paths = tuple(document.relative_path for document in documents)
        self._recent_document_path = document_paths[0]
        self._recent_document_paths = document_paths
        self._save_runtime_context()
        self.tools.run("record_log", message=f"按标签读取知识库资料：{tag} -> {len(documents)} 份")

        lines = [f"标签资料：{tag}"]
        for document_index, document in enumerate(documents, start=1):
            tag_text = f"，标签：{'、'.join(document.tags)}" if document.tags else ""
            lines.append(
                f"{document_index}. data/{document.relative_path}"
                f"（{document.searchable_line_count} 行{tag_text}）"
            )
            preview = self._document_preview(document.relative_path)
            if preview:
                lines.append(f"   摘要：{preview}")
        lines.append(f"可继续操作：读取第一份资料；给第一份资料打标签 标签；/ask {tag}")
        return "\n".join(lines)

    def _tagged_documents(self, tag: str):
        index = build_knowledge_index(self.paths)
        return tuple(document for document in index.documents if tag in document.tags)

    def _tagged_document_tagging_followups(self, documents, tags: tuple[str, ...]) -> str:
        suggestions = []
        for document_index, document in enumerate(documents[:2], start=1):
            ordinal = self._document_ordinal_label(document_index)
            preview_tags = " ".join(self._merged_tags(document.tags, tags))
            suggestions.append(f"给{ordinal}份资料打标签 {preview_tags}")
        return "；".join(suggestions)

    def _merged_tags(self, current_tags: tuple[str, ...], new_tags: tuple[str, ...]) -> tuple[str, ...]:
        merged = list(current_tags)
        for tag in new_tags:
            if tag not in merged:
                merged.append(tag)
        return tuple(merged)

    def _document_ordinal_label(self, document_index: int) -> str:
        labels = {1: "第一", 2: "第二", 3: "第三", 4: "第四", 5: "第五"}
        return labels.get(document_index, f"第{document_index}")

    def _document_preview(self, relative_path: str) -> str:
        document_path = self.paths.data_dir / relative_path
        for raw_line in document_path.read_text(encoding="utf-8").splitlines():
            text = raw_line.strip()
            if text and not text.startswith("#"):
                return text
        return ""

    def _read_recent_document(self) -> str:
        if self._recent_document_path is None:
            return "还没有最近资料。你可以先读取资料、导入资料，或说“读取 note.txt”。"
        return self.handle(f'/read "{self._recent_document_path}"')

    def _read_numbered_recent_document(self, document_index: int) -> str:
        if not self._recent_document_paths:
            return "还没有最近资料列表。你可以先读取资料、导入资料，或说“读取 note.txt”。"
        if document_index < 1 or document_index > len(self._recent_document_paths):
            return f"最近资料列表只有 {len(self._recent_document_paths)} 条，不能选择第 {document_index} 份。"
        relative_path = self._recent_document_paths[document_index - 1]
        output = self.handle(f'/read "{relative_path}"')
        return f"第 {document_index} 份资料：data/{relative_path}\n{output}"

    def _read_numbered_recent_file(self, file_index: int) -> str:
        if not self._recent_files:
            return "还没有最近文件列表。你可以先查看最近文件，或使用 /recent-files。"
        if file_index < 1 or file_index > len(self._recent_files):
            return f"最近文件列表只有 {len(self._recent_files)} 条，不能选择第 {file_index} 份。"
        recent_file = self._recent_files[file_index - 1]
        path = Path(recent_file.path)
        if not path.is_file():
            return f"最近文件已不存在：{path}。你可以先重新查看最近文件。"
        modified_at = path.stat().st_mtime
        modified_text = self._format_timestamp(modified_at)
        self.tools.run("record_log", message=f"查看最近文件详情：第 {file_index} 份 -> {path}")
        return "\n".join(
            [
                f"第 {file_index} 份最近文件：{path.name}",
                f"- 来源：{recent_file.alias}",
                f"- 路径：{path}",
                f"- 修改时间：{modified_text}",
                "- 说明：只展示文件信息，不会读取或打开文件。",
            ]
        )

    def _import_numbered_recent_file(self, file_index: int) -> str:
        if not self._recent_files:
            return "还没有最近文件列表。你可以先查看最近文件，或使用 /recent-files。"
        if file_index < 1 or file_index > len(self._recent_files):
            return f"最近文件列表只有 {len(self._recent_files)} 条，不能选择第 {file_index} 份。"
        recent_file = self._recent_files[file_index - 1]
        path = Path(recent_file.path)
        if not path.is_file():
            return f"最近文件已不存在：{path}。你可以先重新查看最近文件。"
        self.tools.run("record_log", message=f"导入最近文件到知识库：第 {file_index} 份 -> {path}")
        return self.handle(f'/import "{path}"')

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

    def _read_numbered_advice_suggestion(self, advice_index: int) -> str:
        if not self._recent_advice_suggestions:
            return "还没有最近建议。你可以先说“我该怎么导入资料”，或使用 /experience-advice 关键词。"
        if advice_index < 1 or advice_index > len(self._recent_advice_suggestions):
            return f"最近建议只有 {len(self._recent_advice_suggestions)} 条，不能选择第 {advice_index} 条。"
        suggestion = self._recent_advice_suggestions[advice_index - 1]
        self.tools.run("record_log", message=f"查看最近建议：第 {advice_index} 条")
        return f"第 {advice_index} 条建议：{suggestion}"

    def _prepare_numbered_advice_suggestion_execution(self, advice_index: int) -> str:
        suggestion, error = self._recent_advice_suggestion(advice_index)
        if error:
            return error
        assert suggestion is not None
        self._clear_pending_tagged_documents_tagging()
        command = self._executable_advice_command(suggestion)
        if command is None:
            self._pending_advice_command = None
            self._pending_advice_command_draft_command = None
            draft_command = self._advice_command_draft(suggestion)
            lines = [
                f"第 {advice_index} 条建议需要补充参数，不能直接执行：{suggestion}",
            ]
            if draft_command is not None:
                self._pending_advice_command_draft_command = self._advice_command_name(suggestion)
                lines.append(f"命令草稿：{draft_command}")
                lines.append("请把尖括号里的占位内容替换成真实参数；方括号参数可以按需保留或替换。")
            else:
                lines.append("你可以把占位内容补完整后手动输入命令。")
            return "\n".join(
                lines
            )

        self._pending_advice_command = command
        self._pending_advice_command_draft_command = None
        self.tools.run("record_log", message=f"准备执行最近建议：第 {advice_index} 条 -> {command}")
        return "\n".join(
            [
                f"准备执行第 {advice_index} 条建议：{suggestion}",
                f"命令：{command}",
                "确认执行请说“确认执行”，取消请说“取消执行”。",
            ]
        )

    def _confirm_pending_advice_suggestion_execution(self) -> str:
        tagged_documents_result = self._confirm_pending_tagged_documents_tagging()
        if tagged_documents_result is not None:
            return tagged_documents_result
        if self._pending_advice_command is None:
            return "还没有待确认的建议命令。你可以先说“执行第一条建议”。"
        command = self._pending_advice_command
        self._pending_advice_command = None
        self._pending_advice_command_draft_command = None
        self.tools.run("record_log", message=f"确认执行最近建议命令：{command}")
        return f"已确认执行建议命令：{command}\n{self.handle(command)}"

    def _cancel_pending_advice_suggestion_execution(self) -> str:
        tagged_documents_result = self._cancel_pending_tagged_documents_tagging()
        if tagged_documents_result is not None:
            return tagged_documents_result
        if self._pending_advice_command is None:
            return "还没有待取消的建议命令。"
        command = self._pending_advice_command
        self._pending_advice_command = None
        self._pending_advice_command_draft_command = None
        self.tools.run("record_log", message=f"取消执行最近建议命令：{command}")
        return f"已取消待执行建议：{command}"

    def _confirm_pending_tagged_documents_tagging(self) -> str | None:
        if not self._pending_tagged_documents_paths:
            return None
        group_tag = self._pending_tagged_documents_tag or ""
        new_tags = self._pending_tagged_documents_tags
        document_paths = self._pending_tagged_documents_paths
        self._clear_pending_tagged_documents_tagging()

        current_tags_by_path = self._knowledge_tags_by_path()
        lines = [
            f"已确认执行批量打标签：{group_tag}标签资料",
            f"追加标签：{'、'.join(new_tags)}",
        ]
        restore_commands: list[str] = []
        updated_count = 0
        for document_index, relative_path in enumerate(document_paths, start=1):
            current_tags = current_tags_by_path.get(relative_path, ())
            merged_tags = self._merged_tags(current_tags, new_tags)
            try:
                document = set_document_tags(self.paths, relative_path, merged_tags)
            except (FileNotFoundError, ValueError) as exc:
                lines.append(f"{document_index}. data/{relative_path}：失败，{exc}")
                continue
            updated_count += 1
            if current_tags:
                ordinal = self._document_ordinal_label(document_index)
                restore_commands.append(f"给{ordinal}份资料打标签 {' '.join(current_tags)}")
            lines.append(f"{document_index}. data/{document.relative_path}（{'、'.join(document.tags)}）")
        lines.append(f"操作记录：本次已更新 {updated_count} 份资料。")
        if restore_commands:
            lines.append(f"恢复提示：如需撤销本次追加，可逐份执行：{'；'.join(restore_commands)}")
        self._recent_tagged_documents_operation_tag = group_tag
        self._recent_tagged_documents_operation_tags = new_tags
        self._recent_tagged_documents_operation_updated_count = updated_count
        self._recent_tagged_documents_operation_restore_commands = tuple(restore_commands)
        self._save_runtime_context()
        self.tools.run("record_log", message=f"确认执行标签组批量打标签：{group_tag} -> {len(document_paths)} 份")
        return "\n".join(lines)

    def _cancel_pending_tagged_documents_tagging(self) -> str | None:
        if not self._pending_tagged_documents_paths:
            return None
        group_tag = self._pending_tagged_documents_tag or ""
        self._clear_pending_tagged_documents_tagging()
        self.tools.run("record_log", message=f"取消标签组批量打标签：{group_tag}")
        return f"已取消待执行批量打标签：{group_tag}标签资料"

    def _clear_pending_tagged_documents_tagging(self) -> None:
        self._pending_tagged_documents_tag = None
        self._pending_tagged_documents_tags = ()
        self._pending_tagged_documents_paths = ()

    def _knowledge_tags_by_path(self) -> dict[str, tuple[str, ...]]:
        index = build_knowledge_index(self.paths)
        return {document.relative_path: document.tags for document in index.documents}

    def _recent_advice_suggestion(self, advice_index: int) -> tuple[str | None, str | None]:
        if not self._recent_advice_suggestions:
            return None, "还没有最近建议。你可以先说“我该怎么导入资料”，或使用 /experience-advice 关键词。"
        if advice_index < 1 or advice_index > len(self._recent_advice_suggestions):
            return None, f"最近建议只有 {len(self._recent_advice_suggestions)} 条，不能选择第 {advice_index} 条。"
        return self._recent_advice_suggestions[advice_index - 1], None

    def _executable_advice_command(self, suggestion: str) -> str | None:
        command = self._advice_command_text(suggestion)
        if command is None:
            return None
        placeholder_words = ("[", "]", "...", "源文件", "目录路径", "目标文件名", "文件名", "标签", "文本", "问题", "关键词", "别名")
        if any(word in command for word in placeholder_words):
            return None
        return command

    def _advice_command_draft(self, suggestion: str) -> str | None:
        command = self._advice_command_text(suggestion)
        if command is None:
            return None
        return " ".join(self._advice_command_draft_token(token) for token in command.split())

    def _advice_command_text(self, suggestion: str) -> str | None:
        command = suggestion.split("：", 1)[0].strip()
        if not command.startswith("/"):
            return None
        return command

    def _advice_command_name(self, suggestion: str) -> str | None:
        command = self._advice_command_text(suggestion)
        if command is None:
            return None
        return command.split()[0]

    def _advice_command_draft_token(self, token: str) -> str:
        if token.startswith("/") or (token.startswith("[") and token.endswith("]")):
            return token
        placeholder_tokens = {
            "源文件或目录路径",
            "目录路径",
            "文件名",
            "标签",
            "文本",
            "问题",
            "关键词",
            "别名",
            "常用目录别名",
            "清单路径或URL",
            "已识别的语音文本",
            "经验内容",
        }
        if token in placeholder_tokens or token.endswith("..."):
            return f"<{token}>"
        return token

    def _recent_search_result_path(self, result_index: int) -> tuple[str | None, str | None]:
        if not self._recent_search_result_paths:
            return None, "还没有最近搜索结果。你可以先提问，例如“Jarvis Lite 使用什么？”。"
        if result_index < 1 or result_index > len(self._recent_search_result_paths):
            return None, f"最近搜索结果只有 {len(self._recent_search_result_paths)} 条，不能选择第 {result_index} 条。"
        return self._recent_search_result_paths[result_index - 1], None

    def _remember_recent_document(self, relative_path: str) -> None:
        self._recent_document_path = relative_path
        self._recent_document_paths = self._recent_document_list_with(relative_path)
        self._save_runtime_context()

    def _recent_document_list_with(self, relative_path: str) -> tuple[str, ...]:
        paths = [relative_path]
        for existing_path in self._recent_document_paths:
            if existing_path not in paths:
                paths.append(existing_path)
            if len(paths) >= 5:
                break
        return tuple(paths)

    def _remember_recent_search_results(self, relative_paths: tuple[str, ...]) -> None:
        self._recent_search_result_paths = relative_paths
        self._save_runtime_context()

    def _remember_recent_advice_suggestions(self, suggestions: tuple[str, ...]) -> None:
        self._recent_advice_suggestions = suggestions
        self._pending_advice_command = None
        self._pending_advice_command_draft_command = None
        self._save_runtime_context()

    def _remember_recent_files(self, recent_files: tuple[RuntimeRecentFileContext, ...]) -> None:
        self._recent_files = recent_files
        self._save_runtime_context()

    def _remember_recent_directory(self, alias: str, directory_path: Path) -> None:
        self._recent_directory = CommonDirectory(alias, directory_path)
        self._save_runtime_context()

    def _restore_recent_directory(self, context: RuntimeDirectoryContext | None) -> CommonDirectory | None:
        if context is None:
            return None
        return CommonDirectory(context.alias, Path(context.path))

    def _runtime_context(self) -> RuntimeContext:
        recent_directory = None
        if self._recent_directory is not None:
            recent_directory = RuntimeDirectoryContext(
                alias=self._recent_directory.alias,
                path=str(self._recent_directory.path),
            )
        return RuntimeContext(
            recent_document_path=self._recent_document_path,
            recent_document_paths=self._recent_document_paths,
            recent_directory=recent_directory,
            recent_search_result_paths=self._recent_search_result_paths,
            recent_advice_suggestions=self._recent_advice_suggestions,
            recent_files=self._recent_files,
            recent_tagged_documents_operation=self._runtime_tagged_documents_operation(),
        )

    def _save_runtime_context(self) -> None:
        save_runtime_context(self.paths, self._runtime_context())

    def _runtime_tagged_documents_operation(self) -> RuntimeTaggedDocumentsOperationContext | None:
        if self._recent_tagged_documents_operation_tag is None:
            return None
        return RuntimeTaggedDocumentsOperationContext(
            tag=self._recent_tagged_documents_operation_tag,
            tags=self._recent_tagged_documents_operation_tags,
            updated_count=self._recent_tagged_documents_operation_updated_count,
            restore_commands=self._recent_tagged_documents_operation_restore_commands,
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

    def _recent_file_directories(self) -> tuple[CommonDirectory, ...]:
        directories: list[CommonDirectory] = []
        seen_paths: set[str] = set()

        def add(directory: CommonDirectory | None) -> None:
            if directory is None:
                return
            resolved_path = directory.path.resolve()
            path_key = str(resolved_path).casefold()
            if path_key in seen_paths:
                return
            seen_paths.add(path_key)
            directories.append(CommonDirectory(directory.alias, resolved_path))

        for directory in list_common_directories(self.paths):
            add(directory)
        for alias in ("项目", "桌面", "下载"):
            add(self._known_directory(alias))
        return tuple(directories)

    def _known_directory(self, alias: str) -> CommonDirectory | None:
        if alias.strip().lower() in {"项目", "当前项目", "project", "repo", "repository"}:
            return CommonDirectory(alias, self.paths.root.resolve())
        for directory_name in self._known_directory_candidates(alias):
            directory = Path.home() / directory_name
            if directory.is_dir():
                return CommonDirectory(alias, directory.resolve())
        return None

    def _known_directory_candidates(self, alias: str) -> tuple[str, ...]:
        normalized_alias = alias.strip().lower()
        if normalized_alias in {"桌面", "desktop"}:
            return ("Desktop", "桌面")
        if normalized_alias in {"下载", "download", "downloads"}:
            return ("Downloads", "下载")
        return ()

    def _project_path(self, path: Path) -> str:
        return path.relative_to(self.paths.root).as_posix()

    def _strip_quotes(self, value: str) -> str:
        return value.strip().strip('"').strip("'")

    def _format_timestamp(self, timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def _status(self) -> str:
        return "\n".join(
            [
                "Jarvis Lite 当前状态：本地助手基础闭环已具备。",
                "- 入口：命令行、桌面小助手、助手面板和系统托盘",
                f"- 长期记忆：{self._project_path(self.paths.profile_path)}",
                f"- 经验记忆：{self._project_path(self.paths.memory_dir / 'experiences.md')}",
                f"- 个人知识库：{self._project_path(self.paths.data_dir)}",
                f"- 工具日志：{self._project_path(self.paths.log_path)}",
                "- 自然语言：已支持能力询问、身份询问、日报、知识库、更新和打开磁盘等第一批意图",
                "- 语音入口：/voice、/speak、/voice-status",
                "- 工作台自动化：常用目录、最近文件、日报、整理预览和目录打开记录",
                "- 桌面能力：小助手窗口、面板、托盘、主题、开机启动、安装包、更新检查和下载",
                "- 会话能力：/history、/save-summary、/clear",
                "- 记忆写入：/remember、/experience、我叫...、我是...",
                "- 本地验证：python -m unittest discover -s tests -v",
            ]
        )
