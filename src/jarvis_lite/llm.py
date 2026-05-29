from __future__ import annotations

import json
import os
import shlex
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol
from urllib.parse import urlsplit, urlunsplit

from .config import ProjectPaths


VALID_LLM_INTENT_TYPES = {"command", "answer", "clarify", "no_action"}
LLM_PROVIDER_ALIASES = {"qwen": "openai-compatible", "gemini": "openai-compatible"}
VALID_LLM_PROVIDERS = {"off", "fake", "openai", "openai-compatible", *LLM_PROVIDER_ALIASES}
LLM_CONFIG_TEMPLATE_ALIASES = dict(LLM_PROVIDER_ALIASES)
LLM_LOCAL_CONFIG_RELATIVE_PATH = Path("config") / "llm.local.json"
LLM_EXAMPLE_CONFIG_RELATIVE_PATH = Path("config") / "llm.example.json"
LLM_ALLOWED_COMMAND_SPECS = (
    "/kb",
    "/kb-summary",
    "/ask 问题",
    "/read 文件名",
    "/tag 文件名 标签...",
    "/memory",
    "/experiences",
    "/experience-advice 关键词",
    "/recent-files",
    "/tag-history",
    "/daily-report [文件名]",
    "/automation-status",
    "/voice-status",
    "/update-status [清单路径或URL]",
    "/update-download [清单路径或URL]",
    "/search 关键词",
    "/search-summary 关键词",
    "/search-open 编号",
    "/search-compare",
    "/search-save-summary [文件名]",
    "/search-import-summary [文件名]",
    "/llm-config-init [provider]",
    "/search-config-init [provider]",
)
LLM_ALLOWED_COMMAND_NAMES = tuple(spec.split(maxsplit=1)[0] for spec in LLM_ALLOWED_COMMAND_SPECS)
LLM_INTENT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "type": {
            "type": "string",
            "enum": sorted(VALID_LLM_INTENT_TYPES),
        },
        "command": {"type": "string"},
        "answer": {"type": "string"},
        "clarification": {"type": "string"},
        "reason": {"type": "string"},
    },
    "required": ["type", "command", "answer", "clarification", "reason"],
}


@dataclass(frozen=True)
class LLMSettings:
    """保存外脑 provider 的通用配置，不绑定具体厂商。"""

    provider: str = "off"
    model: str = ""
    base_url: str = ""
    api_key: str = ""
    fake_response: str = ""
    config_source: str = ""
    config_error: str = ""

    @property
    def enabled(self) -> bool:
        return self.provider != "off"

    @property
    def adapter_provider(self) -> str:
        """返回实际调用的 adapter，provider alias 只改变配置入口。"""

        return LLM_PROVIDER_ALIASES.get(self.provider, self.provider)

    def configuration_issues(self) -> tuple[str, ...]:
        issues: list[str] = []
        if self.config_error:
            issues.append(self.config_error)
        if self.provider not in VALID_LLM_PROVIDERS:
            issues.append(f"未知 provider：{self.provider}")
            return tuple(issues)
        if not self.enabled or self.provider == "fake":
            return ()
        adapter_provider = self.adapter_provider
        if adapter_provider in {"openai", "openai-compatible"}:
            if not self.model:
                issues.append("缺少 JARVIS_LITE_LLM_MODEL")
            if not self.api_key:
                issues.append("缺少 JARVIS_LITE_LLM_API_KEY")
            if adapter_provider == "openai-compatible" and not self.base_url:
                issues.append("缺少 JARVIS_LITE_LLM_BASE_URL")
        return tuple(issues)

    def sdk_base_url(self) -> str:
        """返回传给 OpenAI SDK 的 base_url，兼容用户粘贴完整 /responses URL。"""

        return normalize_responses_base_url(self.base_url)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "LLMSettings":
        values = env if env is not None else os.environ
        source = "environment" if any(key in values for key in _llm_env_setting_keys()) else ""
        return cls(
            provider=values.get("JARVIS_LITE_LLM_PROVIDER", "off").strip().lower() or "off",
            model=values.get("JARVIS_LITE_LLM_MODEL", "").strip(),
            base_url=values.get("JARVIS_LITE_LLM_BASE_URL", "").strip(),
            api_key=values.get("JARVIS_LITE_LLM_API_KEY", "").strip(),
            fake_response=values.get("JARVIS_LITE_LLM_FAKE_RESPONSE", "").strip(),
            config_source=source,
        )

    @classmethod
    def from_sources(
        cls,
        paths: ProjectPaths | None = None,
        env: Mapping[str, str] | None = None,
    ) -> "LLMSettings":
        """按本地配置文件 + 环境变量覆盖的顺序读取外脑配置。"""

        config_values, config_source, config_error = _read_llm_local_config(paths)
        env_values = env if env is not None else os.environ
        values = dict(config_values)
        env_used = False
        for env_key, setting_key in _llm_env_setting_keys().items():
            if env_key not in env_values:
                continue
            values[setting_key] = str(env_values.get(env_key, "")).strip()
            env_used = True

        provider = str(values.get("provider") or "off").strip().lower() or "off"
        source = config_source
        if env_used:
            source = "environment" if not source else f"environment + {source}"
        return cls(
            provider=provider,
            model=str(values.get("model") or "").strip(),
            base_url=str(values.get("base_url") or "").strip(),
            api_key=str(values.get("api_key") or "").strip(),
            fake_response=str(values.get("fake_response") or "").strip(),
            config_source=source,
            config_error=config_error,
        )


