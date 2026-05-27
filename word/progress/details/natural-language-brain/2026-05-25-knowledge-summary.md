# Jarvis Lite 2026-05-25 知识库摘要进度

> 日期：2026-05-27
> 执行者：Codex
> 说明：本文由旧自然语言本地大脑大进度文件拆分而来，保留原始进度片段。

## 追加进度：最近文件导入进入下一步建议

- “查看最近上下文”和日报“下一步建议”现在会把最近文件建议扩展为查看详情、导入知识库和刷新列表。
- 具体建议为“继续处理最近文件：查看第一份最近文件；导入第一份最近文件到知识库；/recent-files”。
- 本阶段只更新建议文本，不自动导入文件，也不改变 `/recent-files` 和最近文件导入执行路径。
- RED 验证：
  - 更新 1 个 Agent 测试和 1 个 Automation 测试先证明最近文件建议仍缺少导入动作。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_natural_language_recent_context_status_suggests_next_actions tests.test_automation.AutomationTests.test_write_daily_report_suggests_next_actions_from_context -v`：2 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：118 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_automation -v`：8 个测试通过。
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：263 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：知识库摘要增强

- 新增 `/kb-summary` 命令，用于按资料输出确定性知识库摘要。
- “总结知识库”“知识库摘要”“总结资料库”“资料库摘要”会映射到 `/kb-summary`。
- 摘要输出包含资料文件数、可检索文本行数、每份资料来源、行数、标签和第一条可检索文本预览。
- 本阶段复用现有 `_searchable_lines()`、`build_knowledge_index()` 和标签元数据，不改变 `/kb` 状态展示和 `/ask` 检索问答。
- RED 验证：
  - 新增 Knowledge 和 Agent 测试先因 `summarize_knowledge_base` 不存在、`/kb-summary` 未识别、“总结知识库”落入兜底而失败。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_reports_document_previews_with_sources tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_reports_empty_state tests.test_agent.AgentTests.test_knowledge_summary_command_reports_document_previews tests.test_agent.AgentTests.test_natural_language_knowledge_summary_maps_to_summary -v`：4 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_knowledge -v`：26 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：120 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：267 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：知识库摘要联动最近资料上下文

- `/kb-summary` 和“总结知识库”现在会把摘要中的资料列表写入最近资料上下文。
- 摘要结果末尾新增可继续操作提示：`读取第一份资料；给第一份资料打标签 标签；/ask 关键词`。
- 查看摘要后，可以继续说“读取第二份资料”或“给第一份资料打标签 项目”，复用已有编号资料操作。
- 最近资料列表会写入 `jarvis-lite-runtime/agent-context.json`，新 Agent 实例可恢复摘要后的编号资料列表。
- RED 验证：
  - 新增 3 个 Agent 测试先证明 `/kb-summary` 缺少后续提示、没有写入最近资料列表、重启后不能读取摘要中的第二份资料。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_agent.AgentTests.test_knowledge_summary_command_suggests_numbered_followups tests.test_agent.AgentTests.test_knowledge_summary_command_sets_recent_document_list_for_numbered_followups tests.test_agent.AgentTests.test_knowledge_summary_document_list_survives_new_agent_instance -v`：3 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_agent -v`：123 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_knowledge -v`：26 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：270 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 追加进度：知识库摘要长预览截断

- `/kb-summary` 中每份资料的摘要预览现在限制为 80 个字符。
- 资料首条可检索文本超过限制时，会截断并追加 `...`。
- 短预览保持原样，不改变 `/ask`、`/read` 和知识库索引。
- RED 验证：
  - 新增 1 个 Knowledge 测试先证明长预览会完整输出，没有省略标记。
- 专项验证：
  - `.venv\Scripts\python.exe -m unittest tests.test_knowledge.KnowledgeTests.test_summarize_knowledge_base_truncates_long_document_preview -v`：1 个测试通过。
  - `.venv\Scripts\python.exe -m unittest tests.test_knowledge -v`：27 个测试通过。
- 收尾验证：
  - `.venv\Scripts\python.exe -m unittest discover -s tests -v`：271 个测试通过。
  - `.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`：输出 `Jarvis Lite 桌面助手` 和 `desktopPetWindow`。
  - `git diff --check`：退出码为 0，仅出现 CRLF 换行提示。

## 后续建议

- 后续接入大模型时，应让大模型输出结构化意图建议，再由本地大脑决定是否执行。
- 下一步可以继续做“个人设备级 Agent 电脑工作台增强”，优先围绕知识库摘要可读性、最近文件后续操作和桌面入口细化做更稳定的上下文识别。
