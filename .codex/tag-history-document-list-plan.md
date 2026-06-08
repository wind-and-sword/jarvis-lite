# 批量标签历史影响资料读取计划

日期：2026-05-26  
执行者：Codex

## 目标

支持“读取第一条标签历史资料”，把某条批量标签历史影响到的资料列表恢复为最近资料列表，便于继续“读取第二份资料”或逐份处理。

## 步骤

1. 在 `tests/test_agent.py` 新增失败测试，覆盖跨 Agent 实例读取第一条标签历史影响资料，并继续读取第二份资料。
2. 在 `RuntimeTaggedDocumentsOperationContext` 新增 `document_paths` 字段，JSON 读写使用防御式解析并兼容旧记录。
3. 确认批量标签时把 `document_paths` 写入历史操作。
4. 在 `intent.py` 增加“读取/查看第 N 条标签历史资料”的自然语言识别。
5. 在 `agent.py` 新增 `_read_tagged_documents_history_documents()`，设置最近资料列表并输出编号资料。
6. 更新 `/tag-history` 输出可继续操作提示。
7. 更新 README、进度文档和验证记录。

## 验收

- 新 Agent 实例可执行“读取第一条标签历史资料”。
- 输出包含历史摘要和影响资料编号列表。
- 后续“读取第二份资料”复用最近资料列表成功。
- 旧历史记录缺少 `document_paths` 时返回明确提示。
