# v128：记忆与配置候选固化第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v127 记忆与配置候选池第一阶段，在不扩大自动写入范围的前提下，为低风险候选补齐显式固化入口。

## 目标

- 新增显式命令 `/config-candidate-apply 编号`，把当前候选池中的指定活跃候选固化到既有长期存储。
- `memory` 候选复用 `memory/profile.md` 的长期记忆写入逻辑。
- `experience` 候选复用 `memory/experiences.md` 的经验记忆写入逻辑。
- `directory` 候选复用常用目录登记逻辑，接受 `别名 => 路径` 或 `别名 路径` 两种明确格式。
- 固化成功后把候选状态标记为 `applied`，不再出现在活跃候选列表。
- 帮助、状态、README、PROJECT-PLAN、进度和验证记录同步展示固化入口。

## 非目标

- 不把 `/config-candidate-apply` 加入 LLM 白名单。
- 不自动从普通聊天、LLM 输出或候选重复次数触发固化。
- 不固化联系人别名、授权规则、应用路径、偏好或其他候选；这些类型本阶段只返回边界说明并保持活跃。
- 不新增长期配置文件结构，不改写 `config/apps.local.json`、联系人配置或授权规则。

## 实施步骤

1. 扩展 `tests/test_memory_config_candidates.py`，先验证记忆、经验、目录固化和不支持类型拒绝。
2. 扩展 `tests/test_agent.py`，验证 `/config-candidate-apply` 的成功、参数错误、帮助和状态文案。
3. 扩展 `tests/test_llm.py`，验证 LLM 白名单不包含 `/config-candidate-apply`。
4. 将版本元数据测试期望提升到 `0.123.0`，验证 RED。
5. 扩展 `src/jarvis_lite/memory_config_candidates.py`，新增候选固化函数、目录候选解析和 applied 状态写回。
6. 将 `/config-candidate-apply` 接入 `JarvisAgent`、帮助、状态和运行日志。
7. 同步 `pyproject.toml`、`src/jarvis_lite/__init__.py`、README、PROJECT-PLAN、方案索引、文档索引、进度与验证记录。
8. 运行目标测试、相邻回归、全量 unittest、smoke、打包和静态检查。

## 验收标准

- `/config-candidate-apply 1` 可把 `memory` 候选写入 `memory/profile.md`，候选随后从活跃列表消失。
- `/config-candidate-apply 1` 可把 `experience` 候选写入 `memory/experiences.md`。
- `/config-candidate-apply 1` 可把 `directory` 候选登记到 `memory/directories.json`。
- 联系人别名、授权规则、应用别名、偏好和其他候选不会被固化，也不会被隐藏。
- 缺少编号、非数字编号和不存在的编号返回清晰用法或错误。
- LLM 白名单不包含 `/config-candidate-apply`。
