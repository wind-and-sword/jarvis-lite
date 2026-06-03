from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from .config import ProjectPaths
from .knowledge import build_knowledge_index
from .memory import list_recent_experiences, read_profile, summarize_profile
from .runtime_context import RuntimeContext, load_runtime_context


DIRECTORIES_FILENAME = "directories.json"
HotkeyExecutor = Callable[[tuple[str, ...]], None]
MouseClickExecutor = Callable[[int, int, str], None]
TextInputExecutor = Callable[[str], None]
MOUSE_BUTTONS = {"left", "right", "middle"}


@dataclass(frozen=True)
class CommonDirectory:
    alias: str
    path: Path


@dataclass(frozen=True)
class DailyReport:
    path: Path
    relative_path: str


@dataclass(frozen=True)
class DirectoryOpenRecord:
    path: Path
    relative_path: str


@dataclass(frozen=True)
class FileOrganizationGroup:
    extension_label: str
    target_folder: str
    files: tuple[str, ...]


@dataclass(frozen=True)
class FileOrganizationPreview:
    directory: Path
    groups: tuple[FileOrganizationGroup, ...]
    skipped_directory_count: int

    @property
    def file_count(self) -> int:
        return sum(len(group.files) for group in self.groups)


@dataclass(frozen=True)
class RecentFile:
    alias: str
    path: Path
    modified_at: datetime


@dataclass(frozen=True)
class HotkeyAutomationResult:
    hotkeys: tuple[tuple[str, ...], ...]
    executed_at: datetime


@dataclass(frozen=True)
class MouseClickRequest:
    x: int
    y: int
    button: str


@dataclass(frozen=True)
class MouseClickAutomationResult:
    request: MouseClickRequest
    executed_at: datetime


@dataclass(frozen=True)
class TextInputRequest:
    text: str

    @property
    def character_count(self) -> int:
        return len(self.text)


@dataclass(frozen=True)
class TextInputAutomationResult:
    request: TextInputRequest
    executed_at: datetime


def describe_automation(paths: ProjectPaths) -> str:
    """输出阶段 4 工作台自动化状态。"""

    directories = list_common_directories(paths)
    lines = [
        "阶段 4 自动化状态：",
        f"- 常用目录：{len(directories)} 个",
        "- 日报目录：word",
        "- 当前能力：/dir-add、/dirs、/recent-files、/daily-report、/organize-preview、/dir-open、/hotkey、/mouse-click、/type-text、/window-focus、/app-launch、/chrome-open、/chrome-search、/clash-open、/clash-focus、/qq-open、/qq-focus、/wechat-open、/wechat-focus",
        "- 硬件入口：摄像头、麦克风暂缓",
    ]
    if directories:
        lines.append("- 常用目录列表：")
        for directory in directories:
            lines.append(f"  - {directory.alias}：{directory.path}")
    return "\n".join(lines)


def parse_hotkey_sequence(sequence: str) -> tuple[tuple[str, ...], ...]:
    """解析一个或多个快捷键组合，例如 ctrl+l alt+tab。"""

    raw_sequence = sequence.strip()
    if not raw_sequence:
        raise ValueError("快捷键不能为空。")

    hotkeys: list[tuple[str, ...]] = []
    for raw_hotkey in raw_sequence.split():
        raw_parts = raw_hotkey.split("+")
        keys = tuple(part.strip().casefold() for part in raw_parts if part.strip())
        if not keys or len(keys) != len(raw_parts):
            raise ValueError(f"快捷键组合不完整：{raw_hotkey}")
        hotkeys.append(keys)
    return tuple(hotkeys)


def execute_hotkey_sequence(
    sequence: str,
    *,
    executor: HotkeyExecutor | None = None,
) -> HotkeyAutomationResult:
    """按顺序发送显式快捷键组合。"""

    hotkeys = parse_hotkey_sequence(sequence)
    hotkey_executor = executor or _execute_hotkey_with_pyautogui
    for hotkey in hotkeys:
        hotkey_executor(hotkey)
    return HotkeyAutomationResult(hotkeys=hotkeys, executed_at=datetime.now())


def describe_hotkey_automation(
    paths: ProjectPaths,
    sequence: str,
    *,
    executor: HotkeyExecutor | None = None,
) -> str:
    result = execute_hotkey_sequence(sequence, executor=executor)
    lines = [
        f"快捷键执行：{len(result.hotkeys)} 组",
        f"时间：{result.executed_at.isoformat(timespec='seconds')}",
    ]
    for index, hotkey in enumerate(result.hotkeys, start=1):
        lines.append(f"{index}. {'+'.join(hotkey)}")
    lines.append("说明：当前阶段只发送显式快捷键，不点击、不输入文本、不切换窗口。")
    return "\n".join(lines)


