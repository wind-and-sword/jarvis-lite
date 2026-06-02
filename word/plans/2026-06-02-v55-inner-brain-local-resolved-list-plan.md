# v55 InnerBrain 本机 evaluation 已处理样本只读清单方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v54 本机失败视图文件聚焦提示，明确 `0.51.0` 的本机 evaluation 已处理样本只读清单闭环。

## 目标

`0.51.0` 增加 `/inner-brain-eval-local-resolved [文件名]`，让用户在处理本机 evaluation 失败样本后，可以只读查看当前已经通过的本机样本。它与 `/inner-brain-eval-local-failed` 互补：失败视图用于找待处理样本，已处理清单用于确认哪些本机样本已经由 seed/runtime 补强或分类器改进覆盖。

## 范围

- 新增只读命令 `/inner-brain-eval-local-resolved [文件名]`。
- 省略文件名时查看全部本机 evaluation 已通过样本。
- 指定文件名时只查看该 JSONL 文件里当前已通过的样本，文件名继续支持省略 `.jsonl`。
- 输出 `已处理样例：`，无已通过样本时显示 `- 无`。
- 命令输出提示可回到 `/inner-brain-eval-local-failed` 查看待处理样本。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改 `data/inner-brain/evaluation/*.jsonl` payload、保存路径或去重策略。
- 不调整 seed/runtime 样本、不新增自然语言意图正则、不改变轻量分类器评分。
- 不改变 `/inner-brain-eval-local-report` 导出的 Markdown 报告内容。

## 验收

- `/inner-brain-eval-local-resolved` 只显示 `local_evaluation` 中当前通过的样本，不显示失败样本。
- `/inner-brain-eval-local-resolved 文件名` 只显示指定本机 JSONL 文件的当前通过样本。
- 空本机样本或指定文件没有已通过样本时显示 `已处理样例：- 无`。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
