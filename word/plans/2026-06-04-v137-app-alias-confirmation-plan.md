# v137：应用别名确认固化与撤销第一阶段实施计划

> 日期：2026-06-04
> 执行者：Codex
> 说明：本文承接 v136 联系人别名确认固化与撤销第一阶段，把应用别名候选推进到显式确认固化与撤销闭环。

## 目标

- `/config-candidate-apply 编号` 作用于应用别名候选时继续返回确认草稿，并提示 `/config-candidate-confirm 编号`。
- `/config-candidate-confirm 编号` 支持活跃应用别名候选，写入 `config/apps.local.json` 的 `apps.<app_id>.aliases`，并把候选标记为已固化。
- `/config-candidate-undo 编号` 支持历史中的已固化应用别名候选，删除对应别名，并把候选恢复为活跃。
- `/app-find 新别名` 能命中对应已登记应用；确认和撤销本身不启动应用。

## 非目标

- 不确认固化授权规则、偏好、API key、应用路径或自动执行规则。
- 不启动应用、不切换窗口、不点击、不输入。
- 不把确认/撤销命令加入 LLM 白名单，不让普通聊天或外脑自动写入应用配置。

## 实施步骤

1. 在 `tests/test_app_registry.py` 增加 RED：应用别名 JSON 可写入、匹配和删除，撤销时不删除已有 path 覆盖。
2. 在 `tests/test_memory_config_candidates.py` 增加 RED：应用别名候选确认后写入配置、标记已固化；撤销后删除别名并恢复候选。
3. 在 `tests/test_agent.py` 增加 RED：Agent 接入应用别名确认/撤销，`/app-find` 可命中新别名。
4. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.132.0`。
5. 更新 `app_registry.py`，提供应用别名候选解析、保存和删除 helper，复用 `apps.local.json` 既有结构。
6. 更新 `memory_config_candidates.py`，让确认/撤销 helper 同时支持联系人别名和应用别名。
7. 更新 Agent 帮助、状态、版本号、README、PROJECT-PLAN、索引、进度和验证记录。
8. 执行目标测试、相邻回归、全量 unittest、命令行 smoke、源码桌面 smoke、安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 应用别名候选 `晨会入口 => chrome` 经 `/config-candidate-confirm 1` 后写入 `config/apps.local.json`。
- `/app-find 晨会入口` 命中 `Chrome (chrome)`，但确认阶段不启动应用。
- `/config-candidate-history` 展示已固化应用别名，并提示 `/config-candidate-undo 编号`。
- `/config-candidate-undo 1` 删除对应应用别名，并让候选重新出现在 `/config-candidates`。
- 当前阶段不写应用路径、不启动应用、不接入自然语言自动执行。
