from __future__ import annotations

from pathlib import Path

from jarvis_lite.desktop.windows_installer import run_iexpress, stage_windows_installer_files, windows_installer_paths

try:
    from scripts.build_desktop_exe import build_desktop_exe
except ModuleNotFoundError:
    from build_desktop_exe import build_desktop_exe


def build_windows_installer(project_root: Path | None = None, output_root: Path | None = None) -> Path:
    paths = windows_installer_paths(project_root, output_root)
    exe_path = build_desktop_exe(project_root, output_root)
    stage_windows_installer_files(paths, exe_path)
    run_iexpress(paths)
    return paths.installer_path


def main() -> int:
    installer_path = build_windows_installer()
    print(installer_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
