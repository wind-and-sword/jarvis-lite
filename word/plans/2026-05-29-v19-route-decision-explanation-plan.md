# Jarvis Lite v19：路由决策解释详情方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v18 最近路由决策状态，明确 `0.15.0` 的路由选择依据可观察性收口。

## 核心结论

`0.15.0` 不改变自然语言理解策略，不新增正则模板，而是在最近路由状态里追加“依据”：

```text
用户输入
  -> InnerBrain / 知识库 / LLM / 记忆兜底 / 显式命令
  -> Agent 记录最近路由和解释字段
  -> Bridge 读取只读状态
  -> Panel 固定展示最近路由与依据
```

这样当桌面回复看起来像固定模板时，用户不仅能看到“走了哪一层”，还能看到 InnerBrain 的样本来源、置信度、缺失槽位、原因，或 LLM fallback 的 provider、model、返回类型、摘要和 reason。

## 设计边界

- 不新增自然语言正则规则。
- 不改变 InnerBrain 样本分类器优先策略。
- 不改变 LLM fallback、联网搜索和知识库的执行顺序。
- 不把路由解释变成新的路由判断输入。
- 只保存最近一条路由解释，不做完整链路追踪历史。

## 0.15.0 收口内容

- `RuntimeRouteDecisionContext` 增加 `explanation`，随运行态上下文保存和恢复。
- `RuntimeLLMCallContext` 增加 `reason`，让 LLM fallback 路由解释可追溯到外脑返回理由。
- `JarvisAgent.route_status_text()` 在存在解释时追加 `依据：...`。
- InnerBrain 执行和澄清路径解释 `source`、`confidence`、`missing` 和 `reason`。
- LLM fallback 路径解释 `provider`、`model`、`source`、`type`、`summary` 和 `reason`。
- 命令、知识库和记忆兜底路径用简短 `source/action` 标识来源。
- 项目版本同步到 `0.15.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 基于用户真实日志分析低置信度、澄清和 LLM fallback 的分布。
- 后续可扩展为最近多次路由历史，用于训练 InnerBrain runtime 样本和定位误判。
