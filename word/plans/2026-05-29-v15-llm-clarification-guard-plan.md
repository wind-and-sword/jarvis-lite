# Jarvis Lite v15：LLM 外脑澄清轮数与过期策略

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v14 LLM 外脑澄清状态持久化方案，明确 `0.11.0` 的轮数和过期边界。

## 核心结论

`0.11.0` 的主线不是继续堆自然语言模板，而是让 LLM 外脑澄清流程有清晰边界：

```text
LLM 外脑返回 clarify
  -> Agent 保存第 1 轮 pending
  -> 用户补充
  -> LLM 仍需 clarify
  -> Agent 保留原始问题，递增澄清轮次
  -> 达到最大轮数后结束 pending，要求用户重新完整描述
```

同时，待补充状态会记录创建时间。过期的 pending 会在 Agent 启动时清理，避免旧状态在桌面重启后误消费用户的新输入。

## 设计边界

- 不新增自然语言正则模板。
- 不改变 LLM provider adapter。
- 不改变 InnerBrain missing 槽位逻辑。
- 不把 API key 或本地 provider 配置写入 Git。
- 轮数和过期只约束 LLM 外脑 pending 澄清状态。

## 0.11.0 收口内容

- `RuntimeContext` 的 LLM pending 澄清结构增加创建时间和澄清轮次。
- 首次 LLM `clarify` 记录第 1 轮。
- 连续 LLM `clarify` 保留真正原始问题，不嵌套“原始问题/用户补充”组合文本。
- 超过最大澄清轮数后清空 pending，并提示用户重新完整描述需求。
- 过期 pending 在 Agent 启动时清理。
- 最近上下文展示澄清轮次和过期策略。
- 项目版本同步到 `0.11.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 把待补充外脑问题展示到桌面面板固定状态区域。
- 增加 LLM 澄清后的用户纠错样本沉淀。
- 继续让 LLM 基于联网搜索来源做更稳定的事实回答。
