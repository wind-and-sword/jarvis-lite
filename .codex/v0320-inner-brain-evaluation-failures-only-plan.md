# 0.32.0 InnerBrain 评估失败过滤视图计划

> 日期：2026-06-01
> 执行者：Codex

## 目标

让 `/inner-brain-eval-failed` 复用现有 InnerBrain 评估集，只输出失败样本和显式修复建议，便于排查本机 JSONL 评估集中真实失败项。

## 约束

- 不新增自然语言意图正则。
- 不自动训练、不自动采纳、不写入 runtime 样本。
- 不改变正常聊天路由、候选统计或 LLM fallback。
- 保持评估输出和训练动作分离。

## 步骤

1. RED：新增失败过滤描述测试、Agent 命令测试和版本一致性测试。
2. GREEN：扩展 `describe_inner_brain_evaluation()` 的 `failures_only` 参数，并在 Agent 中接入 `/inner-brain-eval-failed`。
3. 回归：运行 InnerBrain 专项、相邻回归、全量 unittest、桌面 smoke。
4. 打包：构建 Windows 安装包并复制为 `JarvisLiteSetup-0.32.0.exe`。
5. 文档：同步 README、PROJECT-PLAN、v36 方案、进度和验证记录。
6. 收尾：运行 diff、Markdown 链接、敏感信息和本地配置跟踪检查，提交并推送。

## 验收

- 失败过滤视图不显示通过样本。
- 失败过滤视图仍展示失败修复建议。
- 无失败样本时可读输出 `- 无`。
- 全量本地验证通过，安装脚本和安装完成弹窗均显示 `0.32.0`。
