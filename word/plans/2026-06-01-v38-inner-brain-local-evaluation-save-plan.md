# Jarvis Lite v38：InnerBrain 本机评估样本显式写入方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v37 本机评估过滤视图，明确 `0.34.0` 的本机评估样本显式写入入口。

## 目标

`0.34.0` 让用户可以把真实日志里的自然语言句子先写入本机 InnerBrain 评估集，而不是直接训练。新增入口把样本保存到 `data/inner-brain/evaluation/runtime.jsonl`，随后可用 `/inner-brain-eval-local` 或 `/inner-brain-eval-local-failed` 观察分类器表现。

## 边界

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不从普通自然语言里猜测 intent、command、API key 或 URL。
- 不改变正常聊天路由、候选统计、LLM fallback 或搜索能力。
- 本阶段不做按文件名过滤和报告导出；样本规模扩大后再评估。

## 实现要点

- 新增 `save_local_evaluation_case()`，将显式确认的 `InnerBrainEvaluationCase` 写入 `data/inner-brain/evaluation/runtime.jsonl`。
- `/inner-brain-eval-add 文本 => /命令` 复用现有教学命令白名单，将已知命令映射为 `expected_intent` 与 `expected_command`。
- `/inner-brain-eval-label 文本 => intent [slot=value ...]` 复用现有 label 参数解析，只把 intent 写入评估样本；slot 继续用于显式命令一致性检查的后续阶段，不在本阶段做自动训练。
- 重复样本按 JSON 负载去重，避免同一句同一期望重复写入。
- 响应明确说明这是评估样本，不执行命令、不训练。

## 验证

- RED：新增 InnerBrain 评估样本保存测试、Agent `/inner-brain-eval-add`、Agent `/inner-brain-eval-label` 和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain 专项、Agent/LLM/桌面/Conversation 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 增加候选编号写入本机评估样本的快捷入口，例如 `/inner-brain-eval-add-candidate`。
- 当本机评估样本继续增多时，再做按文件名过滤、报告导出或失败分组。