@dataclass(frozen=True)
class LLMUsage:
    """记录一次 provider 调用返回的 token 用量。"""

    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


@dataclass
class _LLMUsageBucket:
    count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


@dataclass(frozen=True)
class LLMIntent:
    """LLM 外脑返回给本地 Agent 的结构化意图。"""

    type: str
    command: str = ""
    answer: str = ""
    clarification: str = ""
    reason: str = ""
    usage: LLMUsage | None = None


class LLMProvider(Protocol):
    """不同大模型 provider 需要实现的统一接口。"""

    name: str

    def complete_intent(self, prompt: str, context: tuple[str, ...]) -> LLMIntent:
        """把用户输入和本地上下文转换为结构化意图。"""


class FakeLLMProvider:
    """用于本地测试的固定响应 provider。"""

    name = "fake"

    def __init__(self, response: str = ""):
        self.response = response or '{"type":"no_action","reason":"fake provider 未配置响应"}'
        self.calls: list[tuple[str, tuple[str, ...]]] = []

    def complete_intent(self, prompt: str, context: tuple[str, ...]) -> LLMIntent:
        self.calls.append((prompt, context))
        return parse_llm_intent(self.response)


class OpenAIResponsesProvider:
    """使用 OpenAI Responses API 或兼容端点的 provider 适配器。"""

    name = "openai"

    def __init__(self, settings: LLMSettings):
        self.settings = settings

    def complete_intent(self, prompt: str, context: tuple[str, ...]) -> LLMIntent:
        if not self.settings.api_key:
            return LLMIntent(type="no_action", reason="未配置 JARVIS_LITE_LLM_API_KEY")
        if not self.settings.model:
            return LLMIntent(type="no_action", reason="未配置 JARVIS_LITE_LLM_MODEL")
        if self.settings.adapter_provider == "openai-compatible" and not self.settings.base_url:
            return LLMIntent(type="no_action", reason="openai-compatible provider 未配置 JARVIS_LITE_LLM_BASE_URL")

        client_class = self._openai_client_class()
        if client_class is None:
            return LLMIntent(type="no_action", reason="OpenAI SDK 未安装，请先安装项目依赖")

        client_kwargs = {"api_key": self.settings.api_key}
        sdk_base_url = self.settings.sdk_base_url()
        if sdk_base_url:
            client_kwargs["base_url"] = sdk_base_url

        try:
            client = client_class(**client_kwargs)
            response = client.responses.create(
                model=self.settings.model,
                instructions=self._instructions(),
                input=self._input_text(prompt, context),
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "jarvis_lite_llm_intent",
                        "schema": LLM_INTENT_SCHEMA,
                        "strict": True,
                    }
                },
            )
        except Exception as exc:
            return LLMIntent(type="no_action", reason=self._format_call_error(exc))

        raw_text = self._response_text(response)
        if not raw_text:
            return LLMIntent(type="no_action", reason="OpenAI Responses API 未返回文本内容")
        intent = parse_llm_intent(raw_text)
        usage = self._response_usage(response)
        if usage is None:
            return intent
        return replace(intent, usage=usage)

    def _openai_client_class(self):
        try:
            from openai import OpenAI
        except ImportError:
            return None
        return OpenAI

    def _instructions(self) -> str:
        command_lines = [f"- {command}" for command in LLM_ALLOWED_COMMAND_SPECS]
        return "\n".join(
            [
                "你是 Jarvis Lite 的 LLM 外脑，只能返回结构化意图。",
                "本地 Agent 会先处理命令、身份、本地自然语言意图和知识库问答。",
                "当适合调用本地能力时返回 command，command 必须是一个以 / 开头的 Jarvis Lite 命令。",
                "可返回的 Jarvis Lite 命令：",
                *command_lines,
                "不要返回列表之外的命令；不确定具体参数时返回 clarify。",
                "当可以直接回答时返回 answer；需要补充信息时返回 clarify；不应处理时返回 no_action。",
                "不要声称已经执行命令；命令只由本地 Agent 执行。",
            ]
        )

    def _input_text(self, prompt: str, context: tuple[str, ...]) -> str:
        lines = ["用户输入：", prompt]
        if context:
            lines.extend(["", "本地上下文：", *context])
        return "\n".join(lines)

    def _response_text(self, response) -> str:
        output_text = getattr(response, "output_text", "")
        if isinstance(output_text, str) and output_text.strip():
            return output_text.strip()

        output_items = getattr(response, "output", None)
        if not output_items:
            return ""
        text_parts: list[str] = []
        for output_item in output_items:
            contents = self._item_value(output_item, "content") or ()
            for content in contents:
                text = self._item_value(content, "text")
                if isinstance(text, str) and text.strip():
                    text_parts.append(text.strip())
        return "\n".join(text_parts).strip()

    def _response_usage(self, response) -> LLMUsage | None:
        usage = self._item_value(response, "usage")
        if usage is None:
            return None

        input_tokens = self._usage_int(usage, "input_tokens")
        if input_tokens is None:
            input_tokens = self._usage_int(usage, "prompt_tokens") or 0
        output_tokens = self._usage_int(usage, "output_tokens")
        if output_tokens is None:
            output_tokens = self._usage_int(usage, "completion_tokens") or 0
        total_tokens = self._usage_int(usage, "total_tokens")
        if total_tokens is None:
            total_tokens = input_tokens + output_tokens

        return LLMUsage(
            provider=self.settings.provider,
            model=self.settings.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
        )

    def _usage_int(self, usage, key: str) -> int | None:
        value = self._item_value(usage, key)
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _item_value(self, item, key: str):
        if isinstance(item, dict):
            return item.get(key)
        return getattr(item, key, None)

    def _format_call_error(self, exc: Exception) -> str:
        status_code = self._exception_status_code(exc)
        if self._exception_is_timeout(exc):
            return "OpenAI provider 调用失败：请求超时，请检查网络、Base URL 或稍后重试。"
        if status_code == 401:
            return "OpenAI provider 调用失败：认证失败（HTTP 401），请检查 JARVIS_LITE_LLM_API_KEY。"
        if status_code == 403:
            return "OpenAI provider 调用失败：权限不足（HTTP 403），请检查 provider 账号权限或模型访问权限。"
        if status_code == 429:
            return "OpenAI provider 调用失败：频率或额度受限（HTTP 429），请稍后重试或检查 provider 额度。"
        if status_code is not None and status_code >= 500:
            return f"OpenAI provider 调用失败：provider 服务端错误（HTTP {status_code}），请稍后重试。"
        if status_code is not None:
            safe_message = self._safe_error_message(exc)
            suffix = f"：{safe_message}" if safe_message else ""
            return f"OpenAI provider 调用失败：HTTP {status_code}{suffix}"

        safe_message = self._safe_error_message(exc)
        if safe_message:
            return f"OpenAI provider 调用失败：{safe_message}"
        return "OpenAI provider 调用失败：未知错误。"

    def _exception_status_code(self, exc: Exception) -> int | None:
        for value in (getattr(exc, "status_code", None), getattr(getattr(exc, "response", None), "status_code", None)):
            try:
                return int(value)
            except (TypeError, ValueError):
                continue
        return None

    def _exception_is_timeout(self, exc: Exception) -> bool:
        name = type(exc).__name__.lower()
        message = str(exc).lower()
        return "timeout" in name or "timed out" in message or "timeout" in message

    def _safe_error_message(self, exc: Exception) -> str:
        message = str(exc).strip()
        if self.settings.api_key:
            message = message.replace(self.settings.api_key, "<redacted>")
        return message


