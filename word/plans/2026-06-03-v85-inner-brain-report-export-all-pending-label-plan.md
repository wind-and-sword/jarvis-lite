# v85：InnerBrain 本机当前文件反馈全部待处理失败标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v84 本机失败报告导出反馈当前文件待处理失败标签，明确 `0.81.0` 的本机当前文件失败反馈全部待处理失败标签。

## 目标

`0.81.0` 在 `/inner-brain-eval-local-file-failed 文件名` 和 `/inner-brain-eval-local-report 文件名` 的后续处理中，把返回全量失败视图的入口从 `查看全部本机失败样本：/inner-brain-eval-local-failed` 调整为 `查看全部待处理失败样本：/inner-brain-eval-local-failed`。这样指定文件失败视图、指定文件报告导出反馈和指定文件已处理视图的“待处理失败样本”语义保持一致。

## 范围

- 修改 `JarvisAgent._describe_inner_brain_local_failed_evaluation()` 指定文件分支的后续处理标签：
  - `当前文件总览：/inner-brain-eval-local-file 当前文件名`
  - `查看当前文件已处理样本：/inner-brain-eval-local-resolved 当前文件名`
  - `查看全部待处理失败样本：/inner-brain-eval-local-failed`
  - `导出当前文件失败报告：/inner-brain-eval-local-report 当前文件名`
  - `导出全部本机失败报告：/inner-brain-eval-local-report`
- 修改 `JarvisAgent._export_inner_brain_local_evaluation_report()` 指定文件分支的后续处理标签：
  - `当前文件总览：/inner-brain-eval-local-file 当前文件名`
  - `查看当前文件待处理失败样本：/inner-brain-eval-local-file-failed 当前文件名`
  - `查看当前文件已处理样本：/inner-brain-eval-local-resolved 当前文件名`
  - `查看全部待处理失败样本：/inner-brain-eval-local-failed`
- 同步更新 Agent 断言、项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改失败视图主体、报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload、训练样本写入或命令集合。

## 验证

- RED：指定文件失败视图、指定文件报告导出反馈相关 Agent 测试和版本一致性测试先失败，证明反馈仍输出旧的“查看全部本机失败样本”文案。
- GREEN：实现后目标测试通过，指定文件失败视图和指定文件报告导出反馈均包含 `查看全部待处理失败样本：/inner-brain-eval-local-failed`。
- 回归：运行 Agent + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
