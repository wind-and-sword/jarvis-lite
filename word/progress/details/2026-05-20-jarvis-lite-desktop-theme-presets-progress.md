# Jarvis Lite 桌面主题预设进度

> 日期：2026-05-20
> 执行者：Codex

## 当前目标

在桌面虚拟助手中增加主题预设，让用户可以在深色和浅色外观之间切换，并把选择保存到项目外运行态设置。

## 已完成

- 新增 `jarvis_lite.desktop.app_style` 主题预设体系：
  - 默认主题 `midnight`。
  - 浅色主题 `daylight`。
  - 提供主题名规范化、显示名、面板样式和小助手样式生成函数。
  - 保留 `PANEL_STYLE` 和 `PET_STYLE` 兼容常量，默认指向深色主题。
- `DesktopSettings` 新增 `theme_name` 字段。
- 运行态设置保存和读取会保留主题，无效主题会回退到 `midnight`。
- 保存窗口位置、面板尺寸和其他偏好时会保留已有主题。
- 助手面板设置区新增主题下拉选择。
- 面板设置变更时会立即刷新面板主题，并把主题随设置回调传给桌面小助手。
- 桌面小助手会应用并保存主题，外观和面板保持一致。
- 重新构建项目外安装产物：
  - `E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe`
  - `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`

## 验证结果

- RED 验证：
  - `tests.test_desktop_style` 先因缺少主题 API 失败。
  - `tests.test_desktop_settings` 先因缺少 `theme_name` 字段失败。
  - `tests.test_desktop_widgets` 先因面板和小助手缺少主题设置失败。
  - `tests.test_desktop_app` 先因设置同步不传递主题失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_style -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v`：9 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`：16 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v`：6 个测试通过。
- 全量验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：151 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：未发现空白错误，仅出现 CRLF 换行提示。
- 打包验证：
  - `.venv\Scripts\python.exe scripts\build_windows_installer.py`：成功生成安装器。
  - PyInstaller 日志显示 `Copying icon to EXE` 和 `Copying version information to EXE`。
  - `Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke -Wait -PassThru`：退出码 `0`。

## 后续建议

- 下一步可以继续做桌面应用可视反馈增强，例如状态提示、窗口交互细节或设置项体验整理。
- 摄像头、麦克风和真实语音识别继续按用户要求暂缓。
