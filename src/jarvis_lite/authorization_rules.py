from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .config import ProjectPaths


AUTHORIZATION_RULES_FILENAME = "authorization.local.json"


@dataclass(frozen=True)
class AuthorizationRule:
    """本地授权规则记录；第一阶段只做持久化和展示，不改变执行决策。"""

    rule: str
    source: str = ""
    created_at: str = ""
    updated_at: str = ""


def parse_authorization_rule_candidate(content: str) -> str:
    """解析授权规则候选，当前要求候选内容本身就是明确规则文本。"""

    return _normalize_rule(content)


def read_authorization_rules(paths: ProjectPaths) -> tuple[AuthorizationRule, ...]:
    """读取本地授权规则；缺失或损坏时返回空集合。"""

    payload = _read_authorization_payload(paths)
    records = payload.get("rules")
    if not isinstance(records, list):
        return ()

    rules: list[AuthorizationRule] = []
    for record in records:
        rule = _authorization_rule_from_record(record)
        if rule is not None:
            rules.append(rule)
    return tuple(rules)


def save_authorization_rule(
    paths: ProjectPaths,
    rule: str,
    *,
    source: str = "",
) -> AuthorizationRule:
    """新增或更新本地授权规则，不放行或阻断任何命令。"""

    normalized_rule = _normalize_rule(rule)
    now = _now_iso()
    payload = _read_authorization_payload(paths)
    records = _valid_authorization_rule_records(payload.get("rules"))

    saved = AuthorizationRule(
        rule=normalized_rule,
        source=source.strip(),
        created_at=now,
        updated_at=now,
    )
    rule_key = _rule_key(normalized_rule)
    updated_records: list[dict[str, str]] = []
    replaced = False
    for record in records:
        existing_rule = str(record.get("rule") or "").strip()
        if _rule_key(existing_rule) == rule_key:
            saved = AuthorizationRule(
                rule=normalized_rule,
                source=source.strip() or str(record.get("source") or "").strip(),
                created_at=str(record.get("created_at") or now),
                updated_at=now,
            )
            updated_records.append(_authorization_rule_to_record(saved))
            replaced = True
        else:
            updated_records.append(record)
    if not replaced:
        updated_records.append(_authorization_rule_to_record(saved))

    payload["rules"] = updated_records
    _write_authorization_payload(paths, payload)
    return saved


def remove_authorization_rule(paths: ProjectPaths, rule: str) -> bool:
    """按规则文本删除本地授权规则；删除后保留空配置文件。"""

    normalized_rule = _normalize_rule(rule)
    payload = _read_authorization_payload(paths)
    records = _valid_authorization_rule_records(payload.get("rules"))
    rule_key = _rule_key(normalized_rule)
    updated_records = [
        record
        for record in records
        if _rule_key(str(record.get("rule") or "")) != rule_key
    ]
    removed = len(updated_records) != len(records)
    payload["rules"] = updated_records
    _write_authorization_payload(paths, payload)
    return removed


def authorization_rule_count(paths: ProjectPaths) -> int:
    """返回当前已保存授权规则数量。"""

    return len(read_authorization_rules(paths))


def describe_authorization_rules(paths: ProjectPaths) -> str:
    """展示本地授权规则，只读展示，不触发执行决策变更。"""

    rules = read_authorization_rules(paths)
    lines = [f"本地授权规则：{len(rules)} 条"]
    for rule in rules:
        lines.append(f"- {rule.rule}")
    if rules:
        lines.append("说明：本阶段只持久化和展示规则，不自动改变命令执行决策。")
    return "\n".join(lines)


def _authorization_path(paths: ProjectPaths):
    return paths.config_dir / AUTHORIZATION_RULES_FILENAME


def _read_authorization_payload(paths: ProjectPaths) -> dict[str, Any]:
    target = _authorization_path(paths)
    if not target.exists():
        return {"rules": []}
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"rules": []}
    if not isinstance(payload, dict):
        return {"rules": []}
    return dict(payload)


def _write_authorization_payload(paths: ProjectPaths, payload: dict[str, Any]) -> None:
    target = _authorization_path(paths)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _valid_authorization_rule_records(records: object) -> list[dict[str, str]]:
    if not isinstance(records, list):
        return []

    valid_records: list[dict[str, str]] = []
    for record in records:
        rule = _authorization_rule_from_record(record)
        if rule is not None:
            valid_records.append(_authorization_rule_to_record(rule))
    return valid_records


def _authorization_rule_from_record(record: object) -> AuthorizationRule | None:
    if not isinstance(record, dict):
        return None
    rule = str(record.get("rule") or "").strip()
    if not rule:
        return None
    return AuthorizationRule(
        rule=rule,
        source=str(record.get("source") or "").strip(),
        created_at=str(record.get("created_at") or "").strip(),
        updated_at=str(record.get("updated_at") or "").strip(),
    )


def _authorization_rule_to_record(rule: AuthorizationRule) -> dict[str, str]:
    return {
        "rule": rule.rule,
        "source": rule.source,
        "created_at": rule.created_at,
        "updated_at": rule.updated_at,
    }


def _normalize_rule(rule: str) -> str:
    normalized = rule.strip()
    if not normalized:
        raise ValueError(_authorization_rule_format_message())
    return normalized


def _rule_key(rule: str) -> str:
    return rule.strip().casefold()


def _authorization_rule_format_message() -> str:
    return "授权规则候选格式：规则内容不能为空。"


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
