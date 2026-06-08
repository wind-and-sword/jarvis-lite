# 0.51.0 InnerBrain 本机 evaluation 已处理样本只读清单计划

> 日期：2026-06-02
> 执行者：Codex

## 目标

新增 `/inner-brain-eval-local-resolved [文件名]`，只读列出当前已经通过的本机 evaluation 样本，帮助用户区分失败建议里哪些样本已经通过训练或 seed/runtime 补强被处理。命令支持省略文件名查看全部本机样本，也支持按 JSONL 文件聚焦。

## 约束

- 只读执行 `evaluate_inner_brain(..., source_filter="local_evaluation")`。
- 不写 `data/inner-brain/training/runtime.jsonl`。
- 不自动采纳、不自动训练、不修改 `data/inner-brain/evaluation/*.jsonl`。
- 不新增自然语言意图正则，不改变 LLM fallback、联网搜索和正常聊天路由。

## 执行步骤

1. RED：新增 InnerBrain 已处理描述测试，断言只展示 PASS 本机样本，失败样本不出现在 `已处理样例：`。
2. RED：新增 Agent `/inner-brain-eval-local-resolved [文件名]` 测试，断言命令可用、支持文件过滤、没有样本时显示 `- 无`，且不写 training runtime。
3. RED：版本一致性测试期望 `0.51.0`，更新检测 fixture 期望 `0.51.1`。
4. GREEN：在 `InnerBrainEvaluationReport` 增加通过样本筛选，并新增已处理样本描述函数。
5. GREEN：Agent 命令分发、help 和命令识别白名单接入 `/inner-brain-eval-local-resolved`。
6. 文档：同步 README、PROJECT-PLAN、plans README、文档索引、进度和验证记录。
7. 验证：目标测试、InnerBrain+Agent 相邻回归、全量 unittest、桌面 smoke、安装包构建、打包后 exe smoke、静态和文档链接检查。
8. 提交：本地提交 `feat: 增加本机评估已处理样本清单 0.51.0`。