class LLMRouter:
    """负责选择 provider，并向 JarvisAgent 暴露稳定接口。"""

    def __init__(self, settings: LLMSettings, provider: LLMProvider | None = None):
        self.settings = settings
        self.provider = provider

    def complete_intent(self, prompt: str, context: tuple[str, ...]) -> LLMIntent | None:
        if not self.settings.enabled or self.provider is None:
            return None
        return self.provider.complete_intent(prompt, context)

    def describe(self) -> str:
        issues = self.settings.configuration_issues()
        if not self.settings.enabled:
            lines = [
                "LLM 外脑：未启用",
                f"- Provider：{self.settings.provider}",
            ]
            if self.settings.config_source:
                lines.append(f"- 配置来源：{self.settings.config_source}")
            lines.extend(
                [
                    f"- API key：{self._api_key_status()}",
                    f"- 网络调用：{self._network_call_status(issues)}",
                ]
            )
            if issues:
                lines.append("- 配置问题：")
                for issue in issues:
                    lines.append(f"  - {issue}")
            return "\n".join(lines)
        lines = [
            "LLM 外脑：已启用",
            f"- Provider：{self.settings.provider}",
        ]
        if self.settings.adapter_provider != self.settings.provider:
            lines.append(f"- Adapter：{self.settings.adapter_provider}")
        if self.settings.config_source:
            lines.append(f"- 配置来源：{self.settings.config_source}")
        if self.settings.model:
            lines.append(f"- Model：{self.settings.model}")
        if self.settings.base_url:
            lines.append(f"- Base URL：{self.settings.base_url}")
            sdk_base_url = self.settings.sdk_base_url()
            if sdk_base_url and sdk_base_url != self.settings.base_url.rstrip("/"):
                lines.append(f"- SDK Base URL：{sdk_base_url}")
        lines.append(f"- API key：{self._api_key_status()}")
        lines.append(f"- 网络调用：{self._network_call_status(issues)}")
        if issues:
            lines.append("- 配置问题：")
            for issue in issues:
                lines.append(f"  - {issue}")
        else:
            lines.append("- 配置：可调用")
        return "\n".join(lines)

    def _api_key_status(self) -> str:
        return "已配置" if self.settings.api_key else "未配置"

    def _network_call_status(self, issues: tuple[str, ...]) -> str:
        if not self.settings.enabled:
            return "否（LLM 未启用）"
        if self.settings.provider == "fake":
            return "否（fake provider 本地响应）"
        if self.settings.adapter_provider in {"openai", "openai-compatible"}:
            if issues:
                return "否（配置未完成）"
            return "是（/llm-smoke 或 fallback 会调用 provider）"
        return "否（provider 不支持）"


