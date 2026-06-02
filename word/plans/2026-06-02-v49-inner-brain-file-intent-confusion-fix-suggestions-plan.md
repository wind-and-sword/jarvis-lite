# Jarvis Lite v49：InnerBrain 本机失败评估文件意图混淆修复建议分组方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v48 本机失败评估意图混淆修复建议分组，明确 `0.45.0` 的文件意图混淆修复建议分组闭环。

## 目标

`0.45.0` 在 InnerBrain 本机失败评估视图和 Markdown 报告中增加“失败文件意图混淆修复建议”。用户执行 `/inner-brain-eval-local-failed` 或 `/inner-brain-eval-local-report` 后，除了看到全局 `expected_intent -> actual_intent` 修复建议分组，还能按来源 JSONL 文件查看同一混淆方向下的显式 `/inner-brain-teach` 或 `/inner-brain-label` 建议，便于按真实日志文件逐批处理。

## 边界

- 只对失败样本中 `source_file` 存在且 `expected_intent != result.intent` 的记录做文件意图混淆修复建议分组。
- 策略不匹配或命令不匹配但意图一致的样本继续保留在现有平铺 `失败修复建议：` 中，不进入文件意图混淆分组。
- 指定单个文件导出时不展示文件级分组，避免重复列出同一个文件名。
- 保留现有 `失败意图混淆修复建议：` 和 `失败修复建议：` 段落。
- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变评估样本 JSONL 的持久化字段和去重键。
- 不新增聚类模型、外部依赖或复杂文本相似度算法。
- 不改变 Agent 命令接口、正常聊天路由、LLM fallback 或联网搜索能力。

## 实现要点

- `describe_inner_brain_evaluation(report, failures_only=True)` 复用 `report.failed_case_results` 和 `_inner_brain_evaluation_fix_suggestion()`。
- 新增输出 `失败文件意图混淆修复建议：`：
  - 仅统计 `source_file` 存在且 `case.expected_intent != result.intent` 的失败样本。
  - 仅在 `report.source_file_filter is None` 时展示。
  - 按失败数量降序排列。
  - 数量相同时按来源文件和混淆方向排序，保证输出稳定。
  - 每个来源文件和混淆方向下列出对应的显式修复建议。
- `export_inner_brain_evaluation_report()` 继续复用 failures-only 描述，因此 Markdown 报告自动包含该分组。

## 验证

- RED：新增 InnerBrain 失败文件意图混淆修复建议分组测试、报告导出包含文件分组建议测试、Agent 本机报告包含文件分组建议测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain + Agent 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 根据文件级分组后的修复建议优先补 seed/runtime 样本、槽位抽取或评分补偿。
- 若真实失败样本继续堆积，再考虑把已处理建议状态做成单独只读清单。
