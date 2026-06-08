# 知识库摘要按标签分组计划

> 日期：2026-05-25
> 执行者：Codex

## 目标

增强 `/kb-summary` 的可读性，在逐份摘要前增加按标签聚合的资料分组，让多资料知识库可以先扫标签，再按编号继续操作。

## 实现设计

- 复用 `build_knowledge_index()` 产出的 `KnowledgeDocument.tags`，不新增存储格式。
- `summarize_knowledge_base()` 在总数后输出“标签分组”段。
- 有标签资料进入对应标签组；多标签资料可出现在多个组。
- 无标签资料进入“未标签”组。
- 保持“资料概览”逐份编号顺序不变，避免影响 `/kb-summary` 后续“读取第 N 份资料”。

## 验收标准

- Knowledge 测试覆盖标签分组和未标签分组。
- Agent 命令 `/kb-summary` 输出包含同一分组段。
- 全量测试、桌面 smoke 和 `git diff --check` 通过。
