# Web Search Router Implementation Plan

> 日期：2026-05-28
> 执行者：Codex

## Goal

把“联网搜索”作为 JarvisAgent 控制的工具能力接入当前双脑架构：InnerBrain 负责识别用户是不是要查网上信息，SearchRouter 负责调用搜索 provider，LLM 外脑后续可基于搜索结果做总结和表达增强。

## Design

- 新增 `src/jarvis_lite/search.py`，职责与 `llm.py` 对齐：
  - `SearchSettings.from_sources(paths, env)` 读取 `config/search.local.json`，环境变量覆盖。
  - `SearchRouter.search(query)` 在 provider=off 时不调用网络。
  - `FakeSearchProvider` 用 JSON 配置返回固定结果，覆盖本地测试。
  - `TavilySearchProvider` 通过官方 Python SDK 接入真实联网搜索，SDK 缺失或配置不完整时返回可读错误。
- `JarvisAgent` 新增：
  - 构造参数 `search_router`，测试可注入。
  - `/search-status`、`/search-config-example`、`/search-enable`、`/search 关键词`。
  - 搜索结果格式化为编号、标题、URL、摘要，日志记录查询，不打印 API key。
  - InnerBrain seed 样本把“联网查一下 Python 版本”“搜索一下...”映射到 `/search ...`。
- 文档：
  - `config/search.example.json` 作为模板。
  - `.gitignore` 忽略真实 `search.local.json`。
  - README、`word/PROJECT-PLAN.md`、v4 方案、当日进度、验证记录同步说明。

## TDD Tasks

1. RED：新增 `tests/test_search.py`，覆盖默认 off、本地配置、环境变量覆盖、fake provider、状态不泄露 key、Tavily SDK 缺失。
2. GREEN：实现 `search.py` 最小行为。
3. RED：新增 Agent 测试，覆盖 `/search-status`、`/search` fake 结果、自然语言搜索入口、运行中 `/search-enable` 重载。
4. GREEN：接入 Agent 和 InnerBrain。
5. 文档和验证：更新正式文档，运行专项、全量、smoke、diff、链接和敏感信息扫描。

## Acceptance

- 未配置时不会触发网络请求。
- fake provider 可完全本地验证搜索链路。
- 状态和错误文本不包含真实 API key。
- 搜索结果带来源 URL，后续可供 LLM 总结。
- LLM 不直接“自由浏览”，工具调用仍由 Agent 控制。
