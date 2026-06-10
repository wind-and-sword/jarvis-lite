from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Any

from .config import ProjectPaths
from .runtime_context import (
    PREFERENCE_APPLICATION_HISTORY_LIMIT,
    RuntimePreferenceApplicationContext,
    load_runtime_context,
    save_runtime_context,
)


PREFERENCES_FILENAME = "preferences.local.json"


@dataclass(frozen=True)
class Preference:
    """本地偏好记录；第一阶段只做持久化和展示，不自动改变回复策略。"""

    preference: str
    preference_id: str = ""
    enabled: bool = False
    source: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class PreferenceLocalAnswerTypeSetting:
    """本地回答附注类型开关；只控制附注展示，不改变偏好确认记录。"""

    answer_type: str
    label: str
    enabled: bool


@dataclass(frozen=True)
class PreferenceReplyContextSetting:
    """普通回复偏好上下文开关；只控制 LLM fallback 上下文展示。"""

    enabled: bool


def parse_preference_candidate(content: str) -> str:
    """解析偏好候选，当前要求候选内容本身就是明确偏好文本。"""

    return _normalize_preference(content)


def read_preferences(paths: ProjectPaths) -> tuple[Preference, ...]:
    """读取本地偏好；缺失或损坏时返回空集合。"""

    payload = _read_preferences_payload(paths)
    records = payload.get("preferences")
    if not isinstance(records, list):
        return ()

    preferences: list[Preference] = []
    for record in records:
        preference = _preference_from_record(record)
        if preference is not None:
            preferences.append(preference)
    return tuple(preferences)


def save_preference(
    paths: ProjectPaths,
    preference: str,
    *,
    source: str = "",
    enabled: bool | None = None,
) -> Preference:
    """新增或更新本地偏好，不改变当前回复风格或执行决策。"""

    normalized_preference = _normalize_preference(preference)
    now = _now_iso()
    payload = _read_preferences_payload(paths)
    records = _valid_preference_records(payload.get("preferences"))

    saved = Preference(
        preference=normalized_preference,
        preference_id=_preference_id_for(normalized_preference),
        enabled=bool(enabled) if enabled is not None else False,
        source=source.strip(),
        created_at=now,
        updated_at=now,
    )
    preference_key = _preference_key(normalized_preference)
    updated_records: list[dict[str, object]] = []
    replaced = False
    for record in records:
        existing_preference = str(record.get("preference") or "").strip()
        if _preference_key(existing_preference) == preference_key:
            existing_id = _coerce_preference_id(record.get("id"), existing_preference)
            saved = Preference(
                preference=normalized_preference,
                preference_id=existing_id,
                enabled=_coerce_enabled(record.get("enabled")) if enabled is None else bool(enabled),
                source=source.strip() or str(record.get("source") or "").strip(),
                created_at=str(record.get("created_at") or now),
                updated_at=now,
            )
            updated_records.append(_preference_to_record(saved))
            replaced = True
        else:
            updated_records.append(record)
    if not replaced:
        updated_records.append(_preference_to_record(saved))

    payload["preferences"] = updated_records
    _write_preferences_payload(paths, payload)
    return saved


def set_preference_enabled(paths: ProjectPaths, reference: int | str, enabled: bool) -> Preference:
    """按 1 基编号或稳定 ID 切换偏好启用状态；不自动应用到回复或执行路径。"""

    payload = _read_preferences_payload(paths)
    records = _valid_preference_records(payload.get("preferences"))
    record_index = _resolve_preference_record_index(records, reference)
    if record_index is None:
        raise ValueError("偏好引用不存在。可用 /preference-status 查看本地偏好 ID。")

    now = _now_iso()
    target_record = records[record_index]
    preference_text = str(target_record.get("preference") or "").strip()
    updated = Preference(
        preference=preference_text,
        preference_id=_coerce_preference_id(target_record.get("id"), preference_text),
        enabled=enabled,
        source=str(target_record.get("source") or "").strip(),
        created_at=str(target_record.get("created_at") or now),
        updated_at=now,
    )
    records[record_index] = _preference_to_record(updated)
    payload["preferences"] = records
    _write_preferences_payload(paths, payload)
    return updated


