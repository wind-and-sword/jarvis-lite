# v137 应用别名确认固化与撤销第一阶段计划

> 日期：2026-06-04
> 执行者：Codex

## 目标

- 让 `app_alias` 运行态候选可通过 `/config-candidate-confirm 编号` 显式写入 `config/apps.local.json`。
- 让历史中的已固化 `app_alias` 候选可通过 `/config-candidate-undo 编号` 删除对应别名并恢复为活跃候选。
- 继续保持显式命令边界：不启动应用、不切换窗口、不点击、不输入，不加入 LLM 白名单。

## 实施步骤

1. 在 `tests/test_app_registry.py` 增加 RED：应用别名候选解析、保存、匹配和删除。
2. 在 `tests/test_memory_config_candidates.py` 增加 RED：`app_alias` 确认写入、历史展示、撤销删除和恢复活跃。
3. 在 `tests/test_agent.py` 增加 RED：Agent 通过确认命令固化应用别名，`/app-find` 能命中新别名，撤销后不再命中。
4. 更新 `tests/test_project_metadata.py` 和 update manifest 夹具版本到 `0.132.0`/`0.132.1`。
5. 在 `src/jarvis_lite/app_registry.py` 增加应用别名解析、保存和删除 helper，复用现有 `apps.local.json` schema。
6. 更新 `src/jarvis_lite/memory_config_candidates.py`，让 confirm/undo 支持 `contact_alias` 与 `app_alias` 两类高风险候选。
7. 同步版本、README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
8. 执行目标测试、相邻回归、全量 unittest、smoke、打包和静态检查。

## 验收

- `/config-candidate-add app_alias 我的浏览器 => chrome` 后，`/config-candidate-confirm 1` 写入 `config/apps.local.json`。
- `/app-find 我的浏览器` 命中 Chrome，但确认阶段本身不启动 Chrome。
- `/config-candidate-undo 1` 删除 `我的浏览器` 别名并恢复候选为活跃。
- 撤销别名时不删除已有应用 path 覆盖。
