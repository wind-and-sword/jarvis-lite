# v60 InnerBrain 本机失败视图失败文件汇总排序方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v59 本机评估全量视图文件候选失败优先排序，明确 `0.56.0` 的本机失败文件分组优先级。

## 目标

`0.56.0` 在 `/inner-brain-eval-local-failed` 和本机失败评估报告复用的 `失败文件：` 分组中，优先展示失败数量更多的 JSONL 文件。用户进入失败视图后，可以先处理贡献失败最多的来源文件。

## 范围

- `describe_inner_brain_evaluation(report, failures_only=True)` 未指定单个评估文件时，`失败文件：` 按以下规则排序：
  - 失败数量降序
  - 文件名升序
- `/inner-brain-eval-local-failed` 复用该排序。
- `/inner-brain-eval-local-report` 未指定文件时复用该排序。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不新增 `InnerBrainEvaluationReport` 字段。
- 不改变失败样例、失败原因、意图混淆或修复建议内容。

## 验收

- 失败数量更多的 JSONL 文件排在失败数量更少的文件之前，即使文件名排序在后。
- 同等失败数量时按文件名升序。
- 纯通过文件不出现在 `失败文件：` 分组中。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
