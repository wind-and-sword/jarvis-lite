# Jarvis Lite

> 日期：2026-05-29
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
- InnerBrain 本地内脑：以 seed/runtime 样本分类器作为自然语言主识别路径，输出 `intent`、`slots`、`confidence`、`missing`、`source`、`reason` 和执行策略；旧自然语言规则只作为 `legacy_fallback` 迁移期兼容兜底，不再是高频自然语言主入口。
- InnerBrain 样本闭环：`/inner-brain-adopt 文本` 可采纳正确识别结果，`/inner-brain-label 文本 => intent [slot=value ...]` 可人工标注 unknown 或误识别样本，`/inner-brain-teach 文本 => /命令` 可把自然语言短句教学为已知命令；当已识别 intent 但缺少关键槽位时，支持下一句自然语言补齐导入路径或桌面快捷方式名称。
- 本地自然语言意图层，可用样本分类器处理问候、助手身份/能力询问、知识库、最近上下文、最近文件、显式文件读取/导入、显式文件打标签、读取编号资料、查看/导入编号最近文件、查看编号搜索结果、查看/执行编号建议、当前资料/结果打标签、编号资料/搜索结果打标签、标签组读取与批量标签预览、常用目录打开/整理、最近目录打开/整理、日报、更新、经验记录/搜索/建议、确认/取消执行、联网搜索、联网搜索后续来源处理和明确点名的桌面 `.lnk` 快捷方式删除；InnerBrain 高置信度命中时仍交给 `JarvisAgent` 执行。
- LLM 外脑 Router 第一版，支持 `off`、`fake`、`openai`、`openai-compatible`、`qwen` 和 `gemini`、完整 `/v1/responses` URL 归一化、provider 与 Agent 双层命令白名单、`/llm-config-init`、`/llm-config-set`、`/llm-config-check`、`/llm-context-preview`、`/llm-smoke` 运行时配置验证，并记录、汇总 provider 返回的 token 用量。
- SearchRouter 联网搜索第一版，支持 `off`、`fake` 和 `tavily`，通过 `config/search.local.json` 本地配置搜索 provider，并提供 `/search-config-set` 写入、`/search-config-check` 只读检查和 `/search-smoke` 连通性测试；搜索由 `JarvisAgent` 显式调用并展示 URL 来源，搜索结果会进入最近上下文和 LLM context，`/search-summary 关键词` 与“联网查一下...并总结”会先搜索再把来源交给 LLM 外脑总结；最近联网搜索还支持按编号查看来源、比较来源、保存摘要到 `word/` 和导入摘要到 `data/`。
- 桌面小助手、助手面板、托盘、快捷命令、主题、尺寸、开机启动、更新入口，以及外脑/联网搜索配置面板；桌面写入 API key 时会用脱敏提交，不把真实 key 显示到 transcript 或会话历史。
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
python src/app.py --once "/inner-brain-adopt 帮我看看资料库状态"
python src/app.py --once "/inner-brain-label 可以看看资料库吗 => knowledge.status command=/kb"
python src/app.py --once "/inner-brain-teach 可以看看资料库吗 => /kb"
python src/app.py --once "以后我说“看看资料库”就是 /kb"
python src/app.py --once "/llm-status"
python src/app.py --once "/llm-context-preview"
python src/app.py --once "/llm-smoke"
python src/app.py --once "/search-status"
python src/app.py --once "/search Python 版本"
python src/app.py --once "/search-summary Python 版本"
python src/app.py --once "/search-open 1"
python src/app.py --once "/search-compare"
python src/app.py --once "/search-save-summary python-version"
python src/app.py --once "/search-import-summary"
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

当前版本：`0.8.0`。

Windows 打包产物由 `scripts/build_windows_installer.py` 生成到项目外的 `..\jarvis-lite-dist\JarvisLiteSetup.exe`，不提交到 Git。已经安装过旧版时，默认直接运行新安装包做覆盖安装：

