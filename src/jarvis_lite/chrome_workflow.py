from __future__ import annotations

import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode, urlparse

from .app_registry import RegisteredApp, match_registered_app
from .config import ProjectPaths


ChromeOpenExecutor = Callable[[Path, str], None]


@dataclass(frozen=True)
class ChromeOpenResult:
    app: RegisteredApp
    alias: str
    path: Path
    url: str
    executed_at: datetime


def describe_chrome_workflow_status(paths: ProjectPaths) -> str:
    """输出 Chrome 工作流第一阶段边界。"""

    match = match_registered_app(paths, "chrome")
    launch_path = match.app.launch_path if match is not None else None
    path_status = str(launch_path) if launch_path is not None else "未找到，可在 config/apps.local.json 配置 chrome.path"
    return "\n".join(
        [
            "Chrome 工作流状态：第一阶段",
            "- 当前能力：/chrome-open URL、/chrome-search 关键词",
            f"- Chrome 路径：{path_status}",
            "- 执行动作：只把 URL 交给 Chrome 启动参数。",
            "- 边界：不读取网页、不点击页面、不输入页面内容、不自动截图或保存资料。",
        ]
    )


def normalize_chrome_url(raw_url: str) -> str:
    """把用户显式 URL 规范化为 Chrome 可打开的 http/https URL。"""

    target = raw_url.strip()
    if not target:
        raise ValueError("URL 不能为空。")
    if any(character.isspace() for character in target):
        raise ValueError("URL 不能包含空白字符。")
    if "://" in target and not (target.startswith("http://") or target.startswith("https://")):
        raise ValueError("只支持 http/https URL。")
    if "://" not in target:
        target = f"https://{target}"

    parsed = urlparse(target)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL 格式无效，请提供明确网页地址。")
    return target


def build_chrome_search_url(query: str) -> str:
    """构造 Chrome 第一阶段使用的搜索 URL。"""

    normalized_query = query.strip()
    if not normalized_query:
        raise ValueError("搜索关键词不能为空。")
    return "https://www.google.com/search?" + urlencode({"q": normalized_query})


def open_chrome_url(
    paths: ProjectPaths,
    raw_url: str,
    *,
    executor: ChromeOpenExecutor | None = None,
) -> ChromeOpenResult:
    """使用 AppRegistry 中的 Chrome 路径打开一个明确 URL。"""

    url = normalize_chrome_url(raw_url)
    match = match_registered_app(paths, "chrome")
    if match is None:
        raise FileNotFoundError("Chrome 未登记。可用 /apps 查看应用注册表。")

    launch_path = match.app.launch_path
    if launch_path is None:
        raise FileNotFoundError("Chrome 启动路径未找到。可在 config/apps.local.json 配置 chrome.path。")

    launcher = executor or _launch_chrome_with_subprocess
    launcher(launch_path, url)
    return ChromeOpenResult(
        app=match.app,
        alias=match.alias,
        path=launch_path,
        url=url,
        executed_at=datetime.now(),
    )


def describe_chrome_open(
    paths: ProjectPaths,
    raw_url: str,
    *,
    executor: ChromeOpenExecutor | None = None,
) -> str:
    result = open_chrome_url(paths, raw_url, executor=executor)
    return "\n".join(
        [
            "Chrome 打开网页执行：",
            f"应用：{result.app.display_name} ({result.app.app_id})",
            f"路径：{result.path}",
            f"URL：{result.url}",
            f"时间：{result.executed_at.isoformat(timespec='seconds')}",
            "说明：当前阶段只打开网页，不读取网页、不点击页面、不输入页面内容。",
        ]
    )


def describe_chrome_search(
    paths: ProjectPaths,
    query: str,
    *,
    executor: ChromeOpenExecutor | None = None,
) -> str:
    search_url = build_chrome_search_url(query)
    result = open_chrome_url(paths, search_url, executor=executor)
    return "\n".join(
        [
            "Chrome 搜索执行：",
            f"关键词：{query.strip()}",
            f"路径：{result.path}",
            f"URL：{result.url}",
            f"时间：{result.executed_at.isoformat(timespec='seconds')}",
            "说明：当前阶段只打开搜索结果页，不读取网页、不点击页面、不输入页面内容。",
        ]
    )


def _launch_chrome_with_subprocess(path: Path, url: str) -> None:
    try:
        subprocess.Popen([str(path), url], cwd=str(path.parent))
    except OSError as exc:
        raise RuntimeError(f"Chrome 启动失败：{path}：{exc}") from exc
