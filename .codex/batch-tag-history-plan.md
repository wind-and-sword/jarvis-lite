# 批量标签操作历史命令计划

日期：2026-05-26  
执行者：Codex

## 目标

把最近一次批量标签摘要扩展为最近 5 条历史记录，并提供独立的 `/tag-history` 与自然语言“查看批量标签历史”入口；现有“最近上下文”仍只突出最新一条。

## 方案

1. 在 `tests/test_agent.py` 先新增失败测试，覆盖两次批量标签确认后 `/tag-history` 的新旧顺序和跨 Agent 实例恢复。
2. 在 `runtime_context.py` 增加 `recent_tagged_documents_operations` 列表字段，读取时兼容旧的 `recent_tagged_documents_operation` 单值字段，写入时同时保留单值和列表。
3. 在 `agent.py` 中维护 `_recent_tagged_documents_operations`，确认批量标签后将新操作插入首位并截断为 5 条。
4. 新增 `_tagged_documents_history_status()` 输出历史列表；无历史时给出下一步提示。
5. 在 `intent.py` 增加“查看批量标签历史”等自然语言映射，并更新 README、计划文档、进度文档和验证记录。

## 验收

- `/tag-history` 能显示最近批量打标签历史，最新记录排第 1 条。
- 新 `JarvisAgent` 实例能恢复历史列表。
- “查看最近上下文”仍显示最新一次摘要。
- 全量测试、桌面 smoke、`git diff --check` 通过。
