from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Protocol

from .config import ProjectPaths


VALID_SEARCH_PROVIDERS = {"off", "fake", "tavily"}
SEARCH_LOCAL_CONFIG_RELATIVE_PATH = Path("config") / "search.local.json"
SEARCH_EXAMPLE_CONFIG_RELATIVE_PATH = Path("config") / "search.example.json"
DEFAULT_SEARCH_MAX_RESULTS = 5


@dataclass(frozen=True)
class SearchResult:
    """联网搜索返回给 Agent 的单条来源结果。"""

    title: str
    url: str
    snippet: str = ""
    source: str = ""


@dataclass(frozen=True)
class SearchResponse:
    """一次搜索调用的结构化结果。"""

    query: str
    results: tuple[SearchResult, ...] = ()
    error: str = ""


@dataclass(frozen=True)
class SearchSettings:
    """保存联网搜索 provider 配置。"""

    provider: str = "off"
    api_key: str = ""
    base_url: str = ""
    max_results: int = DEFAULT_SEARCH_MAX_RESULTS
    fake_results: tuple[SearchResult, ...] = ()
    config_source: str = ""
    config_error: str = ""

    @property
    def enabled(self) -> bool:
        return self.provider != "off"

    def configuration_issues(self) -> tuple[str, ...]:
        issues: list[str] = []
        if self.config_error:
            issues.append(self.config_error)
        if self.provider not in VALID_SEARCH_PROVIDERS:
            issues.append(f"未知 provider：{self.provider}")
            return tuple(issues)
        if not self.enabled or self.provider == "fake":
            return tuple(issues)
        if self.provider == "tavily" and not self.api_key:
            issues.append("缺少 JARVIS_LITE_SEARCH_API_KEY")
        if self.max_results < 1:
            issues.append("JARVIS_LITE_SEARCH_MAX_RESULTS 必须大于 0")
        return tuple(issues)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "SearchSettings":
        values = env if env is not None else os.environ
        source = "environment" if any(key in values for key in _search_env_setting_keys()) else ""
        fake_results, fake_results_error = _parse_fake_results(values.get("JARVIS_LITE_SEARCH_FAKE_RESULTS", ""))
        config_error = fake_results_error
        return cls(
            provider=values.get("JARVIS_LITE_SEARCH_PROVIDER", "off").strip().lower() or "off",
            api_key=values.get("JARVIS_LITE_SEARCH_API_KEY", "").strip(),
            base_url=values.get("JARVIS_LITE_SEARCH_BASE_URL", "").strip(),
            max_results=_parse_max_results(values.get("JARVIS_LITE_SEARCH_MAX_RESULTS", ""), DEFAULT_SEARCH_MAX_RESULTS),
            fake_results=fake_results,
            config_source=source,
            config_error=config_error,
        )

    @classmethod
    def from_sources(
        cls,
        paths: ProjectPaths | None = None,
        env: Mapping[str, str] | None = None,
    ) -> "SearchSettings":
        """按本地配置文件 + 环境变量覆盖的顺序读取搜索配置。"""

        config_values, config_source, config_error = _read_search_local_config(paths)
        env_values = env if env is not None else os.environ
        values = dict(config_values)
        env_used = False
        for env_key, setting_key in _search_env_setting_keys().items():
            if env_key not in env_values:
                continue
            values[setting_key] = str(env_values.get(env_key, "")).strip()
            env_used = True

        provider = str(values.get("provider") or "off").strip().lower() or "off"
        max_results = _parse_max_results(values.get("max_results"), DEFAULT_SEARCH_MAX_RESULTS)
        fake_results, fake_results_error = _fake_results_from_value(values.get("fake_results"))
        source = config_source
        if env_used:
            source = "environment" if not source else f"environment + {source}"
        return cls(
            provider=provider,
            api_key=str(values.get("api_key") or "").strip(),
            base_url=str(values.get("base_url") or "").strip(),
            max_results=max_results,
            fake_results=fake_results,
            config_source=source,
            config_error=config_error or fake_results_error,
        )


