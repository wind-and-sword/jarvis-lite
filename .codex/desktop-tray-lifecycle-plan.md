# 桌面助手托盘生命周期 Implementation Plan

> 日期：2026-05-19
> 执行者：Codex

**目标：** 让 Jarvis Lite 桌面助手具备系统托盘、关闭到托盘、托盘显示/隐藏和托盘退出能力。

**架构：** 新增 `desktop/tray.py` 作为托盘生命周期控制器，负责 `QSystemTrayIcon`、托盘菜单和应用退出流程；`DesktopPetWindow` 只暴露关闭到托盘相关方法，不直接管理托盘菜单；`desktop/app.py` 在正常启动时挂载托盘控制器，`--smoke` 保持快速验证。

**技术栈：** Python 3.13、PySide6、unittest、Qt minimal 平台 smoke 验证。

---

## 文件范围

- Create: `src/jarvis_lite/desktop/tray.py`
- Modify: `src/jarvis_lite/desktop/widgets.py`
- Modify: `src/jarvis_lite/desktop/app.py`
- Test: `tests/test_desktop_tray.py`
- Modify docs: `README.md`、`verification.md`、`word/2026-05-19-jarvis-lite-desktop-app-progress.md`

## 任务 1：托盘控制器基础菜单

- [x] 写失败测试：`DesktopTrayController` 应暴露 `显示助手`、`隐藏助手`、`退出` 菜单项。
- [x] 运行 `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v`，预期因缺少 `jarvis_lite.desktop.tray` 失败。
- [x] 新增 `tray.py`，创建 `QSystemTrayIcon`、`QMenu` 和三个 action。
- [x] 再运行专项测试，预期通过。

## 任务 2：关闭到托盘

- [x] 写失败测试：启用托盘控制器后，调用 `pet.close()` 应隐藏小助手而不是销毁窗口。
- [x] 运行专项测试，预期缺少关闭到托盘方法或行为失败。
- [x] 修改 `DesktopPetWindow.closeEvent()`，在 close-to-tray 模式下保存位置、隐藏面板、隐藏小助手并 `ignore()` 关闭事件。
- [x] 新增 `set_close_to_tray_enabled()`、`allow_application_close()`、`is_close_to_tray_enabled()`，供托盘控制器调用。
- [x] 再运行专项测试，预期通过。

## 任务 3：托盘显示/隐藏/退出动作

- [x] 写失败测试：`show_assistant()` 显示小助手，`hide_assistant()` 隐藏小助手和面板，`quit_application()` 允许真正退出。
- [x] 运行专项测试，预期相关方法不存在或状态不符合。
- [x] 实现控制器方法，并让 `QApplication.setQuitOnLastWindowClosed(False)` 在托盘模式下生效。
- [x] 修改 `app.py`，正常启动时创建托盘控制器并保持引用。
- [x] 运行 `tests.test_desktop_app`、`tests.test_desktop_tray` 和 `--smoke`。

## 任务 4：文档和验证

- [x] 更新 README 当前状态和桌面启动说明。
- [x] 更新桌面应用进度文档，记录托盘生命周期已完成和下一步。
- [x] 更新 `verification.md`，增加桌面托盘专项测试。
- [x] 运行全量测试、桌面 smoke 和 `git diff --check`。
- [ ] 提交并推送。
