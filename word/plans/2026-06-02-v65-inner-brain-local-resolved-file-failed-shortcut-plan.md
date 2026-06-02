# v65 InnerBrain 本机已处理视图文件候选待处理入口方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v64 本机已处理视图文件候选待处理优先排序，明确 `0.61.0` 的本机已处理视图文件候选待处理入口。

## 目标

`0.61.0` 在 `/inner-brain-eval-local-resolved` 的 `可查看文件：` 候选行中，为仍有待处理失败样本的来源 JSONL 文件追加失败聚焦入口。用户查看已处理样本时，可以直接从同一候选行跳到 `/inner-brain-eval-local-file-failed 当前文件名` 继续处理失败样本。

## 范围

- `/inner-brain-eval-local-resolved` 未指定文件且存在通过样本时，候选行继续显示：
  - 已处理数量。
  - 同文件待处理失败数量。
  - `/inner-brain-eval-local-resolved 当前文件名`。
- 当同文件待处理失败数量大于 0 时，同一候选行追加：
  - `待处理：/inner-brain-eval-local-file-failed 当前文件名`。
- 当同文件待处理失败数量为 0 时，候选行不追加失败入口，避免引导到空失败视图。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不改变已处理候选排序、失败视图、报告导出或指定文件已处理视图。
- 不新增命令，仅复用既有 `/inner-brain-eval-local-file-failed [文件名]`。

## 验收

- 有待处理失败的 `real-log.jsonl` 候选行包含 `待处理：/inner-brain-eval-local-file-failed real-log.jsonl`。
- 纯已处理的 `clean-log.jsonl` 候选行不包含 `待处理：/inner-brain-eval-local-file-failed clean-log.jsonl`。
- 候选排序仍保持待处理失败数量降序、已处理数量降序、文件名升序。
- 纯失败文件不出现在 `可查看文件：` 候选中。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
