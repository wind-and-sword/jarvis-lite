from __future__ import annotations

import json
from pathlib import Path

from .app_registry import APP_REGISTRY_FILENAME
from .authorization_rules import AUTHORIZATION_RULES_FILENAME, authorization_rule_count
from .automation import list_common_directories
from .config import ProjectPaths
from .contacts import contact_alias_count
from .llm import LLMSettings, llm_local_config_path
from .memory_config_candidates import memory_config_candidate_counts
from .preferences import PREFERENCES_FILENAME, preference_count
from .search import SearchSettings, search_local_config_path


def describe_memory_config_manager(paths: ProjectPaths) -> str:
    """汇总记忆与本地配置状态；敏感字段只展示配置状态。"""

    directories = list_common_directories(paths)
    app_override_path = paths.config_dir / APP_REGISTRY_FILENAME
    app_override_count, app_override_error = _count_app_overrides(app_override_path)
    llm_settings = LLMSettings.from_sources(paths)
    search_settings = SearchSettings.from_sources(paths)
    active_candidate_count, dismissed_candidate_count = memory_config_candidate_counts(paths)

    lines = [
        "记忆与配置管家：",
        "说明：本阶段只做只读盘点和入口提示，不自动写入长期配置。",
        f"- 长期记忆：{_count_markdown_bullets(paths.profile_path)} 条（memory/profile.md）",
        f"- 经验记忆：{_count_markdown_bullets(paths.memory_dir / 'experiences.md')} 条（memory/experiences.md）",
        f"- 常用目录：{len(directories)} 个（memory/directories.json）",
        f"- 联系人别名：{contact_alias_count(paths)} 个（config/contacts.local.json）",
        f"- 授权规则：{authorization_rule_count(paths)} 条（config/{AUTHORIZATION_RULES_FILENAME}）",
        f"- 偏好：{preference_count(paths)} 条（config/{PREFERENCES_FILENAME}）",
    ]
    if directories:
        lines.append(f"  目录别名：{'、'.join(directory.alias for directory in directories)}")
    lines.append(
        f"- 应用本地覆盖：{app_override_count} 个（config/{APP_REGISTRY_FILENAME}"
        f"{'，存在' if app_override_path.exists() else '，未创建'}）"
    )
    if app_override_error:
        lines.append(f"  读取状态：{app_override_error}")
    lines.append(f"- 记忆与配置候选：{active_candidate_count} 条活跃，{dismissed_candidate_count} 条已忽略")

    lines.extend(_describe_llm_config(paths, llm_settings))
    lines.extend(_describe_search_config(paths, search_settings))
    lines.extend(
        [
            "可管理入口：",
            "- /remember 记忆内容：写入长期记忆",
            "- /experience 经验内容：写入经验记忆",
            "- /dir-add 别名 目录路径：登记常用目录",
            "- /apps：查看应用注册表和本地覆盖提示",
            "- /authorization-status：查看本地授权规则和执行决策边界",
            "- /preference-status：查看本地偏好启用状态",
            "- /preference-preview [输入文本]：预览已启用偏好的应用草案",
            "- /preference-apply-draft [输入文本]：生成待确认偏好应用草稿",
            "- /config-candidates：查看记忆与配置候选池",
            "- /llm-config-check：只读检查外脑本地配置",
            "- /search-config-check：只读检查联网搜索本地配置",
            "后续边界：明确保存指令可直接保存；普通对话先进入候选，不会无脑写入长期配置。",
            "敏感字段：API key 只显示已配置/未配置，不回显真实值。",
        ]
    )
    return "\n".join(lines)


def _describe_llm_config(paths: ProjectPaths, settings: LLMSettings) -> list[str]:
    local_path = llm_local_config_path(paths)
    lines = [
        f"- LLM 本地配置：{'存在' if local_path.exists() else '未创建'}（config/llm.local.json）",
        f"  Provider：{settings.provider}",
    ]
    if settings.adapter_provider != settings.provider:
        lines.append(f"  Adapter：{settings.adapter_provider}")
    if settings.model:
        lines.append(f"  Model：{settings.model}")
    if settings.base_url:
        lines.append(f"  Base URL：{settings.base_url}")
    lines.append(f"  API key：{'已配置' if settings.api_key else '未配置'}")
    issues = settings.configuration_issues()
    if issues:
        lines.append(f"  配置问题：{len(issues)} 项")
    return lines


def _describe_search_config(paths: ProjectPaths, settings: SearchSettings) -> list[str]:
    local_path = search_local_config_path(paths)
    lines = [
        f"- 联网搜索本地配置：{'存在' if local_path.exists() else '未创建'}（config/search.local.json）",
        f"  Provider：{settings.provider}",
        f"  Max results：{settings.max_results}",
    ]
    if settings.base_url:
        lines.append(f"  Base URL：{settings.base_url}")
    lines.append(f"  API key：{'已配置' if settings.api_key else '未配置'}")
    issues = settings.configuration_issues()
    if issues:
        lines.append(f"  配置问题：{len(issues)} 项")
    return lines


def _count_markdown_bullets(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip().startswith("- "))
    except OSError:
        return 0


def _count_app_overrides(path: Path) -> tuple[int, str]:
    if not path.exists():
        return 0, ""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return 0, f"config/{APP_REGISTRY_FILENAME} 不是有效 JSON：{exc.msg}"
    except OSError as exc:
        return 0, f"config/{APP_REGISTRY_FILENAME} 读取失败：{exc}"

    apps = payload.get("apps") if isinstance(payload, dict) else None
    if not isinstance(apps, dict):
        return 0, f"config/{APP_REGISTRY_FILENAME} 未包含 apps 对象"
    return sum(1 for app_id, value in apps.items() if isinstance(app_id, str) and isinstance(value, dict)), ""
