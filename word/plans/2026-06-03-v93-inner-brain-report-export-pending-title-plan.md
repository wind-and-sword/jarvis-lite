# v93：InnerBrain 本机报告导出待处理失败标题方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v92 本机文件候选待处理报告标签，明确 `0.89.0` 的本机报告导出待处理失败标题。

## 目标

`0.89.0` 在 `/inner-brain-eval-local-report [文件名]` 的导出反馈、运行日志和 Markdown 标题中，把“本机评估失败报告”调整为“本机评估待处理失败报告”。这样报告导出本身也和入口里的待处理失败语义保持一致。

## 范围

- 修改 `JarvisAgent._export_inner_brain_local_evaluation_report()`：
  - record_log 消息改为导出本机评估待处理失败报告。
  - 成功反馈改为 `已导出 InnerBrain 本机评估待处理失败报告。`
- 修改 `export_inner_brain_evaluation_report()`：
  - 函数说明和 Markdown H1 改为待处理失败报告。
- 同步更新 Agent、InnerBrain 和版本一致性测试、项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改报告文件路径、报告统计正文、失败样本筛选、报告导出命令、本机 evaluation JSONL payload 或训练样本写入。

## 验证

- RED：报告导出反馈、Markdown 标题和版本一致性测试先失败，证明仍输出旧的“本机评估失败报告”标题。
- GREEN：实现后目标测试通过，并覆盖全量导出、指定文件导出和 Markdown 内容。
- 回归：运行 Agent + InnerBrain + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
