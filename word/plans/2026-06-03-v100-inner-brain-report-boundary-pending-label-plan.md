# v100：InnerBrain 本机报告处理边界待处理失败标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v99 全量评估帮助固定与本机评估集标签，明确 `0.96.0` 的本机评估报告处理边界提示。

## 目标

`0.96.0` 把导出的 `word/inner-brain-evaluation-report.md` 处理边界提示从“需要修复失败样本时”收紧为“需要修复待处理失败样本时”。这样 Markdown 报告标题、导出反馈、计数和处理边界都使用同一套待处理失败语义。

## 边界

- 不修改报告标题、报告路径、统计分组、失败筛选或修复建议内容。
- 不修改本机 evaluation JSONL payload、命令集合、运行日志或训练样本写入。
- 不新增真实本机 evaluation 样本。

## 实现要点

- 修改 `export_inner_brain_evaluation_report()` 的处理边界提示。
- 更新 InnerBrain 报告导出测试，断言新提示并排除旧提示。
- 项目版本提升到 `0.96.0`，更新更新清单测试夹具到 `0.96.1`。

## 验证

- RED：报告导出断言和版本一致性测试先失败，证明当前报告仍输出旧提示。
- GREEN：实现后目标测试通过。
- 回归：InnerBrain + Agent + ProjectMetadata 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。
