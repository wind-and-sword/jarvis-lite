# Jarvis Lite v48：InnerBrain 本机评估失败意图混淆修复建议分组方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v47 本机失败评估文件意图混淆汇总，明确 `0.44.0` 的失败意图混淆修复建议分组闭环。

## 目标

`0.44.0` 在 InnerBrain 本机失败评估视图和 Markdown 报告中增加“失败意图混淆修复建议”。用户执行 `/inner-brain-eval-local-failed` 或 `/inner-brain-eval-local-report` 后，除了看到高频 `expected_intent -> actual_intent` 混淆方向，还能直接看到该混淆方向下对应的显式 `/inner-brain-teach` 或 `/inner-brain-label` 修复建议，便于按一类混淆集中处理。

## 边界

- 只对失败样本中 `expected_intent != result.intent` 的记录做意图混淆修复建议分组。
- 策略不匹配或命令不匹配但意图一致的样本继续保留在现有平铺 `失败修复建议：` 中，不进入意图混淆分组。
- 保留现有 `失败修复建议：` 平铺段落，避免旧视图丢失非意图混淆失败建议。
- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变评估样本 JSONL 的持久化字段和去重键。
- 不新增聚类模型、外部依赖或复杂文本相似度算法。
- 不改变 Agent 命令接口、正常聊天路由、LLM fallback 或联网搜索能力。

## 实现要点

- `describe_inner_brain_evaluation(report, failures_only=True)` 复用 `report.failed_case_results` 和 `_inner_brain_evaluation_fix_suggestion()`。
- 新增输出 `失败意图混淆修复建议：`：
  - 仅统计 `case.expected_intent != result.intent` 的失败样本。
  - 按失败数量降序排列。
  - 数量相同时按混淆方向排序，保证输出稳定。
  - 每个混淆方向下列出对应的显式修复建议。
- `export_inner_brain_evaluation_report()` 继续复用 failures-only 描述，因此 Markdown 报告自动包含该分组。

## 验证

- RED：新增 InnerBrain 失败意图混淆修复建议分组测试、报告导出包含分组建议测试、Agent 本机报告包含分组建议测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain + Agent 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 根据分组后的修复建议优先补 seed/runtime 样本、槽位抽取或评分补偿。
- 若真实失败样本继续堆积，再考虑按来源文件和混淆方向联合展示修复建议。
