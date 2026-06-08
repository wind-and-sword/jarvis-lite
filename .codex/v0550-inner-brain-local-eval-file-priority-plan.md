# 0.55.0 InnerBrain 本机评估全量视图文件候选失败优先排序计划

> 日期：2026-06-02
> 执行者：Codex

## 目标

让 `/inner-brain-eval-local` 的 `可聚焦文件：` 候选列表按失败数量优先展示，帮助用户先进入有失败样本的 JSONL 文件。

## 约束

- 只改变 Agent 响应文本中的候选文件顺序。
- 不新增评估数据结构，在 Agent 层复用 `report.case_results` 和 `report.source_file_counts`。
- 不自动训练、不写 `data/inner-brain/training/runtime.jsonl`。
- 不改变文件过滤视图、失败视图、已处理视图、报告导出或本机 evaluation JSONL payload。

## 排序规则

1. 失败数量降序。
2. 总样本数量降序。
3. 文件名升序。

## 执行步骤

1. RED：补强 `/inner-brain-eval-local` 测试，构造纯通过文件名排在前、失败文件名排在后的样本，断言失败文件候选行先出现。
2. RED：版本一致性测试期望 `0.55.0`，更新更新检测 fixture 期望 `0.55.1`。
3. GREEN：在 Agent 层对候选文件排序，不改变候选行格式。
4. 文档：同步 README、PROJECT-PLAN、plans README、文档索引、进度和验证记录。
5. 验证：目标测试、InnerBrain+Agent 相邻回归、全量 `unittest`、桌面 smoke、安装包构建、打包后 exe smoke、静态和链接检查。
6. 提交：本地提交 `feat: 优先展示本机评估失败文件 0.55.0`。
