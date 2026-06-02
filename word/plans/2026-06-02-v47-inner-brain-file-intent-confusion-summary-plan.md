# Jarvis Lite v47：InnerBrain 本机评估失败文件意图混淆汇总方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v46 本机失败评估意图混淆汇总，明确 `0.43.0` 的失败文件与意图混淆方向交叉汇总闭环。

## 目标

`0.43.0` 在 InnerBrain 本机失败评估视图和 Markdown 报告中增加“失败文件意图混淆汇总”。用户执行 `/inner-brain-eval-local-failed` 或未指定单个文件的 `/inner-brain-eval-local-report` 后，除整体失败文件、失败类型、失败期望意图、失败意图混淆和失败原因外，还能看到失败样本按 `source_file + expected_intent -> actual_intent` 聚合后的数量和典型样本，便于判断某个高频混淆方向主要来自哪份本机 evaluation JSONL。

## 边界

- 只统计失败样本中有 `source_file` 且 `expected_intent != result.intent` 的记录。
- 不把策略不匹配或命令不匹配但意图一致的样本计入文件意图混淆汇总。
- 指定单个文件过滤时不展示交叉汇总，避免重复列出同一个文件名。
- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变评估样本 JSONL 的持久化字段和去重键。
- 不新增聚类模型、外部依赖或复杂文本相似度算法，只从现有评估结果做只读统计。
- 不改变 Agent 命令接口、正常聊天路由、LLM fallback 或联网搜索能力。

## 实现要点

- `InnerBrainEvaluationReport` 增加 `failed_source_file_intent_confusion_counts`，遍历 `failed_case_results`，仅当 `case.source_file` 存在且 `case.expected_intent != result.intent` 时按 `(source_file, expected -> actual)` 计数。
- `describe_inner_brain_evaluation(report, failures_only=True)` 在失败意图混淆汇总之后输出 `失败文件意图混淆汇总：`：
  - 仅在 `source_file_filter is None` 时展示。
  - 按失败数量降序排列。
  - 数量相同时按文件名和混淆方向排序，保证输出稳定。
  - 每条汇总包含来源文件、混淆方向、数量和一条典型样本。
- `export_inner_brain_evaluation_report()` 继续复用 failures-only 描述，因此未指定单个文件的 Markdown 报告自动包含失败文件意图混淆汇总。

## 验证

- RED：新增 InnerBrain 失败文件意图混淆汇总测试、报告导出包含交叉汇总测试、Agent 本机报告包含交叉汇总测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain + Agent 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 根据文件意图混淆汇总优先清理贡献高频混淆的 evaluation 文件，补 seed/runtime 样本、槽位抽取或评分补偿。
- 若仍需要更细排查，再考虑把失败修复建议按混淆方向分组展示。
