# v147：偏好格式化本地回答第一阶段实施计划

> 日期：2026-06-09
> 执行者：Codex
> 说明：本文承接 v146 偏好进入普通回复上下文第一阶段。当前阶段只把最近一条有效确认记录以可审计附注追加到本地知识库命中回答和长期记忆兜底回答，不改变检索、路由、LLM 白名单、SearchRouter、InnerBrain、授权层或桌面执行决策。

## 目标

- 新增本地回答偏好格式化附注 helper，复用 v146 的有效确认记录判定。
- `/ask` 和普通问题命中 `data` 目录时，在原有资料命中回答末尾追加偏好确认审计附注。
- 长期记忆兜底回答在原有摘要末尾追加同样的偏好确认审计附注。
- 撤销确认、停用偏好、删除偏好、启用集合变化或偏好冲突后，本地回答不再展示旧确认附注。
- 版本提升到 `0.142.0` 并生成可安装测试包。

## 非目标

- 不重写本地知识库回答主体，不改变 `data/path:line` 来源展示、匹配排序或命中原因。
- 不重写长期记忆摘要主体，不改变 profile 读取和摘要规则。
- 不新增 slash command，不自动写入、启用、停用或确认偏好。
- 不把 `/preference-*` 管理命令加入 LLM provider command 白名单。
- 不改变普通 LLM fallback 已有上下文行为，不接入 SearchRouter、InnerBrain、授权层或桌面执行决策。

## 实施步骤

1. 在 `tests/test_agent.py` 增加 RED：有效偏好确认后，本地知识库 `/ask` 回答包含 `已确认偏好格式化：prefapp-...`、偏好 ID/文本和本地回答边界；撤销后消失，fake provider 不被调用。
2. 在 `tests/test_agent.py` 增加 RED：长期记忆兜底在有效确认后包含偏好格式化附注；撤销后消失。
3. 在 `tests/test_preferences.py` 增加 RED：本地回答偏好附注 helper 在启用集合变化后返回空字符串。
4. 在 `tests/test_llm.py` 补充边界断言：provider instructions 仍不包含本阶段本地回答附注文案。
5. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.142.0`。
6. 在 `preferences.py` 新增 `describe_preference_local_answer_note()`，复用 `_active_preference_application_for_reply()`。
7. 在 `agent.py` 新增 `_apply_preference_local_answer_note()`，并接入 `_answer_from_data()` 和长期记忆兜底返回。
8. 同步版本、README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
9. 跑目标测试、相邻回归、全量回归、命令行 smoke、桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 执行 `/preference-apply-confirm 帮我总结知识库` 后，`/ask Jarvis Lite 使用什么？` 在资料命中回答后展示 `已确认偏好格式化：prefapp-...` 和对应偏好 ID/文本。
- 执行 `/preference-apply-undo 1` 后，后续同类本地知识库回答不再展示该附注。
- 普通输入走长期记忆兜底时，在有效确认期间展示同一附注，撤销或启用集合变化后不展示。
- 本阶段不触发 fake LLM provider 调用，不改变 LLM provider instructions 白名单。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.142.0`。
