# Jarvis Lite Windows 桌面安装器进度

> 日期：2026-05-20
> 执行者：Codex

## 当前目标

完成 Windows 可分发安装产物阶段，生成桌面 exe 和安装器。

## 已完成

- 新增 `jarvis_lite.desktop.windows_installer`，用于生成安装脚本、卸载脚本和 IExpress SED 文件。
- 新增 `scripts/build_windows_installer.py`，串联 PyInstaller exe 构建和 IExpress 安装器构建。
- 安装器产物输出到项目外 `../jarvis-lite-dist/JarvisLiteSetup.exe`。
- 桌面 exe 输出到项目外 `../jarvis-lite-dist/desktop-exe/JarvisLite.exe`。
- 本地虚拟环境已安装 `desktop-build` 可选依赖，并成功构建 PyInstaller 产物。
- IExpress 使用 `/N /Q` 非交互参数构建安装器，避免弹出向导。

## 验证结果

- `.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v`：3 个安装器测试通过。
- `.venv\Scripts\python.exe scripts\build_windows_installer.py`：成功生成 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`。
- `Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke -Wait -PassThru`：退出码 `0`。
- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：132 个测试通过。
- `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check`：未发现空白错误。

## 产物位置

```text
E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe
E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe
```

## 后续建议

- 后续可以替换为更专业的 Inno Setup 或 NSIS 安装器。
- 后续可以加入正式 `.ico` 图标、版本资源和代码签名。
- 摄像头、麦克风和真实语音识别继续放到后续阶段。
