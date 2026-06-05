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
) -> Preference:
    """新增或更新本地偏好，不改变当前回复风格或执行决策。"""

    normalized_preference = _normalize_preference(preference)
    now = _now_iso()
    payload = _read_preferences_payload(paths)
    records = _valid_preference_records(payload.get("preferences"))

    saved = Preference(
        preference=normalized_preference,
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


def describe_preferences(paths: ProjectPaths) -> str:
    """展示本地偏好，只读展示，不触发回复或执行策略变更。"""

    preferences = read_preferences(paths)
    lines = [f"偏好：{len(preferences)} 条"]
    for preference in preferences:
        lines.append(f"- {preference.preference}")
    if preferences:
        lines.append("说明：本阶段只持久化和展示偏好，不自动改变回复或执行决策。")
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


def _valid_preference_records(records: object) -> list[dict[str, str]]:
    if not isinstance(records, list):
        return []

    valid_records: list[dict[str, str]] = []
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
        source=str(record.get("source") or "").strip(),
        created_at=str(record.get("created_at") or "").strip(),
        updated_at=str(record.get("updated_at") or "").strip(),
    )


def _preference_to_record(preference: Preference) -> dict[str, str]:
    return {
        "preference": preference.preference,
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


def _preference_format_message() -> str:
    return "偏好候选格式：偏好内容不能为空。"


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
