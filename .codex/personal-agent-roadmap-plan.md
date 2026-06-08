# Agent 认知沉淀与 Jarvis Lite 下一步计划

日期：2026-05-22  
执行者：Codex

## 目标

1. 新增个人技能记录文档，沉淀用户与 ChatGPT、Codex 关于 Agent、RAG、LLM、MCP、Function Calling 的讨论。
2. 新增 Jarvis Lite 个人设备级 Agent 方案文档，把当前项目进度与后续电脑、手机、手表路线融合。
3. 继续实现“草稿参数接收第一版”，让建议命令草稿可以被用户补全后重新进入确认执行流程。

## 文档产物

- `word/2026-05-22-ai-agent-learning-notes.md`
- `word/2026-05-22-jarvis-lite-personal-device-agent-plan.md`
- 更新 `word/文档索引.md` 和 `README.md` 文档入口。

## 实现范围

- 当用户先通过“执行第一条建议”拿到 `/import <源文件或目录路径> [目标文件名]` 草稿后，再输入完整 `/import 路径` 命令，Jarvis Lite 先进入待确认状态。
- “确认执行”复用现有命令执行路径。
- 没有草稿上下文时，普通 `/import 路径` 仍按原逻辑直接执行。
- 本阶段不做参数自动推断，不持久化草稿，不支持自然语言填槽。

## 验证

- RED：新增 Agent 测试先证明草稿补全命令会被直接执行而不是进入确认。
- GREEN：实现后专项测试通过。
- 收尾：`python -m unittest discover -s tests -v`、桌面 smoke、`git diff --check`。
