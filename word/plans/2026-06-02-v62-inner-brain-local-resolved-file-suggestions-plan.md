# v62 InnerBrain 本机已处理视图文件候选提示方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v61 本机文件失败视图已处理入口，明确 `0.58.0` 的本机已处理视图文件候选提示。

## 目标

`0.58.0` 在 `/inner-brain-eval-local-resolved` 的后续处理区中列出当前有已处理样本的本机 evaluation JSONL 文件。用户查看全部已处理样本后，可以直接复制 `/inner-brain-eval-local-resolved 当前文件名` 聚焦同一文件的已通过样本。

## 范围

- `/inner-brain-eval-local-resolved` 未指定文件且存在通过样本时，追加：
  - `可查看文件：`
  - `/inner-brain-eval-local-resolved 当前文件名`
- 候选文件只统计当前通过样本，不列纯失败文件。
- 候选排序：通过数量降序、文件名升序。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不改变已处理样例、失败视图、报告导出或指定文件已处理视图。
- 不新增命令，仅复用既有 `/inner-brain-eval-local-resolved [文件名]`。

## 验收

- `/inner-brain-eval-local-resolved` 输出包含 `可查看文件：`。
- 有通过样本的 `real-log.jsonl` 输出 `- real-log.jsonl：1 条：/inner-brain-eval-local-resolved real-log.jsonl`。
- 纯失败文件不出现在 `可查看文件：` 候选中。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
