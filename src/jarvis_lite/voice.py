from __future__ import annotations

import base64
import os
import platform
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .config import ProjectPaths


DEFAULT_VOICE_ENGINE = "auto"
VOICE_ENGINE_ENV = "JARVIS_LITE_VOICE_ENGINE"


@dataclass(frozen=True)
class VoiceResult:
    success: bool
    message: str
    transcript_path: Path


def describe_voice(paths: ProjectPaths, engine: str | None = None) -> str:
    """描述当前语音入口配置，方便用户确认阶段 3 状态。"""

    selected_engine = _resolve_engine(engine)
    actual_engine = _actual_engine(selected_engine)
    transcript = _voice_transcript_path(paths)
    return "\n".join(
        [
            "语音入口状态：",
            f"- 当前引擎：{actual_engine}",
            f"- 播报记录：{_project_path(paths, transcript)}",
            "- 语音输入：当前支持 /voice 文本 作为已识别语音文本入口",
            "- 麦克风识别：尚未接入",
        ]
    )


def speak_text(paths: ProjectPaths, text: str, engine: str | None = None) -> VoiceResult:
    """播报文本；自动化测试可使用 transcript 引擎避免依赖扬声器。"""

    content = text.strip()
    if not content:
        raise ValueError("播报内容不能为空。")

    transcript_path = _append_voice_transcript(paths, content)
    selected_engine = _resolve_engine(engine)
    actual_engine = _actual_engine(selected_engine)
    if actual_engine == "transcript":
        return VoiceResult(True, f"已记录语音播报文本：{_project_path(paths, transcript_path)}", transcript_path)

    _speak_with_windows(content)
    return VoiceResult(True, "已通过 Windows 语音引擎播报。", transcript_path)


def _resolve_engine(engine: str | None) -> str:
    return (engine or os.environ.get(VOICE_ENGINE_ENV) or DEFAULT_VOICE_ENGINE).strip().lower()


def _actual_engine(engine: str) -> str:
    if engine in {"transcript", "text"}:
        return "transcript"
    if engine == "windows":
        return "windows"
    if engine == "auto" and platform.system().lower() == "windows" and shutil.which("powershell"):
        return "windows"
    return "transcript"


def _voice_transcript_path(paths: ProjectPaths) -> Path:
    return paths.logs_dir / "voice-output.txt"


def _append_voice_transcript(paths: ProjectPaths, text: str) -> Path:
    paths.logs_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = _voice_transcript_path(paths)
    timestamp = datetime.now().isoformat(timespec="seconds")
    with transcript_path.open("a", encoding="utf-8") as file:
        file.write(f"{timestamp}\t{text}\n")
    return transcript_path


def _speak_with_windows(text: str) -> None:
    powershell = shutil.which("powershell")
    if not powershell:
        raise RuntimeError("未找到 powershell，无法使用 Windows 语音引擎。")

    text_base64 = base64.b64encode(text.encode("utf-8")).decode("ascii")
    script = "\n".join(
        [
            "Add-Type -AssemblyName System.Speech",
            f"$bytes = [Convert]::FromBase64String('{text_base64}')",
            "$text = [Text.Encoding]::UTF8.GetString($bytes)",
            "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer",
            "$speaker.Speak($text)",
        ]
    )
    encoded = base64.b64encode(script.encode("utf-16le")).decode("ascii")
    completed = subprocess.run(
        [powershell, "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "未知错误").strip()
        raise RuntimeError(f"Windows 语音播报失败：{detail}")


def _project_path(paths: ProjectPaths, path: Path) -> str:
    return path.relative_to(paths.root).as_posix()
