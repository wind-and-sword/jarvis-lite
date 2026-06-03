# v123：QQ/微信准备式工作流第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v122 Clash Verge 低风险工作流第一阶段，继续推进 Jarvis Lite 1.0 验收线中的 QQ/微信准备式工作流。

## 背景

`0.117.0` 已完成 Clash Verge 显式打开和聚焦。按照 v108 的推荐落地顺序，下一步进入 QQ/微信准备式工作流。

QQ 和微信涉及联系人、账号、消息内容和发送动作。第一阶段只建立“准备式”边界：可以显式打开应用、聚焦已有窗口、生成消息准备单，但不查找真实联系人、不点击、不输入、不发送消息，也不接入自然语言自动执行。

## 目标

- 新增 `/messaging-workflow-status`，展示 QQ/微信准备式工作流第一阶段边界。
- 新增 `/qq-open` 与 `/wechat-open`，使用 AppRegistry 中的路径显式打开应用。
- 新增 `/qq-focus` 与 `/wechat-focus`，只聚焦当前已经存在的 QQ/微信窗口；无窗口时提示先显式打开。
- 新增 `/qq-prepare-message 联系人 => 消息` 与 `/wechat-prepare-message 联系人 => 消息`，生成“未发送”的消息准备单。
- 复用 `config/apps.local.json` 中的 `qq.path` 和 `wechat.path` 覆盖。
- 将 QQ/微信打开和聚焦动作纳入授权层桌面动作集合；LLM 只允许建议状态命令，不允许直接建议打开、聚焦或准备消息。
- 项目版本提升到 `0.118.0`。

## 非目标

- 不查找真实联系人。
- 不点击、不输入、不发送消息。
- 不读取 QQ/微信界面内容。
- 不保存联系人别名或免确认规则。
- 不接入自然语言自动执行。
- 不在单元测试或默认 smoke 中真实启动 QQ/微信或切换窗口。

## 文件计划

- 新增 `src/jarvis_lite/messaging_workflow.py`：输出状态、启动应用、聚焦已有窗口、解析消息准备单，支持执行器和窗口快照注入。
- 修改 `src/jarvis_lite/agent.py`：接入 `/messaging-workflow-status`、QQ/微信 open/focus/prepare 命令，补充帮助和 `/status`。
- 修改 `src/jarvis_lite/authorization.py`：把 QQ/微信 open/focus 纳入桌面动作集合。
- 修改 `src/jarvis_lite/automation.py`：更新自动化状态能力列表。
- 修改 `src/jarvis_lite/llm.py`：允许 LLM 建议低风险状态命令 `/messaging-workflow-status`，不允许直接建议消息动作命令。
- 新增 `tests/test_messaging_workflow.py`：覆盖状态、启动执行器注入、缺失路径、聚焦执行器注入、无窗口提示和消息准备单解析。
- 修改 `tests/test_agent.py`、`tests/test_authorization.py`、`tests/test_project_metadata.py`、`tests/test_llm.py`：覆盖 Agent 接入、授权边界、版本和白名单。
- 更新 README、PROJECT-PLAN、计划索引、文档索引、进度与验证记录。

## 执行步骤

1. RED：新增 `tests/test_messaging_workflow.py`，验证 QQ/微信打开、聚焦、准备单和边界文案，先确认模块不存在。
2. RED：新增 Agent、Authorization、LLM 和版本测试，确认命令未接入。
3. GREEN：实现 `messaging_workflow.py`，默认启动复用 AppRegistry，聚焦复用 WindowState，测试使用注入执行器和快照。
4. GREEN：接入 `JarvisAgent`、授权层、自动化状态、帮助和 LLM 状态命令白名单。
5. 文档同步：版本提升到 `0.118.0`，更新 README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
6. 验证：运行目标测试、相邻回归、全量 `unittest`、源码桌面 smoke、安装包构建、版本化安装包、打包后 exe smoke、静态检查、Markdown 链接检查和密钥扫描。
7. Smoke：运行 `/messaging-workflow-status`；真实 QQ/微信 open/focus 因会启动或切换本机应用，默认跳过并记录原因。

## 验收标准

- `/messaging-workflow-status` 输出 QQ/微信准备式工作流第一阶段边界。
- `/qq-open` 与 `/wechat-open` 使用对应 AppRegistry 路径启动，单元测试不启动真实应用。
- `/qq-focus` 与 `/wechat-focus` 聚焦已存在窗口，单元测试不真实切换窗口。
- `/qq-prepare-message 联系人 => 消息` 与 `/wechat-prepare-message 联系人 => 消息` 只生成未发送准备单。
- 缺少路径、缺少窗口、缺少联系人或缺少消息时返回可读错误。
- QQ/微信 open/focus 属于授权层桌面动作命令；LLM 只允许建议 `/messaging-workflow-status`。
