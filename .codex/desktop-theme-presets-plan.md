# Jarvis Lite 桌面主题预设执行计划

> 日期：2026-05-20
> 执行者：Codex

## 目标

在已有桌面设置面板上增加主题预设，让桌面虚拟助手可以在深色和浅色两套视觉风格之间切换，并保存到项目外运行态设置。

## 范围

- 新增桌面主题预设定义。
- `DesktopSettings` 增加 `theme_name`。
- 面板设置区增加主题下拉选择。
- 面板与小助手根据主题同步更新样式。
- 主题偏好保存到 `../jarvis-lite-runtime/desktop-settings.json`。

## 不做事项

- 不接入摄像头、麦克风或真实语音识别。
- 不引入图片下载或新外部依赖。
- 不替换安装器、不做代码签名。
- 不做复杂皮肤市场或自定义颜色编辑器。

## TDD 步骤

1. 扩展 `tests/test_desktop_settings.py`：
   - 默认主题为 `midnight`。
   - 保存/读取桌面偏好时保留主题。
   - 保存位置和面板尺寸时保留主题。
2. 新增或扩展 `tests/test_desktop_style.py`：
   - 主题列表包含 `midnight` 和 `daylight`。
   - 无效主题回退默认主题。
   - 面板和小助手样式文本包含主题颜色。
3. 扩展 `tests/test_desktop_widgets.py`：
   - 面板设置值包含主题。
   - `change_settings()` 可通知主题变化。
   - 小助手应用偏好后保存主题并更新样式。
4. 运行 RED，确认失败。
5. 实现 app_style、settings、widgets 改动。
6. 运行专项测试、全量测试、桌面 smoke、打包 exe smoke 和 `git diff --check`。
7. 更新 `word/` 文档、`README.md`、`verification.md`、`.codex/testing.md`。
8. 单独提交并 push 本阶段。
