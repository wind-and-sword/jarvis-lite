# 读取资料后写入最近资料上下文计划

> 日期：2026-05-22  
> 执行者：Codex

## 目标

让 `/read 文件名` 成功读取 data 资料后，把该文件记录为最近资料，供“这个资料”、最近上下文状态、日报和下一步建议复用。

## 范围

- 只处理已有 `/read` 命令。
- 只在读取成功时更新最近资料。
- 复用 `RuntimeContext.recent_document_path`，不新增运行态字段。
- 不新增自然语言读取意图，不改变 `read_data_file` 工具。

## 实施步骤

1. 在 `tests/test_agent.py` 增加 RED 测试：`/read manual.md` 后，新 Agent 实例可以对“这个资料”打标签。
2. 在 `JarvisAgent._handle_command()` 的 `/read` 成功分支调用 `_remember_recent_document()`。
3. 跑专项 Agent 测试，再跑完整测试、桌面 smoke 和 `git diff --check`。
4. 更新 README、进度文档、方案文档、验证记录和 `.codex` 留痕。

## 验收标准

- `/read manual.md` 输出资料内容。
- 重启 Agent 后，“给这个资料打标签 项目”会更新 `data/manual.md`。
- 读取失败时不更新最近资料。