class SearchProvider(Protocol):
    """联网搜索 provider 的统一接口。"""

    name: str

    def search(self, query: str, max_results: int) -> SearchResponse:
        """返回结构化搜索结果。"""


class FakeSearchProvider:
    """用于测试的本地固定搜索 provider。"""

    name = "fake"

    def __init__(self, results: tuple[SearchResult, ...] = ()):
        self.results = results
        self.calls: list[str] = []

    def search(self, query: str, max_results: int) -> SearchResponse:
        self.calls.append(query)
        return SearchResponse(query=query, results=self.results[:max_results])


class TavilySearchProvider:
    """使用 Tavily 官方 Python SDK 的联网搜索 provider。"""

    name = "tavily"

    def __init__(self, settings: SearchSettings):
        self.settings = settings

    def search(self, query: str, max_results: int) -> SearchResponse:
        if not self.settings.api_key:
            return SearchResponse(query=query, error="Tavily 搜索未配置 JARVIS_LITE_SEARCH_API_KEY")

        client_class = self._tavily_client_class()
        if client_class is None:
            return SearchResponse(query=query, error="Tavily SDK 未安装，请先安装项目依赖")

        try:
            client_kwargs = {"api_key": self.settings.api_key}
            if self.settings.base_url:
                client_kwargs["api_base_url"] = self.settings.base_url
            client = client_class(**client_kwargs)
            response = client.search(query=query, max_results=max_results)
        except Exception as exc:
            return SearchResponse(query=query, error=self._format_call_error(exc))

        return SearchResponse(query=query, results=self._parse_results(response, max_results))

    def _tavily_client_class(self):
        try:
            from tavily import TavilyClient
        except ImportError:
            return None
        return TavilyClient

    def _parse_results(self, response: object, max_results: int) -> tuple[SearchResult, ...]:
        raw_results = self._item_value(response, "results")
        if not isinstance(raw_results, list):
            return ()

        results: list[SearchResult] = []
        for raw_result in raw_results:
            title = str(self._item_value(raw_result, "title") or "").strip()
            url = str(self._item_value(raw_result, "url") or "").strip()
            snippet = str(
                self._item_value(raw_result, "content")
                or self._item_value(raw_result, "snippet")
                or self._item_value(raw_result, "description")
                or ""
            ).strip()
            if not title and url:
                title = url
            if not title or not url:
                continue
            results.append(SearchResult(title=title, url=url, snippet=snippet, source=self.name))
            if len(results) >= max_results:
                break
        return tuple(results)

    def _item_value(self, item: object, key: str):
        if isinstance(item, dict):
            return item.get(key)
        return getattr(item, key, None)

    def _format_call_error(self, exc: Exception) -> str:
        message = str(exc).strip()
        if self.settings.api_key:
            message = message.replace(self.settings.api_key, "<redacted>")
        if message:
            return f"Tavily 搜索调用失败：{message}"
        return "Tavily 搜索调用失败：未知错误"


