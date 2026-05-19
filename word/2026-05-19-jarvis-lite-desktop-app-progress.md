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

## 验证结果

- `.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge -v`：3 个桌面 bridge 测试通过。
- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：87 个测试通过。

## 下一步

1. 引入 PySide6，创建最小桌面应用入口。
2. 实现可显示的助手面板，先接入文本输入和输出。
3. 再实现桌面角落常驻的小助手窗口、拖动和点击展开面板。
