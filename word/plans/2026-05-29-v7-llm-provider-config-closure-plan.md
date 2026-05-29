# Jarvis Lite v7：外脑 Provider 配置闭环方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v5 搜索互补方案和 v6 InnerBrain 样本分类器优先方案，明确 `0.3.0` 的外脑 provider 配置闭环。

## 核心结论

`0.3.0` 的主线是让外脑 LLM 的真实配置更贴近用户直觉：

```text
llm.local.json provider=qwen/gemini
  -> LLMSettings 保留原始 provider
  -> adapter_provider=openai-compatible
  -> OpenAIResponsesProvider
  -> JarvisAgent 白名单执行 command intent
```

这不是新增厂商 SDK，也不是让 LLM 绕过 Agent。`qwen` 和 `gemini` 先作为 provider alias 复用现有 OpenAI-compatible adapter；`base_url`、`model` 和 API key 仍由用户按具体平台控制台填写。

## 设计边界

- LLM 外脑仍只返回 `command`、`answer`、`clarify` 或 `no_action`。
- `command` 仍必须命中 Jarvis Lite 命令白名单，再由 `JarvisAgent` 执行。
- 真实 `config/llm.local.json` 不进入 Git；模板只保留占位符。
- 联网搜索仍由 SearchRouter 明确调用，LLM 不自由浏览网页。
- 本阶段不引入 Gemini/Qwen 原生 SDK；除非后续兼容端点无法满足需求，再单独设计原生 adapter。

## 0.3.0 收口内容

- `provider=qwen` 和 `provider=gemini` 可直接写入 `llm.local.json` 或环境变量。
- `/llm-status` 与 `/llm-enable` 同时展示 `Provider` 和实际 `Adapter`。
- `qwen`/`gemini` 复用 OpenAI-compatible 的 `model`、`api_key`、`base_url` 配置校验。
- `/llm-config-example qwen` 和 `/llm-config-example gemini` 直接输出对应 alias，而不是要求用户手动改回 `openai-compatible`。
- 版本提升到 `0.3.0`，生成可安装测试包。

## 后续方向

- 继续用真实日志沉淀 InnerBrain runtime 样本和回归测试。
- 评估 embedding 或小型分类器时，必须先准备可重复评估集。
- 搜索 provider 后续可继续扩展，但应优先使用官方 API 或 SDK，不接入非官方网页抓取。
- 真实 provider 的连接质量、额度限制和返回格式仍需通过 `/llm-smoke`、`/search-status` 和本地日志持续观察。