class SearchRouter:
    """负责选择联网搜索 provider，并向 JarvisAgent 暴露稳定接口。"""

    def __init__(self, settings: SearchSettings, provider: SearchProvider | None = None):
        self.settings = settings
        self.provider = provider

    def search(self, query: str) -> SearchResponse:
        normalized_query = query.strip()
        if not normalized_query:
            return SearchResponse(query=query, error="搜索关键词不能为空")
        if not self.settings.enabled or self.provider is None:
            return SearchResponse(query=normalized_query, error="联网搜索未启用。可先运行 /search-enable。")
        issues = self.settings.configuration_issues()
        if issues:
            return SearchResponse(query=normalized_query, error="联网搜索配置未完成：" + "；".join(issues))
        return self.provider.search(normalized_query, self.settings.max_results)

    def describe(self) -> str:
        issues = self.settings.configuration_issues()
        status = "已启用" if self.settings.enabled else "未启用"
        lines = [
            f"联网搜索：{status}",
            f"- Provider：{self.settings.provider}",
        ]
        if self.settings.config_source:
            lines.append(f"- 配置来源：{self.settings.config_source}")
        if self.settings.base_url:
            lines.append(f"- Base URL：{self.settings.base_url}")
        lines.append(f"- Max results：{self.settings.max_results}")
        lines.append(f"- API key：{self._api_key_status()}")
        lines.append(f"- 网络调用：{self._network_call_status(issues)}")
        if issues:
            lines.append("- 配置问题：")
            for issue in issues:
                lines.append(f"  - {issue}")
        elif self.settings.enabled:
            lines.append("- 配置：可调用")
        return "\n".join(lines)

    def _api_key_status(self) -> str:
        return "已配置" if self.settings.api_key else "未配置"

    def _network_call_status(self, issues: tuple[str, ...]) -> str:
        if not self.settings.enabled:
            return "否（联网搜索未启用）"
        if self.settings.provider == "fake":
            return "否（fake provider 本地结果）"
        if issues:
            return "否（配置未完成）"
        if self.settings.provider == "tavily":
            return "是（/search 会调用 provider）"
        return "否（provider 不支持）"


def build_search_router(
    settings: SearchSettings | None = None,
    paths: ProjectPaths | None = None,
    env: Mapping[str, str] | None = None,
) -> SearchRouter:
    """根据配置构建联网搜索 Router。"""

    resolved_settings = settings or SearchSettings.from_sources(paths, env)
    if not resolved_settings.enabled:
        return SearchRouter(resolved_settings)
    if resolved_settings.provider == "fake":
        return SearchRouter(resolved_settings, FakeSearchProvider(resolved_settings.fake_results))
    if resolved_settings.provider == "tavily":
        return SearchRouter(resolved_settings, TavilySearchProvider(resolved_settings))
    return SearchRouter(resolved_settings)


def search_local_config_path(paths: ProjectPaths) -> Path:
    """返回真实搜索本地配置文件路径。"""

    return paths.config_dir / SEARCH_LOCAL_CONFIG_RELATIVE_PATH.name


def search_example_config_path(paths: ProjectPaths) -> Path:
    """返回搜索配置模板文件路径。"""

    return paths.config_dir / SEARCH_EXAMPLE_CONFIG_RELATIVE_PATH.name


def write_search_example_config(paths: ProjectPaths) -> Path:
    """确保运行态目录里有一份不会包含真实密钥的搜索配置模板。"""

    target = search_example_config_path(paths)
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text(search_example_config_text(), encoding="utf-8")
    return target


