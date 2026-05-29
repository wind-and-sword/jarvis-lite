# Jarvis Lite v17：桌面外脑运行状态方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v16 桌面外脑待补充状态，明确 `0.13.0` 的外脑调用可观察性收口。

## 核心结论

`0.13.0` 不继续扩展自然语言规则，而是把 LLM 外脑的运行状态和最近一次调用结果固定展示到桌面面板：

```text
用户输入
  -> Agent 判断是否需要 LLM
  -> LLMRouter 返回 answer / command / clarify / no_action
  -> Agent 记录最近外脑调用快照
  -> Bridge 读取只读状态
  -> Panel 固定展示外脑运行状态和最近调用结果
```

这样用户可以直接判断当前聊天到底有没有走外脑、外脑返回了什么类型的结果，而不是只能从 transcript 里猜。

## 设计边界

- 不调用 `/llm-status` 做后台刷新，避免污染对话历史。
- 不保存或展示 API key。
- 不改变 LLM provider adapter。
- 不改变 InnerBrain 的样本分类器优先策略。
- 不新增自然语言正则模板。

## 0.13.0 收口内容

- RuntimeContext 增加最近 LLM 调用快照。
- Agent 暴露只读 LLM 运行状态文本。
- LLM fallback、smoke、搜索总结/比较和澄清补充路径记录最近调用。
- DesktopBridge 在每次发送后附带最新 LLM 运行状态。
- AssistantPanel 增加固定外脑运行状态 label，启动时和响应后刷新。
- 项目版本同步到 `0.13.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 将外脑状态进一步拆为“配置状态”“待补充状态”“最近调用结果”三个更清晰的状态块。
- 继续打磨 LLM prompt，让外脑返回更稳定的命令建议、澄清问题和自然语言回答。
