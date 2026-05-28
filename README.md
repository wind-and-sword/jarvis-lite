# Jarvis Lite

> 日期：2026-05-28
> 执行者：Codex
> 说明：本项目是本地优先的个人 PC Agent 实验项目。

Jarvis Lite 的目标是让 AI 逐步理解并使用个人电脑上的记忆、知识库、文件、目录、最近上下文和桌面工作流。它不是纯聊天机器人，也不是一开始就做多端平台；当前主线是先把 PC Agent 做稳，再引入 InnerBrain 本地内脑，随后继续打磨 LLM 外脑，最后评估手机、手表、车机和 AR 眼镜等入口。

当前方案见：[word/PROJECT-PLAN.md](word/PROJECT-PLAN.md)。

## 当前能力

- 命令行助手和 PySide6 桌面助手入口。
- 长期记忆、经验记忆、个人知识库和资料标签。
- Markdown、txt、PDF、JSON 聊天记录和资料目录导入。
- 知识库问答、摘要、按标签读取资料组和批量打标签确认闭环。
- 最近资料、最近文件、最近目录、最近搜索结果、最近建议和批量标签历史。
- InnerBrain 本地内脑第一版：把既有自然语言规则包装为 `legacy_rule`，并用内置 seed 样本和 `data/inner-brain/training/*.jsonl` 运行态样本做轻量相似度识别，输出 `intent`、`slots`、`confidence`、`missing`、`source`、`reason` 和执行策略。
- 本地自然语言意图层，可处理常见中文表达，包括问候、助手身份询问、知识库/最近上下文/目录任务和明确点名的桌面 `.lnk` 快捷方式删除；InnerBrain 高置信度命中时仍交给 `JarvisAgent` 执行。
- LLM 外脑 Router 第一版，支持 `off`、`fake`、`openai` 和 `openai-compatible`、完整 `/v1/responses` URL 归一化、provider 与 Agent 双层命令白名单、`/llm-context-preview`、`/llm-smoke` 配置验证，并记录、汇总 provider 返回的 token 用量。
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
python src/app.py --once "/inner-brain-status"
python src/app.py --once "/inner-brain-preview 麻烦看一下知识库摘要"
python src/app.py --once "/llm-status"
python src/app.py --once "/llm-context-preview"
python src/app.py --once "/llm-smoke"
python src/app.py --once "查看最近上下文"
python src/app.py --once "总结知识库"
python src/app.py --once "早上好"
python src/app.py --once "你叫什么名字"
```

启动桌面助手：

```powershell
jarvis-lite-desktop
```

运行测试：

```powershell
python -m unittest discover -s tests -v
```

## Windows 安装和升级

当前版本：`0.1.2`。

Windows 打包产物由 `scripts/build_windows_installer.py` 生成到项目外的 `..\jarvis-lite-dist\JarvisLiteSetup.exe`，不提交到 Git。已经安装过旧版时，默认直接运行新安装包做覆盖安装：

- 安装脚本会先关闭正在运行的 `JarvisLite.exe`。
- 新版 `JarvisLite.exe` 和 `uninstall.cmd` 会覆盖 `%LOCALAPPDATA%\Programs\Jarvis Lite` 中的旧程序文件。
- 桌面快捷方式、开始菜单快捷方式和当前用户卸载注册表会重新写入，卸载信息中的 `DisplayVersion` 使用当前版本。
- `%LOCALAPPDATA%\Jarvis Lite` 用户数据目录不会被删除；卸载脚本也会保留该目录。
- 安装完成弹窗会显示 `Jarvis Lite <版本号> installation finished`，用于确认新安装包已经生效；本轮测试包为 `0.1.2`。

建议安装前先退出正在运行的桌面助手。只有在安装目录、快捷方式或卸载注册表已经损坏时，才需要先执行卸载再安装；正常升级优先覆盖安装。

```powershell
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
```

## LLM 外脑配置

默认不开启 LLM 外脑，本地命令、身份、InnerBrain、本地知识库问答仍然优先处理。只有本地无法处理的普通输入，才会进入 LLM Router；LLM 返回的是结构化意图，实际命令仍由 `JarvisAgent` 执行，并由 Agent 再按同一命令白名单校验。进入 LLM fallback 时，Jarvis Lite 会带上记忆摘要、最近资料/目录、最近搜索结果和可执行的下一步建议，帮助模型稳定生成本地命令建议。

`/inner-brain-status` 会展示 InnerBrain 是否启用 legacy 规则、seed/runtime 样本数量、置信度阈值和运行态训练目录。`/inner-brain-preview 文本` 会只预览该文本被识别出的策略、意图、来源、置信度、槽位和命令，不执行任何本地动作；例如预览桌面快捷方式删除表达时不会删除 `.lnk` 文件。

真实 provider 的 instructions 会列出可返回的 Jarvis Lite 命令白名单，例如 `/kb-summary`、`/ask 问题`、`/read 文件名` 和 `/tag 文件名 标签...`。模型不得返回列表之外的命令；参数不确定时应返回澄清问题。

```powershell
$env:JARVIS_LITE_LLM_PROVIDER = "off"     # off | fake | openai | openai-compatible
$env:JARVIS_LITE_LLM_MODEL = "按 provider 当前可用模型填写"
$env:JARVIS_LITE_LLM_API_KEY = "..."
$env:JARVIS_LITE_LLM_BASE_URL = ""        # openai-compatible 必填，可填 /v1 或完整 /v1/responses URL
$env:JARVIS_LITE_LLM_FAKE_RESPONSE = '{"type":"answer","answer":"测试回答"}'
python src/app.py --once "/llm-status"
python src/app.py --once "/llm-context-preview"
python src/app.py --once "/llm-smoke 请用一句话确认连接可用"
python src/app.py --once "/llm-usage"
python src/app.py --once "/llm-config-example openai"
```

`openai-compatible` 适用于提供 OpenAI Responses API 兼容端点的合法网关，使用 `base_url + api_key + model` 接入。`JARVIS_LITE_LLM_BASE_URL` 可以填写 SDK 需要的 base URL（通常到 `/v1`），也可以直接粘贴完整 Responses URL（例如完整路径到 `/v1/responses`），Jarvis Lite 调用 SDK 时会自动归一化为 base URL。provider 返回 usage 时，Jarvis Lite 会把 `input_tokens`、`output_tokens` 和 `total_tokens` 记录到 `logs/jarvis.log`。

`/llm-status` 会做本地配置诊断：例如缺少 `JARVIS_LITE_LLM_MODEL`、`JARVIS_LITE_LLM_API_KEY`、`JARVIS_LITE_LLM_BASE_URL` 或 provider 名称不支持时，会直接列出配置问题，不会打印 API key 内容。状态会显示 API key 是否已配置、当前配置是否会触发网络调用；配置了完整 `/v1/responses` URL 时，状态会同时显示原始 Base URL 和 SDK 实际使用的 Base URL。

`/llm-context-preview` 会预览普通输入进入 LLM fallback 时携带的本地上下文，不调用 provider、不触发网络请求，适合在真实调用前检查最近资料、最近搜索结果和下一步建议是否符合预期。

`/llm-smoke [prompt]` 会强制调用当前 LLM Router 做一次配置验证；它只展示模型返回的结构化意图，不会执行模型给出的命令建议。provider 返回 usage 时，仍会写入本地 `logs/jarvis.log`，之后可用 `/llm-usage` 汇总。

`/llm-usage` 会从本地 `logs/jarvis.log` 汇总 provider/model 维度的 token 用量，不需要真实 API key，也不会触发网络请求。

`/llm-config-example [provider]` 会输出 PowerShell 环境变量配置模板，支持 `off`、`fake`、`openai` 和 `openai-compatible`，`qwen` / `gemini` 会先映射到兼容端点模板；模板只显示占位符，不读取或保存真实 API key，并提示兼容端点可填写完整 `/v1/responses` URL。

当前真实 provider 先接入 OpenAI Responses API 和 OpenAI-compatible Responses 端点；Gemini、Qwen 会沿用同一 Router/Provider 接口继续扩展。

## 常用命令

```text
/help
/status
/inner-brain-status
/inner-brain-preview 文本
/llm-status
/llm-context-preview
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
