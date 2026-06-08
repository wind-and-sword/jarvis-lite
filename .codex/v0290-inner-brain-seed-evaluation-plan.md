# 0.29.0 InnerBrain 固定评估集计划

> 日期：2026-06-01
> 执行者：Codex

## 目标

建立 InnerBrain 固定 seed 评估集和 `/inner-brain-eval` 命令，形成后续分类器优化的可重复基线。

## 约束

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳候选。
- 不写入 runtime 样本或最近路由候选。
- 第一批评估集只覆盖当前 seed 样本已经稳定支持的表达。

## 步骤

1. RED：新增 InnerBrain 评估 API 测试、Agent `/inner-brain-eval` 命令测试和版本一致性测试。
2. 实现：新增评估 dataclass、`seed_evaluation_cases()`、`evaluate_inner_brain()`、`describe_inner_brain_evaluation()`。
3. 接入：Agent 增加 `/inner-brain-eval` 和 `brain-eval`，并把它标为路由观察命令。
4. 文档：同步 README、PROJECT-PLAN、方案索引、进度和验证记录。
5. 验证：目标 GREEN、InnerBrain 专项、相邻回归、全量 `unittest`、桌面 smoke、安装包构建和打包后 exe smoke。
6. 收尾：静态检查、Markdown 链接检查、敏感扫描、本地配置跟踪检查、提交并 push。

## 验收

- `/inner-brain-eval` 输出 `InnerBrain 评估`、`seed_evaluation`、通过数、失败数、准确率和逐条样例。
- 固定评估集当前失败数为 0。
- 全量 `unittest` 524 项通过。
- 安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.29.0.exe` 生成并通过 smoke。