- 安装脚本会先关闭正在运行的 `JarvisLite.exe`。
- 新版 `JarvisLite.exe` 和 `uninstall.cmd` 会覆盖 `%LOCALAPPDATA%\Programs\Jarvis Lite` 中的旧程序文件。
- 桌面快捷方式、开始菜单快捷方式和当前用户卸载注册表会重新写入，卸载信息中的 `DisplayVersion` 使用当前版本。
- `%LOCALAPPDATA%\Jarvis Lite` 用户数据目录不会被删除；卸载脚本也会保留该目录。
- 安装完成弹窗会显示 `Jarvis Lite <版本号> installation finished`，用于确认新安装包已经生效；本轮测试包为 `0.8.0`，包含 InnerBrain 样本分类器优先迁移、联网搜索入口、SearchRouter + LLMRouter 搜索总结组合流程、联网搜索后续来源处理、多轮澄清 v1 收口、外脑 provider 配置闭环 v1、运行态配置初始化 v1、本地配置检查 v1、本地配置写入 v1、连通性诊断 v1，以及桌面配置面板 v1：面板可填写 LLM/Search provider 配置并执行写入、检查和 smoke 测试，写入 API key 时不会把真实 key 显示到聊天记录。

建议安装前先退出正在运行的桌面助手。只有在安装目录、快捷方式或卸载注册表已经损坏时，才需要先执行卸载再安装；正常升级优先覆盖安装。

```powershell
.\.venv\Scripts\python.exe scripts\build_windows_installer.py
```

## LLM 外脑配置

默认不开启 LLM 外脑，本地命令、身份、InnerBrain、本地知识库问答仍然优先处理。只有本地无法处理的普通输入，才会进入 LLM Router；LLM 返回的是结构化意图，实际命令仍由 `JarvisAgent` 执行，并由 Agent 再按同一命令白名单校验。进入 LLM fallback 时，Jarvis Lite 会带上记忆摘要、最近资料/目录、最近搜索结果和可执行的下一步建议，帮助模型稳定生成本地命令建议。

`/inner-brain-status` 会展示 InnerBrain 样本分类器优先状态、`legacy_fallback` 迁移期兼容状态、seed/runtime 样本数量、置信度阈值和运行态训练目录。`/inner-brain-preview 文本` 会只预览该文本被识别出的策略、意图、来源、置信度、槽位和命令，不执行任何本地动作；例如预览桌面快捷方式删除表达时不会删除 `.lnk` 文件。`/inner-brain-adopt 文本` 会把当前可识别的非 `unknown` 结果保存到 `data/inner-brain/training/runtime.jsonl`，重复样本不重复写入。`/inner-brain-label 文本 => intent [slot=value ...]` 用于人工标注 `unknown` 或误识别输入，例如 `command=/kb`、`items=比特浏览器`、`missing=source`。`/inner-brain-teach 文本 => /命令` 以及“以后我说“文本”就是 /命令”用于把短句绑定到已知命令，例如 `/kb`、`/kb-summary`、`/daily-report`；保存动作本身不会执行识别出的命令。

真实 provider 的 instructions 会列出可返回的 Jarvis Lite 命令白名单，例如 `/kb-summary`、`/ask 问题`、`/read 文件名`、`/tag 文件名 标签...`、`/search-summary 关键词`、`/search-open 编号`、`/search-compare`、`/search-save-summary [文件名]`、`/search-import-summary [文件名]`、`/llm-smoke [prompt]`、`/llm-config-init [provider]`、`/llm-config-set key=value ...`、`/llm-config-check`、`/search-smoke [query]`、`/search-config-init [provider]`、`/search-config-set key=value ...` 和 `/search-config-check`。模型不得返回列表之外的命令；参数不确定时应返回澄清问题。

