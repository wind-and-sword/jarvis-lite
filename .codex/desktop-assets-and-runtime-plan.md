# 桌面助手素材与运行配置 Implementation Plan

> 日期：2026-05-19
> 执行者：Codex

**目标：** 给桌面小助手补齐项目内状态图片素材，并把运行时窗口位置保存到项目上一层 `jarvis-lite-runtime` 目录。

**架构：** 项目相关素材放在 `src/jarvis_lite/desktop/assets/` 并通过 package-data 打包；运行时设置放在 `paths.root.parent / "jarvis-lite-runtime" / "desktop-settings.json"`，不进入 Git。

**技术栈：** Python 3.13、PySide6、SVG 项目内素材、JSON 设置文件、unittest。

## 文件范围

- Create: `src/jarvis_lite/desktop/assets.py`
- Create: `src/jarvis_lite/desktop/settings.py`
- Create: `src/jarvis_lite/desktop/assets/*.svg`
- Modify: `src/jarvis_lite/desktop/widgets.py`
- Modify: `src/jarvis_lite/desktop/app.py`
- Modify: `pyproject.toml`
- Test: `tests/test_desktop_assets.py`
- Test: `tests/test_desktop_settings.py`
- Modify docs: README、verification、桌面应用进度文档

## TDD 步骤

- [ ] 新增素材路径测试，先确认 `desktop.assets` 不存在。
- [ ] 新增 SVG 素材和 `assets.py`，映射 `DesktopState` 到资产路径。
- [ ] 新增设置路径测试，先确认 `desktop.settings` 不存在。
- [ ] 实现 `runtime_dir`、`desktop_settings_path`、`load_desktop_settings`、`save_desktop_position`。
- [ ] 更新 `DesktopPetWindow`，按状态切换图片，并在拖动/关闭时保存位置。
- [ ] 更新 pyproject package-data，确保 SVG 进入包。
- [ ] 更新文档和验证记录。
- [ ] 跑专项测试、全量测试和 desktop smoke。
