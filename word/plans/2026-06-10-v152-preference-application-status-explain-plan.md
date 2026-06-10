# v152：偏好应用状态解释第一阶段实施计划

> 日期：2026-06-10
> 执行者：Codex
> 说明：本文承接 v151 偏好普通回复上下文开关第一阶段。当前阶段只新增偏好应用确认记录的只读状态解释，帮助用户判断某条确认记录当前在普通回复上下文、本地知识库回答附注和长期记忆兜底回答附注中是否生效，以及失效原因；不改变确认、撤销、偏好启停、LLM 白名单、SearchRouter、InnerBrain、路由或桌面执行决策。

## 目标

- 新增 `/preference-apply-status [编号或ID]`：
  - 不传参数时解释最近一条偏好应用确认记录。
  - 传编号或 `prefapp-...` 时解释指定确认记录。
- 状态解释展示：
  - 确认记录状态：已确认或已撤销。
  - 普通回复上下文：生效或未生效，并说明原因。
  - 本地知识库回答附注：生效或未生效，并说明原因。
  - 长期记忆兜底回答附注：生效或未生效，并说明原因。
  - 已确认偏好列表、确认输入、确认时间、撤销时间和精确撤销命令。
- `/preference-apply-history`、`/help`、`/status` 和 `/config-manager-status` 展示状态解释入口。
- 版本提升到 `0.147.0` 并生成可安装测试包。

## 非目标

- 不改变 `/preference-apply-confirm` 的确认记录写入规则。
- 不改变 `/preference-apply-undo` 的撤销语义；撤销仍只把确认记录标记为已撤销。
- 不新增按回答类型撤销、按输出面撤销或单偏好撤销。
- 不把 `/preference-apply-status` 加入 LLM provider command 白名单。
- 不改变本地知识库检索、长期记忆摘要、SearchRouter、InnerBrain、授权层、路由或桌面执行决策。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：`describe_preference_application_status(paths)` 默认解释最近确认记录，三类输出面均显示“生效”，并包含撤销命令和状态解释入口。
2. 在 `tests/test_preferences.py` 增加 RED：撤销、普通回复上下文开关停用、本地回答类型停用、启用偏好集合变化、非最近确认记录分别给出明确“未生效”原因。
3. 在 `tests/test_agent.py` 增加 RED：`/preference-apply-status` 和 `/preference-apply-status 编号或ID` 可查看状态，未知引用返回可读提示，并出现在 `/help`、`/status` 和 `/config-manager-status`。
4. 在 `tests/test_llm.py` 增加 RED：`/preference-apply-status` 不进入 LLM provider instructions。
5. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.147.0`，更新更新检查夹具版本为 `0.147.1`。
6. 在 `preferences.py` 新增 `describe_preference_application_status(paths, reference=None)` 和内部状态判定 helper，复用现有有效确认判定条件并输出逐面原因。
7. 在 `agent.py` 接入 `/preference-apply-status [编号或ID]`，并更新 `/help` 与 `/status`。
8. 在 `memory_config_manager.py` 增加偏好应用状态解释入口提示。
9. 同步 README、PROJECT-PLAN、计划索引、文档索引、每日进度、验证记录和 `.codex` 留痕。
10. 跑目标测试、相邻回归、全量回归、命令行 smoke、源码桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 默认情况下，最近有效确认记录的三类输出面显示生效。
- 撤销确认记录后，三类输出面显示未生效，原因指向“确认记录已撤销”。
- 停用普通回复上下文后，只有普通回复上下文显示未生效，本地回答附注保持可生效。
- 停用 `knowledge` 或 `memory` 后，只对应回答类型显示未生效。
- 当前启用偏好集合变化或存在冲突后，三类输出面显示未生效并给出原因。
- 非最近确认记录显示未生效，原因指向“只有最近一条匹配确认记录会应用到当前上下文”。
- 新增命令不进入 LLM provider instructions。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.147.0`。
