# v91：InnerBrain 本机评估样本保存反馈待处理失败标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v90 本机当前文件待处理失败报告标签，明确 `0.87.0` 的本机评估样本保存反馈待处理失败标签。

## 目标

`0.87.0` 在本机 evaluation 样本保存反馈中，把后续验证入口从 `只看失败样本：/inner-brain-eval-local-failed` 调整为 `只看待处理失败样本：/inner-brain-eval-local-failed`，并把报告入口从 `导出样本文件失败报告：/inner-brain-eval-local-report runtime.jsonl` 调整为 `导出样本文件待处理失败报告：/inner-brain-eval-local-report runtime.jsonl`。

## 范围

- 修改 `JarvisAgent._describe_inner_brain_evaluation_case_save()` 的后续验证文案：
  - `复跑本机评估：/inner-brain-eval-local`
  - `只看待处理失败样本：/inner-brain-eval-local-failed`
  - `聚焦样本文件：/inner-brain-eval-local-file runtime.jsonl`
  - `导出样本文件待处理失败报告：/inner-brain-eval-local-report runtime.jsonl`
- 同步更新 eval-add、eval-label、eval-add-candidate、eval-label-candidate 四个保存入口断言。
- 同步更新项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改保存样本 JSONL payload、候选保留行为、训练写入、报告正文、报告路径或命令集合。

## 验证

- RED：四个保存入口 Agent 测试和版本一致性测试先失败，证明反馈仍输出旧的失败样本/失败报告标签。
- GREEN：实现后目标测试通过，并覆盖直接保存和候选保存两类入口。
- 回归：运行 Agent + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
