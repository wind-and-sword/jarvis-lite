# Jarvis Lite

> 日期：2026-05-19
> 执行者：Codex
> 说明：本项目是个人 AI 助手实验项目。

Jarvis Lite 是一个本地优先的个人智能助手起点。当前重点是先把命令行助手跑通，再逐步扩展长期记忆、个人知识库、语音入口和桌面自动化。

完整方案和路线图见：[word/jarvis-lite-overall-plan.md](word/jarvis-lite-overall-plan.md)。

## 当前状态

当前已具备：

- 读取 `memory/profile.md` 长期记忆。
- 通过 `/remember`、`我叫...`、`我是...` 写入长期记忆，并能回答“我是谁”。
- 读取 `data/` 目录中的 `.txt` 和 `.md` 文本资料，并通过 `/ask` 或普通问题返回最多 3 条带来源的基础回答。
- 通过 `/kb` 查看个人知识库状态，包括资料文件数量、可检索行数和资料列表。
- 通过 `/import` 把外部 Markdown、txt 文件或资料目录导入 `data/` 个人知识库。
- 在交互式命令行中记录当前会话历史，并可把本轮会话总结写入 `word/`。
- 将工具调用记录到 `logs/jarvis.log`。
- 通过 `/status` 查看第一阶段能力闭环和关键文件位置。
- 使用 Python 3.13 系列和标准库 `unittest` 执行本地测试。

## 快速启动

推荐使用 Python 3.13 系列创建本地虚拟环境：

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\activate
python --version
```

启动交互式命令行助手：

```powershell
python src/app.py
```

一次性执行命令：

```powershell
python src/app.py --once "/memory"
python src/app.py --once "/status"
python src/app.py --once "/kb"
python src/app.py --once "/import E:\path\to\note.md"
python src/app.py --once "/import E:\path\to\knowledge-folder"
python src/app.py --once "/list"
python src/app.py --once "/ask Jarvis Lite 使用什么 Python 版本？"
python src/app.py --once "我叫张三"
python src/app.py --once "你知道我是谁吗"
```

运行本地测试：

```powershell
python -m unittest discover -s tests -v
```

## 常用命令

```text
/help
/memory
/status
/kb
/import 源文件或目录路径 [目标文件名]
/remember 记忆内容
/list [目录]
/read 文件名
/ask 问题
/note 标题 内容
/summary 文件名 内容
/history
/save-summary 文件名
/clear
/exit
```

## 文档入口

- [DOCUMENTATION.md](DOCUMENTATION.md)：项目文档整理约定。
- [word/文档索引.md](word/文档索引.md)：正式文档索引。
- [word/jarvis-lite-overall-plan.md](word/jarvis-lite-overall-plan.md)：整体方案与路线图。
- [word/2026-05-18-jarvis-lite-progress.md](word/2026-05-18-jarvis-lite-progress.md)：阶段 1 当前进度。
- [word/2026-05-18-jarvis-lite-phase-2-progress.md](word/2026-05-18-jarvis-lite-phase-2-progress.md)：阶段 2 当前进度。
- [word/2026-05-19-jarvis-lite-phase-2-progress.md](word/2026-05-19-jarvis-lite-phase-2-progress.md)：阶段 2 资料导入进度。
