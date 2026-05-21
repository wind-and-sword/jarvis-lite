from __future__ import annotations

import re

from .config import ProjectPaths


DEFAULT_PROFILE_MESSAGE = "还没有长期记忆。可以先在 memory/profile.md 里记录用户偏好和项目目标。"
PROFILE_HEADER = "# 长期记忆\n\n> 日期：2026-05-18\n> 执行者：Codex\n"


def read_profile(paths: ProjectPaths) -> str:
    """读取长期记忆文件；缺失时返回清晰的可展示说明。"""

    if not paths.profile_path.exists():
        return DEFAULT_PROFILE_MESSAGE

    content = paths.profile_path.read_text(encoding="utf-8").strip()
    if not content:
        return DEFAULT_PROFILE_MESSAGE

    return content


def summarize_profile(content: str) -> str:
    """提取第一条有意义的记忆，作为普通对话的简短上下文。"""

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith(">"):
            continue
        if line.startswith("- ") or line.startswith("* "):
            return line[2:].strip()
        return line

    return DEFAULT_PROFILE_MESSAGE


def append_memory(paths: ProjectPaths, fact: str) -> str:
    """向长期记忆追加一条事实，重复事实不重复写入。"""

    normalized = fact.strip().lstrip("-").strip()
    if not normalized:
        raise ValueError("记忆内容不能为空。")

    existing = "" if not paths.profile_path.exists() else paths.profile_path.read_text(encoding="utf-8")
    bullet = f"- {normalized}"
    if bullet in existing:
        return normalized

    if not existing.strip():
        content = f"{PROFILE_HEADER}\n{bullet}\n"
    else:
        content = _replace_or_append_bullet(existing, normalized)

    paths.profile_path.write_text(content, encoding="utf-8")
    return normalized


def find_identity(content: str) -> str:
    """从长期记忆中提取用户身份回答。"""

    name = _find_memory_value(content, "用户姓名")
    role = _find_memory_value(content, "用户身份")

    if name and role:
        return f"你是{name}，{role}。"
    if name:
        return f"你是{name}。"
    if role:
        return f"你是{role}。"
    return ""


def parse_identity_fact(text: str) -> str:
    """从简单中文自我介绍中解析可写入的身份事实。"""

    prompt = text.strip().strip("。！？!?.")
    if _looks_like_question(prompt):
        return ""

    name_match = re.fullmatch(r"我叫\s*(.+)", prompt)
    if name_match:
        name = name_match.group(1).strip()
        if name:
            return f"用户姓名：{name}"

    role_match = re.fullmatch(r"我是\s*(.+)", prompt)
    if role_match:
        role = role_match.group(1).strip()
        if role:
            return f"用户身份：{role}"

    remember_match = re.fullmatch(r"记住\s*(.+)", prompt)
    if remember_match:
        fact = remember_match.group(1).strip()
        if fact:
            return fact

    return ""


def is_identity_question(text: str) -> bool:
    prompt = text.strip().strip("。！？!?.")
    direct_questions = {
        "我是谁",
        "你知道我是谁吗",
        "你知道我是谁",
        "知道我是谁吗",
        "我是你的什么人",
        "我是你的什么人你知道吗",
    }
    normalized_prompt = re.sub(r"[，,\s]", "", prompt)
    return prompt in direct_questions or normalized_prompt in direct_questions


def _find_memory_value(content: str, key: str) -> str:
    for raw_line in content.splitlines():
        line = raw_line.strip()
        prefix = f"- {key}："
        if line.startswith(prefix):
            return line.removeprefix(prefix).strip()
    return ""


def _replace_or_append_bullet(existing: str, normalized: str) -> str:
    key = _memory_key(normalized)
    if not key:
        return existing.rstrip() + f"\n- {normalized}\n"

    replaced = False
    lines = []
    prefix = f"- {key}："
    for raw_line in existing.rstrip().splitlines():
        if raw_line.strip().startswith(prefix):
            if not replaced:
                lines.append(f"- {normalized}")
                replaced = True
            continue
        lines.append(raw_line)

    if not replaced:
        lines.append(f"- {normalized}")

    return "\n".join(lines).rstrip() + "\n"


def _memory_key(normalized: str) -> str:
    if "：" not in normalized:
        return ""
    key, value = normalized.split("：", 1)
    if not key.strip() or not value.strip():
        return ""
    return key.strip()


def _looks_like_question(prompt: str) -> bool:
    return any(marker in prompt for marker in ("?", "？", "吗", "什么", "谁", "知道"))
