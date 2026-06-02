# v57 InnerBrain 本机评估全量视图文件名候选提示方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v56 本机评估全量视图后续处理提示，明确 `0.53.0` 的本机 evaluation 文件名候选提示。

## 目标

`0.53.0` 在 `/inner-brain-eval-local` 的后续处理段落中列出真实本机 evaluation JSONL 文件名、样本数量和可复制的文件聚焦命令。

## 范围

- `/inner-brain-eval-local` 有本机样本且存在来源文件时，追加：
  - `可聚焦文件：`
  - `/inner-brain-eval-local-file 当前文件名`
  - 当前文件样本数量
- 保留原有失败视图、已处理清单和占位文件聚焦入口。
- `/inner-brain-eval-local-file 文件名`、失败视图、已处理视图和报告导出不改行为。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不调整 seed/runtime 样本、不新增自然语言意图正则、不改变轻量分类器评分。
- 不改变 `/inner-brain-eval-local-report` 导出的 Markdown 报告内容。

## 验收

- `/inner-brain-eval-local` 有多个本机 evaluation 文件时输出具体文件名候选和数量。
- 输出包含可复制的 `/inner-brain-eval-local-file 文件名` 命令。
- 空本机 evaluation 样本仍只显示添加样本引导，不追加文件名候选。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke均通过。
