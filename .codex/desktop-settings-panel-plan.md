# 桌面助手设置面板 Implementation Plan

> 日期：2026-05-19
> 执行者：Codex

**目标：** 在桌面助手面板中新增设置区域，支持置顶开关、透明度和小助手尺寸设置，并持久化到项目外运行态文件。

**架构：** 扩展 `desktop/settings.py` 的 `DesktopSettings`，统一保存位置和 UI 偏好；`AssistantPanel` 暴露设置控件与变更回调；`DesktopPetWindow` 负责应用置顶、透明度和尺寸；`app.py` 继续组合 bridge、panel、pet，不改核心会话逻辑。

**技术栈：** Python 3.13、PySide6、JSON 运行态设置、unittest。

---

## 文件范围

- Modify: `src/jarvis_lite/desktop/settings.py`
- Modify: `src/jarvis_lite/desktop/widgets.py`
- Modify: `src/jarvis_lite/desktop/app.py`
- Test: `tests/test_desktop_settings.py`
- Test: `tests/test_desktop_widgets.py`
- Modify docs: `README.md`、`verification.md`、`word/2026-05-19-jarvis-lite-desktop-app-progress.md`

## 任务 1：扩展运行态设置模型

- [x] 写失败测试：默认设置包含 `always_on_top=True`、`opacity_percent=100`、`pet_size=148`。
- [x] 写失败测试：保存和读取 UI 偏好后能恢复置顶、透明度和尺寸。
- [x] 运行 `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v`，预期缺少字段或保存函数失败。
- [x] 实现 `DesktopSettings` 新字段、`save_desktop_settings()` 和 `save_desktop_preferences()`。
- [x] 确保旧的位置保存继续保留其他偏好字段。

## 任务 2：小助手应用设置

- [x] 写失败测试：`DesktopPetWindow` 启动时恢复运行态里的置顶、透明度和尺寸。
- [x] 写失败测试：调用设置应用方法后，窗口尺寸、透明度和置顶状态更新并保存。
- [x] 运行 `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`，预期缺少设置应用接口。
- [x] 实现 `apply_settings()`、`current_opacity_percent()`、`current_pet_size()`、`is_always_on_top()`。
- [x] 将头像尺寸和动画帧按当前 pet size 等比计算，避免尺寸变化后素材比例不协调。

## 任务 3：面板设置区域

- [x] 写失败测试：`AssistantPanel` 暴露设置控件状态，默认显示当前设置。
- [x] 写失败测试：触发设置变更后回调小助手并写入运行态文件。
- [x] 运行 widget 专项测试，预期缺少面板设置 API。
- [x] 在 `AssistantPanel` 增加设置区：置顶复选框、透明度滑块、角色尺寸滑块。
- [x] 面板通过 `set_settings_listener()` 把设置变更交给 `DesktopPetWindow`。

## 任务 4：文档和验证

- [x] 更新 README 当前状态和桌面设置说明。
- [x] 更新桌面应用进度文档，记录设置面板已完成和下一步。
- [x] 更新 `verification.md`，增加设置面板测试结果。
- [x] 运行桌面专项、全量测试、桌面 smoke 和 `git diff --check`。
- [ ] 提交并推送。
