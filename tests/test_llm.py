import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.llm import (
    FakeLLMProvider,
    LLMIntent,
    LLMSettings,
    LLMUsage,
    llm_local_config_path,
    OpenAIResponsesProvider,
    build_llm_router,
    describe_llm_config_examples,
    summarize_llm_usage,
)


class LLMTests(unittest.TestCase):
    def test_settings_default_to_off_provider(self):
        settings = LLMSettings.from_env({})

        self.assertEqual(settings.provider, "off")
        self.assertFalse(settings.enabled)

    def test_settings_read_provider_neutral_environment(self):
        settings = LLMSettings.from_env(
            {
                "JARVIS_LITE_LLM_PROVIDER": "fake",
                "JARVIS_LITE_LLM_MODEL": "intent-test-model",
                "JARVIS_LITE_LLM_BASE_URL": "https://example.test/v1",
                "JARVIS_LITE_LLM_API_KEY": "test-key",
                "JARVIS_LITE_LLM_FAKE_RESPONSE": '{"type":"answer","answer":"测试回答"}',
            }
        )

        self.assertEqual(settings.provider, "fake")
        self.assertEqual(settings.model, "intent-test-model")
        self.assertEqual(settings.base_url, "https://example.test/v1")
        self.assertEqual(settings.api_key, "test-key")
        self.assertEqual(settings.fake_response, '{"type":"answer","answer":"测试回答"}')

    def test_settings_read_local_config_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            config_path = llm_local_config_path(paths)
            config_path.write_text(
                json.dumps(
                    {
                        "provider": "openai-compatible",
                        "model": "compatible-model",
                        "base_url": "https://compatible.example/v1/responses",
                        "api_key": "local-config-key",
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            settings = LLMSettings.from_sources(paths, env={})

        self.assertEqual(settings.provider, "openai-compatible")
        self.assertEqual(settings.model, "compatible-model")
        self.assertEqual(settings.base_url, "https://compatible.example/v1/responses")
        self.assertEqual(settings.api_key, "local-config-key")
        self.assertIn("config/llm.local.json", settings.config_source)

    def test_environment_overrides_local_config_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            llm_local_config_path(paths).write_text(
                json.dumps(
                    {
                        "provider": "openai-compatible",
                        "model": "local-model",
                        "base_url": "https://local.example/v1",
                        "api_key": "local-key",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            settings = LLMSettings.from_sources(
                paths,
                env={
                    "JARVIS_LITE_LLM_PROVIDER": "fake",
                    "JARVIS_LITE_LLM_MODEL": "env-model",
                    "JARVIS_LITE_LLM_FAKE_RESPONSE": '{"type":"answer","answer":"env"}',
                },
            )

        self.assertEqual(settings.provider, "fake")
        self.assertEqual(settings.model, "env-model")
        self.assertEqual(settings.base_url, "https://local.example/v1")
        self.assertEqual(settings.api_key, "local-key")
        self.assertEqual(settings.fake_response, '{"type":"answer","answer":"env"}')

    def test_build_router_reads_local_config_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            llm_local_config_path(paths).write_text(
                json.dumps(
                    {
                        "provider": "fake",
                        "fake_response": '{"type":"answer","answer":"来自本地配置"}',
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            router = build_llm_router(paths=paths, env={})
            intent = router.complete_intent("随便聊聊", context=())

        self.assertIsNotNone(intent)
        self.assertEqual(intent.answer, "来自本地配置")

    def test_fake_provider_returns_command_intent_from_json(self):
        provider = FakeLLMProvider('{"type":"command","command":"/kb-summary","reason":"用户想总结资料"}')

        intent = provider.complete_intent("帮我看看资料整体情况", context=())

        self.assertEqual(intent, LLMIntent(type="command", command="/kb-summary", reason="用户想总结资料"))

    def test_fake_provider_returns_clarification_intent_from_json(self):
        provider = FakeLLMProvider('{"type":"clarify","clarification":"你想整理哪个目录？"}')

        intent = provider.complete_intent("帮我整理一下", context=())

        self.assertEqual(intent.type, "clarify")
        self.assertEqual(intent.clarification, "你想整理哪个目录？")

    def test_router_returns_none_when_provider_is_off(self):
        router = build_llm_router(LLMSettings(provider="off"))

        self.assertIsNone(router.complete_intent("随便聊聊", context=()))
        self.assertIn("LLM 外脑：未启用", router.describe())

    def test_router_uses_fake_provider_from_settings(self):
        router = build_llm_router(
            LLMSettings(
                provider="fake",
                fake_response='{"type":"answer","answer":"来自 fake provider"}',
            )
        )

        intent = router.complete_intent("无法本地处理的问题", context=())

        self.assertIsNotNone(intent)
        self.assertEqual(intent.type, "answer")
        self.assertEqual(intent.answer, "来自 fake provider")
        self.assertIn("Provider：fake", router.describe())

    def test_openai_provider_without_api_key_returns_no_action(self):
        provider = OpenAIResponsesProvider(LLMSettings(provider="openai", model="gpt-test"))

        intent = provider.complete_intent("需要外脑处理的问题", context=())

        self.assertEqual(intent.type, "no_action")
        self.assertIn("JARVIS_LITE_LLM_API_KEY", intent.reason)

    def test_openai_compatible_provider_requires_base_url(self):
        provider = OpenAIResponsesProvider(
            LLMSettings(provider="openai-compatible", model="compatible-model", api_key="test-key")
        )

        intent = provider.complete_intent("需要兼容端点处理的问题", context=())

        self.assertEqual(intent.type, "no_action")
        self.assertIn("JARVIS_LITE_LLM_BASE_URL", intent.reason)

    def test_openai_provider_without_sdk_returns_no_action(self):
        real_import = __import__

        def import_without_openai(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "openai":
                raise ImportError("missing openai")
            return real_import(name, globals, locals, fromlist, level)

        provider = OpenAIResponsesProvider(LLMSettings(provider="openai", model="gpt-test", api_key="test-key"))

        with patch("builtins.__import__", side_effect=import_without_openai):
            intent = provider.complete_intent("需要外脑处理的问题", context=())

        self.assertEqual(intent.type, "no_action")
        self.assertIn("OpenAI SDK", intent.reason)

    def test_openai_provider_parses_responses_output_text(self):
        calls = {}

        class FakeResponses:
            def create(self, **kwargs):
                calls["response_kwargs"] = kwargs
                return types.SimpleNamespace(output_text='{"type":"answer","answer":"来自 OpenAI provider"}')

        class FakeOpenAI:
            def __init__(self, **kwargs):
                calls["client_kwargs"] = kwargs
                self.responses = FakeResponses()

        fake_openai_module = types.ModuleType("openai")
        fake_openai_module.OpenAI = FakeOpenAI
        provider = OpenAIResponsesProvider(
            LLMSettings(
                provider="openai",
                model="gpt-test",
                base_url="https://example.test/v1",
                api_key="test-key",
            )
        )

        with patch.dict(sys.modules, {"openai": fake_openai_module}):
            intent = provider.complete_intent("需要外脑处理的问题", context=("记忆摘要：测试",))

        self.assertEqual(intent, LLMIntent(type="answer", answer="来自 OpenAI provider"))
        self.assertEqual(calls["client_kwargs"]["api_key"], "test-key")
        self.assertEqual(calls["client_kwargs"]["base_url"], "https://example.test/v1")
        self.assertEqual(calls["response_kwargs"]["model"], "gpt-test")
        self.assertIn("input", calls["response_kwargs"])
        self.assertIn("text", calls["response_kwargs"])

    def test_openai_provider_instructions_list_supported_agent_commands(self):
        calls = {}

        class FakeResponses:
            def create(self, **kwargs):
                calls["response_kwargs"] = kwargs
                return types.SimpleNamespace(output_text='{"type":"answer","answer":"来自 OpenAI provider"}')

        class FakeOpenAI:
            def __init__(self, **kwargs):
                self.responses = FakeResponses()

        fake_openai_module = types.ModuleType("openai")
        fake_openai_module.OpenAI = FakeOpenAI
        provider = OpenAIResponsesProvider(
            LLMSettings(provider="openai", model="gpt-test", api_key="test-key")
        )

        with patch.dict(sys.modules, {"openai": fake_openai_module}):
            provider.complete_intent("需要外脑处理的问题", context=())

        instructions = calls["response_kwargs"]["instructions"]
        self.assertIn("可返回的 Jarvis Lite 命令", instructions)
        self.assertIn("/kb-summary", instructions)
        self.assertIn("/ask 问题", instructions)
        self.assertIn("/config-manager-status", instructions)
        self.assertIn("/task-status", instructions)
        self.assertIn("/chrome-workflow-status", instructions)
        self.assertIn("/clash-workflow-status", instructions)
        self.assertIn("/messaging-workflow-status", instructions)
        self.assertIn("/idea-workflow-status", instructions)
        self.assertNotIn("/config-candidate-add", instructions)
        self.assertNotIn("/config-candidate-apply", instructions)
        self.assertNotIn("/config-candidate-confirm", instructions)
        self.assertNotIn("/config-candidate-undo", instructions)
        self.assertNotIn("/config-candidate-dismiss", instructions)
        self.assertNotIn("/config-candidate-history", instructions)
        self.assertNotIn("/config-candidate-restore", instructions)
        self.assertNotIn("/preference-status", instructions)
        self.assertNotIn("/preference-enable", instructions)
        self.assertNotIn("/preference-disable", instructions)
        self.assertNotIn("/preference-preview", instructions)
        self.assertNotIn("/preference-apply-draft", instructions)
        self.assertNotIn("/preference-apply-confirm", instructions)
        self.assertNotIn("/preference-apply-history", instructions)
        self.assertNotIn("/preference-apply-undo", instructions)
        self.assertNotIn("/preference-apply-status", instructions)
        self.assertNotIn("/preference-answer-types", instructions)
        self.assertNotIn("/preference-answer-type-enable", instructions)
        self.assertNotIn("/preference-answer-type-disable", instructions)
        self.assertNotIn("/preference-reply-context", instructions)
        self.assertNotIn("/preference-reply-context-enable", instructions)
        self.assertNotIn("/preference-reply-context-disable", instructions)
        self.assertNotIn("已确认偏好应用", instructions)
        self.assertNotIn("已确认偏好格式化", instructions)
        self.assertNotIn("/task-fail-capture", instructions)
        self.assertNotIn("/chrome-open URL", instructions)
        self.assertNotIn("/clash-open", instructions)
        self.assertNotIn("/qq-open", instructions)
        self.assertNotIn("/wechat-prepare-message", instructions)
        self.assertNotIn("/idea-open", instructions)
        self.assertNotIn("/idea-open-project", instructions)
        self.assertIn("不要返回列表之外的命令", instructions)

    def test_openai_provider_formats_401_error_without_leaking_api_key(self):
        class FakeAuthenticationError(Exception):
            status_code = 401

        class FakeResponses:
            def create(self, **kwargs):
                raise FakeAuthenticationError("bad key secret-test-key")

        class FakeOpenAI:
            def __init__(self, **kwargs):
                self.responses = FakeResponses()

        fake_openai_module = types.ModuleType("openai")
        fake_openai_module.OpenAI = FakeOpenAI
        provider = OpenAIResponsesProvider(
            LLMSettings(provider="openai", model="gpt-test", api_key="secret-test-key")
        )

        with patch.dict(sys.modules, {"openai": fake_openai_module}):
            intent = provider.complete_intent("需要外脑处理的问题", context=())

        self.assertEqual(intent.type, "no_action")
        self.assertIn("认证失败", intent.reason)
        self.assertIn("HTTP 401", intent.reason)
        self.assertIn("JARVIS_LITE_LLM_API_KEY", intent.reason)
        self.assertNotIn("secret-test-key", intent.reason)

    def test_openai_provider_formats_429_error_as_rate_or_quota_issue(self):
        class FakeRateLimitError(Exception):
            status_code = 429

        class FakeResponses:
            def create(self, **kwargs):
                raise FakeRateLimitError("rate limit")

        class FakeOpenAI:
            def __init__(self, **kwargs):
                self.responses = FakeResponses()

        fake_openai_module = types.ModuleType("openai")
        fake_openai_module.OpenAI = FakeOpenAI
        provider = OpenAIResponsesProvider(
            LLMSettings(provider="openai", model="gpt-test", api_key="test-key")
        )

        with patch.dict(sys.modules, {"openai": fake_openai_module}):
            intent = provider.complete_intent("需要外脑处理的问题", context=())

        self.assertEqual(intent.type, "no_action")
        self.assertIn("频率或额度", intent.reason)
        self.assertIn("HTTP 429", intent.reason)

    def test_openai_compatible_provider_normalizes_responses_endpoint_url(self):
        calls = {}

        class FakeResponses:
            def create(self, **kwargs):
                calls["response_kwargs"] = kwargs
                return types.SimpleNamespace(output_text='{"type":"answer","answer":"兼容端点正常"}')

        class FakeOpenAI:
            def __init__(self, **kwargs):
                calls["client_kwargs"] = kwargs
                self.responses = FakeResponses()

        fake_openai_module = types.ModuleType("openai")
        fake_openai_module.OpenAI = FakeOpenAI
        provider = OpenAIResponsesProvider(
            LLMSettings(
                provider="openai-compatible",
                model="gpt-test",
                base_url="https://compatible.example/v1/responses",
                api_key="test-key",
            )
        )

        with patch.dict(sys.modules, {"openai": fake_openai_module}):
            intent = provider.complete_intent("需要兼容端点处理的问题", context=())

        self.assertEqual(intent.answer, "兼容端点正常")
        self.assertEqual(calls["client_kwargs"]["base_url"], "https://compatible.example/v1")

    def test_router_describes_normalized_responses_endpoint_url(self):
        router = build_llm_router(
            LLMSettings(
                provider="openai-compatible",
                model="gpt-test",
                base_url="https://compatible.example/v1/responses/",
                api_key="test-key",
            )
        )

        description = router.describe()

        self.assertIn("Base URL：https://compatible.example/v1/responses/", description)
        self.assertIn("SDK Base URL：https://compatible.example/v1", description)

    def test_openai_provider_attaches_usage_from_response(self):
        class FakeResponses:
            def create(self, **kwargs):
                return types.SimpleNamespace(
                    output_text='{"type":"answer","answer":"带用量的回答"}',
                    usage=types.SimpleNamespace(input_tokens=12, output_tokens=5, total_tokens=17),
                )

        class FakeOpenAI:
            def __init__(self, **kwargs):
                self.responses = FakeResponses()

        fake_openai_module = types.ModuleType("openai")
        fake_openai_module.OpenAI = FakeOpenAI
        provider = OpenAIResponsesProvider(
            LLMSettings(provider="openai", model="gpt-test", api_key="test-key")
        )

        with patch.dict(sys.modules, {"openai": fake_openai_module}):
            intent = provider.complete_intent("需要外脑处理的问题", context=())

        self.assertEqual(intent.answer, "带用量的回答")
        self.assertEqual(
            intent.usage,
            LLMUsage(provider="openai", model="gpt-test", input_tokens=12, output_tokens=5, total_tokens=17),
        )

    def test_router_uses_openai_provider_from_settings(self):
        router = build_llm_router(LLMSettings(provider="openai", model="gpt-test", api_key="test-key"))

        self.assertIsInstance(router.provider, OpenAIResponsesProvider)
        self.assertIn("Provider：openai", router.describe())
        self.assertIn("Model：gpt-test", router.describe())
        self.assertIn("API key：已配置", router.describe())
        self.assertIn("网络调用：是", router.describe())

    def test_router_uses_openai_compatible_provider_from_settings(self):
        router = build_llm_router(
            LLMSettings(
                provider="openai-compatible",
                model="compatible-model",
                base_url="https://compatible.example/v1",
                api_key="test-key",
            )
        )

        self.assertIsInstance(router.provider, OpenAIResponsesProvider)
        self.assertIn("Provider：openai-compatible", router.describe())
        self.assertIn("Model：compatible-model", router.describe())
        self.assertIn("Base URL：https://compatible.example/v1", router.describe())
        self.assertIn("API key：已配置", router.describe())
        self.assertIn("网络调用：是", router.describe())

    def test_router_uses_qwen_alias_with_openai_compatible_adapter(self):
        router = build_llm_router(
            LLMSettings(
                provider="qwen",
                model="qwen-test",
                base_url="https://qwen.example/v1",
                api_key="test-key",
            )
        )

        self.assertIsInstance(router.provider, OpenAIResponsesProvider)
        self.assertIn("Provider：qwen", router.describe())
        self.assertIn("Adapter：openai-compatible", router.describe())
        self.assertIn("Base URL：https://qwen.example/v1", router.describe())
        self.assertIn("网络调用：是", router.describe())

    def test_gemini_alias_requires_openai_compatible_base_url(self):
        router = build_llm_router(LLMSettings(provider="gemini", model="gemini-test", api_key="test-key"))

        description = router.describe()

        self.assertIn("Provider：gemini", description)
        self.assertIn("Adapter：openai-compatible", description)
        self.assertIn("缺少 JARVIS_LITE_LLM_BASE_URL", description)
        self.assertIn("网络调用：否（配置未完成）", description)

    def test_router_describes_openai_missing_configuration(self):
        router = build_llm_router(LLMSettings(provider="openai"))

        description = router.describe()

        self.assertIn("API key：未配置", description)
        self.assertIn("网络调用：否（配置未完成）", description)
        self.assertIn("配置问题：", description)
        self.assertIn("缺少 JARVIS_LITE_LLM_MODEL", description)
        self.assertIn("缺少 JARVIS_LITE_LLM_API_KEY", description)

    def test_router_describes_fake_provider_as_local_no_network(self):
        router = build_llm_router(
            LLMSettings(provider="fake", fake_response='{"type":"answer","answer":"本地 fake"}')
        )

        description = router.describe()

        self.assertIn("Provider：fake", description)
        self.assertIn("API key：未配置", description)
        self.assertIn("网络调用：否（fake provider 本地响应）", description)

    def test_router_describes_openai_compatible_missing_base_url(self):
        router = build_llm_router(
            LLMSettings(provider="openai-compatible", model="compatible-model", api_key="test-key")
        )

        description = router.describe()

        self.assertIn("配置问题：", description)
        self.assertIn("缺少 JARVIS_LITE_LLM_BASE_URL", description)

    def test_router_describes_unknown_provider(self):
        router = build_llm_router(LLMSettings(provider="unknown-model-hub", model="test-model"))

        description = router.describe()

        self.assertIn("Provider：unknown-model-hub", description)
        self.assertIn("未知 provider：unknown-model-hub", description)

    def test_summarize_llm_usage_groups_local_log_records(self):
        summary = summarize_llm_usage(
            (
                "2026-05-27T12:00:00\trecord_log\t"
                "LLM 外脑用量：provider=openai model=gpt-4.1 input_tokens=10 output_tokens=4 total_tokens=14",
                "2026-05-27T12:01:00\trecord_log\t"
                "LLM 外脑用量：provider=openai model=gpt-4.1 input_tokens=6 output_tokens=2 total_tokens=8",
                "2026-05-27T12:02:00\trecord_log\t"
                "LLM 外脑用量：provider=openai-compatible model=qwen-test input_tokens=8 output_tokens=3 total_tokens=11",
                "2026-05-27T12:03:00\trecord_log\t普通日志",
            )
        )

        self.assertIn("LLM 用量汇总：3 次调用", summary)
        self.assertIn("总计：input_tokens=24 output_tokens=9 total_tokens=33", summary)
        self.assertIn("openai / gpt-4.1：2 次，input_tokens=16 output_tokens=6 total_tokens=22", summary)
        self.assertIn("openai-compatible / qwen-test：1 次，input_tokens=8 output_tokens=3 total_tokens=11", summary)

    def test_summarize_llm_usage_reports_empty_log(self):
        summary = summarize_llm_usage(())

        self.assertIn("还没有 LLM 用量记录", summary)

    def test_describe_llm_config_examples_lists_provider_templates(self):
        description = describe_llm_config_examples()

        self.assertIn("LLM 配置模板", description)
        self.assertIn('$env:JARVIS_LITE_LLM_PROVIDER = "openai"', description)
        self.assertIn('$env:JARVIS_LITE_LLM_PROVIDER = "openai-compatible"', description)
        self.assertIn('$env:JARVIS_LITE_LLM_API_KEY = "<你的 API key>"', description)
        self.assertIn("不会读取或保存真实 API key", description)
        self.assertIn('python src/app.py --once "/llm-smoke 请用一句话确认连接可用"', description)

    def test_describe_llm_config_examples_can_filter_provider(self):
        description = describe_llm_config_examples("openai-compatible")

        self.assertIn("OpenAI-compatible 端点", description)
        self.assertIn("JARVIS_LITE_LLM_BASE_URL", description)
        self.assertIn("完整 /v1/responses URL", description)
        self.assertNotIn("Fake provider", description)

    def test_describe_llm_config_examples_maps_model_hub_alias_to_compatible_template(self):
        description = describe_llm_config_examples("qwen")

        self.assertIn("qwen 使用 OpenAI-compatible adapter", description)
        self.assertIn('$env:JARVIS_LITE_LLM_PROVIDER = "qwen"', description)
        self.assertIn("JARVIS_LITE_LLM_BASE_URL", description)

    def test_describe_llm_config_examples_maps_gemini_alias_to_compatible_template(self):
        description = describe_llm_config_examples("gemini")

        self.assertIn("gemini 使用 OpenAI-compatible adapter", description)
        self.assertIn('$env:JARVIS_LITE_LLM_PROVIDER = "gemini"', description)
        self.assertIn("JARVIS_LITE_LLM_BASE_URL", description)

    def test_describe_llm_config_examples_reports_unknown_provider(self):
        description = describe_llm_config_examples("unknown-model-hub")

        self.assertIn("暂不支持配置模板 provider：unknown-model-hub", description)
        self.assertIn("openai-compatible", description)


if __name__ == "__main__":
    unittest.main()