def remove_preference(paths: ProjectPaths, preference: str) -> bool:
    """按偏好文本删除本地偏好；删除后保留空配置文件。"""

    normalized_preference = _normalize_preference(preference)
    payload = _read_preferences_payload(paths)
    records = _valid_preference_records(payload.get("preferences"))
    preference_key = _preference_key(normalized_preference)
    updated_records = [
        record
        for record in records
        if _preference_key(str(record.get("preference") or "")) != preference_key
    ]
    removed = len(updated_records) != len(records)
    payload["preferences"] = updated_records
    _write_preferences_payload(paths, payload)
    return removed


def preference_count(paths: ProjectPaths) -> int:
    """返回当前已保存偏好数量。"""

    return len(read_preferences(paths))


def enabled_preferences(paths: ProjectPaths) -> tuple[Preference, ...]:
    """返回已显式启用的偏好；调用方仍需显式决定是否应用。"""

    return tuple(preference for preference in read_preferences(paths) if preference.enabled)


def describe_preferences(paths: ProjectPaths) -> str:
    """展示本地偏好，只读展示，不触发回复或执行策略变更。"""

    preferences = read_preferences(paths)
    enabled_count = sum(1 for preference in preferences if preference.enabled)
    disabled_count = len(preferences) - enabled_count
    lines = [
        f"本地偏好：{len(preferences)} 条",
        f"- 已启用：{enabled_count} 条",
        f"- 未启用：{disabled_count} 条",
    ]
    for index, preference in enumerate(preferences, 1):
        state = "已启用" if preference.enabled else "未启用"
        lines.append(f"{index}. {state} [{preference.preference_id}] {preference.preference}")
    conflict_hints = preference_conflict_hints(preferences)
    if conflict_hints:
        lines.append("偏好冲突提示：")
        lines.extend(conflict_hints)
    lines.extend(
        [
            "说明：启用状态只用于本地可审计管理，不自动改变回复风格、LLM prompt、路由或执行决策。",
            "可用 /preference-enable 编号或ID 启用，/preference-disable 编号或ID 停用。",
        ]
    )
    return "\n".join(lines)


def describe_preference_local_answer_type_settings(paths: ProjectPaths) -> str:
    """展示本地回答偏好附注的回答类型开关。"""

    enabled_types = set(_enabled_preference_local_answer_types(paths))
    lines = [
        "偏好本地回答附注类型",
        "配置文件：config/preferences.local.json",
    ]
    for index, (answer_type, label) in enumerate(_PREFERENCE_LOCAL_ANSWER_TYPE_LABELS.items(), 1):
        state = "已启用" if answer_type in enabled_types else "已停用"
        lines.append(f"{index}. {state} [{answer_type}] {label}")
    lines.extend(
        [
            "可用类型：knowledge（本地知识库回答）、memory（长期记忆兜底回答）。",
            "可用 /preference-answer-type-enable 类型 启用，/preference-answer-type-disable 类型 停用。",
            "说明：只控制本地回答附注展示，不撤销确认记录，不删除或停用偏好，不改变普通 LLM fallback、路由或执行决策。",
        ]
    )
    return "\n".join(lines)


def set_preference_local_answer_type_enabled(
    paths: ProjectPaths,
    reference: str,
    enabled: bool,
) -> PreferenceLocalAnswerTypeSetting:
    """显式启停本地回答附注类型。"""

    answer_type = _resolve_preference_local_answer_type(reference)
    if answer_type is None:
        raise ValueError("回答类型必须是 knowledge 或 memory。可用 /preference-answer-types 查看。")

    enabled_types = list(_enabled_preference_local_answer_types(paths))
    if enabled and answer_type not in enabled_types:
        enabled_types.append(answer_type)
    if not enabled:
        enabled_types = [existing for existing in enabled_types if existing != answer_type]

    payload = _read_preferences_payload(paths)
    payload["local_answer_note_types"] = enabled_types
    _write_preferences_payload(paths, payload)
    return PreferenceLocalAnswerTypeSetting(
        answer_type=answer_type,
        label=_PREFERENCE_LOCAL_ANSWER_TYPE_LABELS[answer_type],
        enabled=enabled,
    )


