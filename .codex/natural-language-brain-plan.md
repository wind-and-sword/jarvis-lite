# Jarvis Lite 自然语言本地大脑执行计划

> 日期：2026-05-21
> 执行者：Codex

## 目标

新增自然语言意图层第一版，让用户无需斜杠命令也能触发常见本地能力，并为后续语音和大模型接入打基础。

## 文件范围

- 新增 `src/jarvis_lite/intent.py`：自然语言意图解析，只负责把文本归类为内部动作。
- 修改 `src/jarvis_lite/agent.py`：在身份问句和资料问答前接入意图路由，新增能力摘要和直接目录打开记录。
- 修改 `src/jarvis_lite/memory.py`：避免疑问句被 `我是...` 误写入身份记忆，扩展身份问句识别。
- 新增或修改测试：
  - `tests/test_memory.py`
  - `tests/test_agent.py`
  - `tests/test_voice.py` 或沿用 `tests/test_agent.py` 覆盖语音复用。
- 更新文档：
  - `README.md`
  - `word/jarvis-lite-overall-plan.md`
  - `word/文档索引.md`
  - 新增 `word/2026-05-21-jarvis-lite-natural-language-brain-progress.md`
  - `verification.md`
  - `.codex/testing.md`
  - `.codex/operations-log.md`

## TDD 步骤

1. 写 `tests/test_memory.py` RED：
   - `parse_identity_fact("我是你的什么人，你知道吗")` 返回空。
   - `is_identity_question("我是你的什么人，你知道吗")` 返回真。
2. 写 `tests/test_agent.py` RED：
   - 先记住姓名，再问 `我是你的什么人，你知道吗`，返回身份，不污染 `用户身份`。
   - `你现在能做什么事` 返回能力摘要。
   - `生成日报` 生成日报。
   - `查看知识库` 返回 `/kb` 等价内容。
   - `检查更新` 返回更新状态。
   - `打开D盘` 记录打开 `D:\` 请求。
3. 运行 RED，确认失败原因来自缺失行为。
4. 新增 `intent.py`，实现最小规则解析。
5. 修改 `memory.py` 和 `agent.py`，接入意图层。
6. 运行专项测试，确认 GREEN。
7. 更新正式文档和验证记录。
8. 运行全量测试、桌面 smoke、`git diff --check`。
9. 提交本地改动，不自动 push。
