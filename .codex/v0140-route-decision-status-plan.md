# 0.14.0 最近路由决策状态计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

新增只读“最近路由决策”状态，解释最近一条输入由哪一层处理：

- `command`：显式命令。
- `inner-brain`：InnerBrain 高置信度命中并执行。
- `inner-brain-clarify`：InnerBrain 需要补槽澄清。
- `knowledge`：本地知识库问答命中。
- `llm-fallback`：进入 LLM 外脑 fallback。
- `memory-fallback`：最终长期记忆兜底回复。

## 边界

- 不新增自然语言正则模板。
- 不改变 InnerBrain、SearchRouter 或 LLMRouter 的决策逻辑。
- 不调用历史/上下文命令生成状态，避免污染 transcript。
- 只记录最近一条路由决策，不做完整路由历史。

## 执行步骤

1. RED：新增 Agent、DesktopBridge、AssistantPanel 和版本一致性测试。
2. GREEN：扩展 RuntimeContext，新增最近路由决策快照。
3. GREEN：Agent 在关键处理路径记录路由状态，并暴露 `route_status_text()`。
4. GREEN：DesktopResponse/Bridge/Panel 透传并展示 `route_status_text`。
5. 文档：同步 README、PROJECT-PLAN、方案索引、进度和验证记录到 `0.14.0`。
6. 验证：目标测试、邻近回归、全量 unittest、桌面 smoke、打包、安装脚本版本、静态检查、Markdown 链接、敏感扫描。
