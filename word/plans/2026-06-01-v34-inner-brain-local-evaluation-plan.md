# Jarvis Lite v34：InnerBrain 本机评估集扩展方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v33 InnerBrain 固定评估集，明确 `0.30.0` 的本机 local evaluation JSONL 扩展。

## 目标

`0.30.0` 让 `/inner-brain-eval` 同时执行内置 seed 评估集和本机 `data/inner-brain/evaluation/*.jsonl` 评估样本。这样真实日志里确认应稳定支持的表达，可以先放入评估集观察分类器表现，而不是直接写入训练样本。

## 边界

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳候选、不写入 `data/inner-brain/training/runtime.jsonl`。
- 本机评估 JSONL 只影响 `/inner-brain-eval` 的统计与输出，不改变正常聊天路由。
- 损坏 JSON、空文本、缺少 `expected_intent` 或非法 `expected_policy` 的行会被忽略。

## 本机评估样本格式

```json
{"text":"请看看资料库状态","expected_intent":"knowledge.status","expected_policy":"execute","expected_command":"/kb"}
```

- `text`：用户输入。
- `expected_intent`：期望 InnerBrain 意图。
- `expected_policy`：可选，默认 `execute`，也可为 `clarify` 或 `fallback_to_llm`。
- `expected_command`：可选，期望生成的命令。

## 实现要点

- `InnerBrainEvaluationCase` 增加 `source` 字段。
- 新增 `load_evaluation_cases(paths)` 读取本机评估 JSONL。
- `evaluate_inner_brain()` 默认合并 seed 与本机评估样本；存在本机样本时评估集名称显示为 `seed_evaluation+local_evaluation`。
- `describe_inner_brain_evaluation()` 输出 `seed_evaluation` 与 `local_evaluation` 来源计数。

## 验证

- RED：新增本机评估 JSONL 加载测试、Agent `/inner-brain-eval` 合并本机评估测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain 专项、Agent/LLM/桌面/Conversation 相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 根据真实测试日志，把确认应稳定支持的表达加入本机评估集或项目 seed 评估集。
- 若评估集中出现失败，优先通过显式样本、槽位补全或分类器评分改进解决，不回到自然语言正则堆叠。
