# 0.28.0 InnerBrain 样本包含签名置信度补偿计划

> 日期：2026-06-01
> 执行者：Codex

## 目标

让 InnerBrain 在用户长句完整包含已知样本签名时，可以通过样本分类器直接达到高置信执行。例如 `帮我看一下知识库状态` 应识别为 `knowledge.status` 并执行 `/kb`。

## 约束

- 不新增自然语言意图正则。
- 不降低全局阈值。
- 不改变 seed/runtime 样本数据格式。
- 不自动训练或自动采纳候选。
- 过短样本不参与包含补偿，降低误吞风险。

## 步骤

1. RED：新增 `test_sample_classifier_boosts_contained_sample_signature` 和版本一致性断言，确认当前行为只到澄清且版本未提升。
2. 实现：在 `_sample_similarity()` 中保留 Dice 相似度，并新增包含签名补偿函数，最终取最大值。
3. GREEN：目标测试通过，InnerBrain 专项通过。
4. 回归：执行相邻模块和全量 `unittest`。
5. 打包：执行源码桌面 smoke、Windows 安装包构建、版本化复制、打包后 exe smoke、安装脚本文案检查。
6. 文档：同步 README、PROJECT-PLAN、方案索引、进度和验证记录。
7. 收尾：静态检查、Markdown 链接检查、敏感信息扫描、本地配置跟踪检查、提交并 push。

## 验收

- `帮我看一下知识库状态` 返回 `knowledge.status`、`EXECUTE`、`seed_sample`，置信度不低于 `HIGH_CONFIDENCE`，命令为 `/kb`。
- 全量 `unittest` 522 项通过。
- 安装包 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.28.0.exe` 生成并通过 smoke。
