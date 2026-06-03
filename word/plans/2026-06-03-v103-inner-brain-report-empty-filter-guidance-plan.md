# v103：InnerBrain 本机报告空筛选文件补样本写入提示方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v102 本机报告指定文件样本计数提示，明确 `0.99.0` 的空筛选文件补样本写入提示。

## 目标

`0.99.0` 在 `/inner-brain-eval-local-report [文件名]` 的指定文件报告反馈中，如果当前筛选文件样本数为 0，则追加提示说明补样本命令默认写入 `runtime.jsonl`。这样用户看到 `当前文件样本：0` 时，能明确下一步应先沉淀本机 evaluation 样本，并理解默认写入目标。

## 边界

- 不新增按任意 JSONL 文件写入 evaluation 样本的命令。
- 不改变 `/inner-brain-eval-add` 或 `/inner-brain-eval-label` 的默认写入目标。
- 不改变 Markdown 报告正文、报告路径、缺失文件空报告行为、本机 evaluation JSONL payload、训练样本写入、筛选或排序。

## 实现

- 在 `_export_inner_brain_local_evaluation_report()` 的指定文件分支中判断 `report.total_count == 0`。
- 空筛选文件时，在 `当前文件样本：0` 后追加 `提示：当前筛选文件暂无本机 evaluation 样本；补样本命令默认写入 runtime.jsonl。`
- 项目版本提升到 `0.99.0`，更新更新清单测试夹具到 `0.99.1`。

## 验证

- RED：新增空筛选文件补样本写入提示测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：Agent + ProjectMetadata 相邻回归、全量 `unittest`、源码 smoke、安装包构建、打包后 smoke、静态检查和 Markdown 本地链接检查。
