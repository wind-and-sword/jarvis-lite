from __future__ import annotations

import re
import shlex
from dataclasses import dataclass
from datetime import datetime, timedelta
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
from .inner_brain import (
    InnerBrain,
    InnerBrainEvaluationCase,
    InnerBrainEvaluationReport,
    InnerBrainEvaluationSaveResult,
    InnerBrainPolicy,
    InnerBrainResult,
    InnerBrainTrainingSaveResult,
    complete_inner_brain_clarification,
    describe_inner_brain_evaluation,
    describe_inner_brain_resolved_evaluation,
    describe_inner_brain_result,
    evaluate_inner_brain,
    export_inner_brain_evaluation_report,
    save_local_evaluation_case,
    save_labeled_runtime_training_sample,
    save_runtime_training_sample,
)
from .llm import (
    LLMIntent,
    LLMRouter,
    LLMSettings,
    build_llm_router,
    describe_llm_config_examples,
    is_llm_allowed_command,
    llm_local_config_path,
    summarize_llm_usage,
    write_llm_example_config,
    write_llm_local_config_draft,
    write_llm_local_config_values,
)
from .search import (
    SearchResult,
    SearchRouter,
    build_search_router,
    describe_search_config_examples,
    search_local_config_path,
    write_search_example_config,
    write_search_local_config_draft,
    write_search_local_config_values,
)
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
    RuntimeInnerBrainCandidateContext,
    RuntimeLLMCallContext,
    RuntimeLLMClarificationContext,
    RuntimeRecentFileContext,
    RuntimeRouteDecisionContext,
    RuntimeTaggedDocumentsOperationContext,
    RuntimeWebSearchContext,
    RuntimeWebSearchResultContext,
    load_runtime_context,
    save_runtime_context,
)
from .tools import ToolRegistry
from .update import describe_update_download, describe_update_status, update_download_dir
from .voice import describe_voice, speak_text


TEACHABLE_INNER_BRAIN_COMMAND_INTENTS = {
    "/help": "assistant.help",
    "/status": "assistant.status",
    "/memory": "memory.status",
    "/experiences": "experience.status",
    "/llm-status": "llm.status",
    "/llm-enable": "llm.enable",
    "/llm-config-init": "llm.config_init",
    "/llm-config-check": "llm.config_check",
    "/llm-config-set": "llm.config_set",
    "/llm-smoke": "llm.smoke",
    "/llm-usage": "llm.usage",
    "/llm-context-preview": "llm.context_preview",
    "/search-status": "web.search.status",
    "/search-enable": "web.search.enable",
    "/search-config-init": "web.search.config_init",
    "/search-config-check": "web.search.config_check",
    "/search-config-set": "web.search.config_set",
    "/search-smoke": "web.search.smoke",
    "/search": "web.search",
    "/search-summary": "web.search_summarize",
    "/search-open": "web_search.open_numbered",
    "/search-compare": "web_search.compare_recent",
    "/search-save-summary": "web_search.save_summary",
    "/search-import-summary": "web_search.import_summary",
    "/kb": "knowledge.status",
    "/knowledge": "knowledge.status",
    "/kb-summary": "knowledge.summary",
    "/knowledge-summary": "knowledge.summary",
    "/voice-status": "voice.status",
    "/automation-status": "automation.status",
    "/recent-files": "context.recent_files",
    "/tag-history": "tag.history",
    "/batch-tag-history": "tag.history",
    "/update-status": "update.status",
    "/dirs": "directory.list",
    "/daily-report": "report.daily",
}


@dataclass(frozen=True)
class PendingLLMClarification:
    original_prompt: str
    clarification: str
    context: tuple[str, ...]
    clarification_count: int = 1
    created_at: str = ""


@dataclass(frozen=True)
class InnerBrainCandidateSummary:
    decision: RuntimeRouteDecisionContext
    count: int


LLM_CLARIFICATION_MAX_ROUNDS = 3
LLM_CLARIFICATION_EXPIRES_AFTER_SECONDS = 12 * 60 * 60


