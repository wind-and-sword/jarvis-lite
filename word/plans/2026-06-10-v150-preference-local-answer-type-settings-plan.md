# v150：偏好本地回答类型开关第一阶段实施计划

> 日期：2026-06-10
> 执行者：Codex
> 说明：本文承接 v149 偏好本地回答附注范围第一阶段。当前阶段新增用户显式可配置的本地回答附注类型开关；默认保持 `0.144.0` 行为，不改变普通 LLM fallback、SearchRouter、InnerBrain、路由或桌面执行决策。

## 目标

- 在 `config/preferences.local.json` 中持久化本地回答附注类型开关。
- 缺失配置时默认启用 `knowledge` 和 `memory`，保持现有本地知识库回答和长期记忆兜底回答附注行为。
- 新增显式命令：
  - `/preference-answer-types`：查看本地回答附注类型开关。
  - `/preference-answer-type-enable 类型`：启用指定回答类型附注。
  - `/preference-answer-type-disable 类型`：停用指定回答类型附注。
- 停用某类后，该类本地回答不再追加偏好附注；另一类仍可继续展示。
- 未知类型拒绝写入，避免未来回答路径误继承偏好格式化。
- 版本提升到 `0.145.0` 并生成可安装测试包。

## 非目标

- 不新增普通聊天或 LLM fallback 自动写入、启停或确认偏好的路径。
- 不把新增偏好开关命令加入 LLM provider command 白名单。
- 不改变 `/preference-apply-confirm`、`/preference-apply-history` 或 `/preference-apply-undo` 的语义。
- 不撤销已有确认记录，不删除或停用已保存偏好。
- 不改变本地知识库检索、长期记忆摘要、SearchRouter、InnerBrain、授权层或桌面执行决策。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：缺失开关配置时 `knowledge` 和 `memory` 默认启用，状态命令显示两类类型和说明。
2. 在 `tests/test_preferences.py` 增加 RED：停用 `knowledge` 后知识库附注为空，`memory` 附注仍展示；重新启用后恢复。
3. 在 `tests/test_preferences.py` 增加 RED：未知回答类型开关引用报错且不写入配置。
4. 在 `tests/test_agent.py` 增加 RED：`/preference-answer-types`、`/preference-answer-type-enable`、`/preference-answer-type-disable` 可显式查看和启停，并出现在帮助、状态和配置管家入口中。
5. 在 `tests/test_agent.py` 增加 RED：停用知识库回答类型后 `/ask` 不展示偏好附注，长期记忆兜底仍展示附注。
6. 在 `tests/test_llm.py` 增加 RED：新增偏好开关命令不进入 LLM provider instructions。
7. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.145.0`，更新更新检查夹具版本为 `0.145.1`。
8. 在 `preferences.py` 增加本地回答类型设置读取、写入、解析和展示 helper，并让 `describe_preference_local_answer_note()` 同时检查类型是否启用。
9. 在 `agent.py` 接入三个显式命令，并更新 `/help` 与 `/status`。
10. 在 `memory_config_manager.py` 增加偏好回答类型开关入口提示。
11. 同步 README、PROJECT-PLAN、计划索引、文档索引、每日进度、验证记录和 `.codex` 留痕。
12. 跑目标测试、相邻回归、全量回归、命令行 smoke、源码桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 默认配置下，知识库命中回答和长期记忆兜底回答继续展示本地偏好附注。
- `/preference-answer-type-disable knowledge` 后，知识库命中回答不展示本地偏好附注，长期记忆兜底不受影响。
- `/preference-answer-type-disable memory` 后，长期记忆兜底不展示本地偏好附注，知识库命中不受影响。
- `/preference-answer-type-enable 类型` 可恢复对应类型附注。
- 未知类型返回可读错误，不污染 `preferences.local.json`。
- 普通 LLM fallback context 不展示本地回答类型标签或撤销命令。
- LLM provider instructions 仍不包含偏好管理或偏好回答类型开关命令。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.145.0`。
