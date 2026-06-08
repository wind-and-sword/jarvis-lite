# 桌面助手托盘快捷命令 Implementation Plan

> 日期：2026-05-19
> 执行者：Codex

**目标：** 在系统托盘菜单中增加常用命令入口，让用户无需先展开面板也能触发状态、知识库、常用目录和日报命令。

**架构：** 扩展 `desktop/tray.py`，复用 `desktop.bridge.quick_commands()` 中已有命令定义，托盘只选择低风险命令并调用 `AssistantPanel.submit_text()`；`DesktopPetWindow` 和 `AssistantPanel` 的现有状态同步继续负责结果展示和状态变化。

**技术栈：** Python 3.13、PySide6、unittest。

---

## 文件范围

- Modify: `src/jarvis_lite/desktop/tray.py`
- Test: `tests/test_desktop_tray.py`
- Modify docs: `README.md`、`verification.md`、`word/2026-05-19-jarvis-lite-desktop-app-progress.md`

## 任务 1：托盘快捷命令菜单

- [x] 写失败测试：托盘控制器暴露快捷命令 action 文案 `状态`、`知识库`、`常用目录`、`生成日报`。
- [x] 运行 `.\.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v`，预期因缺少快捷命令接口失败。
- [x] 扩展 `DesktopTrayController`，新增快捷命令 action 映射和菜单分隔。
- [x] 运行托盘专项测试，预期通过。

## 任务 2：快捷命令触发行为

- [x] 写失败测试：触发托盘 `知识库` action 后显示小助手和面板，并在面板 transcript 中出现 `用户：/kb`。
- [x] 运行托盘专项测试，预期因缺少动作连接失败。
- [x] 实现 `_run_quick_command(prompt)`，先显示助手和面板，再调用 `panel.submit_text(prompt)`。
- [x] 运行托盘专项测试，预期通过。

## 任务 3：文档和验证

- [x] 更新 README，说明托盘可直接触发常用命令。
- [x] 更新桌面应用进度文档，记录托盘快捷命令已完成和下一步。
- [x] 更新 `verification.md`，增加托盘快捷命令覆盖说明。
- [x] 运行桌面托盘专项、桌面 smoke、全量测试和 `git diff --check`。
- [ ] 提交并推送。