def describe_preference_reply_context_settings(paths: ProjectPaths) -> str:
    """展示已确认偏好进入普通回复上下文的显式开关。"""

    enabled = _preference_reply_context_enabled(paths)
    state = "已启用" if enabled else "已停用"
    lines = [
        "偏好普通回复上下文",
        f"状态：{state}",
        "配置文件：config/preferences.local.json",
        "可用 /preference-reply-context-enable 启用，/preference-reply-context-disable 停用。",
        "说明：只控制普通 LLM fallback 和 /llm-context-preview 是否携带已确认偏好上下文。",
        "边界：不影响本地回答附注，不撤销确认记录，不删除或停用偏好，不改变路由或执行决策。",
    ]
    return "\n".join(lines)


def set_preference_reply_context_enabled(paths: ProjectPaths, enabled: bool) -> PreferenceReplyContextSetting:
    """显式启停已确认偏好进入普通回复上下文。"""

    payload = _read_preferences_payload(paths)
    payload["reply_context_enabled"] = bool(enabled)
    _write_preferences_payload(paths, payload)
    return PreferenceReplyContextSetting(enabled=bool(enabled))


def describe_preference_preview(paths: ProjectPaths, user_input: str = "") -> str:
    """预览已启用偏好的应用草案；不自动改变任何回复或执行路径。"""

    preview_input = user_input.strip()
    preferences = enabled_preferences(paths)
    lines = [
        "偏好应用预览",
        f"已启用偏好：{len(preferences)} 条",
    ]
    if preview_input:
        lines.append(f"预览输入：{preview_input}")
    if preferences:
        lines.append("将参考的偏好：")
        for index, preference in enumerate(preferences, 1):
            lines.append(f"{index}. [{preference.preference_id}] {preference.preference}")
        conflict_hints = preference_conflict_hints(preferences)
        if conflict_hints:
            lines.append("偏好冲突提示：")
            lines.extend(conflict_hints)
    else:
        lines.append("暂无已启用偏好。可用 /preference-enable 编号或ID 启用。")
    lines.extend(
        [
            "应用策略草案：已启用偏好只作为显式预览内容展示。",
            "说明：当前不自动改变回复风格、LLM prompt、路由或执行决策。",
        ]
    )
    return "\n".join(lines)


def describe_preference_application_draft(paths: ProjectPaths, user_input: str = "") -> str:
    """生成待确认偏好应用草稿；当前阶段不真正应用偏好。"""

    draft_input = user_input.strip()
    preferences = enabled_preferences(paths)
    lines = [
        "待确认偏好应用草稿",
        "确认状态：待用户显式确认",
        f"已启用偏好：{len(preferences)} 条",
    ]
    if draft_input:
        lines.append(f"预览输入：{draft_input}")
    if preferences:
        lines.append("拟参考的偏好：")
        for index, preference in enumerate(preferences, 1):
            lines.append(f"{index}. [{preference.preference_id}] {preference.preference}")
        conflict_hints = preference_conflict_hints(preferences)
        if conflict_hints:
            lines.append("偏好冲突提示：")
            lines.extend(conflict_hints)
    else:
        lines.append("暂无已启用偏好。可用 /preference-enable 编号或ID 启用。")
    lines.extend(
        [
            "草稿策略：已启用偏好仅生成可审阅草稿，后续真正应用前仍需显式确认。",
            "说明：当前阶段不自动改变回复风格、LLM prompt、路由或执行决策。",
            "确认边界：当前阶段不真正应用偏好，不生成可执行确认命令。",
        ]
    )
    return "\n".join(lines)


