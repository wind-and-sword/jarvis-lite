# v146：偏好进入普通回复上下文第一阶段实施计划

> 日期：2026-06-09
> 执行者：Codex
> 说明：本文承接 v145 偏好应用确认记录与撤销第一阶段。当前阶段只把最近一条有效确认记录接入普通 LLM fallback 上下文，不把偏好管理命令加入 LLM 白名单，不改变 SearchRouter、InnerBrain、桌面动作或本地执行决策。

## 目标

- 新增“有效偏好确认上下文” helper，返回最近一条仍有效的 `prefapp-...` 确认记录。
- 只有最新确认记录满足以下条件时才进入普通回复上下文：
  - 状态为 `confirmed`。
  - 当前已启用偏好 ID 和文本与确认记录完全一致。
  - 当前已启用偏好不存在明显冲突。
- 在 `/llm-context-preview` 和普通 LLM fallback 调用上下文中展示有效偏好确认。
- 撤销确认、停用偏好、删除偏好或启用集合变化后，旧确认不再进入普通回复上下文。
- 版本提升到 `0.141.0` 并生成可安装测试包。

## 非目标

- 不把 `/preference-status`、`/preference-enable`、`/preference-disable`、`/preference-preview`、`/preference-apply-draft`、`/preference-apply-confirm`、`/preference-apply-history` 或 `/preference-apply-undo` 加入 LLM provider command 白名单。
- 不把偏好接入 SearchRouter、InnerBrain、命令路由、授权层或桌面执行决策。
- 不自动确认新启用偏好，不自动解决冲突，不自动恢复已撤销确认。
- 不重写本地知识库命中回答或长期记忆兜底回答；本阶段只覆盖普通 LLM fallback 上下文。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：确认后可生成普通回复偏好上下文，撤销后上下文为空。
2. 在 `tests/test_preferences.py` 增加 RED：确认后若启用集合变化，旧确认上下文失效。
3. 在 `tests/test_agent.py` 增加 RED：`/llm-context-preview` 展示有效偏好确认上下文。
4. 在 `tests/test_agent.py` 增加 RED：普通 LLM fallback 调用收到有效偏好确认上下文；撤销后不再收到。
5. 在 `tests/test_llm.py` 增加 RED：LLM provider instructions 仍不包含偏好管理命令或偏好确认上下文文案。
6. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.141.0`。
7. 在 `preferences.py` 实现有效确认选择和上下文行生成 helper。
8. 在 `agent.py` 的 `_llm_context_lines()` 追加有效偏好确认上下文。
9. 同步 README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
10. 跑目标测试、相邻回归、全量回归、命令行 smoke、桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 成功执行 `/preference-apply-confirm 帮我总结知识库` 后，`/llm-context-preview` 展示 `已确认偏好应用：prefapp-...` 和对应偏好 ID/文本。
- 普通输入走 LLM fallback 时，fake provider 的 context 参数包含同样的偏好确认上下文。
- `/preference-apply-undo 1` 后，后续 `/llm-context-preview` 和普通 LLM fallback context 不再包含该确认。
- 确认后停用偏好或启用新偏好时，旧确认不再进入普通回复上下文，必须重新确认。
- `OpenAIResponsesProvider` 的 instructions 仍不包含任何偏好管理 slash command。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.141.0`。
