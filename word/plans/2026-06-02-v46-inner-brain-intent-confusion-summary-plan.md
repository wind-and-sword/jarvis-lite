# Jarvis Lite v46：InnerBrain 本机评估失败意图混淆汇总方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v45 本机失败评估期望意图汇总，明确 `0.42.0` 的失败意图混淆方向汇总闭环。

## 目标

`0.42.0` 在 InnerBrain 本机失败评估视图和 Markdown 报告中增加“失败意图混淆汇总”。用户执行 `/inner-brain-eval-local-failed` 或 `/inner-brain-eval-local-report [文件名]` 后，除失败文件、失败类型、失败期望意图、失败原因和失败样例外，还能看到失败样本按 `expected_intent -> actual_intent` 聚合后的数量和典型样本，便于判断某个目标意图最常被混到哪里。

## 边界

- 只统计失败样本中 `expected_intent != result.intent` 的意图不匹配方向。
- 不把策略不匹配或命令不匹配但意图一致的样本计入意图混淆汇总。
- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变评估样本 JSONL 的持久化字段和去重键。
- 不新增聚类模型、外部依赖或复杂文本相似度算法，只从现有评估结果做只读统计。
- 不改变 Agent 命令接口、正常聊天路由、LLM fallback 或联网搜索能力。

## 实现要点

- `InnerBrainEvaluationReport` 增加 `failed_intent_confusion_counts`，遍历 `failed_case_results`，仅当 `case.expected_intent != result.intent` 时按 `expected -> actual` 计数。
- `describe_inner_brain_evaluation(report, failures_only=True)` 在失败期望意图汇总之后输出 `失败意图混淆汇总：`：
  - 按失败数量降序排列。
  - 数量相同时按 `expected -> actual` 文本排序，保证输出稳定。
  - 每条汇总包含混淆方向、数量和一条典型样本。
- `export_inner_brain_evaluation_report()` 继续复用 failures-only 描述，因此 Markdown 报告自动包含失败意图混淆汇总。

## 验证

- RED：新增 InnerBrain 失败意图混淆汇总测试、报告导出包含混淆汇总测试、Agent 本机报告包含混淆汇总测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain + Agent 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 根据失败意图混淆汇总优先补对应 seed/runtime 样本、槽位抽取或评分补偿。
- 若同一混淆方向仍无法定位原因，再考虑按来源文件与混淆方向交叉汇总。
