# Jarvis Lite 桌面虚拟助手应用进度

> 日期：2026-05-20
> 执行者：Codex

## 当前目标

继续把 Jarvis Lite 从命令行助手推进为可常驻的桌面虚拟助手应用。本阶段聚焦托盘快捷命令的反馈闭环：托盘命令执行后，用户可以从托盘重新打开最近一次结果。

## 当前取舍

- 摄像头、麦克风和真实语音识别继续暂缓。
- 系统通知气泡暂不接入，避免不同桌面环境下表现不稳定。
- 最近结果只作为运行时 UI 状态，不写入 Git，也不写入项目外运行态设置文件。
- 桌面助手仍复用现有 `ConversationSession` 和命令行能力。

## 已完成

- `AssistantPanel` 新增最近一次提交结果记录，可读取本轮“用户/Jarvis”对话文本。
- `AssistantPanel.submit_text()` 现在返回 `DesktopResponse`，方便托盘控制器在执行命令后更新运行态 UI。
- 托盘菜单新增“最近结果（暂无）”入口，初始不可点击。
- 托盘快捷命令执行成功后，“最近结果”入口会更新为“最近结果：命令标签”并变为可点击。
- 托盘 tooltip 会显示最近一次托盘命令标签，例如 `Jarvis Lite - 最近：知识库`。
- 点击“最近结果”只显示小助手和助手面板，不重复执行上一条命令。

## 验证结果

- `.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`：13 个桌面 widget 测试通过。
- `.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v`：8 个桌面托盘测试通过；Qt minimal 插件会输出 `This plugin does not support raise()`，退出码为 0。
- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：119 个测试通过。
- `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：可以创建桌面小助手窗口并输出 `desktopPetWindow`。
- `git diff --check`：未发现空白错误。

## 下一步

1. 继续完善桌面设置，例如面板尺寸和主题。
2. 后续再评估安装包、开机自启动和更丰富的角色素材。
3. 摄像头、麦克风和真实语音识别继续放到后续阶段。
