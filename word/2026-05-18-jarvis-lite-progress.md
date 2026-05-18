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

## 验证结果

- `.venv\Scripts\python.exe --version`：当前项目虚拟环境使用 Python 3.13.2。
- `.venv\Scripts\python.exe -m unittest discover -s tests -v`：25 个测试通过。
- `.venv\Scripts\python.exe src/app.py --once "/memory"`：可以读取长期记忆。
- `.venv\Scripts\python.exe src/app.py --once "/list"`：可以调用 data 目录列表工具，并记录到 `logs/jarvis.log`。
- `.venv\Scripts\python.exe src/app.py --once "/ask Jarvis Lite 使用什么 Python 版本？"`：可以基于 `data/jarvis-lite.md` 返回带来源的回答。
- `.venv\Scripts\python.exe src/app.py --once "Jarvis Lite 当前可以读取什么？"`：普通问题可以自动命中 `data/` 资料。

## 下一步

继续增强资料问答的质量，例如多片段引用、资料摘要和更稳定的中文关键词匹配。
