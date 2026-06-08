# 持久化最近批量标签操作摘要计划

> 日期：2026-05-26  
> 执行者：Codex

## 目标

确认执行标签组批量打标签后，把最近一次批量标签操作摘要写入 `../jarvis-lite-runtime/agent-context.json`，让新 `JarvisAgent` 实例也能在“最近上下文状态”中展示。

## 设计

- `runtime_context.py` 新增 `RuntimeTaggedDocumentsOperationContext`。
- `RuntimeContext` 新增 `recent_tagged_documents_operation` 可选字段。
- `load_runtime_context()` 兼容读取旧 JSON；缺失、类型错误或字段不完整时回退为 `None`。
- `save_runtime_context()` 写入新字段。
- `JarvisAgent` 初始化时恢复该字段，确认批量打标签后继续通过 `_save_runtime_context()` 持久化。

## TDD 步骤

1. 新增跨 Agent 恢复测试，先确认失败。
2. 实现 runtime context dataclass 与 JSON 读写。
3. 修改 Agent 初始化和 `_runtime_context()`。
4. 运行目标测试和相关回归。
5. 更新 README、验证记录和 `word/` 进度文档。
6. 全量验证后提交并 push。
