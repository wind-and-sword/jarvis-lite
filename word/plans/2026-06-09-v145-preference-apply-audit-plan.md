# v145：偏好应用确认记录与撤销第一阶段实施计划

> 日期：2026-06-09
> 执行者：Codex
> 说明：本文承接 v144 偏好应用确认命令第一阶段。当前阶段补齐显式确认后的可审计记录、历史查看和撤销范围，但仍不把偏好自动接入普通聊天、LLM prompt、路由或执行决策。

## 目标

- `/preference-apply-confirm [输入文本]` 成功确认时写入一条运行态确认记录。
- 新增 `/preference-apply-history` 查看最近偏好应用确认记录。
- 新增 `/preference-apply-undo 编号或ID` 撤销某条确认记录。
- 撤销只标记该确认记录为已撤销，不停用偏好、不删除偏好、不回滚已经展示的输出。
- 版本提升到 `0.140.0` 并生成可安装测试包。

## 非目标

- 不把已启用偏好自动加入普通聊天回复。
- 不写入 LLM prompt、SearchRouter、InnerBrain、命令路由或执行决策。
- 不改变 `/preference-enable`、`/preference-disable` 和 `config/preferences.local.json` 的既有语义。
- 不新增偏好编辑、排序、分组、优先级或自动冲突解决。
- 不把 `/preference-apply-history` 或 `/preference-apply-undo` 加入 LLM provider 白名单。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：成功确认后历史可查看确认 ID、输入文本、偏好 ID 和状态。
2. 在 `tests/test_preferences.py` 增加 RED：无启用偏好或冲突拒绝时不写入确认历史。
3. 在 `tests/test_preferences.py` 增加 RED：撤销确认记录只改确认记录状态，不停用偏好。
4. 在 `tests/test_agent.py` 增加 RED：Agent 支持 `/preference-apply-history` 和 `/preference-apply-undo 编号或ID`，帮助、status 和配置管家展示入口。
5. 在 `tests/test_llm.py` 增加 RED：新增偏好应用历史/撤销命令不进入 provider instructions。
6. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.140.0`。
7. 在 `runtime_context.py` 增加偏好应用确认记录运行态字段和 JSON 读写。
8. 在 `preferences.py` 增加确认记录、历史描述和撤销 helper，并让确认成功时写入记录。
9. 在 `agent.py` 和 `memory_config_manager.py` 接入显式命令与入口文案。
10. 同步 README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
11. 跑目标测试、相邻回归、全量回归、命令行 smoke、桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 成功执行 `/preference-apply-confirm 帮我总结知识库` 后，`/preference-apply-history` 展示最近确认记录。
- 历史记录包含确认 ID、确认状态、输入文本、偏好稳定 ID 和偏好文本。
- `/preference-apply-undo 1` 或 `/preference-apply-undo 确认ID` 会把对应记录标记为已撤销。
- 撤销结果明确说明：只撤销确认记录，不停用偏好，不回滚已经展示的输出。
- 无启用偏好或偏好冲突导致确认失败时，不新增确认记录。
- LLM provider instructions 不包含 `/preference-apply-history` 或 `/preference-apply-undo`。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.140.0`。
