from __future__ import annotations

from .config import ProjectPaths


DEFAULT_PROFILE_MESSAGE = "还没有长期记忆。可以先在 memory/profile.md 里记录用户偏好和项目目标。"


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
