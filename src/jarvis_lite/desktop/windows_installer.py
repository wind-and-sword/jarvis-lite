from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from jarvis_lite import __version__

from .packaging import DESKTOP_EXE_NAME, DesktopBuildPaths, default_desktop_build_paths


INSTALLER_EXE_NAME = "JarvisLiteSetup.exe"
SED_FILENAME = "JarvisLiteSetup.sed"
INSTALL_SCRIPT_NAME = "install.cmd"
UNINSTALL_SCRIPT_NAME = "uninstall.cmd"


@dataclass(frozen=True)
class WindowsInstallerPaths:
    build_paths: DesktopBuildPaths
    output_root: Path
    stage_dir: Path
    installer_path: Path
    sed_path: Path
    packaged_exe_path: Path


def windows_installer_paths(
    project_root: Path | None = None,
    output_root: Path | None = None,
) -> WindowsInstallerPaths:
    build_paths = default_desktop_build_paths(project_root, output_root)
    return WindowsInstallerPaths(
        build_paths=build_paths,
        output_root=build_paths.output_root,
        stage_dir=build_paths.output_root / "windows-installer-stage",
        installer_path=build_paths.output_root / INSTALLER_EXE_NAME,
        sed_path=build_paths.output_root / SED_FILENAME,
        packaged_exe_path=build_paths.dist_dir / f"{DESKTOP_EXE_NAME}.exe",
    )


def render_install_script(exe_name: str = f"{DESKTOP_EXE_NAME}.exe", version: str = __version__) -> str:
    return f"""@echo off
setlocal
set "INSTALL_DIR=%LOCALAPPDATA%\\Programs\\Jarvis Lite"
set "USER_DATA_DIR=%LOCALAPPDATA%\\Jarvis Lite"
set "START_MENU_DIR=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Jarvis Lite"
set "DESKTOP_DIR=%USERPROFILE%\\Desktop"
taskkill /IM {exe_name} /F >nul 2>nul
mkdir "%INSTALL_DIR%" >nul 2>nul
mkdir "%START_MENU_DIR%" >nul 2>nul
copy /Y "%~dp0{exe_name}" "%INSTALL_DIR%\\{exe_name}" >nul
copy /Y "%~dp0{UNINSTALL_SCRIPT_NAME}" "%INSTALL_DIR%\\{UNINSTALL_SCRIPT_NAME}" >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut('%START_MENU_DIR%\\Jarvis Lite.lnk'); $s.TargetPath='%INSTALL_DIR%\\{exe_name}'; $s.WorkingDirectory='%INSTALL_DIR%'; $s.Save(); $d=$w.CreateShortcut('%DESKTOP_DIR%\\Jarvis Lite.lnk'); $d.TargetPath='%INSTALL_DIR%\\{exe_name}'; $d.WorkingDirectory='%INSTALL_DIR%'; $d.Save(); $u=$w.CreateShortcut('%START_MENU_DIR%\\Uninstall Jarvis Lite.lnk'); $u.TargetPath='%INSTALL_DIR%\\{UNINSTALL_SCRIPT_NAME}'; $u.WorkingDirectory='%INSTALL_DIR%'; $u.Save()"
reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JarvisLite" /v DisplayName /d "Jarvis Lite" /f >nul
reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JarvisLite" /v DisplayVersion /d "{version}" /f >nul
reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JarvisLite" /v DisplayIcon /d "%INSTALL_DIR%\\{exe_name}" /f >nul
reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JarvisLite" /v InstallLocation /d "%INSTALL_DIR%" /f >nul
reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JarvisLite" /v UninstallString /d "\\"%INSTALL_DIR%\\{UNINSTALL_SCRIPT_NAME}\\"" /f >nul
reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JarvisLite" /v QuietUninstallString /d "\\"%INSTALL_DIR%\\{UNINSTALL_SCRIPT_NAME}\\"" /f >nul
echo Jarvis Lite {version} installed to "%INSTALL_DIR%".
echo Existing app files were replaced if present.
echo User data kept at "%USER_DATA_DIR%".
endlocal
"""


def render_uninstall_script() -> str:
    return f"""@echo off
setlocal
set "INSTALL_DIR=%LOCALAPPDATA%\\Programs\\Jarvis Lite"
set "USER_DATA_DIR=%LOCALAPPDATA%\\Jarvis Lite"
set "START_MENU_DIR=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Jarvis Lite"
set "STARTUP_DIR=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
set "DESKTOP_DIR=%USERPROFILE%\\Desktop"
taskkill /IM {DESKTOP_EXE_NAME}.exe /F >nul 2>nul
del "%DESKTOP_DIR%\\Jarvis Lite.lnk" >nul 2>nul
del "%START_MENU_DIR%\\Jarvis Lite.lnk" >nul 2>nul
del "%START_MENU_DIR%\\Uninstall Jarvis Lite.lnk" >nul 2>nul
del "%STARTUP_DIR%\\Jarvis Lite.lnk" >nul 2>nul
rmdir "%START_MENU_DIR%" >nul 2>nul
reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\JarvisLite" /f >nul 2>nul
pushd "%TEMP%" >nul 2>nul
rmdir /S /Q "%INSTALL_DIR%" >nul 2>nul
popd >nul 2>nul
echo Jarvis Lite uninstalled.
echo User data kept at "%USER_DATA_DIR%".
endlocal
"""


def render_iexpress_sed(paths: WindowsInstallerPaths) -> str:
    stage_dir = str(paths.stage_dir) + "\\"
    return f"""[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=1
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=
DisplayLicense=
FinishMessage=Jarvis Lite {__version__} installation finished. Start Jarvis Lite from desktop shortcut to use this version.
TargetName={paths.installer_path}
FriendlyName=Jarvis Lite
AppLaunched={INSTALL_SCRIPT_NAME}
PostInstallCmd=<None>
AdminQuietInstCmd={INSTALL_SCRIPT_NAME}
UserQuietInstCmd={INSTALL_SCRIPT_NAME}
SourceFiles=SourceFiles
[SourceFiles]
SourceFiles0={stage_dir}
[SourceFiles0]
{DESKTOP_EXE_NAME}.exe=
{INSTALL_SCRIPT_NAME}=
{UNINSTALL_SCRIPT_NAME}=
"""


def stage_windows_installer_files(paths: WindowsInstallerPaths, packaged_exe_path: Path | None = None) -> WindowsInstallerPaths:
    source_exe = packaged_exe_path or paths.packaged_exe_path
    paths.stage_dir.mkdir(parents=True, exist_ok=True)
    paths.output_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_exe, paths.stage_dir / f"{DESKTOP_EXE_NAME}.exe")
    (paths.stage_dir / INSTALL_SCRIPT_NAME).write_text(render_install_script(), encoding="utf-8", newline="\r\n")
    (paths.stage_dir / UNINSTALL_SCRIPT_NAME).write_text(render_uninstall_script(), encoding="utf-8", newline="\r\n")
    paths.sed_path.write_text(render_iexpress_sed(paths), encoding="utf-8", newline="\r\n")
    return paths


def run_iexpress(paths: WindowsInstallerPaths) -> None:
    subprocess.run(["iexpress.exe", "/N", "/Q", str(paths.sed_path)], check=True)
