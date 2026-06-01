# Jarvis Lite v33：InnerBrain 固定评估集方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v32 InnerBrain 包含签名置信度补偿，明确 `0.29.0` 的本地评估基线。

## 目标

`0.29.0` 建立 InnerBrain 固定评估集和 `/inner-brain-eval` 命令，让后续字符 n-gram、轻量 embedding 或小型分类器调整都先经过可重复的本地基线验证，而不是凭感觉调分。

## 边界

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳候选、不写入 runtime 样本。
- 第一批评估集只覆盖当前 seed 样本已稳定支持的表达。
- 未覆盖或真实失败表达继续进入 `/inner-brain-candidates`、teach、label 显式训练闭环。

## 实现要点

- 新增 `InnerBrainEvaluationCase`、`InnerBrainEvaluationCaseResult` 和 `InnerBrainEvaluationReport`。
- 新增 `seed_evaluation_cases()` 固定基线样本，覆盖问候、知识库、联网搜索、搜索总结、编号资料、标签、导入、缺槽澄清和外脑 fallback。
- 新增 `evaluate_inner_brain()` 执行评估，不触发本地动作、不写状态。
- 新增 `describe_inner_brain_evaluation()` 输出通过数、失败数、准确率和逐条样例。
- Agent 新增 `/inner-brain-eval` 和 `brain-eval` 别名，作为路由观察命令处理，不污染最近路由训练候选。

## 验证

- RED：新增 InnerBrain 评估 API 测试、Agent `/inner-brain-eval` 命令测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain 专项、Agent/LLM/桌面/Conversation 相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 持续把真实日志中确认稳定的本地任务表达加入评估集。
- 评估轻量 embedding 或小型分类器前，先要求固定评估集不退化，再比较新增评估样本的改善情况。
