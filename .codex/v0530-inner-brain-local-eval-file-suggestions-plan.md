# 0.53.0 InnerBrain 本机评估全量视图文件名候选提示计划

> 日期：2026-06-02
> 执行者：Codex

## 目标

让 `/inner-brain-eval-local` 在有多个本机 evaluation JSONL 文件时，直接列出可复制的文件聚焦命令和样本数量。用户不需要把 `文件名` 占位再从其它视图里手动替换。

## 约束

- 只改变 Agent 响应文本。
- 不新增评估数据结构，复用 `InnerBrainEvaluationReport.source_file_counts`。
- 不自动训练、不写 `data/inner-brain/training/runtime.jsonl`。
- 不改变本机 evaluation JSONL payload、保存路径、报告导出内容或失败/已处理视图行为。

## 执行步骤

1. RED：补强 `/inner-brain-eval-local` 测试，写入至少两个本机 JSONL 文件，断言响应包含具体 `/inner-brain-eval-local-file 文件名` 命令和数量。
2. RED：版本一致性测试期望 `0.53.0`，更新更新检测 fixture 期望 `0.53.1`。
3. GREEN：在 `_describe_inner_brain_local_evaluation()` 的全量视图分支中追加文件名候选，按 `report.source_file_counts` 输出。
4. 文档：同步 README、PROJECT-PLAN、plans README、文档索引、进度和验证记录。
5. 验证：目标测试、InnerBrain+Agent 相邻回归、全量 unittest、桌面 smoke、安装包构建、打包后 exe smoke、静态和链接检查。
6. 提交：本地提交 `feat: 提示本机评估文件候选 0.53.0`。
