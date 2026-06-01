# Jarvis Lite v37：InnerBrain 本机评估过滤视图方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v36 评估失败过滤视图，明确 `0.33.0` 的本机评估过滤视图。

## 目标

`0.33.0` 让 `data/inner-brain/evaluation/*.jsonl` 本机评估样本可以单独执行。完整评估仍由 `/inner-brain-eval` 合并 seed 与 local 样本；排查真实日志样本时使用 `/inner-brain-eval-local`，只看本机失败项时使用 `/inner-brain-eval-local-failed`。

## 边界

- 不新增自然语言意图正则。
- 不改变 seed/runtime 样本分类器评分。
- 不自动写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变正常聊天路由、候选统计或 LLM fallback。
- 本机评估过滤只是报告视图，训练仍必须由用户显式执行 `/inner-brain-teach` 或 `/inner-brain-label`。

## 实现要点

- `evaluate_inner_brain()` 增加 `source_filter` 参数，按 `InnerBrainEvaluationCase.source` 过滤评估样本。
- `/inner-brain-eval-local` 使用 `source_filter="local_evaluation"`，只展示本机 JSONL 样本。
- `/inner-brain-eval-local-failed` 叠加 `failures_only=True`，只展示本机失败样本。
- 两个新入口作为路由观察命令处理，不写入最近路由训练候选。

## 验证

- RED：新增 source filter 评估 API 测试、Agent `/inner-brain-eval-local` 和 `/inner-brain-eval-local-failed` 命令测试、版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain 专项、Agent/LLM/桌面/Conversation 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 继续把真实日志中确认应稳定支持的表达加入本机评估 JSONL。
- 如果本机评估样本继续增多，再评估按文件名过滤或导出评估报告，但仍保持显式训练和本地评估优先。
