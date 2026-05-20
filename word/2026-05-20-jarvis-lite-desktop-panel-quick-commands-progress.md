# Jarvis Lite 桌面面板快捷命令收口进度

> 日期：2026-05-20
> 执行者：Codex

## 当前目标

收口助手面板快捷命令，只保留不需要额外参数即可直接执行的命令，让桌面助手的按钮行为更稳定。

## 已完成

- `jarvis_lite.desktop.bridge` 新增 `DIRECT_QUICK_COMMAND_PROMPTS` 和 `direct_quick_commands()`。
- `quick_commands()` 继续保留完整桌面能力清单，包括需要参数的 `/organize-preview`。
- 助手面板快捷按钮改为使用 `direct_quick_commands()`。
- 托盘快捷命令也改为使用 `direct_quick_commands()`，与面板保持一致。
- 面板新增 `quick_command_texts()` 和 `quick_command_button()`，便于自动化测试和后续复用。
- 面板快捷命令只展示：
  - `状态`
  - `知识库`
  - `常用目录`
  - `生成日报`
- 点击面板快捷命令仍复用 `submit_text()`，会写入对话区、最近结果和状态。

## 验证结果

- RED 验证：
  - `tests.test_desktop_bridge` 先因缺少 `direct_quick_commands()` 失败。
  - `tests.test_desktop_widgets` 先因面板缺少快捷命令文本和按钮入口失败。
  - `tests.test_desktop_tray` 先因托盘无法复用无参数快捷命令集合失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge tests.test_desktop_widgets tests.test_desktop_tray -v`：30 个测试通过。
- 全量验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：154 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：未发现空白错误，仅出现 CRLF 换行提示。
- 打包验证：
  - `.venv\Scripts\python.exe scripts\build_windows_installer.py`：成功生成安装器。
  - `Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke -Wait -PassThru`：退出码 `0`。

## 后续建议

- 如果后续要支持 `/organize-preview` 这类命令，可以单独做带参数的命令向导或常用目录选择器。
- 摄像头、麦克风和真实语音识别继续按用户要求暂缓。
