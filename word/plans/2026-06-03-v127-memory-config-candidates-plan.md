# v127：记忆与配置候选池第一阶段实施计划

> 日期：2026-06-03
> 执行者：Codex
> 说明：本文承接 v126 任务失败截图 OCR 复盘第一阶段，回到 Jarvis Lite 1.0 验收线中的自动记忆与配置管家后续阶段。

## 目标

- 新增记忆与配置候选池，复用 `jarvis-lite-runtime/agent-context.json`，不新增长期持久化文件结构。
- 新增显式命令 `/config-candidates` 查看候选，兼容 `/memory-config-candidates`。
- 新增显式命令 `/config-candidate-add 类型 内容`，把用户明确指出的记忆或配置候选写入运行态候选池。
- 新增显式命令 `/config-candidate-dismiss 编号`，忽略当前候选池中的指定候选。
- `/config-manager-status` 展示候选池统计和候选管理入口。

## 非目标

- 不自动写入长期记忆、经验记忆、常用目录、应用路径、联系人别名或免确认规则。
- 不把普通聊天内容自动沉淀为候选；第一阶段只支持显式 slash command。
- 不接入 LLM 白名单生成候选写入命令。
- 不新增联系人、免确认规则或应用路径的真实固化逻辑。

## 候选类型

- `memory`：长期记忆候选。
- `experience`：经验记忆候选。
- `directory`：常用目录候选。
- `app_alias`：应用别名候选。
- `contact_alias`：联系人别名候选。
- `authorization_rule`：授权或免确认规则候选。
- `preference`：非敏感偏好候选。
- `other`：其他低风险候选。

## 实施步骤

1. 新增 `tests/test_memory_config_candidates.py`，先验证空候选池、显式添加候选、重复候选计数、运行态恢复和忽略候选。
2. 扩展 `tests/test_memory_config_manager.py`，验证 `/config-manager-status` 的候选统计和入口提示。
3. 扩展 `tests/test_agent.py`，验证 `/config-candidates`、`/memory-config-candidates`、`/config-candidate-add`、`/config-candidate-dismiss`、帮助和 `/status` 文案。
4. 扩展 `tests/test_llm.py`，验证 LLM 白名单不包含候选写入或忽略命令。
5. 将版本元数据测试期望提升到 `0.122.0`，验证 RED。
6. 扩展 `src/jarvis_lite/runtime_context.py`，增加 `RuntimeMemoryConfigCandidateContext` 与候选池序列化。
7. 新增 `src/jarvis_lite/memory_config_candidates.py`，实现候选添加、列表、忽略、统计和类型规范化。
8. 将候选池统计接入 `src/jarvis_lite/memory_config_manager.py`。
9. 将新命令接入 `JarvisAgent`、帮助、状态文案和运行日志；候选写入命令不加入 LLM 白名单。
10. 同步版本、README、PROJECT-PLAN、方案索引、文档索引、进度与验证记录。
11. 运行目标测试、相邻回归、全量 unittest、smoke、打包和静态检查。

## 验收标准

- `/config-candidates` 空状态提示暂无候选，并说明不会自动写入长期配置。
- `/config-candidate-add memory 以后称这个项目为 Jarvis Lite` 写入运行态候选池。
- 重复添加相同类型和内容会增加出现次数，不重复生成多条候选。
- 重启 `JarvisAgent` 后 `/config-candidates` 仍能看到候选。
- `/config-candidate-dismiss 1` 会忽略当前第 1 条候选，候选列表不再显示该条。
- `/config-manager-status` 显示活跃候选数量、已忽略候选数量和候选管理入口。
- LLM 白名单不包含 `/config-candidate-add` 或 `/config-candidate-dismiss`。
