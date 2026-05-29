# Jarvis Lite v20：最近路由历史方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v19 路由决策解释详情，明确 `0.16.0` 的最近多次路由历史收口。

## 核心结论

`0.16.0` 不改变自然语言理解、LLM fallback、联网搜索或知识库问答策略，而是把最近路由状态从“只看最新一条”扩展为“最新一条 + 最近 5 条短历史”：

```text
用户连续输入
  -> Agent 每次记录 route/detail/prompt/summary/explanation
  -> RuntimeContext 保存最新路由和最近 5 条路由历史
  -> Bridge 读取只读状态
  -> Panel 固定展示最新路由与最近路由历史
```

这样用户连续测试时，可以直接看到上一句、上上一句分别走了 InnerBrain、命令、LLM fallback、知识库还是记忆兜底，为后续沉淀 InnerBrain runtime 样本和定位误判提供依据。

## 设计边界

- 不新增自然语言正则规则。
- 不改变 InnerBrain 样本分类器优先策略。
- 不改变 LLM fallback、联网搜索和知识库的执行顺序。
- 历史只保留最近 5 条，不做完整审计日志。
- 桌面继续复用 `route_status_text()`，不新增后台轮询。

## 0.16.0 收口内容

- `RuntimeContext` 增加 `recent_route_decisions`，保存最近 5 条路由决策。
- 保留 `recent_route_decision` 作为最新单条字段，兼容旧运行态。
- `JarvisAgent._remember_route_decision()` 同步更新最新路由和短历史。
- `JarvisAgent.route_status_text()` 在最新路由详情后追加“最近路由历史”。
- DesktopBridge 和 AssistantPanel 复用既有路由状态透传，自动展示历史。
- 项目版本同步到 `0.16.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 基于最近路由历史分析低置信度、澄清和 LLM fallback 的集中场景。
- 后续可增加独立 explain/detail 命令，展示某条历史的完整 explanation 或原始样本匹配详情。
