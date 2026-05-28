import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from jarvis_lite.config import build_project_paths
from jarvis_lite.search import (
    FakeSearchProvider,
    SearchResult,
    SearchRouter,
    SearchSettings,
    TavilySearchProvider,
    build_search_router,
    describe_search_config_examples,
    search_local_config_path,
)


class SearchTests(unittest.TestCase):
    def test_settings_default_to_off_provider(self):
        settings = SearchSettings.from_env({})

        self.assertEqual(settings.provider, "off")
        self.assertFalse(settings.enabled)

    def test_settings_read_local_config_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            search_local_config_path(paths).write_text(
                json.dumps(
                    {
                        "provider": "tavily",
                        "api_key": "local-search-key",
                        "base_url": "https://search.example/api",
                        "max_results": 3,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            settings = SearchSettings.from_sources(paths, env={})

        self.assertEqual(settings.provider, "tavily")
        self.assertEqual(settings.api_key, "local-search-key")
        self.assertEqual(settings.base_url, "https://search.example/api")
        self.assertEqual(settings.max_results, 3)
        self.assertIn("config/search.local.json", settings.config_source)

    def test_environment_overrides_local_config_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            search_local_config_path(paths).write_text(
                json.dumps(
                    {
                        "provider": "tavily",
                        "api_key": "local-search-key",
                        "base_url": "https://local.example/api",
                        "max_results": 2,
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            settings = SearchSettings.from_sources(
                paths,
                env={
                    "JARVIS_LITE_SEARCH_PROVIDER": "fake",
                    "JARVIS_LITE_SEARCH_MAX_RESULTS": "4",
                    "JARVIS_LITE_SEARCH_FAKE_RESULTS": json.dumps(
                        [
                            {
                                "title": "Env Result",
                                "url": "https://env.example/result",
                                "snippet": "来自环境变量的搜索结果",
                            }
                        ],
                        ensure_ascii=False,
                    ),
                },
            )

        self.assertEqual(settings.provider, "fake")
        self.assertEqual(settings.api_key, "local-search-key")
        self.assertEqual(settings.base_url, "https://local.example/api")
        self.assertEqual(settings.max_results, 4)
        self.assertEqual(settings.fake_results[0].title, "Env Result")

    def test_build_router_reads_fake_results_from_local_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = build_project_paths(Path(temp_dir) / "jarvis-lite")
            search_local_config_path(paths).write_text(
                json.dumps(
                    {
                        "provider": "fake",
                        "fake_results": [
                            {
                                "title": "Python 3.13 release",
                                "url": "https://python.example/3-13",
                                "snippet": "Python 3.13 是当前测试结果。",
                            }
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            router = build_search_router(paths=paths, env={})
            response = router.search("Python 版本")

        self.assertEqual(response.query, "Python 版本")
        self.assertEqual(response.error, "")
        self.assertEqual(len(response.results), 1)
        self.assertEqual(response.results[0].url, "https://python.example/3-13")

    def test_router_describe_does_not_leak_api_key(self):
        router = build_search_router(
            SearchSettings(
                provider="tavily",
                api_key="secret-search-key",
                max_results=5,
            )
        )

        description = router.describe()

        self.assertIn("联网搜索：已启用", description)
        self.assertIn("Provider：tavily", description)
        self.assertIn("API key：已配置", description)
        self.assertIn("网络调用：是", description)
        self.assertNotIn("secret-search-key", description)

    def test_router_reports_missing_tavily_api_key(self):
        router = build_search_router(SearchSettings(provider="tavily"))

        description = router.describe()

        self.assertIn("配置问题：", description)
        self.assertIn("缺少 JARVIS_LITE_SEARCH_API_KEY", description)
        self.assertIn("网络调用：否（配置未完成）", description)

    def test_fake_provider_returns_limited_structured_results(self):
        provider = FakeSearchProvider(
            (
                SearchResult("第一条", "https://example.test/1", "摘要 1", "fake"),
                SearchResult("第二条", "https://example.test/2", "摘要 2", "fake"),
            )
        )
        router = SearchRouter(SearchSettings(provider="fake", max_results=1), provider)

        response = router.search("测试查询")

        self.assertEqual(provider.calls, ["测试查询"])
        self.assertEqual(len(response.results), 1)
        self.assertEqual(response.results[0].title, "第一条")

    def test_tavily_provider_without_sdk_returns_readable_error(self):
        real_import = __import__

        def import_without_tavily(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "tavily":
                raise ImportError("missing tavily")
            return real_import(name, globals, locals, fromlist, level)

        provider = TavilySearchProvider(
            SearchSettings(provider="tavily", api_key="test-key", base_url="https://search.example/api")
        )

        with patch("builtins.__import__", side_effect=import_without_tavily):
            response = provider.search("Python 版本", max_results=3)

        self.assertIn("Tavily SDK 未安装", response.error)
        self.assertEqual(response.results, ())

    def test_tavily_provider_parses_sdk_results(self):
        calls = {}

        class FakeTavilyClient:
            def __init__(self, **kwargs):
                calls["client_kwargs"] = kwargs

            def search(self, **kwargs):
                calls["search_kwargs"] = kwargs
                return {
                    "results": [
                        {
                            "title": "Python release",
                            "url": "https://python.example/release",
                            "content": "Python 发布信息摘要。",
                        }
                    ]
                }

        fake_tavily_module = types.ModuleType("tavily")
        fake_tavily_module.TavilyClient = FakeTavilyClient
        provider = TavilySearchProvider(
            SearchSettings(provider="tavily", api_key="test-key", base_url="https://search.example/api")
        )

        with patch.dict(sys.modules, {"tavily": fake_tavily_module}):
            response = provider.search("Python 版本", max_results=2)

        self.assertEqual(calls["client_kwargs"]["api_key"], "test-key")
        self.assertEqual(calls["client_kwargs"]["api_base_url"], "https://search.example/api")
        self.assertEqual(calls["search_kwargs"]["query"], "Python 版本")
        self.assertEqual(calls["search_kwargs"]["max_results"], 2)
        self.assertEqual(response.results[0].title, "Python release")
        self.assertEqual(response.results[0].snippet, "Python 发布信息摘要。")

    def test_describe_search_config_examples_lists_templates(self):
        description = describe_search_config_examples()

        self.assertIn("联网搜索配置模板", description)
        self.assertIn('$env:JARVIS_LITE_SEARCH_PROVIDER = "tavily"', description)
        self.assertIn('$env:JARVIS_LITE_SEARCH_API_KEY = "<你的搜索 API key>"', description)
        self.assertIn('python src/app.py --once "/search-status"', description)


if __name__ == "__main__":
    unittest.main()
