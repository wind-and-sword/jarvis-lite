# Jarvis Lite 0.11.0：LLM 外脑澄清轮数与过期策略计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

在 `0.10.0` 已经让 LLM pending 澄清状态跨 Agent 恢复后，补齐运行边界：

- LLM 连续追问时不嵌套原始 prompt。
- LLM 澄清轮数可观察、可限制。
- 过期 pending 不继续拦截用户新问题。

## 设计

### 数据结构

- `PendingLLMClarification` 增加：
  - `clarification_count`：当前第几轮澄清。
  - `created_at`：首次 pending 创建时间，ISO 秒级字符串。
- `RuntimeLLMClarificationContext` 同步增加以上字段。

### 行为

- 首次 LLM `clarify`：保存第 1 轮 pending。
- 用户补充后 LLM 再次返回 `clarify`：
  - 未超过最大轮数时，继续保存 pending，保留最初的 `original_prompt`。
  - 超过最大轮数时，清空 pending，并提示用户重新完整描述需求。
- Agent 启动时发现 pending 过期：清空 pending 并写回 runtime context。
- `/recent-context` 显示“澄清轮次：x/y”和过期说明。

## 验证

1. 先写失败测试：
   - 连续 clarify 保留原始问题、递增轮数、继续可补齐。
   - 超过最大轮数后清空 pending，新输入可进入新的 LLM fallback。
   - 过期 runtime pending 启动后不会消费新输入。
   - 版本一致性目标为 `0.11.0`。
2. 实现最小生产代码。
3. 运行目标测试、邻近回归、全量测试、桌面 smoke、安装包验证、静态检查和敏感扫描。
