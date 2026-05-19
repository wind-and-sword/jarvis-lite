# 验证记录

> 日期：2026-05-19
> 执行者：Codex

## 验证命令

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe src/app.py --once "/memory"
.\.venv\Scripts\python.exe src/app.py --once "/status"
.\.venv\Scripts\python.exe src/app.py --once "/kb"
.\.venv\Scripts\python.exe src/app.py --once "/import .codex/import-smoke.md import-smoke.md"
.\.venv\Scripts\python.exe src/app.py --once "/list"
.\.venv\Scripts\python.exe src/app.py --once "你好"
.\.venv\Scripts\python.exe src/app.py --once "/ask Jarvis Lite 使用什么 Python 版本？"
.\.venv\Scripts\python.exe src/app.py --once "Jarvis Lite 当前可以读取什么？"
@'
hello
/history
/save-summary cli-smoke
/exit
'@ | .\.venv\Scripts\python.exe -X utf8 src/app.py
@'
我叫测试用户
我是Jarvis Lite测试者
你知道我是谁吗
/exit
'@ | .\.venv\Scripts\python.exe -X utf8 src/app.py
```

## 验证结论

- 单元测试：53 个测试通过。
- 命令行入口：可启动并执行一次性输入。
- 记忆读取：`/memory` 可读取 `memory/profile.md`。
- 阶段状态：`/status` 可输出阶段 1 能力闭环和关键文件位置。
- 知识库状态：`/kb` 可输出 `data/` 中可检索资料数量、行数和资料列表。
- 资料导入：`/import 源文件路径 [目标文件名]` 可把 Markdown 或 txt 导入 `data/`，导入后可被 `/kb` 和 `/ask` 使用。
- 工具日志：`/list` 会写入 `logs/jarvis.log`。
- Python 版本：项目虚拟环境使用 Python 3.13.2。
- 资料问答：`/ask` 和普通问题可以基于 `data/` 文本返回最多 3 条带来源的回答，并过滤弱相关片段。
- 会话功能：交互式 CLI 可以查看 `/history`，并用 `/save-summary 文件名` 写入 `word/` 会话总结。
- 长期记忆写入：`/remember`、`我叫...`、`我是...` 可以写入 `memory/profile.md`，并支持回答“我是谁”。
- 长期记忆更新：同 key 记忆会替换旧值，例如 `用户姓名` 不会重复保留多个版本。

## 未覆盖事项

- 未接入大模型 API。
- 未实现语音入口、桌面 UI 或外部系统控制。
