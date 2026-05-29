# Jarvis Lite v18：最近路由决策状态方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v17 桌面外脑运行状态，明确 `0.14.0` 的输入处理路径可观察性收口。

## 核心结论

`0.14.0` 不改变自然语言识别策略，而是让 Agent 明确记录最近一条输入的处理路径：

```text
用户输入
  -> 命令 / 身份 / InnerBrain / 知识库 / LLM / 记忆兜底
  -> Agent 记录最近路由决策
  -> Bridge 读取只读状态
  -> Panel 固定展示最近路由
```

这样当桌面回复看起来像固定模板时，用户可以直接看到它到底是本地能力、InnerBrain、知识库命中，还是 LLM 外脑生成。

## 设计边界

- 不新增自然语言正则模板。
- 不改变 InnerBrain 样本分类器优先策略。
- 不改变 LLM fallback 决策顺序。
- 不调用 `/recent-context` 或 `/history` 做后台状态刷新。
- 只记录最近一条路由决策，不做完整链路追踪历史。

## 0.14.0 收口内容

- RuntimeContext 增加最近路由决策快照。
- Agent 暴露只读最近路由状态文本。
- 关键处理路径记录 `command`、`inner-brain`、`inner-brain-clarify`、`knowledge`、`llm-fallback` 和 `memory-fallback`。
- DesktopBridge 在每次发送后附带最新路由状态。
- AssistantPanel 增加固定路由状态 label，启动时和响应后刷新。
- 项目版本同步到 `0.14.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 在真实日志中沉淀“为什么没有走外脑”的路由决策样本。
- 后续可把最近路由扩展为最近多次路由历史，用于分析误判和训练 InnerBrain。
