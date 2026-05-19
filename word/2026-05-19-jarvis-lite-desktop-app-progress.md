# Jarvis Lite 桌面虚拟助手应用进度

> 日期：2026-05-19
> 执行者：Codex

## 当前目标

根据桌面虚拟助手应用方案，把 Jarvis Lite 从命令行助手推进为第一版桌面虚拟助手应用。当前目标是完成“桌面常驻小助手 + 点击展开助手面板 + 设置区域 + 系统托盘 + 状态素材与动效 + 运行态位置保存”的闭环。

## 当前取舍

- 先不接入摄像头、麦克风和真实硬件入口。
- 先保留命令行入口，桌面应用复用 `ConversationSession`。
- Bridge 层只负责把 UI 输入交给现有会话核心，并返回 UI 可识别的状态。
- 项目相关的角色素材放在 `src/jarvis_lite/desktop/assets/`，随项目提交到 GitHub。
- 运行时窗口位置保存到项目上一层 `jarvis-lite-runtime/desktop-settings.json`，不进入 Git。
- 运行时偏好设置也保存到同一个项目外文件，包括置顶、透明度和小助手尺寸。

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
- 新增 5 个项目内 SVG 状态素材：`idle`、`thinking`、`working`、`success`、`error`。
- 小助手会根据状态切换对应角色图片，并使用 Qt 定时器执行待机呼吸、思考脉冲、工作脉冲、完成弹跳和错误抖动等轻量动效。
- 小助手拖动或关闭时会保存窗口位置，下次启动会从项目外运行态设置恢复位置。
- 损坏的运行态设置文件会回退到默认窗口位置，避免桌面入口启动失败。
- 新增系统托盘控制器，托盘菜单包含“显示助手”“隐藏助手”“退出”。
- 正常启动桌面助手后，关闭小助手窗口会隐藏到托盘，不会直接退出进程。
- 托盘“退出”会允许小助手真正关闭，并结束桌面应用。
- 助手面板新增设置区域，支持切换小助手置顶、调节透明度和调节小助手尺寸。
- 设置变更会立即应用到桌面小助手，并写入项目外运行态文件；下次启动会自动恢复。

## 验证结果

- `.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge -v`：3 个桌面 bridge 测试通过。
- `.venv\Scripts\python.exe -m unittest tests.test_desktop_app -v`：3 个桌面入口测试通过。
- `.venv\Scripts\python.exe -m unittest tests.test_desktop_assets -v`：2 个桌面素材测试通过。
- `.venv\Scripts\python.exe -m unittest tests.test_desktop_settings -v`：6 个桌面设置测试通过。
- `.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v`：3 个桌面托盘测试通过。
- `.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`：12 个桌面 widget 测试通过。
- `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：可以创建桌面小助手窗口并输出 `desktopPetWindow`。
- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：113 个测试通过。

## 下一步

1. 继续做托盘菜单里的常用命令入口，例如状态、知识库和日报。
2. 继续做更完整的设置项，例如开机自启动预留、面板尺寸和主题。
3. 后续再评估安装包、开机自启动和更丰富的角色素材；摄像头、麦克风和真实语音识别继续暂缓。
