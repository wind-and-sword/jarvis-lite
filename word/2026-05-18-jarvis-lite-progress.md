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
- 使用标准库 `unittest` 编写本地测试。

## 验证结果

- `python -m unittest discover -s tests -v`：16 个测试通过。
- `python src/app.py --once "/memory"`：可以读取长期记忆。
- `python src/app.py --once "/list"`：可以调用 data 目录列表工具，并记录到 `logs/jarvis.log`。

## 下一步

围绕 `data/` 目录补充文本资料读取问答能力，并让 `/read` 和普通对话更自然地结合。
