# Jarvis Lite v21：路由历史详情方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v20 最近路由历史，明确 `0.17.0` 的路由历史详情与最近上下文集成。

## 核心结论

`0.17.0` 不改变自然语言理解链路，不新增正则模板，不调整 InnerBrain、知识库、LLM fallback 或联网搜索的优先级。本阶段只补齐一条显式诊断入口：

```text
用户输入 /route-history
  -> Agent 读取 RuntimeContext 中最近 5 条 route decisions
  -> 返回每条记录的 route/detail/prompt/summary/explanation/created_at
  -> /recent-context 同步展示最近路由短摘要
```

这样用户测试时不必只看桌面状态短文本，可以直接在聊天区复制完整路由依据，判断某句是否走了固定命令、本地内脑、知识库、LLM 外脑或记忆兜底。

## 设计边界

- 不新增自然语言正则规则。
- 不改变 InnerBrain 样本分类器优先策略。
- 不改变 LLM fallback、联网搜索和知识库执行顺序。
- 不新增桌面控件，桌面继续展示短状态；聊天命令提供详情。
- 不扩大历史保留数量，仍然只展示最近 5 条。

## 0.17.0 收口内容

- 新增 `/route-history`、`route-history`、`/routes`、`routes` 显式命令。
- 无路由历史时返回空状态和下一步提示。
- 有路由历史时按最近优先展示完整详情：路由、时间、输入、结果和依据。
- `/recent-context` 追加最近路由摘要，和资料、搜索、LLM pending 等上下文放在同一入口。
- `/help` 与显式命令判定同步纳入路由历史入口。
- 项目版本同步到 `0.17.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 基于 `/route-history` 的明细，沉淀低置信度 InnerBrain、LLM fallback 和记忆兜底样本候选。
- 后续再考虑“采纳最近第 N 条路由为训练样本”的显式命令，仍避免把自然语言理解做成正则堆叠。
