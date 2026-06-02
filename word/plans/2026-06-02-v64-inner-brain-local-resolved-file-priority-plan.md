# v64 InnerBrain 本机已处理视图文件候选待处理优先排序方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v63 本机已处理视图文件候选状态摘要，明确 `0.60.0` 的本机已处理视图文件候选待处理优先排序。

## 目标

`0.60.0` 在 `/inner-brain-eval-local-resolved` 的 `可查看文件：` 候选列表中，优先展示同文件仍有待处理失败样本的 JSONL 文件。用户查看已处理样本后，可以先回到仍有失败的文件继续治理，而不是被纯已处理文件的通过数量干扰。

## 范围

- `/inner-brain-eval-local-resolved` 未指定文件且存在通过样本时，候选排序调整为：
  - 同文件待处理失败数量降序。
  - 已处理数量降序。
  - 文件名升序。
- 候选行继续显示已处理数量、同文件待处理失败数量和 `/inner-brain-eval-local-resolved 当前文件名`。
- 候选文件仍只包含有通过样本的来源文件。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不改变失败视图、报告导出、全量本机评估视图或指定文件已处理视图。
- 不新增命令，仅调整既有全量已处理视图候选排序。

## 验收

- 有待处理失败的 `real-log.jsonl` 排在纯已处理但通过数更多的 `clean-log.jsonl` 前。
- 候选行继续输出 `已处理 N 条，待处理失败 N 条`。
- 纯失败文件不出现在 `可查看文件：` 候选中。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
