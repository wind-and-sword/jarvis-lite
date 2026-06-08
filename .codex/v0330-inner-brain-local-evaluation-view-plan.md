# 0.33.0 InnerBrain 本机评估过滤视图计划

> 日期：2026-06-01
> 执行者：Codex

## 目标

新增本机评估视图，让 `data/inner-brain/evaluation/*.jsonl` 的真实日志样本可以单独评估和只看失败项。

## 约束

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 runtime 样本。
- 不改变正常聊天路由、候选统计或 LLM fallback。
- 保持 seed 基线、local 本机样本和训练动作可区分。

## 步骤

1. RED：新增 source filter 评估 API 测试、Agent `/inner-brain-eval-local` 和 `/inner-brain-eval-local-failed` 测试、版本一致性测试。
2. GREEN：扩展 `evaluate_inner_brain()` 的 source filter，并在 Agent 中接入本机评估命令。
3. 回归：运行 InnerBrain 专项、相邻回归、全量 unittest、桌面 smoke。
4. 打包：构建 Windows 安装包并复制为 `JarvisLiteSetup-0.33.0.exe`。
5. 文档：同步 README、PROJECT-PLAN、v37 方案、进度和验证记录。
6. 收尾：运行 diff、Markdown 链接、敏感信息和本地配置跟踪检查，提交并推送。

## 验收

- `/inner-brain-eval-local` 只展示 `local_evaluation` 样本，不展示 seed 样本。
- `/inner-brain-eval-local-failed` 只展示本机失败样本和修复建议。
- 本机评估命令不创建 `data/inner-brain/training/runtime.jsonl`。
- 全量本地验证通过，安装脚本和安装完成弹窗均显示 `0.33.0`。
