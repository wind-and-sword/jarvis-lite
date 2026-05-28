# Jarvis Lite v5：Agent 联网搜索与 LLM 外脑互补方案

> 日期：2026-05-28
> 执行者：Codex
> 说明：本文承接 v4 双脑架构，明确联网搜索不是替代 LLM，也不是让 LLM 自由浏览，而是作为 JarvisAgent 可控工具能力接入。

## 1. 核心判断

联网搜索和 LLM 外脑是互补关系，不是二选一。

- 搜索负责拿到当前互联网上的来源、标题、摘要和 URL。
- LLM 负责在有来源的前提下做总结、比较、解释和自然表达。
- JarvisAgent 负责决定何时搜索、调用哪个 provider、如何展示来源，以及是否把结果交给 LLM 继续处理。

这能避免两个问题：一是只靠 LLM 容易把过期知识当成事实；二是让 LLM 自由浏览会让工具调用、来源展示和成本不可控。

## 2. 架构位置

```text
用户输入
  -> 命令 / InnerBrain / 本地知识库优先
  -> SearchRouter（需要联网资料时由 Agent 显式调用）
     -> SearchProvider：off / fake / tavily / 后续 provider
     -> SearchResult：title / url / snippet / source
  -> JarvisAgent 展示来源、写入上下文
  -> 可选：LLMRouter 基于搜索结果总结、比较或追问
```

SearchRouter 与 LLMRouter 平级，都是 Agent 控制的外部能力。不同点是：SearchRouter 返回事实来源列表，LLMRouter 返回结构化意图或自然语言总结。

## 3. 第一版范围

第一版先做可配置、可测试、可观察的联网搜索入口：

- `/search-status`：查看搜索 provider、配置来源、API key 是否配置、是否会触发网络调用。
- `/search-config-example`：输出配置模板。
- `/search-enable`：创建运行态模板并重新加载当前会话的 SearchRouter。
- `/search 关键词`：执行搜索并返回编号结果、标题、URL 和摘要。
- 自然语言入口：例如“联网查一下 Python 版本”“搜索一下 Jarvis Lite”映射到 `/search ...`。

第一版不把所有搜索结果自动交给 LLM 总结。先把来源展示和工具链路做稳，后续再增加 `/search-summarize` 或“查一下并总结”这类组合能力。

## 4. 配置约定

沿用 LLM 外脑配置约定：

```text
config/search.example.json   可提交模板
config/search.local.json     本地真实配置，忽略 Git
```

配置字段：

```json
{
  "provider": "tavily",
  "api_key": "<你的搜索 API key>",
  "base_url": "",
  "max_results": 5,
  "fake_results": []
}
```

环境变量可覆盖本地配置，便于临时调试：

```powershell
$env:JARVIS_LITE_SEARCH_PROVIDER = "tavily"
$env:JARVIS_LITE_SEARCH_API_KEY = "..."
$env:JARVIS_LITE_SEARCH_BASE_URL = ""
$env:JARVIS_LITE_SEARCH_MAX_RESULTS = "5"
```

## 5. 边界原则

- 未配置 provider 时不触发网络请求。
- 状态、日志和回复不输出 API key。
- 搜索结果必须展示 URL，不能只给无来源结论。
- LLM 可以总结搜索结果，但不能伪造来源，也不能绕过 Agent 直接执行搜索。
- 本地知识库和用户记忆仍优先；联网搜索主要处理当前性强、资料库没有覆盖的问题。

## 6. 后续方向

- 增加“搜索后交给 LLM 总结”的组合命令。
- 将最近联网搜索结果写入运行态上下文，供后续追问使用。
- 支持更多搜索 provider，例如 Brave Search、SerpAPI 或自建搜索网关。
- 根据用户真实日志，把“查网上”“搜一下”“帮我看看现在网上怎么说”等表达沉淀为 InnerBrain 样本。
