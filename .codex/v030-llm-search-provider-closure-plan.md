# 0.3.0 外脑 Provider 配置闭环 v1 计划

> 日期：2026-05-29
> 执行者：Codex

## 里程碑定义

`0.3.0` 定义为：外脑 provider 配置闭环 v1。

本阶段的目标不是新增一堆厂商 SDK，而是让安装后的真实配置更顺：用户可以把常见 provider alias（先覆盖 `qwen`、`gemini`）直接写入 `llm.local.json`，Jarvis Lite 会用现有 OpenAI-compatible adapter 执行，并在 `/llm-status`、`/llm-enable` 和配置模板里说明“原始 provider”和“实际 adapter”。

## 推荐方案

选择“provider alias -> OpenAI-compatible adapter”作为 0.3.0 的主线。

理由：

- 复用已有 OpenAI Responses/OpenAI-compatible adapter，不新增并行执行层。
- `qwen`/`gemini` 的兼容端点、模型名和 base_url 可能随平台变化，项目只保存占位模板，不硬编码真实 URL。
- 用户已明确可以配置 URL 和 API key；本轮让配置字段更贴近用户直觉。
- 真实联网搜索继续使用 SearchRouter，暂不新增 Google/Baidu 抓取或非官方搜索实现。

## 收口范围

- `provider=qwen` 和 `provider=gemini` 在 `LLMSettings` 中保留原始 provider，同时解析出实际 adapter：`openai-compatible`。
- `build_llm_router()` 使用实际 adapter 构建 `OpenAIResponsesProvider`。
- `LLMSettings.configuration_issues()` 对 alias 复用 OpenAI-compatible 的 `model/api_key/base_url` 校验。
- `LLMRouter.describe()` 显示原始 provider 和实际 adapter，避免用户以为 alias 未生效。
- `/llm-config-example qwen` 和 `/llm-config-example gemini` 输出可直接写入 local config 的 provider alias 示例。
- README、当前方案、进度和验证记录同步 `0.3.0`。

## 执行规则

- 先写 RED 测试，再改实现。
- 不提交 `config/llm.local.json`、`config/search.local.json` 或真实密钥。
- 不让 LLM 直接自由执行命令；仍由 `JarvisAgent` 校验白名单并执行。
- 不让 LLM 自由浏览网页；联网搜索仍由 SearchRouter 明确触发。
- 产物为 `JarvisLiteSetup-0.3.0.exe`。

## 任务拆分

1. 新增 LLM alias 失败测试：`qwen`/`gemini` 配置可被识别、校验和构建到 OpenAI-compatible adapter。
2. 新增 Agent reload 失败测试：`/llm-enable` 读取 `provider=qwen` 的本地配置后显示 provider 与 adapter。
3. 实现 provider alias 解析和状态展示。
4. 更新配置模板、README 和正式方案文档。
5. 升级版本到 `0.3.0`。
6. 全量验证、打包、提交并 push。
