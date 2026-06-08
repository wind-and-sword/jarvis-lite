# 0.22.0 InnerBrain 候选运行态统计计划

> 日期：2026-06-01
> 执行者：Codex

## 验收契约

- 候选观察只记录 `llm-fallback`、`memory-fallback` 和 `inner-brain-clarify`。
- 候选统计保存 prompt、最近路由、摘要、依据、出现次数和首次/最近观察时间。
- `/inner-brain-candidates` 使用运行态统计排序，不再受最近 5 条路由窗口限制。
- `/inner-brain-teach-candidate` 和 `/inner-brain-label-candidate` 使用同一候选编号。
- 显式 teach、label 或 adopt 后删除对应候选统计。
- 不自动训练、不猜 intent、不新增自然语言正则规则。

## 执行步骤

1. RED：新增候选运行态统计、编号教学和训练后清理的失败测试。
2. GREEN：扩展 runtime context，并在 Agent 路由记录时更新候选统计。
3. 文档：同步 README、PROJECT-PLAN、方案索引、进度和验证记录。
4. 验证：运行目标测试、相邻回归、全量 unittest、桌面 smoke、安装包构建与静态检查。
