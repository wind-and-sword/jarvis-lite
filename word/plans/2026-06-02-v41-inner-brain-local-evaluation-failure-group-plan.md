# Jarvis Lite v41：InnerBrain 本机评估失败文件分组方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v40 本机评估 JSONL 文件过滤，明确 `0.37.0` 的本机失败评估按文件分组入口。

## 目标

`0.37.0` 让 `/inner-brain-eval-local-failed` 在本机评估样本分散到多个 JSONL 文件后，先显示失败样本来自哪些文件以及每个文件失败条数，便于优先处理失败集最集中的来源。

## 边界

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变评估样本 JSONL 的持久化字段和去重键。
- 不改变正常聊天路由、LLM fallback 或联网搜索能力。
- 本阶段只做失败文件分组，不做报告导出。

## 实现要点

- `InnerBrainEvaluationReport` 增加 `failed_source_file_counts`，只统计失败样本的 `source_file`。
- `describe_inner_brain_evaluation(..., failures_only=True)` 在未指定单个文件过滤时显示 `失败文件：` 分组。
- 失败视图不再把通过文件列入文件分组，避免误导排查。
- `/inner-brain-eval-local-failed` 复用同一描述逻辑，继续只读评估样本，不污染最近路由历史。

## 验证

- RED：新增 InnerBrain 失败文件分组测试、Agent 本机失败文件分组测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain/Agent/LLM/桌面/Conversation 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 根据失败文件分组优先扩展样本、槽位补全或轻量分类器评分。
- 当失败分组仍不足以排查时，再做报告导出或按文件汇总治理视图。
