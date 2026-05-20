from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.request import urlopen

from . import __version__


UPDATE_MANIFEST_ENV = "JARVIS_LITE_UPDATE_MANIFEST_URL"


@dataclass(frozen=True)
class UpdateManifest:
    version: str
    download_url: str
    release_notes: str = ""
    published_at: str = ""


@dataclass(frozen=True)
class UpdateCheckResult:
    current_version: str
    latest_version: str
    update_available: bool
    download_url: str
    release_notes: str
    published_at: str
    source: str


def is_newer_version(candidate_version: str, current_version: str) -> bool:
    """比较点分数字版本号，避免把 0.10.0 当成小于 0.2.0。"""

    return _version_tuple(candidate_version) > _version_tuple(current_version)


def check_for_update(source: str | None = None, current_version: str = __version__) -> UpdateCheckResult:
    """读取更新清单并返回版本比较结果。"""

    resolved_source = _resolve_update_source(source)
    if not resolved_source:
        raise ValueError(f"未配置更新源，请设置 {UPDATE_MANIFEST_ENV} 或传入清单路径。")

    manifest = load_update_manifest(resolved_source)
    return UpdateCheckResult(
        current_version=current_version,
        latest_version=manifest.version,
        update_available=is_newer_version(manifest.version, current_version),
        download_url=manifest.download_url,
        release_notes=manifest.release_notes,
        published_at=manifest.published_at,
        source=resolved_source,
    )


def describe_update_status(source: str | None = None, current_version: str = __version__) -> str:
    """返回适合命令行和桌面面板展示的更新状态。"""

    resolved_source = _resolve_update_source(source)
    if not resolved_source:
        return "\n".join(
            [
                "更新状态：",
                f"- 当前版本：{current_version}",
                "- 更新源：未配置",
                f"- 说明：设置 {UPDATE_MANIFEST_ENV}，或使用 /update-status 清单路径，来检查新版本。",
            ]
        )

    try:
        result = check_for_update(resolved_source, current_version=current_version)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return f"更新检查失败：{exc}"

    if result.update_available:
        lines = [
            f"发现新版本：{result.latest_version}",
            f"- 当前版本：{result.current_version}",
            f"- 更新源：{result.source}",
            f"- 下载地址：{result.download_url}",
        ]
        if result.release_notes:
            lines.append(f"- 更新说明：{result.release_notes}")
        if result.published_at:
            lines.append(f"- 发布时间：{result.published_at}")
        lines.append("- 说明：请下载安装包后覆盖安装。")
        return "\n".join(lines)

    return "\n".join(
        [
            "当前已是最新版本。",
            f"- 当前版本：{result.current_version}",
            f"- 最新版本：{result.latest_version}",
            f"- 更新源：{result.source}",
        ]
    )


def load_update_manifest(source: str) -> UpdateManifest:
    raw = _read_manifest_text(source)
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("更新清单必须是 JSON 对象。")

    version = _read_required_str(data, "version")
    download_url = _read_required_str(data, "download_url")
    release_notes = _read_optional_str(data, "release_notes")
    published_at = _read_optional_str(data, "published_at")
    _version_tuple(version)
    return UpdateManifest(
        version=version,
        download_url=download_url,
        release_notes=release_notes,
        published_at=published_at,
    )


def _read_manifest_text(source: str) -> str:
    if source.startswith(("http://", "https://")):
        with urlopen(source, timeout=10) as response:
            return response.read().decode("utf-8")
    return Path(source).expanduser().read_text(encoding="utf-8")


def _resolve_update_source(source: str | None) -> str:
    return (source or os.environ.get(UPDATE_MANIFEST_ENV, "")).strip()


def _read_required_str(data: dict[str, object], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"更新清单缺少 {key}。")
    return value.strip()


def _read_optional_str(data: dict[str, object], key: str) -> str:
    value = data.get(key, "")
    return value.strip() if isinstance(value, str) else ""


def _version_tuple(version: str) -> tuple[int, ...]:
    normalized = version.strip().removeprefix("v")
    if not normalized:
        raise ValueError("版本号不能为空。")
    try:
        return tuple(int(segment) for segment in normalized.split("."))
    except ValueError as exc:
        raise ValueError(f"版本号必须使用点分数字格式：{version}") from exc
