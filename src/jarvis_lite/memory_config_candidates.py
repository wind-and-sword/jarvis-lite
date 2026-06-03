from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from .automation import add_common_directory
from .config import ProjectPaths
from .memory import append_experience, append_memory
from .runtime_context import (
    MEMORY_CONFIG_CANDIDATE_LIMIT,
    RuntimeMemoryConfigCandidateContext,
    load_runtime_context,
    save_runtime_context,
)


_TYPE_ALIASES = {
    "memory": ("memory", "长期记忆"),
    "记忆": ("memory", "长期记忆"),
    "长期记忆": ("memory", "长期记忆"),
    "experience": ("experience", "经验记忆"),
    "经验": ("experience", "经验记忆"),
    "经验记忆": ("experience", "经验记忆"),
    "directory": ("directory", "常用目录"),
    "dir": ("directory", "常用目录"),
    "目录": ("directory", "常用目录"),
    "常用目录": ("directory", "常用目录"),
    "app_alias": ("app_alias", "应用别名"),
    "app": ("app_alias", "应用别名"),
    "应用": ("app_alias", "应用别名"),
    "应用别名": ("app_alias", "应用别名"),
    "contact_alias": ("contact_alias", "联系人别名"),
    "contact": ("contact_alias", "联系人别名"),
    "联系人": ("contact_alias", "联系人别名"),
    "联系人别名": ("contact_alias", "联系人别名"),
    "authorization_rule": ("authorization_rule", "授权规则"),
    "authorization": ("authorization_rule", "授权规则"),
    "auth": ("authorization_rule", "授权规则"),
    "授权": ("authorization_rule", "授权规则"),
    "授权规则": ("authorization_rule", "授权规则"),
    "免确认": ("authorization_rule", "授权规则"),
    "preference": ("preference", "偏好"),
    "偏好": ("preference", "偏好"),
    "other": ("other", "其他"),
    "其他": ("other", "其他"),
}


def describe_memory_config_candidates(paths: ProjectPaths) -> str:
    """展示运行态记忆与配置候选池，不做长期写入。"""

    context = load_runtime_context(paths)
    active_candidates = _active_candidates(context.memory_config_candidates)
    if not active_candidates:
        return "\n".join(
            [
                "记忆与配置候选：暂无。",
                "说明：候选池只保存运行态建议，不会自动写入长期记忆或配置。",
                "添加候选：/config-candidate-add 类型 内容",
                "固化候选：/config-candidate-apply 编号",
                "忽略候选：/config-candidate-dismiss 编号",
            ]
        )

    lines = [
        "记忆与配置候选：",
        "说明：候选池只保存运行态建议，不会自动写入长期记忆或配置。",
    ]
    for index, candidate in enumerate(active_candidates, start=1):
        lines.append(f"{index}. {_candidate_type_label(candidate.candidate_type)}：{candidate.content}")
        lines.append(f"   出现次数：{candidate.count}")
    lines.extend(
        [
            "添加候选：/config-candidate-add 类型 内容",
            "固化候选：/config-candidate-apply 编号",
            "忽略候选：/config-candidate-dismiss 编号",
        ]
    )
    return "\n".join(lines)


def record_memory_config_candidate(paths: ProjectPaths, candidate_type: str, content: str) -> str:
    """显式记录一条运行态候选；重复候选只增加计数。"""

    normalized_type, label = _normalize_candidate_type(candidate_type)
    normalized_content = content.strip()
    if not normalized_content:
        return "用法：/config-candidate-add 类型 内容"

    now = _now_iso()
    context = load_runtime_context(paths)
    candidates = list(context.memory_config_candidates)
    existing_index = _find_candidate_index(candidates, normalized_type, normalized_content)
    if existing_index is None:
        updated_candidate = RuntimeMemoryConfigCandidateContext(
            candidate_type=normalized_type,
            content=normalized_content,
            status="active",
            count=1,
            first_seen_at=now,
            last_seen_at=now,
        )
        candidates.append(updated_candidate)
    else:
        existing = candidates[existing_index]
        updated_candidate = RuntimeMemoryConfigCandidateContext(
            candidate_type=normalized_type,
            content=existing.content,
            status="active",
            count=existing.count + 1,
            first_seen_at=existing.first_seen_at or now,
            last_seen_at=now,
        )
        candidates[existing_index] = updated_candidate

    save_runtime_context(paths, replace(context, memory_config_candidates=_limit_candidates(tuple(candidates))))
    return "\n".join(
        [
            f"已记录记忆与配置候选：{label}",
            f"内容：{updated_candidate.content}",
            f"出现次数：{updated_candidate.count}",
            "查看：/config-candidates",
        ]
    )


def dismiss_memory_config_candidate(paths: ProjectPaths, index: int) -> str:
    """按当前活跃候选编号忽略候选。"""

    if index < 1:
        return "候选编号必须从 1 开始。"

    context = load_runtime_context(paths)
    candidates = list(context.memory_config_candidates)
    active_indices = [candidate_index for candidate_index, candidate in enumerate(candidates) if candidate.status == "active"]
    if index > len(active_indices):
        return "\n".join(
            [
                f"没有第 {index} 条候选。",
                "请先运行 /config-candidates 查看当前候选编号。",
            ]
        )

    candidate_index = active_indices[index - 1]
    candidate = candidates[candidate_index]
    dismissed_candidate = RuntimeMemoryConfigCandidateContext(
        candidate_type=candidate.candidate_type,
        content=candidate.content,
        status="dismissed",
        count=candidate.count,
        first_seen_at=candidate.first_seen_at,
        last_seen_at=candidate.last_seen_at or _now_iso(),
    )
    candidates[candidate_index] = dismissed_candidate
    save_runtime_context(paths, replace(context, memory_config_candidates=_limit_candidates(tuple(candidates))))
    return f"已忽略候选 {index}：{_candidate_type_label(candidate.candidate_type)}：{candidate.content}"


