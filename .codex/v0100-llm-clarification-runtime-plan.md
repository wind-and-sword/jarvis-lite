# Jarvis Lite 0.10.0 LLM 外脑澄清状态持久化计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

把 0.9.0 的 LLM 外脑待澄清状态纳入运行态上下文，让桌面重启或新建 Agent 后仍能继续补充；同时让用户可以在最近上下文里看到当前待补充的外脑问题。

## 设计

- 在 `runtime_context.py` 增加可序列化的 LLM pending 澄清结构，字段包含原始问题、澄清问题和当时上下文。
- `JarvisAgent.__init__` 从 RuntimeContext 恢复 `_pending_llm_clarification`。
- LLM 返回 `clarify` 时，保存 pending 并写入 runtime context。
- 用户补齐、取消或 provider 无结果时，清空 pending 并写入 runtime context。
- `_recent_context_status()` 展示：
  - 待补充外脑问题
  - 外脑原始问题
  - 取消提示
- 增加 `/recent-context` 命令作为不消耗 pending 的显式查看入口。

## 边界

- 不新增自然语言正则模板。
- 不改变 LLM command 白名单。
- 不持久化真实 API key 或 provider 响应原文。
- 不把 InnerBrain pending 一并持久化，避免扩大范围。

## TDD 验收

1. RED：LLM 澄清 pending 能跨 Agent 实例恢复，并用用户补充继续调用 provider。
2. RED：最近上下文能展示待补充外脑问题，查看时不消耗 pending。
3. RED：取消 LLM 澄清会清空运行态 pending，新 Agent 不再继续该澄清。
4. RED：项目版本提升到 `0.10.0`。
5. GREEN：实现 runtime context 读写、Agent 恢复、清理和最近上下文展示。
6. 验证：目标测试、邻近回归、全量 unittest、桌面 smoke、安装包构建和 packaged exe smoke。