def build_llm_router(
    settings: LLMSettings | None = None,
    paths: ProjectPaths | None = None,
    env: Mapping[str, str] | None = None,
) -> LLMRouter:
    """根据通用配置构建 LLM Router。"""

    resolved_settings = settings or LLMSettings.from_sources(paths, env)
    if not resolved_settings.enabled:
        return LLMRouter(resolved_settings)
    if resolved_settings.provider == "fake":
        return LLMRouter(resolved_settings, FakeLLMProvider(resolved_settings.fake_response))
    if resolved_settings.adapter_provider in {"openai", "openai-compatible"}:
        return LLMRouter(resolved_settings, OpenAIResponsesProvider(resolved_settings))
    return LLMRouter(resolved_settings)


def is_llm_allowed_command(command: str) -> bool:
    """校验 LLM command intent 是否属于本地 Agent 允许执行的命令集合。"""

    try:
        parts = shlex.split(command.strip(), posix=False)
    except ValueError:
        return False
    if not parts:
        return False
    return parts[0] in LLM_ALLOWED_COMMAND_NAMES


def normalize_responses_base_url(base_url: str) -> str:
    """把完整 Responses URL 归一化为 SDK 需要的 base_url。"""

    value = base_url.strip()
    if not value:
        return ""
    parts = urlsplit(value)
    path = parts.path.rstrip("/")
    if path.endswith("/responses"):
        path = path[: -len("/responses")] or "/"
        return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment)).rstrip("/")
    return value.rstrip("/")


