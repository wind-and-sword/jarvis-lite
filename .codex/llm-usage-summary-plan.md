# LLM 本地用量汇总计划

> 日期：2026-05-27
> 执行者：Codex

## 目标

在真实 API key 未就绪时，继续完善不触网的 LLM 基础设施：新增 `/llm-usage`，从本地 `logs/jarvis.log` 汇总已经记录的 token usage。

## 设计

- `LLMUsage` 继续作为 provider-neutral 用量结构。
- `summarize_llm_usage(log_lines)` 只接收日志行，不读取文件系统，便于本地单元测试。
- `JarvisAgent` 增加 `/llm-usage` slash command，读取 `paths.log_path` 并调用汇总函数。
- `/help` 展示 `/llm-usage`，避免用户只能通过文档发现命令。

## 验收

- RED：汇总函数未导出、`/llm-usage` 未识别、`/help` 未列出命令。
- GREEN：LLM usage 汇总专项测试通过。
- 回归：`tests.test_llm`、`tests.test_agent`、全量 `unittest`、桌面 smoke、Markdown 本地链接和 `git diff --check`。
