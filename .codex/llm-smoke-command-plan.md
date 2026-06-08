# LLM 调用 Smoke 命令计划

> 日期：2026-05-27
> 执行者：Codex

## 目标

新增 `/llm-smoke [prompt]`，用于强制通过当前 LLM Router 做一次调用验证，同时避免执行模型返回的命令建议。

## 接口契约

- 输入：`/llm-smoke` 或 `/llm-smoke 自定义提示词`。
- 未配置/未启用：返回 `LLM smoke：LLM 外脑未启用。`，并建议查看 `/llm-status` 和 `/llm-config-example openai-compatible`。
- 已启用：调用 `llm_router.complete_intent(prompt, context)`。
- 输出：展示 intent 类型，并按类型展示回答、澄清问题、命令建议或原因。
- 约束：不执行 LLM 返回的 command；不打印 API key；不写死 base URL、model 或 key。
- 用量：如果 provider 返回 usage，沿用现有 `_record_llm_usage()` 写入本地日志。

## 实施步骤

1. 补 Agent 测试：help 列出 `/llm-smoke`，未启用时返回配置提示。
2. 补 Agent 测试：fake answer provider 返回 smoke 结果并记录调用 prompt。
3. 补 Agent 测试：fake command provider 只展示命令建议，不执行 `/kb-summary`。
4. 补 Agent 测试：usage provider 返回 usage 时写入 `logs/jarvis.log`。
5. 实现命令分支、默认 prompt 和 `_llm_smoke()` 辅助方法。
6. 更新 README、方案、进度和验证记录。
7. 运行专项、全量、桌面 smoke、Markdown 链接检查和 diff 检查。