def parse_mouse_click_request(command: str) -> MouseClickRequest:
    """解析显式鼠标点击坐标和按钮参数。"""

    parts = command.strip().split()
    if len(parts) < 2:
        raise ValueError("鼠标点击需要 x y 坐标。")
    if len(parts) > 3:
        raise ValueError("鼠标点击只支持 x y 和一个 button=... 参数。")

    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError as exc:
        raise ValueError("坐标必须是整数。") from exc

    button = "left"
    if len(parts) == 3:
        raw_button = parts[2]
        if not raw_button.casefold().startswith("button="):
            raise ValueError("第三个参数必须是 button=left|right|middle。")
        button = raw_button.split("=", 1)[1].strip().casefold()

    if button not in MOUSE_BUTTONS:
        raise ValueError(f"不支持的鼠标按钮：{button}")

    return MouseClickRequest(x=x, y=y, button=button)


def execute_mouse_click(
    command: str,
    *,
    executor: MouseClickExecutor | None = None,
) -> MouseClickAutomationResult:
    """执行一次显式坐标鼠标点击。"""

    request = parse_mouse_click_request(command)
    mouse_executor = executor or _execute_mouse_click_with_pyautogui
    mouse_executor(request.x, request.y, request.button)
    return MouseClickAutomationResult(request=request, executed_at=datetime.now())


def describe_mouse_click_automation(
    paths: ProjectPaths,
    command: str,
    *,
    executor: MouseClickExecutor | None = None,
) -> str:
    result = execute_mouse_click(command, executor=executor)
    request = result.request
    return "\n".join(
        [
            f"鼠标点击执行：{request.button} @ ({request.x}, {request.y})",
            f"时间：{result.executed_at.isoformat(timespec='seconds')}",
            "说明：当前阶段只执行显式坐标点击，不做目标识别、不拖动、不切换窗口。",
        ]
    )


def parse_text_input_request(command: str) -> TextInputRequest:
    """解析显式文本输入内容。"""

    text = command.strip()
    if not text:
        raise ValueError("文本输入内容不能为空。")
    return TextInputRequest(text=text)


def execute_text_input(
    command: str,
    *,
    executor: TextInputExecutor | None = None,
) -> TextInputAutomationResult:
    """向当前焦点输入显式文本。"""

    request = parse_text_input_request(command)
    text_executor = executor or _execute_text_input_with_pyautogui
    text_executor(request.text)
    return TextInputAutomationResult(request=request, executed_at=datetime.now())


def describe_text_input_automation(
    paths: ProjectPaths,
    command: str,
    *,
    executor: TextInputExecutor | None = None,
) -> str:
    result = execute_text_input(command, executor=executor)
    request = result.request
    return "\n".join(
        [
            f"文本输入执行：{request.character_count} 个字符",
            f"时间：{result.executed_at.isoformat(timespec='seconds')}",
            "说明：当前阶段只向当前焦点输入显式文本，不点击、不切换窗口、不启动应用。",
        ]
    )


def add_common_directory(paths: ProjectPaths, alias: str, directory: str | Path) -> CommonDirectory:
    """登记常用目录，供后续桌面自动化复用。"""

    normalized_alias = _normalize_alias(alias)
    target = Path(directory).expanduser().resolve()
    if not target.is_dir():
        raise FileNotFoundError(f"目录不存在：{directory}")

    registry = _read_directories(paths)
    registry[normalized_alias] = str(target)
    _write_directories(paths, registry)
    return CommonDirectory(normalized_alias, target)


def list_common_directories(paths: ProjectPaths) -> tuple[CommonDirectory, ...]:
    """读取已登记的常用目录。"""

    registry = _read_directories(paths)
    directories = [
        CommonDirectory(alias=alias, path=Path(directory_path))
        for alias, directory_path in sorted(registry.items(), key=lambda item: item[0].lower())
    ]
    return tuple(directories)


def write_daily_report(paths: ProjectPaths, filename: str | None = None) -> DailyReport:
    """生成工作日报到 word 目录。"""

    target = paths.word_dir / _report_filename(filename)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_daily_report_content(paths), encoding="utf-8")
    return DailyReport(target, target.relative_to(paths.root).as_posix())


def record_directory_open_request(paths: ProjectPaths, alias: str, directory: str | Path) -> DirectoryOpenRecord:
    """记录打开常用目录的请求，当前不启动外部应用。"""

    target = Path(directory).expanduser().resolve()
    if not target.is_dir():
        raise FileNotFoundError(f"目录不存在：{directory}")

    transcript_path = paths.logs_dir / "desktop-actions.txt"
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')}\topen_directory\t{alias}\t{target}\n"
    with transcript_path.open("a", encoding="utf-8") as file:
        file.write(line)
    return DirectoryOpenRecord(transcript_path, transcript_path.relative_to(paths.root).as_posix())


