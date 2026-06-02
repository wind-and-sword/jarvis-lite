# v92：InnerBrain 本机文件候选待处理报告标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v91 本机评估样本保存反馈待处理失败标签，明确 `0.88.0` 的本机文件候选待处理报告标签。

## 目标

`0.88.0` 在本机 evaluation 文件候选和失败文件分组中，把短标签从 `报告：/inner-brain-eval-local-report 文件名` 调整为 `待处理报告：/inner-brain-eval-local-report 文件名`。这样仍有失败的文件候选会明确表达报告针对待处理失败样本。

## 范围

- 修改 `describe_inner_brain_evaluation()` 未指定文件的失败文件分组：
  - `总览：/inner-brain-eval-local-file 文件名`
  - `待处理：/inner-brain-eval-local-file-failed 文件名`
  - `待处理报告：/inner-brain-eval-local-report 文件名`
- 修改 `JarvisAgent._describe_inner_brain_local_evaluation()` 未指定文件的文件候选：
  - `总览：/inner-brain-eval-local-file 文件名`
  - `待处理：/inner-brain-eval-local-file-failed 文件名`
  - `待处理报告：/inner-brain-eval-local-report 文件名`
- 修改 `JarvisAgent._inner_brain_local_resolved_evaluation()` 未指定文件的已处理文件候选：
  - `总览：/inner-brain-eval-local-file 文件名`
  - `已处理：/inner-brain-eval-local-resolved 文件名`
  - `待处理：/inner-brain-eval-local-file-failed 文件名`
  - `待处理报告：/inner-brain-eval-local-report 文件名`
- 同步更新 Agent 与 InnerBrain 断言、项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改候选排序、报告正文、报告导出路径、本机 evaluation JSONL payload、训练样本写入或命令集合。

## 验证

- RED：文件候选和失败文件分组相关测试以及版本一致性测试先失败，证明仍输出旧的 `报告：` 短标签。
- GREEN：实现后目标测试通过，并覆盖全量视图、失败视图、已处理视图和排序。
- 回归：运行 Agent + InnerBrain + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
