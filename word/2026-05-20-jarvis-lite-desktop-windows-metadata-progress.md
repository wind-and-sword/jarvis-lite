# Jarvis Lite Windows 安装产物元数据进度

> 日期：2026-05-20
> 执行者：Codex

## 当前目标

完成 Windows 安装产物元数据收口，让打包后的 `JarvisLite.exe` 具备正式桌面应用所需的图标和版本信息。

## 已完成

- 新增 `packaging/windows/JarvisLite.ico`，作为 PyInstaller Windows exe 图标。
- 新增 `scripts/generate_windows_icon.py`，用于可复现生成 Windows `.ico` 图标。
- 扩展 `jarvis_lite.desktop.packaging`：
  - 默认构建路径增加 `icon_path` 和 `version_file_path`。
  - 新增 Windows 四段版本号转换。
  - 新增 PyInstaller 版本资源文本生成和写入。
  - PyInstaller 参数增加 `--icon` 和 `--version-file`。
- 更新 `scripts/build_desktop_exe.py`，构建 exe 前写入版本资源文件。
- 更新 `jarvis_lite.desktop.windows_installer`，安装脚本 `DisplayVersion` 使用项目版本号。
- 重新生成项目外安装产物：
  - `E:\oyzj\ai\jarvis-lite-dist\desktop-exe\JarvisLite.exe`
  - `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup.exe`

## 验证结果

- RED 验证：
  - `tests.test_desktop_packaging` 先因缺少 `render_windows_version_info` 失败。
  - `tests.test_windows_installer` 先因 `render_install_script()` 不支持 `version` 参数失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_packaging -v`：7 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_windows_installer -v`：4 个测试通过。
- 构建验证：
  - `.venv\Scripts\python.exe scripts\build_windows_installer.py`：成功生成安装器。
  - PyInstaller 日志显示 `Copying icon to EXE` 和 `Copying version information to EXE`。
- 版本信息验证：
  - `JarvisLite.exe` 的 `FileDescription` 为 `Jarvis Lite desktop assistant`。
  - `ProductName` 为 `Jarvis Lite`。
  - `FileVersion` 和 `ProductVersion` 均为 `0.1.0`。
- 全量验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：137 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `Start-Process ..\jarvis-lite-dist\desktop-exe\JarvisLite.exe --smoke -Wait -PassThru`：退出码 `0`。
  - `git diff --check`：未发现空白错误，仅出现 CRLF 换行提示。

## 后续建议

- 后续可继续补代码签名，但需要证书条件。
- 后续可替换为 Inno Setup 或 NSIS，但需要对应安装器工具。
- 摄像头、麦克风和真实语音识别继续放到后续阶段。
