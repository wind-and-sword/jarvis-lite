from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .config import ProjectPaths


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