def preview_file_organization(directory: str | Path) -> FileOrganizationPreview:
    """按扩展名生成文件整理预览，不移动或删除文件。"""

    target = Path(directory).expanduser().resolve()
    if not target.is_dir():
        raise FileNotFoundError(f"目录不存在：{directory}")

    grouped_files: dict[tuple[str, str], list[str]] = {}
    skipped_directory_count = 0
    for item in sorted(target.iterdir(), key=lambda path: path.name.lower()):
        if item.is_dir():
            skipped_directory_count += 1
            continue
        if not item.is_file():
            continue
        extension_label, target_folder = _organization_bucket(item)
        grouped_files.setdefault((extension_label, target_folder), []).append(item.name)

    groups = tuple(
        FileOrganizationGroup(extension_label=label, target_folder=folder, files=tuple(files))
        for (label, folder), files in sorted(grouped_files.items(), key=lambda item: item[0][1])
    )
    return FileOrganizationPreview(target, groups, skipped_directory_count)


def list_recent_files(directories: tuple[CommonDirectory, ...], limit: int = 5) -> tuple[RecentFile, ...]:
    """列出一组目录顶层最近修改的普通文件。"""

    if limit <= 0:
        return ()

    recent_files: list[tuple[float, RecentFile]] = []
    seen_paths: set[str] = set()
    for directory in directories:
        target = Path(directory.path).expanduser().resolve()
        if not target.is_dir():
            continue
        for item in target.iterdir():
            try:
                if item.name.startswith(".") or not item.is_file():
                    continue
                resolved = item.resolve()
                path_key = str(resolved).casefold()
                if path_key in seen_paths:
                    continue
                stat = resolved.stat()
            except OSError:
                continue
            seen_paths.add(path_key)
            recent_files.append(
                (
                    stat.st_mtime,
                    RecentFile(
                        alias=directory.alias,
                        path=resolved,
                        modified_at=datetime.fromtimestamp(stat.st_mtime),
                    ),
                )
            )

    return tuple(
        recent_file
        for _, recent_file in sorted(
            recent_files,
            key=lambda item: (
                -item[0],
                item[1].alias.lower(),
                item[1].path.name.lower(),
            ),
        )[:limit]
    )


def _directories_path(paths: ProjectPaths) -> Path:
    return paths.memory_dir / DIRECTORIES_FILENAME


def _read_directories(paths: ProjectPaths) -> dict[str, str]:
    registry_path = _directories_path(paths)
    if not registry_path.exists():
        return {}

    raw = json.loads(registry_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}

    registry: dict[str, str] = {}
    for alias, directory_path in raw.items():
        if isinstance(alias, str) and isinstance(directory_path, str):
            registry[alias] = directory_path
    return registry


def _write_directories(paths: ProjectPaths, registry: dict[str, str]) -> None:
    registry_path = _directories_path(paths)
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _normalize_alias(alias: str) -> str:
    normalized = alias.strip()
    if not normalized:
        raise ValueError("目录别名不能为空。")
    return normalized


def _execute_hotkey_with_pyautogui(keys: tuple[str, ...]) -> None:
    try:
        import pyautogui
    except ModuleNotFoundError as exc:
        raise RuntimeError("未安装 pyautogui，无法发送快捷键。") from exc

    pyautogui.hotkey(*keys)


def _execute_mouse_click_with_pyautogui(x: int, y: int, button: str) -> None:
    try:
        import pyautogui
    except ModuleNotFoundError as exc:
        raise RuntimeError("未安装 pyautogui，无法执行鼠标点击。") from exc

    pyautogui.click(x=x, y=y, button=button)


def _execute_text_input_with_pyautogui(text: str) -> None:
    try:
        import pyautogui
        import pyperclip
    except ModuleNotFoundError as exc:
        raise RuntimeError("未安装 pyautogui 或 pyperclip，无法输入文本。") from exc

    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")


def _report_filename(filename: str | None) -> str:
    if not filename:
        return f"{date.today().isoformat()}-daily-report.md"
    name = Path(filename.strip()).name
    if not name:
        raise ValueError("日报文件名不能为空。")
    return name if name.endswith(".md") else f"{name}.md"


