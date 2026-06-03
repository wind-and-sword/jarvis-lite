# v133：记忆与配置候选恢复第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v128 记忆与配置候选固化第一阶段，为候选误忽略或误固化后的重新处理补齐第一阶段闭环。

## 目标

- 新增显式命令 `/config-candidate-history`，只读查看已忽略或已固化的记忆与配置候选。
- 新增显式命令 `/config-candidate-restore 编号`，把候选历史中的指定候选恢复为活跃候选，便于重新固化或忽略。
- 恢复只改变候选运行态状态，不自动删除已经写入的长期记忆、经验记忆或常用目录。

## 非目标

- 不从 `memory/profile.md`、`memory/experiences.md` 或 `memory/directories.json` 自动删除已固化内容。
- 不支持联系人、授权规则或应用配置的长期写入。
- 不把候选恢复命令加入 LLM 白名单。
- 不改变候选池 active 编号规则。

## 实施步骤

1. 在 `tests/test_memory_config_candidates.py` 增加 RED：忽略候选后，`describe_memory_config_candidate_history()` 展示已忽略候选，`restore_memory_config_candidate()` 可恢复为 active。
2. 在同一测试文件增加 RED：固化候选后恢复只恢复候选状态，不删除已经写入的长期记忆或目录。
3. 在 `tests/test_agent.py` 增加 RED：Agent 接入 `/config-candidate-history`、`/memory-config-candidate-history` 和 `/config-candidate-restore 编号`，并覆盖参数错误、帮助和状态文案。
4. 在 `tests/test_llm.py` 增加 RED：LLM 白名单不包含 `/config-candidate-history` 或 `/config-candidate-restore`。
5. 将版本元数据测试期望提升到 `0.128.0`，验证 RED。
6. 在 `src/jarvis_lite/memory_config_candidates.py` 新增候选历史描述与恢复 helper。
7. 将命令接入 `JarvisAgent`、帮助、状态与公开文档，同步版本、进度和验证记录。
8. 运行目标测试、相邻回归、全量 unittest、临时项目 smoke、桌面 smoke、打包后 smoke 和静态检查。

## 验收标准

- `/config-candidate-history` 能列出已忽略和已固化候选，并提示 `/config-candidate-restore 编号`。
- `/config-candidate-restore 1` 能把历史候选恢复到 `/config-candidates` 活跃列表。
- 恢复已固化候选不会删除已经写入的长期记忆、经验记忆或常用目录。
- 输出继续明确不自动写入高风险配置、不自动删除长期存储、不加入 LLM 白名单。
