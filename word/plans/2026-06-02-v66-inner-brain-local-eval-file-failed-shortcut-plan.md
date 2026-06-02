# v66 InnerBrain 本机评估全量视图文件候选待处理入口方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v65 本机已处理视图文件候选待处理入口，明确 `0.62.0` 的本机评估全量视图文件候选待处理入口。

## 目标

`0.62.0` 在 `/inner-brain-eval-local` 的 `可聚焦文件：` 候选行中，为仍有失败样本的来源 JSONL 文件追加失败聚焦入口。用户查看本机全量评估结果时，可以直接从候选行进入 `/inner-brain-eval-local-file-failed 当前文件名` 处理同文件失败样本。

## 范围

- `/inner-brain-eval-local` 未指定文件且存在本机样本时，候选行继续显示：
  - 文件总样本数量。
  - 通过数量。
  - 失败数量。
  - `/inner-brain-eval-local-file 当前文件名`。
- 当同文件失败数量大于 0 时，同一候选行追加：
  - `待处理：/inner-brain-eval-local-file-failed 当前文件名`。
- 当同文件失败数量为 0 时，候选行不追加失败入口。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不改变文件候选排序、失败视图、报告导出或指定文件本机评估视图。
- 不新增命令，仅复用既有 `/inner-brain-eval-local-file-failed [文件名]`。

## 验收

- 有失败样本的 `zzz-failed-log.jsonl` 候选行包含 `待处理：/inner-brain-eval-local-file-failed zzz-failed-log.jsonl`。
- 纯通过的 `aaa-real-log.jsonl` 候选行不包含 `待处理：/inner-brain-eval-local-file-failed aaa-real-log.jsonl`。
- 候选排序仍保持失败数量降序、总样本数降序、文件名升序。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
