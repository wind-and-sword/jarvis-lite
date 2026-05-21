from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.request import urlopen

from . import __version__


UPDATE_MANIFEST_ENV = "JARVIS_LITE_UPDATE_MANIFEST_URL"
UPDATE_RUNTIME_DIRNAME = "jarvis-lite-runtime"
UPDATE_DOWNLOADS_DIRNAME = "updates"


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


@dataclass(frozen=True)
class UpdateDownloadResult:
    current_version: str
    latest_version: str
    update_available: bool
    download_url: str
    destination_path: Path | None
    bytes_written: int
    source: str


def is_newer_version(candidate_version: str, current_version: str) -> bool:
    """比较点分数字版本号，避免把 0.10.0 当成小于 0.2.0。"""

    return _version_tuple(candidate_version) > _version_tuple(current_version)


def update_download_dir(project_root: Path) -> Path:
    """返回项目外更新下载目录，避免安装包进入 Git 工作区。"""

    return project_root.resolve().parent / UPDATE_RUNTIME_DIRNAME / UPDATE_DOWNLOADS_DIRNAME


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


def download_update(
    source: str | None = None,
    *,
    downloads_dir: Path | None = None,
    current_version: str = __version__,
) -> UpdateDownloadResult:
    """检查更新并把新版本安装包下载到运行态目录。"""

    result = check_for_update(source, current_version=current_version)
    if not result.update_available:
        return UpdateDownloadResult(
            current_version=result.current_version,
            latest_version=result.latest_version,
            update_available=False,
            download_url=result.download_url,
            destination_path=None,
            bytes_written=0,
            source=result.source,
        )

    target_dir = downloads_dir or update_download_dir(Path.cwd())
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = target_dir / _download_filename(result.download_url, result.latest_version)
    bytes_written = _write_download(result.download_url, destination)
    return UpdateDownloadResult(
        current_version=result.current_version,
        latest_version=result.latest_version,
        update_available=True,
        download_url=result.download_url,
        destination_path=destination,
        bytes_written=bytes_written,
        source=result.source,
    )


def describe_update_download(
    source: str | None = None,
    *,
    downloads_dir: Path | None = None,
    current_version: str = __version__,
) -> str:
    """返回适合命令行和桌面面板展示的更新下载结果。"""

    try:
        result = download_update(source, downloads_dir=downloads_dir, current_version=current_version)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return f"更新下载失败：{exc}"

    if not result.update_available:
        return "\n".join(
            [
                "当前已是最新版本，无需下载更新。",
                f"- 当前版本：{result.current_version}",
                f"- 最新版本：{result.latest_version}",
                f"- 更新源：{result.source}",
            ]
        )

    return "\n".join(
        [
            "已下载更新安装包：",
            f"- 版本：{result.latest_version}",
            f"- 保存位置：{result.destination_path}",
            f"- 文件大小：{result.bytes_written} 字节",
            f"- 下载来源：{result.download_url}",
            "- 说明：请关闭 Jarvis Lite 后运行安装包覆盖安装。",
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


def _write_download(download_url: str, destination: Path) -> int:
    if download_url.startswith(("http://", "https://")):
        with urlopen(download_url, timeout=30) as response:
            with destination.open("wb") as target:
                shutil.copyfileobj(response, target)
        return destination.stat().st_size

    source_path = _download_local_path(download_url)
    if not source_path.is_file():
        raise FileNotFoundError(f"更新安装包不存在：{source_path}")
    if source_path.resolve() == destination.resolve():
        return destination.stat().st_size
    with source_path.open("rb") as source_file:
        with destination.open("wb") as target:
            shutil.copyfileobj(source_file, target)
    return destination.stat().st_size


def _download_local_path(download_url: str) -> Path:
    if _looks_like_windows_path(download_url):
        return Path(download_url).expanduser()

    parsed = urlparse(download_url)
    if parsed.scheme == "file":
        path_text = unquote(parsed.path)
        if os.name == "nt" and path_text.startswith("/") and len(path_text) > 2 and path_text[2] == ":":
            path_text = path_text[1:]
        return Path(path_text).expanduser()
    if parsed.scheme:
        raise ValueError(f"不支持的下载地址协议：{parsed.scheme}")
    return Path(download_url).expanduser()


def _download_filename(download_url: str, latest_version: str) -> str:
    parsed = urlparse(download_url)
    raw_path = download_url if _looks_like_windows_path(download_url) else parsed.path if parsed.scheme else download_url
    candidate = Path(unquote(raw_path)).name
    if candidate:
        return candidate
    return f"JarvisLiteSetup-{latest_version}.exe"


def _looks_like_windows_path(value: str) -> bool:
    return len(value) >= 3 and value[1] == ":" and value[2] in {"\\", "/"}


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
