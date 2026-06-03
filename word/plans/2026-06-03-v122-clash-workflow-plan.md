# v122：Clash Verge 低风险工作流第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v121 Chrome 低风险工作流第一阶段，继续推进 Jarvis Lite 1.0 验收线中的常用应用低风险工作流。

## 背景

`0.116.0` 已完成 Chrome 显式打开网页和搜索。按照 v108 的推荐落地顺序，下一步进入 Clash Verge 低风险工作流。

Clash Verge 涉及系统代理、节点、规则和网络路由配置，直接切换会影响用户当前网络环境。本阶段只提供显式打开和聚焦代理面板，不修改代理状态、不切换节点、不点击界面、不输入内容，也不接入自然语言自动执行。

## 目标

- 新增 `/clash-workflow-status`，展示 Clash Verge 工作流第一阶段边界。
- 新增 `/clash-open`，使用 AppRegistry 中的 Clash Verge 启动路径打开代理面板。
- 新增 `/clash-focus`，只聚焦当前已经存在的 Clash Verge 窗口；无窗口时提示先显式打开。
- 复用 `config/apps.local.json` 中的 `clash_verge.path` 覆盖。
- 将 Clash 工作流动作纳入授权层桌面动作集合，避免 LLM 或后续自然语言路径绕过确认边界。
- 项目版本提升到 `0.117.0`。

## 非目标

- 不切换节点。
- 不开关系统代理。
- 不修改 Clash Verge 配置。
- 不点击、不输入、不发送快捷键。
- 不读取 Clash Verge 页面内容。
- 不接入自然语言自动执行。
- 不在单元测试或默认 smoke 中真实启动 Clash Verge 或切换窗口。

## 文件计划

- 新增 `src/jarvis_lite/clash_workflow.py`：输出状态、启动代理面板、聚焦已有窗口，支持执行器和窗口快照注入。
- 修改 `src/jarvis_lite/agent.py`：接入 `/clash-workflow-status`、`/clash-open` 和 `/clash-focus`，补充帮助和 `/status`。
- 修改 `src/jarvis_lite/authorization.py`：把 `/clash-open`、`/clash-focus` 纳入桌面动作集合。
- 修改 `src/jarvis_lite/automation.py`：更新自动化状态能力列表。
- 修改 `src/jarvis_lite/llm.py`：允许 LLM 建议低风险状态命令 `/clash-workflow-status`，不允许直接建议 `/clash-open` 或 `/clash-focus`。
- 新增 `tests/test_clash_workflow.py`：覆盖状态、启动执行器注入、缺失路径、聚焦执行器注入和无窗口提示。
- 修改 `tests/test_agent.py`、`tests/test_authorization.py`、`tests/test_project_metadata.py`、`tests/test_llm.py`：覆盖 Agent 接入、授权边界、版本和白名单。
- 更新 README、PROJECT-PLAN、计划索引、文档索引、进度与验证记录。

## 执行步骤

1. RED：新增 `tests/test_clash_workflow.py`，验证 Clash 启动、聚焦和边界文案，先确认模块不存在。
2. RED：新增 Agent、Authorization、LLM 和版本测试，确认命令未接入。
3. GREEN：实现 `clash_workflow.py`，默认启动复用 AppRegistry，聚焦复用 WindowState，测试使用注入执行器和快照。
4. GREEN：接入 `JarvisAgent`、授权层、自动化状态、帮助和 LLM 状态命令白名单。
5. 文档同步：版本提升到 `0.117.0`，更新 README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
6. 验证：运行目标测试、相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建、版本化安装包、打包后 exe smoke、静态检查、Markdown 链接检查和密钥扫描。
7. Smoke：运行 `/clash-workflow-status`；真实 `/clash-open` 和 `/clash-focus` 因会启动或切换本机应用，默认跳过并记录原因。

## 验收标准

- `/clash-workflow-status` 输出 Clash Verge 工作流第一阶段边界。
- `/clash-open` 会使用 `clash_verge` 注册路径启动代理面板，单元测试不启动真实应用。
- `/clash-focus` 会聚焦已存在的 Clash Verge 窗口，单元测试不真实切换窗口。
- Clash 路径缺失时提示配置 `config/apps.local.json`，不触发执行器。
- 当前无 Clash 窗口时，`/clash-focus` 提示先执行 `/clash-open`。
- `/clash-open` 和 `/clash-focus` 属于授权层桌面动作命令。
