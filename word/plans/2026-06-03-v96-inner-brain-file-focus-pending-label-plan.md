# v96：InnerBrain 本机全量反馈按文件聚焦待处理失败标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v95 本机报告导出反馈待处理失败计数标签，明确 `0.92.0` 的按文件聚焦待处理失败标签。

## 目标

`0.92.0` 在本机全量失败视图和全量报告导出反馈中，把 `按文件聚焦失败：/inner-brain-eval-local-file-failed 文件名` 收紧为 `按文件聚焦待处理失败：/inner-brain-eval-local-file-failed 文件名`。这样入口标签会明确表达目标视图只展示待处理失败样本。

## 范围

- 修改 `JarvisAgent._describe_inner_brain_local_failed_evaluation()` 未指定文件分支：
  - 后续处理入口改为 `按文件聚焦待处理失败：/inner-brain-eval-local-file-failed 文件名`。
- 修改 `JarvisAgent._export_inner_brain_local_evaluation_report()` 未指定文件分支：
  - 后续处理入口改为 `按文件聚焦待处理失败：/inner-brain-eval-local-file-failed 文件名`。
- 同步 Agent 测试、版本一致性测试、项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改固定评估 `/inner-brain-eval-failed`，不修改指定文件反馈、命令集合、别名、筛选、排序、报告路径、本机 evaluation JSONL payload 或训练样本写入。

## 验证

- RED：两个全量反馈标签断言和版本一致性测试先失败，证明仍输出旧的 `按文件聚焦失败`。
- GREEN：实现后目标测试通过，覆盖全量本机失败视图、全量报告导出反馈和版本一致性。
- 回归：运行 Agent + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
