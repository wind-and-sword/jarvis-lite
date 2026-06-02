# Jarvis Lite v52：InnerBrain 本机失败评估报告导出后续处理提示方案

> 日期：2026-06-02
> 执行者：Codex
> 说明：本文承接 v51 本机评估样本保存后续验证提示，明确 `0.48.0` 的本机失败评估报告导出后续处理提示闭环。

## 目标

`0.48.0` 在用户导出本机失败评估报告后，直接提示下一步处理命令。用户通过 `/inner-brain-eval-local-report` 或 `/inner-brain-eval-local-report 文件名` 写出 `word/inner-brain-evaluation-report.md` 后，可以马上看到如何查看本机失败样本、聚焦来源 JSONL 文件和继续补充本机 evaluation 样本。

## 边界

- 不新增命令。
- 不改变导出的 Markdown 报告内容。
- 不自动运行评估。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变 evaluation JSONL payload、去重键或保存路径。

## 实现要点

- 继续复用 `_export_inner_brain_local_evaluation_report()` 作为报告导出响应出口。
- 在响应末尾追加 `后续处理：`。
- 未指定文件时提示：
  - `/inner-brain-eval-local-failed`
  - `/inner-brain-eval-local-file-failed 文件名`
  - `/inner-brain-eval-add 文本 => /命令`
  - `/inner-brain-eval-label 文本 => intent [slot=value ...]`
- 指定文件时提示：
  - `/inner-brain-eval-local-file-failed <当前文件名>`
  - `/inner-brain-eval-local-failed`
  - `/inner-brain-eval-add 文本 => /命令`
  - `/inner-brain-eval-label 文本 => intent [slot=value ...]`
- 既有报告文件、失败样本数量、评估文件和“不写训练样本”说明保持不变。

## 验证

- RED：新增 Agent 报告导出后续处理提示测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain + Agent 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 用户沉淀真实本机 evaluation 样本后，再根据失败报告中的高频失败维度补 seed/runtime 样本、槽位补全或轻量评分补偿。
