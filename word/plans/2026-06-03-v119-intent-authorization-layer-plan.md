# v119：意图授权层第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v118 应用启动自动化第一阶段，开始推进 Jarvis Lite 1.0 验收线中的意图授权层。

## 目标

`0.114.0` 建立意图授权层第一阶段，让 Jarvis Lite 能在自然语言理解、LLM 外脑命令建议和桌面动作执行之间输出可测试的执行决策。该阶段先做策略归类、状态可观察和 LLM 桌面动作降级，不改变显式 slash command 的直接执行体验，也不新增自然语言自动桌面操作。

## 范围

- 新增 `src/jarvis_lite/authorization.py`：
  - 定义授权动作：直接执行、准备后确认、追问补充、拒绝和降级。
  - 定义意图来源：显式命令、自然语言、LLM 外脑、建议确认。
  - 定义桌面动作命令集合：`/app-launch`、`/window-focus`、`/hotkey`、`/mouse-click`、`/type-text`、`/screen-ocr`、`/screenshot`。
  - 根据命令来源、是否已确认、是否缺少槽位和置信度输出决策与原因。
  - 提供 `describe_authorization_status()` 只读状态文本。
- 在 `JarvisAgent` 新增 `/authorization-status`：
  - 展示授权层第一阶段的策略、命令来源、桌面动作范围和确认规则。
  - 加入 `TEACHABLE_INNER_BRAIN_COMMAND_INTENTS` 和 `/help`。
  - 在 `/status` 中增加授权层摘要。
- 在 LLM 外脑命令执行路径中接入授权判断：
  - LLM 返回桌面动作命令时，输出授权层降级说明，不进入实际桌面动作执行。
  - 既有 LLM 白名单命令仍按原逻辑执行。
- 更新版本、README、PROJECT-PLAN、计划索引、文档索引、进度记录和验证记录到 `0.114.0`。

## 非目标

- 不新增免确认规则持久化。
- 不引入联系人、账号、凭据或消息发送工作流。
- 不让自然语言直接启动应用、切换窗口、点击、输入文本或发送快捷键。
- 不改变显式 slash command 的现有执行行为。
- 不删除或绕过既有建议命令确认流程。

## 文件计划

- 修改 `pyproject.toml`：版本提升到 `0.114.0`。
- 修改 `src/jarvis_lite/__init__.py`：版本提升到 `0.114.0`。
- 新增 `src/jarvis_lite/authorization.py`：实现授权决策模型、桌面动作识别和状态描述。
- 修改 `src/jarvis_lite/agent.py`：接入 `/authorization-status`、状态摘要、帮助文案和 LLM 桌面动作降级。
- 新增 `tests/test_authorization.py`：覆盖授权决策、桌面动作识别、状态文本和缺失槽位处理。
- 修改 `tests/test_agent.py`：覆盖 `/authorization-status`、`/status` 摘要、LLM 桌面动作降级和版本更新测试夹具。
- 修改 `tests/test_project_metadata.py`：版本提升到 `0.114.0`。
- 更新 `README.md`、`word/PROJECT-PLAN.md`、`word/plans/README.md`、`word/文档索引.md`、`word/progress/2026-06-03.md`、`verification.md` 和 `verification/2026-06/*`。

## 执行步骤

1. RED：新增授权模块单元测试，先确认 `jarvis_lite.authorization` 不存在。
2. GREEN：实现授权决策模型、桌面动作命令集合和状态描述。
3. RED：新增 Agent `/authorization-status`、`/status` 和 LLM 桌面动作降级测试，先确认命令未接入。
4. GREEN：接入 `JarvisAgent` 命令、帮助、状态摘要和 LLM 命令授权判断。
5. RED/GREEN：版本一致性测试更新到 `0.114.0`。
6. 文档同步：更新当前方案、索引、README、进度和验证记录。
7. 回归：运行 `tests.test_authorization`、相关 Agent 测试、`tests.test_project_metadata` 和全量 `unittest`。
8. Smoke：运行 `/authorization-status` 与 LLM 桌面动作降级 smoke；真实桌面动作 smoke 继续跳过并记录原因。
9. 打包验证：运行 Windows 安装包构建、版本化复制、安装脚本/SED/版本资源检查和打包后 smoke。

## 验收标准

- `/authorization-status` 能说明直接执行、准备确认、追问、拒绝和降级的决策边界。
- 授权模块能把显式 `/hotkey` 判为直接执行，把自然语言或 LLM 的 `/hotkey` 判为准备确认或降级。
- LLM 外脑返回 `/hotkey`、`/mouse-click`、`/type-text`、`/window-focus` 或 `/app-launch` 时不会触发真实桌面动作。
- 既有建议命令确认流程仍需要“确认执行”后才调用 `self.handle(command)`。
- 既有显式 slash command 的单元测试保持通过。
