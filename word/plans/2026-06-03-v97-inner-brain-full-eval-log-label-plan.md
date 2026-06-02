# v97：InnerBrain 全量评估运行日志固定与本机评估集标签方案

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v96 本机全量反馈按文件聚焦待处理失败标签，明确 `0.93.0` 的全量评估运行日志标签。

## 目标

`0.93.0` 把 `/inner-brain-eval` 与 `/inner-brain-eval-failed` 的运行日志从“本地评估集”收紧为“固定与本机评估集”。这两个命令会执行固定 seed 评估并合并本机 `data/inner-brain/evaluation/*.jsonl` 样本，日志应和只看本机样本的 `/inner-brain-eval-local` 区分。

## 范围

- 修改 `/inner-brain-eval` 分支的 `record_log` 文案：
  - `执行 InnerBrain 固定与本机评估集`。
- 修改 `/inner-brain-eval-failed` 分支的 `record_log` 文案：
  - `执行 InnerBrain 固定与本机评估集并只显示失败样本`。
- 同步 Agent 测试、版本一致性测试、项目版本、README、PROJECT-PLAN、计划索引、进度和验证记录。
- 不修改评估输出正文、不修改 `/inner-brain-eval-local` 或指定文件本机评估日志、不修改命令集合、别名、失败筛选、排序、报告正文、报告路径、本机 evaluation JSONL payload 或训练样本写入。

## 验证

- RED：全量评估日志标签断言、全量失败评估日志标签断言和版本一致性测试先失败，证明仍输出旧的“本地评估集”。
- GREEN：实现后目标测试通过，覆盖 `/inner-brain-eval`、`/inner-brain-eval-failed` 和版本一致性。
- 回归：运行 Agent + ProjectMetadata 相邻回归、全量 `unittest`、桌面 smoke、Windows 安装包构建、打包后 smoke、Markdown 链接检查、敏感信息差异扫描和本地配置文件检查。
