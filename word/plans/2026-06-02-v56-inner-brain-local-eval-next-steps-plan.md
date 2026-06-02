# v56 InnerBrain 本机评估全量视图后续处理提示方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v55 本机 evaluation 已处理样本只读清单，明确 `0.52.0` 的本机评估全量视图后续处理提示。

## 目标

`0.52.0` 在 `/inner-brain-eval-local` 和 `/inner-brain-eval-local-file 文件名` 的响应后追加后续处理入口。用户看到本机 evaluation 全量结果后，可以立即切换到待处理失败样本、已处理样本或文件聚焦视图。

## 范围

- `/inner-brain-eval-local` 有本机样本时提示：
  - `/inner-brain-eval-local-failed`
  - `/inner-brain-eval-local-resolved`
  - `/inner-brain-eval-local-file 文件名`
- `/inner-brain-eval-local-file 文件名` 有样本时提示：
  - `/inner-brain-eval-local-file-failed 当前文件名`
  - `/inner-brain-eval-local-resolved 当前文件名`
  - `/inner-brain-eval-local`
- 本机 evaluation 样本为空时保留添加样本引导，不追加全量后续处理。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不调整 seed/runtime 样本、不新增自然语言意图正则、不改变轻量分类器评分。
- 不改变 `/inner-brain-eval-local-report` 导出的 Markdown 报告内容。

## 验收

- `/inner-brain-eval-local` 有样本时输出 `后续处理：` 和失败/已处理/文件聚焦入口。
- `/inner-brain-eval-local-file 文件名` 有样本时输出当前文件失败视图、当前文件已处理清单和返回全部本机评估入口。
- 空本机 evaluation 样本仍只显示添加样本引导，不追加全量后续处理。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
