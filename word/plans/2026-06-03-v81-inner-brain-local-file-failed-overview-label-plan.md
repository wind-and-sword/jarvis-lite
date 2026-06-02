# v81：InnerBrain 本机文件失败视图当前文件总览标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v80 本机评估全量视图文件候选总览标签，明确 `0.77.0` 的本机文件失败视图当前文件总览标签。

## 目标

`0.77.0` 在 `/inner-brain-eval-local-file-failed 文件名` 的后续处理中，把回到同文件全部样本的入口从 `查看当前文件全部样本：/inner-brain-eval-local-file 当前文件名` 调整为 `当前文件总览：/inner-brain-eval-local-file 当前文件名`。这样指定文件失败视图和全量候选行中的“总览”语义保持一致。

## 范围

- 指定文件失败视图继续保留：
  - `当前文件总览：/inner-brain-eval-local-file 当前文件名`
  - `查看当前文件已处理样本：/inner-brain-eval-local-resolved 当前文件名`
  - `查看全部本机失败样本：/inner-brain-eval-local-failed`
  - `导出当前文件失败报告：/inner-brain-eval-local-report 当前文件名`
  - `导出全部本机失败报告：/inner-brain-eval-local-report`
- 全量失败视图、全量本机评估视图、已处理视图、报告导出反馈和样本保存反馈保持既有入口。
- 不新增命令，继续复用既有 `/inner-brain-eval-local-file [文件名]`。
- 不修改评估主体、失败排序、失败修复建议、报告正文、训练样本写入或本机 evaluation JSONL payload。

## 验收

- RED：指定文件失败视图相关 Agent 测试和版本一致性测试先失败，证明后续处理仍输出旧的“查看当前文件全部样本”文案。
- GREEN：实现后目标测试通过，指定文件失败视图包含 `当前文件总览：/inner-brain-eval-local-file failed-log.jsonl`。
- 回归：运行 `tests.test_agent`、`tests.test_project_metadata` 和全量 `unittest discover`。
- 打包：构建 Windows 安装包并验证源码 smoke、打包后 exe smoke、安装脚本版本号和 Markdown 本地链接。
