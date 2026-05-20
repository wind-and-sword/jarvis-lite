from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from jarvis_lite.desktop.packaging import (
    DESKTOP_EXE_NAME,
    default_desktop_build_paths,
    pyinstaller_desktop_args,
    write_windows_version_file,
)


def build_desktop_exe(project_root: Path | None = None, output_root: Path | None = None) -> Path:
    paths = default_desktop_build_paths(project_root, output_root)
    paths.output_root.mkdir(parents=True, exist_ok=True)
    write_windows_version_file(paths)
    command = [sys.executable, "-m", "PyInstaller", *pyinstaller_desktop_args(paths)]
    subprocess.run(command, cwd=paths.project_root, check=True)
    return paths.dist_dir / f"{DESKTOP_EXE_NAME}.exe"


def main() -> int:
    exe_path = build_desktop_exe()
    print(exe_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
