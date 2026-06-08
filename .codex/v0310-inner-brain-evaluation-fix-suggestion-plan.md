# 2026-06-01 0.31.0 InnerBrain 评估失败修复建议计划

> 日期：2026-06-01
> 执行者：Codex

## 目标

让 `/inner-brain-eval` 在存在失败样本时输出可复制的显式训练建议，帮助把评估失败转成下一步人工 teach/label 操作。评估命令仍然只观察，不自动训练。

## 约束

- 不新增自然语言意图正则。
- 不自动写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变正常聊天路由、最近路由历史或候选统计。
- 失败建议只是文本提示，最终训练必须由用户显式执行。

## 实施步骤

1. RED：新增 InnerBrain 失败评估建议测试、Agent `/inner-brain-eval` 失败建议测试和版本一致性测试。
2. GREEN：扩展评估报告失败结果视图，格式化显式训练建议，版本提升到 `0.31.0`。
3. 文档：同步 README、PROJECT-PLAN、v35 方案、方案索引、今日进度和验证记录。
4. 验证：运行 InnerBrain 专项、相邻回归、全量 unittest、桌面 smoke、安装包构建、打包 exe smoke、静态/链接/敏感检查。
5. 发布：提交 `feat: 增加内脑评估失败修复建议 0.31.0` 并推送 `origin/main`。

## 验收

- 失败评估输出包含 `失败修复建议：`。
- 带 `expected_command` 的失败样本输出 `/inner-brain-teach 文本 => /命令`。
- Agent `/inner-brain-eval` 输出相同建议。
- 执行评估不会创建 runtime 训练样本。
- 0.31.0 安装包生成到 `E:\oyzj\ai\jarvis-lite-dist\JarvisLiteSetup-0.31.0.exe`。
