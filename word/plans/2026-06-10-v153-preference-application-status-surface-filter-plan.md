# v153：偏好应用状态输出面过滤第一阶段实施计划

> 日期：2026-06-10
> 执行者：Codex
> 说明：本文承接 v152 偏好应用状态解释第一阶段。当前阶段只新增状态解释的只读输出面过滤，便于用户只查看普通回复上下文、本地知识库回答附注或长期记忆兜底回答附注的生效状态；不改变确认、撤销、偏好启停、LLM 白名单、SearchRouter、InnerBrain、路由或桌面执行决策。

## 目标

- 扩展 `/preference-apply-status [编号或ID] [输出面]`：
  - 不传参数时保持 v152 行为，解释最近确认记录的全部输出面。
  - 只传输出面时解释最近确认记录的指定输出面。
  - 传编号或 `prefapp-...` 后可继续传输出面，解释指定确认记录的指定输出面。
- 输出面支持：
  - `reply` / `context` / `普通回复` / `普通回复上下文`
  - `knowledge` / `kb` / `知识库` / `本地知识库回答`
  - `memory` / `长期记忆` / `长期记忆兜底回答`
- 过滤后只展示目标输出面的“生效/未生效”和原因，同时保留确认记录、输入、已确认偏好、撤销命令和只读边界说明。
- 未知输出面返回可读提示，并引导使用 `reply`、`knowledge` 或 `memory`。
- `/preference-apply-history`、`/help`、`/status` 和 `/config-manager-status` 展示可选输出面参数。
- 版本提升到 `0.148.0` 并生成可安装测试包。

## 非目标

- 不新增按回答类型撤销、按输出面撤销或单偏好撤销。
- 不改变 `/preference-apply-confirm` 的确认记录写入规则。
- 不改变 `/preference-apply-undo` 的撤销语义；撤销仍只把确认记录标记为已撤销。
- 不把 `/preference-apply-status` 加入 LLM provider command 白名单。
- 不改变本地知识库检索、长期记忆摘要、SearchRouter、InnerBrain、授权层、路由或桌面执行决策。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：`describe_preference_application_status(paths, surface="knowledge")` 只展示本地知识库回答附注，不展示普通回复上下文和长期记忆兜底回答附注。
2. 在 `tests/test_preferences.py` 增加 RED：输出面中文别名可解析，未知输出面返回可读错误且不修改运行态。
3. 在 `tests/test_agent.py` 增加 RED：`/preference-apply-status knowledge`、`/preference-apply-status 编号或ID memory` 可过滤状态；未知输出面有可读提示，并出现在 `/help`、`/status` 和 `/config-manager-status`。
4. 在 `tests/test_llm.py` 保持 RED 边界：`/preference-apply-status` 仍不进入 LLM provider instructions。
5. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.148.0`，更新更新检查夹具版本为 `0.148.1`。
6. 在 `preferences.py` 新增状态输出面解析 helper，并扩展 `describe_preference_application_status(paths, reference=None, surface=None)`。
7. 在 `agent.py` 解析可选输出面参数，保持单参数编号/ID兼容。
8. 在 `memory_config_manager.py`、`/help`、`/status` 和历史提示中同步参数说明。
9. 同步 README、PROJECT-PLAN、计划索引、文档索引、每日进度、验证记录和 `.codex` 留痕。
10. 跑目标测试、相邻回归、全量回归、命令行 smoke、源码桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 无参数 `/preference-apply-status` 行为与 v152 保持一致。
- `/preference-apply-status knowledge` 只展示本地知识库回答附注状态和原因。
- `/preference-apply-status 1 memory` 和 `/preference-apply-status prefapp-... memory` 可解释指定确认记录的长期记忆兜底回答附注状态。
- `/preference-apply-status 普通回复` 可解释最近确认记录的普通回复上下文状态。
- 未知输出面返回“状态输出面必须是 reply、knowledge 或 memory”。
- 新增过滤不写入配置、不修改确认记录、不影响撤销、不进入 LLM 白名单。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.148.0`。
