# v83：InnerBrain 本机失败报告导出反馈当前文件总览标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v82 本机已处理指定文件视图当前文件总览标签，明确 `0.79.0` 的本机失败报告导出反馈当前文件总览标签。

## 目标

`0.79.0` 在 `/inner-brain-eval-local-report 文件名` 的导出反馈中，把回到同文件全部样本的入口从 `查看当前文件全部样本：/inner-brain-eval-local-file 当前文件名` 调整为 `当前文件总览：/inner-brain-eval-local-file 当前文件名`。这样报告导出反馈与指定文件失败视图、指定文件已处理视图的“当前文件总览”语义保持一致。

## 范围

- 指定文件报告导出反馈继续保留：
  - `当前文件总览：/inner-brain-eval-local-file 当前文件名`
  - `复查当前文件失败样本：/inner-brain-eval-local-file-failed 当前文件名`
  - `查看当前文件已处理样本：/inner-brain-eval-local-resolved 当前文件名`
  - `查看全部本机失败样本：/inner-brain-eval-local-failed`
  - 补命令评估样本和补意图评估样本入口
- 全量报告导出反馈、报告正文、失败统计、报告导出路径和本机 evaluation JSONL payload 保持不变。
- 不新增命令，继续复用既有 `/inner-brain-eval-local-file [文件名]`。
- 不自动训练，不写入 `data/inner-brain/training/runtime.jsonl`。

## 验收

- RED：指定文件报告导出反馈相关 Agent 测试和版本一致性测试先失败，证明反馈仍输出旧的“查看当前文件全部样本”文案。
- GREEN：实现后目标测试通过，指定文件报告导出反馈包含 `当前文件总览：/inner-brain-eval-local-file failed-log.jsonl`。
- 回归：运行 `tests.test_agent`、`tests.test_project_metadata` 和全量 `unittest discover`。
- 打包：构建 Windows 安装包并验证源码 smoke、打包后 exe smoke、安装脚本版本号和 Markdown 本地链接。
