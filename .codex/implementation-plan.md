# Jarvis Lite 阶段 1 骨架实现计划

> 日期：2026-05-18
> 执行者：Codex

## 目标

把 Jarvis Lite 从 README 变成可启动、可读记忆、可调用基础本地工具并记录日志的 Python 命令行项目骨架。

## 文件结构

- `src/app.py`：命令行启动脚本，支持 `python src/app.py`。
- `src/jarvis_lite/config.py`：项目路径配置和目录初始化。
- `src/jarvis_lite/memory.py`：长期记忆读取。
- `src/jarvis_lite/tools.py`：本地工具白名单、文件读取、笔记写入、总结写入、日志记录。
- `src/jarvis_lite/agent.py`：命令解析和对话调度。
- `memory/profile.md`：第一版长期记忆文件。
- `data/.gitkeep`、`logs/.gitkeep`：保留数据和日志目录。
- `tests/`：使用标准库 `unittest` 编写本地测试。
- `word/文档索引.md`、`word/2026-05-18-jarvis-lite-progress.md`：用户可读文档入口和阶段进度。

## 执行步骤

1. 先写失败测试：记忆读取、工具白名单、日志记录、Agent 命令响应。
2. 运行 `python -m unittest discover -s tests -v`，确认测试因模块缺失失败。
3. 实现 `src/jarvis_lite` 最小代码和 `src/app.py` 启动入口。
4. 运行单元测试，修复失败直到通过。
5. 运行 CLI 冒烟验证，确认命令行可启动并能读取记忆。
6. 更新 `.codex/testing.md`、`.codex/review-report.md`、`verification.md` 和 `word/` 进度文档。

## 验收标准

- `python -m unittest discover -s tests -v` 通过。
- `python src/app.py --once "/memory"` 能输出 `memory/profile.md` 内容摘要。
- 调用工具时生成 `logs/jarvis.log`。
- `word/文档索引.md` 能索引当前进度文档。