推荐用本地配置文件启用外脑。源码运行时配置文件是 `config/llm.local.json`；安装版配置文件位于 `%LOCALAPPDATA%\Jarvis Lite\config\llm.local.json`。`config/llm.example.json` 是可提交模板，真实 `llm.local.json` 已加入 `.gitignore`，不进入 Git 历史。可执行 `/llm-config-init qwen`、`/llm-config-init gemini` 或直接说“生成外脑配置”来生成不含真实 API key 的本机草稿；也可执行 `/llm-config-set provider=qwen model=模型名 base_url=https://.../v1/responses api_key=你的key` 直接写入本机配置。写入后可执行 `/llm-config-check` 或直接说“检查外脑配置”做只读检查，不会发起网络请求；确认配置完整后可执行 `/llm-smoke 请用一句话确认连接可用` 做真实连通性测试。`JarvisAgent` 启动时会读取该文件，已经运行中的桌面助手可说“开启外脑”或执行 `/llm-enable` 重新加载配置并查看状态；`/llm-smoke` 每次执行前也会重新读取当前本地配置。

桌面助手面板也提供外脑配置区，可填写 provider、model、base_url 和 api_key，并点击“写入外脑”“检查”“测试”。写入动作复用 `/llm-config-set`，但面板只显示“api_key 已隐藏”，不会把真实 key 写入聊天 transcript 或会话历史。

```json
{
  "provider": "openai-compatible",
  "model": "<兼容端点模型名>",
  "base_url": "<兼容端点 base_url 或完整 /v1/responses URL>",
  "api_key": "<你的 API key>",
  "fake_response": ""
}
```

`provider` 可填写 `off`、`fake`、`openai`、`openai-compatible`、`qwen` 或 `gemini`。`qwen` / `gemini` 是 provider alias，实际会走 OpenAI-compatible adapter；`base_url`、`model` 和 API key 以对应平台控制台为准。`/llm-status` 和 `/llm-enable` 会同时显示 `Provider` 和 `Adapter`，便于确认 alias 已生效。

环境变量仍然可用，并且会覆盖本地配置文件中的同名字段，适合临时调试：

```powershell
$env:JARVIS_LITE_LLM_PROVIDER = "off"     # off | fake | openai | openai-compatible | qwen | gemini
$env:JARVIS_LITE_LLM_MODEL = "按 provider 当前可用模型填写"
$env:JARVIS_LITE_LLM_API_KEY = "..."
$env:JARVIS_LITE_LLM_BASE_URL = ""        # openai-compatible 必填，可填 /v1 或完整 /v1/responses URL
$env:JARVIS_LITE_LLM_FAKE_RESPONSE = '{"type":"answer","answer":"测试回答"}'
python src/app.py --once "/llm-status"
python src/app.py --once "/llm-context-preview"
python src/app.py --once "/llm-smoke 请用一句话确认连接可用"
python src/app.py --once "/llm-usage"
python src/app.py --once "/llm-config-example openai"
python src/app.py --once "/llm-config-init qwen"
python src/app.py --once "/llm-config-set provider=qwen model=qwen-plus base_url=https://example.com/v1/responses api_key=你的key"
python src/app.py --once "/llm-config-check"
python src/app.py --once "/llm-enable"
```

`openai-compatible` 适用于提供 OpenAI Responses API 兼容端点的合法网关，使用 `base_url + api_key + model` 接入。`JARVIS_LITE_LLM_BASE_URL` 可以填写 SDK 需要的 base URL（通常到 `/v1`），也可以直接粘贴完整 Responses URL（例如完整路径到 `/v1/responses`），Jarvis Lite 调用 SDK 时会自动归一化为 base URL。provider 返回 usage 时，Jarvis Lite 会把 `input_tokens`、`output_tokens` 和 `total_tokens` 记录到 `logs/jarvis.log`。

`/llm-status` 会做本地配置诊断：例如缺少模型、API key、Base URL 或 provider 名称不支持时，会直接列出配置问题，不会打印 API key 内容。状态会显示配置来源、API key 是否已配置、当前配置是否会触发网络调用；配置了完整 `/v1/responses` URL 时，状态会同时显示原始 Base URL 和 SDK 实际使用的 Base URL。

`/llm-config-check` 会重新读取当前 `config/llm.local.json` 和环境变量覆盖，只展示配置路径、本地配置是否存在、Provider/Adapter、模型、Base URL、API key 状态和配置问题，不发起网络请求，也不会显示真实 API key。它适合在 `/llm-config-init` 生成草稿并填入 key 后，先确认配置结构再执行 `/llm-enable` 或 `/llm-smoke`。