def describe_preference_application_history(paths: ProjectPaths) -> str:
    """只读展示最近偏好应用确认记录，便于审计和撤销。"""

    applications = load_runtime_context(paths).recent_preference_applications
    if not applications:
        return "\n".join(
            [
                "偏好应用确认历史：暂无。",
                "说明：只有成功执行 /preference-apply-confirm 后才会记录历史。",
            ]
        )

    lines = [
        "偏好应用确认历史",
        "说明：这里只记录显式确认；不会自动改变普通聊天、LLM prompt、路由或执行决策。",
    ]
    for index, application in enumerate(applications, 1):
        lines.append(f"{index}. {_preference_application_status_label(application.status)} [{application.application_id}]")
        if application.user_input:
            lines.append(f"   应用输入：{application.user_input}")
        if application.created_at:
            lines.append(f"   确认时间：{application.created_at}")
        if application.status == "undone" and application.undone_at:
            lines.append(f"   撤销时间：{application.undone_at}")
        lines.append("   偏好：")
        for preference_id, preference in zip(application.preference_ids, application.preferences):
            lines.append(f"   - [{preference_id}] {preference}")
    lines.extend(
        [
            "撤销确认：/preference-apply-undo 编号或ID",
            "撤销范围：只撤销确认记录，不删除或停用偏好，不回滚已经展示的输出。",
        ]
    )
    return "\n".join(lines)


def describe_preference_reply_context(paths: ProjectPaths) -> str:
    """返回可放入普通 LLM fallback 的已确认偏好上下文。"""

    if not _preference_reply_context_enabled(paths):
        return ""

    application = _active_preference_application_for_reply(paths)
    if application is None:
        return ""

    lines = [
        f"已确认偏好应用：{application.application_id}",
        "应用边界：仅作为普通 LLM fallback 上下文，不改变命令路由、SearchRouter、InnerBrain 或桌面执行决策。",
    ]
    if application.user_input:
        lines.append(f"确认输入：{application.user_input}")
    lines.append("已确认偏好：")
    for preference_id, preference in zip(application.preference_ids, application.preferences):
        lines.append(f"- [{preference_id}] {preference}")
    return "\n".join(lines)


def describe_preference_local_answer_note(paths: ProjectPaths, answer_type: str) -> str:
    """返回可追加到本地知识库和长期记忆回答的偏好确认附注。"""

    normalized_answer_type = _resolve_preference_local_answer_type(answer_type)
    if normalized_answer_type is None:
        return ""
    if normalized_answer_type not in _enabled_preference_local_answer_types(paths):
        return ""
    answer_type_label = _PREFERENCE_LOCAL_ANSWER_TYPE_LABELS[normalized_answer_type]
    if not answer_type_label:
        return ""

    application = _active_preference_application_for_reply(paths)
    if application is None:
        return ""

    lines = [
        f"已确认偏好格式化：{application.application_id}",
        f"回答类型：{answer_type_label}",
        "应用边界：仅用于本地知识库和长期记忆回答格式化，不改变检索、路由、LLM 白名单、SearchRouter、InnerBrain 或桌面执行决策。",
        _preference_application_undo_command(application),
    ]
    if application.user_input:
        lines.append(f"确认输入：{application.user_input}")
    lines.append("已确认偏好：")
    for preference_id, preference in zip(application.preference_ids, application.preferences):
        lines.append(f"- [{preference_id}] {preference}")
    return "\n".join(lines)


def describe_confirmed_preference_application(paths: ProjectPaths, user_input: str = "") -> str:
    """确认已启用偏好仅应用到本次显式命令输出。"""

    application_input = user_input.strip()
    preferences = enabled_preferences(paths)
    if not preferences:
        lines = ["无法确认偏好应用：暂无已启用偏好。"]
        if application_input:
            lines.append(f"应用输入：{application_input}")
        lines.extend(
            [
                "未确认应用偏好。",
                "可用 /preference-enable 编号或ID 启用。",
                "说明：未改变回复风格、LLM prompt、路由或执行决策。",
            ]
        )
        return "\n".join(lines)

    conflict_hints = preference_conflict_hints(preferences)
    if conflict_hints:
        lines = ["无法确认偏好应用：存在偏好冲突。"]
        if application_input:
            lines.append(f"应用输入：{application_input}")
        lines.append("偏好冲突提示：")
        lines.extend(conflict_hints)
        lines.extend(
            [
                "未确认应用偏好。",
                "可用 /preference-disable 编号或ID 停用冲突偏好。",
                "说明：冲突只提示人工确认，不自动裁决优先级。",
            ]
        )
        return "\n".join(lines)

    application = _record_preference_application(paths, application_input, preferences)
    lines = [
        "已确认本次偏好应用",
        f"确认ID：{application.application_id}",
        f"已确认偏好：{len(preferences)} 条",
        _preference_application_undo_command(application),
    ]
    if application_input:
        lines.append(f"应用输入：{application_input}")
    lines.append("本次应用的偏好：")
    for index, preference in enumerate(preferences, 1):
        lines.append(f"{index}. [{preference.preference_id}] {preference.preference}")
    lines.extend(
        [
            "应用范围：仅限本次 /preference-apply-confirm 命令输出。",
            "说明：本次确认不写入 LLM prompt，不影响普通聊天、路由或执行决策。",
        ]
    )
    return "\n".join(lines)


