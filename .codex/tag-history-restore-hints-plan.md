# 批量标签历史资料恢复提示计划

日期：2026-05-26  
执行者：Codex

## 目标

执行“读取第一条标签历史资料”后，结果除了恢复最近资料列表，还直接显示该历史条目的逐份恢复命令，减少用户在历史详情和 `/tag-history` 之间来回查找。

## 设计

- 复用 `RuntimeTaggedDocumentsOperationContext.restore_commands`。
- 只在 `_read_tagged_documents_history_documents()` 输出中追加恢复提示。
- 不新增运行态字段，不改变批量标签确认和历史保存逻辑。
- 旧历史没有 `restore_commands` 时保持原输出。

## 步骤

1. 在 `tests/test_agent.py` 先新增失败测试，要求读取第一条标签历史资料时显示恢复提示。
2. 运行目标测试确认 RED。
3. 在 `agent.py` 中复用 `operation.restore_commands` 追加恢复提示。
4. 运行目标测试和相关回归确认 GREEN。
5. 更新 README、进度文档、验证记录和审查记录。
6. 全量验证后提交并推送。

## 验收

- “读取第一条标签历史资料”输出包含 `恢复提示：给第一份资料打标签 ...`。
- 输出仍包含影响资料编号列表和“可继续操作”。
- “读取第二份资料”继续复用最近资料列表。
- `/tag-history`、最近上下文、确认批量标签恢复提示回归通过。