def llm_local_config_path(paths: ProjectPaths) -> Path:
    """返回真实 LLM 本地配置文件路径。"""

    return paths.config_dir / LLM_LOCAL_CONFIG_RELATIVE_PATH.name


def llm_example_config_path(paths: ProjectPaths) -> Path:
    """返回本地配置模板文件路径。"""

    return paths.config_dir / LLM_EXAMPLE_CONFIG_RELATIVE_PATH.name


def write_llm_example_config(paths: ProjectPaths) -> Path:
    """确保运行态目录里有一份不会包含真实密钥的 LLM 配置模板。"""

    target = llm_example_config_path(paths)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(llm_example_config_text(), encoding="utf-8")
    return target


def write_llm_local_config_draft(paths: ProjectPaths, provider: str = "") -> tuple[Path, bool, str]:
    """创建不会包含真实密钥的 LLM 本地配置草稿；已存在时不覆盖。"""

    normalized_provider = _normalize_llm_config_provider(provider)
    target = llm_local_config_path(paths)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        return target, False, normalized_provider
    target.write_text(llm_local_config_draft_text(normalized_provider), encoding="utf-8")
    return target, True, normalized_provider


def llm_local_config_draft_text(provider: str = "") -> str:
    """返回 llm.local.json 草稿，敏感字段保持空值。"""

    normalized_provider = _normalize_llm_config_provider(provider)
    fake_response = ""
    if normalized_provider == "fake":
        fake_response = '{"type":"answer","answer":"本地 fake 外脑已启用"}'
    payload = {
        "provider": normalized_provider,
        "model": "",
        "base_url": "",
        "api_key": "",
        "fake_response": fake_response,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def llm_example_config_text() -> str:
    """返回 JSON 模板文本；真实配置应复制到 llm.local.json。"""

    payload = {
        "provider": "openai-compatible",
        "model": "<兼容端点模型名>",
        "base_url": "<兼容端点 base_url 或完整 /v1/responses URL>",
        "api_key": "<你的 API key>",
        "fake_response": "",
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def summarize_llm_usage(log_lines: Iterable[str]) -> str:
    """汇总本地日志中已经记录的 LLM token 用量。"""

    buckets: dict[tuple[str, str], _LLMUsageBucket] = {}
    total = _LLMUsageBucket()
    for line in log_lines:
        usage = _parse_llm_usage_line(line)
        if usage is None:
            continue
        key = (usage.provider, usage.model)
        bucket = buckets.setdefault(key, _LLMUsageBucket())
        for target in (bucket, total):
            target.count += 1
            target.input_tokens += usage.input_tokens
            target.output_tokens += usage.output_tokens
            target.total_tokens += usage.total_tokens

    if total.count == 0:
        return "LLM 用量汇总：还没有 LLM 用量记录。"

    lines = [
        f"LLM 用量汇总：{total.count} 次调用",
        (
            "总计："
            f"input_tokens={total.input_tokens} "
            f"output_tokens={total.output_tokens} "
            f"total_tokens={total.total_tokens}"
        ),
        "按 provider/model：",
    ]
    for provider, model in sorted(buckets):
        bucket = buckets[(provider, model)]
        lines.append(
            f"- {provider} / {model}：{bucket.count} 次，"
            f"input_tokens={bucket.input_tokens} "
            f"output_tokens={bucket.output_tokens} "
            f"total_tokens={bucket.total_tokens}"
        )
    return "\n".join(lines)


def describe_llm_config_examples(provider: str = "") -> str:
    """输出不会包含真实密钥的 LLM 环境变量配置模板。"""

    normalized_provider = provider.strip().lower()
    sections = _llm_config_template_sections()
    if normalized_provider:
        template_provider = LLM_CONFIG_TEMPLATE_ALIASES.get(normalized_provider, normalized_provider)
        section = sections.get(template_provider)
        if section is None:
            return "\n".join(
                [
                    f"暂不支持配置模板 provider：{normalized_provider}",
                    "可用 provider：off、fake、openai、openai-compatible、qwen、gemini",
                    "如果厂商提供 OpenAI-compatible Responses 端点，可先使用 openai-compatible 模板。",
                ]
            )
        if template_provider != normalized_provider:
            section = section.replace(
                '$env:JARVIS_LITE_LLM_PROVIDER = "openai-compatible"',
                f'$env:JARVIS_LITE_LLM_PROVIDER = "{normalized_provider}"',
            )
            section = "\n".join(
                [
                    f"# {normalized_provider} 使用 OpenAI-compatible adapter",
                    "# base_url、model 和 API key 请以厂商官方控制台为准。",
                    section,
                ]
            )
        selected_sections = [section]
    else:
        selected_sections = list(sections.values())

    lines = [
        "LLM 配置模板",
        "这些示例只使用占位符，不会读取或保存真实 API key。",
        "PowerShell 示例：",
        "",
    ]
    lines.extend("\n\n".join(selected_sections).splitlines())
    lines.extend(
        [
            "",
            "配置后可运行：",
            'python src/app.py --once "/llm-status"',
            'python src/app.py --once "/llm-smoke 请用一句话确认连接可用"',
            'python src/app.py --once "/llm-usage"',
        ]
    )
    return "\n".join(lines)


def _llm_config_template_sections() -> dict[str, str]:
    return {
        "off": "\n".join(
            [
                "# 关闭 LLM 外脑",
                '$env:JARVIS_LITE_LLM_PROVIDER = "off"',
            ]
        ),
        "fake": "\n".join(
            [
                "# Fake provider，本地测试固定响应",
                '$env:JARVIS_LITE_LLM_PROVIDER = "fake"',
                '$env:JARVIS_LITE_LLM_FAKE_RESPONSE = \'{"type":"answer","answer":"测试回答"}\'',
            ]
        ),
        "openai": "\n".join(
            [
                "# OpenAI Responses API",
                '$env:JARVIS_LITE_LLM_PROVIDER = "openai"',
                '$env:JARVIS_LITE_LLM_MODEL = "<模型名>"',
                '$env:JARVIS_LITE_LLM_API_KEY = "<你的 API key>"',
                '$env:JARVIS_LITE_LLM_BASE_URL = ""',
            ]
        ),
        "openai-compatible": "\n".join(
            [
                "# OpenAI-compatible 端点",
                "# BASE_URL 可填 SDK base_url（通常到 /v1），也可直接粘贴完整 /v1/responses URL",
                '$env:JARVIS_LITE_LLM_PROVIDER = "openai-compatible"',
                '$env:JARVIS_LITE_LLM_MODEL = "<兼容端点模型名>"',
                '$env:JARVIS_LITE_LLM_API_KEY = "<你的 API key>"',
                '$env:JARVIS_LITE_LLM_BASE_URL = "<兼容端点 base_url 或完整 /v1/responses URL>"',
            ]
        ),
    }


def _normalize_llm_config_provider(provider: str = "") -> str:
    normalized_provider = provider.strip().lower() or "openai-compatible"
    if normalized_provider not in VALID_LLM_PROVIDERS:
        raise ValueError(
            f"暂不支持 LLM provider：{normalized_provider}。"
            "可用 provider：off、fake、openai、openai-compatible、qwen、gemini"
        )
    return normalized_provider


def _parse_llm_usage_line(line: str) -> LLMUsage | None:
    marker = "LLM 外脑用量："
    if marker not in line:
        return None
    fields: dict[str, str] = {}
    for item in line.split(marker, 1)[1].split():
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        fields[key] = value
    provider = fields.get("provider", "").strip()
    model = fields.get("model", "").strip()
    if not provider or not model:
        return None

    input_tokens = _usage_field_int(fields, "input_tokens")
    output_tokens = _usage_field_int(fields, "output_tokens")
    total_tokens = _usage_field_int(fields, "total_tokens")
    if total_tokens == 0:
        total_tokens = input_tokens + output_tokens
    return LLMUsage(
        provider=provider,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
    )


def _llm_env_setting_keys() -> dict[str, str]:
    return {
        "JARVIS_LITE_LLM_PROVIDER": "provider",
        "JARVIS_LITE_LLM_MODEL": "model",
        "JARVIS_LITE_LLM_BASE_URL": "base_url",
        "JARVIS_LITE_LLM_API_KEY": "api_key",
        "JARVIS_LITE_LLM_FAKE_RESPONSE": "fake_response",
    }


def _read_llm_local_config(paths: ProjectPaths | None) -> tuple[dict[str, str], str, str]:
    if paths is None:
        return {}, "", ""

    config_path = llm_local_config_path(paths)
    if not config_path.exists():
        return {}, "", ""

    source = _llm_config_source_label(paths, config_path)
    try:
        raw_payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, source, f"{source} 不是有效 JSON：{exc.msg}"
    except OSError as exc:
        return {}, source, f"{source} 读取失败：{exc}"

    if not isinstance(raw_payload, dict):
        return {}, source, f"{source} 必须是 JSON 对象"

    values: dict[str, str] = {}
    for key in ("provider", "model", "base_url", "api_key", "fake_response"):
        if key not in raw_payload or raw_payload[key] is None:
            continue
        value = raw_payload[key]
        if key == "fake_response" and not isinstance(value, str):
            values[key] = json.dumps(value, ensure_ascii=False)
        else:
            values[key] = str(value).strip()
    if "provider" in values:
        values["provider"] = values["provider"].lower() or "off"
    return values, source, ""


def _llm_config_source_label(paths: ProjectPaths, config_path: Path) -> str:
    try:
        return config_path.relative_to(paths.root).as_posix()
    except ValueError:
        return config_path.as_posix()


def _usage_field_int(fields: Mapping[str, str], key: str) -> int:
    try:
        return int(fields.get(key, "0"))
    except ValueError:
        return 0


def parse_llm_intent(raw_text: str) -> LLMIntent:
    """解析 provider 返回的 JSON，并收敛为项目内部结构。"""

    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        return LLMIntent(type="no_action", reason="LLM 返回内容不是有效 JSON")
    if not isinstance(payload, dict):
        return LLMIntent(type="no_action", reason="LLM 返回内容不是 JSON 对象")

    intent_type = str(payload.get("type") or payload.get("action") or "no_action").strip()
    if intent_type not in VALID_LLM_INTENT_TYPES:
        intent_type = "no_action"
    return LLMIntent(
        type=intent_type,
        command=str(payload.get("command") or "").strip(),
        answer=str(payload.get("answer") or "").strip(),
        clarification=str(payload.get("clarification") or payload.get("clarify") or "").strip(),
        reason=str(payload.get("reason") or "").strip(),
    )
