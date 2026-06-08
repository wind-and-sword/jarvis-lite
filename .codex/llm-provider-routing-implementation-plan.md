# LLM Provider Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 Jarvis Lite 增加可切换的 LLM 外脑层，第一版支持通用 provider 架构、fake provider 测试路径和 OpenAI adapter。

**Architecture:** `JarvisAgent` 只依赖 provider-neutral 的 `LLMRouter` 和 `LLMIntent`。本地命令、身份、本地自然语言和知识库问答仍优先处理；只有本地无法处理时才调用 LLM。真实 provider 细节放入 adapter，测试默认使用 fake provider。

**Tech Stack:** Python 3.13、标准库 `unittest`、可选 OpenAI Python SDK。

---

### Task 1: LLM 核心接口和 fake provider

**Files:**
- Create: `src/jarvis_lite/llm.py`
- Test: `tests/test_llm.py`

- [ ] 写失败测试：解析 `off`、`fake` 配置。
- [ ] 写失败测试：fake provider 从固定 JSON 返回 `command` / `answer` / `clarify`。
- [ ] 实现 `LLMSettings`、`LLMIntent`、`LLMProvider`、`FakeLLMProvider`、`build_llm_router()`。
- [ ] 运行 `.\.venv\Scripts\python.exe -m unittest tests.test_llm -v`。

### Task 2: Agent 接入 LLM Router

**Files:**
- Modify: `src/jarvis_lite/agent.py`
- Test: `tests/test_agent.py`

- [ ] 写失败测试：本地确定性意图优先，不调用 LLM。
- [ ] 写失败测试：知识库可回答时不调用 LLM。
- [ ] 写失败测试：本地无法处理时调用 LLM，`command` 结果仍由 `JarvisAgent` 执行。
- [ ] 写失败测试：`clarify` 结果只提示澄清，不执行命令。
- [ ] 实现 `JarvisAgent(paths, llm_router=None)`，在长期记忆兜底前调用 LLM。
- [ ] 运行相关 agent 测试。

### Task 3: OpenAI adapter 和状态命令

**Files:**
- Modify: `src/jarvis_lite/llm.py`
- Modify: `src/jarvis_lite/agent.py`
- Modify: `pyproject.toml`
- Test: `tests/test_llm.py`
- Test: `tests/test_agent.py`

- [ ] 写失败测试：OpenAI provider 在缺 SDK 或缺 API key 时返回清晰错误。
- [ ] 写失败测试：`/llm-status` 显示 provider、model、启用状态。
- [ ] 实现 `OpenAIResponsesProvider`，延迟导入 OpenAI SDK，输出统一 `LLMIntent`。
- [ ] 将 `openai` 加入依赖。
- [ ] 运行 llm 和 agent 测试。

### Task 4: 文档与完整验证

**Files:**
- Modify: `README.md`
- Modify: `word/PROJECT-PLAN.md`
- Modify: `word/plans/2026-05-27-v3-pc-agent-llm-first-plan.md`
- Modify: `word/progress/2026-05-27.md`
- Modify: `verification/2026-05/2026-05-27.md`

- [ ] 文档补充 LLM provider 配置方式。
- [ ] 运行 `git diff --check`。
- [ ] 运行 Markdown 本地链接检查。
- [ ] 运行 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`。
- [ ] 运行 `.\.venv\Scripts\python.exe -m jarvis_lite.desktop.app --smoke`。
- [ ] 提交并 push。
