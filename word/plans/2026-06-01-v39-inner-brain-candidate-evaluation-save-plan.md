# Jarvis Lite v39：InnerBrain 候选编号写入本机评估样本方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v38 本机评估样本显式写入，明确 `0.35.0` 的候选编号写入评估样本入口。

## 目标

`0.35.0` 让用户在 `/inner-brain-candidates` 中看到候选后，可以直接按编号把候选保存为本机评估样本，而不必复制完整原句。该入口用于先观察分类器表现，不进入 runtime 训练集。

## 边界

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 保存评估样本后不移除候选，候选仍可继续用于显式 teach 或 label。
- 不改变正常聊天路由、LLM fallback 或联网搜索能力。

## 实现要点

- 新增 `/inner-brain-eval-add-candidate 编号 => /命令`，复用候选编号和教学命令白名单，把候选文本写入本机 evaluation JSONL。
- 新增 `/inner-brain-eval-label-candidate 编号 => intent [slot=value ...]`，复用候选编号和 label 参数解析，把候选文本写入本机 evaluation JSONL。
- `/inner-brain-candidates` 输出增加按编号保存评估样本的提示。
- 两个命令作为观察/治理入口处理，不污染最近路由历史。

## 验证

- RED：新增 Agent 候选评估写入测试、候选缺失测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：Agent 专项、InnerBrain 专项、LLM/桌面/Conversation 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 根据本机评估失败集继续改进样本、槽位补全或轻量分类器评分。
- 当本机评估样本规模扩大时，再做按来源文件过滤、失败分组或报告导出。
