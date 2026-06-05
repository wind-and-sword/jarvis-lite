from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .config import ProjectPaths


PREFERENCES_FILENAME = "preferences.local.json"


@dataclass(frozen=True)
class Preference:
    """本地偏好记录；第一阶段只做持久化和展示，不自动改变回复策略。"""

    preference: str
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
        enabled=bool(enabled) if enabled is not None else False,
        source=source.strip(),
        created_at=now,
        updated_at=now,
    )
    preference_key = _preference_key(normalized_preference)
    updated_records: list[dict[str, str]] = []
    replaced = False
    for record in records:
        existing_preference = str(record.get("preference") or "").strip()
        if _preference_key(existing_preference) == preference_key:
            saved = Preference(
                preference=normalized_preference,
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


def set_preference_enabled(paths: ProjectPaths, index: int, enabled: bool) -> Preference:
    """按 1 基编号切换偏好启用状态；不自动应用到回复或执行路径。"""

    payload = _read_preferences_payload(paths)
    records = _valid_preference_records(payload.get("preferences"))
    if index < 1 or index > len(records):
        raise ValueError("偏好编号不存在。可用 /preference-status 查看本地偏好。")

    now = _now_iso()
    target_record = records[index - 1]
    updated = Preference(
        preference=str(target_record.get("preference") or "").strip(),
        enabled=enabled,
        source=str(target_record.get("source") or "").strip(),
        created_at=str(target_record.get("created_at") or now),
        updated_at=now,
    )
    records[index - 1] = _preference_to_record(updated)
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
        lines.append(f"{index}. {state} {preference.preference}")
    lines.extend(
        [
            "说明：启用状态只用于本地可审计管理，不自动改变回复风格、LLM prompt、路由或执行决策。",
            "可用 /preference-enable 编号 启用，/preference-disable 编号 停用。",
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
            lines.append(f"{index}. {preference.preference}")
    else:
        lines.append("暂无已启用偏好。可用 /preference-enable 编号 启用。")
    lines.extend(
        [
            "应用策略草案：已启用偏好只作为显式预览内容展示。",
            "说明：当前不自动改变回复风格、LLM prompt、路由或执行决策。",
        ]
    )
    return "\n".join(lines)


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
        enabled=_coerce_enabled(record.get("enabled")),
        source=str(record.get("source") or "").strip(),
        created_at=str(record.get("created_at") or "").strip(),
        updated_at=str(record.get("updated_at") or "").strip(),
    )


def _preference_to_record(preference: Preference) -> dict[str, object]:
    return {
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


def _coerce_enabled(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().casefold() in {"1", "true", "yes", "enabled", "已启用"}
    return False


def _preference_format_message() -> str:
    return "偏好候选格式：偏好内容不能为空。"


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
