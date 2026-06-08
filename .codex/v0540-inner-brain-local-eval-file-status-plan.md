# 0.54.0 InnerBrain 本机评估全量视图文件候选状态摘要计划

> 日期：2026-06-02
> 执行者：Codex

## 目标

让 `/inner-brain-eval-local` 的 `可聚焦文件：` 候选行同时展示每个本机 evaluation JSONL 文件的通过和失败数量，帮助用户优先进入有失败的文件。

## 约束

- 只改变 Agent 响应文本。
- 不新增评估数据结构，在 Agent 层复用 `report.case_results` 和 `report.source_file_counts`。
- 不自动训练、不写 `data/inner-brain/training/runtime.jsonl`。
- 不改变文件过滤视图、失败视图、已处理视图、报告导出或本机 evaluation JSONL payload。

## 执行步骤

1. RED：补强 `/inner-brain-eval-local` 测试，断言候选文件行包含 `通过 N 条，失败 N 条`。
2. RED：版本一致性测试期望 `0.54.0`，更新更新检测 fixture 期望 `0.54.1`。
3. GREEN：在 Agent 层按 `source_file` 统计 passed/failed，扩展候选文件行。
4. 文档：同步 README、PROJECT-PLAN、plans README、文档索引、进度和验证记录。
5. 验证：目标测试、InnerBrain+Agent 相邻回归、全量 unittest、桌面 smoke、安装包构建、打包后 exe smoke、静态和链接检查。
6. 提交：本地提交 `feat: 汇总本机评估文件候选状态 0.54.0`。
