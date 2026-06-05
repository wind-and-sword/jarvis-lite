# v140：偏好显式启用与停用第一阶段实施计划

> 日期：2026-06-05
> 执行者：Codex
> 说明：本文承接 v139 偏好确认固化与撤销第一阶段，把已保存偏好推进到可查看、可显式启用和可显式停用的本地可审计状态。

## 目标

- `config/preferences.local.json` 中的偏好记录增加 `enabled` 状态；缺失该字段的旧记录按未启用读取。
- `/preference-status` 只读展示本地偏好总数、已启用数量、未启用数量和编号列表。
- `/preference-enable 编号` 支持按状态列表编号启用已保存偏好。
- `/preference-disable 编号` 支持按状态列表编号停用已保存偏好。
- `/config-manager-status` 继续展示偏好数量，并提示 `/preference-status` 管理入口。

## 非目标

- 不让启用偏好自动改变当前对话风格、LLM prompt、命令路由或执行决策。
- 不把 `/preference-status`、`/preference-enable` 或 `/preference-disable` 加入 LLM 白名单。
- 不从普通聊天或外脑 fallback 自动启用、停用或应用偏好。
- 不点击、不输入、不切换窗口、不启动应用。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：偏好默认未启用，可按编号启用和停用，状态展示包含数量与边界说明。
2. 在 `tests/test_agent.py` 增加 RED：Agent 接入 `/preference-status`、`/preference-enable 编号`、`/preference-disable 编号`、参数校验和帮助/status 文案。
3. 在 `tests/test_memory_config_manager.py` 增加 RED：配置管家提示 `/preference-status`。
4. 在 `tests/test_llm.py` 增加 RED：偏好启停命令不进入真实 provider instructions。
5. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.135.0`。
6. 扩展 `preferences.py`，增加 `enabled` 字段、状态摘要、按编号启用/停用 helper，旧记录缺失字段时按 `false` 处理。
7. 更新 `JarvisAgent` 命令分发、帮助和状态文案，保持所有偏好命令只通过显式 slash command 执行。
8. 更新配置管家、版本号、README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
9. 执行目标测试、相邻回归、全量 unittest、命令行 smoke、源码桌面 smoke、安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 偏好候选确认后在 `/preference-status` 中显示为 `未启用`。
- `/preference-enable 1` 把该偏好标记为 `已启用`，再次 `/preference-status` 显示已启用数量为 1。
- `/preference-disable 1` 把该偏好标记为 `未启用`，状态列表保留偏好文本。
- 启用或停用偏好只改变 `preferences.local.json` 的 `enabled` 字段，不改变当前回复、LLM prompt、路由或执行决策。
- 真实 provider instructions 不包含偏好启停命令。
