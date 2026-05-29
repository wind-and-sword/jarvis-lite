# Jarvis Lite v14：LLM 外脑澄清状态持久化方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v13 LLM 外脑多轮澄清方案，明确 `0.10.0` 的运行态恢复和可观察能力。

## 核心结论

`0.10.0` 的主线是让 LLM 外脑澄清状态不只存在于当前 Python 对象内存：

```text
LLM 外脑返回 clarify
  -> JarvisAgent 保存 pending 澄清状态
  -> RuntimeContext 写入原始问题、澄清问题和上下文
  -> 桌面重启或新建 Agent 后恢复 pending
  -> 用户下一句补充继续交给 LLM
```

同时，最近上下文会显示当前待补充的外脑问题，方便用户知道助手正在等什么。

## 设计边界

- 不新增自然语言正则模板。
- 不改变 LLM 命令白名单。
- 不持久化 API key。
- 不把 InnerBrain pending 一并持久化；本阶段只处理 LLM 外脑澄清状态。
- `/recent-context` 作为显式查看入口，不消耗 pending 澄清。

## 0.10.0 收口内容

- `RuntimeContext` 增加 LLM pending 澄清结构。
- `JarvisAgent` 启动时恢复 LLM pending。
- LLM `clarify`、补齐、取消和无结果路径都会同步 runtime context。
- 最近上下文状态展示待补充外脑问题和原始问题。
- 项目版本同步到 `0.10.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 增加 LLM 澄清轮数和过期策略。
- 把待补充外脑问题展示到桌面面板的固定状态区域。
- 继续让 LLM 基于联网搜索来源做更稳定的事实回答。
