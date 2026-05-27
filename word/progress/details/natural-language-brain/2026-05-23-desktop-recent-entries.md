# Jarvis Lite 2026-05-23 桌面最近上下文入口进度

> 日期：2026-05-27
> 执行者：Codex
> 说明：本文由旧自然语言本地大脑大进度文件拆分而来，保留原始进度片段。

## 追加进度：桌面快捷入口补齐最近上下文和最近文件

- 桌面面板快捷命令新增“最近上下文”和“最近文件”。
- 托盘快捷命令继续复用同一套 `direct_quick_commands()`，会同步出现这两个入口。
- “最近上下文”快捷入口提交自然语言 `查看最近上下文`，复用本地意图层。
- “最近文件”快捷入口提交 `/recent-files`。
- `/organize-preview` 仍然因为需要参数而不会进入直接快捷入口。
- RED 验证：
  - 扩展桌面桥接和面板测试，先证明快捷命令缺少 `查看最近上下文`、`/recent-files`，面板无法点击“最近上下文”。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_bridge -v`：4 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_widgets -v`：19 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_desktop_tray -v`：8 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：260 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：按编号导入最近文件到知识库

- 执行 `/recent-files` 或“查看最近文件”后，可以继续说“导入第一份最近文件到知识库”。
- 也支持“把第2份最近文件导入知识库”等编号表达。
- Agent 只负责从运行态最近文件列表中选择路径，实际导入继续复用 `/import` 和 `import_knowledge_path()`。
- 缺少最近文件列表、编号越界或文件已不存在时，会返回明确提示。
- RED 验证：
  - 新增 3 个 Agent 测试先证明“第一份最近文件”会被误当成普通导入路径，缺列表和编号越界也没有最近文件语义提示。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_import_numbered_recent_file_adds_document_to_knowledge_base tests.test_agent.AgentTests.test_natural_language_import_numbered_recent_file_requires_recent_files tests.test_agent.AgentTests.test_natural_language_import_numbered_recent_file_reports_out_of_range -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：118 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_knowledge -v`：24 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：263 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

