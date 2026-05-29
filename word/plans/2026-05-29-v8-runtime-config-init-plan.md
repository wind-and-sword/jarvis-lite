# Jarvis Lite v8：运行态配置初始化方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v7 外脑 provider 配置闭环，明确 `0.4.0` 的运行态配置初始化闭环。

## 核心结论

`0.4.0` 的主线不是新增厂商 SDK，也不是扩大正则匹配，而是把安装后的外脑与联网搜索配置路径变成可执行闭环：

```text
用户输入：生成外脑配置 / /llm-config-init qwen
  -> InnerBrain 或命令入口
  -> JarvisAgent
  -> 生成 config/llm.local.json 草稿
  -> 用户填入 model/base_url/api_key
  -> /llm-enable 重新加载并诊断
```

联网搜索同理：

```text
用户输入：生成联网搜索配置 / /search-config-init tavily
  -> 生成 config/search.local.json 草稿
  -> 用户填入 api_key
  -> /search-enable 重新加载并诊断
```

## 设计边界

- 只生成本地运行态配置草稿，不提交真实 `llm.local.json` 或 `search.local.json`。
- 草稿中的 key、model、base_url 默认空值，避免误判为已配置或误触发网络调用。
- 已存在本地配置时不覆盖，也不打印已有 API key。
- `qwen`/`gemini` 仍是 provider alias，实际走 OpenAI-compatible adapter。
- 搜索仍由 SearchRouter 显式执行，不让 LLM 自由联网。

## 0.4.0 收口内容

- 新增 `/llm-config-init [provider]`，默认生成 `openai-compatible` 草稿，支持现有 LLM provider。
- 新增 `/search-config-init [provider]`，默认生成 `tavily` 草稿，支持现有搜索 provider。
- Help、README、项目方案和验证记录同步配置初始化入口。
- InnerBrain seed 样本增加“生成外脑配置”“创建外脑配置文件”“生成联网搜索配置”“创建搜索配置文件”。
- 版本提升到 `0.4.0`，生成可安装测试包。

## 后续方向

- 若用户真实配置日志显示仍容易填错，再增加只做本地校验、不发起网络调用的配置检查明细。
- 继续沉淀自然语言缺口为 InnerBrain runtime/seed 样本。
- 在拥有稳定评估集后，再评估 embedding 或小型分类器。
