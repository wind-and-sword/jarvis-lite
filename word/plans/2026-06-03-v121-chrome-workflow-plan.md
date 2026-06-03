# v121：Chrome 低风险工作流第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v120 自动记忆与配置管家第一阶段，进入 Jarvis Lite 1.0 验收线中的 Chrome 和 Clash Verge 低风险工作流。

## 背景

`0.115.0` 已完成自动记忆与配置管家第一阶段。按照 v108 的推荐落地顺序，下一步进入五个常用应用首批工作流，先从 Chrome 和 Clash Verge 的低风险动作开始。

当前已有 `/apps`、`/app-find` 和 `/app-launch`，能登记、匹配和启动 Chrome，但还不能把 URL 或搜索关键词作为 Chrome 工作流参数传入。本阶段先补齐显式 Chrome 打开网页和搜索能力，不做页面点击、页面读取、截图联动或自然语言自动执行。

## 目标

- 新增 `/chrome-workflow-status`，展示 Chrome 工作流第一阶段边界。
- 新增 `/chrome-open URL`，使用 AppRegistry 中的 Chrome 启动路径打开明确网页。
- 新增 `/chrome-search 关键词`，构造搜索 URL 后使用 Chrome 打开。
- 复用 `config/apps.local.json` 中的 Chrome 路径覆盖。
- 将 Chrome 工作流命令纳入授权层桌面动作集合，避免后续自然语言或 LLM 建议绕过确认边界。
- 项目版本提升到 `0.116.0`。

## 非目标

- 不读取网页内容。
- 不点击页面、输入页面表单或发送浏览器快捷键。
- 不自动截图、OCR 或保存网页资料。
- 不接入自然语言自动打开网页。
- 不在单元测试或默认 smoke 中真实启动 Chrome。

## 文件计划

- 新增 `src/jarvis_lite/chrome_workflow.py`：解析 URL/搜索词、查找 Chrome、执行器注入、生成可读结果。
- 修改 `src/jarvis_lite/agent.py`：接入 `/chrome-workflow-status`、`/chrome-open` 和 `/chrome-search`，补充帮助和 `/status`。
- 修改 `src/jarvis_lite/authorization.py`：把 `/chrome-open`、`/chrome-search` 纳入桌面动作集合。
- 修改 `src/jarvis_lite/automation.py`：更新自动化状态能力列表。
- 修改 `src/jarvis_lite/llm.py`：允许 LLM 建议低风险状态命令 `/chrome-workflow-status`，不允许直接建议打开网页命令。
- 新增 `tests/test_chrome_workflow.py`：覆盖 URL 规范化、搜索 URL 构造、执行器注入、缺失 Chrome 路径和状态文案。
- 修改 `tests/test_agent.py`、`tests/test_authorization.py`、`tests/test_project_metadata.py`、`tests/test_llm.py`：覆盖 Agent 接入、授权边界、版本和白名单。
- 更新 README、PROJECT-PLAN、计划索引、文档索引、进度与验证记录。

## 执行步骤

1. RED：新增 `tests/test_chrome_workflow.py`，验证 Chrome URL 打开、搜索 URL 和状态文案，先确认模块不存在。
2. RED：新增 Agent、Authorization、LLM 和版本测试，确认命令未接入。
3. GREEN：实现 `chrome_workflow.py`，默认执行器使用 `subprocess.Popen([chrome_path, url])`，测试使用注入执行器。
4. GREEN：接入 `JarvisAgent`、授权层、自动化状态、帮助和 LLM 状态命令白名单。
5. 文档同步：版本提升到 `0.116.0`，更新 README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
6. 验证：运行目标测试、相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建、版本化安装包、打包后 exe smoke、静态检查、Markdown 链接检查和密钥扫描。
7. Smoke：运行 `/chrome-workflow-status`；真实 `/chrome-open` 和 `/chrome-search` 因会启动浏览器，默认跳过并记录原因。

## 验收标准

- `/chrome-workflow-status` 输出 Chrome 工作流第一阶段边界。
- `/chrome-open example.com` 会规范化为 `https://example.com` 并传给 Chrome 执行器。
- `/chrome-search Jarvis Lite` 会构造搜索 URL 并传给 Chrome 执行器。
- Chrome 路径缺失时提示配置 `config/apps.local.json`，不触发执行器。
- `/chrome-open` 和 `/chrome-search` 属于授权层桌面动作命令。
- 单元测试不真实启动 Chrome，默认 smoke 不启动浏览器。
