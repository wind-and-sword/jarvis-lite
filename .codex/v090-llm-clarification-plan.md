# Jarvis Lite 0.9.0 LLM 外脑多轮澄清计划

> 日期：2026-05-29
> 执行者：Codex

## 目标

让 LLM 外脑返回 `clarify` 时进入真正的多轮澄清：Agent 保存原始问题和澄清问题，用户下一句补充后继续交给 LLM 生成最终 `command` 或 `answer`，不再把补充当作全新问题。

## 设计

- 在 `JarvisAgent` 中新增 LLM 待澄清状态，保存原始 prompt、澄清问题和当时的上下文。
- `handle()` 在 InnerBrain 待澄清之后、重新理解新输入之前消费 LLM 待澄清。
- 用户回复取消短语时清空 LLM 待澄清，不再次调用 provider。
- 用户回复补充信息时构造续聊 prompt：
  - 原始问题
  - 外脑澄清问题
  - 用户补充
- 续聊上下文复用原上下文，并追加“LLM 澄清补充：...”标记。
- 最终 LLM 返回 `command` 时继续走白名单与既有命令执行；返回 `answer` 时继续按“LLM 外脑：...”输出；再次返回 `clarify` 时替换 pending。

## 边界

- 不新增正则自然语言意图识别。
- 不新增 provider adapter。
- 不提交本机 `config/*.local.json`。
- 不让 LLM 绕过 `is_llm_allowed_command` 白名单。

## TDD 验收

1. RED：LLM clarify 后用户补充应带着原始问题和补充信息再次调用 provider，并能执行最终命令。
2. RED：LLM clarify 后用户补充可返回最终 answer。
3. RED：LLM clarify 可取消，取消时不发生第二次 provider 调用。
4. RED：项目版本提升到 `0.9.0`。
5. GREEN：实现 pending 状态、续聊 prompt、取消和日志。
6. 验证：目标测试、Agent/LLM/InnerBrain/桌面邻近回归、全量 unittest、桌面 smoke、安装包构建和 packaged exe smoke。
