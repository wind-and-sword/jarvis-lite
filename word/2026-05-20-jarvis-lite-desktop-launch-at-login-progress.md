# Jarvis Lite 桌面开机自启动进度

> 日期：2026-05-20
> 执行者：Codex

## 当前目标

在桌面助手设置面板中加入当前用户级“开机启动”能力，让 Jarvis Lite 可以作为常驻桌面助手随用户登录启动。

## 已完成

- 新增 `jarvis_lite.desktop.autostart`：
  - 解析当前用户 Startup 目录。
  - 生成 `Jarvis Lite.lnk` 快捷方式配置。
  - 源码运行模式使用 `python -m jarvis_lite.desktop.app`。
  - 打包运行模式使用当前 `JarvisLite.exe`。
  - 支持启用、关闭、同步和状态检查。
- `DesktopSettings` 新增 `launch_at_login` 字段，保存到项目外 `../jarvis-lite-runtime/desktop-settings.json`。
- 助手面板设置区新增“开机启动”复选框。
- 面板设置变更时会保存偏好，并同步当前用户 Startup 快捷方式。
- 只有“开机启动”值真正变化时才同步 Startup 快捷方式，避免调整透明度或尺寸时重复调用 PowerShell。
- 自动化测试通过注入 runner 验证 PowerShell 创建快捷方式命令，不在测试中真实修改用户系统。
- 重新构建项目外安装产物：
  - `E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe`
  - `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`

## 验证结果

- RED 验证：
  - `tests.test_desktop_autostart` 先因 `jarvis_lite.desktop.autostart` 不存在失败。
  - `tests.test_desktop_settings` 先因缺少 `launch_at_login` 字段失败。
  - `tests.test_desktop_widgets` 先因面板设置缺少开机启动值失败。
  - `tests.test_desktop_app` 先因缺少 `apply_panel_settings` 失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_autostart -v`：7 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v`：8 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`：15 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v`：6 个测试通过。
- 全量验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：146 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：未发现空白错误，仅出现 CRLF 换行提示。
- 打包验证：
  - `.venv\Scripts\python.exe scripts\build_windows_installer.py`：成功生成安装器。
  - PyInstaller 日志显示 `Copying icon to EXE` 和 `Copying version information to EXE`。
  - `Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke -Wait -PassThru`：退出码 `0`。

## 后续建议

- 如果需要更专业的安装体验，可在安装 Inno Setup 或 NSIS 后替换 IExpress。
- 如果需要发布给更多用户，可继续做代码签名，但需要证书。
- 摄像头、麦克风和真实语音识别继续放到后续阶段。
