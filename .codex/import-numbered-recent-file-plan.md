# 按编号导入最近文件到知识库计划

日期：2026-05-23
执行者：Codex

## 目标

用户查看最近文件后，可以继续说“导入第一份最近文件到知识库”或“把第2份最近文件导入知识库”，系统按编号选择最近文件并复用现有 `/import` 导入链路。

## 实施步骤

1. 在 `tests/test_agent.py` 先新增失败测试，覆盖成功导入、缺最近文件列表、编号越界。
2. 在 `src/jarvis_lite/intent.py` 新增 `import_numbered_recent_file` 意图，并让它早于通用 `_parse_import_intent()`。
3. 在 `src/jarvis_lite/agent.py` 新增 `_import_numbered_recent_file()`，复用最近文件校验和 `/import`。
4. 更新 README、验证记录和阶段文档。
5. 执行专项与全量本地验证后提交推送。

## 验收标准

- “导入第一份最近文件到知识库”会把最近文件复制进 `data/`，并可被 `/ask` 命中。
- 没有最近文件列表时提示先查看最近文件。
- 编号越界时提示当前最近文件数量。
- 不新增独立导入实现，不读取或打开系统文件内容，导入内容读取继续由 `knowledge.py` 负责。
