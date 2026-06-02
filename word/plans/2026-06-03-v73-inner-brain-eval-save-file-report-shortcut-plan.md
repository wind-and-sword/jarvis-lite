# v73 InnerBrain 本机 evaluation 保存反馈按文件报告入口方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v72 本机已处理指定文件视图报告入口，明确 `0.69.0` 的本机 evaluation 保存反馈按文件报告入口。

## 目标

`0.69.0` 在 `/inner-brain-eval-add`、`/inner-brain-eval-label`、`/inner-brain-eval-add-candidate` 和 `/inner-brain-eval-label-candidate` 保存本机 evaluation 样本后，直接提示可复制的当前样本文件报告入口 `/inner-brain-eval-local-report runtime.jsonl`。用户保存真实日志样本后，可以先复跑本机评估，再按 `runtime.jsonl` 聚焦或导出失败报告，不需要手动拼接文件名。

## 范围

- 四条本机 evaluation 保存入口继续复用统一反馈出口。
- 保存反馈保留：
  - `/inner-brain-eval-local`
  - `/inner-brain-eval-local-failed`
  - `/inner-brain-eval-local-file runtime.jsonl`
- 保存反馈的报告入口改为：
  `/inner-brain-eval-local-report runtime.jsonl`

## 非目标

- 不新增命令，继续复用既有 `/inner-brain-eval-local-report [文件名]`。
- 不自动运行本机评估或报告导出。
- 不改变本机 evaluation JSONL payload、保存路径、去重逻辑或候选保留逻辑。
- 不写入 `data/inner-brain/training/runtime.jsonl`。

## 验收

- RED：新增 Agent 本机 evaluation 保存反馈按文件报告入口断言和版本一致性测试先失败。
- GREEN：实现后目标测试通过，保存反馈包含 `/inner-brain-eval-local-report runtime.jsonl`。
- 回归：运行 Agent + ProjectMetadata 相邻测试、全量 `unittest`、桌面 smoke、安装包构建、打包后 exe smoke、静态检查、Markdown 本地链接检查和敏感信息差异扫描。
