# v61 InnerBrain 本机文件失败视图已处理入口方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v60 本机失败视图失败文件汇总排序，明确 `0.57.0` 的当前文件失败视图后续处理入口。

## 目标

`0.57.0` 在 `/inner-brain-eval-local-file-failed 文件名` 的后续处理区中提示查看同一 JSONL 文件的已处理样本。用户聚焦某个文件的失败样本后，可以直接切到 `/inner-brain-eval-local-resolved 当前文件名` 对照该文件已经通过的本机 evaluation 样本。

## 范围

- `/inner-brain-eval-local-file-failed 文件名` 有失败样本时，后续处理追加：
  - `/inner-brain-eval-local-resolved 当前文件名`
- 保留当前输出中的全部失败视图入口、当前文件报告导出入口和全部报告导出入口。
- `/inner-brain-eval-local-failed` 未指定文件时不追加具体文件的已处理入口。

## 非目标

- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不修改本机 evaluation JSONL payload、保存路径或去重策略。
- 不改变评估执行、失败样例、失败原因、汇总分组或报告导出内容。
- 不新增命令，仅复用既有 `/inner-brain-eval-local-resolved [文件名]`。

## 验收

- `/inner-brain-eval-local-file-failed failed-log.jsonl` 输出包含 `- 查看当前文件已处理样本：/inner-brain-eval-local-resolved failed-log.jsonl`。
- 输出仍包含查看全部本机失败样本、导出当前文件失败报告和导出全部本机失败报告。
- 执行命令后不创建 `data/inner-brain/training/runtime.jsonl`。
- 目标测试、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke 均通过。
