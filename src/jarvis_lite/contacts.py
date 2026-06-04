from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .config import ProjectPaths


CONTACTS_FILENAME = "contacts.local.json"


@dataclass(frozen=True)
class ContactAlias:
    """联系人别名配置项，只保存别名到用户可识别联系人标识的映射。"""

    alias: str
    target: str
    source: str = ""
    created_at: str = ""
    updated_at: str = ""


def parse_contact_alias_candidate(content: str) -> tuple[str, str]:
    """解析联系人别名候选，当前要求显式写出别名和联系人标识。"""

    normalized = content.strip()
    if "=>" in normalized:
        alias, target = normalized.split("=>", 1)
    elif "->" in normalized:
        alias, target = normalized.split("->", 1)
    else:
        raise ValueError(_contact_alias_format_message())

    normalized_alias = _normalize_alias(alias)
    normalized_target = _normalize_target(target)
    return normalized_alias, normalized_target


def read_contact_aliases(paths: ProjectPaths) -> tuple[ContactAlias, ...]:
    """读取联系人别名配置；缺失或损坏时返回空集合。"""

    payload = _read_contacts_payload(paths)
    records = payload.get("contact_aliases")
    if not isinstance(records, list):
        return ()

    aliases: list[ContactAlias] = []
    for record in records:
        alias = _contact_alias_from_record(record)
        if alias is not None:
            aliases.append(alias)
    return tuple(aliases)


def save_contact_alias(
    paths: ProjectPaths,
    alias: str,
    target: str,
    *,
    source: str = "",
) -> ContactAlias:
    """新增或更新联系人别名，不执行真实联系人查找。"""

    normalized_alias = _normalize_alias(alias)
    normalized_target = _normalize_target(target)
    now = _now_iso()
    payload = _read_contacts_payload(paths)
    records = _valid_contact_alias_records(payload.get("contact_aliases"))

    saved = ContactAlias(
        alias=normalized_alias,
        target=normalized_target,
        source=source.strip(),
        created_at=now,
        updated_at=now,
    )
    alias_key = _alias_key(normalized_alias)
    updated_records: list[dict[str, str]] = []
    replaced = False
    for record in records:
        existing_alias = str(record.get("alias") or "").strip()
        if _alias_key(existing_alias) == alias_key:
            saved = ContactAlias(
                alias=normalized_alias,
                target=normalized_target,
                source=source.strip() or str(record.get("source") or "").strip(),
                created_at=str(record.get("created_at") or now),
                updated_at=now,
            )
            updated_records.append(_contact_alias_to_record(saved))
            replaced = True
        else:
            updated_records.append(record)
    if not replaced:
        updated_records.append(_contact_alias_to_record(saved))

    payload["contact_aliases"] = updated_records
    _write_contacts_payload(paths, payload)
    return saved


def remove_contact_alias(paths: ProjectPaths, alias: str) -> bool:
    """按别名删除联系人别名；删除后保留空配置文件，便于撤销留痕。"""

    normalized_alias = _normalize_alias(alias)
    payload = _read_contacts_payload(paths)
    records = _valid_contact_alias_records(payload.get("contact_aliases"))
    alias_key = _alias_key(normalized_alias)
    updated_records = [
        record
        for record in records
        if _alias_key(str(record.get("alias") or "")) != alias_key
    ]
    removed = len(updated_records) != len(records)
    payload["contact_aliases"] = updated_records
    _write_contacts_payload(paths, payload)
    return removed


def contact_alias_count(paths: ProjectPaths) -> int:
    """返回当前已保存联系人别名数量。"""

    return len(read_contact_aliases(paths))


def describe_contact_aliases(paths: ProjectPaths) -> str:
    """展示联系人别名配置，只读展示，不触发消息动作。"""

    aliases = read_contact_aliases(paths)
    lines = [f"联系人别名：{len(aliases)} 个"]
    for alias in aliases:
        lines.append(f"- {alias.alias} -> {alias.target}")
    return "\n".join(lines)


def _contacts_path(paths: ProjectPaths):
    return paths.config_dir / CONTACTS_FILENAME


def _read_contacts_payload(paths: ProjectPaths) -> dict[str, Any]:
    target = _contacts_path(paths)
    if not target.exists():
        return {"contact_aliases": []}
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"contact_aliases": []}
    if not isinstance(payload, dict):
        return {"contact_aliases": []}
    return dict(payload)


def _write_contacts_payload(paths: ProjectPaths, payload: dict[str, Any]) -> None:
    target = _contacts_path(paths)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _valid_contact_alias_records(records: object) -> list[dict[str, str]]:
    if not isinstance(records, list):
        return []

    valid_records: list[dict[str, str]] = []
    for record in records:
        alias = _contact_alias_from_record(record)
        if alias is not None:
            valid_records.append(_contact_alias_to_record(alias))
    return valid_records


def _contact_alias_from_record(record: object) -> ContactAlias | None:
    if not isinstance(record, dict):
        return None
    alias = str(record.get("alias") or "").strip()
    target = str(record.get("target") or "").strip()
    if not alias or not target:
        return None
    return ContactAlias(
        alias=alias,
        target=target,
        source=str(record.get("source") or "").strip(),
        created_at=str(record.get("created_at") or "").strip(),
        updated_at=str(record.get("updated_at") or "").strip(),
    )


def _contact_alias_to_record(alias: ContactAlias) -> dict[str, str]:
    return {
        "alias": alias.alias,
        "target": alias.target,
        "source": alias.source,
        "created_at": alias.created_at,
        "updated_at": alias.updated_at,
    }


def _normalize_alias(alias: str) -> str:
    normalized = alias.strip()
    if not normalized:
        raise ValueError(_contact_alias_format_message())
    return normalized


def _normalize_target(target: str) -> str:
    normalized = target.strip()
    if not normalized:
        raise ValueError(_contact_alias_format_message())
    return normalized


def _alias_key(alias: str) -> str:
    return alias.strip().casefold()


def _contact_alias_format_message() -> str:
    return "联系人别名候选格式：别名 => 联系人标识。"


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
