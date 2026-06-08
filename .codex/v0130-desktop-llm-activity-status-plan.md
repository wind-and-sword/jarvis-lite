# 0.13.0 桌面外脑运行状态与最近调用结果计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

在 0.12.0 的“待补充状态”之外，新增只读“外脑运行状态”：

- 展示外脑是否启用、provider、model 和配置问题数量。
- 展示最近一次真实 LLM 调用的触发来源、返回类型、输入摘要和结果摘要。
- 状态进入 RuntimeContext，桌面重启后可恢复。
- 桌面 Bridge 和 Panel 固定展示该状态，不调用 `/llm-status` 污染历史。

## 边界

- 不新增自然语言正则模板。
- 不把 API key 或完整敏感配置写入运行态上下文。
- 不改变 provider adapter 的调用协议。
- 不自动轮询外脑状态，只在启动和发送后刷新。

## 执行步骤

1. RED：新增 Agent、DesktopBridge、AssistantPanel 和版本一致性测试。
2. GREEN：扩展 RuntimeContext，新增最近 LLM 调用快照。
3. GREEN：Agent 在 LLM fallback、smoke、搜索总结/比较、澄清补充等路径记录最近调用，并暴露 `llm_activity_status_text()`。
4. GREEN：DesktopResponse/Bridge/Panel 透传并展示 `llm_activity_status_text`。
5. 文档：同步 README、PROJECT-PLAN、方案索引、进度和验证记录到 `0.13.0`。
6. 验证：目标测试、邻近回归、全量 unittest、桌面 smoke、打包、安装脚本版本、静态检查、Markdown 链接、敏感扫描。
