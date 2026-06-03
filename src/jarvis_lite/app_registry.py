from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

from .config import ProjectPaths


APP_REGISTRY_FILENAME = "apps.local.json"


@dataclass(frozen=True)
class RegisteredApp:
    app_id: str
    display_name: str
    aliases: tuple[str, ...]
    executable_candidates: tuple[Path, ...]
    configured_path: Path | None = None

    @property
    def launch_path(self) -> Path | None:
        candidates = ((self.configured_path,) if self.configured_path is not None else ()) + self.executable_candidates
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None


@dataclass(frozen=True)
class RegisteredAppMatch:
    app: RegisteredApp
    alias: str


def list_registered_apps(paths: ProjectPaths) -> tuple[RegisteredApp, ...]:
    """读取 1.0 首批常用应用注册表。"""

    overrides = _read_local_registry(paths)
    apps: list[RegisteredApp] = []
    for builtin in _builtin_apps():
        override = overrides.get(builtin.app_id, {})
        apps.append(
            RegisteredApp(
                app_id=builtin.app_id,
                display_name=builtin.display_name,
                aliases=_merge_aliases(builtin.aliases, override.get("aliases")),
                executable_candidates=builtin.executable_candidates,
                configured_path=_configured_path(override),
            )
        )
    return tuple(apps)


def find_registered_app(paths: ProjectPaths, query: str) -> RegisteredApp | None:
    match = match_registered_app(paths, query)
    return match.app if match is not None else None


def match_registered_app(paths: ProjectPaths, query: str) -> RegisteredAppMatch | None:
    normalized_query = _normalize_match_text(query)
    if not normalized_query:
        return None

    best: tuple[int, RegisteredApp, str] | None = None
    for app in list_registered_apps(paths):
        for alias in (app.app_id, app.display_name, *app.aliases):
            normalized_alias = _normalize_match_text(alias)
            if normalized_alias and (normalized_query == normalized_alias or normalized_alias in normalized_query):
                score = len(normalized_alias)
                if best is None or score > best[0]:
                    best = (score, app, alias)

    if best is None:
        return None
    return RegisteredAppMatch(app=best[1], alias=best[2])


def describe_registered_apps(paths: ProjectPaths) -> str:
    lines = [
        "应用注册表：",
        "说明：当前阶段只做注册和匹配，不启动应用。",
    ]
    for app in list_registered_apps(paths):
        lines.append(f"- {app.display_name} ({app.app_id})")
        launch_path = app.launch_path
        if launch_path is not None:
            lines.append(f"  路径：{launch_path}")
        elif app.configured_path is not None:
            lines.append(f"  路径：未找到（已配置 {app.configured_path}）")
        else:
            lines.append("  路径：未配置")
        lines.append(f"  别名：{'、'.join(app.aliases)}")
    lines.append("本地覆盖：config/apps.local.json")
    return "\n".join(lines)


def _read_local_registry(paths: ProjectPaths) -> dict[str, dict[str, object]]:
    registry_path = paths.config_dir / APP_REGISTRY_FILENAME
    if not registry_path.exists():
        return {}

    try:
        raw = json.loads(registry_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    apps = raw.get("apps") if isinstance(raw, dict) else None
    if not isinstance(apps, dict):
        return {}

    registry: dict[str, dict[str, object]] = {}
    for app_id, payload in apps.items():
        if isinstance(app_id, str) and isinstance(payload, dict):
            registry[app_id] = payload
    return registry


def _configured_path(payload: dict[str, object]) -> Path | None:
    raw_path = payload.get("path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        return None
    return Path(raw_path).expanduser().resolve()


def _merge_aliases(default_aliases: tuple[str, ...], extra_aliases: object) -> tuple[str, ...]:
    aliases = list(default_aliases)
    if isinstance(extra_aliases, list):
        aliases.extend(alias for alias in extra_aliases if isinstance(alias, str) and alias.strip())

    unique_aliases: list[str] = []
    seen: set[str] = set()
    for alias in aliases:
        normalized = _normalize_match_text(alias)
        if normalized and normalized not in seen:
            unique_aliases.append(alias.strip())
            seen.add(normalized)
    return tuple(unique_aliases)


def _builtin_apps() -> tuple[RegisteredApp, ...]:
    return (
        RegisteredApp(
            app_id="chrome",
            display_name="Chrome",
            aliases=("Chrome", "Google Chrome", "谷歌浏览器", "谷歌", "浏览器"),
            executable_candidates=_candidate_paths(
                ("Google", "Chrome", "Application", "chrome.exe"),
            ),
        ),
        RegisteredApp(
            app_id="qq",
            display_name="QQ",
            aliases=("QQ", "腾讯QQ", "腾讯 QQ"),
            executable_candidates=_candidate_paths(("Tencent", "QQ", "Bin", "QQ.exe")),
        ),
        RegisteredApp(
            app_id="wechat",
            display_name="微信",
            aliases=("微信", "WeChat", "Weixin", "微信电脑版"),
            executable_candidates=_candidate_paths(("Tencent", "WeChat", "WeChat.exe")),
        ),
        RegisteredApp(
            app_id="idea",
            display_name="IntelliJ IDEA",
            aliases=("IntelliJ IDEA", "IDEA", "IntelliJ", "JetBrains IDEA"),
            executable_candidates=_candidate_paths(("JetBrains", "IntelliJ IDEA", "bin", "idea64.exe")),
        ),
        RegisteredApp(
            app_id="clash_verge",
            display_name="Clash Verge",
            aliases=("Clash Verge", "Clash", "代理面板", "代理", "Clash Verge Rev"),
            executable_candidates=_candidate_paths(("Clash Verge", "Clash Verge.exe")),
        ),
    )


def _candidate_paths(*relative_parts: tuple[str, ...]) -> tuple[Path, ...]:
    roots = (
        os.environ.get("ProgramFiles"),
        os.environ.get("ProgramFiles(x86)"),
        os.environ.get("LOCALAPPDATA"),
        os.environ.get("APPDATA"),
    )
    candidates: list[Path] = []
    for root in roots:
        if not root:
            continue
        for parts in relative_parts:
            candidates.append(Path(root, *parts))
    return tuple(candidates)


def _normalize_match_text(text: str) -> str:
    return re.sub(r"[\s_\-]+", "", text.strip().casefold())