def undo_preference_application(paths: ProjectPaths, reference: int | str) -> str:
    """撤销某条偏好应用确认记录，不改变偏好本身。"""

    context = load_runtime_context(paths)
    applications = list(context.recent_preference_applications)
    application_index = _resolve_preference_application_index(applications, reference)
    if application_index is None:
        return "\n".join(
            [
                "偏好应用确认记录不存在。",
                "请先运行 /preference-apply-history 查看当前编号或ID。",
            ]
        )

    application = applications[application_index]
    if application.status == "undone":
        return "\n".join(
            [
                f"偏好应用确认记录已撤销：{application.application_id}",
                "撤销范围：只撤销确认记录，不删除或停用偏好，不回滚已经展示的输出。",
            ]
        )

    undone = RuntimePreferenceApplicationContext(
        application_id=application.application_id,
        user_input=application.user_input,
        preference_ids=application.preference_ids,
        preferences=application.preferences,
        status="undone",
        created_at=application.created_at,
        undone_at=_now_iso(),
    )
    applications[application_index] = undone
    save_runtime_context(paths, replace(context, recent_preference_applications=tuple(applications)))
    return "\n".join(
        [
            f"已撤销偏好应用确认：{undone.application_id}",
            "撤销范围：只撤销确认记录，不删除或停用偏好，不回滚已经展示的输出。",
            "说明：已保存偏好和启用状态保持不变。",
        ]
    )


def preference_conflict_hints(preferences: tuple[Preference, ...]) -> tuple[str, ...]:
    """返回已启用偏好的明显冲突提示；只提示，不自动裁决。"""

    enabled = tuple(preference for preference in preferences if preference.enabled)
    hints: list[str] = []
    for label, left_keywords, right_keywords in _CONFLICT_RULES:
        left_matches = tuple(
            preference
            for preference in enabled
            if _contains_any(preference.preference, left_keywords)
            and not _contains_any(preference.preference, right_keywords)
        )
        right_matches = tuple(
            preference
            for preference in enabled
            if _contains_any(preference.preference, right_keywords)
            and not _contains_any(preference.preference, left_keywords)
        )
        if left_matches and right_matches:
            hints.append(
                f"- {label}可能冲突：{_format_conflict_preference(left_matches[0])} 与 "
                f"{_format_conflict_preference(right_matches[0])}。只提示冲突，不自动裁决优先级。"
            )
    return tuple(hints)


def _record_preference_application(
    paths: ProjectPaths,
    user_input: str,
    preferences: tuple[Preference, ...],
) -> RuntimePreferenceApplicationContext:
    now = _now_iso()
    context = load_runtime_context(paths)
    application = RuntimePreferenceApplicationContext(
        application_id=_unique_preference_application_id_for(
            now,
            user_input,
            preferences,
            context.recent_preference_applications,
        ),
        user_input=user_input,
        preference_ids=tuple(preference.preference_id for preference in preferences),
        preferences=tuple(preference.preference for preference in preferences),
        status="confirmed",
        created_at=now,
    )
    applications = (application, *context.recent_preference_applications)[:PREFERENCE_APPLICATION_HISTORY_LIMIT]
    save_runtime_context(paths, replace(context, recent_preference_applications=applications))
    return application


def _active_preference_application_for_reply(paths: ProjectPaths) -> RuntimePreferenceApplicationContext | None:
    context = load_runtime_context(paths)
    if not context.recent_preference_applications:
        return None

    application = context.recent_preference_applications[0]
    if application.status != "confirmed":
        return None

    preferences = enabled_preferences(paths)
    if preference_conflict_hints(preferences):
        return None

    current_ids = tuple(preference.preference_id for preference in preferences)
    current_texts = tuple(preference.preference for preference in preferences)
    if current_ids != application.preference_ids or current_texts != application.preferences:
        return None
    return application