def search_example_config_text() -> str:
    """返回 JSON 模板文本；真实配置应复制到 search.local.json。"""

    payload = {
        "provider": "tavily",
        "api_key": "<你的搜索 API key>",
        "base_url": "",
        "max_results": DEFAULT_SEARCH_MAX_RESULTS,
        "fake_results": [],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def describe_search_config_examples(provider: str = "") -> str:
    """输出不会包含真实密钥的联网搜索环境变量配置模板。"""

    normalized_provider = provider.strip().lower()
    sections = _search_config_template_sections()
    if normalized_provider:
        section = sections.get(normalized_provider)
        if section is None:
            return "\n".join(
                [
                    f"暂不支持搜索配置模板 provider：{normalized_provider}",
                    "可用 provider：off、fake、tavily",
                ]
            )
        selected_sections = [section]
    else:
        selected_sections = list(sections.values())

    lines = [
        "联网搜索配置模板",
        "这些示例只使用占位符，不会读取或保存真实 API key。",
        "PowerShell 示例：",
        "",
    ]
    lines.extend("\n\n".join(selected_sections).splitlines())
    lines.extend(
        [
            "",
            "配置后可运行：",
            'python src/app.py --once "/search-status"',
            'python src/app.py --once "/search Python 版本"',
            'python src/app.py --once "/search-enable"',
        ]
    )
    return "\n".join(lines)


def _search_config_template_sections() -> dict[str, str]:
    return {
        "off": "\n".join(
            [
                "# 关闭联网搜索",
                '$env:JARVIS_LITE_SEARCH_PROVIDER = "off"',
            ]
        ),
        "fake": "\n".join(
            [
                "# Fake provider，本地测试固定搜索结果",
                '$env:JARVIS_LITE_SEARCH_PROVIDER = "fake"',
                '$env:JARVIS_LITE_SEARCH_FAKE_RESULTS = \'[{"title":"测试结果","url":"https://example.test","snippet":"本地测试摘要"}]\'',
            ]
        ),
        "tavily": "\n".join(
            [
                "# Tavily Search API",
                '$env:JARVIS_LITE_SEARCH_PROVIDER = "tavily"',
                '$env:JARVIS_LITE_SEARCH_API_KEY = "<你的搜索 API key>"',
                '$env:JARVIS_LITE_SEARCH_BASE_URL = ""',
                '$env:JARVIS_LITE_SEARCH_MAX_RESULTS = "5"',
            ]
        ),
    }


def _search_env_setting_keys() -> dict[str, str]:
    return {
        "JARVIS_LITE_SEARCH_PROVIDER": "provider",
        "JARVIS_LITE_SEARCH_API_KEY": "api_key",
        "JARVIS_LITE_SEARCH_BASE_URL": "base_url",
        "JARVIS_LITE_SEARCH_MAX_RESULTS": "max_results",
        "JARVIS_LITE_SEARCH_FAKE_RESULTS": "fake_results",
    }


def _read_search_local_config(paths: ProjectPaths | None) -> tuple[dict[str, object], str, str]:
    if paths is None:
        return {}, "", ""

    config_path = search_local_config_path(paths)
    if not config_path.exists():
        return {}, "", ""

    source = _search_config_source_label(paths, config_path)
    try:
        raw_payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, source, f"{source} 不是有效 JSON：{exc.msg}"
    except OSError as exc:
        return {}, source, f"{source} 读取失败：{exc}"

    if not isinstance(raw_payload, dict):
        return {}, source, f"{source} 必须是 JSON 对象"

    values: dict[str, object] = {}
    for key in ("provider", "api_key", "base_url", "max_results", "fake_results"):
        if key not in raw_payload or raw_payload[key] is None:
            continue
        value = raw_payload[key]
        if key == "provider":
            values[key] = str(value).strip().lower() or "off"
        elif key in {"api_key", "base_url"}:
            values[key] = str(value).strip()
        else:
            values[key] = value
    return values, source, ""


def _search_config_source_label(paths: ProjectPaths, config_path: Path) -> str:
    try:
        return config_path.relative_to(paths.root).as_posix()
    except ValueError:
        return config_path.as_posix()


def _parse_max_results(value: object, default: int) -> int:
    if value in (None, ""):
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return max(parsed, 1)


def _fake_results_from_value(value: object) -> tuple[tuple[SearchResult, ...], str]:
    if value in (None, ""):
        return (), ""
    if isinstance(value, str):
        return _parse_fake_results(value)
    if isinstance(value, list):
        return _fake_results_from_list(value), ""
    return (), "fake_results 必须是 JSON 数组"


def _parse_fake_results(raw_value: str) -> tuple[tuple[SearchResult, ...], str]:
    if not raw_value.strip():
        return (), ""
    try:
        payload = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        return (), f"JARVIS_LITE_SEARCH_FAKE_RESULTS 不是有效 JSON：{exc.msg}"
    if not isinstance(payload, list):
        return (), "JARVIS_LITE_SEARCH_FAKE_RESULTS 必须是 JSON 数组"
    return _fake_results_from_list(payload), ""


def _fake_results_from_list(payload: list[object]) -> tuple[SearchResult, ...]:
    results: list[SearchResult] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "").strip()
        url = str(item.get("url") or "").strip()
        snippet = str(item.get("snippet") or item.get("content") or "").strip()
        source = str(item.get("source") or "fake").strip()
        if not title or not url:
            continue
        results.append(SearchResult(title=title, url=url, snippet=snippet, source=source))
    return tuple(results)
