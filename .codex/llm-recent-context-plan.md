# LLM fallback 近期上下文增强计划

> 日期：2026-05-28
> 执行者：Codex

## 目标

让 LLM fallback 在本地无法处理用户输入时，收到更有用的近期上下文摘要，尤其是基于当前资料、目录、最近文件和经验建议生成的可执行下一步建议。

## 设计

- 不改变 `LLMRouter` / `LLMProvider` / `LLMIntent` 分层。
- 不新增真实网络调用，不依赖真实 API key。
- 在 `JarvisAgent._llm_context_lines()` 内复用已有 `suggest_next_actions_from_context()`。
- 将最多 3 条建议拼成一行：`下一步建议：...`。
- 继续保持本地优先：本地命令、身份、本地自然语言意图和知识库问答仍优先于 LLM。

## 验收

- 新增 Agent 测试先失败，证明 LLM provider 收到的 context 还没有下一步建议。
- GREEN 后测试通过，并确认 provider.calls 中包含 `下一步建议：继续处理最近资料...`。
- 回归 `tests.test_agent`、`tests.test_llm` 和全量 `unittest`。
- 更新 2026-05-28 进度和验证记录。
