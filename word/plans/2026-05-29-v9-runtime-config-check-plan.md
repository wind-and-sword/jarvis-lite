# Jarvis Lite v9：运行态配置检查方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v8 运行态配置初始化方案，明确 `0.5.0` 的本地配置检查闭环。

## 核心结论

`0.5.0` 的主线是补齐配置草稿生成后的下一步：

```text
用户输入：检查外脑配置 / /llm-config-check
  -> JarvisAgent 重新读取本地配置和环境变量覆盖
  -> LLMRouter.describe()
  -> 输出 provider、adapter、model、base_url、SDK Base URL、API key 状态、配置问题
  -> 不发起网络请求，不执行 LLM fallback
```

联网搜索同理：

```text
用户输入：检查联网搜索配置 / /search-config-check
  -> 重新读取搜索配置
  -> SearchRouter.describe()
  -> 输出 provider、max_results、API key 状态、配置问题
  -> 不发起网络请求，不执行 /search
```

## 设计边界

- 检查命令只读配置，不创建、不覆盖、不修改 `local.json`。
- 不展示真实 API key，只显示“已配置/未配置”。
- 不调用真实 LLM provider，不调用真实搜索 provider。
- 不新增 Gemini/Qwen 原生 SDK；`qwen`/`gemini` 仍走 OpenAI-compatible adapter。
- 不扩大正则自然语言解析，只增加 InnerBrain seed 样本。

## 0.5.0 收口内容

- 新增 `/llm-config-check`，用于本地外脑配置检查。
- 新增 `/search-config-check`，用于本地联网搜索配置检查。
- InnerBrain seed 样本增加“检查外脑配置”“检查联网搜索配置”。
- 修复 LLM 本地配置 JSON 错误在 `provider=off` 状态下被吞掉的问题。
- README、项目方案、验证记录和版本同步到 `0.5.0`。

## 后续方向

- 如果用户真实测试显示仍难以填写配置，再增加交互式 `/llm-config-set` 或桌面配置表单。
- 真实 provider 连接失败时，继续增强 `/llm-smoke` 和 `/search` 的错误可读化。
- 继续把用户实际表达沉淀为 InnerBrain runtime/seed 样本。
