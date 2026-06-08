# 自然语言资料标签计划

> 日期：2026-05-21
> 执行者：Codex

## 上下文扫描

- `/tag 文件名 标签...` 已在 `JarvisAgent._handle_command()` 中实现。
- 标签写入 `data/.knowledge-tags.json`，由 `set_document_tags()` 负责规范化和去重。
- 自然语言入口集中在 `src/jarvis_lite/intent.py`，简单意图可返回 `NaturalLanguageIntent("command", command="...")`。
- `tests/test_agent.py` 已覆盖 `/tag` 命令和标签检索。

## 方案

- 新增确定性自然语言格式：
  - `给 note.txt 打标签 项目 Python`
  - `把 note.txt 标记为 项目 Python`
- 解析结果直接映射为 `/tag note.txt 项目 Python`。
- 不做“这个资料”上下文指代，不做模糊文件名搜索，不做批量标签，避免引入不稳定语义。

## 验收

- RED：自然语言标签表达先落入普通资料问答或兜底，无法更新标签。
- GREEN：自然语言标签表达可更新知识库标签，`/kb` 展示标签。
- 验证：`tests.test_agent`、全量测试、桌面 smoke、`git diff --check`。
