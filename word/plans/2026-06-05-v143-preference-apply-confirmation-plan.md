# v143：偏好应用确认草稿第一阶段实施计划

> 日期：2026-06-05
> 执行者：Codex
> 说明：本文承接 v142 偏好稳定 ID 与冲突提示第一阶段，把已启用偏好推进到真正应用前的显式确认草稿，但仍不自动改变回复、LLM prompt、路由或执行决策。

## 目标

- 新增 `/preference-apply-draft [输入文本]`，生成“待确认偏好应用草稿”。
- 草稿展示输入文本、已启用偏好、稳定 ID、冲突提示和显式确认边界。
- 无已启用偏好时提示先用 `/preference-enable 编号或ID` 启用。
- 版本提升到 `0.138.0` 并生成可安装测试包。

## 非目标

- 不让已启用偏好自动影响普通回答。
- 不把偏好写入 LLM prompt、SearchRouter、InnerBrain、命令路由或执行决策。
- 不新增真正的偏好应用执行器、优先级裁决、自动冲突解决或持久 pending 状态。
- 不把 `/preference-apply-draft` 加入 LLM provider 白名单。
- 不从自然语言自动映射到偏好应用草稿。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：`describe_preference_application_draft()` 无已启用偏好时提示先启用。
2. 在 `tests/test_preferences.py` 增加 RED：已启用偏好时草稿展示输入、偏好 ID、冲突提示和不自动应用边界。
3. 在 `tests/test_agent.py` 增加 RED：Agent 支持 `/preference-apply-draft [输入文本]`，帮助、status 和配置管家展示入口。
4. 在 `tests/test_llm.py` 增加 RED：`/preference-apply-draft` 不进入 provider instructions。
5. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.138.0`。
6. 在 `preferences.py` 实现确认草稿 helper，复用 `enabled_preferences()` 与 `preference_conflict_hints()`。
7. 在 `agent.py` 接入显式 slash command，并补帮助/status 文案。
8. 在 `memory_config_manager.py` 补配置管家入口提示。
9. 同步 README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
10. 跑目标测试、相邻回归、全量回归、命令行 smoke、桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- `/preference-apply-draft 帮我总结知识库` 返回“待确认偏好应用草稿”。
- 草稿包含 `预览输入`、已启用偏好数量、偏好稳定 ID 和偏好文本。
- 存在明显冲突时草稿展示“偏好冲突提示”，并明确只提示人工确认、不自动裁决优先级。
- 草稿明确当前阶段不自动改变回复风格、LLM prompt、路由或执行决策，并提示当前不真正应用。
- 无已启用偏好时提示用 `/preference-enable 编号或ID` 启用。
- LLM provider instructions 不包含 `/preference-apply-draft`。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.138.0`。