def _resolve_preference_application_index(
    applications: list[RuntimePreferenceApplicationContext],
    reference: int | str,
) -> int | None:
    if isinstance(reference, int):
        return reference - 1 if 1 <= reference <= len(applications) else None
    normalized = str(reference).strip()
    if normalized.isdigit():
        index = int(normalized)
        return index - 1 if 1 <= index <= len(applications) else None
    for index, application in enumerate(applications):
        if application.application_id == normalized:
            return index
    return None


def _preference_application_id_for(
    created_at: str,
    user_input: str,
    preferences: tuple[Preference, ...],
    sequence: int = 0,
) -> str:
    payload_parts = [
        created_at,
        user_input,
        *[preference.preference_id for preference in preferences],
        *[preference.preference for preference in preferences],
    ]
    if sequence > 0:
        payload_parts.append(f"sequence={sequence}")
    payload = "|".join(payload_parts)
    return f"prefapp-{hashlib.sha1(payload.encode('utf-8')).hexdigest()[:10]}"


def _unique_preference_application_id_for(
    created_at: str,
    user_input: str,
    preferences: tuple[Preference, ...],
    applications: tuple[RuntimePreferenceApplicationContext, ...],
) -> str:
    existing_ids = {application.application_id for application in applications}
    sequence = 0
    while True:
        application_id = _preference_application_id_for(created_at, user_input, preferences, sequence)
        if application_id not in existing_ids:
            return application_id
        sequence += 1


def _preference_application_status_label(status: str) -> str:
    if status == "undone":
        return "已撤销"
    return "已确认"


def _preference_application_undo_command(application: RuntimePreferenceApplicationContext) -> str:
    return f"撤销确认：/preference-apply-undo {application.application_id}"


def _preference_local_answer_type_label(answer_type: str) -> str:
    normalized_answer_type = _resolve_preference_local_answer_type(answer_type)
    if normalized_answer_type is None:
        return ""
    return _PREFERENCE_LOCAL_ANSWER_TYPE_LABELS[normalized_answer_type]


def _resolve_preference_local_answer_type(reference: str) -> str | None:
    normalized_reference = str(reference or "").strip().casefold()
    return _PREFERENCE_LOCAL_ANSWER_TYPE_ALIASES.get(normalized_reference)


def _enabled_preference_local_answer_types(paths: ProjectPaths) -> tuple[str, ...]:
    payload = _read_preferences_payload(paths)
    if "local_answer_note_types" not in payload:
        return _PREFERENCE_LOCAL_ANSWER_DEFAULT_TYPES

    raw_types = payload.get("local_answer_note_types")
    if not isinstance(raw_types, list):
        return _PREFERENCE_LOCAL_ANSWER_DEFAULT_TYPES

    enabled_types: list[str] = []
    for raw_type in raw_types:
        answer_type = _resolve_preference_local_answer_type(str(raw_type or ""))
        if answer_type is not None and answer_type not in enabled_types:
            enabled_types.append(answer_type)
    return tuple(enabled_types)


def _preference_reply_context_enabled(paths: ProjectPaths) -> bool:
    payload = _read_preferences_payload(paths)
    if "reply_context_enabled" not in payload:
        return True
    value = payload.get("reply_context_enabled")
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().casefold()
        if normalized in {"1", "true", "yes", "enabled", "已启用"}:
            return True
        if normalized in {"0", "false", "no", "disabled", "已停用"}:
            return False
    return True


def _preferences_path(paths: ProjectPaths):
    return paths.config_dir / PREFERENCES_FILENAME


def _read_preferences_payload(paths: ProjectPaths) -> dict[str, Any]:
    target = _preferences_path(paths)
    if not target.exists():
        return {"preferences": []}
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"preferences": []}
    if not isinstance(payload, dict):
        return {"preferences": []}
    return dict(payload)


