# v139：偏好确认固化与撤销第一阶段实施计划

> 日期：2026-06-05
> 执行者：Codex
> 说明：本文承接 v138 授权规则确认固化与撤销第一阶段，把偏好候选推进到显式确认固化与撤销闭环。

## 目标

- `/config-candidate-apply 编号` 作用于偏好候选时继续返回确认草稿，并提示 `/config-candidate-confirm 编号`。
- `/config-candidate-confirm 编号` 支持活跃偏好候选，写入 `config/preferences.local.json`，并把候选标记为已固化。
- `/config-candidate-undo 编号` 支持历史中的已固化偏好候选，删除对应偏好，并把候选恢复为活跃。
- `/config-manager-status` 只读展示本地偏好数量；偏好确认和撤销本身不改变回答风格、不触发任何桌面动作。

## 非目标

- 不确认固化 API key、账号、密钥、自动执行规则或其他敏感配置。
- 不让保存的偏好自动改变当前对话风格、LLM prompt、命令路由或执行决策。
- 不点击、不输入、不切换窗口、不启动应用。
- 不把确认/撤销命令加入 LLM 白名单，不让普通聊天或外脑自动写入偏好。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：偏好 JSON 可写入、读取、删除、计数和展示。
2. 在 `tests/test_memory_config_candidates.py` 增加 RED：偏好候选确认后写入配置、标记已固化；撤销后删除偏好并恢复候选。
3. 在 `tests/test_memory_config_manager.py` 增加 RED：配置管家展示偏好数量。
4. 在 `tests/test_agent.py` 增加 RED：Agent 接入偏好确认/撤销，配置管家可观察本地偏好。
5. 在 `tests/test_llm.py` 和 `tests/test_project_metadata.py` 增加 RED：确认/撤销命令仍不进入 LLM 命令建议，版本提升到 `0.134.0`。
6. 新增 `preferences.py`，集中处理 `config/preferences.local.json` 的读写、解析、展示、删除和计数。
7. 更新 `memory_config_candidates.py`，让确认/撤销 helper 支持联系人别名、应用别名、授权规则和偏好。
8. 更新配置管家、Agent 帮助和状态、版本号、README、PROJECT-PLAN、索引、进度和验证记录。
9. 执行目标测试、相邻回归、全量 unittest、命令行 smoke、源码桌面 smoke、安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 偏好候选 `回答尽量简洁` 经 `/config-candidate-confirm 1` 后写入 `config/preferences.local.json`。
- `/config-manager-status` 展示 `偏好：1 条`，但当前对话和命令执行路径不因该偏好自动变化。
- `/config-candidate-history` 展示已固化偏好，并提示 `/config-candidate-undo 编号`。
- `/config-candidate-undo 1` 删除对应偏好，并让候选重新出现在 `/config-candidates`。
- 确认/撤销命令仍不进入 LLM 白名单，普通聊天不会自动写入偏好。
