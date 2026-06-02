# v67 InnerBrain 本机失败视图失败文件分组聚焦入口方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v66 本机评估全量视图文件候选待处理入口，明确 `0.63.0` 的本机失败视图失败文件分组聚焦入口。

## 目标

`0.63.0` 在 `/inner-brain-eval-local-failed` 的 `失败文件：` 分组行中，为每个仍有失败样本的来源 JSONL 文件追加可复制的失败聚焦入口。用户查看全部本机失败样本时，可以直接从文件分组行进入 `/inner-brain-eval-local-file-failed 当前文件名`，不再手动拼接文件名。

## 范围

- `/inner-brain-eval-local-failed` 未指定文件且存在失败样本时，`失败文件：` 分组继续显示来源文件和失败数量。
- 每个失败文件分组行追加：
  - `/inner-brain-eval-local-file-failed 当前文件名`。
- 失败文件分组继续按失败数量降序、文件名升序排序。
- 复用 `describe_inner_brain_evaluation(..., failures_only=True)` 的 Markdown 报告同步获得该入口，保持聊天响应和导出内容一致。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不改变失败样例、失败原因、失败类型、期望意图、意图混淆或修复建议分组。
- 不改变指定文件失败视图；指定文件时继续不显示跨文件 `失败文件：` 分组。
- 不新增命令，仅复用既有 `/inner-brain-eval-local-file-failed [文件名]`。

## 验收

- `/inner-brain-eval-local-failed` 输出包含 `- failed-log.jsonl：1 条：/inner-brain-eval-local-file-failed failed-log.jsonl`。
- 纯通过的 `real-log.jsonl` 不出现在 `失败文件：` 分组中。
- 多文件失败分组仍按失败数量降序、文件名升序排序，且排序断言使用追加入口后的完整行。
- `/inner-brain-eval-local-file-failed 文件名` 指定文件视图不出现跨文件 `失败文件：` 分组。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
