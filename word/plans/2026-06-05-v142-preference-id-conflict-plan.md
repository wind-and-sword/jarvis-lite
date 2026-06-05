# v142：偏好稳定 ID 与冲突提示第一阶段实施计划

> 日期：2026-06-05
> 执行者：Codex
> 说明：本文承接 v141 偏好应用预览第一阶段，把已保存偏好推进到可审计稳定 ID 与只读冲突提示，但仍不自动改变回复、LLM prompt、路由或执行决策。

## 目标

- 为本地偏好记录增加稳定 ID，旧记录缺失 ID 时按偏好文本生成确定性 ID。
- `/preference-status` 和 `/preference-preview [输入文本]` 展示偏好 ID，便于后续撤销、确认和真实应用前审计。
- `/preference-enable` 与 `/preference-disable` 支持 `编号或ID`，保留原有编号用法。
- 对已启用偏好中明显互斥的表达给出只读冲突提示，提示用户后续需要人工确认，不自动裁决优先级。
- 版本提升到 `0.137.0` 并生成可安装测试包。

## 非目标

- 不新增偏好编辑、排序、分组或优先级系统。
- 不自动解决冲突，不选择哪条偏好生效。
- 不把已启用偏好自动加入普通回答、LLM prompt、SearchRouter、InnerBrain 或命令路由。
- 不把 `/preference-status`、`/preference-enable`、`/preference-disable` 或 `/preference-preview` 加入 LLM provider 白名单。
- 不新增自然语言自动映射，不从普通聊天自动启用、停用、预览或应用偏好。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：保存偏好写入稳定 ID，旧记录可读出确定性 ID，状态和预览展示 ID。
2. 在 `tests/test_preferences.py` 增加 RED：按 ID 启用/停用偏好，并保留按编号启停。
3. 在 `tests/test_preferences.py` 增加 RED：已启用的明显冲突偏好在状态和预览中展示冲突提示。
4. 在 `tests/test_agent.py` 增加 RED：Agent 支持 `/preference-enable ID` 和 `/preference-disable ID`，帮助/status 文案改为编号或 ID。
5. 在 `tests/test_llm.py` 保持 RED 边界：偏好状态、启停和预览命令不进入 provider instructions。
6. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.137.0`。
7. 在 `preferences.py` 实现偏好稳定 ID、引用解析、启停写回和冲突提示 helper。
8. 在 `agent.py` 接入编号或 ID 解析与文案。
9. 同步 README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
10. 跑目标测试、相邻回归、全量回归、命令行 smoke、桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 新保存偏好写入 `id` 字段，旧记录缺失 `id` 时仍显示稳定 ID。
- `/preference-enable pref-...` 和 `/preference-disable pref-...` 可切换对应偏好，返回文案包含 ID。
- `/preference-status` 展示每条偏好的 ID、启用状态和文本。
- `/preference-preview [输入文本]` 只展示已启用偏好及其 ID；存在明显冲突时展示“偏好冲突提示”。
- 冲突提示明确只用于人工确认，不自动改变回复风格、LLM prompt、路由或执行决策。
- LLM provider instructions 不包含偏好管理命令。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.137.0`。
