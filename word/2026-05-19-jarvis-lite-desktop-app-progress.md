# Jarvis Lite 桌面虚拟助手应用进度

> 日期：2026-05-19
> 执行者：Codex

## 当前目标

根据桌面虚拟助手应用方案，开始把 Jarvis Lite 从命令行助手推进为桌面应用。第一步先实现桌面 UI 与现有 Python 核心之间的 bridge 层。

## 当前取舍

- 先不写 PySide6 窗口，避免 UI 代码和核心适配同时变动。
- 先不接入摄像头、麦克风和真实硬件入口。
- 先保留命令行入口，桌面应用复用 `ConversationSession`。
- Bridge 层只负责把 UI 输入交给现有会话核心，并返回 UI 可识别的状态。

## 已完成

- 新增 `src/jarvis_lite/desktop/` 包，作为桌面助手适配层。
- 新增 `DesktopState`，定义 `idle`、`thinking`、`working`、`success`、`error` 等 UI 状态。
- 新增 `DesktopBridge`，封装 `ConversationSession.handle()`，返回 `DesktopResponse`。
- 新增 `quick_commands()`，为未来助手面板提供快捷命令按钮数据。
- 新增 `tests/test_desktop_bridge.py`，覆盖会话调用、错误状态和快捷命令。
- 新增 PySide6 依赖和 `jarvis-lite-desktop` 桌面入口脚本。
- 新增 `src/jarvis_lite/desktop/app.py`，提供最小助手面板、文本输入、快捷命令按钮和 `--smoke` 验证模式。
- 新增 `src/jarvis_lite/desktop/widgets.py`，拆分 `AssistantPanel` 和 `DesktopPetWindow`。
- `DesktopPetWindow` 已具备无边框、置顶、小尺寸常驻窗口和点击展开/收起面板能力。
- `AssistantPanel` 已能通过 `DesktopBridge` 发送文本，并展示会话输出和状态。
- 小助手会跟随面板执行结果显示 `待命`、`思考`、`工作`、`完成`、`错误` 等状态。

## 验证结果

- `.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge -v`：3 个桌面 bridge 测试通过。
- `.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v`：3 个桌面入口测试通过。
- `.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`：4 个桌面 widget 测试通过。
- `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：可以创建桌面小助手窗口并输出 `desktopPetWindow`。
- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：94 个测试通过。

## 下一步

1. 增加角色图片资产和状态切换显示。
2. 增加窗口位置保存和开机后恢复位置。
3. 增加更接近虚拟宠物的待机/工作动效。
