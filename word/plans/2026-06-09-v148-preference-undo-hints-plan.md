# v148：偏好应用撤销提示第一阶段实施计划

> 日期：2026-06-09
> 执行者：Codex
> 说明：本文承接 v147 偏好格式化本地回答第一阶段。当前阶段只在用户可见的确认输出和本地回答偏好附注里展示按确认 ID 撤销的精确命令，不新增命令，不改变 LLM provider instructions、SearchRouter、InnerBrain、路由或桌面执行决策。

## 目标

- 成功执行 `/preference-apply-confirm [输入文本]` 后，在确认输出中展示 `撤销确认：/preference-apply-undo prefapp-...`。
- 本地知识库命中回答和长期记忆兜底回答的偏好附注中展示同一确认 ID 的撤销命令。
- 撤销提示使用确认 ID 而不是编号，避免历史排序变化后提示失效。
- 版本提升到 `0.143.0` 并生成可安装测试包。

## 非目标

- 不新增新的撤销命令；继续复用 `/preference-apply-undo 编号或ID`。
- 不把撤销提示加入普通 LLM fallback provider context。
- 不把 `/preference-apply-undo` 加入 LLM provider command 白名单。
- 不新增偏好适用范围开关，不改变本地知识库检索、长期记忆摘要或偏好有效性判定。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：确认输出包含按确认 ID 撤销的精确命令。
2. 在 `tests/test_preferences.py` 增加 RED：本地回答偏好附注包含按确认 ID 撤销的精确命令。
3. 在 `tests/test_agent.py` 增加 RED：知识库 `/ask` 和长期记忆兜底的实际输出包含撤销提示。
4. 在 `tests/test_agent.py` 或 `tests/test_preferences.py` 增加 RED：普通 LLM fallback context 不包含 `/preference-apply-undo prefapp-...`。
5. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.143.0`，并把更新 manifest 夹具提升到 `0.143.1`。
6. 在 `preferences.py` 新增内部格式化 helper，生成 `/preference-apply-undo {application_id}`。
7. 把 helper 接入 `describe_confirmed_preference_application()` 和 `describe_preference_local_answer_note()`。
8. 同步 README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
9. 跑目标测试、相邻回归、全量回归、命令行 smoke、桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- `/preference-apply-confirm 帮我总结知识库` 输出中存在 `撤销确认：/preference-apply-undo prefapp-...`，且 ID 与 `确认ID` 一致。
- 有效确认期间，本地知识库和长期记忆兜底的偏好附注都展示同一个撤销命令。
- `/llm-context-preview` 和 fake provider 收到的 LLM fallback context 不包含 `/preference-apply-undo prefapp-...`。
- LLM provider instructions 仍不包含偏好管理命令。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.143.0`。
