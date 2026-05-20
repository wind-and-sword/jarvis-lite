from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DESKTOP_EXE_NAME = "JarvisLite"
DIST_DIRNAME = "jarvis-lite-dist"


@dataclass(frozen=True)
class DesktopBuildPaths:
    project_root: Path
    output_root: Path
    dist_dir: Path
    build_dir: Path
    spec_dir: Path
    launcher_path: Path
    assets_dir: Path


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
    )


def pyinstaller_desktop_args(paths: DesktopBuildPaths | None = None) -> list[str]:
    build_paths = paths or default_desktop_build_paths()
    return [
        "--noconfirm",
        "--clean",
        "--windowed",
        "--onefile",
        "--name",
        DESKTOP_EXE_NAME,
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
