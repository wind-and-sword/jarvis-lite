from __future__ import annotations

import json
import os
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .config import ProjectPaths


APP_REGISTRY_FILENAME = "apps.local.json"
AppLaunchExecutor = Callable[[Path], None]


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


@dataclass(frozen=True)
class AppLaunchResult:
    app: RegisteredApp
    alias: str
    path: Path
    executed_at: datetime


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
        "说明：可用 /app-launch 启动已登记且有路径的应用；当前列表只展示注册和路径状态。",
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


def parse_app_alias_candidate(content: str) -> tuple[str, str]:
    """解析应用别名候选，格式为别名到已登记应用标识或名称。"""

    normalized = content.strip()
    for separator in ("=>", "->", "="):
        if separator in normalized:
            alias, app_query = normalized.split(separator, 1)
            return _normalize_app_alias(alias), _normalize_app_query(app_query)
    raise ValueError(_app_alias_format_message())


def save_app_alias(paths: ProjectPaths, alias: str, app_query: str) -> RegisteredApp:
    """把应用别名保存到本地覆盖，不写入应用路径。"""

    normalized_alias = _normalize_app_alias(alias)
    app = _resolve_registered_app(paths, app_query)
    payload = _read_local_registry_payload(paths)
    apps = payload["apps"]
    app_payload = dict(apps.get(app.app_id, {}))
    aliases = _valid_aliases(app_payload.get("aliases"))
    alias_key = _normalize_match_text(normalized_alias)
    if all(_normalize_match_text(existing_alias) != alias_key for existing_alias in aliases):
        aliases.append(normalized_alias)
    app_payload["aliases"] = aliases
    apps[app.app_id] = app_payload
    payload["apps"] = apps
    _write_local_registry_payload(paths, payload)
    return app


def remove_app_alias(paths: ProjectPaths, alias: str, app_query: str) -> bool:
    """从本地覆盖中删除应用别名；保留同一应用已有 path 等其他覆盖。"""

    normalized_alias = _normalize_app_alias(alias)
    app = _resolve_registered_app(paths, app_query)
    payload = _read_local_registry_payload(paths)
    apps = payload["apps"]
    raw_app_payload = apps.get(app.app_id)
    if not isinstance(raw_app_payload, dict):
        return False

    app_payload = dict(raw_app_payload)
    aliases = _valid_aliases(app_payload.get("aliases"))
    alias_key = _normalize_match_text(normalized_alias)
    updated_aliases = [
        existing_alias
        for existing_alias in aliases
        if _normalize_match_text(existing_alias) != alias_key
    ]
    removed = len(updated_aliases) != len(aliases)
    if not removed:
        return False

    if updated_aliases:
        app_payload["aliases"] = updated_aliases
    else:
        app_payload.pop("aliases", None)

    if app_payload:
        apps[app.app_id] = app_payload
    else:
        apps.pop(app.app_id, None)
    payload["apps"] = apps
    _write_local_registry_payload(paths, payload)
    return True


def launch_registered_app(
    paths: ProjectPaths,
    query: str,
    *,
    executor: AppLaunchExecutor | None = None,
) -> AppLaunchResult:
    """启动一个已登记且有可用路径的应用。"""

    normalized_query = query.strip()
    if not normalized_query:
        raise ValueError("应用名称或别名不能为空。")

    match = match_registered_app(paths, normalized_query)
    if match is None:
        raise ValueError(f"没有找到应用：{normalized_query}。可用 /apps 查看已登记应用。")

    launch_path = match.app.launch_path
    if launch_path is None:
        raise FileNotFoundError(
            f"应用启动路径未找到：{match.app.display_name}。可在 config/apps.local.json 配置 path。"
        )

    launcher = executor or _launch_app_with_subprocess
    launcher(launch_path)
    return AppLaunchResult(app=match.app, alias=match.alias, path=launch_path, executed_at=datetime.now())


def describe_app_launch(
    paths: ProjectPaths,
    query: str,
    *,
    executor: AppLaunchExecutor | None = None,
) -> str:
    result = launch_registered_app(paths, query, executor=executor)
    return "\n".join(
        [
            f"应用启动执行：{result.app.display_name} ({result.app.app_id})",
            f"命中别名：{result.alias}",
            f"路径：{result.path}",
            f"时间：{result.executed_at.isoformat(timespec='seconds')}",
            "说明：当前阶段只启动已登记应用，不切换窗口、不点击、不输入。",
        ]
    )


def _read_local_registry(paths: ProjectPaths) -> dict[str, dict[str, object]]:
    apps = _read_local_registry_payload(paths).get("apps")
    if isinstance(apps, dict):
        return apps
    return {}


def _read_local_registry_payload(paths: ProjectPaths) -> dict[str, object]:
    registry_path = paths.config_dir / APP_REGISTRY_FILENAME
    if not registry_path.exists():
        return {"apps": {}}

    try:
        raw = json.loads(registry_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"apps": {}}
    if not isinstance(raw, dict):
        return {"apps": {}}

    payload = dict(raw)
    apps = payload.get("apps")
    if not isinstance(apps, dict):
        payload["apps"] = {}
        return payload

    registry: dict[str, dict[str, object]] = {}
    for app_id, app_payload in apps.items():
        if isinstance(app_id, str) and isinstance(app_payload, dict) and app_id.strip():
            registry[app_id] = dict(app_payload)
    payload["apps"] = registry
    return payload


def _write_local_registry_payload(paths: ProjectPaths, payload: dict[str, object]) -> None:
    registry_path = paths.config_dir / APP_REGISTRY_FILENAME
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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


def _valid_aliases(raw_aliases: object) -> list[str]:
    if not isinstance(raw_aliases, list):
        return []

    aliases: list[str] = []
    seen: set[str] = set()
    for alias in raw_aliases:
        if not isinstance(alias, str):
            continue
        normalized_alias = alias.strip()
        alias_key = _normalize_match_text(normalized_alias)
        if alias_key and alias_key not in seen:
            aliases.append(normalized_alias)
            seen.add(alias_key)
    return aliases


def _normalize_app_alias(alias: str) -> str:
    normalized = alias.strip()
    if not normalized:
        raise ValueError(_app_alias_format_message())
    return normalized


def _normalize_app_query(app_query: str) -> str:
    normalized = app_query.strip()
    if not normalized:
        raise ValueError(_app_alias_format_message())
    return normalized


def _resolve_registered_app(paths: ProjectPaths, app_query: str) -> RegisteredApp:
    normalized_query = _normalize_app_query(app_query)
    app = find_registered_app(paths, normalized_query)
    if app is None:
        raise ValueError(f"没有找到应用：{normalized_query}。可用 /apps 查看已登记应用。")
    return app


def _app_alias_format_message() -> str:
    return "应用别名候选格式：别名 => 应用标识或已登记应用名。"


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


def _launch_app_with_subprocess(path: Path) -> None:
    try:
        subprocess.Popen([str(path)], cwd=str(path.parent))
    except OSError as exc:
        raise RuntimeError(f"应用启动失败：{path}：{exc}") from exc
