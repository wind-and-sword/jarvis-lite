# v102：InnerBrain 本机报告指定文件样本计数提示方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v101 本机失败视图文档待处理失败标签，明确 `0.98.0` 的指定文件报告导出反馈样本计数提示。

## 目标

`0.98.0` 在 `/inner-brain-eval-local-report [文件名]` 的成功反馈中追加 `当前文件样本：N`。当指定的 `runtime.jsonl` 或其他本机 evaluation 文件当前没有样本时，用户可以直接从响应判断这是“无样本”，而不是误以为只是没有待处理失败。

## 边界

- 不改变 Markdown 报告正文、报告路径或报告文件名。
- 不改变本机 evaluation JSONL payload、训练样本写入、筛选、排序或后续处理入口。
- 不改变缺失指定文件仍可导出空报告的既有行为。

## 实现

- 在 `_export_inner_brain_local_evaluation_report()` 的指定文件分支中复用 `report.total_count`。
- 有 `source_file_filter` 时，在 `评估文件：...` 后输出 `当前文件样本：N`。
- 项目版本提升到 `0.98.0`，更新更新清单测试夹具到 `0.98.1`。

## 验证

- RED：新增指定文件空报告反馈测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：Agent + ProjectMetadata 相邻回归、全量 `unittest`、源码 smoke、安装包构建、打包后 smoke、静态检查和 Markdown 本地链接检查。