def _daily_report_content(paths: ProjectPaths) -> str:
    profile_summary = summarize_profile(read_profile(paths))
    index = build_knowledge_index(paths)
    directories = list_common_directories(paths)
    lines = [
        "# Jarvis Lite 日报",
        "",
        f"> 日期：{date.today().isoformat()}",
        "> 执行者：Codex",
        "",
        "## 长期记忆摘要",
        "",
        f"- {profile_summary}",
        "",
        "## 知识库状态",
        "",
        f"- 知识库资料：{index.document_count} 个",
        f"- 可检索文本行：{index.searchable_line_count} 行",
        "",
        "## 常用目录",
        "",
    ]
    if directories:
        for directory in directories:
            lines.append(f"- {directory.alias}：{directory.path}")
    else:
        lines.append("- 还没有登记常用目录。")

    runtime_context = load_runtime_context(paths)
    lines.extend(["", "## 最近上下文", ""])
    _append_recent_context_lines(lines, runtime_context)

    lines.extend(["", "## 经验记忆", ""])
    recent_experiences = list_recent_experiences(paths)
    if recent_experiences:
        for experience in recent_experiences:
            lines.append(f"- {experience}")
    else:
        lines.append("- 暂无经验记忆。")

    lines.extend(["", "## 最近工具日志", ""])
    recent_logs = _recent_log_lines(paths)
    if recent_logs:
        for line in recent_logs:
            lines.append(f"- {line}")
    else:
        lines.append("- 暂无工具日志。")

    lines.extend(["", "## 下一步建议", ""])
    _append_next_action_lines(lines, runtime_context, recent_experiences, recent_logs)

    return "\n".join(lines).rstrip() + "\n"


def _append_recent_context_lines(lines: list[str], context: RuntimeContext) -> None:
    has_context = any(
        (
            context.recent_document_path,
            context.recent_document_paths,
            context.recent_directory,
            context.recent_files,
            context.recent_search_result_paths,
            context.recent_advice_suggestions,
        )
    )
    if not has_context:
        lines.append("- 暂无最近上下文。")
        return

    if context.recent_document_path:
        lines.append(f"- 最近资料：data/{context.recent_document_path}")
    if context.recent_document_paths:
        lines.append(f"- 最近资料列表：{len(context.recent_document_paths)} 条")
        for index, path in enumerate(context.recent_document_paths, start=1):
            lines.append(f"  {index}. data/{path}")
    if context.recent_directory is not None:
        lines.append(f"- 最近目录：{context.recent_directory.alias} -> {context.recent_directory.path}")
    if context.recent_files:
        lines.append(f"- 最近文件列表：{len(context.recent_files)} 条")
        for index, recent_file in enumerate(context.recent_files, start=1):
            lines.append(f"  {index}. {recent_file.alias} -> {recent_file.path}")
    if context.recent_search_result_paths:
        lines.append(f"- 最近搜索结果：{len(context.recent_search_result_paths)} 条")
        for index, path in enumerate(context.recent_search_result_paths, start=1):
            lines.append(f"  {index}. data/{path}")
    if context.recent_advice_suggestions:
        lines.append(f"- 最近建议：{len(context.recent_advice_suggestions)} 条")
        for index, suggestion in enumerate(context.recent_advice_suggestions, start=1):
            lines.append(f"  {index}. {suggestion}")


def _append_next_action_lines(
    lines: list[str],
    context: RuntimeContext,
    recent_experiences: tuple[str, ...],
    recent_logs: list[str],
) -> None:
    for suggestion in suggest_next_actions_from_context(context, recent_experiences, tuple(recent_logs)):
        lines.append(f"- {suggestion}")


def suggest_next_actions_from_context(
    context: RuntimeContext,
    recent_experiences: tuple[str, ...] = (),
    recent_logs: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """根据运行态上下文生成可跨入口复用的下一步建议。"""

    suggestions: list[str] = []
    if context.recent_document_path:
        suggestions.append(
            f"继续处理最近资料：/read {context.recent_document_path}；/tag {context.recent_document_path} 标签..."
        )
    if context.recent_directory is not None:
        suggestions.append(
            f"继续处理最近目录：/organize-preview {context.recent_directory.alias}；/dir-open {context.recent_directory.alias}"
        )
    if context.recent_files:
        suggestions.append("继续处理最近文件：查看第一份最近文件；导入第一份最近文件到知识库；/recent-files")
    if context.recent_advice_suggestions:
        suggestions.append("继续最近建议：查看第一条建议；执行第一条建议")
    if recent_experiences:
        suggestions.append("复用经验记忆：/experience-advice 关键词")
    if recent_logs:
        suggestions.append("沉淀工具流程：/experience 经验内容")
    if not suggestions:
        suggestions.extend(
            [
                "导入资料：/import 源文件或目录路径 [目标文件名]",
                "登记常用目录：/dir-add 别名 目录路径",
                "记录经验：/experience 经验内容",
            ]
        )

    return tuple(suggestions)


def _recent_log_lines(paths: ProjectPaths, limit: int = 5) -> list[str]:
    if not paths.log_path.exists():
        return []
    lines = [line.strip() for line in paths.log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return lines[-limit:]


def _organization_bucket(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if not suffix:
        return "无后缀", "no-extension"
    return suffix, suffix.removeprefix(".")
