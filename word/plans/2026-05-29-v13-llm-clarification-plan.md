# Jarvis Lite v13：LLM 外脑多轮澄清方案

> 日期：2026-05-29
> 执行者：Codex
> 说明：本文承接 v12 桌面配置面板方案，明确 `0.9.0` 的外脑自然语言澄清链路。

## 核心结论

`0.9.0` 的主线是把 LLM 外脑自己的 `clarify` 结果接成多轮对话：

```text
用户提出开放式自然语言问题
  -> InnerBrain 与 data 未命中
  -> LLM 外脑返回 clarify
  -> JarvisAgent 保存原始问题、澄清问题和上下文
  -> 用户直接补充一句话
  -> JarvisAgent 将“原始问题 + 澄清问题 + 用户补充”再次交给 LLM
  -> LLM 返回 answer 或白名单 command
  -> JarvisAgent 按既有外脑执行规则输出或执行
```

这不是继续堆正则。InnerBrain 仍负责本地轻量分类和工具槽位，LLM 外脑负责开放式自然语言理解、推理和追问。

## 设计边界

- 不新增自然语言正则模板。
- 不新增 LLM provider adapter。
- 不改变 LLM 命令白名单，外脑 command 仍必须通过 `is_llm_allowed_command`。
- 不把用户补充直接当本地命令执行，补充只用于完成同一次 LLM 外脑判断。
- LLM 再次返回 `clarify` 时保存新的待澄清状态，保持多轮能力的最小闭环。

## 0.9.0 收口内容

- `JarvisAgent` 增加 LLM 待澄清状态。
- `handle()` 在 InnerBrain 待澄清之后处理 LLM 待澄清。
- LLM clarify 首次响应时保存 pending 并提示用户补充。
- 用户补充后再次调用 LLM，继续处理最终 `answer` 或 `command`。
- 用户回复取消短语时清空 pending，不再调用 LLM。
- 项目版本同步到 `0.9.0`，README、PROJECT-PLAN、验证记录和安装包同步本轮范围。

## 后续方向

- 增加 LLM 多轮澄清的轮数和超时策略。
- 把 LLM 澄清状态展示到桌面面板的状态区域。
- 继续让联网搜索结果进入 LLM 外脑上下文，用于需要事实来源的自然语言回答。
