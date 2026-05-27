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
- LLM 外脑 Router 第一版，支持 `off`、`fake`、`openai` 和 `openai-compatible`、完整 `/v1/responses` URL 归一化、provider 命令白名单、`/llm-smoke` 配置验证，并记录、汇总 provider 返回的 token 用量。
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
python src/app.py --once "/llm-smoke"
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

真实 provider 的 instructions 会列出可返回的 Jarvis Lite 命令白名单，例如 `/kb-summary`、`/ask 问题`、`/read 文件名` 和 `/tag 文件名 标签...`。模型不得返回列表之外的命令；参数不确定时应返回澄清问题。

```powershell
$env:JARVIS_LITE_LLM_PROVIDER = "off"     # off | fake | openai | openai-compatible
$env:JARVIS_LITE_LLM_MODEL = "按 provider 当前可用模型填写"
$env:JARVIS_LITE_LLM_API_KEY = "..."
$env:JARVIS_LITE_LLM_BASE_URL = ""        # openai-compatible 必填，可填 /v1 或完整 /v1/responses URL
$env:JARVIS_LITE_LLM_FAKE_RESPONSE = '{"type":"answer","answer":"测试回答"}'
python src/app.py --once "/llm-status"
python src/app.py --once "/llm-smoke 请用一句话确认连接可用"
python src/app.py --once "/llm-usage"
python src/app.py --once "/llm-config-example openai"
```

`openai-compatible` 适用于提供 OpenAI Responses API 兼容端点的合法网关，使用 `base_url + api_key + model` 接入。`JARVIS_LITE_LLM_BASE_URL` 可以填写 SDK 需要的 base URL（通常到 `/v1`），也可以直接粘贴完整 Responses URL（例如完整路径到 `/v1/responses`），Jarvis Lite 调用 SDK 时会自动归一化为 base URL。provider 返回 usage 时，Jarvis Lite 会把 `input_tokens`、`output_tokens` 和 `total_tokens` 记录到 `logs/jarvis.log`。

`/llm-status` 会做本地配置诊断：例如缺少 `JARVIS_LITE_LLM_MODEL`、`JARVIS_LITE_LLM_API_KEY`、`JARVIS_LITE_LLM_BASE_URL` 或 provider 名称不支持时，会直接列出配置问题，不会打印 API key 内容。配置了完整 `/v1/responses` URL 时，状态会同时显示原始 Base URL 和 SDK 实际使用的 Base URL。

`/llm-smoke [prompt]` 会强制调用当前 LLM Router 做一次配置验证；它只展示模型返回的结构化意图，不会执行模型给出的命令建议。provider 返回 usage 时，仍会写入本地 `logs/jarvis.log`，之后可用 `/llm-usage` 汇总。

`/llm-usage` 会从本地 `logs/jarvis.log` 汇总 provider/model 维度的 token 用量，不需要真实 API key，也不会触发网络请求。

`/llm-config-example [provider]` 会输出 PowerShell 环境变量配置模板，支持 `off`、`fake`、`openai` 和 `openai-compatible`，`qwen` / `gemini` 会先映射到兼容端点模板；模板只显示占位符，不读取或保存真实 API key，并提示兼容端点可填写完整 `/v1/responses` URL。

当前真实 provider 先接入 OpenAI Responses API 和 OpenAI-compatible Responses 端点；Gemini、Qwen 会沿用同一 Router/Provider 接口继续扩展。

## 常用命令

```text
/help
/status
/llm-status
/llm-smoke [prompt]
/llm-usage
/llm-config-example [provider]
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
