# v82：InnerBrain 本机已处理指定文件视图当前文件总览标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v81 本机文件失败视图当前文件总览标签，明确 `0.78.0` 的本机已处理指定文件视图当前文件总览标签。

## 目标

`0.78.0` 在 `/inner-brain-eval-local-resolved 文件名` 的后续处理中，把回到同文件全部样本的入口从 `查看当前文件全部样本：/inner-brain-eval-local-file 当前文件名` 调整为 `当前文件总览：/inner-brain-eval-local-file 当前文件名`。这样指定文件已处理视图与失败视图、全量候选行的“总览”语义保持一致。

## 范围

- 指定文件已处理视图继续保留：
  - `当前文件总览：/inner-brain-eval-local-file 当前文件名`
  - `查看当前文件待处理失败样本：/inner-brain-eval-local-file-failed 当前文件名`
  - 当前文件仍有失败时的 `导出当前文件失败报告：/inner-brain-eval-local-report 当前文件名`
  - `查看全部已处理样本：/inner-brain-eval-local-resolved`
  - `查看全部待处理失败样本：/inner-brain-eval-local-failed`
- 全量已处理视图、指定文件失败视图、报告导出反馈和本机 evaluation 样本保存反馈保持既有入口。
- 不新增命令，继续复用既有 `/inner-brain-eval-local-file [文件名]`。
- 不修改评估主体、已处理筛选、失败排序、失败修复建议、报告正文、训练样本写入或本机 evaluation JSONL payload。

## 验收

- RED：指定文件已处理视图相关 Agent 测试和版本一致性测试先失败，证明后续处理仍输出旧的“查看当前文件全部样本”文案。
- GREEN：实现后目标测试通过，指定文件已处理视图包含 `当前文件总览：/inner-brain-eval-local-file real-log.jsonl`。
- 回归：运行 `tests.test_agent`、`tests.test_project_metadata` 和全量 `unittest discover`。
- 打包：构建 Windows 安装包并验证源码 smoke、打包后 exe smoke、安装脚本版本号和 Markdown 本地链接。
