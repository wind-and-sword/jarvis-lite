# Jarvis Lite

> 日期：2026-05-27
> 执行者：Codex
> 说明：本项目是本地优先的个人 PC Agent 实验项目。

Jarvis Lite 的目标是让 AI 逐步理解并使用个人电脑上的记忆、知识库、文件、目录、最近上下文和桌面工作流。它不是纯聊天机器人，也不是一开始就做多端平台；当前主线是先把 PC Agent 做稳，再接入 LLM 外脑，最后评估手机、手表、车机和 AR 眼镜等入口。

当前方案见：[word/PROJECT-PLAN.md](word/PROJECT-PLAN.md)。

## 当前能力

- 命令行助手和 PySide6 桌面助手入口。
- 长期记忆、经验记忆、个人知识库和资料标签。
- Markdown、txt、PDF、JSON 聊天记录和资料目录导入。
- 知识库问答、摘要、按标签读取资料组和批量打标签确认闭环。
- 最近资料、最近文件、最近目录、最近搜索结果、最近建议和批量标签历史。
- 本地自然语言意图层，可处理常见中文表达。
- LLM 外脑 Router 第一版，支持 `off`、`fake` 和 OpenAI Responses API provider。
- 桌面小助手、助手面板、托盘、快捷命令、主题、尺寸、开机启动和更新入口。
- 本地 `unittest` 验证体系。

## 快速启动

推荐使用 Python 3.13 系列：

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\activate
python -m pip install -e .
```

启动命令行助手：

```powershell
python src/app.py
```

一次性执行命令：

```powershell
python src/app.py --once "/status"
python src/app.py --once "/kb"
python src/app.py --once "/kb-summary"
python src/app.py --once "/llm-status"
python src/app.py --once "查看最近上下文"
python src/app.py --once "总结知识库"
```

启动桌面助手：

```powershell
jarvis-lite-desktop
```

运行测试：

```powershell
python -m unittest discover -s tests -v
```

## LLM 外脑配置

默认不开启 LLM 外脑，本地命令、身份、本地自然语言意图和知识库问答仍然优先处理。只有本地无法处理的普通输入，才会进入 LLM Router；LLM 返回的是结构化意图，实际命令仍由 `JarvisAgent` 执行。

```powershell
$env:JARVIS_LITE_LLM_PROVIDER = "off"     # off | fake | openai
$env:JARVIS_LITE_LLM_MODEL = "按 provider 当前可用模型填写"
$env:JARVIS_LITE_LLM_API_KEY = "..."
$env:JARVIS_LITE_LLM_BASE_URL = ""        # 可选，预留给兼容端点
$env:JARVIS_LITE_LLM_FAKE_RESPONSE = '{"type":"answer","answer":"测试回答"}'
python src/app.py --once "/llm-status"
```

当前真实 provider 先接入 OpenAI Responses API；Gemini、Qwen 和 OpenAI-compatible 端点会沿用同一 Router/Provider 接口继续扩展。

## 常用命令

```text
/help
/status
/llm-status
/memory
/kb
/kb-summary
/import 源文件或目录路径 [目标文件名]
/tag 文件名 标签...
/tag-history
/read 文件名
/ask 问题
/recent-files
/daily-report [文件名]
/experience 经验内容
/experience-advice 关键词
/update-status [清单路径或URL]
/update-download [清单路径或URL]
```

## 文档入口

- [word/PROJECT-PLAN.md](word/PROJECT-PLAN.md)：当前项目方案。
- [word/文档索引.md](word/文档索引.md)：正式文档索引。
- [DOCUMENTATION.md](DOCUMENTATION.md)：项目文档整理约定。
- [verification.md](verification.md)：验证记录入口。
