# Jarvis Lite 桌面体验收口进度

> 日期：2026-05-20
> 执行者：Codex

## 当前目标

完成进入安装包阶段前的桌面体验收口，让应用在窗口和托盘层面具备一致的名称、版本和图标。

## 已完成

- 新增 `src/jarvis_lite/desktop/assets/app-icon.svg`，作为桌面应用图标。
- 新增 `desktop_app_icon_path()`，统一返回应用图标路径。
- `create_desktop_app()` 设置应用名、组织名、版本号和 app 图标。
- `AssistantPanel` 和 `DesktopPetWindow` 现在会使用应用图标。
- `DesktopTrayController` 的托盘图标改为应用图标，不再直接使用状态图。

## 验证结果

- `.venv\Scripts\python.exe -m unittest tests.test_desktop_assets tests.test_desktop_app tests.test_desktop_tray -v`：15 个测试通过。
- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：125 个测试通过。
- `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
- `git diff --check`：未发现空白错误。

## 下一步

进入阶段 2：打包前准备，补冻结运行时目录、PyInstaller 命令生成、打包入口脚本和打包依赖声明。
