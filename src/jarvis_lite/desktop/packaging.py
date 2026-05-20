from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from jarvis_lite import __version__


DESKTOP_EXE_NAME = "JarvisLite"
DIST_DIRNAME = "jarvis-lite-dist"
WINDOWS_ICON_FILENAME = f"{DESKTOP_EXE_NAME}.ico"
WINDOWS_VERSION_FILENAME = f"{DESKTOP_EXE_NAME}.version.txt"
WINDOWS_VERSION_COMPANY = "Jarvis Lite"
WINDOWS_VERSION_DESCRIPTION = "Jarvis Lite desktop assistant"
WINDOWS_VERSION_PRODUCT = "Jarvis Lite"


@dataclass(frozen=True)
class DesktopBuildPaths:
    project_root: Path
    output_root: Path
    dist_dir: Path
    build_dir: Path
    spec_dir: Path
    launcher_path: Path
    assets_dir: Path
    icon_path: Path
    version_file_path: Path


def default_desktop_build_paths(
    project_root: Path | None = None,
    output_root: Path | None = None,
) -> DesktopBuildPaths:
    root = (project_root or Path(__file__).resolve().parents[3]).resolve()
    out = (output_root or root.parent / DIST_DIRNAME).resolve()
    return DesktopBuildPaths(
        project_root=root,
        output_root=out,
        dist_dir=out / "desktop-exe",
        build_dir=out / "pyinstaller-build",
        spec_dir=out / "pyinstaller-spec",
        launcher_path=root / "packaging" / "windows" / "desktop_launcher.py",
        assets_dir=root / "src" / "jarvis_lite" / "desktop" / "assets",
        icon_path=root / "packaging" / "windows" / WINDOWS_ICON_FILENAME,
        version_file_path=out / WINDOWS_VERSION_FILENAME,
    )


def windows_version_tuple(version: str) -> tuple[int, int, int, int]:
    """把项目版本号转换为 Windows 版本资源需要的四段整数。"""

    base_version = re.split(r"[-+]", version, maxsplit=1)[0]
    values: list[int] = []
    for segment in base_version.split("."):
        match = re.match(r"\d+", segment)
        if match is None:
            break
        values.append(int(match.group(0)))
    if not values:
        raise ValueError(f"无法转换 Windows 版本号：{version}")
    return tuple((values + [0, 0, 0, 0])[:4])


def render_windows_version_info(version: str = __version__) -> str:
    """渲染 PyInstaller 可读取的 Windows 版本资源文件内容。"""

    version_tuple = windows_version_tuple(version)
    return f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version_tuple},
    prodvers={version_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [
          StringStruct('CompanyName', '{WINDOWS_VERSION_COMPANY}'),
          StringStruct('FileDescription', '{WINDOWS_VERSION_DESCRIPTION}'),
          StringStruct('FileVersion', '{version}'),
          StringStruct('InternalName', '{DESKTOP_EXE_NAME}'),
          StringStruct('OriginalFilename', '{DESKTOP_EXE_NAME}.exe'),
          StringStruct('ProductName', '{WINDOWS_VERSION_PRODUCT}'),
          StringStruct('ProductVersion', '{version}')
        ]
      )
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""


def write_windows_version_file(paths: DesktopBuildPaths, version: str = __version__) -> Path:
    """写入 Windows 版本资源文件，供 PyInstaller 构建 exe 时使用。"""

    paths.version_file_path.parent.mkdir(parents=True, exist_ok=True)
    paths.version_file_path.write_text(render_windows_version_info(version), encoding="utf-8", newline="\n")
    return paths.version_file_path


def pyinstaller_desktop_args(paths: DesktopBuildPaths | None = None) -> list[str]:
    build_paths = paths or default_desktop_build_paths()
    return [
        "--noconfirm",
        "--clean",
        "--windowed",
        "--onefile",
        "--name",
        DESKTOP_EXE_NAME,
        "--icon",
        str(build_paths.icon_path),
        "--version-file",
        str(build_paths.version_file_path),
        "--distpath",
        str(build_paths.dist_dir),
        "--workpath",
        str(build_paths.build_dir),
        "--specpath",
        str(build_paths.spec_dir),
        "--paths",
        str(build_paths.project_root / "src"),
        "--add-data",
        f"{build_paths.assets_dir}{os.pathsep}jarvis_lite/desktop/assets",
        str(build_paths.launcher_path),
    ]