def _write_preferences_payload(paths: ProjectPaths, payload: dict[str, Any]) -> None:
    target = _preferences_path(paths)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _valid_preference_records(records: object) -> list[dict[str, object]]:
    if not isinstance(records, list):
        return []

    valid_records: list[dict[str, object]] = []
    for record in records:
        preference = _preference_from_record(record)
        if preference is not None:
            valid_records.append(_preference_to_record(preference))
    return valid_records


def _preference_from_record(record: object) -> Preference | None:
    if not isinstance(record, dict):
        return None
    preference = str(record.get("preference") or "").strip()
    if not preference:
        return None
    return Preference(
        preference=preference,
        preference_id=_coerce_preference_id(record.get("id"), preference),
        enabled=_coerce_enabled(record.get("enabled")),
        source=str(record.get("source") or "").strip(),
        created_at=str(record.get("created_at") or "").strip(),
        updated_at=str(record.get("updated_at") or "").strip(),
    )


def _preference_to_record(preference: Preference) -> dict[str, object]:
    return {
        "id": preference.preference_id or _preference_id_for(preference.preference),
        "preference": preference.preference,
        "enabled": preference.enabled,
        "source": preference.source,
        "created_at": preference.created_at,
        "updated_at": preference.updated_at,
    }


def _normalize_preference(preference: str) -> str:
    normalized = preference.strip()
    if not normalized:
        raise ValueError(_preference_format_message())
    return normalized


def _preference_key(preference: str) -> str:
    return preference.strip().casefold()


def _preference_id_for(preference: str) -> str:
    digest = hashlib.sha1(_preference_key(preference).encode("utf-8")).hexdigest()
    return f"pref-{digest[:10]}"


def _coerce_preference_id(value: object, preference: str) -> str:
    raw_id = str(value or "").strip().casefold()
    if _is_valid_preference_id(raw_id):
        return raw_id
    return _preference_id_for(preference)


def _is_valid_preference_id(value: str) -> bool:
    if not value.startswith("pref-") or len(value) != 15:
        return False
    return all(character in "0123456789abcdef" for character in value[5:])


def _resolve_preference_record_index(records: list[dict[str, object]], reference: int | str) -> int | None:
    if isinstance(reference, int):
        return reference - 1 if 1 <= reference <= len(records) else None

    normalized_reference = str(reference or "").strip().casefold()
    if not normalized_reference:
        raise ValueError("偏好引用必须是编号或ID。")
    if normalized_reference.isdigit():
        index = int(normalized_reference)
        return index - 1 if 1 <= index <= len(records) else None
    if not _is_valid_preference_id(normalized_reference):
        raise ValueError("偏好引用必须是编号或ID。")

    for index, record in enumerate(records):
        preference = str(record.get("preference") or "").strip()
        preference_id = _coerce_preference_id(record.get("id"), preference)
        if preference_id == normalized_reference:
            return index
    return None


def _coerce_enabled(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().casefold() in {"1", "true", "yes", "enabled", "已启用"}
    return False


def _preference_format_message() -> str:
    return "偏好候选格式：偏好内容不能为空。"


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(keyword in text for keyword in keywords)


def _format_conflict_preference(preference: Preference) -> str:
    return f"{preference.preference_id} {preference.preference}"


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


_CONFLICT_RULES: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
    ("回答长度", ("简洁", "简短", "精简", "短回答"), ("详细", "详尽", "展开", "完整说明")),
    ("回复语言", ("中文", "汉语"), ("英文", "英语")),
)


_PREFERENCE_LOCAL_ANSWER_TYPE_LABELS: dict[str, str] = {
    "knowledge": "本地知识库回答",
    "memory": "长期记忆兜底回答",
}


_PREFERENCE_LOCAL_ANSWER_DEFAULT_TYPES: tuple[str, ...] = tuple(_PREFERENCE_LOCAL_ANSWER_TYPE_LABELS)


_PREFERENCE_LOCAL_ANSWER_TYPE_ALIASES: dict[str, str] = {
    "knowledge": "knowledge",
    "kb": "knowledge",
    "本地知识库": "knowledge",
    "知识库": "knowledge",
    "本地知识库回答": "knowledge",
    "memory": "memory",
    "长期记忆": "memory",
    "记忆": "memory",
    "长期记忆兜底": "memory",
    "长期记忆兜底回答": "memory",
}
