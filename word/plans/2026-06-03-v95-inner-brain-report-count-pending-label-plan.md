# v95：InnerBrain 本机报告导出反馈待处理失败计数标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v94 本机失败帮助待处理标签，明确 `0.91.0` 的本机报告导出反馈计数标签。

## 目标

`0.91.0` 在 `/inner-brain-eval-local-report [文件名]` 的导出反馈中，把计数行从 `失败样本：N` 收紧为 `待处理失败样本：N`。这样报告标题、帮助入口、运行日志、后续处理入口和导出反馈计数都使用同一套待处理失败语义。

## 范围

- 修改 `JarvisAgent._export_inner_brain_local_evaluation_report()`：
  - 成功反馈的计数行改为 `待处理失败样本：N`。
- 同步 Agent 测试、版本一致性测试、项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改 Markdown 报告正文里的失败统计标题，不修改命令集合、别名、失败筛选、排序、报告路径、本机 evaluation JSONL payload 或训练样本写入。

## 验证

- RED：报告导出反馈断言和版本一致性测试先失败，证明仍输出旧的 `失败样本：N`。
- GREEN：实现后目标测试通过，覆盖全量报告导出反馈、指定文件报告导出反馈和版本一致性。
- 回归：运行 Agent + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
