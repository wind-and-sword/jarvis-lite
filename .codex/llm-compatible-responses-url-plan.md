# LLM 兼容端点完整 Responses URL 计划

> 日期：2026-05-27
> 执行者：Codex

## 目标

让 `openai-compatible` provider 的 `JARVIS_LITE_LLM_BASE_URL` 同时接受 SDK base URL 和用户从 Postman 复制的完整 `/v1/responses` URL，并保持 key、URL、model 全部可配置。

## 实施步骤

1. 补充 RED 测试，覆盖完整 `/v1/responses` URL 归一化、`/llm-status` 展示 SDK Base URL、配置模板提示。
2. 在 `LLMSettings` 增加 SDK base URL 派生方法，运行时调用 SDK 前归一化。
3. 在 Router 状态输出中保留用户原始 Base URL，并在归一化发生时展示 SDK Base URL。
4. 更新 `/llm-config-example openai-compatible` 模板和正式文档。
5. 运行专项测试、模块测试、全量测试、桌面 smoke、Markdown 链接检查和 diff 检查。

## 验收标准

- 真实 key 和具体 endpoint 不进入仓库文件。
- `https://example/v1/responses` 形式的配置传给 SDK 时变为 `https://example/v1`。
- 原本配置到 `/v1` 的兼容端点不受影响。
- 文档明确说明两种 base URL 写法。
- 本地验证通过并记录到 `verification/2026-05/2026-05-27.md`。
