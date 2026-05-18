from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from .config import ProjectPaths


class ToolNotAllowedError(ValueError):
    """请求了第一阶段白名单之外的工具。"""


@dataclass(frozen=True)
class ToolResult:
    name: str
    success: bool
    message: str
    output: str = ""


class ToolRegistry:
    """第一阶段本地工具注册表。"""

    allowed_tool_names = {
        "list_data",
        "read_data_file",
        "write_note",
        "write_summary",
        "record_log",
    }

    def __init__(self, paths: ProjectPaths):
        self.paths = paths
        self._handlers: dict[str, Callable[..., ToolResult]] = {
            "list_data": self._list_data,
            "read_data_file": self._read_data_file,
            "write_note": self._write_note,
            "write_summary": self._write_summary,
            "record_log": self._record_log_tool,
        }

    def run(self, name: str, **kwargs: Any) -> ToolResult:
        if name not in self.allowed_tool_names:
            raise ToolNotAllowedError(f"工具不在第一阶段白名单中：{name}")

        if name != "record_log":
            self._append_log(name, f"准备执行：{self._format_kwargs(kwargs)}")

        return self._handlers[name](**kwargs)

    def _list_data(self, path: str = ".") -> ToolResult:
        target = self._resolve_inside(self.paths.data_dir, path)
        if not target.exists():
            return ToolResult("list_data", False, f"路径不存在：{path}")

        if target.is_file():
            output = target.name
        else:
            names = []
            for child in sorted(target.iterdir(), key=lambda item: item.name.lower()):
                if child.name.startswith("."):
                    continue
                names.append(f"{child.name}/" if child.is_dir() else child.name)
            output = "\n".join(names) if names else "data 目录为空。"

        return ToolResult("list_data", True, "已列出 data 目录。", output)

    def _read_data_file(self, path: str) -> ToolResult:
        target = self._resolve_inside(self.paths.data_dir, path)
        if not target.is_file():
            return ToolResult("read_data_file", False, f"文件不存在：{path}")

        return ToolResult(
            "read_data_file",
            True,
            f"已读取文件：{path}",
            target.read_text(encoding="utf-8"),
        )

    def _write_note(self, title: str, content: str) -> ToolResult:
        filename = self._markdown_filename(title)
        target = self.paths.notes_dir / filename
        target.write_text(f"# {target.stem}\n\n{content.strip()}\n", encoding="utf-8")
        return ToolResult("write_note", True, f"已写入笔记：{target.relative_to(self.paths.root)}")

    def _write_summary(self, filename: str, content: str) -> ToolResult:
        target = self._resolve_inside(self.paths.word_dir, self._markdown_filename(filename))
        target.write_text(f"# {target.stem}\n\n{content.strip()}\n", encoding="utf-8")
        return ToolResult("write_summary", True, f"已写入总结：{target.relative_to(self.paths.root)}")

    def _record_log_tool(self, message: str) -> ToolResult:
        line = self._append_log("record_log", message)
        return ToolResult("record_log", True, "日志已记录。", line)

    def _append_log(self, action: str, detail: str) -> str:
        self.paths.logs_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().isoformat(timespec="seconds")
        line = f"{timestamp}\t{action}\t{detail}\n"
        with self.paths.log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(line)
        return line

    def _resolve_inside(self, base_dir: Path, relative_path: str) -> Path:
        base = base_dir.resolve()
        target = (base / relative_path).resolve()
        if target != base and base not in target.parents:
            raise ValueError(f"路径必须位于 {base_dir.name}/ 目录内：{relative_path}")
        return target

    def _markdown_filename(self, value: str) -> str:
        name = Path(value.strip()).name
        if not name:
            raise ValueError("文件名不能为空。")
        return name if name.endswith(".md") else f"{name}.md"

    def _format_kwargs(self, kwargs: dict[str, Any]) -> str:
        if not kwargs:
            return "无参数"
        return ", ".join(f"{key}={value!r}" for key, value in sorted(kwargs.items()))
