# v63 InnerBrain 本机已处理视图文件候选状态摘要方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v62 本机已处理视图文件候选提示，明确 `0.59.0` 的本机已处理视图文件候选状态摘要。

## 目标

`0.59.0` 在 `/inner-brain-eval-local-resolved` 的 `可查看文件：` 候选行中追加同一 JSONL 文件的待处理失败数量。用户查看已处理样本时，可以判断某个来源文件是否仍需要回到失败视图继续治理。

## 范围

- `/inner-brain-eval-local-resolved` 未指定文件且存在通过样本时，候选行显示：
  - 已处理数量。
  - 同文件待处理失败数量。
  - 可复制的 `/inner-brain-eval-local-resolved 当前文件名` 命令。
- 候选文件仍只包含有通过样本的来源文件。
- 候选排序继续保持通过数量降序、文件名升序。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不改变失败视图、报告导出、全量本机评估视图或指定文件已处理视图。
- 不新增命令，仅调整既有全量已处理视图候选行文案。

## 验收

- `/inner-brain-eval-local-resolved` 输出包含 `可查看文件：`。
- 有通过和失败样本的 `real-log.jsonl` 输出 `- real-log.jsonl：已处理 1 条，待处理失败 1 条：/inner-brain-eval-local-resolved real-log.jsonl`。
- 纯失败文件不出现在 `可查看文件：` 候选中。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
