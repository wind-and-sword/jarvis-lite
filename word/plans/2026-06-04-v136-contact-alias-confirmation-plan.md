# v136：联系人别名确认固化与撤销第一阶段实施计划

> 日期：2026-06-04
> 执行者：Codex
> 说明：本文承接 v134 高风险记忆与配置候选确认草稿第一阶段和 v108 Jarvis Lite 1.0 验收线，先把联系人别名候选从确认草稿推进到显式确认固化与撤销闭环。

## 目标

- `/config-candidate-apply 编号` 作用于联系人别名候选时继续返回确认草稿，但明确提示 `/config-candidate-confirm 编号`。
- `/config-candidate-confirm 编号` 仅对活跃联系人别名候选生效，写入 `config/contacts.local.json`，并把候选标记为已固化。
- `/config-candidate-undo 编号` 仅对历史中的已固化联系人别名候选生效，删除对应联系人别名，并把候选恢复为活跃。
- `/config-manager-status` 展示联系人别名数量。

## 非目标

- 不确认固化授权规则、应用别名、偏好、API key 或自动发送规则。
- 不查找真实联系人、不点击、不输入、不发送消息。
- 不把确认/撤销命令加入 LLM 白名单，不让普通聊天或外脑自动写入联系人配置。

## 实施步骤

1. 在 `tests/test_contacts.py` 增加 RED：联系人别名 JSON 可写入、读取和删除。
2. 在 `tests/test_memory_config_candidates.py` 增加 RED：联系人别名候选确认后写入配置、标记已固化；撤销后删除配置并恢复候选。
3. 在 `tests/test_memory_config_manager.py` 增加 RED：配置管家展示联系人别名数量。
4. 在 `tests/test_agent.py` 增加 RED：Agent 接入 `/config-candidate-confirm` 和 `/config-candidate-undo`，帮助和状态页展示入口。
5. 在 `tests/test_llm.py` 和 `tests/test_project_metadata.py` 增加 RED：新高风险命令不进入 LLM 命令建议，版本提升到 `0.131.0`。
6. 新增 `contacts.py`，集中处理 `config/contacts.local.json` 的读写、解析、展示和删除。
7. 更新 `memory_config_candidates.py`，加入联系人别名确认和撤销 helper，并让确认草稿提示确认命令。
8. 更新 Agent 命令、配置管家、版本号、README、PROJECT-PLAN、索引、进度和验证记录。
9. 执行目标测试、相邻回归、全量 unittest、命令行 smoke、源码桌面 smoke、安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 联系人别名候选 `小王 => 微信联系人王工` 经 `/config-candidate-confirm 1` 后写入 `config/contacts.local.json`。
- `/config-candidate-history` 展示已固化联系人别名，并提示 `/config-candidate-undo 编号`。
- `/config-candidate-undo 1` 删除对应联系人别名，并让候选重新出现在 `/config-candidates`。
- 授权规则、应用别名和偏好候选仍只给确认草稿或暂不支持真实确认，不写入长期配置。
- 当前阶段不查找真实联系人、不发送消息、不接入自然语言自动执行。
