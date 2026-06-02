# v86：InnerBrain 本机失败报告导出反馈全量待处理失败标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v85 本机当前文件反馈全部待处理失败标签，明确 `0.82.0` 的本机失败报告导出反馈全量待处理失败标签。

## 目标

`0.82.0` 在 `/inner-brain-eval-local-report` 未指定文件的导出反馈中，把返回全量失败视图的入口从 `查看本机失败样本：/inner-brain-eval-local-failed` 调整为 `查看待处理失败样本：/inner-brain-eval-local-failed`。这样全量报告导出反馈与指定文件报告导出反馈、全量已处理视图的“待处理失败样本”语义保持一致。

## 范围

- 修改 `JarvisAgent._export_inner_brain_local_evaluation_report()` 未指定文件分支的后续处理标签：
  - `查看待处理失败样本：/inner-brain-eval-local-failed`
  - `按文件聚焦失败：/inner-brain-eval-local-file-failed 文件名`
  - `补命令评估样本：/inner-brain-eval-add 文本 => /命令`
  - `补意图评估样本：/inner-brain-eval-label 文本 => intent [slot=value ...]`
- 同步更新 Agent 断言、项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload、训练样本写入或命令集合。

## 验证

- RED：全量报告导出反馈相关 Agent 测试和版本一致性测试先失败，证明反馈仍输出旧的“查看本机失败样本”文案。
- GREEN：实现后目标测试通过，全量报告导出反馈包含 `查看待处理失败样本：/inner-brain-eval-local-failed`。
- 回归：运行 Agent + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
