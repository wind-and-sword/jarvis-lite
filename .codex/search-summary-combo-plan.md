# SearchRouter + LLMRouter 搜索总结组合计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

把联网搜索和 LLM 外脑按已确认方案串起来：InnerBrain 识别明确的“查一下并总结”，Agent 先调用 SearchRouter 获取当前网页来源，再把来源写入运行态上下文和 LLM context，最后由 LLMRouter 基于这些来源生成总结。

## 约束

- InnerBrain 主路径仍是样本分类器优先。
- 正则只用于抽取 `query` 等结构化槽位，不用作自然语言主意图判定。
- `/search` 只搜索和展示来源，不自动调用 LLM。
- `/search-summary` 和“联网查一下...并总结”才触发 SearchRouter + LLMRouter 组合流程。
- LLM 不自由浏览；它只接收 Agent 提供的搜索标题、URL、摘要和来源。
- 真实 `config/llm.local.json` 与 `config/search.local.json` 不进入 Git。

## 任务拆分

- [x] 为 InnerBrain 增加 `web.search_summarize` 样本、签名和 `query` 槽位抽取。
- [x] 为 Agent 增加 `/search-summary 关键词` 命令。
- [x] `/search` 成功后写入最近联网搜索上下文，并持久化到 runtime context。
- [x] `_llm_context_lines()` 注入最近联网搜索来源。
- [x] `/search-summary` 先搜索，再让 LLM 基于上下文总结。
- [x] LLM 未启用或未返回结果时保留搜索来源并提示 `/llm-status`、`/llm-enable`。
- [x] `/inner-brain-teach ... => /search-summary ...` 保存为 `web.search_summarize`，并通过 command slot 执行教学目标。
- [x] 更新 README、项目方案、v5/v6 方案、进度和验证文档。
- [x] 运行全量测试、桌面 smoke、命令 smoke、静态检查和敏感信息扫描。
- [x] 提交本阶段改动。

## 验收标准

- `联网查一下 Python 版本并总结` 识别为 `web.search_summarize`，命令为 `/search-summary Python 版本`。
- `/search Python 版本` 后，“查看最近上下文”和 `/llm-context-preview` 均能看到最近联网搜索来源。
- `/search-summary Python 版本` 展示搜索结果和 `LLM 外脑总结：...`。
- LLM 关闭时 `/search-summary` 不崩溃，仍展示搜索来源并提示启用 LLM。
- 教学 `/search-summary` 的 runtime 样本 intent 与 seed intent 保持一致。
