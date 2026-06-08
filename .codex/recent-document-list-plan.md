# 最近资料列表第一版计划

> 日期：2026-05-22  
> 执行者：Codex

## 目标

在已有最近资料指针之外，维护一个最近资料列表，让用户通过“查看最近上下文”和日报看到最近处理过的多份资料。

## 方案

- `runtime_context.py` 增加 `recent_document_paths: tuple[str, ...]`，读写 JSON 时兼容旧的 `recent_document_path`。
- `JarvisAgent` 初始化时恢复最近资料列表；`_remember_recent_document()` 更新当前资料并把路径移到列表首位，最多保留 5 条。
- `_save_runtime_context()` 同步保存当前资料和最近资料列表。
- `_recent_context_status()` 在原有“最近资料”之外追加“最近资料列表：N 条”。
- `automation.py` 日报最近上下文展示最近资料列表，下一步建议仍以当前资料为主。

## 验收

- RED：新增 Agent 测试先证明读取两份资料后“查看最近上下文”没有最近资料列表。
- GREEN：最近上下文展示最近资料列表，最新在前。
- GREEN：新建 Agent 实例后仍能恢复最近资料列表。
- 回归：已有读取最近资料、最近搜索结果、最近建议和日报测试保持通过。
- 收尾：`unittest discover`、桌面 smoke、`git diff --check` 通过。
