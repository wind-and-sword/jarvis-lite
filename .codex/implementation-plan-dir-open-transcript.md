# 常用目录打开记录实现计划

> 日期：2026-05-19
> 执行者：Codex

**目标：** 增加 `/dir-open 常用目录别名`，当前只记录打开目录请求，不启动外部应用，便于自动化验证。

**架构：** 在 `automation.py` 中新增目录打开记录函数，把请求写入 `logs/desktop-actions.txt`。Agent 复用常用目录别名解析，输出 dry-run 结果。

**技术栈：** Python 3.13、标准库 `pathlib`、`datetime`、`unittest`。

## 文件范围

- 修改 `src/jarvis_lite/automation.py`：新增目录打开记录数据结构和写入函数。
- 修改 `src/jarvis_lite/agent.py`：接入 `/dir-open` 命令和帮助文本。
- 修改 `tests/test_automation.py`：新增 transcript 写入单元测试。
- 修改 `tests/test_agent.py`：新增 `/dir-open` 命令测试。
- 修改 `README.md`、`verification.md`、`word/2026-05-19-jarvis-lite-phase-4-progress.md`：同步文档和验证记录。

## TDD 步骤

- [ ] 新增 `record_directory_open_request` 单元测试，先确认函数缺失。
- [ ] 实现写入 `logs/desktop-actions.txt` 的最小函数。
- [ ] 新增 Agent `/dir-open` 测试，先确认命令缺失。
- [ ] 接入 `/dir-open 常用目录别名`，复用已登记目录。
- [ ] 更新文档。
- [ ] 运行全量测试和 CLI 冒烟。
- [ ] 提交并推送。
