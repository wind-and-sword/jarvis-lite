# 文件整理预览实现计划

> 日期：2026-05-19
> 执行者：Codex

**目标：** 增加阶段 4 非硬件自动化能力：按扩展名生成文件整理预览计划，只输出建议，不移动、不删除文件。

**架构：** 在 `automation.py` 中新增整理预览数据结构和生成函数，复用常用目录登记数据。Agent 增加 `/organize-preview 别名` 命令，读取已登记目录并输出可读计划。

**技术栈：** Python 3.13、标准库 `pathlib`、`dataclasses`、`unittest`。

## 文件范围

- 修改 `src/jarvis_lite/automation.py`：新增文件分组预览能力。
- 修改 `src/jarvis_lite/agent.py`：接入 `/organize-preview` 命令和帮助文本。
- 修改 `tests/test_automation.py`：新增整理预览单元测试。
- 修改 `tests/test_agent.py`：新增 Agent 命令测试。
- 修改 `README.md`、`verification.md`、`word/2026-05-19-jarvis-lite-phase-4-progress.md`：同步用户文档和验证记录。

## TDD 步骤

- [ ] 新增 `tests/test_automation.py` 中的失败测试：给临时目录创建 `.md`、`.txt`、无后缀文件和子目录，期望整理预览按后缀分组并跳过目录。
- [ ] 运行单个测试，确认因缺少 `preview_file_organization` 或相关类型失败。
- [ ] 在 `automation.py` 实现最小整理预览：目录存在校验、文件扫描、扩展名归类、建议目标文件夹名。
- [ ] 运行单个测试，确认通过。
- [ ] 新增 `tests/test_agent.py` 中的失败测试：登记常用目录后执行 `/organize-preview 项目`，期望输出分组计划。
- [ ] 运行单个 Agent 测试，确认旧 Agent 不识别命令。
- [ ] 在 `agent.py` 接入 `/organize-preview 别名`，增加错误提示和日志记录。
- [ ] 运行两个新增测试，确认通过。
- [ ] 更新 README、阶段 4 进度文档和验证记录。
- [ ] 运行全量测试和临时目录 CLI 冒烟。
- [ ] 提交并推送本阶段改动。
