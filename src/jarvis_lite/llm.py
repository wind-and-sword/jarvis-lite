from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Mapping, Protocol


VALID_LLM_INTENT_TYPES = {"command", "answer", "clarify", "no_action"}
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

    @property
    def enabled(self) -> bool:
        return self.provider != "off"

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "LLMSettings":
        values = env if env is not None else os.environ
        return cls(
            provider=values.get("JARVIS_LITE_LLM_PROVIDER", "off").strip().lower() or "off",
            model=values.get("JARVIS_LITE_LLM_MODEL", "").strip(),
            base_url=values.get("JARVIS_LITE_LLM_BASE_URL", "").strip(),
            api_key=values.get("JARVIS_LITE_LLM_API_KEY", "").strip(),
            fake_response=values.get("JARVIS_LITE_LLM_FAKE_RESPONSE", "").strip(),
        )


@dataclass(frozen=True)
class LLMIntent:
    """LLM 外脑返回给本地 Agent 的结构化意图。"""

    type: str
    command: str = ""
    answer: str = ""
    clarification: str = ""
    reason: str = ""


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
    """使用 OpenAI Responses API 的 provider 适配器。"""

    name = "openai"

    def __init__(self, settings: LLMSettings):
        self.settings = settings

    def complete_intent(self, prompt: str, context: tuple[str, ...]) -> LLMIntent:
        if not self.settings.api_key:
            return LLMIntent(type="no_action", reason="未配置 JARVIS_LITE_LLM_API_KEY")
        if not self.settings.model:
            return LLMIntent(type="no_action", reason="未配置 JARVIS_LITE_LLM_MODEL")

        client_class = self._openai_client_class()
        if client_class is None:
            return LLMIntent(type="no_action", reason="OpenAI SDK 未安装，请先安装项目依赖")

        client_kwargs = {"api_key": self.settings.api_key}
        if self.settings.base_url:
            client_kwargs["base_url"] = self.settings.base_url

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
            return LLMIntent(type="no_action", reason=f"OpenAI provider 调用失败：{exc}")

        raw_text = self._response_text(response)
        if not raw_text:
            return LLMIntent(type="no_action", reason="OpenAI Responses API 未返回文本内容")
        return parse_llm_intent(raw_text)

    def _openai_client_class(self):
        try:
            from openai import OpenAI
        except ImportError:
            return None
        return OpenAI

    def _instructions(self) -> str:
        return "\n".join(
            [
                "你是 Jarvis Lite 的 LLM 外脑，只能返回结构化意图。",
                "本地 Agent 会先处理命令、身份、本地自然语言意图和知识库问答。",
                "当适合调用本地能力时返回 command，command 必须是一个以 / 开头的 Jarvis Lite 命令。",
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

    def _item_value(self, item, key: str):
        if isinstance(item, dict):
            return item.get(key)
        return getattr(item, key, None)


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
        if not self.settings.enabled:
            return "LLM 外脑：未启用"
        lines = [
            "LLM 外脑：已启用",
            f"- Provider：{self.settings.provider}",
        ]
        if self.settings.model:
            lines.append(f"- Model：{self.settings.model}")
        return "\n".join(lines)


def build_llm_router(settings: LLMSettings | None = None) -> LLMRouter:
    """根据通用配置构建 LLM Router。"""

    resolved_settings = settings or LLMSettings.from_env()
    if not resolved_settings.enabled:
        return LLMRouter(resolved_settings)
    if resolved_settings.provider == "fake":
        return LLMRouter(resolved_settings, FakeLLMProvider(resolved_settings.fake_response))
    if resolved_settings.provider == "openai":
        return LLMRouter(resolved_settings, OpenAIResponsesProvider(resolved_settings))
    return LLMRouter(resolved_settings)


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
