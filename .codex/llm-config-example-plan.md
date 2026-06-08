# LLM 配置模板命令计划

> 日期：2026-05-27
> 执行者：Codex

## 目标

在真实 API key 未就绪时，继续降低接入成本：新增 `/llm-config-example [provider]`，让用户可以在命令行直接查看 LLM provider 环境变量模板。

## 设计

- `describe_llm_config_examples(provider='')` 放在 `src/jarvis_lite/llm.py`，保持 provider-neutral。
- 模板只输出占位符，不读取环境变量、不读取文件、不保存真实 API key。
- 支持 `off`、`fake`、`openai`、`openai-compatible` 四类模板。
- `qwen` / `gemini` 先映射到 `openai-compatible` 模板，原生 adapter 后续接入。
- `JarvisAgent` 只增加 slash command 入口和 help 文案，不感知具体 SDK 细节。

## 验收

- RED：函数未导出、命令未知、help 未列出命令。
- GREEN：配置模板专项测试通过。
- 回归：`tests.test_llm`、`tests.test_agent`、全量 `unittest`、桌面 smoke、Markdown 本地链接和 `git diff --check`。
