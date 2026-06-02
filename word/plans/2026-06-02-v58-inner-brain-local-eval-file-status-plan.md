# v58 InnerBrain 本机评估全量视图文件候选状态摘要方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v57 本机评估全量视图文件名候选提示，明确 `0.54.0` 的文件候选通过/失败状态摘要。

## 目标

`0.54.0` 在 `/inner-brain-eval-local` 的 `可聚焦文件：` 候选行中追加每个 JSONL 文件的通过和失败数量。用户可以先进入有失败的文件，再用失败视图或已处理清单继续治理。

## 范围

- `/inner-brain-eval-local` 有本机样本且存在来源文件时，候选行展示：
  - 文件名
  - 总样本数
  - 通过样本数
  - 失败样本数
  - `/inner-brain-eval-local-file 文件名`
- `/inner-brain-eval-local-file 文件名`、失败视图、已处理视图和报告导出不改行为。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不新增 `InnerBrainEvaluationReport` 字段。
- 不改变 `/inner-brain-eval-local-report` 导出的 Markdown 报告内容。

## 验收

- `/inner-brain-eval-local` 有多个本机 evaluation 文件时输出每个文件的通过/失败数量。
- 输出仍包含可复制的 `/inner-brain-eval-local-file 文件名` 命令。
- 空本机 evaluation 样本仍只显示添加样本引导，不追加文件候选状态摘要。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
