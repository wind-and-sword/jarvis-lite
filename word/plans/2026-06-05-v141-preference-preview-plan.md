# v141：偏好应用预览第一阶段实施计划

> 日期：2026-06-05
> 执行者：Codex
> 说明：本文承接 v140 偏好显式启用与停用第一阶段，把已启用偏好推进到显式预览入口，但仍不自动改变回复、LLM prompt、路由或执行决策。

## 目标

- 新增 `/preference-preview [输入文本]`，只读展示当前已启用偏好和偏好应用草案。
- 无输入文本时展示通用预览；有输入文本时展示 `预览输入：...`，便于用户审计某次输入如果未来应用偏好会参考哪些条目。
- 配置管家、`/help` 和 `/status` 增加偏好预览入口提示。
- 版本提升到 `0.136.0` 并生成可安装测试包。

## 非目标

- 不把已启用偏好自动加入普通回答、LLM prompt、SearchRouter、InnerBrain 或命令路由。
- 不把 `/preference-preview` 加入 LLM provider 白名单。
- 不新增自然语言自动映射，不从普通聊天自动启用、停用或应用偏好。
- 不设计偏好冲突解析或优先级排序；本阶段只按保存顺序展示已启用偏好。

## 实施步骤

1. 在 `tests/test_preferences.py` 增加 RED：`describe_preference_preview()` 展示已启用偏好、忽略未启用偏好、无启用偏好时提示先启用。
2. 在 `tests/test_agent.py` 增加 RED：Agent 接入 `/preference-preview [输入文本]`、参数自由文本、帮助/status 文案和配置管家入口。
3. 在 `tests/test_memory_config_manager.py` 增加 RED：配置管家提示 `/preference-preview`。
4. 在 `tests/test_llm.py` 增加 RED：`/preference-preview` 不进入 provider instructions。
5. 在 `tests/test_project_metadata.py` 增加 RED：版本提升到 `0.136.0`。
6. 在 `preferences.py` 实现启用偏好读取和预览描述 helper。
7. 在 `agent.py`、`memory_config_manager.py` 接入显式命令与入口文案。
8. 同步 README、PROJECT-PLAN、计划索引、文档索引、进度和验证记录。
9. 跑目标测试、相邻回归、全量回归、命令行 smoke、桌面 smoke、Windows 安装包构建、打包后 smoke 和静态检查。

## 验收标准

- 偏好确认后默认未启用，`/preference-preview` 提示暂无已启用偏好。
- `/preference-enable 1` 后，`/preference-preview 帮我总结知识库` 展示 `预览输入：帮我总结知识库` 和已启用偏好列表。
- 预览输出明确说明当前不会自动改变回复风格、LLM prompt、路由或执行决策。
- LLM provider instructions 不包含 `/preference-preview`。
- 本地测试、smoke、打包和静态检查通过，安装包版本资源为 `0.136.0`。
