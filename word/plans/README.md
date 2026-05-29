# Jarvis Lite 方案版本索引

> 日期：2026-05-29
> 执行者：Codex

## 当前方案

- [../PROJECT-PLAN.md](../PROJECT-PLAN.md)：当前项目方案入口。
- [2026-05-29-v21-route-history-detail-plan.md](2026-05-29-v21-route-history-detail-plan.md)：当前方案版本，明确路由历史详情与最近上下文集成。

## 历史版本

- [2026-05-18-v1-overall-plan.md](2026-05-18-v1-overall-plan.md)：本地个人助手起点，定义命令行、记忆、知识库、语音和桌面自动化的初始路线。
- [2026-05-22-v2-personal-device-agent-plan.md](2026-05-22-v2-personal-device-agent-plan.md)：个人设备级 Agent 设想，将电脑、手机和手表纳入长期路线。
- [2026-05-27-v3-pc-agent-llm-first-plan.md](2026-05-27-v3-pc-agent-llm-first-plan.md)：明确当前优先级为 PC Agent -> LLM 外脑 -> 多端入口。
- [2026-05-28-v4-inner-brain-llm-dual-brain-plan.md](2026-05-28-v4-inner-brain-llm-dual-brain-plan.md)：明确 InnerBrain 本地内脑与 LLM 外脑的分工。
- [2026-05-28-v5-agent-web-search-llm-complement-plan.md](2026-05-28-v5-agent-web-search-llm-complement-plan.md)：明确 Agent 控制的联网搜索与 LLM 外脑互补关系。
- [2026-05-28-v6-inner-brain-classifier-first-plan.md](2026-05-28-v6-inner-brain-classifier-first-plan.md)：明确 InnerBrain 样本分类器优先、legacy fallback 仅迁移期兼容，并记录多轮澄清状态第一版。
- [2026-05-29-v7-llm-provider-config-closure-plan.md](2026-05-29-v7-llm-provider-config-closure-plan.md)：明确外脑 provider alias 与 OpenAI-compatible adapter 的配置闭环。
- [2026-05-29-v8-runtime-config-init-plan.md](2026-05-29-v8-runtime-config-init-plan.md)：明确外脑与联网搜索的运行态配置初始化闭环。
- [2026-05-29-v9-runtime-config-check-plan.md](2026-05-29-v9-runtime-config-check-plan.md)：明确外脑与联网搜索的运行态配置只读检查闭环。
- [2026-05-29-v10-runtime-config-set-plan.md](2026-05-29-v10-runtime-config-set-plan.md)：明确外脑与联网搜索的运行态配置写入闭环。
- [2026-05-29-v11-smoke-diagnostics-plan.md](2026-05-29-v11-smoke-diagnostics-plan.md)：明确外脑与联网搜索的 provider 连通性诊断闭环。
- [2026-05-29-v12-desktop-config-panel-plan.md](2026-05-29-v12-desktop-config-panel-plan.md)：明确桌面端外脑与联网搜索配置面板闭环。
- [2026-05-29-v13-llm-clarification-plan.md](2026-05-29-v13-llm-clarification-plan.md)：明确 LLM 外脑多轮澄清续聊闭环。
- [2026-05-29-v14-llm-clarification-runtime-plan.md](2026-05-29-v14-llm-clarification-runtime-plan.md)：明确 LLM 外脑澄清状态运行态恢复闭环。
- [2026-05-29-v15-llm-clarification-guard-plan.md](2026-05-29-v15-llm-clarification-guard-plan.md)：明确 LLM 外脑澄清轮数与过期策略。
- [2026-05-29-v16-desktop-llm-pending-status-plan.md](2026-05-29-v16-desktop-llm-pending-status-plan.md)：明确桌面外脑待补充状态固定展示。
- [2026-05-29-v17-desktop-llm-activity-status-plan.md](2026-05-29-v17-desktop-llm-activity-status-plan.md)：明确桌面外脑运行状态和最近调用结果固定展示。
- [2026-05-29-v18-route-decision-status-plan.md](2026-05-29-v18-route-decision-status-plan.md)：明确最近路由决策状态固定展示。
- [2026-05-29-v19-route-decision-explanation-plan.md](2026-05-29-v19-route-decision-explanation-plan.md)：明确最近路由决策解释详情固定展示。
- [2026-05-29-v20-route-history-plan.md](2026-05-29-v20-route-history-plan.md)：明确最近 5 条路由历史固定展示。

## 维护规则

- 当前方案始终写入 `word/PROJECT-PLAN.md`。
- 重大路线调整时新增一个版本文件。
- 历史版本不覆盖，用于追溯项目路线变化。
