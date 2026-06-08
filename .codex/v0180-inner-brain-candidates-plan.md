# 0.18.0 InnerBrain 训练候选实施计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

新增 `/inner-brain-candidates` 只读命令，从最近路由历史中列出适合人工沉淀为 InnerBrain 样本的输入，并给出 `/inner-brain-teach` 与 `/inner-brain-label` 示例。本阶段不自动写训练样本。

## 接口契约

- `/inner-brain-candidates`、`inner-brain-candidates`、`/brain-candidates`、`brain-candidates`：返回训练候选。
- 候选来源：最近路由历史中的 `llm-fallback`、`memory-fallback`、`inner-brain-clarify`。
- 空候选时返回“InnerBrain 训练候选：暂无。”。
- 候选入口不写入路由历史，避免查询动作污染候选。

## TDD 步骤

1. 新增空候选测试，验证只读入口不污染最近路由。
2. 新增 LLM fallback 与 memory fallback 候选测试。
3. 新增跨 Agent 恢复候选测试。
4. 更新版本测试到 `0.18.0`。
5. 实现命令入口、候选筛选和格式化。
6. 更新 README、PROJECT-PLAN、方案索引、进度和验证记录。
7. 执行目标、邻近、全量、桌面 smoke、打包、安装器元数据和静态验证。
