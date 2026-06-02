# v90：InnerBrain 本机当前文件待处理失败报告标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v89 本机失败视图按文件待处理失败报告标签，明确 `0.86.0` 的本机当前文件待处理失败报告标签。

## 目标

`0.86.0` 在当前文件相关反馈中，把当前文件报告导出入口从 `导出当前文件失败报告：/inner-brain-eval-local-report 文件名` 调整为 `导出当前文件待处理失败报告：/inner-brain-eval-local-report 文件名`。这样当前文件总览、当前文件失败视图和当前文件已处理视图里的报告入口都明确指向仍待处理的失败样本。

## 范围

- 修改 `JarvisAgent._describe_inner_brain_local_evaluation()` 指定文件分支：
  - `查看当前文件待处理失败样本：/inner-brain-eval-local-file-failed 当前文件名`
  - `查看当前文件已处理样本：/inner-brain-eval-local-resolved 当前文件名`
  - `导出当前文件待处理失败报告：/inner-brain-eval-local-report 当前文件名`
- 修改 `JarvisAgent._describe_inner_brain_local_failed_evaluation()` 指定文件分支：
  - `当前文件总览：/inner-brain-eval-local-file 当前文件名`
  - `查看当前文件已处理样本：/inner-brain-eval-local-resolved 当前文件名`
  - `查看全部待处理失败样本：/inner-brain-eval-local-failed`
  - `导出当前文件待处理失败报告：/inner-brain-eval-local-report 当前文件名`
  - `导出全部待处理失败报告：/inner-brain-eval-local-report`
- 修改 `JarvisAgent._inner_brain_local_resolved_evaluation()` 指定文件分支：
  - `当前文件总览：/inner-brain-eval-local-file 当前文件名`
  - `查看当前文件待处理失败样本：/inner-brain-eval-local-file-failed 当前文件名`
  - `导出当前文件待处理失败报告：/inner-brain-eval-local-report 当前文件名`
- 同步更新 Agent 断言、项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改报告正文、失败统计、报告导出路径、本机 evaluation JSONL payload、训练样本写入或命令集合。

## 验证

- RED：三个当前文件报告入口相关 Agent 测试和版本一致性测试先失败，证明反馈仍输出旧的“导出当前文件失败报告”文案。
- GREEN：实现后目标测试通过，并分别覆盖当前文件总览、当前文件失败视图和当前文件已处理视图。
- 回归：运行 Agent + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
