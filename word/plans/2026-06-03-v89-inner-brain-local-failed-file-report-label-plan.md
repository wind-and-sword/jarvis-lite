# v89：InnerBrain 本机失败视图按文件待处理失败报告标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v88 本机失败视图待处理失败报告标签，明确 `0.85.0` 的本机失败视图按文件待处理失败报告标签。

## 目标

`0.85.0` 在 `/inner-brain-eval-local-failed` 未指定文件的后续处理中，把按文件报告导出入口从 `按文件导出失败报告：/inner-brain-eval-local-report 文件名` 调整为 `按文件导出待处理失败报告：/inner-brain-eval-local-report 文件名`。这样全量失败视图里的全量报告入口和按文件报告入口都使用“待处理失败报告”语义。

## 范围

- 修改 `JarvisAgent._describe_inner_brain_local_failed_evaluation()` 未指定文件分支的按文件报告入口标签：
  - `按文件聚焦失败：/inner-brain-eval-local-file-failed 文件名`
  - `导出待处理失败报告：/inner-brain-eval-local-report`
  - `按文件导出待处理失败报告：/inner-brain-eval-local-report 文件名`
- 同步更新 Agent 断言、项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改指定文件失败视图、报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload、训练样本写入或命令集合。

## 验证

- RED：全量失败视图相关 Agent 测试和版本一致性测试先失败，证明反馈仍输出旧的“按文件导出失败报告”文案。
- GREEN：实现后目标测试通过，全量失败视图包含 `按文件导出待处理失败报告：/inner-brain-eval-local-report 文件名`。
- 回归：运行 Agent + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
