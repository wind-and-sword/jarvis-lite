# v144：偏好应用确认命令第一阶段实施计划

> 日期：2026-06-05
> 执行者：Codex
> 说明：本文承接 v143 偏好应用确认草稿第一阶段，新增显式确认命令和应用范围说明，但仍不把偏好自动接入普通回复、LLM prompt、路由或执行决策。

## 目标

- 新增 `/preference-apply-confirm [输入文本]`，显式确认已启用偏好应用到本次输入。
- 有启用偏好且无明显冲突时，输出“已确认本次偏好应用”、输入文本、偏好稳定 ID、偏好文本和应用范围。
- 无启用偏好时拒绝确认，并提示 `/preference-enable 编号或ID`。
- 已启用偏好存在明显冲突时拒绝确认，并展示冲突提示，要求先停用冲突偏好。
- 版本提升到 `0.139.0` 并生成可安装测试包。

## 非目标

- 不把已启用偏好自动加入普通聊天回复。
- 不写入 LLM prompt、SearchRouter、InnerBrain、命令路由或执行决策。
- 不新增偏好优先级、排序、编辑、分组或自动冲突解决。
- 不持久化本次确认结果，不影响后续会话。
- 不把 `/preference-apply-confirm` 加入 LLM provider 白名单。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：`describe_confirmed_preference_application()` 无启用偏好时拒绝确认。
2. 在 `tests/test_preferences.py` 增加 RED：有启用偏好且无冲突时输出确认结果和本次范围。
3. 在 `tests/test_preferences.py` 增加 RED：存在冲突时拒绝确认并展示冲突提示。
4. 在 `tests/test_agent.py` 增加 RED：Agent 支持 `/preference-apply-confirm [输入文本]`，帮助、status 和配置管家展示入口。
5. 在 `tests/test_llm.py` 增加 RED：`/preference-apply-confirm` 不进入 provider instructions。
6. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.139.0`。
7. 在 `preferences.py` 实现确认 helper，复用 `enabled_preferences()` 和 `preference_conflict_hints()`。
8. 在 `agent.py` 接入显式 slash command，并补帮助/status 文案。
9. 在 `memory_config_manager.py` 补配置管家入口提示。
10. 同步 README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
11. 跑目标测试、相邻回归、全量回归、命令行 smoke、桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- `/preference-apply-confirm 帮我总结知识库` 在有启用偏好且无冲突时返回“已确认本次偏好应用”。
- 确认结果包含输入文本、已确认偏好数量、偏好稳定 ID 和偏好文本。
- 确认结果明确应用范围仅限本次显式命令输出，不影响普通聊天、LLM prompt、路由或执行决策。
- 无启用偏好时拒绝确认，并提示 `/preference-enable 编号或ID`。
- 存在明显冲突时拒绝确认，展示“偏好冲突提示”和“只提示冲突，不自动裁决优先级”。
- LLM provider instructions 不包含 `/preference-apply-confirm`。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.139.0`。
