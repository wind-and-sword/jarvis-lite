# v149：偏好本地回答附注范围第一阶段实施计划

> 日期：2026-06-09
> 执行者：Codex
> 说明：本文承接 v148 偏好应用撤销提示第一阶段。当前阶段只收紧本地回答偏好附注的回答类型范围，并在附注中标明回答类型；不新增用户设置，不改变普通 LLM fallback、SearchRouter、InnerBrain、路由或桌面执行决策。

## 目标

- `describe_preference_local_answer_note()` 增加显式回答类型输入。
- 仅允许本地知识库回答和长期记忆兜底回答生成偏好附注。
- 本地回答偏好附注展示回答类型，便于审计偏好格式化到底作用在哪条回答路径上。
- 未知或未来回答类型默认不生成附注，避免误用。
- 版本提升到 `0.144.0` 并生成可安装测试包。

## 非目标

- 不新增偏好适用范围设置命令。
- 不改变 `/preference-apply-confirm`、`/preference-apply-history` 或 `/preference-apply-undo` 的命令语义。
- 不把本地回答附注、回答类型标签或撤销命令加入普通 LLM fallback provider context。
- 不把偏好管理命令加入 LLM provider command 白名单。
- 不改变本地知识库检索、长期记忆摘要、InnerBrain、SearchRouter、授权层或桌面执行决策。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：知识库和长期记忆回答类型分别展示不同回答类型标签。
2. 在 `tests/test_preferences.py` 增加 RED：未知回答类型返回空附注。
3. 在 `tests/test_agent.py` 增加 RED：`/ask` 知识库命中附注展示 `回答类型：本地知识库回答`。
4. 在 `tests/test_agent.py` 增加 RED：长期记忆兜底附注展示 `回答类型：长期记忆兜底回答`。
5. 在 `tests/test_agent.py` 增加 RED：普通 LLM fallback context 不包含本地回答类型标签和撤销命令。
6. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.144.0`。
7. 在 `preferences.py` 为 `describe_preference_local_answer_note()` 增加 answer type allowlist 和显示标签。
8. 在 `agent.py` 让本地知识库路径传入 `knowledge`，长期记忆兜底路径传入 `memory`。
9. 同步 README、PROJECT-PLAN、计划索引、文档索引、每日进度、验证记录和 `.codex` 留痕。
10. 跑目标测试、相邻回归、全量回归、命令行 smoke、桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 有效确认期间，知识库命中回答附注包含 `回答类型：本地知识库回答`。
- 有效确认期间，长期记忆兜底回答附注包含 `回答类型：长期记忆兜底回答`。
- 未支持回答类型不会生成本地回答偏好附注。
- 普通 LLM fallback context 不包含本地回答类型标签，也不包含 `/preference-apply-undo prefapp-...`。
- LLM provider instructions 仍不包含偏好管理命令。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.144.0`。
