# Jarvis Lite 桌面面板快捷命令收口执行计划

> 日期：2026-05-20
> 执行者：Codex

## 目标

收口助手面板快捷命令，只保留不需要额外参数的命令按钮，让面板一键操作更稳定。

## 范围

- 新增无参数快捷命令筛选 API。
- 托盘和面板复用该筛选 API。
- 面板提供快捷命令文本和 action 入口，便于测试和后续复用。
- 点击面板快捷命令继续走 `submit_text()`。

## 不做事项

- 不接入摄像头、麦克风或真实语音识别。
- 不做参数弹窗、命令向导或复杂表单。
- 不改安装器、不做代码签名。

## TDD 步骤

1. 扩展 `tests/test_desktop_bridge.py`：
   - `direct_quick_commands()` 返回 `状态`、`知识库`、`常用目录`、`生成日报`。
   - 结果不包含 `/organize-preview`。
2. 扩展 `tests/test_desktop_widgets.py`：
   - 面板快捷命令文本为四个无参数命令。
   - 点击 `知识库` 按钮会提交 `/kb` 并写入对话区。
3. 扩展 `tests/test_desktop_tray.py`：
   - 托盘快捷命令来自同一组无参数命令。
4. 运行 RED，确认失败。
5. 实现 bridge、widgets、tray 改动。
6. 运行专项测试、全量测试、桌面 smoke、打包 exe smoke 和 `git diff --check`。
7. 更新 `README.md`、`verification.md`、`word/` 进度文档和本地 `.codex/` 记录。
8. 单独提交并 push 本阶段。
