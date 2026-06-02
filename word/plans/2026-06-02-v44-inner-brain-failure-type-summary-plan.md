# Jarvis Lite v44：InnerBrain 本机评估失败类型汇总方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v43 本机失败评估原因汇总，明确 `0.40.0` 的失败类型归一化闭环。

## 目标

`0.40.0` 在 InnerBrain 本机失败评估视图和 Markdown 报告中增加“失败类型汇总”。用户执行 `/inner-brain-eval-local-failed` 或 `/inner-brain-eval-local-report [文件名]` 后，除失败文件、失败原因和失败样例外，还能看到意图、命令、策略维度的失败数量和典型样本，便于优先处理高频类型。

## 边界

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变评估样本 JSONL 的持久化字段和去重键。
- 不新增聚类模型、外部依赖或复杂文本相似度算法，只从现有失败原因文本做轻量类型识别。
- 不改变 Agent 命令接口、正常聊天路由、LLM fallback 或联网搜索能力。

## 实现要点

- `InnerBrainEvaluationReport` 增加失败类型计数视图，直接遍历 `failed_case_results`。
- 类型识别仅基于现有 reason 片段：
  - 包含 `意图期望` 时计入 `意图不匹配`。
  - 包含 `命令期望` 时计入 `命令不匹配`。
  - 包含 `策略期望` 时计入 `策略不匹配`。
- 同一失败样本可计入多个类型，保留 v43 的精确失败原因汇总用于查看具体差异。
- `describe_inner_brain_evaluation(report, failures_only=True)` 在失败文件分组后输出 `失败类型汇总：`，每类包含数量和一条典型样本。
- `export_inner_brain_evaluation_report()` 继续复用 failures-only 描述，因此 Markdown 报告自动包含失败类型汇总。

## 验证

- RED：新增 InnerBrain 失败类型汇总测试、报告导出包含失败类型汇总测试、Agent 本机报告包含失败类型汇总测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain + Agent 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 根据失败类型汇总优先处理高频意图或命令不匹配样本。
- 若失败类型仍不足以定位根因，再考虑按 expected intent 或来源文件交叉汇总，仍避免引入复杂聚类模型。
