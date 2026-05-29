# Jarvis Lite v11：连通性诊断方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v10 运行态配置写入方案，明确 `0.7.0` 的 provider 连通性诊断闭环。

## 核心结论

`0.7.0` 的主线是补齐配置写入后的下一步：

```text
用户输入：/llm-smoke 请用一句话确认连接可用
  -> JarvisAgent 重新读取当前 llm.local.json
  -> LLMRouter 执行一次结构化意图调用
  -> 只展示 type、回答/澄清/命令建议和失败原因
  -> smoke 不执行模型建议命令
```

联网搜索同理：

```text
用户输入：/search-smoke Python 版本
  -> JarvisAgent 重新读取当前 search.local.json
  -> SearchRouter 执行一次 provider 搜索
  -> 展示成功条数和来源预览，或展示 provider 错误
  -> 不写入最近联网搜索上下文
```

## 设计边界

- `/llm-smoke` 和 `/search-smoke` 都是主动测试命令，可能触发真实 provider 调用。
- Search smoke 不替代 `/search`，不保存最近搜索结果，不触发 LLM 总结。
- 不新增厂商 SDK；`qwen`/`gemini` 仍走 OpenAI-compatible adapter。
- 不从自然语言中猜测配置值；自然语言只负责进入 smoke 命令。
- 输出继续隐藏真实 API key。

## 0.7.0 收口内容

- 增强 `/llm-smoke [prompt]`，运行时重新读取当前本地配置。
- 新增 `/search-smoke [query]`，默认查询 `Python 版本`。
- InnerBrain seed 样本增加“测试外脑连接”“测试联网搜索连接”。
- README、项目方案、验证记录和版本同步到 `0.7.0`。

## 后续方向

- 如果真实 LLM smoke 经常返回非结构化结果，再增强提示词和解析错误解释。
- 如果用户仍觉得命令行配置复杂，再做桌面配置表单。
- 继续根据真实日志沉淀 InnerBrain 样本，并把开放表达交给外脑 LLM。
