# 自然语言读取资料计划

> 日期：2026-05-22  
> 执行者：Codex

## 目标

让“读取 note.txt”“查看 manual.md”等自然语言表达复用现有 `/read 文件名`，并继承 `/read` 已具备的最近资料上下文更新。

## 范围

- 识别 `读取`、`查看`、`看看` 后接 `.md` 或 `.txt` 文件名。
- 支持引号包裹的带空格文件名。
- 复用 `NaturalLanguageIntent("command", command="/read ...")`。
- 不新增新的读取工具，不改变 `/read` 输出格式。
- 不把“查看知识库”“查看最近上下文”“查看第一条结果/建议”映射为文件读取。

## 实施步骤

1. 在 `tests/test_agent.py` 增加 RED 测试：自然语言读取 data 文件后可继续“给这个资料打标签”。
2. 在 `intent.py` 增加 `_parse_read_document_intent()`，并在编号结果/建议解析之前调用。
3. 跑新增测试、Agent 专项测试、完整测试、桌面 smoke 和 `git diff --check`。
4. 更新 README、进度文档、方案文档、验证记录和 `.codex` 留痕。

## 验收标准

- “读取 manual.md”返回文件内容。
- 读取后“给这个资料打标签 项目”更新 `data/manual.md`。
- “查看第一条结果”和“查看第一条建议”仍走原编号上下文逻辑。
