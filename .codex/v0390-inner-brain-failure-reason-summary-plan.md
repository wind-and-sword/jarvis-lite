# 0.39.0 InnerBrain 本机评估失败原因汇总计划

> 日期：2026-06-02
> 执行者：Codex
> 说明：当前会话未暴露 sequential-thinking、shrimp-task-manager、code-index、exa MCP；按项目约定降级为本地检索、update_plan、TDD 和本地验证。

## 目标

在 `/inner-brain-eval-local-report [文件名]` 导出的 `word/inner-brain-evaluation-report.md` 中增加失败原因汇总，让用户可以先按错误类型处理本机 evaluation JSONL 失败样本。

## 边界

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变 evaluation JSONL payload、去重键或本机样本读取路径。
- 不改变命令入口名称；继续复用 `/inner-brain-eval-local-report [文件名]`。
- 不引入聚类模型或新依赖；仅按现有失败原因文本计数。

## 执行步骤

1. RED：新增 InnerBrain 失败原因汇总测试，要求 failures-only 描述和导出 Markdown 包含 `失败原因汇总：`。
2. RED：新增 Agent 命令测试，要求 `/inner-brain-eval-local-report` 导出的报告包含失败原因汇总且不写 training runtime。
3. RED：更新版本一致性测试到 `0.39.0`，先确认失败。
4. GREEN：在 `InnerBrainEvaluationReport` 增加 `failed_reason_counts`，在 failures-only 描述中输出按数量排序的失败原因汇总。
5. GREEN：导出报告自然复用描述函数，Agent 无需新入口。
6. 版本与文档：同步 `pyproject.toml`、`src/jarvis_lite/__init__.py`、版本测试、README、PROJECT-PLAN、v43 方案索引、进度和验证记录。
7. 验证：目标测试、InnerBrain + Agent 回归、全量 unittest、源码桌面 smoke、Windows 安装包构建、打包 exe smoke、静态检查、链接检查、敏感扫描、本地配置跟踪检查。

## 验收

- 报告中出现 `失败原因汇总：`，按失败原因计数。
- 相同失败原因只显示一条汇总，并包含典型样本。
- 文件过滤报告仍显示 `评估文件：<文件名>`。
- 训练 runtime 文件不存在。
- 版本为 `0.39.0`，安装包为 `JarvisLiteSetup-0.39.0.exe`。
