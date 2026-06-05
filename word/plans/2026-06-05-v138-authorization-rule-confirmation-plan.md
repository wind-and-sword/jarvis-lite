# v138：授权规则确认固化与撤销第一阶段实施计划

> 日期：2026-06-05
> 执行者：Codex
> 说明：本文承接 v137 应用别名确认固化与撤销第一阶段，把授权规则候选推进到显式确认固化与撤销闭环。

## 目标

- `/config-candidate-apply 编号` 作用于授权规则候选时继续返回确认草稿，并提示 `/config-candidate-confirm 编号`。
- `/config-candidate-confirm 编号` 支持活跃授权规则候选，写入 `config/authorization.local.json`，并把候选标记为已固化。
- `/config-candidate-undo 编号` 支持历史中的已固化授权规则候选，删除对应规则，并把候选恢复为活跃。
- `/authorization-status` 和 `/config-manager-status` 只读展示本地授权规则数量；授权规则确认和撤销本身不触发任何桌面动作。

## 非目标

- 不确认固化偏好、API key、联系人目标查找、消息发送规则或自动执行规则。
- 不改变 `authorize_intent_execution()` 的既有执行决策，不让本阶段规则自动放行或阻断命令。
- 不点击、不输入、不切换窗口、不启动应用。
- 不把确认/撤销命令加入 LLM 白名单，不让普通聊天或外脑自动写入授权规则。

## 实施步骤

1. 在 `tests/test_authorization.py` 增加 RED：授权规则 JSON 可写入、读取、删除、计数和状态展示。
2. 在 `tests/test_memory_config_candidates.py` 增加 RED：授权规则候选确认后写入配置、标记已固化；撤销后删除规则并恢复候选。
3. 在 `tests/test_memory_config_manager.py` 增加 RED：配置管家展示授权规则数量。
4. 在 `tests/test_agent.py` 增加 RED：Agent 接入授权规则确认/撤销，`/authorization-status` 可观察本地规则。
5. 在 `tests/test_llm.py` 和 `tests/test_project_metadata.py` 增加 RED：确认/撤销命令仍不进入 LLM 命令建议，版本提升到 `0.133.0`。
6. 新增 `authorization_rules.py`，集中处理 `config/authorization.local.json` 的读写、解析、展示、删除和计数。
7. 更新 `authorization.py`，让 `describe_authorization_status(paths)` 可选展示本地授权规则；不改变执行决策函数。
8. 更新 `memory_config_candidates.py`，让确认/撤销 helper 支持联系人别名、应用别名和授权规则。
9. 更新 Agent 帮助、状态、版本号、README、PROJECT-PLAN、索引、进度和验证记录。
10. 执行目标测试、相邻回归、全量 unittest、命令行 smoke、源码桌面 smoke、安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 授权规则候选 `微信发消息前需要确认` 经 `/config-candidate-confirm 1` 后写入 `config/authorization.local.json`。
- `/authorization-status` 展示 `本地授权规则：1 条` 和该规则文本，但不改变现有命令执行路径。
- `/config-candidate-history` 展示已固化授权规则，并提示 `/config-candidate-undo 编号`。
- `/config-candidate-undo 1` 删除对应授权规则，并让候选重新出现在 `/config-candidates`。
- 偏好候选仍只给确认草稿或暂不支持真实确认，不写入长期配置。