`/llm-config-set key=value ...` 会创建或更新 `config/llm.local.json`，支持字段 `provider`、`model`、`base_url`、`api_key` 和 `fake_response`；未指定字段保持不变。命令会校验 provider，遇到未知字段、未知 provider 或损坏 JSON 时不会写入部分配置。用户直接说“设置外脑配置”会得到用法模板，不会从自然语言中猜测 API key 或 URL。响应和日志只显示变更字段，不显示真实 API key。

`/llm-enable` 会确保运行态目录里存在 `config/llm.example.json`，展示 `config/llm.local.json` 路径，并重新加载当前会话的 LLM Router。用户说“开启外脑”会走同一入口；如果本地配置已写好，会立即显示已启用状态。

`/llm-config-init [provider]` 会生成 `config/llm.local.json` 草稿，默认 `openai-compatible`，支持 `off`、`fake`、`openai`、`openai-compatible`、`qwen` 和 `gemini`。草稿中的 `api_key`、`model` 和 `base_url` 默认为空，不会触发真实网络调用；已有本地配置时不会覆盖，也不会打印已有 API key。

`/llm-context-preview` 会预览普通输入进入 LLM fallback 时携带的本地上下文，不调用 provider、不触发网络请求，适合在真实调用前检查最近资料、最近搜索结果和下一步建议是否符合预期。

`/llm-smoke [prompt]` 会重新读取当前 `config/llm.local.json`，再强制调用 LLM Router 做一次配置验证；它可能触发真实 provider 调用，只展示模型返回的结构化意图，不会执行模型给出的命令建议。provider 返回 usage 时，仍会写入本地 `logs/jarvis.log`，之后可用 `/llm-usage` 汇总。用户也可以直接说“测试外脑连接”进入同一入口。

`/llm-usage` 会从本地 `logs/jarvis.log` 汇总 provider/model 维度的 token 用量，不需要真实 API key，也不会触发网络请求。

`/llm-config-example [provider]` 会输出 PowerShell 环境变量配置模板，支持 `off`、`fake`、`openai`、`openai-compatible`、`qwen` 和 `gemini`；模板只显示占位符，不读取或保存真实 API key，并提示兼容端点可填写完整 `/v1/responses` URL。

当前真实 provider 先接入 OpenAI Responses API 和 OpenAI-compatible Responses 端点；Gemini、Qwen 先以 alias 方式复用兼容端点 adapter，后续如确有必要再接原生 SDK。

## 联网搜索配置

联网搜索默认关闭，和 LLM 外脑互补：搜索负责获取当前网页来源、标题和摘要，LLM 外脑负责在 Agent 提供来源后做总结、比较和自然表达。Jarvis Lite 不让 LLM 自由浏览；何时搜索、展示哪些来源、是否继续交给 LLM，仍由 `JarvisAgent` 控制。

推荐用本地配置文件启用搜索。源码运行时配置文件是 `config/search.local.json`；安装版配置文件位于 `%LOCALAPPDATA%\Jarvis Lite\config\search.local.json`。`config/search.example.json` 是可提交模板，真实 `search.local.json` 已加入 `.gitignore`。可执行 `/search-config-init tavily` 或直接说“生成联网搜索配置”来生成不含真实 API key 的本机草稿；也可执行 `/search-config-set provider=tavily api_key=你的key max_results=3` 直接写入本机配置。写入后可执行 `/search-config-check` 或直接说“检查联网搜索配置”做只读检查，不会发起网络请求；确认配置完整后可执行 `/search-smoke Python 版本` 做真实连通性测试且不污染最近搜索上下文。当前真实 provider 使用 Tavily Python SDK（官方文档：https://docs.tavily.com/sdk/python/quick-start）。

桌面助手面板也提供联网搜索配置区，可填写 provider、api_key、base_url 和 max_results，并点击“写入搜索”“检查”“测试”。写入动作复用 `/search-config-set`，同样以脱敏显示方式隐藏真实 API key。

```json
{
  "provider": "tavily",
  "api_key": "<你的搜索 API key>",
  "base_url": "",
  "max_results": 5,
  "fake_results": []
}
```

