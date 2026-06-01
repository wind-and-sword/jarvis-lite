# Jarvis Lite v35：InnerBrain 评估失败修复建议方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v34 本机评估集扩展，明确 `0.31.0` 的评估失败修复建议。

## 目标

`0.31.0` 让 `/inner-brain-eval` 在发现失败样本时，直接给出显式训练建议。评估仍然只观察分类器表现，不自动训练、不自动采纳、不写入 runtime 样本。

## 边界

- 不新增自然语言意图正则。
- 不自动写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变正常聊天路由、候选统计或 LLM fallback。
- 失败建议只是可复制的人工操作提示，最终是否训练仍由用户显式执行。

## 实现要点

- `InnerBrainEvaluationReport` 增加失败结果视图。
- `describe_inner_brain_evaluation()` 在 `failed_count > 0` 时追加“失败修复建议”。
- 如果评估样本包含 `expected_command`，建议使用 `/inner-brain-teach 文本 => /命令`。
- 如果评估样本只包含可执行 intent，建议使用 `/inner-brain-label 文本 => intent`。
- 对 `clarify` 或 `fallback_to_llm` 期望，只提示先确认策略，不直接建议自动训练。

## 验证

- RED：新增 InnerBrain 失败评估建议测试、Agent `/inner-brain-eval` 失败建议测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain 专项、Agent/LLM/桌面/Conversation 相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 根据真实评估失败样本，继续增强样本治理、槽位补全和分类器评分。
- 若失败建议过多，再考虑增加失败过滤、只看失败样本或导出评估报告，但仍保持显式训练。
