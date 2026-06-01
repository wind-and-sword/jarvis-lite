# Jarvis Lite v36：InnerBrain 评估失败过滤视图方案

> 日期：2026-06-01
> 执行者：Codex
> 说明：本文承接 v35 评估失败修复建议，明确 `0.32.0` 的失败样本过滤视图。

## 目标

`0.32.0` 为 InnerBrain 评估增加只看失败样本的入口。完整评估仍由 `/inner-brain-eval` 展示，排查大量本机 JSONL 样本时可用 `/inner-brain-eval-failed` 聚焦失败样例和显式修复建议。

## 边界

- 不新增自然语言意图正则。
- 不改变 seed/runtime 样本分类器评分。
- 不自动写入 `data/inner-brain/training/runtime.jsonl`。
- 不改变正常聊天路由、候选统计或 LLM fallback。
- 失败过滤只是评估报告展示视图，训练仍必须由用户显式执行 `/inner-brain-teach` 或 `/inner-brain-label`。

## 实现要点

- `describe_inner_brain_evaluation(report, failures_only=True)` 只格式化 `failed_case_results`。
- 失败过滤视图使用 `失败样例：` 标题，保留评估摘要、来源计数和“失败修复建议”。
- 无失败样本时显示 `- 无`，避免用户误以为命令无输出。
- Agent 新增 `/inner-brain-eval-failed`，并提供 `brain-eval-failed` 与 `inner-brain-eval-failures` 别名。
- 新入口作为路由观察命令处理，不写入最近路由训练候选。

## 验证

- RED：新增 InnerBrain 失败过滤描述测试、Agent `/inner-brain-eval-failed` 命令测试和版本一致性测试先失败。
- GREEN：目标测试通过。
- 回归：InnerBrain 专项、Agent/LLM/桌面/Conversation 相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建和打包后 exe smoke。

## 后续

- 继续把真实日志中确认稳定的表达加入本机评估 JSONL。
- 如果失败样本继续增多，再评估导出评估报告或按来源过滤，但仍保持显式训练和本地评估优先。
