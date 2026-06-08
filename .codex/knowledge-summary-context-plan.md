# 知识库摘要联动最近资料上下文计划

> 日期：2026-05-25  
> 执行者：Codex

## 目标

让用户查看 `/kb-summary` 或说“总结知识库”后，可以继续用“读取第一份资料”“给第二份资料打标签 项目”等编号表达操作摘要中的资料。

## 范围

- 只更新 Agent 层的上下文写入和摘要后的下一步提示。
- 不改变 `summarize_knowledge_base()` 的确定性摘要内容。
- 不改变 `/kb` 状态展示、`/ask` 检索排序和资料导入流程。

## 实现步骤

1. 新增 RED 测试：
   - `/kb-summary` 输出可继续操作提示。
   - `/kb-summary` 后可读取第二份资料。
   - 新 Agent 实例可恢复摘要写入的最近资料列表。
2. Agent 实现：
   - 引入 `build_knowledge_index()`。
   - `/kb-summary` 统一走 `_knowledge_summary()`。
   - 有摘要资料时写入 `_recent_document_path` 和 `_recent_document_paths` 并保存运行态上下文。
   - 在响应末尾追加可继续操作提示。
3. 验证：
   - 目标测试。
   - `tests.test_agent`、`tests.test_knowledge`。
   - 全量测试、桌面 smoke、`git diff --check`。
