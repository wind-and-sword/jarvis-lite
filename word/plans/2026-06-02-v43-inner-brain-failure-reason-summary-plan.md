# Jarvis Lite v43：InnerBrain 本机评估失败原因汇总方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v42 本机失败评估 Markdown 报告导出，明确 `0.39.0` 的失败原因汇总闭环。

## 目标

`0.39.0` 在 InnerBrain 本机失败评估视图和 Markdown 报告中增加“失败原因汇总”。用户执行 `/inner-brain-eval-local-report [文件名]` 后，报告除失败文件、失败样例和修复建议外，还会按失败原因统计数量并列出典型样本，便于先处理高频错误类型。

## 边界

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变评估样本 JSONL 的持久化字段和去重键。
- 不新增聚类模型或外部依赖，只按现有失败原因文本聚合。
- 不改变正常聊天路由、LLM fallback 或联网搜索能力。

## 实现要点

- `InnerBrainEvaluationReport` 增加失败原因计数视图，直接遍历 `failed_case_results`。
- `describe_inner_brain_evaluation(report, failures_only=True)` 在失败文件分组之后输出 `失败原因汇总：`：
  - 按失败数量降序排列。
  - 数量相同时按原因文本排序，保证输出稳定。
  - 每条汇总包含原因、数量和一条典型样本。
- `export_inner_brain_evaluation_report()` 继续复用 failures-only 描述，因此 Markdown 报告自动包含失败原因汇总。
- Agent 命令 `/inner-brain-eval-local-report [文件名]` 不变，仍作为只读路由观察命令处理。

## 验证

- RED：新增 InnerBrain 失败原因汇总测试、Agent 报告导出包含失败原因汇总测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain + Agent 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 根据失败原因汇总处理高频失败样本，优先补 seed/runtime 样本或槽位抽取。
- 若同一根因存在多种原因文本，再考虑轻量原因归一化，而不是引入复杂聚类模型。
