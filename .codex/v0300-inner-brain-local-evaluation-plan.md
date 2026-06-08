# 2026-06-01 0.30.0 InnerBrain 本机评估集扩展计划

> 日期：2026-06-01
> 执行者：Codex

## 目标

让 `/inner-brain-eval` 在固定 seed 评估集之外，读取 `data/inner-brain/evaluation/*.jsonl` 本机评估样本。真实日志中确认应稳定支持的表达，可以先进入评估集观察，不直接成为训练样本。

## 约束

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳候选、不写入 `data/inner-brain/training/runtime.jsonl`。
- 本机评估样本只影响 `/inner-brain-eval` 输出，不改变正常聊天路由。
- 损坏 JSON、空文本、缺少 `expected_intent` 或非法 `expected_policy` 的行直接忽略。

## 实施步骤

1. RED：新增本机评估 JSONL 加载测试、Agent `/inner-brain-eval` 合并本机评估测试和版本一致性测试。
2. GREEN：扩展 `InnerBrainEvaluationCase`、新增 `load_evaluation_cases()`、合并 seed/local cases 并输出来源计数。
3. 文档：同步 README、PROJECT-PLAN、v34 方案、方案索引、今日进度和验证记录。
4. 验证：运行 InnerBrain 专项、相邻回归、全量 unittest、桌面 smoke、安装包构建、打包 exe smoke、静态/链接/敏感检查。
5. 发布：提交 `feat: 支持内脑本机评估样本 0.30.0` 并推送 `origin/main`。

## 验收

- `/inner-brain-eval` 在存在本机评估样本时显示 `评估集：seed_evaluation+local_evaluation`。
- 输出包含 `seed_evaluation` 和 `local_evaluation` 来源计数。
- 示例 JSONL `{"text":"请看看资料库状态","expected_intent":"knowledge.status","expected_command":"/kb"}` 可通过评估。
- 执行评估不会创建 runtime 训练样本。
- 0.30.0 安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.30.0.exe`。
