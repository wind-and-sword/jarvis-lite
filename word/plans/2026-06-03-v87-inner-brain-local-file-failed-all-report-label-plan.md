# v87：InnerBrain 本机文件失败视图全部待处理失败报告标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v86 本机失败报告导出反馈全量待处理失败标签，明确 `0.83.0` 的本机文件失败视图全部待处理失败报告标签。

## 目标

`0.83.0` 在 `/inner-brain-eval-local-file-failed 文件名` 的后续处理中，把返回全量报告导出的入口从 `导出全部本机失败报告：/inner-brain-eval-local-report` 调整为 `导出全部待处理失败报告：/inner-brain-eval-local-report`。这样指定文件失败视图中的“查看全部待处理失败样本”和“导出全部待处理失败报告”语义保持一致。

## 范围

- 修改 `JarvisAgent._describe_inner_brain_local_failed_evaluation()` 指定文件分支的全量报告入口标签：
  - `当前文件总览：/inner-brain-eval-local-file 当前文件名`
  - `查看当前文件已处理样本：/inner-brain-eval-local-resolved 当前文件名`
  - `查看全部待处理失败样本：/inner-brain-eval-local-failed`
  - `导出当前文件失败报告：/inner-brain-eval-local-report 当前文件名`
  - `导出全部待处理失败报告：/inner-brain-eval-local-report`
- 同步更新 Agent 断言、项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改全量失败视图、报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload、训练样本写入或命令集合。

## 验证

- RED：指定文件失败视图相关 Agent 测试和版本一致性测试先失败，证明反馈仍输出旧的“导出全部本机失败报告”文案。
- GREEN：实现后目标测试通过，指定文件失败视图包含 `导出全部待处理失败报告：/inner-brain-eval-local-report`。
- 回归：运行 Agent + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
