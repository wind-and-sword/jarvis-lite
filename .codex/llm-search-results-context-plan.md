# LLM fallback 最近搜索结果上下文计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

让 LLM fallback 在本地知识库问答产生多条最近搜索结果后，能看到这些结果路径，从而更稳定地建议 `/read 文件名`、`/tag 文件名 标签...` 或后续资料处理命令。

## 设计

- 不改变本地优先顺序。
- 不改变 `LLMRouter` / `LLMProvider` / `LLMIntent`。
- 在 `JarvisAgent._llm_context_lines()` 中追加：
  - `最近搜索结果：N 条`
  - `1. data/<path>`
  - `2. data/<path>`
- 最多列出 3 条，避免 context 过长。

## 验收

- 新增 Agent 测试先失败，证明 provider context 未包含最近搜索结果。
- GREEN 后目标测试通过。
- 回归 `tests.test_agent`、`tests.test_llm` 和全量 `unittest`。
- 更新 2026-05-28 正式进度和验证记录。
