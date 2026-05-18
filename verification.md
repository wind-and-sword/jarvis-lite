# 验证记录

> 日期：2026-05-18
> 执行者：Codex

## 验证命令

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe src/app.py --once "/memory"
.\.venv\Scripts\python.exe src/app.py --once "/list"
.\.venv\Scripts\python.exe src/app.py --once "你好"
```

## 验证结论

- 单元测试：19 个测试通过。
- 命令行入口：可启动并执行一次性输入。
- 记忆读取：`/memory` 可读取 `memory/profile.md`。
- 工具日志：`/list` 会写入 `logs/jarvis.log`。
- Python 版本：项目虚拟环境使用 Python 3.13.2。

## 未覆盖事项

- 未接入大模型 API。
- 未实现语音入口、桌面 UI 或外部系统控制。
