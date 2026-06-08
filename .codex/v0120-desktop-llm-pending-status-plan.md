# 0.12.0 桌面外脑 pending 固定状态计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

让桌面助手面板在不需要用户手动点击“最近上下文”的情况下，固定展示 LLM 外脑待补充问题、澄清轮次和取消提示。

## 实现约束

- 不新增自然语言正则模板。
- 不调用 `/recent-context` 做后台轮询，避免污染会话历史。
- 不改变 LLM provider adapter 和 InnerBrain missing 槽位逻辑。
- 优先复用 `JarvisAgent` 已有 pending 状态。

## 接口设计

- `JarvisAgent.llm_clarification_status_text()`：返回桌面可直接展示的只读状态文本。
- `DesktopBridge.llm_pending_status_text()`：代理读取当前 Agent 状态。
- `DesktopResponse.llm_pending_status_text`：每次发送后附带最新 pending 状态。
- `AssistantPanel` 新增固定 label，初始化和每次响应后刷新。

## TDD 验收

- Bridge 在 LLM 返回 `clarify` 后能暴露 `外脑待补充（1/3）` 状态。
- Panel 提交触发 LLM clarify 后固定状态区域显示问题；取消补充后刷新为无 pending。
- 新 DesktopBridge/AssistantPanel 启动时能展示 runtime 里恢复的 pending。
- 版本同步到 `0.12.0`。

## 风险

- 面板空间已经较紧，固定状态区需要使用短文本和 word wrap，避免挤压输入区。
- 状态快照必须只读，不能为了显示状态而写入会话历史。