class JarvisAgent:
    """负责解析命令并调度第一阶段本地能力。"""

    def __init__(
        self,
        paths: ProjectPaths | None = None,
        llm_router: LLMRouter | None = None,
        search_router: SearchRouter | None = None,
        inner_brain: InnerBrain | None = None,
    ):
        self.paths = paths or build_project_paths()
        self.tools = ToolRegistry(self.paths)
        self._llm_router_injected = llm_router is not None
        self.llm_router = llm_router or build_llm_router(paths=self.paths)
        self._search_router_injected = search_router is not None
        self.search_router = search_router or build_search_router(paths=self.paths)
        self.inner_brain = inner_brain or InnerBrain(self.paths)
        runtime_context = load_runtime_context(self.paths)
        self._recent_document_path: str | None = runtime_context.recent_document_path
        self._recent_document_paths: tuple[str, ...] = runtime_context.recent_document_paths
        self._recent_directory: CommonDirectory | None = self._restore_recent_directory(runtime_context.recent_directory)
        self._recent_search_result_paths: tuple[str, ...] = runtime_context.recent_search_result_paths
        self._recent_web_search: RuntimeWebSearchContext | None = runtime_context.recent_web_search
        self._recent_advice_suggestions: tuple[str, ...] = runtime_context.recent_advice_suggestions
        self._recent_files: tuple[RuntimeRecentFileContext, ...] = runtime_context.recent_files
        self._pending_advice_command: str | None = None
        self._pending_advice_command_draft_command: str | None = None
        self._pending_tagged_documents_tag: str | None = None
        self._pending_tagged_documents_tags: tuple[str, ...] = ()
        self._pending_tagged_documents_paths: tuple[str, ...] = ()
        self._pending_inner_brain_clarification: InnerBrainResult | None = None
        self._pending_llm_clarification: PendingLLMClarification | None = (
            self._restore_pending_llm_clarification(runtime_context.pending_llm_clarification)
        )
        self._recent_llm_call: RuntimeLLMCallContext | None = runtime_context.recent_llm_call
        self._recent_route_decision: RuntimeRouteDecisionContext | None = runtime_context.recent_route_decision
        self._recent_route_decisions: tuple[RuntimeRouteDecisionContext, ...] = (
            runtime_context.recent_route_decisions
        )
        self._inner_brain_candidate_stats: tuple[RuntimeInnerBrainCandidateContext, ...] = (
            runtime_context.inner_brain_candidates or ()
        )
        self._inner_brain_candidate_stats_initialized = runtime_context.inner_brain_candidates is not None
        self._recent_tagged_documents_operations: tuple[RuntimeTaggedDocumentsOperationContext, ...] = (
            runtime_context.recent_tagged_documents_operations
        )
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
        if runtime_context.pending_llm_clarification is not None and self._pending_llm_clarification is None:
            self._save_runtime_context()

    def handle(self, user_input: str) -> str:
        prompt = user_input.strip()
        if not prompt:
            return "请输入问题或命令。输入 /help 查看可用命令。"

        if self._is_explicit_command_prompt(prompt) and not self._is_route_observability_prompt(prompt):
            self._remember_command_route(prompt)

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
        if prompt in {"/llm-status", "llm-status"}:
            return self.llm_router.describe()
        if prompt in {"/search-status", "search-status"}:
            return self.search_router.describe()
        if prompt in {"/inner-brain-status", "inner-brain-status"}:
            self.tools.run("record_log", message="查看 InnerBrain 本地内脑状态")
            return self.inner_brain.describe_status()
        if self._is_inner_brain_eval_local_failures_prompt(prompt):
            self.tools.run("record_log", message="执行 InnerBrain 本机评估集并只显示失败样本")
            report = evaluate_inner_brain(self.inner_brain, source_filter="local_evaluation")
            return self._describe_inner_brain_local_failed_evaluation(report)
        if self._is_inner_brain_eval_local_resolved_prompt(prompt):
            args = shlex.split(prompt)[1:] if prompt.startswith("/") else []
            return self._inner_brain_local_resolved_evaluation(args)
        if self._is_inner_brain_eval_local_prompt(prompt):
            self.tools.run("record_log", message="执行 InnerBrain 本机评估集")
            report = evaluate_inner_brain(self.inner_brain, source_filter="local_evaluation")
            return self._describe_inner_brain_local_evaluation(report)
        if self._is_inner_brain_eval_failures_prompt(prompt):
            self.tools.run("record_log", message="执行 InnerBrain 本地评估集并只显示失败样本")
            return describe_inner_brain_evaluation(evaluate_inner_brain(self.inner_brain), failures_only=True)
        if self._is_inner_brain_eval_prompt(prompt):
            self.tools.run("record_log", message="执行 InnerBrain 本地评估集")
            return describe_inner_brain_evaluation(evaluate_inner_brain(self.inner_brain))
        if self._is_inner_brain_candidates_prompt(prompt):
            return self._inner_brain_candidates_status()
        if prompt in {"/llm-usage", "llm-usage"}:
            self.tools.run("record_log", message="查看 LLM 用量汇总")
            return summarize_llm_usage(self.paths.log_path.read_text(encoding="utf-8").splitlines())
        if prompt in {"/llm-context-preview", "llm-context-preview"}:
            self.tools.run("record_log", message="预览 LLM fallback 上下文")
            return self._llm_context_preview()
        if self._is_recent_context_prompt(prompt):
            return self._recent_context_status()
        if self._is_route_history_prompt(prompt):
            return self._route_history_status()
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
        if prompt in {"/tag-history", "tag-history", "/batch-tag-history", "batch-tag-history"}:
            return self._tagged_documents_history_status()
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
                self._remember_route_decision(
                    "memory-fallback",
                    "identity",
                    prompt,
                    "长期记忆命中",
                    "source=memory/profile.md action=read",
                )
                return identity
            self._remember_route_decision(
                "memory-fallback",
                "identity",
                prompt,
                "长期记忆未命中",
                "source=memory/profile.md action=read",
            )
            return "我还不知道你是谁。你可以说“我叫张三”或使用 /remember 用户姓名：张三。"

        if prompt.startswith("/"):
            return self._handle_command(prompt)

        fact = parse_identity_fact(prompt)
        if fact:
            response = self._remember(fact)
            self._remember_route_decision(
                "memory-fallback",
                "remember",
                prompt,
                "长期记忆写入",
                "source=memory/profile.md action=write",
            )
            return response

        teach_response = self._teach_inner_brain_sample_from_natural_language(prompt)
        if teach_response is not None:
            return teach_response

        clarification_response = self._handle_pending_inner_brain_clarification(prompt)
        if clarification_response is not None:
            return clarification_response

        llm_clarification_response = self._handle_pending_llm_clarification(prompt)
        if llm_clarification_response is not None:
            return llm_clarification_response

        inner_brain_result = self.inner_brain.understand(prompt)
        if inner_brain_result.policy == InnerBrainPolicy.EXECUTE and inner_brain_result.natural_language_intent is not None:
            self.tools.run(
                "record_log",
                message=(
                    "InnerBrain 命中："
                    f"intent={inner_brain_result.intent} "
                    f"source={inner_brain_result.source} "
                    f"confidence={inner_brain_result.confidence:.2f}"
                ),
            )
            response = self._handle_natural_language_intent(inner_brain_result.natural_language_intent)
            self._remember_route_decision(
                "inner-brain",
                inner_brain_result.intent,
                prompt,
                "本地内脑命中",
                self._inner_brain_route_explanation(inner_brain_result),
            )
            return response
        if inner_brain_result.policy == InnerBrainPolicy.CLARIFY:
            response = self._inner_brain_clarification(inner_brain_result)
            self._remember_route_decision(
                "inner-brain-clarify",
                inner_brain_result.intent,
                prompt,
                "本地内脑需要补充槽位",
                self._inner_brain_route_explanation(inner_brain_result),
            )
            return response

        data_answer = self._answer_from_data(prompt)
        if data_answer:
            self.tools.run("record_log", message=f"基于 data 目录回答普通问题：{prompt}")
            self._remember_route_decision(
                "knowledge",
                "data-answer",
                prompt,
                "本地知识库命中",
                "source=data action=local-answer",
            )
            return data_answer

        llm_answer = self._answer_from_llm(prompt)
        if llm_answer:
            self.tools.run("record_log", message=f"LLM 外脑处理输入：{prompt}")
            detail = self._recent_llm_call.intent_type if self._recent_llm_call is not None else "unknown"
            self._remember_route_decision(
                "llm-fallback",
                detail,
                prompt,
                "LLM 外脑处理",
                self._llm_route_explanation(),
            )
            return llm_answer

        profile = read_profile(self.paths)
        summary = summarize_profile(profile)
        self._remember_route_decision(
            "memory-fallback",
            "profile",
            prompt,
            "长期记忆兜底",
            "source=memory/profile.md action=fallback",
        )
        return f"Jarvis Lite 已读取长期记忆。当前记忆摘要：{self._sentence(summary)}你可以输入 /help 查看我现在能做的事。"

    def llm_clarification_status_text(self) -> str:
        """返回桌面面板可展示的 LLM 外脑待补充状态。"""

        pending = self._pending_llm_clarification
        if pending is None:
            return "外脑待补充：无"
        return "\n".join(
            [
                (
                    f"外脑待补充（{pending.clarification_count}/"
                    f"{LLM_CLARIFICATION_MAX_ROUNDS}）：{pending.clarification}"
                ),
                f"原始问题：{pending.original_prompt}",
                "回复缺失信息继续，或输入“取消补充”。",
            ]
        )

    def llm_activity_status_text(self) -> str:
        """返回桌面面板可展示的 LLM 外脑运行状态和最近调用快照。"""

        settings = self.llm_router.settings
        lines = [
            f"外脑运行状态：{'已启用' if settings.enabled else '未启用'}",
            f"Provider：{settings.provider}",
        ]
        if settings.adapter_provider != settings.provider:
            lines.append(f"Adapter：{settings.adapter_provider}")
        if settings.model:
            lines.append(f"Model：{settings.model}")
        issues = settings.configuration_issues()
        if issues:
            lines.append(f"配置问题：{len(issues)} 项")
        if self._recent_llm_call is None:
            lines.append("最近调用：无")
            return "\n".join(lines)

        call = self._recent_llm_call
        lines.append(f"最近调用：{call.source} / {call.intent_type}")
        if call.created_at:
            lines.append(f"时间：{call.created_at}")
        if call.provider and call.provider != settings.provider:
            lines.append(f"调用 Provider：{call.provider}")
        if call.model and call.model != settings.model:
            lines.append(f"调用 Model：{call.model}")
        lines.append(f"输入：{call.prompt}")
        if call.summary:
            lines.append(f"结果：{call.summary}")
        return "\n".join(lines)

    def route_status_text(self) -> str:
        """返回桌面面板可展示的最近输入路由决策。"""

        decision = self._recent_route_decision
        if decision is None:
            return "最近路由：无"
        lines = [f"最近路由：{decision.route} / {decision.detail}"]
        if decision.created_at:
            lines.append(f"时间：{decision.created_at}")
        lines.append(f"输入：{decision.prompt}")
        if decision.summary:
            lines.append(f"结果：{decision.summary}")
        if decision.explanation:
            lines.append(f"依据：{decision.explanation}")
        if len(self._recent_route_decisions) > 1:
            lines.append("最近路由历史：")
            for index, route_decision in enumerate(self._recent_route_decisions, start=1):
                lines.append(self._route_history_line(index, route_decision))
        return "\n".join(lines)

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

        if command == "/llm-config-example":
            self.tools.run("record_log", message="查看 LLM 配置模板")
            return describe_llm_config_examples(args[0] if args else "")
        if command == "/llm-config-init":
            return self._llm_config_init(args[0] if args else "")
        if command == "/llm-config-check":
            return self._llm_config_check()
        if command == "/llm-config-set":
            return self._llm_config_set(args)
        if command == "/llm-enable":
            return self._llm_enable_guidance()
        if command == "/search-config-example":
            self.tools.run("record_log", message="查看联网搜索配置模板")
            return describe_search_config_examples(args[0] if args else "")
        if command == "/search-config-init":
            return self._search_config_init(args[0] if args else "")
        if command == "/search-config-check":
            return self._search_config_check()
        if command == "/search-config-set":
            return self._search_config_set(args)
        if command == "/search-enable":
            return self._search_enable_guidance()
        if command == "/search-smoke":
            return self._search_smoke(" ".join(args))
        if command == "/search":
            if not args:
                return "用法：/search 关键词"
            return self._search_web(" ".join(args))
        if command == "/search-summary":
            if not args:
                return "用法：/search-summary 关键词"
            return self._search_web_and_summarize(" ".join(args))
        if command == "/search-open":
            if not args:
                return "用法：/search-open 编号"
            return self._open_recent_web_search_source(args[0])
        if command == "/search-compare":
            return self._compare_recent_web_search_sources()
        if command == "/search-save-summary":
            return self._save_recent_web_search_summary(" ".join(args))
        if command == "/search-import-summary":
            return self._import_recent_web_search_summary(" ".join(args))
        if command == "/inner-brain-preview":
            if not args:
                return "用法：/inner-brain-preview 文本"
            preview_prompt = " ".join(args)
            self.tools.run("record_log", message=f"预览 InnerBrain 识别结果：{preview_prompt}")
            return describe_inner_brain_result(self.inner_brain.understand(preview_prompt))
        if command == "/inner-brain-adopt":
            if not args:
                return "用法：/inner-brain-adopt 文本"
            sample_prompt = " ".join(args)
            return self._adopt_inner_brain_sample(sample_prompt)
        if command == "/inner-brain-label":
            return self._label_inner_brain_sample(prompt)
        if command in {"/inner-brain-teach", "/teach"}:
            return self._teach_inner_brain_sample(prompt, command)
        if command == "/inner-brain-eval-add":
            return self._save_inner_brain_command_evaluation_case(prompt, command)
        if command == "/inner-brain-eval-label":
            return self._save_inner_brain_labeled_evaluation_case(prompt, command)
        if command == "/inner-brain-eval-local-file":
            return self._inner_brain_local_file_evaluation(args, failures_only=False)
        if command in {"/inner-brain-eval-local-file-failed", "/inner-brain-eval-local-file-failures"}:
            return self._inner_brain_local_file_evaluation(args, failures_only=True)
        if command == "/inner-brain-eval-local-resolved":
            return self._inner_brain_local_resolved_evaluation(args)
        if command == "/inner-brain-eval-local-report":
            return self._export_inner_brain_local_evaluation_report(args)
        if command == "/inner-brain-eval-add-candidate":
            return self._save_inner_brain_command_evaluation_candidate(prompt, command)
        if command == "/inner-brain-eval-label-candidate":
            return self._save_inner_brain_labeled_evaluation_candidate(prompt, command)
        if command == "/inner-brain-teach-candidate":
            return self._teach_inner_brain_candidate(prompt, command)
        if command == "/inner-brain-label-candidate":
            return self._label_inner_brain_candidate(prompt, command)
        if command == "/llm-smoke":
            smoke_prompt = " ".join(args)
            self.tools.run("record_log", message="执行 LLM smoke 调用")
            return self._llm_smoke(smoke_prompt)

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
                "/llm-status：查看 LLM 外脑 provider 状态",
                "/llm-enable：查看外脑启用状态和本地配置路径",
                "/inner-brain-status：查看 InnerBrain 本地内脑状态",
                "/inner-brain-eval：执行 InnerBrain 评估集，失败时显示显式训练建议",
                "/inner-brain-eval-failed：只显示 InnerBrain 评估失败样本",
                "/inner-brain-eval-local：只执行本机 InnerBrain 评估样本",
                "/inner-brain-eval-local-failed：只显示本机 InnerBrain 评估失败样本",
                "/inner-brain-eval-local-report [文件名]：导出本机 InnerBrain 失败评估报告",
                "/inner-brain-eval-local-file 文件名：只执行指定本机评估 JSONL",
                "/inner-brain-eval-local-file-failed 文件名：只显示指定本机评估 JSONL 的失败样本",
                "/inner-brain-eval-local-resolved [文件名]：只读查看本机评估已处理样本",
                "/inner-brain-eval-add 文本 => /命令：保存本机评估样本，不训练",
                "/inner-brain-eval-label 文本 => intent [slot=value ...]：保存本机评估标注，不训练",
                "/inner-brain-eval-add-candidate 编号 => /命令：把训练候选按编号保存为评估样本",
                "/inner-brain-eval-label-candidate 编号 => intent [slot=value ...]：把训练候选按编号保存为评估标注",
                "/inner-brain-preview 文本：预览 InnerBrain 识别结果，不执行动作",
                "/inner-brain-adopt 文本：采纳 InnerBrain 识别结果为运行态样本",
                "/inner-brain-label 文本 => intent [slot=value ...]：人工标注 InnerBrain runtime 样本",
                "/inner-brain-teach 文本 => /命令：把自然语言短句教学为已知命令",
                "/inner-brain-candidates：查看最近输入中的内脑训练候选",
                "/inner-brain-teach-candidate 编号 => /命令：把训练候选按编号教学为命令",
                "/inner-brain-label-candidate 编号 => intent [slot=value ...]：把训练候选按编号人工标注",
                "/llm-usage：查看 LLM token 用量汇总",
                "/llm-smoke [prompt]：强制调用 LLM 做一次配置验证",
                "/llm-context-preview：预览 LLM fallback 上下文，不调用 provider",
                "/route-history：查看最近 5 条输入的路由历史详情",
                "/llm-config-example [provider]：查看 LLM 环境变量配置模板",
                "/llm-config-init [provider]：生成外脑本地配置草稿",
                "/llm-config-check：只读检查外脑本地配置，不调用 provider",
                "/llm-config-set key=value ...：写入外脑本地配置",
                "/search-status：查看联网搜索 provider 状态",
                "/search-enable：查看联网搜索启用状态和本地配置路径",
                "/search-config-example [provider]：查看联网搜索环境变量配置模板",
                "/search-config-init [provider]：生成联网搜索本地配置草稿",
                "/search-config-check：只读检查联网搜索本地配置，不调用 provider",
                "/search-config-set key=value ...：写入联网搜索本地配置",
                "/search-smoke [query]：测试联网搜索 provider 连通性，不写入最近上下文",
                "/search 关键词：联网搜索并返回来源",
                "/search-summary 关键词：联网搜索并交给 LLM 外脑总结",
                "/search-open 编号：查看最近联网搜索的编号来源 URL",
                "/search-compare：让 LLM 外脑比较最近联网搜索来源",
                "/search-save-summary [文件名]：保存最近联网搜索摘要到 word/",
                "/search-import-summary [文件名]：导入最近联网搜索摘要到 data/",
                "/kb：查看个人知识库状态",
                "/kb-summary：查看知识库资料摘要",
                "/voice-status：查看阶段 3 语音入口状态",
                "/speak 文本：播报一段文本",
                "/voice 已识别的语音文本：按语音入口处理文本并播报回答",
                "/automation-status：查看阶段 4 自动化状态",
                "/recent-files：查看常用目录、项目目录、桌面和下载目录中的最近文件",
                "/tag-history：查看最近批量打标签历史",
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
        if intent.name == "greeting":
            return self._greeting(intent.alias)
        if intent.name == "assistant_identity":
            return self._assistant_identity()
        if intent.name == "capabilities":
            return self._capability_summary()
        if intent.name == "recent_context_status":
            return self._recent_context_status()
        if intent.name == "recent_files_status":
            return self._recent_files_status()
        if intent.name == "delete_desktop_shortcuts":
            return self._delete_desktop_shortcuts(intent.items)
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
        if intent.name == "read_tagged_documents_history_documents":
            return self._read_tagged_documents_history_documents(intent.result_index)
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

    def _adopt_inner_brain_sample(self, sample_prompt: str) -> str:
        result = self.inner_brain.understand(sample_prompt)
        try:
            save_result = save_runtime_training_sample(self.paths, sample_prompt, result)
        except ValueError as exc:
            self.tools.run("record_log", message=f"InnerBrain 样本保存失败：{sample_prompt} -> {exc}")
            return "\n".join(
                [
                    f"无法保存 InnerBrain 样本：{exc}",
                    f"- 意图：{result.intent}",
                    f"- 策略：{result.policy.value}",
                    f"- 原因：{result.reason}",
                ]
            )

        self.inner_brain = InnerBrain(self.paths)
        self._forget_inner_brain_candidate(save_result.sample.text)
        self.tools.run(
            "record_log",
            message=(
                "采纳 InnerBrain runtime 样本："
                f"intent={save_result.sample.intent} "
                f"created={save_result.created} "
                f"text={save_result.sample.text}"
            ),
        )
        return self._describe_inner_brain_sample_save(save_result, result)

    def _inner_brain_candidates_status(self) -> str:
        self.tools.run("record_log", message="查看 InnerBrain 训练候选")
        candidates = self._inner_brain_candidate_summaries()
        if not candidates:
            return "\n".join(
                [
                    "InnerBrain 训练候选：暂无。",
                    "- 最近输入都已经由命令、本地内脑或知识库稳定处理，暂时不需要写入新样本。",
                ]
            )

        lines = [
            "InnerBrain 训练候选：",
            "说明：这里只列候选，不自动训练；候选出现次数来自本地运行态统计。",
        ]
        for index, candidate in enumerate(candidates, start=1):
            lines.extend(self._inner_brain_candidate_lines(index, candidate))
        return "\n".join(lines)

    def _is_inner_brain_candidate_decision(self, decision: RuntimeRouteDecisionContext) -> bool:
        return decision.route in {"llm-fallback", "memory-fallback", "inner-brain-clarify"}

    def _inner_brain_candidate_decisions(self) -> tuple[RuntimeRouteDecisionContext, ...]:
        return tuple(candidate.decision for candidate in self._inner_brain_candidate_summaries())

    def _inner_brain_candidate_summaries(self) -> tuple[InnerBrainCandidateSummary, ...]:
        if self._inner_brain_candidate_stats_initialized:
            return tuple(
                InnerBrainCandidateSummary(
                    decision=self._inner_brain_candidate_decision(candidate),
                    count=candidate.count,
                )
                for candidate in self._inner_brain_candidate_stats
            )

        candidates_by_prompt: dict[str, InnerBrainCandidateSummary] = {}
        for decision in self._recent_route_decisions:
            if not self._is_inner_brain_candidate_decision(decision):
                continue
            prompt_key = decision.prompt.strip()
            if not prompt_key:
                continue
            existing = candidates_by_prompt.get(prompt_key)
            if existing is None:
                candidates_by_prompt[prompt_key] = InnerBrainCandidateSummary(decision=decision, count=1)
            else:
                candidates_by_prompt[prompt_key] = InnerBrainCandidateSummary(
                    decision=existing.decision,
                    count=existing.count + 1,
                )
        return tuple(sorted(candidates_by_prompt.values(), key=lambda candidate: -candidate.count))

    def _inner_brain_candidate_decision(
        self,
        candidate: RuntimeInnerBrainCandidateContext,
    ) -> RuntimeRouteDecisionContext:
        return RuntimeRouteDecisionContext(
            route=candidate.route,
            detail=candidate.detail,
            prompt=candidate.prompt,
            summary=candidate.summary,
            explanation=candidate.explanation,
            created_at=candidate.last_seen_at,
        )

    def _inner_brain_candidate_lines(self, index: int, candidate: InnerBrainCandidateSummary) -> list[str]:
        decision = candidate.decision
        sample_text = decision.prompt
        lines = [
            f"{index}. {sample_text}",
            f"   当前路由：{decision.route} / {decision.detail}",
            f"   出现次数：{candidate.count}",
        ]
        if decision.summary:
            lines.append(f"   结果：{decision.summary}")
        if decision.explanation:
            lines.append(f"   依据：{decision.explanation}")
        lines.append(f"   固定为命令：/inner-brain-teach {sample_text} => /命令")
        lines.append(f"   按编号固定：/inner-brain-teach-candidate {index} => /命令")
        lines.append(f"   人工标注：/inner-brain-label {sample_text} => intent slot=value")
        lines.append(f"   按编号标注：/inner-brain-label-candidate {index} => intent slot=value")
        lines.append(f"   保存评估命令：/inner-brain-eval-add-candidate {index} => /命令")
        lines.append(f"   保存评估标注：/inner-brain-eval-label-candidate {index} => intent slot=value")
        return lines

    def _label_inner_brain_sample(self, prompt: str) -> str:
        usage = "用法：/inner-brain-label 文本 => intent [slot=value ...]"
        body = prompt[len("/inner-brain-label") :].strip()
        if "=>" not in body:
            return usage

        sample_text, raw_label = (part.strip() for part in body.split("=>", 1))
        if not sample_text or not raw_label:
            return usage
        return self._save_inner_brain_labeled_sample(sample_text, raw_label, usage)

    def _label_inner_brain_candidate(self, prompt: str, command: str) -> str:
        usage = "用法：/inner-brain-label-candidate 编号 => intent [slot=value ...]"
        body = prompt[len(command) :].strip()
        parsed = self._parse_inner_brain_label_candidate_body(body)
        if parsed is None:
            return usage
        candidate_index, raw_label = parsed
        candidates = self._inner_brain_candidate_decisions()
        if candidate_index < 1 or candidate_index > len(candidates):
            return "\n".join(
                [
                    f"没有第 {candidate_index} 条 InnerBrain 训练候选。",
                    "请先运行 /inner-brain-candidates 查看当前候选编号。",
                ]
            )
        return self._save_inner_brain_labeled_sample(candidates[candidate_index - 1].prompt, raw_label, usage)

    def _save_inner_brain_labeled_sample(self, sample_text: str, raw_label: str, usage: str) -> str:
        try:
            label_parts = shlex.split(raw_label, posix=True)
        except ValueError as exc:
            return f"标注参数错误：{exc}\n{usage}"
        if not label_parts:
            return usage

        intent = label_parts[0]
        try:
            slots, missing = self._inner_brain_label_slots(label_parts[1:])
            save_result = save_labeled_runtime_training_sample(self.paths, sample_text, intent, slots, missing)
        except ValueError as exc:
            self.tools.run("record_log", message=f"InnerBrain 人工标注失败：{sample_text} -> {exc}")
            return f"标注参数错误：{exc}\n{usage}"

        self.inner_brain = InnerBrain(self.paths)
        self._forget_inner_brain_candidate(save_result.sample.text)
        self.tools.run(
            "record_log",
            message=(
                "保存 InnerBrain 人工标注样本："
                f"intent={save_result.sample.intent} "
                f"created={save_result.created} "
                f"text={save_result.sample.text}"
            ),
        )
        return self._describe_inner_brain_labeled_sample_save(save_result, missing)

    def _save_inner_brain_command_evaluation_case(self, prompt: str, command: str) -> str:
        usage = "用法：/inner-brain-eval-add 文本 => /命令"
        body = prompt[len(command) :].strip()
        parsed = self._parse_inner_brain_teach_body(body)
        if parsed is None:
            return usage
        sample_text, target_command = parsed
        return self._save_inner_brain_command_evaluation_sample(sample_text, target_command, usage)

    def _save_inner_brain_command_evaluation_candidate(self, prompt: str, command: str) -> str:
        usage = "用法：/inner-brain-eval-add-candidate 编号 => /命令"
        body = prompt[len(command) :].strip()
        parsed = self._parse_inner_brain_teach_candidate_body(body)
        if parsed is None:
            return usage
        candidate_index, target_command = parsed
        candidate_prompt = self._inner_brain_candidate_prompt(candidate_index)
        if candidate_prompt is None:
            return self._missing_inner_brain_candidate_message(candidate_index)
        return self._save_inner_brain_command_evaluation_sample(candidate_prompt, target_command, usage)

    def _save_inner_brain_command_evaluation_sample(
        self,
        sample_text: str,
        target_command: str,
        usage: str,
    ) -> str:
        try:
            command_text, intent = self._inner_brain_teach_target(target_command)
            save_result = save_local_evaluation_case(
                self.paths,
                InnerBrainEvaluationCase(sample_text, intent, expected_command=command_text),
            )
        except ValueError as exc:
            self.tools.run("record_log", message=f"InnerBrain 本机评估样本保存失败：{sample_text} -> {exc}")
            return f"{exc}\n{usage}"

        self.tools.run(
            "record_log",
            message=(
                "保存 InnerBrain 本机命令评估样本："
                f"intent={save_result.case.expected_intent} "
                f"created={save_result.created} "
                f"text={save_result.case.text} "
                f"command={command_text}"
            ),
        )
        return self._describe_inner_brain_evaluation_case_save(save_result)

    def _save_inner_brain_labeled_evaluation_case(self, prompt: str, command: str) -> str:
        usage = "用法：/inner-brain-eval-label 文本 => intent [slot=value ...]"
        body = prompt[len(command) :].strip()
        if "=>" not in body:
            return usage
        sample_text, raw_label = (part.strip() for part in body.split("=>", 1))
        if not sample_text or not raw_label:
            return usage
        return self._save_inner_brain_labeled_evaluation_sample(sample_text, raw_label, usage)

    def _save_inner_brain_labeled_evaluation_candidate(self, prompt: str, command: str) -> str:
        usage = "用法：/inner-brain-eval-label-candidate 编号 => intent [slot=value ...]"
        body = prompt[len(command) :].strip()
        parsed = self._parse_inner_brain_label_candidate_body(body)
        if parsed is None:
            return usage
        candidate_index, raw_label = parsed
        candidate_prompt = self._inner_brain_candidate_prompt(candidate_index)
        if candidate_prompt is None:
            return self._missing_inner_brain_candidate_message(candidate_index)
        return self._save_inner_brain_labeled_evaluation_sample(candidate_prompt, raw_label, usage)

    def _inner_brain_local_file_evaluation(self, args: list[str], failures_only: bool) -> str:
        usage = (
            "用法：/inner-brain-eval-local-file-failed 文件名"
            if failures_only
            else "用法：/inner-brain-eval-local-file 文件名"
        )
        if not args:
            return usage
        source_file = self._inner_brain_evaluation_source_file_arg(" ".join(args))
        if not source_file:
            return usage
        self.tools.run(
            "record_log",
            message=(
                "执行 InnerBrain 本机评估文件并只显示失败样本："
                if failures_only
                else "执行 InnerBrain 本机评估文件："
            )
            + source_file,
        )
        report = evaluate_inner_brain(
            self.inner_brain,
            source_filter="local_evaluation",
            source_file_filter=source_file,
        )
        if failures_only:
            return self._describe_inner_brain_local_failed_evaluation(report)
        return self._describe_inner_brain_local_evaluation(report)

    def _describe_inner_brain_local_evaluation(self, report: InnerBrainEvaluationReport) -> str:
        """本机全量评估视图追加治理入口，不改评估主体。"""

        description = describe_inner_brain_evaluation(report, failures_only=False)
        if report.total_count == 0:
            return description
        lines = [description, "后续处理："]
        if report.source_file_filter is not None:
            lines.append(f"- 查看当前文件待处理失败样本：/inner-brain-eval-local-file-failed {report.source_file_filter}")
            lines.append(f"- 查看当前文件已处理样本：/inner-brain-eval-local-resolved {report.source_file_filter}")
            lines.append("- 查看全部本机评估样本：/inner-brain-eval-local")
        else:
            lines.append("- 只看待处理失败样本：/inner-brain-eval-local-failed")
            lines.append("- 查看已处理样本：/inner-brain-eval-local-resolved")
            lines.append("- 按文件聚焦样本：/inner-brain-eval-local-file 文件名")
            source_file_counts = report.source_file_counts
            if source_file_counts:
                file_passed_counts: dict[str, int] = {}
                file_failed_counts: dict[str, int] = {}
                for case_result in report.case_results:
                    source_file = case_result.case.source_file
                    if source_file is None:
                        continue
                    if case_result.passed:
                        file_passed_counts[source_file] = file_passed_counts.get(source_file, 0) + 1
                    else:
                        file_failed_counts[source_file] = file_failed_counts.get(source_file, 0) + 1
                lines.append("可聚焦文件：")
                sorted_source_file_counts = sorted(
                    source_file_counts.items(),
                    key=lambda item: (-file_failed_counts.get(item[0], 0), -item[1], item[0]),
                )
                for source_file, count in sorted_source_file_counts:
                    passed_count = file_passed_counts.get(source_file, 0)
                    failed_count = file_failed_counts.get(source_file, 0)
                    candidate_line = (
                        f"- {source_file}：{count} 条，通过 {passed_count} 条，失败 {failed_count} 条："
                        f"/inner-brain-eval-local-file {source_file}"
                    )
                    if failed_count > 0:
                        candidate_line += f"；待处理：/inner-brain-eval-local-file-failed {source_file}"
                    lines.append(candidate_line)
        return "\n".join(lines)

    def _describe_inner_brain_local_failed_evaluation(self, report: InnerBrainEvaluationReport) -> str:
        """本机失败视图追加报告导出入口，不改评估主体。"""

        description = describe_inner_brain_evaluation(report, failures_only=True)
        if not report.failed_case_results:
            return description
        lines = [description, "后续处理："]
        if report.source_file_filter is not None:
            lines.append(f"- 查看当前文件已处理样本：/inner-brain-eval-local-resolved {report.source_file_filter}")
            lines.append("- 查看全部本机失败样本：/inner-brain-eval-local-failed")
            lines.append(f"- 导出当前文件失败报告：/inner-brain-eval-local-report {report.source_file_filter}")
            lines.append("- 导出全部本机失败报告：/inner-brain-eval-local-report")
        else:
            lines.append("- 按文件聚焦失败：/inner-brain-eval-local-file-failed 文件名")
            lines.append("- 导出本机失败报告：/inner-brain-eval-local-report")
            lines.append("- 按文件导出失败报告：/inner-brain-eval-local-report 文件名")
        return "\n".join(lines)

    def _inner_brain_local_resolved_evaluation(self, args: list[str]) -> str:
        source_file = self._inner_brain_evaluation_source_file_arg(" ".join(args)) if args else None
        self.tools.run(
            "record_log",
            message=(
                f"查看 InnerBrain 本机评估已处理样本：{source_file}"
                if source_file is not None
                else "查看 InnerBrain 本机评估已处理样本"
            ),
        )
        report = evaluate_inner_brain(
            self.inner_brain,
            source_filter="local_evaluation",
            source_file_filter=source_file,
        )
        lines = [describe_inner_brain_resolved_evaluation(report), "后续处理："]
        if report.source_file_filter is not None:
            lines.append(f"- 查看当前文件待处理失败样本：/inner-brain-eval-local-file-failed {report.source_file_filter}")
            lines.append("- 查看全部已处理样本：/inner-brain-eval-local-resolved")
            lines.append("- 查看全部待处理失败样本：/inner-brain-eval-local-failed")
        else:
            lines.append("- 查看待处理失败样本：/inner-brain-eval-local-failed")
            lines.append("- 按文件查看已处理样本：/inner-brain-eval-local-resolved 文件名")
            lines.append("- 按文件查看待处理失败样本：/inner-brain-eval-local-file-failed 文件名")
            passed_source_file_counts: dict[str, int] = {}
            failed_source_file_counts: dict[str, int] = {}
            for case_result in report.case_results:
                source_file = case_result.case.source_file
                if source_file is None:
                    continue
                if case_result.passed:
                    passed_source_file_counts[source_file] = passed_source_file_counts.get(source_file, 0) + 1
                else:
                    failed_source_file_counts[source_file] = failed_source_file_counts.get(source_file, 0) + 1
            if passed_source_file_counts:
                lines.append("可查看文件：")
                for source_file, count in sorted(
                    passed_source_file_counts.items(),
                    key=lambda item: (-failed_source_file_counts.get(item[0], 0), -item[1], item[0]),
                ):
                    failed_count = failed_source_file_counts.get(source_file, 0)
                    candidate_line = (
                        f"- {source_file}：已处理 {count} 条，待处理失败 {failed_count} 条："
                        f"/inner-brain-eval-local-resolved {source_file}"
                    )
                    if failed_count > 0:
                        candidate_line += f"；待处理：/inner-brain-eval-local-file-failed {source_file}"
                    lines.append(candidate_line)
        return "\n".join(lines)

    def _export_inner_brain_local_evaluation_report(self, args: list[str]) -> str:
        source_file = self._inner_brain_evaluation_source_file_arg(" ".join(args)) if args else None
        self.tools.run(
            "record_log",
            message=(
                f"导出 InnerBrain 本机评估失败报告：{source_file}"
                if source_file is not None
                else "导出 InnerBrain 本机评估失败报告"
            ),
        )
        report = evaluate_inner_brain(
            self.inner_brain,
            source_filter="local_evaluation",
            source_file_filter=source_file,
        )
        save_result = export_inner_brain_evaluation_report(self.paths, report)
        lines = [
            "已导出 InnerBrain 本机评估失败报告。",
            f"报告文件：{save_result.relative_path}",
            f"失败样本：{save_result.failed_count}",
        ]
        if save_result.source_file_filter is not None:
            lines.append(f"评估文件：{save_result.source_file_filter}")
        lines.append("说明：这里只导出评估报告，不写入 runtime 训练样本。")
        lines.append("后续处理：")
        if save_result.source_file_filter is not None:
            lines.append(
                f"- 复查当前文件失败样本：/inner-brain-eval-local-file-failed {save_result.source_file_filter}"
            )
            lines.append("- 查看全部本机失败样本：/inner-brain-eval-local-failed")
        else:
            lines.append("- 查看本机失败样本：/inner-brain-eval-local-failed")
            lines.append("- 按文件聚焦失败：/inner-brain-eval-local-file-failed 文件名")
        lines.append("- 补命令评估样本：/inner-brain-eval-add 文本 => /命令")
        lines.append("- 补意图评估样本：/inner-brain-eval-label 文本 => intent [slot=value ...]")
        return "\n".join(lines)

    def _inner_brain_evaluation_source_file_arg(self, value: str) -> str:
        source_file = Path(self._strip_quotes(value).strip()).name
        if not source_file:
            return ""
        if Path(source_file).suffix:
            return source_file
        return f"{source_file}.jsonl"

    def _save_inner_brain_labeled_evaluation_sample(
        self,
        sample_text: str,
        raw_label: str,
        usage: str,
    ) -> str:
        try:
            label_parts = shlex.split(raw_label, posix=True)
        except ValueError as exc:
            return f"标注参数错误：{exc}\n{usage}"
        if not label_parts:
            return usage

        intent = label_parts[0]
        try:
            slots, missing = self._inner_brain_label_slots(label_parts[1:])
            expected_command = slots.get("command") if isinstance(slots.get("command"), str) else None
            expected_policy = InnerBrainPolicy.CLARIFY if missing else InnerBrainPolicy.EXECUTE
            save_result = save_local_evaluation_case(
                self.paths,
                InnerBrainEvaluationCase(
                    sample_text,
                    intent,
                    expected_policy=expected_policy,
                    expected_command=expected_command,
                ),
            )
        except ValueError as exc:
            self.tools.run("record_log", message=f"InnerBrain 本机评估标注保存失败：{sample_text} -> {exc}")
            return f"标注参数错误：{exc}\n{usage}"

        self.tools.run(
            "record_log",
            message=(
                "保存 InnerBrain 本机标注评估样本："
                f"intent={save_result.case.expected_intent} "
                f"created={save_result.created} "
                f"text={save_result.case.text}"
            ),
        )
        return self._describe_inner_brain_evaluation_case_save(save_result)

    def _inner_brain_candidate_prompt(self, candidate_index: int) -> str | None:
        candidates = self._inner_brain_candidate_decisions()
        if candidate_index < 1 or candidate_index > len(candidates):
            return None
        return candidates[candidate_index - 1].prompt

    def _missing_inner_brain_candidate_message(self, candidate_index: int) -> str:
        return "\n".join(
            [
                f"没有第 {candidate_index} 条 InnerBrain 训练候选。",
                "请先运行 /inner-brain-candidates 查看当前候选编号。",
            ]
        )

    def _describe_inner_brain_evaluation_case_save(self, save_result: InnerBrainEvaluationSaveResult) -> str:
        title = "已保存 InnerBrain 本机评估样本。" if save_result.created else "InnerBrain 本机评估样本已存在，未重复写入。"
        lines = [
            title,
            f"样本文件：{save_result.relative_path}",
            f"用户说法：{save_result.case.text}",
            f"意图：{save_result.case.expected_intent}",
            f"期望策略：{save_result.case.expected_policy.value}",
        ]
        if save_result.case.expected_command:
            lines.append(f"目标命令：{save_result.case.expected_command}")
        lines.append("说明：这里只保存评估样本，不执行命令、不训练。")
        source_file = save_result.path.name
        lines.extend(
            [
                "后续验证：",
                "- 复跑本机评估：/inner-brain-eval-local",
                "- 只看失败样本：/inner-brain-eval-local-failed",
                f"- 聚焦样本文件：/inner-brain-eval-local-file {source_file}",
                "- 导出失败报告：/inner-brain-eval-local-report",
            ]
        )
        return "\n".join(lines)

    def _parse_inner_brain_label_candidate_body(self, body: str) -> tuple[int, str] | None:
        if "=>" not in body:
            return None
        raw_index, raw_label = (part.strip() for part in body.split("=>", 1))
        if not raw_index or not raw_label:
            return None
        try:
            candidate_index = int(raw_index)
        except ValueError:
            return None
        return candidate_index, raw_label

    def _inner_brain_label_slots(self, raw_slots: list[str]) -> tuple[dict[str, object], tuple[str, ...]]:
        slots: dict[str, object] = {}
        missing: tuple[str, ...] = ()
        for raw_slot in raw_slots:
            if "=" not in raw_slot:
                raise ValueError(f"slot 必须使用 key=value：{raw_slot}")
            key, value = (part.strip() for part in raw_slot.split("=", 1))
            if not key:
                raise ValueError(f"slot 名称不能为空：{raw_slot}")
            value = self._strip_quotes(value)
            if key == "missing":
                missing = tuple(self._split_inner_brain_label_values(value))
            else:
                slots[key] = self._inner_brain_label_value(key, value)
        return slots, missing

    def _inner_brain_label_value(self, key: str, value: str) -> object:
        if key in {"items", "tags"}:
            return self._split_inner_brain_label_values(value)
        values = self._split_inner_brain_label_values(value)
        if len(values) > 1:
            return values
        return value

    def _split_inner_brain_label_values(self, value: str) -> list[str]:
        return [item.strip() for item in re.split(r"\s*(?:,|，|、)\s*", value) if item.strip()]

    def _describe_inner_brain_labeled_sample_save(
        self,
        save_result: InnerBrainTrainingSaveResult,
        missing: tuple[str, ...],
    ) -> str:
        title = "已保存 InnerBrain 人工标注样本。" if save_result.created else "InnerBrain 人工标注样本已存在，未重复写入。"
        lines = [
            title,
            f"样本文件：{save_result.relative_path}",
            f"意图：{save_result.sample.intent}",
        ]
        slot_lines = self._inner_brain_sample_slot_lines(save_result.sample.slots)
        if slot_lines:
            lines.extend(slot_lines)
        if missing:
            lines.append(f"缺失：{'、'.join(missing)}")
        lines.append("说明：这里只保存人工标注样本，不执行命令。")
        return "\n".join(lines)

    def _teach_inner_brain_sample(self, prompt: str, command: str) -> str:
        usage = "用法：/inner-brain-teach 文本 => /命令"
        body = prompt[len(command) :].strip()
        parsed = self._parse_inner_brain_teach_body(body)
        if parsed is None:
            return usage
        sample_text, target_command = parsed
        return self._save_inner_brain_teach_command(sample_text, target_command, usage)

    def _teach_inner_brain_candidate(self, prompt: str, command: str) -> str:
        usage = "用法：/inner-brain-teach-candidate 编号 => /命令"
        body = prompt[len(command) :].strip()
        parsed = self._parse_inner_brain_teach_candidate_body(body)
        if parsed is None:
            return usage
        candidate_index, target_command = parsed
        candidates = self._inner_brain_candidate_decisions()
        if candidate_index < 1 or candidate_index > len(candidates):
            return "\n".join(
                [
                    f"没有第 {candidate_index} 条 InnerBrain 训练候选。",
                    "请先运行 /inner-brain-candidates 查看当前候选编号。",
                ]
            )
        return self._save_inner_brain_teach_command(candidates[candidate_index - 1].prompt, target_command, usage)

    def _teach_inner_brain_sample_from_natural_language(self, prompt: str) -> str | None:
        parsed = self._parse_inner_brain_teach_sentence(prompt)
        if parsed is None:
            return None
        sample_text, target_command = parsed
        usage = "你可以这样教我：以后我说“可以看看资料库吗”就是 /kb"
        return self._save_inner_brain_teach_command(sample_text, target_command, usage)

    def _parse_inner_brain_teach_body(self, body: str) -> tuple[str, str] | None:
        if "=>" not in body:
            return None
        sample_text, target_command = (part.strip() for part in body.split("=>", 1))
        sample_text = self._strip_quotes(sample_text).strip("“”")
        target_command = target_command.strip().rstrip("。")
        if not sample_text or not target_command:
            return None
        return sample_text, target_command

    def _parse_inner_brain_teach_candidate_body(self, body: str) -> tuple[int, str] | None:
        if "=>" not in body:
            return None
        raw_index, target_command = (part.strip() for part in body.split("=>", 1))
        target_command = target_command.strip().rstrip("。")
        if not raw_index or not target_command:
            return None
        try:
            candidate_index = int(raw_index)
        except ValueError:
            return None
        return candidate_index, target_command

    def _parse_inner_brain_teach_sentence(self, prompt: str) -> tuple[str, str] | None:
        patterns = (
            r"^以后我说\s*[“\"'](?P<text>.+?)[”\"']\s*(?:就是|等于|对应)\s*(?P<command>/\S.*)$",
            r"^以后我说\s*(?P<text>.+?)\s*(?:就是|等于|对应)\s*(?P<command>/\S.*)$",
            r"^把\s*[“\"'](?P<text>.+?)[”\"']\s*(?:记成|教成|设为)\s*(?P<command>/\S.*)$",
            r"^把\s*(?P<text>.+?)\s*(?:记成|教成|设为)\s*(?P<command>/\S.*)$",
        )
        normalized_prompt = prompt.strip().rstrip("。")
        for pattern in patterns:
            match = re.fullmatch(pattern, normalized_prompt)
            if not match:
                continue
            sample_text = match.group("text").strip()
            target_command = match.group("command").strip()
            if sample_text and target_command:
                return sample_text, target_command
        return None

    def _save_inner_brain_teach_command(self, sample_text: str, target_command: str, usage: str) -> str:
        try:
            command_text, intent = self._inner_brain_teach_target(target_command)
            save_result = save_labeled_runtime_training_sample(
                self.paths,
                sample_text,
                intent,
                {"command": command_text},
            )
        except ValueError as exc:
            self.tools.run("record_log", message=f"InnerBrain 教学样本保存失败：{sample_text} -> {exc}")
            return f"{exc}\n{usage}"

        self.inner_brain = InnerBrain(self.paths)
        self._forget_inner_brain_candidate(save_result.sample.text)
        self.tools.run(
            "record_log",
            message=(
                "保存 InnerBrain 教学样本："
                f"intent={save_result.sample.intent} "
                f"created={save_result.created} "
                f"text={save_result.sample.text} "
                f"command={command_text}"
            ),
        )
        return self._describe_inner_brain_teach_sample_save(save_result, command_text)

    def _inner_brain_teach_target(self, target_command: str) -> tuple[str, str]:
        command_text = target_command.strip().rstrip("。")
        if not command_text.startswith("/"):
            raise ValueError("教学目标必须是 / 开头的已知命令")
        try:
            parts = shlex.split(command_text, posix=False)
        except ValueError as exc:
            raise ValueError(f"教学目标命令解析失败：{exc}") from exc
        if not parts:
            raise ValueError("教学目标不能为空")
        command_name = parts[0]
        intent = TEACHABLE_INNER_BRAIN_COMMAND_INTENTS.get(command_name)
        if intent is None:
            raise ValueError(f"教学目标不是已知命令：{command_name}")
        return command_text, intent

    def _describe_inner_brain_teach_sample_save(
        self,
        save_result: InnerBrainTrainingSaveResult,
        target_command: str,
    ) -> str:
        title = "已保存 InnerBrain 教学样本。" if save_result.created else "InnerBrain 教学样本已存在，未重复写入。"
        return "\n".join(
            [
                title,
                f"样本文件：{save_result.relative_path}",
                f"用户说法：{save_result.sample.text}",
                f"目标命令：{target_command}",
                f"意图：{save_result.sample.intent}",
                "说明：这里只保存教学样本，不执行命令。",
            ]
        )

    def _describe_inner_brain_sample_save(
        self,
        save_result: InnerBrainTrainingSaveResult,
        result: InnerBrainResult,
    ) -> str:
        title = "已保存 InnerBrain runtime 样本。" if save_result.created else "InnerBrain runtime 样本已存在，未重复写入。"
        lines = [
            title,
            f"样本文件：{save_result.relative_path}",
            f"意图：{save_result.sample.intent}",
            f"策略：{result.policy.value}",
        ]
        if save_result.duplicate:
            lines.append("说明：样本已存在，未重复写入。")
        slot_lines = self._inner_brain_sample_slot_lines(save_result.sample.slots)
        if slot_lines:
            lines.extend(slot_lines)
        lines.append("说明：这里只保存识别样本，不执行命令。")
        return "\n".join(lines)

    def _inner_brain_sample_slot_lines(self, slots: dict[str, object]) -> list[str]:
        lines: list[str] = []
        for key, value in slots.items():
            if isinstance(value, list | tuple):
                value_text = "、".join(str(item) for item in value if str(item).strip())
            else:
                value_text = str(value).strip()
            if value_text:
                lines.append(f"槽位 {key}：{value_text}")
        return lines

    def _inner_brain_clarification(self, result: InnerBrainResult) -> str:
        self._pending_inner_brain_clarification = result
        missing = (
            "、".join(self._inner_brain_missing_label(item, result.intent) for item in result.missing)
            or "更多信息"
        )
        self.tools.run(
            "record_log",
            message=(
                "InnerBrain 需要澄清："
                f"intent={result.intent} "
                f"missing={','.join(result.missing) or 'unknown'} "
                f"confidence={result.confidence:.2f}"
            ),
        )
        lines = [
            "我理解到这个请求可能需要本地执行，但信息还不够。",
            f"- 意图：{result.intent}",
            f"- 需要补充：{missing}",
            "- 你也可以直接回复缺失信息，我会接着这次请求继续处理。",
        ]
        action_hint = self._inner_brain_clarification_action_hint(result)
        if action_hint:
            lines.append(f"- 可直接补充：{action_hint}")
        label_hint = self._inner_brain_clarification_label_hint(result)
        if label_hint:
            lines.append(f"- 如果这次理解错了：{label_hint}")
        lines.append("- 想固定一种说法：/inner-brain-teach 原话 => /命令")
        return "\n".join(lines)

    def _handle_pending_inner_brain_clarification(self, prompt: str) -> str | None:
        pending = self._pending_inner_brain_clarification
        if pending is None:
            return None
        if self._is_inner_brain_clarification_cancel(prompt):
            self._pending_inner_brain_clarification = None
            self.tools.run("record_log", message=f"取消 InnerBrain 澄清补槽：intent={pending.intent}")
            return f"已取消这次补充：{pending.intent}。"

        completed = complete_inner_brain_clarification(pending, prompt)
        if completed.policy == InnerBrainPolicy.EXECUTE and completed.natural_language_intent is not None:
            self._pending_inner_brain_clarification = None
            self.tools.run(
                "record_log",
                message=(
                    "InnerBrain 澄清补槽完成："
                    f"intent={completed.intent} "
                    f"source={completed.source}"
                ),
            )
            response = self._handle_natural_language_intent(completed.natural_language_intent)
            self._remember_route_decision(
                "inner-brain",
                completed.intent,
                prompt,
                "本地内脑澄清补槽完成",
                self._inner_brain_route_explanation(completed),
            )
            return "\n".join(["已补齐缺失信息，继续执行。", response])

        return self._inner_brain_clarification(completed)

    def _is_inner_brain_clarification_cancel(self, prompt: str) -> bool:
        return prompt.strip() in {"取消", "取消补充", "不用了", "先不用", "算了"}

    def _inner_brain_clarification_action_hint(self, result: InnerBrainResult) -> str:
        if result.intent == "knowledge.import" and "source" in result.missing:
            return "/import 源文件或目录路径 [目标文件名]"
        if result.intent == "document.read_path" and "path" in result.missing:
            return "请直接回复文件路径，例如“note.txt”"
        if result.intent == "desktop.delete_shortcut" and "items" in result.missing:
            return "/inner-brain-label 原话 => desktop.delete_shortcut items=快捷方式名称"
        if result.intent == "web.search" and "query" in result.missing:
            return "/search 关键词"
        if result.intent == "web.search_summarize" and "query" in result.missing:
            return "/search-summary 关键词"
        if result.intent in {"directory.open_alias", "directory.organize_alias"} and "alias" in result.missing:
            return "请直接回复目录别名，例如“项目”"
        if result.intent == "experience.record" and "experience" in result.missing:
            return "请直接回复经验内容，例如“导入资料后先打标签”"
        if result.intent in {"experience.search", "experience.advice"} and "query" in result.missing:
            return "请直接回复经验关键词，例如“导入资料”"
        if result.intent == "tag_group.preview_tagging" and {"alias", "tags"}.issubset(set(result.missing)):
            return "请直接回复标签组和新标签，例如“项目 归档”"
        if {"result_index", "tags"}.issubset(set(result.missing)):
            return "请直接回复编号和标签，例如“第二份 项目 Python”"
        if "tags" in result.missing:
            return "请直接回复标签，例如“项目 Python”"
        if "result_index" in result.missing:
            if result.intent == "document.read_numbered_recent":
                return "请补充编号，例如“第二份”"
            if result.intent == "web_search.open_numbered":
                return "请补充编号，例如“第一条”"
            if result.intent in {"advice.read_numbered", "advice.execute_numbered"}:
                return "请补充编号，例如“第一条建议”"
            return "请补充编号，例如“查看第一条结果”"
        return ""

    def _inner_brain_clarification_label_hint(self, result: InnerBrainResult) -> str:
        if result.intent == "knowledge.import" and "source" in result.missing:
            return "/inner-brain-label 原话 => knowledge.import source=文件或目录路径"
        if result.intent == "document.read_path" and "path" in result.missing:
            return "/inner-brain-label 原话 => document.read_path path=文件路径"
        if result.intent == "desktop.delete_shortcut" and "items" in result.missing:
            return "/inner-brain-label 原话 => desktop.delete_shortcut items=快捷方式名称"
        if result.intent in {"web.search", "web.search_summarize"} and "query" in result.missing:
            return f"/inner-brain-label 原话 => {result.intent} query=关键词"
        if result.intent in {"directory.open_alias", "directory.organize_alias"} and "alias" in result.missing:
            return f"/inner-brain-label 原话 => {result.intent} alias=目录别名"
        if result.intent == "experience.record" and "experience" in result.missing:
            return "/inner-brain-label 原话 => experience.record experience=经验内容"
        if result.intent in {"experience.search", "experience.advice"} and "query" in result.missing:
            return f"/inner-brain-label 原话 => {result.intent} query=经验关键词"
        if result.intent == "tag_group.preview_tagging" and {"alias", "tags"}.issubset(set(result.missing)):
            return "/inner-brain-label 原话 => tag_group.preview_tagging alias=标签组 tags=新标签"
        if result.intent != "unknown":
            return f"/inner-brain-label 原话 => {result.intent} slot=value"
        return ""

    def _inner_brain_missing_label(self, missing: str, intent: str = "") -> str:
        if intent == "document.read_path" and missing == "path":
            return "文件路径"
        if intent in {"experience.search", "experience.advice"} and missing == "query":
            return "经验关键词"
        if intent == "tag_group.preview_tagging" and missing == "alias":
            return "标签组"
        labels = {
            "source": "要导入的文件或目录",
            "items": "要处理的对象名称",
            "path": "路径",
            "tag": "标签",
            "tags": "标签",
            "result_index": "编号",
            "query": "查询关键词",
            "alias": "目录别名",
            "experience": "经验内容",
        }
        return labels.get(missing, missing)

    def _capability_summary(self) -> str:
        lines = [
            "我现在可以做这些事：",
            "- 记忆：记住你的姓名、身份和偏好，也能回答“我是谁”。",
            "- 经验：记录和查看可复用流程经验。",
            "- 知识库：导入 Markdown、txt、PDF、JSON 聊天记录，并基于资料回答。",
            "- 工作台：登记常用目录、查看目录、生成日报、做文件整理预览。",
            "- 桌面：通过小助手面板和托盘触发常用能力，也能删除明确点名的桌面 .lnk 快捷方式。",
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
        has_web_search = self._recent_web_search is not None and bool(self._recent_web_search.results)
        has_advice_suggestions = bool(self._recent_advice_suggestions)
        has_pending_advice_command = self._pending_advice_command is not None
        has_pending_tagged_documents_tagging = bool(self._pending_tagged_documents_paths)
        has_recent_tagged_documents_operation = self._recent_tagged_documents_operation_tag is not None
        has_pending_llm_clarification = self._pending_llm_clarification is not None
        has_route_history = bool(self._recent_route_decisions)
        if (
            not has_document
            and not has_document_list
            and not has_directory
            and not has_recent_files
            and not has_search_results
            and not has_web_search
            and not has_advice_suggestions
            and not has_pending_advice_command
            and not has_pending_tagged_documents_tagging
            and not has_recent_tagged_documents_operation
            and not has_pending_llm_clarification
            and not has_route_history
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

        if has_web_search and self._recent_web_search is not None:
            lines.append(f"- 最近联网搜索：{self._recent_web_search.query}")
            for index, result in enumerate(self._recent_web_search.results, start=1):
                lines.append(f"  {index}. {result.title}")
                lines.append(f"     URL：{result.url}")
                if result.snippet:
                    lines.append(f"     摘要：{result.snippet}")
        else:
            lines.append("- 最近联网搜索：无")

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
        if has_route_history:
            latest_route = self._recent_route_decisions[0]
            lines.append(f"- 最近路由：{latest_route.route} / {latest_route.detail}")
            for index, route_decision in enumerate(self._recent_route_decisions, start=1):
                lines.append(f"  {self._route_history_line(index, route_decision)}")
        else:
            lines.append("- 最近路由：无")
        if self._pending_llm_clarification is not None:
            lines.append(f"- 待补充外脑问题：{self._pending_llm_clarification.clarification}")
            lines.append(f"  外脑原始问题：{self._pending_llm_clarification.original_prompt}")
            lines.append(
                f"  澄清轮次：{self._pending_llm_clarification.clarification_count}/"
                f"{LLM_CLARIFICATION_MAX_ROUNDS}"
            )
            lines.append("  过期策略：超过 12 小时未补充会在下次启动时清理。")
            lines.append("  可回复缺失信息继续，或回复“取消补充”。")
        else:
            lines.append("- 待补充外脑问题：无")
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

    def _route_history_status(self) -> str:
        self.tools.run("record_log", message="查看最近路由历史详情")
        if not self._recent_route_decisions:
            return "\n".join(
                [
                    "路由历史：还没有记录。",
                    "- 先输入一个问题或命令，再用 /route-history 查看它由哪一层处理。",
                ]
            )

        lines = ["路由历史："]
        for index, decision in enumerate(self._recent_route_decisions, start=1):
            lines.extend(self._route_history_detail_lines(index, decision))
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

    def _tagged_documents_history_status(self) -> str:
        self.tools.run("record_log", message="查看批量标签历史")
        if not self._recent_tagged_documents_operations:
            return "\n".join(
                [
                    "批量打标签历史：还没有记录。",
                    "- 你可以先说“给项目标签资料都打标签 归档”，再说“确认执行”。",
                ]
            )

        lines = ["批量打标签历史："]
        for index, operation in enumerate(self._recent_tagged_documents_operations, start=1):
            appended_tags = "、".join(operation.tags)
            lines.append(
                f"{index}. {operation.tag}标签资料 -> "
                f"追加标签：{appended_tags}，已更新 {operation.updated_count} 份"
            )
            if operation.restore_commands:
                lines.append(f"   恢复提示：{'；'.join(operation.restore_commands)}")
            if operation.document_paths:
                lines.append(f"   影响资料：{len(operation.document_paths)} 份；可说“读取第{index}条标签历史资料”。")
        return "\n".join(lines)

    def _sentence(self, text: str) -> str:
        return text if text.endswith(("。", "！", "？", ".", "!", "?")) else f"{text}。"

    def _greeting(self, greeting: str) -> str:
        user_name = self._user_name_from_profile()
        salutation = self._salutation(greeting)
        addressed_salutation = f"{salutation}，{user_name}" if user_name else salutation
        self.tools.run("record_log", message=f"自然语言问候：{greeting}")
        return f"{addressed_salutation}。我是 Jarvis Lite，可以继续帮你处理知识库、最近上下文、桌面目录和本地任务。"

    def _assistant_identity(self) -> str:
        self.tools.run("record_log", message="回答助手身份")
        return "我叫 Jarvis Lite，是你的本地 PC 助手。当前优先处理记忆、知识库、最近上下文、桌面文件和本地任务。"

    def _salutation(self, greeting: str) -> str:
        normalized = greeting.strip().lower()
        if normalized in {"早", "早安", "早上好", "上午好"}:
            return "早上好"
        if normalized == "中午好":
            return "中午好"
        if normalized == "下午好":
            return "下午好"
        if normalized == "晚上好":
            return "晚上好"
        return "你好"

    def _user_name_from_profile(self) -> str:
        for raw_line in read_profile(self.paths).splitlines():
            line = raw_line.strip()
            if line.startswith("- 用户姓名："):
                return line.removeprefix("- 用户姓名：").strip()
        return ""

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

    def _search_web(self, query: str) -> str:
        normalized_query = self._strip_quotes(query)
        if not normalized_query:
            return "用法：/search 关键词"
        response = self.search_router.search(normalized_query)
        self.tools.run("record_log", message=f"联网搜索：{normalized_query}")
        if response.error:
            return "\n".join(
                [
                    response.error,
                    "可先运行：/search-status",
                    "启用入口：/search-enable",
                ]
            )
        if response.results:
            self._remember_recent_web_search(response.query, response.results)
        return self._format_search_web_response(response, include_summary_hint=True)

    def _search_smoke(self, query: str) -> str:
        smoke_query = self._strip_quotes(query.strip()) or "Python 版本"
        if not self._search_router_injected:
            self.search_router = build_search_router(paths=self.paths)

        response = self.search_router.search(smoke_query)
        if response.error:
            self.tools.run("record_log", message=f"联网搜索 smoke 失败：query={smoke_query} error={response.error}")
            return "\n".join(
                [
                    f"联网搜索 smoke：{response.query}",
                    "说明：这是一次 provider 连通性测试，可能发起真实网络调用。",
                    "调用结果：失败",
                    f"错误：{response.error}",
                    "可先运行：/search-config-check",
                    "启用入口：/search-enable",
                ]
            )

        self.tools.run("record_log", message=f"联网搜索 smoke 成功：query={response.query} results={len(response.results)}")
        lines = [
            f"联网搜索 smoke：{response.query}",
            "说明：这是一次 provider 连通性测试，可能发起真实网络调用。",
            f"调用结果：成功，返回 {len(response.results)} 条来源。",
        ]
        if response.results:
            for index, result in enumerate(response.results, start=1):
                lines.append(f"{index}. {result.title}")
                lines.append(f"   URL：{result.url}")
                if result.snippet:
                    lines.append(f"   摘要：{result.snippet}")
                if result.source:
                    lines.append(f"   来源：{result.source}")
        else:
            lines.append("说明：provider 已响应但没有返回来源。")
        lines.extend(
            [
                "说明：smoke 不会写入最近联网搜索上下文。",
                "下一步：/search 关键词",
            ]
        )
        return "\n".join(lines)

    def _search_web_and_summarize(self, query: str) -> str:
        normalized_query = self._strip_quotes(query)
        if not normalized_query:
            return "用法：/search-summary 关键词"
        response = self.search_router.search(normalized_query)
        self.tools.run("record_log", message=f"联网搜索并总结：{normalized_query}")
        if response.error:
            return "\n".join(
                [
                    response.error,
                    "可先运行：/search-status",
                    "启用入口：/search-enable",
                ]
            )
        if response.results:
            self._remember_recent_web_search(response.query, response.results)
        lines = self._format_search_web_response(response, include_summary_hint=False).splitlines()
        if not response.results:
            return "\n".join(lines)

        intent = self.llm_router.complete_intent(
            f"请基于联网搜索结果总结：{response.query}",
            self._llm_context_lines(),
        )
        if intent is None:
            lines.append("LLM 外脑未返回总结：LLM 外脑未启用或未返回结果")
            lines.append("可先运行：/llm-status 或 /llm-enable")
            return "\n".join(lines)
        self._record_llm_usage(intent)
        self._remember_recent_llm_call("search-summary", f"请基于联网搜索结果总结：{response.query}", intent)
        if intent.type == "answer" and intent.answer:
            lines.append(f"LLM 外脑总结：{intent.answer}")
        elif intent.type == "clarify" and intent.clarification:
            lines.append(f"LLM 外脑需要补充信息：{intent.clarification}")
        elif intent.type == "command" and intent.command:
            lines.append(f"LLM 外脑返回了命令建议，本次搜索总结不会执行命令：{intent.command}")
        else:
            reason = intent.reason or "LLM 外脑未返回可用总结"
            lines.append(f"LLM 外脑未返回总结：{reason}")
            lines.append("可先运行：/llm-status 或 /llm-enable")
        return "\n".join(lines)

    def _format_search_web_response(self, response, include_summary_hint: bool) -> str:
        lines = [f"联网搜索：{response.query}"]
        if not response.results:
            lines.append("- 没有返回搜索结果。")
            return "\n".join(lines)
        for index, result in enumerate(response.results, start=1):
            lines.append(f"{index}. {result.title}")
            lines.append(f"   URL：{result.url}")
            if result.snippet:
                lines.append(f"   摘要：{result.snippet}")
            if result.source:
                lines.append(f"   来源：{result.source}")
        if include_summary_hint:
            lines.append("说明：搜索结果来自 provider 返回的网页来源；需要总结时可使用 /search-summary 关键词。")
        return "\n".join(lines)

    def _open_recent_web_search_source(self, raw_index: str) -> str:
        result_index = self._parse_command_index(raw_index)
        if result_index <= 0:
            return "用法：/search-open 编号"
        result, error = self._recent_web_search_result(result_index)
        if error:
            return error
        assert result is not None
        self.tools.run("record_log", message=f"查看联网搜索来源：index={result_index} url={result.url}")
        lines = [
            f"联网搜索来源 {result_index}：{result.title}",
            f"URL：{result.url}",
        ]
        if result.snippet:
            lines.append(f"摘要：{result.snippet}")
        if result.source:
            lines.append(f"来源：{result.source}")
        lines.append("说明：当前不会启动浏览器；请复制 URL 到浏览器打开。")
        return "\n".join(lines)

    def _compare_recent_web_search_sources(self) -> str:
        if self._recent_web_search is None or not self._recent_web_search.results:
            return self._missing_recent_web_search_message()
        lines = self._recent_web_search_source_lines("联网搜索来源比较：")
        intent = self.llm_router.complete_intent(
            f"请比较最近联网搜索来源：{self._recent_web_search.query}",
            self._llm_context_lines(),
        )
        if intent is None:
            lines.append("LLM 外脑未返回比较：LLM 外脑未启用或未返回结果")
            lines.append("可先运行：/llm-status 或 /llm-enable")
            return "\n".join(lines)
        self._record_llm_usage(intent)
        self._remember_recent_llm_call("search-compare", f"请比较最近联网搜索来源：{self._recent_web_search.query}", intent)
        if intent.type == "answer" and intent.answer:
            lines.append(f"LLM 外脑比较：{intent.answer}")
        elif intent.type == "clarify" and intent.clarification:
            lines.append(f"LLM 外脑需要补充信息：{intent.clarification}")
        elif intent.type == "command" and intent.command:
            lines.append(f"LLM 外脑返回了命令建议，本次来源比较不会执行命令：{intent.command}")
        else:
            reason = intent.reason or "LLM 外脑未返回可用比较"
            lines.append(f"LLM 外脑未返回比较：{reason}")
            lines.append("可先运行：/llm-status 或 /llm-enable")
        return "\n".join(lines)

    def _save_recent_web_search_summary(self, filename: str = "") -> str:
        if self._recent_web_search is None or not self._recent_web_search.results:
            return self._missing_recent_web_search_message()
        markdown = self._recent_web_search_summary_markdown("保存最近联网搜索摘要")
        target_name = self._web_search_summary_filename(filename)
        result = self.tools.run("write_summary", filename=target_name, content=markdown)
        self.tools.run("record_log", message=f"保存联网搜索摘要：{target_name}")
        if not result.success:
            return result.message
        relative_path = result.message.removeprefix("已写入总结：").replace("\\", "/")
        return f"已保存联网搜索摘要：{relative_path}"

    def _import_recent_web_search_summary(self, filename: str = "") -> str:
        if self._recent_web_search is None or not self._recent_web_search.results:
            return self._missing_recent_web_search_message()
        markdown = self._recent_web_search_summary_markdown("导入最近联网搜索摘要到知识库")
        target_name = self._web_search_summary_filename(filename)
        target = self.paths.data_dir / target_name
        if target.exists():
            return f"导入失败：目标文件已存在：data/{target_name}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(markdown, encoding="utf-8")
        relative_path = target.relative_to(self.paths.data_dir).as_posix()
        self._remember_recent_document(relative_path)
        self.tools.run("record_log", message=f"导入联网搜索摘要：data/{relative_path}")
        return f"已导入联网搜索摘要：data/{relative_path}"

    def _recent_web_search_summary_markdown(self, task: str) -> str:
        assert self._recent_web_search is not None
        answer = ""
        intent = self.llm_router.complete_intent(
            f"{task}：{self._recent_web_search.query}",
            self._llm_context_lines(),
        )
        if intent is not None:
            self._record_llm_usage(intent)
            self._remember_recent_llm_call("search-summary-file", f"{task}：{self._recent_web_search.query}", intent)
            if intent.type == "answer" and intent.answer:
                answer = intent.answer.strip()
            elif intent.type == "clarify" and intent.clarification:
                answer = f"LLM 外脑需要补充信息：{intent.clarification}"
            elif intent.type == "command" and intent.command:
                answer = f"LLM 外脑返回命令建议，本次未执行：{intent.command}"
            elif intent.reason:
                answer = f"LLM 外脑未返回摘要：{intent.reason}"
        if not answer:
            answer = "LLM 外脑未启用或未返回摘要；以下保留联网搜索来源。"

        lines = [
            f"# 联网搜索摘要：{self._recent_web_search.query}",
            "",
            f"生成时间：{datetime.now().isoformat(timespec='seconds')}",
            f"查询：{self._recent_web_search.query}",
            "",
            "## LLM 外脑摘要",
            "",
            answer,
            "",
            "## 联网来源",
            "",
        ]
        for index, result in enumerate(self._recent_web_search.results, start=1):
            lines.append(f"{index}. {result.title}")
            lines.append(f"   - URL：{result.url}")
            if result.snippet:
                lines.append(f"   - 摘要：{result.snippet}")
            if result.source:
                lines.append(f"   - 来源：{result.source}")
        lines.append("")
        return "\n".join(lines)

    def _recent_web_search_source_lines(self, title: str) -> list[str]:
        assert self._recent_web_search is not None
        lines = [title, f"查询：{self._recent_web_search.query}"]
        for index, result in enumerate(self._recent_web_search.results, start=1):
            lines.append(f"{index}. {result.title}")
            lines.append(f"   URL：{result.url}")
            if result.snippet:
                lines.append(f"   摘要：{result.snippet}")
        return lines

    def _recent_web_search_result(self, result_index: int) -> tuple[RuntimeWebSearchResultContext | None, str | None]:
        if self._recent_web_search is None or not self._recent_web_search.results:
            return None, self._missing_recent_web_search_message()
        if result_index < 1 or result_index > len(self._recent_web_search.results):
            return None, f"最近联网搜索结果只有 {len(self._recent_web_search.results)} 条，不能选择第 {result_index} 条。"
        return self._recent_web_search.results[result_index - 1], None

    def _missing_recent_web_search_message(self) -> str:
        return "还没有最近联网搜索。你可以先运行 /search 关键词，或说“联网查一下 Python 版本”。"

    def _web_search_summary_filename(self, filename: str) -> str:
        raw_name = self._strip_quotes(filename.strip())
        if not raw_name:
            assert self._recent_web_search is not None
            raw_name = f"web-search-{self._recent_web_search.query}"
        name = Path(raw_name).name.strip()
        path_name = Path(name)
        stem = path_name.stem if path_name.suffix else name
        suffix = path_name.suffix if path_name.suffix else ".md"
        safe_stem = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._-]+", "-", stem.strip().lower()).strip("-._")
        if not safe_stem:
            safe_stem = "web-search-summary"
        return f"{safe_stem}{suffix if suffix.lower() == '.md' else '.md'}"

    def _parse_command_index(self, value: str) -> int:
        normalized = self._strip_quotes(value)
        if not normalized.isdigit():
            return 0
        return int(normalized)

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

    def _answer_from_llm(self, prompt: str) -> str:
        context = self._llm_context_lines()
        intent = self.llm_router.complete_intent(prompt, context)
        if intent is None:
            return ""
        self._record_llm_usage(intent)
        self._remember_recent_llm_call("fallback", prompt, intent)
        return self._handle_llm_intent(intent, prompt, context)

    def _llm_smoke(self, prompt: str) -> str:
        smoke_prompt = prompt.strip() or "请用一句话确认 Jarvis Lite LLM smoke 可用。"
        if not self._llm_router_injected:
            self.llm_router = build_llm_router(paths=self.paths)
        if not self.llm_router.settings.enabled or self.llm_router.provider is None:
            return "\n".join(
                [
                    "LLM smoke：LLM 外脑未启用。",
                    "可先运行：/llm-status",
                    "配置模板：/llm-config-example openai-compatible",
                ]
            )

        issues = self.llm_router.settings.configuration_issues()
        if issues:
            lines = ["LLM smoke：配置未完成。", *[f"- {issue}" for issue in issues]]
            lines.extend(["可先运行：/llm-status", "配置模板：/llm-config-example openai-compatible"])
            return "\n".join(lines)

        intent = self.llm_router.complete_intent(
            smoke_prompt,
            ("LLM smoke 配置验证：只返回结构化意图，不要声称执行工具。",),
        )
        if intent is None:
            return "LLM smoke：LLM 外脑未返回结果。"
        self._record_llm_usage(intent)
        self._remember_recent_llm_call("smoke", smoke_prompt, intent)
        return self._format_llm_smoke_intent(intent)

    def _format_llm_smoke_intent(self, intent: LLMIntent) -> str:
        lines = [f"LLM smoke：type={intent.type}"]
        if intent.type == "command" and intent.command:
            lines.append(f"命令建议：{intent.command.strip()}")
            lines.append("说明：smoke 不会自动执行命令建议。")
        elif intent.type == "answer" and intent.answer:
            lines.append(f"回答：{intent.answer}")
        elif intent.type == "clarify" and intent.clarification:
            lines.append(f"澄清问题：{intent.clarification}")
        elif intent.reason:
            lines.append(f"原因：{intent.reason}")
        if intent.reason and intent.type != "no_action":
            lines.append(f"原因：{intent.reason}")
        return "\n".join(lines)

    def _llm_context_preview(self) -> str:
        lines = ["LLM context preview（不会调用 provider）："]
        for context_line in self._llm_context_lines():
            lines.append(f"- {context_line}")
        return "\n".join(lines)

    def _llm_enable_guidance(self) -> str:
        example_path = write_llm_example_config(self.paths)
        local_path = llm_local_config_path(self.paths)
        if not self._llm_router_injected:
            self.llm_router = build_llm_router(paths=self.paths)
        self.tools.run("record_log", message="查看 LLM 外脑启用入口")

        lines = [
            "外脑启用入口：",
            self.llm_router.describe(),
            f"配置文件：{self._project_path(local_path)}",
            f"模板文件：{self._project_path(example_path)}",
        ]
        if not local_path.exists():
            lines.append("下一步：复制模板为 config/llm.local.json，填入 provider、model、base_url、api_key 后重启 Jarvis Lite。")
        else:
            lines.append("下一步：修改 config/llm.local.json 后再次执行 /llm-enable，即可重新加载当前会话。")
        lines.extend(
            [
                "状态检查：/llm-status",
                "连通性测试：/llm-smoke 请用一句话确认连接可用",
            ]
        )
        return "\n".join(lines)

    def _llm_config_init(self, provider: str) -> str:
        try:
            local_path, created, normalized_provider = write_llm_local_config_draft(self.paths, provider)
        except ValueError as exc:
            return str(exc)
        if not self._llm_router_injected:
            self.llm_router = build_llm_router(paths=self.paths)
        self.tools.run("record_log", message=f"生成 LLM 本地配置草稿：provider={normalized_provider} created={created}")

        if created:
            lines = [
                f"已生成外脑本地配置草稿：{self._project_path(local_path)}",
                f"Provider：{normalized_provider}",
            ]
            adapter_provider = LLMSettings(provider=normalized_provider).adapter_provider
            if adapter_provider != normalized_provider:
                lines.append(f"Adapter：{adapter_provider}")
            lines.append("下一步：填入 model、base_url、api_key 后执行 /llm-enable。")
        else:
            lines = [
                f"外脑本地配置已存在：{self._project_path(local_path)}",
                "未覆盖已有配置，也不会显示已有 API key。",
                "下一步：编辑该文件后执行 /llm-enable。",
            ]
        lines.extend(
            [
                "状态检查：/llm-status",
                "连通性测试：/llm-smoke 请用一句话确认连接可用",
            ]
        )
        return "\n".join(lines)

    def _llm_config_check(self) -> str:
        local_path = llm_local_config_path(self.paths)
        router = build_llm_router(paths=self.paths)
        issues = router.settings.configuration_issues()
        self.tools.run("record_log", message=f"检查 LLM 本地配置：exists={local_path.exists()} issues={len(issues)}")

        lines = [
            "外脑配置检查：",
            f"配置文件：{self._project_path(local_path)}",
            f"本地配置：{'存在' if local_path.exists() else '未创建'}",
            router.describe(),
            "检查方式：只读取本地配置和环境变量，不发起网络请求。",
        ]
        if issues:
            lines.append("结果：配置未完成，修正后执行 /llm-enable。")
        elif not router.settings.enabled:
            lines.append("结果：LLM 外脑未启用，可先执行 /llm-config-init。")
        else:
            lines.append("结果：配置完整，可执行 /llm-enable 或 /llm-smoke。")
        return "\n".join(lines)

    def _llm_config_set(self, args: list[str]) -> str:
        if not args:
            self.tools.run("record_log", message="查看 LLM 本地配置写入用法")
            return self._llm_config_set_usage()
        try:
            updates = self._parse_config_set_updates(args)
            local_path, changed_fields = write_llm_local_config_values(self.paths, updates)
        except ValueError as exc:
            return f"外脑配置写入失败：{exc}\n{self._llm_config_set_usage()}"

        if not self._llm_router_injected:
            self.llm_router = build_llm_router(paths=self.paths)
        self.tools.run("record_log", message=f"写入 LLM 本地配置：fields={','.join(changed_fields)}")
        return "\n".join(
            [
                f"已写入外脑本地配置：{self._project_path(local_path)}",
                f"变更字段：{'、'.join(changed_fields)}",
                "说明：响应和日志不会显示真实 API key。",
                "下一步：/llm-config-check",
                "启用：/llm-enable",
                "连通性测试：/llm-smoke 请用一句话确认连接可用",
            ]
        )

    def _llm_config_set_usage(self) -> str:
        return "\n".join(
            [
                "用法：/llm-config-set key=value ...",
                "示例：/llm-config-set provider=qwen model=qwen-plus base_url=https://example.com/v1/responses api_key=你的key",
                "支持字段：provider、model、base_url、api_key、fake_response",
                "说明：不会回显 api_key；写入后执行 /llm-config-check。",
            ]
        )

    def _search_enable_guidance(self) -> str:
        example_path = write_search_example_config(self.paths)
        local_path = search_local_config_path(self.paths)
        if not self._search_router_injected:
            self.search_router = build_search_router(paths=self.paths)
        self.tools.run("record_log", message="查看联网搜索启用入口")

        lines = [
            "联网搜索启用入口：",
            self.search_router.describe(),
            f"配置文件：{self._project_path(local_path)}",
            f"模板文件：{self._project_path(example_path)}",
        ]
        if not local_path.exists():
            lines.append("下一步：复制模板为 config/search.local.json，填入 provider、api_key 后重启 Jarvis Lite。")
        else:
            lines.append("下一步：修改 config/search.local.json 后再次执行 /search-enable，即可重新加载当前会话。")
        lines.extend(
            [
                "状态检查：/search-status",
                "搜索测试：/search Python 版本",
            ]
        )
        return "\n".join(lines)

    def _search_config_init(self, provider: str) -> str:
        try:
            local_path, created, normalized_provider = write_search_local_config_draft(self.paths, provider)
        except ValueError as exc:
            return str(exc)
        if not self._search_router_injected:
            self.search_router = build_search_router(paths=self.paths)
        self.tools.run("record_log", message=f"生成联网搜索本地配置草稿：provider={normalized_provider} created={created}")

        if created:
            lines = [
                f"已生成联网搜索本地配置草稿：{self._project_path(local_path)}",
                f"Provider：{normalized_provider}",
                "下一步：填入 api_key 后执行 /search-enable。",
            ]
        else:
            lines = [
                f"联网搜索本地配置已存在：{self._project_path(local_path)}",
                "未覆盖已有配置，也不会显示已有 API key。",
                "下一步：编辑该文件后执行 /search-enable。",
            ]
        lines.extend(
            [
                "状态检查：/search-status",
                "搜索测试：/search Python 版本",
            ]
        )
        return "\n".join(lines)

    def _search_config_check(self) -> str:
        local_path = search_local_config_path(self.paths)
        router = build_search_router(paths=self.paths)
        issues = router.settings.configuration_issues()
        self.tools.run("record_log", message=f"检查联网搜索本地配置：exists={local_path.exists()} issues={len(issues)}")

        lines = [
            "联网搜索配置检查：",
            f"配置文件：{self._project_path(local_path)}",
            f"本地配置：{'存在' if local_path.exists() else '未创建'}",
            router.describe(),
            "检查方式：只读取本地配置和环境变量，不发起网络请求。",
        ]
        if issues:
            lines.append("结果：配置未完成，修正后执行 /search-enable。")
        elif not router.settings.enabled:
            lines.append("结果：联网搜索未启用，可先执行 /search-config-init。")
        else:
            lines.append("结果：配置完整，可执行 /search-enable 或 /search 关键词。")
        return "\n".join(lines)

    def _search_config_set(self, args: list[str]) -> str:
        if not args:
            self.tools.run("record_log", message="查看联网搜索本地配置写入用法")
            return self._search_config_set_usage()
        try:
            updates = self._parse_config_set_updates(args)
            local_path, changed_fields = write_search_local_config_values(self.paths, updates)
        except ValueError as exc:
            return f"联网搜索配置写入失败：{exc}\n{self._search_config_set_usage()}"

        if not self._search_router_injected:
            self.search_router = build_search_router(paths=self.paths)
        self.tools.run("record_log", message=f"写入联网搜索本地配置：fields={','.join(changed_fields)}")
        return "\n".join(
            [
                f"已写入联网搜索本地配置：{self._project_path(local_path)}",
                f"变更字段：{'、'.join(changed_fields)}",
                "说明：响应和日志不会显示真实 API key。",
                "下一步：/search-config-check",
                "启用：/search-enable",
                "搜索测试：/search Python 版本",
            ]
        )

    def _search_config_set_usage(self) -> str:
        return "\n".join(
            [
                "用法：/search-config-set key=value ...",
                "示例：/search-config-set provider=tavily api_key=你的key max_results=3",
                "支持字段：provider、api_key、base_url、max_results、fake_results",
                "说明：不会回显 api_key；写入后执行 /search-config-check。",
            ]
        )

    def _parse_config_set_updates(self, args: list[str]) -> dict[str, str]:
        updates: dict[str, str] = {}
        for raw_arg in args:
            if "=" not in raw_arg:
                raise ValueError(f"配置参数必须使用 key=value：{raw_arg}")
            key, value = raw_arg.split("=", 1)
            normalized_key = key.strip().lower()
            if not normalized_key:
                raise ValueError(f"配置字段不能为空：{raw_arg}")
            updates[normalized_key] = self._strip_quotes(value.strip())
        if not updates:
            raise ValueError("至少需要提供一个 key=value 参数")
        return updates

    def _handle_pending_llm_clarification(self, prompt: str) -> str | None:
        pending = self._pending_llm_clarification
        if pending is None:
            return None
        if self._is_inner_brain_clarification_cancel(prompt):
            self._pending_llm_clarification = None
            self._save_runtime_context()
            self.tools.run("record_log", message="取消 LLM 外脑澄清")
            return "已取消这次外脑补充。"

        combined_prompt = "\n".join(
            [
                f"原始问题：{pending.original_prompt}",
                f"外脑澄清问题：{pending.clarification}",
                f"用户补充：{prompt}",
            ]
        )
        context = (*pending.context, f"LLM 澄清补充：{prompt}")
        intent = self.llm_router.complete_intent(combined_prompt, context)
        if intent is None:
            self._pending_llm_clarification = None
            self._save_runtime_context()
            self.tools.run("record_log", message="LLM 外脑澄清补充未返回结果")
            return "已补齐外脑需要的信息，但 LLM 外脑没有返回可执行结果。"

        self._record_llm_usage(intent)
        self._remember_recent_llm_call("clarification", combined_prompt, intent)
        if intent.type == "clarify" and intent.clarification:
            next_count = pending.clarification_count + 1
            if next_count > LLM_CLARIFICATION_MAX_ROUNDS:
                self._pending_llm_clarification = None
                self._save_runtime_context()
                self.tools.run("record_log", message="LLM 外脑连续澄清超过上限")
                return "LLM 外脑连续追问过多，已结束这次外脑补充。请把完整需求重新说一遍。"
            self._pending_llm_clarification = PendingLLMClarification(
                original_prompt=pending.original_prompt,
                clarification=intent.clarification,
                context=context,
                clarification_count=next_count,
                created_at=pending.created_at or self._now_iso(),
            )
            self._save_runtime_context()
            self.tools.run("record_log", message=f"LLM 外脑继续澄清第 {next_count} 轮：{intent.clarification}")
            return (
                f"LLM 外脑仍需要补充信息（第 {next_count}/{LLM_CLARIFICATION_MAX_ROUNDS} 轮）："
                f"{intent.clarification}"
            )

        self._pending_llm_clarification = None
        self._save_runtime_context()
        self.tools.run("record_log", message="LLM 外脑澄清补充完成")
        response = self._handle_llm_intent(intent, combined_prompt, context)
        if not response:
            return "已补齐外脑需要的信息，但 LLM 外脑没有返回可执行结果。"
        return "\n".join(["已补齐外脑需要的信息，继续处理。", response])

    def _handle_llm_intent(
        self,
        intent: LLMIntent,
        prompt: str = "",
        context: tuple[str, ...] = (),
    ) -> str:
        if intent.type == "command" and intent.command:
            command = intent.command.strip()
            if not command.startswith("/"):
                return f"LLM 外脑给出了非命令建议：{command}"
            if not is_llm_allowed_command(command):
                return f"LLM 外脑拒绝执行未列入白名单的命令：{command}"
            return "\n".join(
                [
                    f"LLM 外脑建议执行命令：{command}",
                    self.handle(command),
                ]
            )
        if intent.type == "answer" and intent.answer:
            return f"LLM 外脑：{intent.answer}"
        if intent.type == "clarify" and intent.clarification:
            if prompt:
                self._pending_llm_clarification = PendingLLMClarification(
                    original_prompt=prompt,
                    clarification=intent.clarification,
                    context=context,
                    clarification_count=1,
                    created_at=self._now_iso(),
                )
                self._save_runtime_context()
                self.tools.run("record_log", message=f"LLM 外脑需要澄清：{intent.clarification}")
            return f"LLM 外脑需要补充信息：{intent.clarification}"
        return ""

    def _record_llm_usage(self, intent: LLMIntent) -> None:
        if intent.usage is None:
            return
        usage = intent.usage
        self.tools.run(
            "record_log",
            message=(
                "LLM 外脑用量："
                f"provider={usage.provider} "
                f"model={usage.model} "
                f"input_tokens={usage.input_tokens} "
                f"output_tokens={usage.output_tokens} "
                f"total_tokens={usage.total_tokens}"
            ),
        )

    def _llm_context_lines(self) -> tuple[str, ...]:
        lines = [f"记忆摘要：{summarize_profile(read_profile(self.paths))}"]
        if self._recent_document_path is not None:
            lines.append(f"最近资料：data/{self._recent_document_path}")
        if self._recent_search_result_paths:
            lines.append(f"最近搜索结果：{len(self._recent_search_result_paths)} 条")
            for index, relative_path in enumerate(self._recent_search_result_paths[:3], start=1):
                lines.append(f"{index}. data/{relative_path}")
        if self._recent_web_search is not None and self._recent_web_search.results:
            lines.append(f"最近联网搜索：{self._recent_web_search.query}")
            for index, result in enumerate(self._recent_web_search.results[:3], start=1):
                result_line = f"{index}. {result.title} | URL：{result.url}"
                if result.snippet:
                    result_line += f" | 摘要：{result.snippet}"
                if result.source:
                    result_line += f" | 来源：{result.source}"
                lines.append(result_line)
        if self._recent_directory is not None:
            lines.append(f"最近目录：{self._recent_directory.alias} -> {self._recent_directory.path}")
        if self._recent_advice_suggestions:
            lines.append(f"最近建议数量：{len(self._recent_advice_suggestions)}")
        recent_experiences = list_recent_experiences(self.paths)
        if (
            self._recent_document_path is not None
            or self._recent_directory is not None
            or self._recent_files
            or self._recent_advice_suggestions
            or recent_experiences
        ):
            next_actions = suggest_next_actions_from_context(self._runtime_context(), recent_experiences)
            if next_actions:
                lines.append(f"下一步建议：{'；'.join(next_actions[:3])}")
        return tuple(lines)

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
        if not (self.paths.data_dir / relative_path).is_file():
            return f"第 {document_index} 份资料：data/{relative_path}（资料缺失）\n你可以先查看 /kb，或重新导入资料。"
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

    def _read_tagged_documents_history_documents(self, history_index: int) -> str:
        if not self._recent_tagged_documents_operations:
            return "还没有批量标签历史。你可以先说“给项目标签资料都打标签 归档”，再说“确认执行”。"
        if history_index < 1 or history_index > len(self._recent_tagged_documents_operations):
            return f"批量标签历史只有 {len(self._recent_tagged_documents_operations)} 条，不能选择第 {history_index} 条。"

        operation = self._recent_tagged_documents_operations[history_index - 1]
        if not operation.document_paths:
            return f"第 {history_index} 条批量标签历史没有保存影响资料列表。你可以查看 /tag-history。"

        self._recent_document_path = operation.document_paths[0]
        self._recent_document_paths = operation.document_paths
        self._save_runtime_context()
        self.tools.run("record_log", message=f"读取批量标签历史影响资料：第 {history_index} 条")

        appended_tags = "、".join(operation.tags)
        lines = [
            f"第 {history_index} 条批量标签历史影响资料：{operation.tag}标签资料 -> 追加标签：{appended_tags}",
        ]
        for document_index, relative_path in enumerate(operation.document_paths, start=1):
            document_path = self.paths.data_dir / relative_path
            if not document_path.is_file():
                lines.append(f"{document_index}. data/{relative_path}（资料缺失）")
                continue
            lines.append(f"{document_index}. data/{relative_path}")
            preview = self._document_preview(relative_path)
            if preview:
                lines.append(f"   摘要：{preview}")
        if operation.restore_commands:
            lines.append(f"恢复提示：{'；'.join(operation.restore_commands)}")
        lines.append("可继续操作：读取第一份资料；给第一份资料打标签 标签；/tag-history")
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
        if not (self.paths.data_dir / relative_path).is_file():
            return f"第 {document_index} 份资料：data/{relative_path}（资料缺失）\n你可以先查看 /kb，或重新导入资料。"
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
        self._remember_tagged_documents_operation(
            RuntimeTaggedDocumentsOperationContext(
                tag=group_tag,
                tags=new_tags,
                updated_count=updated_count,
                restore_commands=tuple(restore_commands),
                document_paths=document_paths,
            )
        )
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

    def _remember_recent_web_search(self, query: str, results: tuple[SearchResult, ...]) -> None:
        self._recent_web_search = RuntimeWebSearchContext(
            query=query,
            results=tuple(
                RuntimeWebSearchResultContext(
                    title=result.title,
                    url=result.url,
                    snippet=result.snippet,
                    source=result.source,
                )
                for result in results[:5]
            ),
        )
        self._save_runtime_context()

    def _remember_recent_advice_suggestions(self, suggestions: tuple[str, ...]) -> None:
        self._recent_advice_suggestions = suggestions
        self._pending_advice_command = None
        self._pending_advice_command_draft_command = None
        self._save_runtime_context()

    def _remember_recent_files(self, recent_files: tuple[RuntimeRecentFileContext, ...]) -> None:
        self._recent_files = recent_files
        self._save_runtime_context()

    def _remember_tagged_documents_operation(self, operation: RuntimeTaggedDocumentsOperationContext) -> None:
        self._recent_tagged_documents_operation_tag = operation.tag
        self._recent_tagged_documents_operation_tags = operation.tags
        self._recent_tagged_documents_operation_updated_count = operation.updated_count
        self._recent_tagged_documents_operation_restore_commands = operation.restore_commands
        self._recent_tagged_documents_operations = (operation, *self._recent_tagged_documents_operations)[:5]
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
            recent_web_search=self._recent_web_search,
            recent_advice_suggestions=self._recent_advice_suggestions,
            recent_files=self._recent_files,
            recent_tagged_documents_operation=self._runtime_tagged_documents_operation(),
            recent_tagged_documents_operations=self._recent_tagged_documents_operations,
            pending_llm_clarification=self._runtime_pending_llm_clarification(),
            recent_llm_call=self._recent_llm_call,
            recent_route_decision=self._recent_route_decision,
            recent_route_decisions=self._recent_route_decisions,
            inner_brain_candidates=(
                self._inner_brain_candidate_stats if self._inner_brain_candidate_stats_initialized else None
            ),
        )

    def _save_runtime_context(self) -> None:
        save_runtime_context(self.paths, self._runtime_context())

    def _restore_pending_llm_clarification(
        self,
        context: RuntimeLLMClarificationContext | None,
    ) -> PendingLLMClarification | None:
        if context is None:
            return None
        created_at = context.created_at or self._now_iso()
        if self._is_llm_clarification_expired(created_at):
            return None
        return PendingLLMClarification(
            original_prompt=context.original_prompt,
            clarification=context.clarification,
            context=context.context,
            clarification_count=max(1, min(context.clarification_count, LLM_CLARIFICATION_MAX_ROUNDS)),
            created_at=created_at,
        )

    def _runtime_pending_llm_clarification(self) -> RuntimeLLMClarificationContext | None:
        if self._pending_llm_clarification is None:
            return None
        return RuntimeLLMClarificationContext(
            original_prompt=self._pending_llm_clarification.original_prompt,
            clarification=self._pending_llm_clarification.clarification,
            context=self._pending_llm_clarification.context,
            clarification_count=self._pending_llm_clarification.clarification_count,
            created_at=self._pending_llm_clarification.created_at or self._now_iso(),
        )

    def _remember_recent_llm_call(self, source: str, prompt: str, intent: LLMIntent) -> None:
        summary = self._llm_intent_summary(intent)
        settings = self.llm_router.settings
        self._recent_llm_call = RuntimeLLMCallContext(
            source=source,
            prompt=self._compact_status_text(prompt),
            intent_type=intent.type,
            summary=self._compact_status_text(summary),
            reason=self._compact_status_text(intent.reason),
            provider=settings.provider,
            model=settings.model,
            created_at=self._now_iso(),
        )
        self._save_runtime_context()

    def _remember_route_decision(
        self,
        route: str,
        detail: str,
        prompt: str,
        summary: str,
        explanation: str = "",
    ) -> None:
        decision = RuntimeRouteDecisionContext(
            route=route,
            detail=detail,
            prompt=self._compact_status_text(prompt),
            summary=self._compact_status_text(summary),
            explanation=self._compact_status_text(explanation, max_length=220),
            created_at=self._now_iso(),
        )
        self._recent_route_decision = decision
        self._recent_route_decisions = (decision, *self._recent_route_decisions)[:5]
        if self._is_inner_brain_candidate_decision(decision):
            self._remember_inner_brain_candidate_observation(decision)
        self._save_runtime_context()

    def _remember_inner_brain_candidate_observation(self, decision: RuntimeRouteDecisionContext) -> None:
        prompt_key = decision.prompt.strip()
        if not prompt_key:
            return
        self._inner_brain_candidate_stats_initialized = True
        existing = next(
            (candidate for candidate in self._inner_brain_candidate_stats if candidate.prompt.strip() == prompt_key),
            None,
        )
        first_seen_at = existing.first_seen_at if existing is not None else decision.created_at
        count = existing.count + 1 if existing is not None else 1
        updated_candidate = RuntimeInnerBrainCandidateContext(
            prompt=decision.prompt,
            route=decision.route,
            detail=decision.detail,
            summary=decision.summary,
            explanation=decision.explanation,
            count=count,
            first_seen_at=first_seen_at or decision.created_at,
            last_seen_at=decision.created_at,
        )
        remaining_candidates = tuple(
            candidate for candidate in self._inner_brain_candidate_stats if candidate.prompt.strip() != prompt_key
        )
        candidates = (updated_candidate, *remaining_candidates)
        self._inner_brain_candidate_stats = tuple(sorted(candidates, key=lambda candidate: -candidate.count))[:20]

    def _forget_inner_brain_candidate(self, sample_text: str) -> None:
        prompt_key = sample_text.strip()
        if not prompt_key:
            return
        remaining_candidates = tuple(
            candidate for candidate in self._inner_brain_candidate_stats if candidate.prompt.strip() != prompt_key
        )
        if remaining_candidates == self._inner_brain_candidate_stats and self._inner_brain_candidate_stats_initialized:
            return
        self._inner_brain_candidate_stats = remaining_candidates
        self._inner_brain_candidate_stats_initialized = True
        self._save_runtime_context()

    def _remember_command_route(self, prompt: str) -> None:
        self._remember_route_decision(
            "command",
            self._route_command_detail(prompt),
            prompt,
            "显式命令",
            "source=explicit-command action=direct-dispatch",
        )

    def _route_command_detail(self, prompt: str) -> str:
        try:
            parts = shlex.split(prompt, posix=False)
        except ValueError:
            parts = prompt.split()
        if not parts:
            return "unknown"
        return parts[0]

    def _route_history_line(self, index: int, decision: RuntimeRouteDecisionContext) -> str:
        parts = [
            f"{index}. {decision.route} / {decision.detail}",
            f"输入：{decision.prompt}",
        ]
        if decision.summary:
            parts.append(f"结果：{decision.summary}")
        return " | ".join(parts)

    def _route_history_detail_lines(self, index: int, decision: RuntimeRouteDecisionContext) -> list[str]:
        lines = [f"{index}. {decision.route} / {decision.detail}"]
        if decision.created_at:
            lines.append(f"   时间：{decision.created_at}")
        lines.append(f"   输入：{decision.prompt}")
        if decision.summary:
            lines.append(f"   结果：{decision.summary}")
        if decision.explanation:
            lines.append(f"   依据：{decision.explanation}")
        return lines

    def _inner_brain_route_explanation(self, result: InnerBrainResult) -> str:
        parts = [
            f"source={result.source}",
            f"confidence={result.confidence:.2f}",
        ]
        if result.missing:
            parts.append(f"missing={','.join(result.missing)}")
        if result.reason:
            parts.append(f"reason={result.reason}")
        return " ".join(parts)

    def _llm_route_explanation(self) -> str:
        call = self._recent_llm_call
        if call is None:
            return "source=llm-fallback type=unknown"
        parts = [
            f"provider={call.provider or self.llm_router.settings.provider}",
        ]
        if call.model or self.llm_router.settings.model:
            parts.append(f"model={call.model or self.llm_router.settings.model}")
        parts.extend(
            [
                f"source={call.source}",
                f"type={call.intent_type}",
            ]
        )
        if call.summary:
            parts.append(f"summary={call.summary}")
        if call.reason:
            parts.append(f"reason={call.reason}")
        return " ".join(parts)

    def _is_explicit_command_prompt(self, prompt: str) -> bool:
        if prompt.startswith("/"):
            return True
        return prompt in {
            "help",
            "memory",
            "experiences",
            "tools",
            "status",
            "llm-status",
            "search-status",
            "inner-brain-status",
            "inner-brain-eval",
            "inner-brain-eval-failed",
            "inner-brain-eval-local",
            "inner-brain-eval-local-failed",
            "inner-brain-eval-local-report",
            "inner-brain-eval-local-file",
            "inner-brain-eval-local-file-failed",
            "inner-brain-eval-local-resolved",
            "inner-brain-candidates",
            "inner-brain-teach-candidate",
            "inner-brain-label-candidate",
            "brain-candidates",
            "llm-usage",
            "llm-context-preview",
            "recent-context",
            "context",
            "route-history",
            "routes",
            "kb",
            "knowledge",
            "kb-summary",
            "knowledge-summary",
            "voice-status",
            "automation-status",
            "recent-files",
            "tag-history",
            "batch-tag-history",
            "update-status",
            "update-download",
            "dirs",
        }

    def _is_recent_context_prompt(self, prompt: str) -> bool:
        return prompt in {"/recent-context", "recent-context", "/context", "context"}

    def _is_route_history_prompt(self, prompt: str) -> bool:
        return prompt in {"/route-history", "route-history", "/routes", "routes"}

    def _is_inner_brain_candidates_prompt(self, prompt: str) -> bool:
        return prompt in {"/inner-brain-candidates", "inner-brain-candidates", "/brain-candidates", "brain-candidates"}

    def _is_inner_brain_eval_prompt(self, prompt: str) -> bool:
        return prompt in {"/inner-brain-eval", "inner-brain-eval", "/brain-eval", "brain-eval"}

    def _is_inner_brain_eval_failures_prompt(self, prompt: str) -> bool:
        return prompt in {
            "/inner-brain-eval-failed",
            "inner-brain-eval-failed",
            "/brain-eval-failed",
            "brain-eval-failed",
            "/inner-brain-eval-failures",
            "inner-brain-eval-failures",
        }

    def _is_inner_brain_eval_local_prompt(self, prompt: str) -> bool:
        return prompt in {
            "/inner-brain-eval-local",
            "inner-brain-eval-local",
            "/brain-eval-local",
            "brain-eval-local",
        }

    def _is_inner_brain_eval_local_failures_prompt(self, prompt: str) -> bool:
        return prompt in {
            "/inner-brain-eval-local-failed",
            "inner-brain-eval-local-failed",
            "/brain-eval-local-failed",
            "brain-eval-local-failed",
            "/inner-brain-eval-local-failures",
            "inner-brain-eval-local-failures",
        }

    def _is_inner_brain_eval_local_report_prompt(self, prompt: str) -> bool:
        return prompt == "/inner-brain-eval-local-report" or prompt.startswith("/inner-brain-eval-local-report ")

    def _is_inner_brain_eval_local_file_prompt(self, prompt: str) -> bool:
        return prompt in {
            "/inner-brain-eval-local-file",
            "inner-brain-eval-local-file",
        } or prompt.startswith("/inner-brain-eval-local-file ")

    def _is_inner_brain_eval_local_file_failures_prompt(self, prompt: str) -> bool:
        return prompt in {
            "/inner-brain-eval-local-file-failed",
            "inner-brain-eval-local-file-failed",
            "/inner-brain-eval-local-file-failures",
            "inner-brain-eval-local-file-failures",
        } or prompt.startswith(("/inner-brain-eval-local-file-failed ", "/inner-brain-eval-local-file-failures "))

    def _is_inner_brain_eval_local_resolved_prompt(self, prompt: str) -> bool:
        return prompt in {
            "/inner-brain-eval-local-resolved",
            "inner-brain-eval-local-resolved",
        } or prompt.startswith("/inner-brain-eval-local-resolved ")

    def _is_inner_brain_teach_candidate_prompt(self, prompt: str) -> bool:
        return prompt == "/inner-brain-teach-candidate" or prompt.startswith("/inner-brain-teach-candidate ")

    def _is_inner_brain_label_candidate_prompt(self, prompt: str) -> bool:
        return prompt == "/inner-brain-label-candidate" or prompt.startswith("/inner-brain-label-candidate ")

    def _is_inner_brain_eval_add_candidate_prompt(self, prompt: str) -> bool:
        return prompt == "/inner-brain-eval-add-candidate" or prompt.startswith("/inner-brain-eval-add-candidate ")

    def _is_inner_brain_eval_label_candidate_prompt(self, prompt: str) -> bool:
        return prompt == "/inner-brain-eval-label-candidate" or prompt.startswith("/inner-brain-eval-label-candidate ")

    def _is_route_observability_prompt(self, prompt: str) -> bool:
        return (
            self._is_recent_context_prompt(prompt)
            or self._is_route_history_prompt(prompt)
            or self._is_inner_brain_eval_local_report_prompt(prompt)
            or self._is_inner_brain_eval_local_file_failures_prompt(prompt)
            or self._is_inner_brain_eval_local_file_prompt(prompt)
            or self._is_inner_brain_eval_local_failures_prompt(prompt)
            or self._is_inner_brain_eval_local_prompt(prompt)
            or self._is_inner_brain_eval_failures_prompt(prompt)
            or self._is_inner_brain_eval_prompt(prompt)
            or self._is_inner_brain_candidates_prompt(prompt)
            or self._is_inner_brain_teach_candidate_prompt(prompt)
            or self._is_inner_brain_label_candidate_prompt(prompt)
            or self._is_inner_brain_eval_add_candidate_prompt(prompt)
            or self._is_inner_brain_eval_label_candidate_prompt(prompt)
        )

    def _llm_intent_summary(self, intent: LLMIntent) -> str:
        if intent.type == "answer" and intent.answer:
            return intent.answer
        if intent.type == "command" and intent.command:
            return intent.command
        if intent.type == "clarify" and intent.clarification:
            return intent.clarification
        if intent.reason:
            return intent.reason
        return "无可用内容"

    def _compact_status_text(self, text: str, max_length: int = 120) -> str:
        value = " ".join(text.split())
        if self.llm_router.settings.api_key:
            value = value.replace(self.llm_router.settings.api_key, "<redacted>")
        value = re.sub(r"(api_key\s*=\s*)\S+", r"\1<redacted>", value, flags=re.IGNORECASE)
        if len(value) <= max_length:
            return value
        return f"{value[: max_length - 1]}…"

    def _is_llm_clarification_expired(self, created_at: str) -> bool:
        try:
            created = datetime.fromisoformat(created_at)
        except ValueError:
            return True
        now = datetime.now(created.tzinfo) if created.tzinfo is not None else datetime.now()
        return now - created > timedelta(seconds=LLM_CLARIFICATION_EXPIRES_AFTER_SECONDS)

    def _now_iso(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def _runtime_tagged_documents_operation(self) -> RuntimeTaggedDocumentsOperationContext | None:
        if self._recent_tagged_documents_operations:
            operation = self._recent_tagged_documents_operations[0]
            if (
                operation.tag == self._recent_tagged_documents_operation_tag
                and operation.tags == self._recent_tagged_documents_operation_tags
                and operation.updated_count == self._recent_tagged_documents_operation_updated_count
                and operation.restore_commands == self._recent_tagged_documents_operation_restore_commands
            ):
                return operation
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

    def _delete_desktop_shortcuts(self, names: tuple[str, ...]) -> str:
        if not names:
            return "没有识别到要删除的桌面快捷方式名称。"

        desktop = self._known_directory("桌面")
        if desktop is None:
            return "没有找到桌面目录，无法删除桌面快捷方式。"

        deleted: list[str] = []
        missing: list[str] = []
        for raw_name in names:
            shortcut_name = self._desktop_shortcut_filename(raw_name)
            if not shortcut_name:
                continue
            target = desktop.path / shortcut_name
            if target.is_file() and target.suffix.lower() == ".lnk":
                target.unlink()
                deleted.append(shortcut_name)
            else:
                missing.append(shortcut_name)

        self.tools.run(
            "record_log",
            message=(
                "删除桌面快捷方式："
                f"deleted={','.join(deleted) or '无'} "
                f"missing={','.join(missing) or '无'}"
            ),
        )

        lines: list[str] = []
        if deleted:
            lines.append(f"已删除桌面快捷方式：{'、'.join(deleted)}")
        if missing:
            lines.append(f"未找到：{'、'.join(missing)}")
        if not lines:
            lines.append("没有识别到可处理的桌面快捷方式名称。")
        lines.append("范围：只处理桌面目录下明确点名的 .lnk 快捷方式。")
        return "\n".join(lines)

    def _desktop_shortcut_filename(self, raw_name: str) -> str:
        name = Path(raw_name.replace("\\", "/")).name.strip().strip("“”\"'").strip()
        name = name.removeprefix("的").strip()
        name = name.removesuffix("的").removesuffix("快捷方式").removesuffix("的").strip()
        if not name:
            return ""
        if name.lower().endswith(".lnk"):
            return name
        return f"{name}.lnk"

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
                "- 批量标签：标签组预览、确认、恢复提示和 /tag-history 历史记录",
                "- 记忆写入：/remember、/experience、我叫...、我是...",
                "- 本地验证：python -m unittest discover -s tests -v",
                f"- LLM 外脑：{self.llm_router.settings.provider}",
                f"- 联网搜索：{self.search_router.settings.provider}",
            ]
        )
