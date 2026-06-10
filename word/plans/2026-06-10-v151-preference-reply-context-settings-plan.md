# v151：偏好普通回复上下文开关第一阶段实施计划

> 日期：2026-06-10
> 执行者：Codex
> 说明：本文承接 v150 偏好本地回答类型开关第一阶段。当前阶段只为已确认偏好进入普通 LLM fallback 上下文增加显式开关；默认保持 `0.145.0` 行为，不改变本地回答附注、SearchRouter、InnerBrain、路由或桌面执行决策。

## 目标

- 在 `config/preferences.local.json` 中持久化普通回复偏好上下文开关。
- 缺失配置时默认启用，保持 `0.145.0` 中最近有效确认记录进入普通 LLM fallback 上下文和 `/llm-context-preview` 的行为。
- 新增显式命令：
  - `/preference-reply-context`：查看普通回复偏好上下文开关。
  - `/preference-reply-context-enable`：启用普通回复偏好上下文。
  - `/preference-reply-context-disable`：停用普通回复偏好上下文。
- 停用后，`describe_preference_reply_context()` 返回空字符串，普通 LLM fallback 和 `/llm-context-preview` 不再携带确认偏好上下文。
- 停用普通回复上下文不影响本地知识库回答和长期记忆兜底回答的偏好附注；本地回答附注仍由 v150 的 `knowledge` / `memory` 类型开关单独控制。
- 版本提升到 `0.146.0` 并生成可安装测试包。

## 非目标

- 不撤销偏好应用确认记录。
- 不删除、停用或重写已保存偏好。
- 不改变 `/preference-apply-confirm`、`/preference-apply-history` 或 `/preference-apply-undo` 的历史语义。
- 不把新增开关命令加入 LLM provider command 白名单。
- 不改变本地知识库检索、长期记忆摘要、SearchRouter、InnerBrain、授权层、路由或桌面执行决策。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：默认普通回复偏好上下文开关启用，状态文案展示配置文件、启停命令和边界。
2. 在 `tests/test_preferences.py` 增加 RED：停用普通回复上下文后 `describe_preference_reply_context()` 返回空字符串，但 `describe_preference_local_answer_note(paths, "knowledge")` 仍展示本地回答附注；重新启用后普通回复上下文恢复。
3. 在 `tests/test_agent.py` 增加 RED：`/preference-reply-context`、`/preference-reply-context-enable`、`/preference-reply-context-disable` 可显式查看和启停，并出现在 `/help`、`/status` 和 `/config-manager-status`。
4. 在 `tests/test_agent.py` 增加 RED：停用普通回复上下文后 `/llm-context-preview` 不再展示确认偏好上下文；本地知识库回答仍可展示附注。
5. 在 `tests/test_llm.py` 增加 RED：新增普通回复上下文开关命令不进入 LLM provider instructions。
6. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.146.0`，更新更新检查夹具版本为 `0.146.1`。
7. 在 `preferences.py` 增加普通回复上下文开关读取、写入和展示 helper，并让 `describe_preference_reply_context()` 先检查开关。
8. 在 `agent.py` 接入三个显式命令，并更新 `/help` 与 `/status`。
9. 在 `memory_config_manager.py` 增加普通回复偏好上下文开关入口提示。
10. 同步 README、PROJECT-PLAN、计划索引、文档索引、每日进度、验证记录和 `.codex` 留痕。
11. 跑目标测试、相邻回归、全量回归、命令行 smoke、源码桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 默认配置下，最近有效确认记录继续进入普通 LLM fallback 上下文和 `/llm-context-preview`。
- `/preference-reply-context-disable` 后，普通 LLM fallback 和 `/llm-context-preview` 不展示确认偏好上下文。
- `/preference-reply-context-disable` 不影响本地知识库回答和长期记忆兜底回答的本地回答附注。
- `/preference-reply-context-enable` 可恢复普通回复偏好上下文。
- 新增命令不进入 LLM provider instructions。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.146.0`。
