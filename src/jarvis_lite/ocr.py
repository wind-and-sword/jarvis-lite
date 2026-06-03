from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from .config import ProjectPaths


DEFAULT_OCR_LANGUAGE = "chi_sim+eng"
OCR_PROVIDER = "tesseract-cli"

OcrProbe = Callable[[], "OcrAvailability"]
ImageRecognizer = Callable[[Path, str], str]


@dataclass(frozen=True)
class OcrAvailability:
    provider: str
    available: bool
    command: str | None
    version: str | None
    reason: str | None


def describe_ocr_status(paths: ProjectPaths, *, probe: OcrProbe | None = None) -> str:
    """返回当前 OCR 引擎可用性，不读取图片、不执行识别。"""

    availability = (probe or probe_tesseract_availability)()
    status = "可用" if availability.available else "不可用"
    lines = [
        f"OCR 状态：{status}",
        f"Provider：{availability.provider}",
        f"默认语言：{DEFAULT_OCR_LANGUAGE}",
    ]
    if availability.command:
        lines.append(f"命令：{availability.command}")
    if availability.version:
        lines.append(f"版本：{availability.version}")
    if availability.reason:
        lines.append(f"原因：{availability.reason}")
    lines.append("说明：当前阶段只识别指定图片，不截图、不点击、不切换窗口。")
    return "\n".join(lines)


def describe_image_ocr(
    paths: ProjectPaths,
    image_path: str,
    *,
    language: str | None = None,
    recognizer: ImageRecognizer | None = None,
) -> str:
    requested = image_path.strip()
    if not requested:
        return "用法：/ocr-image 图片路径 [lang=chi_sim+eng]"

    source_path = _resolve_image_path(paths.root, requested)
    if not source_path.is_file():
        return f"OCR 图片识别失败：图片不存在：{requested}"

    effective_language = language.strip() if language and language.strip() else DEFAULT_OCR_LANGUAGE
    try:
        text = (recognizer or recognize_image_text)(source_path, effective_language).strip()
    except RuntimeError as exc:
        return f"OCR 图片识别失败：{exc}"

    if not text:
        text = "（未识别到文字）"
    display_path = _display_path(paths.root, source_path)
    return "\n".join(
        [
            f"OCR 图片识别：{display_path}",
            f"Provider：{OCR_PROVIDER}",
            f"语言：{effective_language}",
            "文本：",
            text,
            "说明：当前阶段只识别指定图片，不截图、不点击、不切换窗口。",
        ]
    )


def probe_tesseract_availability() -> OcrAvailability:
    command = _resolve_tesseract_command()
    if command is None:
        return OcrAvailability(
            provider=OCR_PROVIDER,
            available=False,
            command=None,
            version=None,
            reason="未找到 tesseract.exe；请安装 Tesseract CLI，或设置 JARVIS_LITE_TESSERACT_CMD。",
        )

    try:
        completed = subprocess.run(
            [command, "--version"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except OSError as exc:
        return OcrAvailability(
            provider=OCR_PROVIDER,
            available=False,
            command=command,
            version=None,
            reason=f"无法执行 tesseract：{exc}",
        )
    except subprocess.TimeoutExpired:
        return OcrAvailability(
            provider=OCR_PROVIDER,
            available=False,
            command=command,
            version=None,
            reason="执行 tesseract --version 超时。",
        )

    output = "\n".join([completed.stdout, completed.stderr])
    version = next((line.strip() for line in output.splitlines() if line.strip()), None)
    if completed.returncode != 0:
        return OcrAvailability(
            provider=OCR_PROVIDER,
            available=False,
            command=command,
            version=version,
            reason=f"执行 tesseract --version 失败，退出码 {completed.returncode}。",
        )
    return OcrAvailability(
        provider=OCR_PROVIDER,
        available=True,
        command=command,
        version=version,
        reason=None,
    )


def recognize_image_text(image_path: Path, language: str) -> str:
    availability = probe_tesseract_availability()
    if not availability.available or availability.command is None:
        raise RuntimeError(availability.reason or "OCR 引擎不可用。")

    try:
        completed = subprocess.run(
            [availability.command, str(image_path), "stdout", "-l", language],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
    except OSError as exc:
        raise RuntimeError(f"无法执行 tesseract：{exc}") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Tesseract OCR 超时。") from exc

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        if not detail:
            detail = f"退出码 {completed.returncode}"
        raise RuntimeError(f"Tesseract OCR 失败：{detail}")
    return completed.stdout


def _resolve_tesseract_command() -> str | None:
    configured = os.environ.get("JARVIS_LITE_TESSERACT_CMD", "").strip().strip('"')
    if configured:
        return configured
    return shutil.which("tesseract")


def _resolve_image_path(root: Path, image_path: str) -> Path:
    path = Path(image_path).expanduser()
    if path.is_absolute():
        return path
    return root / path


def _display_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)
