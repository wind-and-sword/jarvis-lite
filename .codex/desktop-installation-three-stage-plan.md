# Desktop Installation Three Stage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 Jarvis Lite 桌面助手从可运行桌面入口推进到可打包、可生成 Windows 安装产物的状态，并保持三个阶段分别提交和推送。

**Architecture:** 阶段 1 收口桌面体验，补应用图标和窗口/托盘身份一致性。阶段 2 做打包前准备，补冻结运行时目录、PyInstaller 命令生成和打包依赖声明。阶段 3 增加 Windows 安装器生成脚本，实际构建桌面 exe 和 IExpress 安装器，产物输出到项目外目录，不提交二进制。

**Tech Stack:** Python 3.13、PySide6、PyInstaller、Windows IExpress、标准库 `unittest`。

---

## Stage 1: 桌面体验收口

**Files:**
- Modify: `src/jarvis_lite/desktop/assets.py`
- Modify: `src/jarvis_lite/desktop/app.py`
- Modify: `src/jarvis_lite/desktop/tray.py`
- Modify: `src/jarvis_lite/desktop/widgets.py`
- Create: `src/jarvis_lite/desktop/assets/app-icon.svg`
- Modify: `tests/test_desktop_assets.py`
- Modify: `tests/test_desktop_app.py`
- Modify: `tests/test_desktop_tray.py`
- Create: `word/2026-05-20-jarvis-lite-desktop-experience-closeout-design.md`
- Create: `word/2026-05-20-jarvis-lite-desktop-experience-closeout-progress.md`

- [x] **Step 1: Write failing tests**
  - App icon asset exists in project.
  - `create_desktop_app()` applies non-null app/window/panel icons.
  - tray uses a non-null icon from the app icon helper.
- [x] **Step 2: Run failing tests**
  - `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_assets tests.test_desktop_app tests.test_desktop_tray -v`
- [x] **Step 3: Implement app identity and icon**
  - Add `desktop_app_icon_path()`.
  - Add `app-icon.svg`.
  - Apply icon to `QApplication`、`AssistantPanel`、`DesktopPetWindow` and tray.
- [x] **Step 4: Verify, document, commit, push**
  - Run focused tests, full tests, smoke, `git diff --check`.
  - Commit: `feat: 收口桌面应用体验`
  - Push `origin main`.

## Stage 2: 打包前准备

**Files:**
- Modify: `src/jarvis_lite/config.py`
- Create: `src/jarvis_lite/desktop/packaging.py`
- Create: `packaging/windows/desktop_launcher.py`
- Create: `scripts/build_desktop_exe.py`
- Modify: `pyproject.toml`
- Create/Modify tests: `tests/test_config.py`, `tests/test_desktop_packaging.py`
- Create: `word/2026-05-20-jarvis-lite-desktop-package-prep-design.md`
- Create: `word/2026-05-20-jarvis-lite-desktop-package-prep-progress.md`

- [x] **Step 1: Write failing tests**
  - Frozen app defaults to `%LOCALAPPDATA%/Jarvis Lite` for user data.
  - PyInstaller args are deterministic and output outside repo.
  - optional dependency includes PyInstaller.
- [x] **Step 2: Run failing tests**
  - `.\.venv\Scripts\python.exe -m unittest tests.test_config tests.test_desktop_packaging -v`
- [x] **Step 3: Implement package prep**
  - Add frozen runtime root handling.
  - Add PyInstaller command generator and build script.
  - Add launcher entrypoint and optional dependency.
- [x] **Step 4: Verify, document, commit, push**
  - Run focused tests, full tests, smoke, `git diff --check`.
  - Commit: `chore: 增加桌面打包准备`
  - Push `origin main`.

## Stage 3: Windows 安装产物

**Files:**
- Create: `src/jarvis_lite/desktop/windows_installer.py`
- Create: `scripts/build_windows_installer.py`
- Create/Modify: `tests/test_windows_installer.py`
- Create: `word/2026-05-20-jarvis-lite-desktop-windows-installer-design.md`
- Create: `word/2026-05-20-jarvis-lite-desktop-windows-installer-progress.md`

- [x] **Step 1: Write failing tests**
  - install/uninstall batch content includes LocalAppData install path and shortcuts.
  - IExpress SED content points to project-external output path and uses the packaged exe.
- [x] **Step 2: Run failing tests**
  - `.\.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v`
- [x] **Step 3: Implement installer builder**
  - Build onefile exe via PyInstaller.
  - Stage installer files.
  - Run IExpress when available.
  - Output artifacts under `../jarvis-lite-dist/`.
- [x] **Step 4: Verify package artifact, document, commit, push**
  - Install PyInstaller optional dependency if needed.
  - Build package.
  - Run packaged exe `--smoke` and confirm exit code 0.
  - Run full tests and `git diff --check`.
  - Commit: `build: 增加 Windows 桌面安装包`
  - Push `origin main`.
