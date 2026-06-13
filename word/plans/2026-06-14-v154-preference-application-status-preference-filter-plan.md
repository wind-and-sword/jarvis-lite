# v154：偏好应用状态单条偏好过滤第一阶段实施计划

> 日期：2026-06-14
> 执行者：Codex
> 说明：本文承接 v153 偏好应用状态输出面过滤第一阶段。当前阶段只新增状态解释的只读单条偏好过滤，便于用户在一次确认包含多条偏好时只查看某一条偏好的审计状态；不改变确认、撤销、偏好启停、LLM 白名单、SearchRouter、InnerBrain、路由或桌面执行决策。

## 目标

- 扩展 `/preference-apply-status [编号或ID] [输出面] [偏好编号或ID]`：
  - 不传参数时保持 v153 行为，解释最近确认记录的全部输出面和全部偏好。
  - 传 `pref-...` 时解释最近确认记录中的指定偏好。
  - 传 `preference 2`、`pref 2` 或 `偏好 2` 时解释最近确认记录中的第 2 条偏好。
  - 传确认记录编号或 `prefapp-...` 后，可继续传输出面和偏好过滤。
  - 传输出面后可继续传 `pref-...` 或 `preference 2` 过滤指定偏好。
- 单条偏好过滤后只展示目标偏好，并补充目标偏好当前是否仍在已启用偏好集合中。
- 输出面过滤和单条偏好过滤可组合；输出面仍只支持 `reply`、`knowledge`、`memory` 及既有中文别名。
- 未知偏好返回可读提示，引导先运行 `/preference-apply-status [编号或ID]` 查看确认记录里的偏好。
- `/preference-apply-history`、`/help`、`/status` 和 `/config-manager-status` 展示可选偏好参数。
- 版本提升到 `0.149.0` 并生成可安装测试包。

## 非目标

- 不新增按回答类型撤销、按输出面撤销或单偏好撤销。
- 不改变 `/preference-apply-confirm` 的确认记录写入规则。
- 不改变 `/preference-apply-undo` 的撤销语义；撤销仍只把整条确认记录标记为已撤销。
- 不把 `/preference-apply-status` 加入 LLM provider command 白名单。
- 不改变本地知识库检索、长期记忆摘要、SearchRouter、InnerBrain、授权层、路由或桌面执行决策。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：`describe_preference_application_status(paths, preference_reference="pref-...")` 只展示目标偏好，不展示同一确认记录中的其他偏好。
2. 在 `tests/test_preferences.py` 增加 RED：输出面过滤和单条偏好过滤可组合，未知偏好返回可读错误且不修改运行态。
3. 在 `tests/test_agent.py` 增加 RED：`/preference-apply-status pref-...`、`/preference-apply-status prefapp-... knowledge pref-...` 和 `/preference-apply-status preference 2` 可过滤目标偏好；帮助、状态和配置管家展示新参数。
4. 在 `tests/test_llm.py` 保持边界：`/preference-apply-status` 仍不进入 LLM provider instructions。
5. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.149.0`，更新更新检查夹具版本为 `0.149.1`。
6. 在 `preferences.py` 扩展 `describe_preference_application_status(paths, reference=None, surface=None, preference_reference=None)`，新增确认记录内偏好引用解析和目标偏好当前启用状态说明。
7. 在 `agent.py` 扩展 `_parse_preference_apply_status_args()`，保持旧用法兼容，并新增 `pref-...`、`preference/pref/偏好` 标记解析。
8. 在 `memory_config_manager.py`、`/help`、`/status` 和历史提示中同步参数说明。
9. 同步 README、PROJECT-PLAN、计划索引、文档索引、每日进度、验证记录和 `.codex` 留痕。
10. 跑目标测试、相邻回归、全量回归、命令行 smoke、源码桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 无参数 `/preference-apply-status` 行为与 v153 保持一致。
- `/preference-apply-status pref-...` 只展示最近确认记录中的目标偏好。
- `/preference-apply-status preference 2` 可按确认记录内编号过滤最近确认记录中的第 2 条偏好。
- `/preference-apply-status prefapp-... knowledge pref-...` 可同时过滤指定确认记录、指定输出面和指定偏好。
- 单条偏好过滤会展示“目标偏好当前状态”，说明该偏好是否仍在当前已启用偏好集合中。
- 未知偏好返回“偏好应用确认中的偏好不存在”。
- 新增过滤不写入配置、不修改确认记录、不影响撤销、不进入 LLM 白名单。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.149.0`。
