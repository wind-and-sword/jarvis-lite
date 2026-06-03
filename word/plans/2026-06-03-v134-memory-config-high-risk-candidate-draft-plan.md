# v134：高风险记忆与配置候选确认草稿第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v133 记忆与配置候选恢复第一阶段，为联系人、授权规则等更高风险候选补齐确认草稿和撤销入口的第一阶段。

## 目标

- 当用户对联系人别名、授权规则、应用别名或偏好候选执行 `/config-candidate-apply 编号` 时，返回确认草稿，而不是只给出“暂不支持”。
- 确认草稿必须展示候选类型、候选内容、当前阶段不写入长期配置的边界，以及 `/config-candidate-dismiss 编号` 撤销入口。
- 高风险候选在确认草稿输出后继续保持 active，便于用户稍后忽略、恢复或等待后续真实固化阶段。

## 非目标

- 不创建联系人、授权规则、应用别名或偏好的长期配置文件。
- 不新增 `/config-candidate-confirm` 等真实固化命令。
- 不把候选命令加入 LLM 白名单。
- 不改变 memory、experience、directory 低风险候选的固化行为。

## 实施步骤

1. 在 `tests/test_memory_config_candidates.py` 增加 RED：联系人别名和授权规则候选执行 apply 后返回确认草稿、撤销入口和不写入边界，候选仍保持 active，且不写入高风险配置文件。
2. 更新同文件现有 unsupported 覆盖，让高风险候选断言新确认草稿文案，目录格式错误仍保持原行为。
3. 在 `tests/test_agent.py` 更新 `/config-candidate-apply` 高风险候选断言，覆盖 Agent 输出确认草稿和活跃候选保留。
4. 将版本元数据测试期望提升到 `0.129.0`，验证 RED。
5. 在 `src/jarvis_lite/memory_config_candidates.py` 增加高风险候选识别和确认草稿格式化 helper。
6. 同步版本、README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
7. 运行目标测试、相邻回归、全量 unittest、临时项目 smoke、桌面 smoke、打包后 smoke 和静态检查。

## 验收标准

- `/config-candidate-apply 1` 作用于联系人别名候选时，输出“需要确认后再固化联系人别名候选”、确认草稿、不写入长期配置说明和 `/config-candidate-dismiss 1`。
- `/config-candidate-apply 2` 作用于授权规则候选时，输出同类确认草稿，且编号与当前活跃候选编号一致。
- 高风险候选输出确认草稿后仍在 `/config-candidates` 活跃列表中。
- 本阶段不生成 `contacts.local.json`、`authorization.local.json`、`apps.local.json`、`preferences.local.json` 或其他高风险长期配置文件。