def apply_memory_config_candidate(paths: ProjectPaths, index: int) -> str:
    """按当前活跃候选编号固化低风险候选。"""

    if index < 1:
        return "候选编号必须从 1 开始。"

    context = load_runtime_context(paths)
    candidates = list(context.memory_config_candidates)
    active_indices = _active_candidate_indices(candidates)
    if index > len(active_indices):
        return "\n".join(
            [
                f"没有第 {index} 条候选。",
                "请先运行 /config-candidates 查看当前候选编号。",
            ]
        )

    candidate_index = active_indices[index - 1]
    candidate = candidates[candidate_index]
    try:
        target = _apply_candidate_to_storage(paths, candidate)
    except ValueError as exc:
        return str(exc)
    except FileNotFoundError as exc:
        return f"候选固化失败：{exc}"

    applied_candidate = RuntimeMemoryConfigCandidateContext(
        candidate_type=candidate.candidate_type,
        content=candidate.content,
        status="applied",
        count=candidate.count,
        first_seen_at=candidate.first_seen_at,
        last_seen_at=candidate.last_seen_at or _now_iso(),
    )
    candidates[candidate_index] = applied_candidate
    save_runtime_context(paths, replace(context, memory_config_candidates=_limit_candidates(tuple(candidates))))
    return "\n".join(
        [
            f"已固化记忆与配置候选 {index}：{_candidate_type_label(candidate.candidate_type)}",
            f"内容：{candidate.content}",
            f"写入：{target}",
            "查看剩余候选：/config-candidates",
        ]
    )


def memory_config_candidate_counts(paths: ProjectPaths) -> tuple[int, int]:
    """返回活跃和已忽略候选数量。"""

    candidates = load_runtime_context(paths).memory_config_candidates
    active_count = sum(1 for candidate in candidates if candidate.status == "active")
    dismissed_count = sum(1 for candidate in candidates if candidate.status == "dismissed")
    return active_count, dismissed_count


def _normalize_candidate_type(candidate_type: str) -> tuple[str, str]:
    key = candidate_type.strip()
    if not key:
        return "other", "其他"
    return _TYPE_ALIASES.get(key, _TYPE_ALIASES.get(key.lower(), ("other", "其他")))


def _candidate_type_label(candidate_type: str) -> str:
    return _TYPE_ALIASES.get(candidate_type, ("other", "其他"))[1]


def _active_candidates(
    candidates: tuple[RuntimeMemoryConfigCandidateContext, ...],
) -> tuple[RuntimeMemoryConfigCandidateContext, ...]:
    return tuple(candidate for candidate in candidates if candidate.status == "active")


def _active_candidate_indices(candidates: list[RuntimeMemoryConfigCandidateContext]) -> list[int]:
    return [candidate_index for candidate_index, candidate in enumerate(candidates) if candidate.status == "active"]


def _find_candidate_index(
    candidates: list[RuntimeMemoryConfigCandidateContext],
    candidate_type: str,
    content: str,
) -> int | None:
    for index, candidate in enumerate(candidates):
        if candidate.candidate_type == candidate_type and candidate.content.strip() == content:
            return index
    return None


def _apply_candidate_to_storage(paths: ProjectPaths, candidate: RuntimeMemoryConfigCandidateContext) -> str:
    if candidate.candidate_type == "memory":
        append_memory(paths, candidate.content)
        return "memory/profile.md"
    if candidate.candidate_type == "experience":
        append_experience(paths, candidate.content)
        return "memory/experiences.md"
    if candidate.candidate_type == "directory":
        alias, directory = _parse_directory_candidate(candidate.content)
        add_common_directory(paths, alias, directory)
        return "memory/directories.json"

    label = _candidate_type_label(candidate.candidate_type)
    raise ValueError(_unsupported_candidate_message(label))


def _parse_directory_candidate(content: str) -> tuple[str, str]:
    normalized = content.strip()
    if "=>" in normalized:
        alias, directory = normalized.split("=>", 1)
    else:
        parts = normalized.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError("目录候选格式：别名 => 路径，或 别名 路径。")
        alias, directory = parts

    normalized_alias = alias.strip()
    normalized_directory = directory.strip().strip('"').strip("'")
    if not normalized_alias or not normalized_directory:
        raise ValueError("目录候选格式：别名 => 路径，或 别名 路径。")
    return normalized_alias, normalized_directory


def _unsupported_candidate_message(label: str) -> str:
    return "\n".join(
        [
            f"暂不支持固化{label}候选。",
            "说明：本阶段只固化长期记忆、经验记忆和常用目录，不会写入长期配置。",
            "候选仍保持活跃，可用 /config-candidate-dismiss 编号 忽略。",
        ]
    )


def _limit_candidates(
    candidates: tuple[RuntimeMemoryConfigCandidateContext, ...],
) -> tuple[RuntimeMemoryConfigCandidateContext, ...]:
    if len(candidates) <= MEMORY_CONFIG_CANDIDATE_LIMIT:
        return candidates
    return candidates[-MEMORY_CONFIG_CANDIDATE_LIMIT:]


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
