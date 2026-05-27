import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.llm import FakeLLMProvider, LLMIntent, LLMSettings, OpenAIResponsesProvider, build_llm_router


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

    def test_router_uses_openai_provider_from_settings(self):
        router = build_llm_router(LLMSettings(provider="openai", model="gpt-test", api_key="test-key"))

        self.assertIsInstance(router.provider, OpenAIResponsesProvider)
        self.assertIn("Provider：openai", router.describe())
        self.assertIn("Model：gpt-test", router.describe())


if __name__ == "__main__":
    unittest.main()
