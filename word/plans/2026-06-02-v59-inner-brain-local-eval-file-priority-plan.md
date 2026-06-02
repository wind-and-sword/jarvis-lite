# v59 InnerBrain 本机评估全量视图文件候选失败优先排序方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v58 本机评估全量视图文件候选状态摘要，明确 `0.55.0` 的失败文件优先展示。

## 目标

`0.55.0` 在 `/inner-brain-eval-local` 的 `可聚焦文件：` 候选列表中优先展示失败数量更多的 JSONL 文件。用户看到全量本机评估后，可以先进入失败最多的文件继续治理。

## 范围

- `/inner-brain-eval-local` 有本机样本且存在来源文件时，候选文件按以下规则排序：
  - 失败数量降序
  - 总样本数量降序
  - 文件名升序
- 候选行继续展示文件名、总样本数、通过样本数、失败样本数和 `/inner-brain-eval-local-file 文件名`。
- `/inner-brain-eval-local-file 文件名`、失败视图、已处理视图和报告导出不改行为。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不新增 `InnerBrainEvaluationReport` 字段。
- 不改变 `/inner-brain-eval-local-report` 导出的 Markdown 报告内容。

## 验收

- 有失败的本机 evaluation 文件排在纯通过文件之前，即使文件名排序在后。
- 同等失败数量时，样本更多的文件排在前；样本数也相同时按文件名升序。
- 输出仍包含可复制的 `/inner-brain-eval-local-file 文件名` 命令。
- 空本机 evaluation 样本仍只显示添加样本引导。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