环境变量可覆盖本地配置文件中的同名字段：

```powershell
$env:JARVIS_LITE_SEARCH_PROVIDER = "tavily"   # off | fake | tavily
$env:JARVIS_LITE_SEARCH_API_KEY = "..."
$env:JARVIS_LITE_SEARCH_BASE_URL = ""         # 通常留空；自定义 Tavily 兼容入口时填写
$env:JARVIS_LITE_SEARCH_MAX_RESULTS = "5"
python src/app.py --once "/search-status"
python src/app.py --once "/search Python 版本"
python src/app.py --once "/search-config-init tavily"
python src/app.py --once "/search-config-set provider=tavily api_key=你的key max_results=3"
python src/app.py --once "/search-config-check"
python src/app.py --once "/search-smoke Python 版本"
python src/app.py --once "/search-enable"
```

`/search-status` 会展示 provider、配置来源、API key 是否已配置、最大结果数和当前配置是否会触发网络调用，不会打印 API key。`/search-enable` 会确保运行态目录里有 `config/search.example.json`，展示 `config/search.local.json` 路径，并重新加载当前会话的 SearchRouter。`/search-smoke [query]` 会重新读取当前搜索本地配置，执行一次 provider 连通性测试，默认查询 `Python 版本`，成功时展示返回来源条数和预览，失败时展示可读错误；它不会写入最近联网搜索上下文，用户也可以直接说“测试联网搜索连接”进入同一入口。`/search 关键词` 会执行联网搜索并返回编号来源、URL 和摘要，同时把结果写入最近上下文；自然语言“联网查一下 Python 版本”会走同一入口。`/search-summary 关键词` 和“联网查一下 Python 版本并总结”会先执行搜索，再把最近联网搜索来源放入 LLM context，请外脑基于来源生成总结；LLM 未启用时仍返回搜索来源并提示启用方式。搜索后可继续用 `/search-open 编号` 查看某条来源 URL（只返回 URL，不启动浏览器）、`/search-compare` 让 LLM 外脑比较最近来源、`/search-save-summary [文件名]` 保存摘要到 `word/`，或 `/search-import-summary [文件名]` 把摘要写入 `data/` 进入知识库。

`/search-config-init [provider]` 会生成 `config/search.local.json` 草稿，默认 `tavily`，支持 `off`、`fake` 和 `tavily`。草稿中的 `api_key` 为空，不会触发真实网络调用；已有本地配置时不会覆盖，也不会打印已有 API key。

`/search-config-check` 会重新读取当前 `config/search.local.json` 和环境变量覆盖，只展示配置路径、本地配置是否存在、Provider、Base URL、Max results、API key 状态和配置问题，不发起网络请求，也不会显示真实 API key。它适合在 `/search-config-init` 生成草稿并填入 key 后，先确认配置结构再执行 `/search-enable` 或 `/search 关键词`。

`/search-config-set key=value ...` 会创建或更新 `config/search.local.json`，支持字段 `provider`、`api_key`、`base_url`、`max_results` 和 `fake_results`；未指定字段保持不变。命令会校验 provider 和 `max_results`，遇到未知字段、非法值或损坏 JSON 时不会写入部分配置。用户直接说“设置联网搜索配置”会得到用法模板，不会从自然语言中猜测 API key。响应和日志只显示变更字段，不显示真实 API key。

## 常用命令

```text
/help
/status
/inner-brain-status
/inner-brain-preview 文本
/inner-brain-adopt 文本
/inner-brain-label 文本 => intent [slot=value ...]
/inner-brain-teach 文本 => /命令
/llm-status
/llm-context-preview
/llm-smoke [prompt]
/llm-usage
/llm-config-example [provider]
/llm-config-init [provider]
/llm-config-set key=value ...
/llm-config-check
/search-status
/search-enable
/search-config-example [provider]
/search-config-init [provider]
/search-config-set key=value ...
/search-config-check
/search-smoke [query]
/search 关键词
/search-summary 关键词
/search-open 编号
/search-compare
/search-save-summary [文件名]
/search-import-summary [文件名]
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
