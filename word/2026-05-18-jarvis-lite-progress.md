# Jarvis Lite 阶段 1 进度记录

> 日期：2026-05-18
> 执行者：Codex

## 当前目标

初始化第一阶段 Python 命令行助手骨架，让项目具备命令行启动、读取长期记忆、调用基础本地工具和记录日志的能力。

## 本次计划

1. 创建 `src/`、`memory/`、`data/`、`logs/`、`tests/` 等目录。
2. 创建 `memory/profile.md` 作为第一版长期记忆。
3. 实现命令行入口和基础 Agent 调度。
4. 实现本地工具白名单和日志记录。
5. 编写并运行本地自动化测试。

## 当前状态

已完成第一步骨架初始化。

## 已完成

- 创建 `src/jarvis_lite/` Python 包和 `src/app.py` 命令行入口。
- 创建 `memory/profile.md` 长期记忆文件。
- 创建 `data/`、`logs/`、`tests/`、`word/` 目录。
- 实现基础 Agent 调度、长期记忆读取、本地工具白名单和日志记录。
- 写入 `pyproject.toml`，保留后续安装为命令行脚本的入口。
- 创建 `.python-version`，并将 `pyproject.toml` 的 Python 版本范围固定为 `>=3.13,<3.14`。
- 使用标准库 `unittest` 编写本地测试。
- 新增 `src/jarvis_lite/knowledge.py`，支持检索 `data/` 目录中的 `.txt` 和 `.md` 文本资料。
- 新增 `/ask 问题` 命令，普通问题也会优先尝试使用 `data/` 资料回答。
- 新增 `data/jarvis-lite.md` 示例资料，用于验证第一阶段资料问答能力。
- 增强资料问答输出：最多返回 3 条来源片段，跳过 Markdown 标题，并在强命中存在时过滤弱相关片段。
- 新增 `src/jarvis_lite/conversation.py`，交互式命令行可以记录当前会话历史。
- 新增 `/history`、`/save-summary 文件名`、`/clear`，支持查看会话、保存会话总结和清空当前会话。
- 新增长期记忆写入能力：`/remember 记忆内容` 可以追加到 `memory/profile.md`。
- 新增基础身份识别：`我叫...` 会写入 `用户姓名`，`我是...` 会写入 `用户身份`，之后可以回答“你知道我是谁吗”。
- 调整 README 职责：README 只保留项目入口、快速启动和当前状态，整体方案迁移到 `word/jarvis-lite-overall-plan.md`。
- 增强长期记忆更新：同 key 记忆会替换旧值，例如再次说“我叫...”会更新 `用户姓名`，不会保留旧姓名。

## 验证结果

- `.venv\Scripts\python.exe --version`：当前项目虚拟环境使用 Python 3.13.2。
- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：43 个测试通过。
- `.venv\Scripts\python.exe src/app.py --once "/memory"`：可以读取长期记忆。
- `.venv\Scripts\python.exe src/app.py --once "/list"`：可以调用 data 目录列表工具，并记录到 `logs/jarvis.log`。
- `.venv\Scripts\python.exe src/app.py --once "/ask Jarvis Lite 使用什么 Python 版本？"`：可以基于 `data/jarvis-lite.md` 返回带来源的回答。
- `.venv\Scripts\python.exe src/app.py --once "Jarvis Lite 当前可以读取什么？"`：普通问题可以自动命中 `data/` 资料。
- `.venv\Scripts\python.exe src/app.py --once "/ask Jarvis Lite 当前可以什么？"`：可以返回多个强相关资料片段。
- 交互式 CLI 冒烟验证通过：`/history` 能查看当前会话，`/save-summary cli-smoke` 能写入会话总结；临时冒烟文件已删除，不作为正式文档保留。
- 身份记忆 CLI 冒烟验证通过：`我叫测试用户`、`我是Jarvis Lite测试者` 能写入长期记忆，随后“你知道我是谁吗”能回答身份；测试后已恢复原始 `memory/profile.md`。
- 记忆更新测试通过：先写入 `用户姓名：张三`，再写入 `用户姓名：李四`，最终只保留 `李四`。

## 下一步

继续完善长期记忆体验，例如记忆分类、记忆查看筛选和可编辑的记忆管理命令。
