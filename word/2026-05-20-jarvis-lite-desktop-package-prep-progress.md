# Jarvis Lite 桌面打包前准备进度

> 日期：2026-05-20
> 执行者：Codex

## 当前目标

完成 Windows 桌面打包前准备，为下一阶段生成 exe 和安装产物提供稳定脚本。

## 已完成

- `build_project_paths()` 在冻结应用中默认使用 `%LOCALAPPDATA%\Jarvis Lite` 作为用户数据根目录。
- 新增 `jarvis_lite.desktop.packaging`，包含桌面 exe 名称、输出路径模型和 PyInstaller 参数生成。
- 新增 `packaging/windows/desktop_launcher.py`，作为 PyInstaller 冻结入口。
- 新增 `scripts/build_desktop_exe.py`，用于生成桌面 exe。
- `pyproject.toml` 新增 `desktop-build` 可选依赖组，包含 `pyinstaller>=6,<7`。

## 验证结果

- `.venv\Scripts\python.exe -m unittest tests.test_config tests.test_desktop_packaging -v`：5 个测试通过。
- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：129 个测试通过。
- `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check`：未发现空白错误。

## 下一步

进入阶段 3：安装产物阶段，安装 PyInstaller 构建依赖，生成桌面 exe，并用 Windows IExpress 生成可分发安装器。
